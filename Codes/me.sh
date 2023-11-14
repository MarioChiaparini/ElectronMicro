#!/bin/bash

# Define the directory containing the TIFF files
TIFF_DIR="../LFP_PÓ_TIFF"
OUTPUT_DIR="../Measurements_CSV"

# Path to the Python script
PYTHON_SCRIPT_PATH="./me.py"

# Create output directory if it doesn't exist
mkdir -p "$OUTPUT_DIR"

# Loop through each TIFF file in the directory
for tiff_file in "$TIFF_DIR"/*.tiff; do
  # Extract the base filename without path and extension
  base_filename=$(basename "$tiff_file" .tiff)

  # Define the output CSV file path
  output_csv="$OUTPUT_DIR/${base_filename}_measurement_mev.csv"

  # Run the Python code with the current TIFF file and output to the corresponding CSV file
  python "$PYTHON_SCRIPT_PATH" "$tiff_file" "$output_csv"

done

# Print completion message
echo "All measurements completed."
