# For our purposes, using an official Python runtime for the parent image.
FROM python:3.8-slim

# Set the working directory to /apps
WORKDIR /apps

# Install any needed packages specified in requirements.txt with python package index
COPY requirements.txt .
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Copy the current directory contents into the container at /apps after copying source code
COPY . /apps

# Make port 8080 available to the world outside this container
EXPOSE 8080

# Define environment variable
ENV NAME World

# Run app.py when the container launches
CMD ["python", "app.py"]