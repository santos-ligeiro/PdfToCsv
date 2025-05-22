#!/bin/bash

# Check if input folder argument is provided
if [ -z "$1" ]; then
  echo "Error: Input folder argument is missing."
  echo "Usage: $0 <input_folder> <output_folder>"
  exit 1
fi

# Check if output folder argument is provided
if [ -z "$2" ]; then
  echo "Error: Output folder argument is missing."
  echo "Usage: $0 <input_folder> <output_folder>"
  exit 1
fi

# Get the input and output folders from the arguments
input_folder="$1"
output_folder="$2"

# Delete the output folder if it exists
if [ -d "$output_folder" ]; then
  rm -rf "$output_folder"
fi

# Create the output folder
mkdir -p "$output_folder"

# Find all PDF files recursively in the input folder
iteration=1
find "$input_folder" -type f -name "*.pdf" | while read -r file; do
  # Get the filename without the extension
  filename=$(basename -- "$file")
  filename="${filename%.*}"
   
  output_file="$output_folder/${filename}_$iteration.csv"

  # Generate the output file path
#   output_file="$output_folder/$filename.csv"
  echo "##########################"
  echo "$file" 
  echo "$output_file" 
  
  # Convert the PDF to text using pdftotext
  java -jar /home/eugenio/ana_banana/tabula.jar "$file" --out "$output_file"
  
  ((iteration++))
  echo "Converted $file to $output_file"
done


