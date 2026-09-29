import streamlit as st

class FormsView:
    """Pure Presentation View responsible for structuring stock entry interactive panels."""

    @staticmethod
    def render_action_panels(all_items: list) -> tuple[dict, dict]:
        st.subheader("🛠️ Distribution Operations Controls")
        form_col1, form_col2 = st.columns(2)

        # Default dictionary responses returned to the Controller layer
        restock_payload = {"submitted": False}
        sku_payload = {"submitted": False}

        # Panel A: Inbound Bulk Shipments Form Interface
        with form_col1:
            st.markdown("### 📥 Log Inbound Shipment (Restock)")
            if not all_items:
                st.caption("A minimum of 1 active SKU item is required before receiving cargo logs.")
            else:
                item_options = {item.name: item.id for item in all_items}
                selected_name = st.selectbox("Select Target Warehouse Item", options=list(item_options.keys()))
                added_volume = st.number_input("Inbound Case Volume", min_value=1, value=50, step=5)
                
                if st.button("Commit Restock to Database", use_container_width=True):
                    restock_payload = {
                        "submitted": True,
                        "item_id": item_options[selected_name],
                        "volume": added_volume
                    }

        # Panel B: Provision New Structural SKU Items Code Layout
        with form_col2:
            st.markdown("### 🆕 Catalog New Bulk Product (SKU)")
            with st.form("new_sku_form", clear_on_submit=True):
                new_sku = st.text_input("Unique SKU Code (e.g., MILK-10L-BULK)")
                new_name = st.text_input("Descriptive Product Name")
                new_category = st.selectbox("Category Classification", ["Dairy", "Dry Goods", "Oils", "Meat & Poultry", "Disposables"])
                
                input_col1, input_col2 = st.columns(2)
                with input_col1:
                    initial_qty = st.number_input("Initial Quantity", min_value=0, value=100)
                    wholesale_cost = st.number_input("Wholesale Unit Cost (\$)", min_value=0.01, value=10.00, step=0.50)
                with input_col2:
                    min_buffer = st.number_input("Safe Minimum Buffer Alert Level", min_value=1, value=15)
                    retail_price = st.number_input("Selling Unit Price (\$)", min_value=0.01, value=15.99, step=0.50)
                    
                submit_sku = st.form_submit_button("Provision Product to Ledger", use_container_width=True)
                
                if submit_sku:
                    if not new_sku.strip() or not new_name.strip():
                        st.error("Validation Error: Both unique SKU code and descriptive product name fields are mandatory.")
                    else:
                        sku_payload = {
                            "submitted": True,
                            "sku": new_sku.strip().upper(),
                            "name": new_name.strip(),
                            "category": new_category,
                            "qty": initial_qty,
                            "buffer": min_buffer,
                            "cost": wholesale_cost,
                            "price": retail_price
                        }

        return restock_payload, sku_payload
