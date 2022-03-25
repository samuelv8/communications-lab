from encoder import Hamming as HammingEncoder
from channel import Channel
from decoder import Hamming as HammingDecoder
from lab1.main import generate_bits


class System:
    def __init__(self) -> None:
        print('new system created')
        self.encoder = HammingEncoder()
        self.channel = Channel()
        self.decoder = HammingDecoder()
        self.original_msg = generate_bits()
        self.encoded_msg 
        self.received_msg
        self.decoded_msg

    def _encode_message(self, msg):
        pass

    def _transmit_word(self, word):
        pass

    def _decode_word(self, word):
        pass
    
    def process_message(self, msg):
        pass
