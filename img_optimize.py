import os
from PIL import Image

def optimize_images(root_dir, quality=80):
    """
    Scans the directory tree starting from root_dir, finds image files,
    and optimizes them to reduce file size while maintaining good quality.
    - Converts PNG and GIF to JPEG.
    - Recompresses existing JPEGs.
    - Replaces original files (after saving the optimized version).
    """
    image_extensions = ('.png', '.jpg', '.jpeg', '.gif')
    
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file.lower().endswith(image_extensions):
                full_path = os.path.join(root, file)
                print(f"Processing: {full_path}")
                
                try:
                    img = Image.open(full_path)
                    
                    # Determine new path: convert non-JPEG to .jpg
                    if img.format in ['PNG', 'GIF']:
                        new_path = os.path.splitext(full_path)[0] + '.jpg'
                        img = img.convert('RGB')  # Convert to RGB for JPEG compatibility
                    else:
                        new_path = full_path
                    
                    # Save with compression
                    img.save(new_path, 'JPEG', quality, optimize=True)
                    print(f"Optimized: {new_path} (new size: {os.path.getsize(new_path)} bytes)")
                    
                    # Remove original if it was converted
                    if new_path != full_path:
                        os.remove(full_path)
                        print(f"Removed original: {full_path}")
                
                except Exception as e:
                    print(f"Error processing {full_path}: {e}")

# Example usage: replace '.' with your root directory path
optimize_images('/Users/neo_collection1/Documents/GitHub/data-science-practice', 76)