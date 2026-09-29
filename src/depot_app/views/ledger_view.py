import streamlit as st
import pandas as pd

class LedgerView:
    """Pure Presentation View responsible for rendering central tracking data grids."""

    @staticmethod
    def render_table(all_items: list):
        st.subheader("📋 Core Stock Inventory Ledger")

        if not all_items:
            st.info("💡 The repository database is currently empty. Initialize product codes below to start tracking.")
            return

        # Transform raw object streams into interface-friendly structures
        serialized_data = [
            {
                "Database ID": item.id,
                "SKU Code": item.sku,
                "Product Name": item.name,
                "Category Group": item.category,
                "Current Stock Volume": item.quantity,
                "Minimum Buffer Alert": item.min_stock_level,
                "Wholesale Cost (\$)": float(item.wholesale_cost),
                "Selling Unit Price (\$)": float(item.unit_price)
            }
            for item in all_items
        ]
        
        inventory_dataframe = pd.DataFrame(serialized_data)
        
        # Render a read-only table view to the user
        st.dataframe(inventory_dataframe, use_container_width=True, hide_index=True)
