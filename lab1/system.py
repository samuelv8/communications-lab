from encoder import Hamming as HammingEncoder
from channel import Channel
from decoder import Hamming as HammingDecoder

class System:
    def __init__(self) -> None:
        print('new system created')
        self.encoder = HammingEncoder()
        self.channel = Channel()
        self.decoder = HammingDecoder()

    def _encode_message(self, msg):
        pass

    def _transmit_word(self, word):
        pass

    def _decode_word(self, word):
        pass
    
    def process_message(self, msg):
        pass
