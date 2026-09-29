from sqlalchemy.orm import Session
from sqlalchemy import select
from src.depot_app.models.supplier import Supplier

class SupplierService:
    """Handles operational queries and transaction logic for database vendors."""
    
    @staticmethod
    def get_all_suppliers(db: Session) -> list[Supplier]:
        """Fetches all restaurant vendors currently on record inside MySQL."""
        stmt = select(Supplier).order_by(Supplier.name)
        return list(db.scalars(stmt).all())

    @staticmethod
    def create_supplier(db: Session, name: str, contact_name: str = None, email: str = None, phone: str = None) -> Supplier:
        """Provisions a brand new distributor entry to the database mapping grids."""
        new_supplier = Supplier(
            name=name.strip(), contact_name=contact_name, email=email, phone=phone
        )
        db.add(new_supplier)
        db.commit()
        db.refresh(new_supplier)
        return new_supplier

