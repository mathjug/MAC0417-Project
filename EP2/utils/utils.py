import cv2
import os
import numpy as np

def rescale_image(img):
    min_value = np.min(img)
    max_value = np.max(img)
    new_img = ((img - min_value) / (max_value - min_value)) * 255
    new_img = new_img.astype(np.uint8)
    return new_img

def compare_images(img1_path, img2_path):
    """
    Compare two images and return True if they are the same, else False.
    """
    try:
        img1 = cv2.imread(img1_path)
        img2 = cv2.imread(img2_path)
        if img1.shape != img2.shape:
            return False
        difference = cv2.absdiff(img1, img2)
        result = not np.any(difference)
        return result
    except Exception as e:
        print(f"Error comparing {img1_path} and {img2_path}: {e}")
        return False

def compare_images_in_folders(folder1, folder2):
    """
    Compare images with the same names in two folders.
    """
    folder1_files = {f for f in os.listdir(folder1) if os.path.isfile(os.path.join(folder1, f))}
    folder2_files = {f for f in os.listdir(folder2) if os.path.isfile(os.path.join(folder2, f))}

    # Find common files
    common_files = folder1_files & folder2_files
    
    comparison_results = {}
    
    for file_name in common_files:
        img1_path = os.path.join(folder1, file_name)
        img2_path = os.path.join(folder2, file_name)
        are_equal = compare_images(img1_path, img2_path)
        comparison_results[file_name] = are_equal
    
    return comparison_results
