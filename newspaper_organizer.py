import os
import shutil
from PIL import Image

# Define the standard newspaper size (in pixels)
NEWSPAPER_WIDTH = 2250
NEWSPAPER_HEIGHT = 3412

# Get the source directory from user input
while True:
    SOURCE_DIR = input("Please enter the full path to the source directory: ").strip()
    if os.path.isdir(SOURCE_DIR):
        break
    else:
        print("The specified path is not a valid directory. Please try again.")

# Create the exported directory at the same level as SOURCE_DIR
EXPORT_DIR = os.path.join(
    os.path.dirname(SOURCE_DIR), f"exported_{os.path.basename(SOURCE_DIR)}"
)

# Define destination directories within the exported directory
FULL_DIR = os.path.join(EXPORT_DIR, "full")
HALF_DIR = os.path.join(EXPORT_DIR, "half-horizontal")
QUARTER_DIR = os.path.join(EXPORT_DIR, "quarter-vertical")

# Create destination directories if they don't exist
os.makedirs(FULL_DIR, exist_ok=True)
os.makedirs(HALF_DIR, exist_ok=True)
os.makedirs(QUARTER_DIR, exist_ok=True)


def categorize_image(image_path):
    try:
        with Image.open(image_path) as img:
            width, height = img.size
            print(f"Image size: {width} x {height}")

            # Calculate the ratio of image dimensions to newspaper dimensions
            width_ratio = width / NEWSPAPER_WIDTH
            height_ratio = height / NEWSPAPER_HEIGHT

            # Full page
            if 0.75 <= width_ratio <= 1.1 and 0.75 <= height_ratio <= 1.1:
                return FULL_DIR
            # Half-horizontal
            elif 0.75 <= width_ratio <= 1.1 and 0.3 <= height_ratio <= 0.6:
                return HALF_DIR
            # Quarter-vertical
            elif 0.35 <= width_ratio <= 0.6 and 0.35 <= height_ratio <= 0.6:
                return QUARTER_DIR
            else:
                return None
    except Exception as e:
        print(f"Error processing {image_path}: {str(e)}")
        return None


def process_directory(directory):
    for item in os.listdir(directory):
        item_path = os.path.join(directory, item)
        if os.path.isfile(item_path):
            if item.lower().endswith((".png", ".jpg", ".jpeg", ".tiff", ".bmp")):
                category = categorize_image(item_path)
                if category:
                    destination = os.path.join(category, item)
                    # Ensure unique filenames in the destination
                    base, ext = os.path.splitext(item)
                    counter = 1
                    while os.path.exists(destination):
                        destination = os.path.join(category, f"{base}_{counter}{ext}")
                        counter += 1
                    shutil.copy2(item_path, destination)
                    print(f"Copied {item} to {os.path.basename(category)}")
                else:
                    print(f"Skipped {item} - doesn't meet criteria")
        elif os.path.isdir(item_path):
            process_directory(item_path)  # Recursive call for subdirectories


# Main script
print(f"Source directory: {SOURCE_DIR}")
print(f"Export directory: {EXPORT_DIR}")
confirmation = input("Do you want to proceed? (y/n): ").strip().lower()
if confirmation == "y":
    process_directory(SOURCE_DIR)
    print("Image organization complete!")
else:
    print("Operation cancelled.")
