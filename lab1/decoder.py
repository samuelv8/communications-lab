from abc import ABC
import numpy as np


class Decoder(ABC):
    def __init__(self) -> None:
        super().__init__()

    def decode(self):
        raise NotImplementedError('Abstract method!')


class Hamming(Decoder):
    def __init__(self) -> None:
        super().__init__()
        self.HT = [
            [1, 1, 1],  # b1
            [1, 0, 1],  # b2
            [1, 1, 0],  # b3
            [0, 1, 1],  # b4
            [1, 0, 0],  # p1
            [0, 1, 0],  # p2
            [0, 0, 1],  # p3
        ]

    def decode(self, msg: np.ndarray) -> np.ndarray:
        N: int = msg.shape[0]
        s: np.ndarray = np.matmul(msg, self.HT) % 2
        e = np.zeros((N, 7))
        e[:, 0] = s[:, 0] * s[:, 1] * s[:, 2]  # b1 = s1.s2.s3
        e[:, 1] = s[:, 0] * s[:, 2] * (s[:, 1] + np.ones(N) % 2)  # b2 = s1.!s2.s3
        e[:, 2] = s[:, 0] * s[:, 1] * (s[:, 2] + np.ones(N) % 2)  # b3 = s1.s2.!s3
        e[:, 3] = s[:, 1] * s[:, 2] * (s[:, 0] + np.ones(N) % 2)  # b4 = !s1.s2.s3

        return (msg[:, :4] + e) % 2
