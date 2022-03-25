from abc import ABC

class Encoder(ABC):
    def __init__(self) -> None:
        super().__init__()
    
    def decode(self):
        raise NotImplementedError('Método abstrato')


class Hamming(Encoder):
    def __init__(self) -> None:
        super().__init__()
        print('hamming encoder created')
    
    def decode(self):
        pass
