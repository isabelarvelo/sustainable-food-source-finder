FROM python:3.9-slim

WORKDIR /ds5760/python

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker cache
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Create directory for logs and notebooks
RUN mkdir -p /ds5760/python/logs /ds5760/python/notebooks

# Set up Jupyter configuration
RUN python -m jupyter notebook --generate-config
RUN echo "c.NotebookApp.allow_origin = '*'" >> /root/.jupyter/jupyter_notebook_config.py
RUN echo "c.NotebookApp.ip = '0.0.0.0'" >> /root/.jupyter/jupyter_notebook_config.py
