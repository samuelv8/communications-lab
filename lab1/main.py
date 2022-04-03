import numpy as np
import pandas as pd

from system import System


def generate_bits(n_messages: int = 250_000, message_length: int = 4):
    return np.random.randint(0, 2, (n_messages, message_length))


def calculate_bit_error_probability(original_msg: np.ndarray, decoded_msg: np.ndarray):
    diff_table: np.ndarray = original_msg != decoded_msg
    probability = sum(sum(diff_table)) / diff_table.size
    return probability


if __name__ == "__main__":
    print("hello, Manish")

    # fmt: off
    ps = [0.000002,0.000005,0.00001,0.00002,0.00005,0.0001,0.0002,0.0005,               
        0.001,0.002,0.005,0.01,0.02,0.05,0.1,0.2,0.5] 
    # fmt: on

    bit_errors = []

    for p_value in ps:
        original_msg = generate_bits()
        decoded_msg = original_msg.copy()
        system = System(p_value)
        decoded_msg = system.process_message(decoded_msg)

        bit_error = calculate_bit_error_probability(original_msg, decoded_msg)
        bit_errors.append(bit_error)

    df = pd.DataFrame.from_dict({"p": ps, "bit_error": bit_errors})

    df.to_csv("results.csv")
