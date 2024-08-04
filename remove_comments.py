import re
import sys

def remove_comments(file_path):
    # Read the content of the file
    with open(file_path, 'r') as file:
        content = file.read()
    
    # Remove text between < and > including the brackets
    modified_content = re.sub(r"<[^>]*>", " ", content)
    
    # Write the modified content back to the file
    with open(file_path, 'w') as file:
        file.write(modified_content)
    
    print(f"Processed file '{file_path}' successfully.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <file_path>")
        sys.exit(1)
    
    file_path = sys.argv[1]
    remove_comments(file_path)

