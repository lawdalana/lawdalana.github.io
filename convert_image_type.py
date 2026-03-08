import os
import pillow_avif
from PIL import Image

# Set the folder path where your images are located
folder_path = "./assets/img"

def convert_images_in_folder(folder_path):
    # Loop through all files in the folder
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)

        # Check if the current item is a folder
        if os.path.isdir(file_path):
            # Recursively convert images in subfolders
            convert_images_in_folder(file_path)
        else:
            if filename.endswith((".png", ".jpg", ".jpeg", ".webp")):
                # Open the image
                image_path = os.path.join(folder_path, filename)
                image = Image.open(image_path)
        
                # Generate the new AVIF filename
                base_name, extension = os.path.splitext(filename)
                new_filename = base_name + ".avif"
                new_image_path = os.path.join(folder_path, new_filename)
        
                # Convert and save the image to AVIF format
                image.save(new_image_path, format="avif")
                print(f"Converted {filename} to {new_filename}")

convert_images_in_folder(folder_path)

print("\nFiles in directory after conversion:")
for filename in os.listdir(folder_path):
    print(filename)
