# Use the official Python image from the Docker Hub
FROM python:3.12.0-slim

# Set environment variable to ignore existing virtual environments
ENV PIPENV_IGNORE_VIRTUALENVS=1

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt to the working directory
COPY requirements.txt /app/

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . /app

# Expose the port Flask runs on
EXPOSE 5000

# Define the command to run the application using gunicorn with app:app
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
