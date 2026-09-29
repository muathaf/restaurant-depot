import os
import streamlit as st
from src.depot_app.controllers.supplier_controller import SupplierController
from prometheus_client import start_http_server

from src.depot_app.core.database import init_db
from src.depot_app.controllers.inventory_controller import InventoryController

# ==========================================
# ⚙️ GLOBAL INFRASUCTURE CONTROLLER INITIALIZATION
# ==========================================
if "infrastructure_ready" not in st.session_state:
    try:
        start_http_server(8000) # Start Prometheus server
    except Exception:
        pass
    
    try:
        init_db() # Provision MySQL Schemas
        st.session_state.infrastructure_ready = True
    except Exception as db_err:
        st.error(f"❌ Core Infrastructure Initialization Failed: {db_err}")
        st.stop()

# ==========================================
# 🎨 LANDING PAGE LAYOUT CONFIGURATION
# ==========================================
st.set_page_config(page_title="Restaurant Depot Repository", page_icon="🏪", layout="wide")

# Sidebar Landing Menu Navigation
st.sidebar.title("🏪 Depot Navigation")
st.sidebar.markdown("---")
app_mode = st.sidebar.radio(
    "Go To Workspace Menu:",
    ["📊 Dashboard & Inventory", "🚚 Supplier Directory", "📈 System Diagnostics"]
)

db_host = os.getenv("DB_HOST", "localhost")
st.sidebar.markdown("---")
st.sidebar.success(f"🧬 Active Engine Host: `{db_host}`")

# ==========================================
# 🗺️ CONTROLLER ROUTING LOGIC
# ==========================================
if app_mode == "📊 Dashboard & Inventory":
    InventoryController.handle_index_view()

elif app_mode == "🚚 Supplier Directory":
    # Transfer control context entirely to the Supplier Sub-Controller
    SupplierController.handle_supplier_workflow()

elif app_mode == "📈 System Diagnostics":
    st.title("📈 Telemetry & Operational Diagnostics")
    st.markdown("### Active Cluster Links")
    st.write("- **Prometheus Collector Engine:** [http://localhost:9090](http://localhost:9090)")
    st.write("- **Grafana Dashboard Monitor:** [http://localhost:3000](http://localhost:3000)")
