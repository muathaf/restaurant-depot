import streamlit as st
import pandas as pd

class SupplierView:
    """Pure Presentation View responsible for rendering supplier lists and forms."""

    @staticmethod
    def render_supplier_page(all_suppliers: list) -> dict:
        st.title("🚚 Supplier Directory Control Tower")
        st.markdown("---")

        # Layout Columns: Data Display Left, Intake Form Right
        grid_col, form_col = st.columns([2, 1])
        form_payload = {"submitted": False}

        with grid_col:
            st.subheader("📋 Registered Food & Beverage Distributors")
            if not all_suppliers:
                st.info("💡 No supplier profiles found. Register your first wholesale distribution partner using the form panel.")
            else:
                # Serialize objects safely for DataFrame rendering
                serialized_suppliers = [
                    {
                        "ID": vendor.id,
                        "Distributor Name": vendor.name,
                        "Point of Contact": vendor.contact_name or "N/A",
                        "Email Address": vendor.email or "N/A",
                        "Phone Connection": vendor.phone or "N/A"
                    }
                    for vendor in all_suppliers
                ]
                st.dataframe(pd.DataFrame(serialized_suppliers), use_container_width=True, hide_index=True)

        with form_col:
            st.subheader("🆕 Register New Vendor")
            with st.form("supplier_intake_form", clear_on_submit=True):
                v_name = st.text_input("Wholesale Distributor Name *")
                v_poc = st.text_input("Point of Contact Name")
                v_email = st.text_input("Corporate Email Address")
                v_phone = st.text_input("Support Phone Number")
                
                submit_button = st.form_submit_button("Provision Vendor Account", use_container_width=True)
                
                if submit_button:
                    if not v_name.strip():
                        st.error("Validation Error: Distributor Name is a mandatory field.")
                    else:
                        form_payload = {
                            "submitted": True,
                            "name": v_name.strip(),
                            "contact": v_poc.strip() or None,
                            "email": v_email.strip() or None,
                            "phone": v_phone.strip() or None
                        }

        return form_payload
