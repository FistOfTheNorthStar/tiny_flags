from .validations import BitFieldValidation


class BitField:
    def __init__(self, bits64: bool = False) -> None:
        self.value: int = 0
        self.bits: int = 64 if bits64 else 32
        self.validations = BitFieldValidation(self.bits)

    def set_bit(self, position: int, bit_value: int) -> int:
        """Set a bit at given position (0-31/63) to 0 or 1"""
        self.validations.validate_position(position)

        if bit_value:
            self.value |= 1 << position
        else:
            self.value &= ~(1 << position)
        return self.value

    def get_bit(self, position: int) -> int:
        """Get bit value at given position (0-31/63)"""
        self.validations.validate_position(position)
        return (self.value >> position) & 1

    def set_bits(self, start_position: int, width: int, bit_values: int) -> int:
        """Set multiple bits starting at position with given width"""
        self.validations.validate_start_position_and_width(start_position, width)

        # Create mask and clear bits in range
        mask = ((1 << width) - 1) << start_position
        self.value &= ~mask

        # Set new value
        self.value |= (bit_values & ((1 << width) - 1)) << start_position
        return self.value

    def get_bits(self, start_position: int, width: int) -> int:
        """Get multiple bits starting at position with given width"""
        self.validations.validate_start_position_and_width(start_position, width)

        mask = ((1 << width) - 1) << start_position
        return (self.value & mask) >> start_position

    def __str__(self) -> str:
        return f"{self.value:0{self.bits}b}"
