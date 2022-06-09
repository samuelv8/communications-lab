import numpy as np


class Channel:
    def __init__(self, p: float = 0.5) -> None:
        self.error_probability = p

    def transmit(self, msg: list) -> list:
        corrupted = np.random.rand(len(msg)) < self.error_probability
        transmitted_msg = []
        for i in range(len(msg)):
            if (np.random.rand() < self.error_probability):
                transmitted_msg.append((msg[i] + 1) % 2)
            else:
                transmitted_msg.append(msg[i])
        return transmitted_msg
