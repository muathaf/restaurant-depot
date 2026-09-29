import streamlit as st
from src.depot_app.core.database import get_db
from src.depot_app.services.inventory_manager import InventoryService
from src.depot_app.views.dashboard_view import DashboardView
from src.depot_app.views.ledger_view import LedgerView
from src.depot_app.views.forms_view import FormsView

class InventoryController:
    """
    Coordinates data bindings between the InventoryService (Model Layer) 
    and the Streamlit Inventory Interfaces (View Layer).
    """

    @staticmethod
    def handle_index_view():
        # Open database handle instance cleanly
        db = next(get_db())

        try:
            # 1. MODEL DATA EXTRACTION: Fetch data layers from backend service layers
            all_items = InventoryService.get_all_items(db)
            low_stock_items = InventoryService.get_critical_low_stock(db)
            InventoryService.update_low_stock_metrics(db)

            # 2. VIEW PRESENTATION: Route extracted records out to presentation renderers
            DashboardView.render_metrics(all_items, low_stock_items)
            st.markdown("---")
            
            LedgerView.render_table(all_items)
            st.markdown("---")

            # 3. INTERACTION HANDLING: Render input view targets and intercept postback signals
            restock_data, sku_data = FormsView.render_action_panels(all_items)

            # Process inbound restock postback events
            if restock_data["submitted"]:
                InventoryService.adjust_stock(db, restock_data["item_id"], restock_data["volume"])
                st.toast(f"Success: Added stock volume layers into database mappings!")
                st.rerun()

            # Process brand new SKU registration postback events
            if sku_data["submitted"]:
                try:
                    InventoryService.create_item(
                        db=db, sku=sku_data["sku"], name=sku_data["name"], category=sku_data["category"],
                        quantity=sku_data["qty"], min_stock_level=sku_data["buffer"],
                        unit_price=sku_data["price"], wholesale_cost=sku_data["cost"]
                    )
                    st.success(f"Success: Product catalog registration mapped safely into MySQL tables!")
                    st.rerun()
                except Exception as err:
                    st.error(f"Data Integrity Error encountered on persist routines: {err}")

        finally:
            db.close() # Safely recycle socket pipelines back to engine pool mappings
