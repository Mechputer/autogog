from flask import Flask, request, jsonify
from transformers import AutoTokenizer, AutoModelForCausalLM
import traceback
import logging
import json

logging.basicConfig(level=logging.DEBUG)

# Initialize Flask app
app = Flask(__name__)

app.logger.addHandler(logging.StreamHandler())
app.logger.setLevel(logging.DEBUG)

# Example usage for a log
app.logger.debug("Starting Flask App")

# Load the model and tokenizer
model_path = "./"
tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModelForCausalLM.from_pretrained(model_path)

# Fix pad_token_id warning
model.config.pad_token_id = model.config.eos_token_id

@app.route('/v1/completions', methods=['POST'])
def completions():
    try:
        # Parse JSON payload
        data = request.json
        app.logger.debug(f"Received Payload: {data}")  # Log the received payload for debugging

        # Required fields
        if not data:
            return jsonify({"error": "No JSON payload received"}), 400

        if "prompt" not in data or not data["prompt"]:
            return jsonify({"error": "The 'prompt' field is required"}), 400

        prompt = data["prompt"]
        max_tokens = data.get("max_tokens", 150)  # Defaults to 150
        temperature = data.get("temperature", 0.7)  # Defaults to 0.7
        top_p = data.get("top_p", 0.9)  # Defaults to 0.9
        top_k = data.get("top_k", 50)  # Defaults to 50
        repetition_penalty = data.get("repetition_penalty", 1.2)  # Defaults to 1.2
        stop = data.get("stop", None)  # Optional stop sequences

        app.logger.debug(f"Generating response with: {data}")

        # Tokenize input with attention mask
        inputs = tokenizer(
            prompt,
            return_tensors="pt",
            truncation=True,
            padding=True,
            max_length=1024
        )

        # Generate response
        outputs = model.generate(
            inputs['input_ids'],
            attention_mask=inputs['attention_mask'],
            max_new_tokens=max_tokens,
            temperature=temperature,
            top_p=top_p,
            top_k=top_k,
            repetition_penalty=repetition_penalty
        )

        # Decode model output
        generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
        app.logger.debug(f"Raw Generated Text: {generated_text}")

        # If the generated text starts with the prompt, remove it to extract only the answer.
        if generated_text.startswith(prompt):
            answer_text = generated_text[len(prompt):].strip()
        else:
            answer_text = generated_text

        # Stop sequences handling
        if stop:
            for sequence in stop:
                if sequence in generated_text:
                    answer_text = answer_text.split(sequence)[0].strip()
                    break

        app.logger.debug(f"Final Answer Text: {answer_text}")

        # Return the processed answer text in the expected format.
        return jsonify({"choices": [{"prompt": answer_text}]})

    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
