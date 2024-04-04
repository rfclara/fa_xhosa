import argparse
import os
import pandas as pd
from glob import glob

def convert_xlsx_to_txt(input_file, output_file):
    # Load the Excel file
    df = pd.read_excel(input_file)

    # Initialize a dictionary to hold sentences
    utterances = {}

    # Iterate over the rows to populate the dictionary
    for _, row in df.iterrows():
        phrase = row['phrase']
        token = row['token']
        if phrase not in utterances:
            utterances[phrase] = [token]
        else:
            utterances[phrase].append(token)

    # Convert the dictionary to a list of utterances
    final_utterances = [' '.join(tokens) for tokens in utterances.values()]

    # Write to a .txt file
    with open(output_file, 'w') as file:
        for sentence in final_utterances:
            file.write(sentence + "\n")

def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Convert .xlsx files to .txt format.')
    parser.add_argument('input_dir', type=str, help='Input directory containing .xlsx files')
    parser.add_argument('output_dir', type=str, help='Output directory for .txt files')
    args = parser.parse_args()

    # List all .xlsx files in the input directory
    xlsx_files = glob(os.path.join(args.input_dir, '*.xlsx'))

    # Ensure output directory exists, or creates it
    if not os.path.exists(args.output_dir):
        os.makedirs(args.output_dir)

    # Process each .xlsx file
    total =0
    for input_file in xlsx_files:
        # Construct output file path
        base_name = os.path.basename(input_file)
        output_file = os.path.join(args.output_dir, os.path.splitext(base_name)[0] + '.txt')
        # Convert and save
        convert_xlsx_to_txt(input_file, output_file)
        print(f"Processed {input_file} -> {output_file}")
        total +=1
    print(total, "files processed")

if __name__ == "__main__":
    main()
