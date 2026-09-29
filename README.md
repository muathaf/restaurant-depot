# 🏪 Restaurant Depot Application

A containerized, production-ready internal inventory management application built using Python and Streamlit. This repository features robust data persistence, live health instrumentation, and real-time infrastructure performance visualization.

---

## 🛠️ Tech Stack & Architecture

- **Frontend/UI:** [Streamlit](https://streamlit.io) (Pure Python operational dashboards)
- **Database Layer:** [MySQL 8.0](https://mysql.com) (Relational schema for inventory tracking)
- **Observability Stack:** 
  - [Prometheus](https://prometheus.io) (Scraping custom engine & database metrics)
  - [Grafana](https://grafana.com) (Visual health & query load monitoring panels)
- **Containerization:** [Docker Engine](https://docker.com) & Docker Compose

---

## 📂 Repository Structure

```text
restaurant_depot/
├── docker-compose.yml       # Orchestrates Streamlit, MySQL, Prometheus, and Grafana
├── requirements.txt         # Explicit list of application and monitoring dependencies
├── README.md                # Project documentation
│
├── config/                  # Monitoring configuration files
│   ├── prometheus.yml       # Defines targets and scraping frequencies
│   └── grafana/             # Optional: Pre-configured datasource provisioning configs
│
└── src/                     # Main source code directory
    └── depot_app/
        ├── main.py          # Streamlit UI entry point and app loops
        ├── core/            # Database initialization and telemetry middleware
        ├── models/          # SQLAlchemy schemas (inventory, suppliers, orders)
        └── services/        # Business logic & metrics registration
```

## 🚀 Quick Start (Local Setup)

### 1. Configure Local Environment
Create a `.env` file in the root directory to hold database credentials:
```env
MYSQL_ROOT_PASSWORD=your_secure_root_password
MYSQL_DATABASE=depot_db
MYSQL_USER=depot_admin
MYSQL_PASSWORD=your_secure_password
```

### 2. Spin Up Ecosystem via Docker
Launch all interconnected services simultaneously using docker-compose:
```bash
docker-compose up --build -d
```

### 3. Accessible Port mappings
Once the cluster spins up successfully, you can view the individual systems at:
- **Streamlit Application Layer:** `http://localhost:8501`
- **Prometheus Telemetry Dashboard:** `http://localhost:9090`
- **Grafana Visualization Hub:** `http://localhost:3000`

---

## 📊 Telemetry & Metrics Tracked
The system exposes an internal metrics endpoint (`/metrics`) using the Python Prometheus Client to track:
- Total active restaurant sessions.
- High-latency MySQL transaction requests.
- Low-stock warnings and stock exhaustion rates.
