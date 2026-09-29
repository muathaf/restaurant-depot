import streamlit as st
from src.depot_app.core.database import get_db
from src.depot_app.services.supplier_manager import SupplierService
from src.depot_app.views.supplier_view import SupplierView

class SupplierController:
    """Coordinates data bindings between the SupplierService Model and SupplierView Layout."""

    @staticmethod
    def handle_supplier_workflow():
        # Open dynamic transactional context
        db = next(get_db())

        try:
            # 1. Fetch current vendor profiles from database layer
            all_suppliers = SupplierService.get_all_suppliers(db)

            # 2. Render UI layout framework and capture interactive signals
            form_data = SupplierView.render_supplier_page(all_suppliers)

            # 3. Handle data transaction requests
            if form_data["submitted"]:
                try:
                    SupplierService.create_supplier(
                        db=db,
                        name=form_data["name"],
                        contact_name=form_data["contact"],
                        email=form_data["email"],
                        phone=form_data["phone"]
                    )
                    st.success(f"Success: '{form_data['name']}' provisioned securely into MySQL database!")
                    st.rerun()
                except Exception as db_err:
                    st.error(f"Data Integrity Error: A vendor profile with that name may already exist. Details: {db_err}")

        finally:
            db.close() # Recycle database socket back to SQLAlchemy context pool
