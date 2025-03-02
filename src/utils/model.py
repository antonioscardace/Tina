import os
import torch 

from sklearn.metrics import f1_score
from monai.networks.nets import DenseNet
from torch.nn import BCEWithLogitsLoss
from torch.optim import AdamW

# Function to save the best model and optimizer states.
# It also prints a message confirming the update.

def save_model(net: DenseNet, optimizer: AdamW, folder_path: str) -> None:
    torch.save(net.state_dict(), os.path.join(folder_path, 'best_model.pth'))
    torch.save(optimizer.state_dict(), os.path.join(folder_path, 'best_optimizer.pth'))
    print('Best Model Updated.')

# Function to load the best model from a specified folder.
# It prints a message confirming the loading of the model.

def load_model(net: DenseNet, folder_path: str, device: str) -> None:
    net.load_state_dict(torch.load(os.path.join(folder_path, 'best_model.pth'), map_location=device))
    net.to(device)
    print('The Best Saved Model has been Loaded.')

# Function to calculate loss and performance metrics.
# Calculates the loss using the specified loss criterion and computes the F1-Score as the performance metric.

def calculate_metrics(y_true: torch.Tensor, y_pred: torch.Tensor, criterion: BCEWithLogitsLoss, device: str) -> tuple:
    with torch.autocast(device, enabled=False):
        loss = criterion(y_pred, y_true)
        y_pred_label = (torch.sigmoid(y_pred) > 0.5).float()
        performance = f1_score(y_true.cpu().numpy(), y_pred_label.cpu().numpy())
        return loss, performance