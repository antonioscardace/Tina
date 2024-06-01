import numpy as np
import matplotlib.pyplot as plt

# Function to display a confusion matrix.
# The x-axis represents the predicted labels, while the y-axis represents the true labels.

def plot_confusion_matrix(cm: np.ndarray, class_names: list, figsize: tuple) -> None:
    plt.figure(figsize=figsize)
    plt.imshow(cm, cmap='GnBu')
    plt.colorbar()

    for i in range(len(class_names)):
        for j in range(len(class_names)):
            plt.text(j, i, cm[i, j], ha='center', va='center')

    plt.xlabel('Predicted label', fontsize=12)
    plt.ylabel('True label', fontsize=12)
    plt.xticks(np.arange(len(class_names)), class_names, rotation=45)
    plt.yticks(np.arange(len(class_names)), class_names)
    plt.show()
    plt.close()

# Function to display the central slices of a MRI from three different perspectives - axial, coronal, sagittal.
# Takes the shape of the 3D scan (z, y, x) and the scan data as a numpy array.

def plot_scan_central_slices(shape: tuple, scan: np.ndarray, label: str, figsize: tuple, padding: int) -> None:
    slices = {
        'Sagittal': scan[shape[0] // 2, :, :],
        'Axial': scan[:, :, shape[2] // 2],
        'Coronal': scan[:, shape[1] // 2, :]
    }
    
    fig, axes = plt.subplots(nrows=1, ncols=3, figsize=figsize)
    for ax, (title, slice) in zip(axes, slices.items()):
        padded_slice = np.pad(slice, pad_width=padding, mode='constant', constant_values=0)
        ax.imshow(padded_slice, cmap='gray')
        ax.set_title(title)
        ax.axis('off')

    fig.suptitle(label, fontsize=15, y=0.75)
    plt.show()
    plt.close()