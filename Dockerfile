# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements
RUN pip install --no-cache-dir Flask==2.1.1 Flask-SQLAlchemy==2.5.1 SQLAlchemy==1.4.47 Werkzeug==2.0.3 Flask-Migrate

# Set environment variables
ENV FLASK_APP=app.py
ENV FLASK_ENV=development

# Expose port 5000 for the Flask app
EXPOSE 5000

# Run the command to start the Flask app
CMD ["flask", "run", "--host=0.0.0.0"]