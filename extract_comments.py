import os
import re
from glob import glob

def extract_comments_from_file(file_path):
    """
    Extract unique comments enclosed in <> from a given file.
    """
    comments = set()
    with open(file_path, 'r') as file:
        for line in file:
            comments_found = re.findall(r'(<.*?>)', line)
            comments.update(comments_found)
    return comments

def main(input_dir):
    # Construct the path for comments.txt in the input directory
    comments_file_path = os.path.join(input_dir, 'comments.txt')

    # Find all .txt files in the specified directory
    txt_files = glob(os.path.join(input_dir, '*.txt'))

    # Initialize a set to hold all unique comments
    all_comments = set()

    # Iterate over each .txt file, extracting comments
    for txt_file in txt_files:
        file_comments = extract_comments_from_file(txt_file)
        all_comments.update(file_comments)

    # Write all unique comments to comments.txt
    with open(comments_file_path, 'w') as comments_file:
        for comment in sorted(all_comments):  # sort the comments for consistent output
            comments_file.write(comment + "\n")

    print(f"All unique comments have been extracted to {comments_file_path}")

if __name__ == "__main__":
    # Example usage: python extract_comments.py /path/to/directory
    import sys
    if len(sys.argv) != 2:
        print("Usage: python extract_comments.py <directory>")
        sys.exit(1)
    
    input_dir = sys.argv[1]
    main(input_dir)
