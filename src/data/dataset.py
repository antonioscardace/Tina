import os
import torch
import pandas as pd

from monai.data import Dataset
from monai.transforms import Transform

# Defining a Dictionary to map text labels to numbers.
# CN = 0 = Negative for Alzheimer's.
# AD = 1 = Positive for Alzheimer's.

LABELS = {
    'CN': 0,
    'AD': 1
}

# Custom class for our brain MRI dataset (CSV + MRIs).
# Author: Antonio Scardace
# Version: 1.0

class BrainMriDataset(Dataset):
    
    def __init__(self, csv_path: str, images_path: str, transform: Transform = None):
        self.examples = pd.read_csv(csv_path)
        self.images_path = images_path
        self.transform = transform
        
    def __len__(self) -> int:
        return len(self.examples)
    
    def __getitem__(self, index: int) -> dict:
        label      = self.examples.loc[index, 'diagnosis']
        subject_id = self.examples.loc[index, 'subject_id']
        image_id   = self.examples.loc[index, 'image_id']
        image_path = os.path.join(self.images_path, subject_id, str(image_id), 'normalized.nii.gz')

        example = { 'image': image_path, 'label': torch.tensor(LABELS[label], dtype=torch.float32) }
        return example if self.transform is None else self.transform(example)