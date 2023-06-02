# Use the official Python base image
FROM python:3.9-slim

# Install system dependencies
RUN apt-get update \
    && apt-get install -y build-essential \
    python3-dev \
    libpcre3 \
    libpcre3-dev

# Set the working directory in the container
WORKDIR /app

# Add non-root user
RUN groupadd -r uwsgi && useradd -r -g uwsgi uwsgi

# Copy all files
COPY . .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port on which the application will run
EXPOSE 3000

# Set the command to run the uWSGI server
CMD ["uwsgi", "--ini", "uwsgi.ini"]