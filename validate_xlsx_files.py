import argparse
import os
import pandas as pd
from glob import glob

def validate_xlsx(df):
    expected_columns = ['phrase', 'token']
    errors = []

    # Check for missing columns
    for col in expected_columns:
        if col not in df.columns:
            errors.append(f"Missing column: {col}")

    if errors:
        return False, errors

    previous_phrase_number = None
    for index, row in df.iterrows():
        try:
            phrase = row['phrase']
            token = row['token']
            
            # Check for missing values
            if pd.isna(phrase) or pd.isna(token):
                errors.append(f"Missing phrase or token at row {index}")

            # Check for integer phrase values
            if not isinstance(phrase, int):
                try:
                    phrase = int(phrase)
                except ValueError:
                    errors.append(f"Non-integer phrase value at row {index}: {phrase}")

            # Check for string token values
            if not isinstance(token, str):
                errors.append(f"Non-string token value at row {index}: {token}")

            # Check for sequential phrase numbers starting from 1
            if previous_phrase_number is None:
                if phrase != 1:
                    errors.append(f"Phrase numbers should start at 1, but found {phrase} at row {index}")
            else:
                # Allow consecutive same phrase numbers
                if phrase != previous_phrase_number and phrase != previous_phrase_number + 1:
                    errors.append(f"Non-sequential phrase number at row {index}: expected {previous_phrase_number + 1} but got {phrase}")

            previous_phrase_number = phrase
        except Exception as e:
            errors.append(f"Error at row {index}: {str(e)}")
    
    return len(errors) == 0, errors

def main():
    parser = argparse.ArgumentParser(description='Validate .xlsx files.')
    parser.add_argument('input_dir', type=str, help='Input directory containing .xlsx files')
    parser.add_argument('output_file', type=str, help='Output file for error logs')
    args = parser.parse_args()

    xlsx_files = glob(os.path.join(args.input_dir, '*.xlsx'))

    total_files = 0
    files_with_errors = 0
    all_errors = []

    for input_file in xlsx_files:
        df = pd.read_excel(input_file)
        is_valid, errors = validate_xlsx(df)
        
        if not is_valid:
            for error in errors:
                all_errors.append(f"{input_file}: {error}")
            print(f"Validation failed for {input_file}.")
            files_with_errors += 1
        
        total_files += 1

    # Write all errors to a single log file
    with open(args.output_file, 'w') as log_file:
        for error in all_errors:
            log_file.write(error + "\n")
    
    print(f"Processed {total_files} files.")
    print(f"Found errors in {files_with_errors} files.")

if __name__ == "__main__":
    main()
