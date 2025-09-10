FROM python:3.12.7-slim

WORKDIR /frontend_app

COPY . /frontend_app/

# Requirements to run plotly dash app
RUN pip install --no-cache-dir -r /frontend_app/requirements.txt

# Expose port
EXPOSE 8050

# Run app
CMD ["gunicorn", "--bind", "0.0.0.0:8050", "--workers", "4", "app:server"]
