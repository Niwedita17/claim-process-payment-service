# Start with Python 3.10 slim-buster image
FROM python:3.10-slim-buster

# Create and set the working directory
WORKDIR /app

# Copy the requirements.txt file into the container and install the dependencies
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Expose the port that the application will be running on
EXPOSE 8000

# Start the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
