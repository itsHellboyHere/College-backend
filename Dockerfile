# Use the Python 3.12 slim image as the base image
ARG PYTHON_VERSION=3.12-slim-bullseye
FROM python:${PYTHON_VERSION}

# Set environment variables to avoid Python bytecode and buffering
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install system dependencies required by Python, Pillow, and PostgreSQL
RUN apt-get update && apt-get install -y \
    libpq-dev \
    libjpeg-dev \
    zlib1g-dev \
    libfreetype6-dev \
    liblcms2-dev \
    libopenjp2-7 \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Create a virtual environment for the project
RUN python -m venv /opt/venv
ENV PATH=/opt/venv/bin:$PATH

# Upgrade pip
RUN pip install --upgrade pip

# Create a directory for the project
RUN mkdir -p /code
WORKDIR /code

# Copy the requirements file into the container
COPY requirements.txt /tmp/requirements.txt

# Install Python dependencies
RUN pip install -r /tmp/requirements.txt

# Copy the entire project code into the container
COPY ./src /code

# Copy .env into the container (optional: adjust path if needed)
COPY .env /code/.env

# Set environment variables for Django
ARG DJANGO_SECRET_KEY
ENV DJANGO_SECRET_KEY=${DJANGO_SECRET_KEY}

ARG DJANGO_DEBUG=0
ENV DJANGO_DEBUG=${DJANGO_DEBUG}



# Collect static files (skip if static files are not configured correctly)
RUN python manage.py collectstatic --noinput || echo "Skipping collectstatic during build."

# Create a startup script for runtime
RUN printf "#!/bin/bash\n" > ./entrypoint.sh && \
    printf "RUN_PORT=\"\${PORT:-8000}\"\n\n" >> ./entrypoint.sh && \
    printf "python manage.py migrate --no-input\n" >> ./entrypoint.sh && \
    printf "gunicorn myproject.wsgi:application --bind \"0.0.0.0:\$RUN_PORT\"\n" >> ./entrypoint.sh

# Make the script executable
RUN chmod +x entrypoint.sh

# Clean up the container image
RUN apt-get autoremove -y && apt-get clean && rm -rf /var/lib/apt/lists/*

# Set the default command to run the project
CMD ./entrypoint.sh
