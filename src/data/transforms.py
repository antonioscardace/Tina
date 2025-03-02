import torch

from numpy import percentile
from monai.transforms import Compose, Lambda
from monai.transforms import LoadImageD
from monai.transforms import EnsureChannelFirstD, ResizeWithPadOrCropD, ScaleIntensityD, SpacingD

# Class to define a set of useful transformations.
# Author: Antonio Scardace
# Version: 1.0

class Transforms:

    # Removes outlier intensities from a brain component.
    # Calculates the lower percentile (1st percentile) value and the upper percentile (99th percentile).
    # Replaces image values ​​below the lower percentile with the lower percentile value.
    # Replaces image values above the upper percentile with the upper percentile value.

    @staticmethod
    def percentile_norm(example: dict) -> dict:
        lowerbound = torch.tensor(percentile(example['image'], 1), dtype=torch.float32)
        upperbound = torch.tensor(percentile(example['image'], 99), dtype=torch.float32)
        example['image'] = torch.clamp(example['image'], lowerbound, upperbound)
        return example

    # Loads the image without its metadata.
    # Ensures the channel (greyscale) is the first axis of the image.
    # Modifies the image spacing to 1.4 millimetres.
    # Resizes the image with padding or cropping to a size of (130, 130, 130).
    # Scales the pixel intensity of the image to the range [0, 1].

    @staticmethod
    def get_data_loading() -> Compose:
        return Compose([
            LoadImageD(keys='image', image_only=True),
            EnsureChannelFirstD(keys='image'), 
            SpacingD(keys='image', pixdim=1.4),
            ResizeWithPadOrCropD(keys='image', spatial_size=(130, 130, 130), mode='minimum'),
            Lambda(lambda record: Transforms.percentile_norm(record)),
            ScaleIntensityD(keys='image', minv=0, maxv=1),
        ])