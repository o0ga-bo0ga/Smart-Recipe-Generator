from ultralytics import YOLO
from PIL import Image
import os

# --- MODEL LOADING ---
# Load the YOLOv8 model. This line runs only once when the module is first imported,
# not on every function call. On Vercel, this means it loads once per "warm" instance.
# The model file 'yolov8n.pt' will be downloaded automatically on first run.
model = YOLO('best.pt') 

def allowed_file(filename):
    """Checks if the uploaded file has an allowed extension."""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg'}

def process_image(file, upload_folder):
    """
    Processes an uploaded image file to detect ingredients using YOLOv8.
    """
    if not file or not allowed_file(file.filename):
        return []

    filename = file.filename
    filepath = os.path.join(upload_folder, filename)
    
    try:
        # Save the file temporarily
        file.save(filepath)

        # Perform object detection
        results = model(filepath)  # The core YOLOv8 prediction step

        # Extract the names of the detected objects
        detected_objects = set()  # Use a set to store unique ingredient names
        for r in results:
            for box in r.boxes:
                # Get the class name from the model's names dictionary
                class_name = model.names[int(box.cls)]
                detected_objects.add(class_name)

        return list(detected_objects)

    except Exception as e:
        print(f"Image processing error: {str(e)}")
        return []
    finally:
        # Clean up the saved file
        if os.path.exists(filepath):
            os.remove(filepath)

# The load_unique_ingredients function is no longer needed with YOLO
# as we are detecting objects directly, not comparing against a predefined list.