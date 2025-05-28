# Use official python image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy backend requirements and dashboard requirements, install both
COPY backend/requirements.txt ./backend_requirements.txt
COPY housing_prices_dashboard/requirements.txt ./dashboard_requirements.txt

RUN pip install --no-cache-dir -r backend_requirements.txt -r dashboard_requirements.txt

# Copy backend code
COPY backend ./backend

# Copy required files from housing_prices_dashboard
COPY housing_prices_dashboard/model.joblib ./housing_prices_dashboard/model.joblib
COPY housing_prices_dashboard/main.py ./housing_prices_dashboard/main.py

# Set environment variables if needed
ENV PYTHONPATH=/app/backend:/app/housing_prices_dashboard

# Expose port if needed
EXPOSE 5000

# Run your app (adjust as per your actual start command)
CMD ["python", "api.py"]
