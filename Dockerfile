FROM python:3.9-alpine

# Install build dependencies (optional, if needed for your app)
RUN apk add --no-cache gcc musl-dev

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install the dependencies from the requirements file
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 5000 to allow access to the container
EXPOSE 8000

# Run the application
CMD ["python", "app.py"]
