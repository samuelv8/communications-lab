from abc import ABC

class Decoder(ABC):
    def __init__(self) -> None:
        super().__init__()
    
    def decode(self):
        raise NotImplementedError('Método abstrato')


class Hamming(Decoder):
    def __init__(self) -> None:
        super().__init__()
        print('hamming decoder created')
    
    def decode(self):
        pass
