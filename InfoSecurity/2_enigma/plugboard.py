class Plugboard:
    def __init__(self, mapping):
        """
        Args mapping: 'AB DT QL'
        """
        self.mapping_str = mapping
        mapping = mapping.split() + mapping[::-1].split()
        self.mapping = dict(mapping)
        print(self.mapping)

    def exchange(self, char):
        return self.mapping[char] if char in self.mapping else char

    def __str__(self) -> str:
        return f'{self.mapping_str}'


# Merge dict
# z = x | y      # 3.9+ ONLY
# z = {**x, **y}
