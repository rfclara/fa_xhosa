import argparse
import json
import os
import textgrid

def convert_json_to_textgrid(json_file, output_file_path):
    # Load JSON data
    with open(json_file, 'r') as f:
        lines = f.readlines()

    data = [json.loads(line) for line in lines]

    # Create a new TextGrid object
    tg = textgrid.TextGrid()

    # Add an interval tier called "Transcription"
    tier_name = "Transcription"
    transcription_tier = textgrid.IntervalTier(name=tier_name)
    tg.append(transcription_tier)

    # Populate the tier with intervals from the JSON data
    for item in data:
        start_time = float(item["audio_start_sec"])
        end_time = start_time + float(item["duration"])
        text = item["text"]
        transcription_tier.add(start_time, end_time, text)

    # Save the TextGrid file
    with open(output_file_path, 'w') as f:
        tg.write(f.name)

    print(f"TextGrid file saved as {output_file_path}")

def main():
    parser = argparse.ArgumentParser(description='Convert a JSON file to a TextGrid file.')
    parser.add_argument('json_file', type=str, help='Path to the JSON file')
    parser.add_argument('output_file_path', type=str, help='Full output file path for the TextGrid file')
    args = parser.parse_args()

    print(f"JSON file path: {args.json_file}")  # Debugging print
    print(f"Output file path: {args.output_file_path}")  # Debugging print

    output_directory = os.path.dirname(args.output_file_path)
    # Ensure output directory exists
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    # Convert the specified JSON file
    convert_json_to_textgrid(args.json_file, args.output_file_path)

if __name__ == "__main__":
    main()
