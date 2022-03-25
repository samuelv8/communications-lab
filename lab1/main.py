from http.client import IM_USED
from system import System
from random import seed
from random import random
from random import randint
import numpy as np


def generate_bits(n_messages: int = 250_000, message_length: int = 4):
    return np.random.randint(0, 2, (n_messages, message_length))


def calculate_probability(original_msg: np.ndarray, decoded_msg:np.ndarray):
    diff_table: np.ndarray = original_msg != decoded_msg
    probability = sum(sum(diff_table))/diff_table.size
    return probability



if (__name__ == '__main__'):
    print('hello, Manish')

    lista_p = [0.5, 0.2, 0.1, 0.05, 0.02, 0.01, 0.005]

    system = System()