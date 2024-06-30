from constants import ALPHABET


class EnigmaDisk:
    def __init__(self, disk_key: str, rotation: int = 0):
        self.changes = []
        self.rotation = rotation if 0 <= rotation <= 25 else 0
        for char in disk_key:
            char_position = ALPHABET.find(char)
            self.changes.append(char_position)

    def get_num(self, index: int, inverse: bool = False):
        if inverse:
            value_index = (
                self.changes.index((index + self.rotation) % 26) - self.rotation
            ) % 26
            return value_index
        return (self.changes[(index + self.rotation) % 26] - self.rotation) % 26

    def rotate(self):
        self.rotation = (self.rotation + 1) % 26
