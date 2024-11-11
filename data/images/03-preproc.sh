#!/bin/bash

cd ADNI/
mkdir -p derivatives

# Our goal is to preprocess each MRI in our dataset using the following pipeline:
# 1. Bias Field Correction
# 2. Affine Registration
# 3. Skull Stripping
# 4. Intensity Normalization (WhiteStripe)

for subject_folder in "subjects/"*/; do

    subject_id=$(basename "$subject_folder")
    echo "Preprocessing MRIs for the subject $subject_id"

    # Process each MRI scan in the subject folder.
    # If an error occur, the script exits.

    for mri_file in "$subject_folder"*; do

        filename=$(basename "$mri_file")
        image_id="${filename%.nii.gz}"
        new_path="derivatives/$subject_id/$image_id"

        # To avoid repetitions, we check if the preprocessing has already been performed for that image.
        # If so, the loop moves to the next image without repeating the preprocessing.

        if [ -s "$new_path/preprocessed.nii.gz" ] && [ -s "$new_path/skullstrip_mask.nii.gz" ]; then
            echo "Image $filename already preprocessed"
            continue
        fi

        echo "Starting preprocessing for the image $filename putting results in $new_path/"
        mkdir -p "$new_path"

        # Step 1: Bias Field Correction using the N4 algorithm from the ANTs toolkit.
        # In the N4 algorithm, the shrink factor "-s 3" controls the degree of regularization applied.
        # After that, we check if Bias Field Correction was successful.

        echo "Bias Field Correction of $mri_file"
        N4BiasFieldCorrection -d 3 -s 3 -i "$mri_file" -o "$new_path/corrected.nii.gz" 

        if [ ! -s "$new_path/corrected.nii.gz" ]; then
            echo "Bias Field Correction failed"
            exit 1
        fi

        # Step 2: Affine Registration using antsRegistrationSyNQuick from the ANTs toolkit.
        # After that, we check if Affine Registration was successful.

        echo "Affine Registration of $new_path/corrected.nii.gz"
        antsRegistrationSyNQuick.sh -d 3 -m "$new_path/corrected.nii.gz" -o "$new_path/" -t "a" -s "../MNI152_T1_1mm.nii.gz" > /dev/null
        mv "$new_path/Warped.nii.gz" "$new_path/registered.nii.gz"

        if [ ! -s "$new_path/registered.nii.gz" ]; then
            echo "Affine Registration failed"
            exit 1
        fi

        # Step 3: Skull Stripping using the HD-BET brain extraction tool.
        # After that, we check if Bias Field Correction was successful.

        echo "Skull Stripping of $new_path/registered.nii.gz"
        hd-bet -i "$new_path/registered.nii.gz" -o "$new_path/skullstrip.nii.gz" > /dev/null

        if [ ! -s "$new_path/skullstrip.nii.gz" ] || [ ! -s "$new_path/skullstrip_mask.nii.gz" ]; then
            echo "Skull Stripping failed"
            exit 1
        fi

        # Step 4: Intensity Normalization using WhiteStripe.
        # After that, we check if Intensity Normalization was successful.

        echo "Intensity Normalization (WhiteStrip) of $new_path/skullstrip.nii.gz"
        ws-normalize -mo t1 -o "$new_path/preprocessed.nii.gz" "$new_path/skullstrip.nii.gz"

        if [ ! -s "$new_path/preprocessed.nii.gz" ]; then
            echo "Intensity Normalization failed"
            exit 1
        fi

        # We are just interested in the Skull Stripping Mask and Intensity Normalization files. 
        # Remove intermediate files, keeping only the final preprocessed files.

        find "$new_path" -type f ! \( -name "skullstrip_mask.nii.gz" -o -name "preprocessed.nii.gz" \) -exec rm {} +
         
    done
done