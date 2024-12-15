FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy the project files into the container
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 80 for the app
EXPOSE 80

# Command to run the app
CMD ["uvicorn", "distilbert_finetuned:app", "--host", "0.0.0.0", "--port", "80"]
