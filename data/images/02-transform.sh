#!/bin/bash

cd ADNI/subjects/

# Our goal is to convert the images of each subject from the DICOM format to the NIfTI (compressed) format.
# Additionally, we finalize the process of organizing the images into a simplified structure.

for subject_folder in */; do

    subject_id=$(basename "$subject_folder")
    echo "Converting the images of the subject $subject_id from DCM files to NIfTI"

    # For each image folder, which contains a set of DCM files, we create a .nii.gz file.
    # We will then move the .nii.gz file to the subject folder and delete the original DCM files:
    # Old structure: /ADNI/subjects/SUBJECT_ID/IMAGE_ID/*.dcm | something.nii.gz
    # New structure: /ADNI/subjects/SUBJECT_ID/IMAGE_ID.nii.gz

    for image_id_folder in "$subject_folder"*/; do

        image_id=$(basename "$image_id_folder")
        echo "Converting the image $image_id"

        # Use "dcm2niix" to convert the DICOM files to a compressed NIfTI file.
        # The "-z y" option enables gzip compression.
        # After that, move the NIfTI file to the subject folder and remove the DICOM image folder.

        dcm2niix -z y -o "$image_id_folder" "$image_id_folder" > /dev/null
        mv "$image_id_folder"*.gz "$subject_folder$image_id.nii.gz"
        rm -r "$image_id_folder"

    done
done