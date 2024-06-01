# Class to compute average metrics over multiple samples.
# Provides attributes and methods for loss and accuracy (specifically F1-score) metrics.
# Author: Antonio Scardace
# Version: 1.0

class AverageMetricsMeter:

    def __init__(self):
        self.reset()

    def reset(self) -> None:
        self.loss_sum = 0
        self.performance_sum = 0
        self.num_samples = 0

    def add(self, loss_value: float, performance_value: float, num: int) -> None:
        self.loss_sum += loss_value * num
        self.performance_sum += performance_value * num
        self.num_samples += num

    def loss_value(self) -> float:
        return self.loss_sum / self.num_samples if self.num_samples != 0 else 0

    def performance_value(self) -> float:
        return self.performance_sum / self.num_samples if self.num_samples != 0 else 0