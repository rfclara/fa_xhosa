import pandas as pd
import json
import argparse
import logging
import sys

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def update_excel_with_times(excel_path, json_path, output_path):
    try:
        # Load the Excel file
        df = pd.read_excel(excel_path)
    except Exception as e:
        logging.error(f"Failed to read the Excel file: {e}")
        sys.exit(1)
    
    try:
        # Load the JSON file
        with open(json_path, 'r') as file:
            json_data = [json.loads(line.strip()) for line in file]
    except Exception as e:
        logging.error(f"Failed to read the JSON file: {e}")
        sys.exit(1)
    
    # Initialize lists for start and end times
    sentence_starts = [None] * len(df)
    sentence_ends = [None] * len(df)
    
    # Print debug information
    logging.info(f"Excel rows: {len(df)}")
    logging.info(f"JSON entries: {len(json_data)}")
    
    # Create a dictionary to map phrases to their corresponding timestamps
    phrase_to_timestamps = {}
    for i, entry in enumerate(json_data):
        phrase_to_timestamps[i + 1] = (entry['audio_start_sec'], entry['audio_start_sec'] + entry['duration'])
    
    # Assign timestamps to rows in the DataFrame based on phrases
    for idx, row in df.iterrows():
        phrase_number = row['phrase']
        if phrase_number in phrase_to_timestamps:
            start_time, end_time = phrase_to_timestamps[phrase_number]
            sentence_starts[idx] = start_time
            sentence_ends[idx] = end_time
    
    # Add new columns to the DataFrame
    df['sentence_start'] = sentence_starts
    df['sentence_end'] = sentence_ends
    
    try:
        # Save the updated DataFrame to a new Excel file
        df.to_excel(output_path, index=False)
        logging.info(f"Updated Excel file created: {output_path}")
    except Exception as e:
        logging.error(f"Failed to save the updated Excel file: {e}")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description='Update Excel file with times from JSON')
    parser.add_argument('input_excel', help='Path to the input Excel file')
    parser.add_argument('input_json', help='Path to the input JSON file')
    parser.add_argument('output_excel', help='Path to the output Excel file')
    
    args = parser.parse_args()
    
    update_excel_with_times(args.input_excel, args.input_json, args.output_excel)

if __name__ == "__main__":
    main()
