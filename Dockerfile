# Use an official Python 3.8.10 runtime as a parent image
FROM python:3.8.10-slim-buster

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install any dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code into the container
COPY . .

# Expose the port that the application runs on
EXPOSE 8000

# Set environment variables (if needed) - consider using .env file
# ENV AIPROXY_TOKEN=your_default_token  #It's better to pass this at runtime

# Command to run the application
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]