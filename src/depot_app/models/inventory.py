from datetime import datetime
from sqlalchemy import Integer, String, Numeric, DateTime, func, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from src.depot_app.core.database import Base

class InventoryItem(Base):
    """
    SQLAlchemy Model representing wholesale products tracked within 
    the Restaurant Depot inventory system.
    """
    __tablename__ = "inventory_items"

    # Core Database Identifiers
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    sku: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    category: Mapped[str] = mapped_column(String(100), nullable=False)
    
    # Stock Metrics & Capacity Tracking
    quantity: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    min_stock_level: Mapped[int] = mapped_column(Integer, default=10, nullable=False)
    
    # Financial Analytics (Using Numeric to prevent floating point inaccuracies)
    unit_price: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    wholesale_cost: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    
    # ✅ CORRECT POSITION: Links to the 'id' column inside the 'suppliers' database table
    supplier_id: Mapped[int] = mapped_column(Integer, ForeignKey("suppliers.id"), nullable=True)
    
    # Metadata Audit Trails
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())

    def __repr__(self) -> str:
        return f"<InventoryItem(sku='{self.sku}', name='{self.name}', qty={self.quantity})>"
