from torch.utils.tensorboard import SummaryWriter

# Function to log loss and performance metrics for visualization in TensorBoard.
# It also prints the F1-score and loss values.
    
def log_metrics(writer: SummaryWriter, mode: str, epoch: int, loss: float, performance: float) -> None:
    writer.add_scalar(tag=f'loss/{mode}', scalar_value=loss, global_step=epoch)
    writer.add_scalar(tag=f'accuracy/{mode}', scalar_value=performance, global_step=epoch)
    print('F1-Score:', performance)
    print('Loss:', loss)