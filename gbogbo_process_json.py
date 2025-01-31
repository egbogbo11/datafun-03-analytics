#####################################
# Import Modules
#####################################

# Import from Python Standard Library
import pathlib
import json

# Import from local project modules
from utils_logger import logger

#####################################
# Declare Global Variables
#####################################

fetched_folder_name: str = "data"
processed_folder_name: str = "data_processed"

#####################################
# Define Functions
#####################################

def count_tracks_with_other_artists(file_path: pathlib.Path, main_artist: str) -> int:
    """Count the number of tracks have an artist other Drake from a JSON file."""
    try:
        with file_path.open('r') as file:
            # Use the json module load() function 
            # to read data file into a Python dictionary
            track_data = json.load(file)  
            media_list = track_data.get("media", [])
            count_other_artists = 0
            for media in media_list:  
                tracks = media.get('tracks', [])
                for track in tracks:
                    artist_credits = track.get("artist-credit", [])
                    artist_names = {artist.get('name', '').lower() for artist in artist_credits}

                    if len(artist_names) > 1 or (artist_names and main_artist.lower() not in artist_names):
                        count_other_artists += 1
            return count_other_artists
    except Exception as e:
        logger.error(f"Error reading or processing JSON file: {e}")
        return {}

def process_json_file():
    """Read a JSON file, count astronauts by spacecraft, and save the result."""
    input_file: pathlib.Path = pathlib.Path(fetched_folder_name, "calabasas.json")
    output_file: pathlib.Path = pathlib.Path(processed_folder_name, "json_artists_by_track.txt")
    
    main_artist = "Drake" 
    count_other_artists = count_tracks_with_other_artists(input_file, main_artist)
    
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    with output_file.open('w') as file:
        file.write(f"Tracks with another artist besides {main_artist}: {count_other_artists}\n")
    
    logger.info(f"Processed JSON file: {input_file}, Results saved to: {output_file}")

#####################################
# Main Execution
#####################################

if __name__ == "__main__":
    logger.info("Starting JSON processing...")
    process_json_file()
    logger.info("JSON processing complete.")
