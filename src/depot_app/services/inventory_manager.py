from sqlalchemy.orm import Session
from sqlalchemy import select
from prometheus_client import Counter, Gauge
from src.depot_app.models.inventory import InventoryItem

# ==========================================
# 📊 SERVICE TELEMETRY INSTRUMENTATION
# ==========================================
LOW_STOCK_ALERT_GAUGE = Gauge(
    "depot_low_stock_items_total", 
    "Total number of inventory items currently sitting below their safe threshold"
)
STOCK_TRANSACTION_COUNTER = Counter(
    "depot_stock_transactions_total", 
    "Total count of stock volume alterations", 
    ["operation_type"]
)

class InventoryService:
    """
    Handles core business operations regarding stock alterations, tracking limits, 
    and transaction telemetry metrics inside the Depot Repository.
    """
    
    @staticmethod
    def get_all_items(db: Session) -> list[InventoryItem]:
        """Fetches all inventory assets currently tracked in the database."""
        stmt = select(InventoryItem)
        return list(db.scalars(stmt).all())

    @staticmethod
    def create_item(db: Session, sku: str, name: str, category: str, quantity: int, min_stock_level: int, unit_price: float, wholesale_cost: float, supplier_id: int = None) -> InventoryItem:
        """Creates a new unique SKU asset row in the repository database."""
        new_item = InventoryItem(
            sku=sku, name=name, category=category, quantity=quantity,
            min_stock_level=min_stock_level, unit_price=unit_price,
            wholesale_cost=wholesale_cost, supplier_id=supplier_id
        )
        db.add(new_item)
        db.commit()
        db.refresh(new_item)
        
        STOCK_TRANSACTION_COUNTER.labels(operation_type="sku_creation").inc()
        InventoryService.update_low_stock_metrics(db)
        return new_item

    @staticmethod
    def adjust_stock(db: Session, item_id: int, volume_delta: int) -> InventoryItem | None:
        """
        Adjusts warehouse item volume dynamically. Supports positive integers 
        for shipments received or negative integers for sales fulfillments.
        """
        item = db.get(InventoryItem, item_id)
        if not item:
            return None
            
        item.quantity += volume_delta
        db.commit()
        db.refresh(item)
        
        # Track metrics telemetry
        op_label = "inbound_restock" if volume_delta > 0 else "outbound_sale"
        STOCK_TRANSACTION_COUNTER.labels(operation_type=op_label).inc()
        InventoryService.update_low_stock_metrics(db)
        
        return item

    @staticmethod
    def get_critical_low_stock(db: Session) -> list[InventoryItem]:
        """Returns all warehouse stock entries operating below their assigned safe minimum levels."""
        stmt = select(InventoryItem).where(InventoryItem.quantity <= InventoryItem.min_stock_level)
        items = list(db.scalars(stmt).all())
        return items

    @staticmethod
    def update_low_stock_metrics(db: Session) -> None:
        """Synchronizes the operational Prometheus tracking state gauge with active database metrics."""
        low_stock_count = len(InventoryService.get_critical_low_stock(db))
        LOW_STOCK_ALERT_GAUGE.set(low_stock_count)

