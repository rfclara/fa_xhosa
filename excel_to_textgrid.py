import pandas as pd
from praatio import textgrid
import argparse
import os

def create_textgrid_from_excel(excel_path, output_path):
    # Load the updated Excel file
    df = pd.read_excel(excel_path)
    
    # Group by phrase and speaker to get sentence level intervals
    grouped = df.groupby(['phrase', 'speaker']).agg({
        'sentence_start': 'min',
        'sentence_end': 'max',
        'token': lambda x: ' '.join(x),
        'translation': 'first'
    }).reset_index()
    
    # Create a new TextGrid object
    tg = textgrid.Textgrid()
    
    # Get the minimum and maximum timestamps
    min_timestamp = grouped['sentence_start'].min()
    max_timestamp = grouped['sentence_end'].max()
    tg.minTimestamp = min_timestamp
    tg.maxTimestamp = max_timestamp
    
    # Create dictionaries to hold intervals for each speaker
    speaker_intervals = {}
    translation_intervals = []
    
    for _, row in grouped.iterrows():
        speaker = row['speaker']
        start_time = row['sentence_start']
        end_time = row['sentence_end']
        text = row['token']

        # Use the translation if available, otherwise use the original text (handles comments like <laugh>)
        translation = row['translation'] if pd.notna(row['translation']) else text
        
        if speaker not in speaker_intervals:
            speaker_intervals[speaker] = []
        
        speaker_intervals[speaker].append((start_time, end_time, text))
        translation_intervals.append((start_time, end_time, translation))
    
    # Create new tiers for each speaker and add intervals
    for speaker, intervals in speaker_intervals.items():
        tier = textgrid.IntervalTier(speaker, intervals, min_timestamp, max_timestamp)
        tg.addTier(tier)
    
    # Create a tier for the translations
    translation_tier = textgrid.IntervalTier('English', translation_intervals, min_timestamp, max_timestamp)
    tg.addTier(translation_tier)
    
    # Save the TextGrid file
    tg.save(output_path, format='long_textgrid', includeBlankSpaces=True)

def main():
    parser = argparse.ArgumentParser(description='Convert Excel file to TextGrid')
    parser.add_argument('input', help='Path to the input Excel file')
    parser.add_argument('-o', '--output', help='Path to the output TextGrid file (optional)')
    
    args = parser.parse_args()
    
    input_path = args.input
    
    if args.output:
        output_path = args.output
    else:
        # If no output path is provided, use the input filename with .TextGrid extension
        output_path = os.path.splitext(input_path)[0] + '.TextGrid'
    
    create_textgrid_from_excel(input_path, output_path)
    print(f"TextGrid file created: {output_path}")

if __name__ == "__main__":
    main()
