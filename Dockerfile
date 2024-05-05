# Use an official Python runtime as a parent image
FROM python:3.12.2-alpine3.19

# Install system packages required for building matplotlib
RUN apk --no-cache add build-base zlib-dev libpng-dev freetype-dev

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy just the requirements file first to leverage Docker cache
COPY app/requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Create a non-root user
RUN adduser --disabled-password --gecos '' dashboard

# Set the ownership of the working directory to the non-root user
RUN chown -R dashboard:dashboard /usr/src/app

# Switch to the non-root user
USER dashboard

# Copy the entire app folder into the container
COPY app .

# Make port 8080 available to the world outside this container
EXPOSE 8080

# Set the default command to run when the container starts
ENTRYPOINT ["python", "dash_app.py"]
