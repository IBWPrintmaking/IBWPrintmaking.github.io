# How to run:
# 1. Make sure you have Python installed on your computer.
#  1.1. If you don't have Python installed, you can download it from https://www.python.org/downloads/ and follow the installation instructions for your operating system.
# 2. Open a terminal or command prompt.
#  2.1. If you're in vs code, you can open the terminal by going to View > Terminal or using the shortcut Ctrl + ` (backtick).
# 3. Navigate to the directory where this script is located.
#  3.1. Open your file explorer and find the folder containing this script. Then, in the terminal, use the cd command to change to that directory. For example, if the script is in a folder called "printmaking-website" on your desktop, you would use the following command:
#     cd Desktop/printmaking-website
# 4. Run the script using the command in the terminal: python compileImages.py



# Script starts here:

# Install Pillow if it's not already installed
try:
  import PIL
except ImportError:
  import subprocess
  subprocess.check_call(["python", "-m", "pip", "install", "Pillow"])
  import PIL

import os
import shutil
from PIL import Image

# Define the directory containing the images
image_directory = "fullQualityImages"
# Define the output directory
output_directory = "images"

# Also handle subdirectories
for root, dirs, files in os.walk(image_directory):
  for image_file in files:
    if image_file.endswith((".png", ".jpg", ".jpeg", ".svg")):
      # Create corresponding output subdirectory
      rel_path = os.path.relpath(root, image_directory)
      out_dir = os.path.join(output_directory, rel_path) if rel_path != "." else output_directory
      os.makedirs(out_dir, exist_ok=True)

      img_path = os.path.join(root, image_file)
      out_path = os.path.join(out_dir, image_file)

      if image_file.endswith(".svg"):
        shutil.copy2(img_path, out_path)
        print(f"Copied {os.path.relpath(img_path, image_directory)}")
        continue
      
      # Open and process image
      img: Image.Image = Image.open(img_path)
      
      # Rescale the image while maintaining aspect ratio
      quality = 800
      aspect_ratio = img.width / img.height
      new_width, new_height = 0, 0
      if aspect_ratio > 1:  # Landscape orientation
        new_width = quality
        new_height = int(quality / aspect_ratio)
      else:  # Portrait orientation
        new_width = int(quality * aspect_ratio)
        new_height = quality
      img.thumbnail((new_width, new_height), Image.LANCZOS)
      
      # Save the resized image to the output directory
      img.save(out_path)
      print(f"Processed {os.path.relpath(img_path, image_directory)}")