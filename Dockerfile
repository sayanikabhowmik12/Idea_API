FROM python:3.8.1

# Set the working directory in the container
WORKDIR /app

# Copy the application files into the working directory
COPY . /app

# Install the application dependencies
RUN pip install -r requirements.txt

# Expose a TCP port
EXPOSE 8000

# Define the entry point for the container
CMD uvicorn main:app --host 0.0.0.0 --port 8000