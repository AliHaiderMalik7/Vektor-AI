import os, base64

def get_image_base64(image_path: str) -> str:
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image not fount at path: {image_path}")
    
    try:
        with open(image_path, "rb") as img_file:
            encoded_bytes = base64.b64encode(img_file.read())
            return encoded_bytes.decode('utf-8')
    except Exception as e:
        raise Exception(f"Error encoding image to base64: {str(e)}")