ENV_FILE=".env"

# Create .env file if it doesn't exist
if [ ! -f "$ENV_FILE" ]; then
    echo "Creating $ENV_FILE..."
    cp sample.env .env
fi

docker run --rm --network app-network -v "$(pwd):/app" python:3.11 sh -c "cd /app && pip install -r requirements.txt && python3 generate_data.py && python3 populate_index.py"
