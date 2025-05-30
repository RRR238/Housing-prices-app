# Use official python image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy backend and dashboard requirements
COPY backend/requirements.txt ./backend_requirements.txt
COPY housing_prices_dashboard/requirements.txt ./dashboard_requirements.txt

# Install both sets of dependencies
RUN pip install --no-cache-dir -r backend_requirements.txt -r dashboard_requirements.txt

# Copy backend code
COPY backend ./backend

# Copy necessary dashboard files
COPY housing_prices_dashboard/model.joblib ./housing_prices_dashboard/model.joblib
COPY housing_prices_dashboard/main.py ./housing_prices_dashboard/main.py

# Set environment variables
ENV MODEL_PATH=/app/housing_prices_dashboard/model.joblib \
    HOST=0.0.0.0 \
    PORT=5000 \
    DATABASE_URL=sqlite:///./users.db \
    DATA_PATH=/app/housing_prices_dashboard/housing.csv \
    SECRET_KEY=SuperSecretKey \
    ALGORITHM=HS256 \
    ISSUER=http://127.0.0.1:5000 \
    AUDIENCE=FastAPI

# Add backend and dashboard folders to PYTHONPATH
ENV PYTHONPATH=/app/backend:/app/housing_prices_dashboard

# Expose app port
EXPOSE 5000

# Default command
CMD ["python", "backend/api.py"]
