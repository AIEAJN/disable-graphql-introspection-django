FROM python:alpine

# Upgrade pip
RUN python -m pip install --upgrade pip
WORKDIR /app
COPY pyproject.toml ./

# Install dependencies
RUN pip install poetry \
    && poetry install --only main

# Copy the project in docker c
COPY . .

# Set permissions to entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# Define the entrypoint
ENTRYPOINT ["/app/entrypoint.sh"]

 

