# Set the python version as a build-time argument with Python 3.12 as the default
ARG PYTHON_VERSION=3.12-slim-bullseye
FROM python:${PYTHON_VERSION}

# Create a virtual environment
RUN python -m venv /opt/venv

# Set the virtual environment as the current location
ENV PATH=/opt/venv/bin:$PATH

# Upgrade pip and install essential OS dependencies
RUN pip install --upgrade pip
RUN apt-get update && apt-get install -y \
    # For PostgreSQL
    libpq-dev \
    # For Pillow
    libjpeg-dev \
    # For CairoSVG
    libcairo2 \
    # Other
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Set Python-related environment variables for better performance
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Create the application directory and set it as the working directory
RUN mkdir -p /code
WORKDIR /code

# Copy only the requirements file to leverage Docker layer caching
COPY requirements.txt /tmp/requirements.txt

# Install Python dependencies
RUN pip install -r /tmp/requirements.txt

# Copy the project code into the container
COPY ./src /code

# Set build-time arguments for environment configuration
ARG DJANGO_SECRET_KEY
ENV DJANGO_SECRET_KEY=${DJANGO_SECRET_KEY}

ARG DJANGO_DEBUG=0
ENV DJANGO_DEBUG=${DJANGO_DEBUG}

# Collect static files during the build stage
RUN python manage.py collectstatic --noinput

# Prepare runtime script to handle database-dependent commands
ARG PROJ_NAME="cfehome"
RUN printf "#!/bin/bash\n" > ./paracord_runner.sh && \
    printf "RUN_PORT=\"\${PORT:-8000}\"\n\n" >> ./paracord_runner.sh && \
    printf "python manage.py migrate --no-input\n" >> ./paracord_runner.sh && \
    printf "python manage.py vendor_pull\n" >> ./paracord_runner.sh && \
    printf "gunicorn ${PROJ_NAME}.wsgi:application --bind \"0.0.0.0:\$RUN_PORT\"\n" >> ./paracord_runner.sh

# Make the runtime script executable
RUN chmod +x paracord_runner.sh

# Clean up apt cache to reduce image size
RUN apt-get remove --purge -y \
    && apt-get autoremove -y \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set the default command to run the runtime script
CMD ./paracord_runner.sh
