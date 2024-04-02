import json
import textgrid
"""
Converts a manifest.json from NeMO/tools/speech_data_explorer format to  a Praat .TextGrid
TODO: modify the script to take arguments from command and take a directory as input, treating *.json files.
"""
# Load JSON data
json_file = 'manifest.json'
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
    # Fix the method call here
    transcription_tier.add(start_time, end_time, text)

# Save the TextGrid file
tg_filename = 'output.TextGrid'  # Adjust the output file name as needed
with open(tg_filename, 'w') as f:
    tg.write(f.name)

print(f"TextGrid file saved as {tg_filename}")

