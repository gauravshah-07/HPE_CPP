# Use an official Python runtime as a parent image
FROM python:3.9

# Set the working directory inside the container
WORKDIR /app

# Copy all the files to the container
COPY . /app

# Install required Python packages
RUN pip install confluent-kafka

# Expose the Kafka port (if needed)
EXPOSE 9092

# Run the menu script
CMD ["python", "Run.py"]
