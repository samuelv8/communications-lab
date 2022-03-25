from abc import ABC
import numpy as np

class Encoder(ABC):
    def __init__(self) -> None:
        super().__init__()
    
    def encode(self):
        raise NotImplementedError('Método abstrato')


class Hamming(Encoder):
    def __init__(self) -> None:
        super().__init__()
        self.G = [  [1, 0, 0, 0, 1, 1, 1],
                    [0, 1, 0, 0, 1, 0, 1],
                    [0, 0, 1, 0, 1, 1, 0],
                    [0, 0, 0, 1, 0, 1, 1]]
        print('hamming encoder created')
    
    def encode(self, Original_msg: np.array):
        
        return np.matmul(Original_msg, self.G)
