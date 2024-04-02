import os
import pandas as pd
import sys

def extract_transcriptions(directory):
    for filename in os.listdir(directory):
        if filename.endswith('.xlsx') or filename.endswith('.xls'):
            filepath = os.path.join(directory, filename)
            df = pd.read_excel(filepath, sheet_name=0)
            filtered_rows = df.iloc[0::5, 1:]  # Adjusted for zero-based indexing
            txt_filepath = os.path.splitext(filepath)[0] + '.txt'
            with open(txt_filepath, 'w', encoding='utf-8') as txt_file:
                for index, row in filtered_rows.iterrows():
                    # Join non-NaN values into a string, separated by spaces, and write to file
                    txt_file.write(' '.join(row.dropna().astype(str)) + '\n')

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python extract_transcriptions.py /path/containing/the/excelfiles")
        sys.exit(1)
    extract_transcriptions(sys.argv[1])
