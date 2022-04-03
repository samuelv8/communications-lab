from encoder import Hamming as HammingEncoder
from channel import Channel
from decoder import Hamming as HammingDecoder
import numpy as np


class System:
    def __init__(self, p: float) -> None:
        self.encoder = HammingEncoder()
        self.channel = Channel(p)
        self.decoder = HammingDecoder()

    def _encode_message(self, msg: np.ndarray) -> np.ndarray:
        return self.encoder.encode(msg)

    def _transmit_message(self, msg: np.ndarray) -> np.ndarray:
        return self.channel.transmit(msg)

    def _decode_message(self, msg: np.ndarray) -> np.ndarray:
        return self.decoder.decode(msg)

    def process_message(self, msg: np.ndarray) -> np.ndarray:
        msg = self._encode_message(msg)
        msg = self._transmit_message(msg)
        return self._decode_message(msg)
