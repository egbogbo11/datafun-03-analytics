"""
Process a CSV file on NFL rushing data to analyze the `Yards` column and save statistics.
"""

#####################################
# Import Modules
#####################################

# Import from Python Standard Library
import pathlib
import csv
import statistics

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

def analyze_yards(file_path: pathlib.Path) -> dict:
    """Analyze the Yards column to calculate min, max, mean, and stdev."""
    try:
        yards_list = []
        with file_path.open('r') as file:
            dict_reader = csv.DictReader(file)  
            for row in dict_reader:
                try:
                    yards = float(row["Yards"])  
                    yards_list.append(yards)
                except ValueError as e:
                    logger.warning(f"Skipping invalid row: {row} ({e})")
       
        # Calculate statistics
        stats = {
            "min": min(yards_list),
            "max": max(yards_list),
            "mean": statistics.mean(yards_list),
            "stdev": statistics.stdev(yards_list) if len(yards_list) > 1 else 0,
        }
        return stats
    except Exception as e:
        logger.error(f"Error processing CSV file: {e}")
        return {}

def process_csv_file():
    """Read a CSV file, analyze Yards, and save the results."""
    input_file = pathlib.Path(fetched_folder_name, "nflfantasy.csv")
    output_file = pathlib.Path(processed_folder_name, "nfl_rushing_yards_stats.txt")
   
    stats = analyze_yards(input_file)
    output_file.parent.mkdir(parents=True, exist_ok=True)
   
    with output_file.open('w') as file:
        file.write("Yards Statistics:\n")
        file.write(f"Minimum: {stats['min']:.2f}\n")
        file.write(f"Maximum: {stats['max']:.2f}\n")
        file.write(f"Mean: {stats['mean']:.2f}\n")
        file.write(f"Standard Deviation: {stats['stdev']:.2f}\n")
   
    logger.info(f"Processed CSV file: {input_file}, Statistics saved to: {output_file}")

#####################################
# Main Execution
#####################################

if __name__ == "__main__":
    logger.info("Starting CSV processing...")
    process_csv_file()
    logger.info("CSV processing complete.")