# Python Enivornment
FROM python:3.11-slim

# Establish the workspace directory inside the container
WORKDIR /app

# Ensure the data directory exists for the script's export methods
RUN mkdir -p /app/data

# Copy source scripts directly into the image path
COPY main.py watch.py /app/

# Forces output streams to print instantly to the terminal without buffering
ENV PYTHONUNBUFFERED=1

# Run the automated main execution script on startup
CMD ["python", "main.py"]
