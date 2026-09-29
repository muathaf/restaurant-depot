FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501
EXPOSE 8000

# 🧬 FIXED: Explicitly forces Python to look at the root directory level for your 'src' package mapping chains
CMD ["python", "-m", "streamlit", "run", "src/depot_app/main.py", "--server.port=8501", "--server.address=0.0.0.0"]
