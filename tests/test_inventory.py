import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from prometheus_client import REGISTRY

# Clean, standard absolute package imports
from src.depot_app.core.database import Base
from src.depot_app.services.inventory_manager import InventoryService

# ==========================================
# 🧱 ISOLATED ENGINE FIXTURE SETUPS
# ==========================================
@pytest.fixture(name="db_session")
def fixture_db_session():
    """
    Creates an isolated, in-memory SQLite database context for each individual 
    test function loop. Automatically handles teardowns on completion.
    """
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    Base.metadata.create_all(engine)
    
    SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
    session = SessionLocal()
    
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(engine)

# ==========================================
# 🎯 CORE BACKEND VALIDATION TESTS
# ==========================================

def test_create_inventory_item_persists_correctly(db_session):
    """Verifies that creating a new SKU safely saves all metadata attributes to the database."""
    new_item = InventoryService.create_item(
        db=db_session, sku="TEST-MILK-01", name="Organic Milk 1 Gallon",
        category="Dairy", quantity=50, min_stock_level=10,
        unit_price=5.99, wholesale_cost=3.50
    )
    
    assert new_item.id is not None
    assert new_item.sku == "TEST-MILK-01"
    assert new_item.quantity == 50
    
    all_items = InventoryService.get_all_items(db_session)
    assert len(all_items) == 1
    assert all_items[0].name == "Organic Milk 1 Gallon"


def test_adjust_stock_increases_and_decreases_volumes(db_session):
    """Validates that receiving shipments and processing sales dynamically mutates stock sizes."""
    item = InventoryService.create_item(
        db=db_session, sku="RICE-20KG", name="Basmati Rice Bag",
        category="Dry Goods", quantity=20, min_stock_level=5,
        unit_price=25.00, wholesale_cost=15.00
    )
    
    updated_inbound = InventoryService.adjust_stock(db_session, item.id, 15)
    assert updated_inbound.quantity == 35
    
    updated_outbound = InventoryService.adjust_stock(db_session, item.id, -10)
    assert updated_outbound.quantity == 25


def test_get_critical_low_stock_filters_correct_skus(db_session):
    """Ensures business routing logic accurately identifies running stocks sitting below safety lines."""
    InventoryService.create_item(
        db=db_session, sku="APPLES-BOX", name="Fuji Apples Bulk Box",
        category="Produce", quantity=50, min_stock_level=10,
        unit_price=18.00, wholesale_cost=10.00
    )
    
    InventoryService.create_item(
        db=db_session, sku="OILS-FRYER", name="Canola Frying Oil Jug",
        category="Oils", quantity=3, min_stock_level=15,
        unit_price=42.00, wholesale_cost=30.00
    )
    
    low_stock_alerts = InventoryService.get_critical_low_stock(db_session)
    
    assert len(low_stock_alerts) == 1
    assert low_stock_alerts[0].sku == "OILS-FRYER"


def test_prometheus_telemetry_metrics_increment_on_transactions(db_session):
    """Verifies that executing service actions updates the background telemetry collectors."""
    # 🛑 FIXED: Removed the extra trailing '_total' suffix
    before_count = REGISTRY.get_sample_value('depot_stock_transactions_total', {'operation_type': 'sku_creation'}) or 0.0
    
    InventoryService.create_item(
        db=db_session, sku="TEST-TELEMETRY", name="Telemetry Test SKU",
        category="Disposables", quantity=100, min_stock_level=5,
        unit_price=1.99, wholesale_cost=0.50
    )
    
    # 🛑 FIXED: Removed the extra trailing '_total' suffix
    after_count = REGISTRY.get_sample_value('depot_stock_transactions_total', {'operation_type': 'sku_creation'}) or 0.0
    
    assert after_count == before_count + 1.0
