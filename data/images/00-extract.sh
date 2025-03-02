#!/bin/bash

mkdir -p ADNI

# For each zip file containing the dataset images, we will extract the images of the subjects.
# Then, we will merge them into the main "ADNI" folder.

for file in *.zip; do

    filename=$(basename "$file" .zip)

    # Here, we extract the MRIs of the dataset from the provided zip file.
    # We store the images in a temporary folder to be successively merged with the main folder.

    echo "Extracting the dataset images from $file"
    unzip -q -d "$filename" "$file"

    # Merge the extracted images from the temporary directory into the main "ADNI" folder.
    # We use the "rsync --ignore-existing" command instead of "mv" since a subject can be present in more than one zip.

    echo "Merging ./$filename/ files with the main ADNI folder"
    rsync -a --ignore-existing "$filename/ADNI/" "ADNI/"

    # Clean up by removing the temporary directory and the zip file
    
    rm -r "$filename"
    rm "$file"
    
done