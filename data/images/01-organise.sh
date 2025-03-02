#!/bin/bash

cd ADNI/
mkdir -p subjects

# Our goal is to organise the images with a simplified and improved structure.
# We perform this process on each subject folder within the ADNI directory.

for subject_folder in */; do

    # Check if we have reached the 'subjects' directory, indicating the completion of the process.
    # This acts as a stopping condition to prevent infinite loops.

    if [[ "$subject_folder" == *"subjects"* ]]; then
        echo "Job completed."
        exit 0
    fi

    # Navigate through the nested structure: SUBJECT_ID/DESCRIPTION/DATE/IMAGE_ID/*.dcm
    # We need to move these images to the new structure: subjects/SUBJECT_ID/IMAGE_ID/*.dcm

    subject_id=$(basename "$subject_folder")
    echo "Organising the folder of the subject $subject_id"

    for variable_folder in "$subject_folder"*/; do
        for date_folder in "$variable_folder"*/; do
            for image_id_folder in "$date_folder"*/; do

                image_id=$(basename "$image_id_folder")

                echo "Moving all images from $image_id_folder to subjects/$subject_id/$image_id/"
                mkdir -p "subjects/$subject_id/$image_id"
                mv "$image_id_folder"*.dcm "subjects/$subject_id/$image_id"
                
            done
        done
    done

    # Remove the original (now empty) subject folder to clean up

    rm -r "$subject_folder"

done