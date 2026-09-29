import streamlit as st

class DashboardView:
    """Pure Presentation View responsible for rendering high level structural KPI blocks."""
    
    @staticmethod
    def render_metrics(all_items: list, low_stock_items: list):
        st.title("📊 Warehouse Operational Diagnostics")
        
        total_skus = len(all_items)
        total_valuation = sum(float(item.quantity) * float(item.unit_price) for item in all_items)
        critical_alerts = len(low_stock_items)

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Active SKUs", total_skus)
        with col2:
            st.metric("Total Asset Value", f"\${total_valuation:,.2f}")
        with col3:
            st.metric(
                "Critical Low Stock Alerts", 
                critical_alerts, 
                delta=-critical_alerts if critical_alerts > 0 else 0, 
                delta_color="inverse"
            )
