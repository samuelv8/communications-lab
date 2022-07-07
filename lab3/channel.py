import numpy as np


class Channel:
    def __init__(self, p: float = 0.5) -> None:
        self.error_probability = p

    def transmit(self, msg: list) -> list:
        transmitted_msg = []
        for i in range(len(msg)):
            if np.random.rand() < self.error_probability:
                transmitted_msg.append((msg[i] + 1) % 2)
            else:
                transmitted_msg.append(msg[i])
        return transmitted_msg

    def transmit_eucli(self, msg: list) -> list:
        transmitted_msg = []
        sigma = -1 / (6 * np.log(2 * self.error_probability))
        for i in range(len(msg)):
            e = np.random.normal(0, sigma)
            transmitted_msg.append(msg[i] + 2 * e * np.sqrt(3))
        return transmitted_msg
