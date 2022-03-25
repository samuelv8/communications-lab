from base64 import encode
from operator import xor
from random import seed
from random import random
import numpy as np


class Channel:
    def __init__(self, p: float = 0.5) -> None:
        print('channel created')
        self.error_probability = p
        

    def transmit(self, encoded_msg: np.array):
        
        corrupted = np.random.rand(*encoded_msg.shape) < self.error_probability
            
        return np.logical_xor(encoded_msg, corrupted)  

    
    