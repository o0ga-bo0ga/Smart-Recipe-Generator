import requests
import os
import base64

# The Qwen2-VL model is hosted on Hugging Face; we just call its API endpoint.
API_URL = "https://api-inference.huggingface.co/models/Qwen/Qwen2-VL-2B-Instruct"

def get_hf_token():
    """Retrieves the Hugging Face API token from environment variables."""
    token = os.environ.get("HUGGING_FACE_TOKEN")
    if not token:
        raise ValueError("HUGGING_FACE_TOKEN environment variable is not set!")
    return token

def allowed_file(filename):
    """Checks if the uploaded file has an allowed extension."""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg'}

def process_image(file, upload_folder):
    """
    Processes an image by sending it to the Hugging Face Inference API
    to identify ingredients with the Qwen2-VL model.
    """
    if not file or not allowed_file(file.filename):
        return []

    try:
        headers = {"Authorization": f"Bearer {get_hf_token()}"}
        
        # Read the image file from the request and encode it in base64
        image_bytes = file.read()
        encoded_image = base64.b64encode(image_bytes).decode('utf-8')

        # This payload is structured specifically for the Qwen2-VL model API
        payload = {
            "inputs": f"<|image_1|>\nList the food ingredients in this image as a comma-separated list.",
            "parameters": {
                "max_new_tokens": 100, # Limit the length of the response
            },
            "images": [encoded_image]
        }
        
        # Make the API call
        response = requests.post(API_URL, headers=headers, json=payload)
        response.raise_for_status() # This will raise an error for bad responses (4xx or 5xx)

        # Parse the JSON response
        result = response.json()
        
        # Extract and clean up the generated text to get a simple list of ingredients
        generated_text = result[0].get('generated_text', '')
        clean_text = generated_text.split("list.")[-1].strip() # Remove the prompt from the output
        ingredients = [ing.strip() for ing in clean_text.split(',') if ing.strip()]
        
        return ingredients

    except requests.exceptions.RequestException as e:
        print(f"API request error: {e}")
        # Handle the common case where the free model is still loading
        if e.response and "is currently loading" in e.response.text:
             return ["The image model is warming up. Please try again in 20 seconds."]
        return ["Error: Could not process the image via API."]
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return ["An unexpected error occurred."]