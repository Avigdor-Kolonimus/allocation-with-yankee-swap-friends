import os

def create_folders(base_path, weight, course_limits):
    # Create folder names based on the weight and course limits
    folder_names = [
        f"{course_limit}_courseLimit_{weight}_weight_accumulate"  
        for course_limit in course_limits
    ]
    
    # Create each folder in the specified base path
    for folder_name in folder_names:
        folder_path = os.path.join(base_path, folder_name)
        os.makedirs(folder_path, exist_ok=True)
        print(f"Created folder: {folder_path}")

# Example usage
if __name__ == "__main__":
    base_path = '.'  # Specify the base path where the folders should be created
    
    weight = 0
    course_limits = [90, 85, 80, 75, 70, 65, 60]

    create_folders(base_path, weight, course_limits)
