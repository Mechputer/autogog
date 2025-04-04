from flask import Flask, send_file, request, jsonify
import requests
import logging
import json

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)

app.logger.addHandler(logging.StreamHandler())
app.logger.setLevel(logging.DEBUG)

# Example usage for a log
app.logger.debug("Starting Flask App")

# Map container names to their internal API endpoints
CONTAINER_APIS = {
    "input": "http://input:5000/v1/completions",
    "reflection": "http://reflection:5000/v1/completions",
    "ethics": "http://ethics:5000/v1/completions"
}

@app.route("/")
def index():
    # Serve the HTML interface
    return send_file("index.html")

@app.route("/v1/completions", methods=["POST"])
def completions():
    data = request.json
    app.logger.debug(f"Received data: {data}")  # Log the incoming payload

    # Get the selected container and user inputs
    container = data.get("container")
    user_input = data.get("prompt")

    # Convert numeric fields to proper types
    max_tokens = int(data.get("max_tokens", 150)) # Default to 150 if missing
    temperature = float(data.get("temperature", 0.7)) # Default to 0.7 if missing
    top_p = float(data.get("top_p", 0.9)) # Default to 0.9 if missing

    # Validate required fields
    if not container or container not in CONTAINER_APIS:
        app.logger.debug(f"Invalid container: {container}")
        return jsonify({"error": "Invalid or missing container"}), 400

    if not user_input:
        app.logger.debug(f"Missing prompt: {user_input}")
        return jsonify({"error": "The 'prompt' field is required"}), 400

    # Forward the request to the selected container
    container_url = CONTAINER_APIS[container]
    app.logger.debug(f"Forwarding to Container: {container_url}")

    try:
        response = requests.post(container_url, json={
            "prompt": user_input,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "top_p": top_p
        })

        app.logger.debug(f"Container Response (raw): {response.status_code} - {response.text}")
        return jsonify(response.json())
    except requests.exceptions.RequestException as e:
        app.logger.debug(f"Error Forwarding to Container: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
