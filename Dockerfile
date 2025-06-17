# This Dockerfile sets up a Python environment for a web application.
FROM python:3.11

# Establish the working directory
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY requirements.txt /app/

# Install the required Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . /app/

# Expose the port the app runs on
EXPOSE 8081

# Command to run the application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]