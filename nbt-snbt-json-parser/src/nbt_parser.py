class NbtParser:
    def __init__(self):
        pass

    def parse_snbt(self, snbt_string):
        from nbtlib import nbt
        return nbt.parse(snbt_string)

    def to_json(self, nbt_data):
        return nbt_data.to_json()