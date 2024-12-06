class BitFieldValidation:
    def __init__(self, bits):
        self.bits = bits

    def validate_position_or_width(self, position, error_prefix):
        if not 0 <= position <= self.bits - 1:
            raise ValueError(f"{error_prefix} must be between 0 and {self.bits - 1}")

    def validate_bit_value(self, bit_value):
        if bit_value not in (0, 1):
            raise ValueError("Bit value must be 0 or 1")

    def validate_bit_range(self, bit_range):
        if bit_range > self.bits:
            raise ValueError(f"Bit range exceeds {self.bits} bits")

    def validate_bit_with_position(self, position, bit_value):
        self.validate_position(position)
        self.validate_bit_value(bit_value)

    def validate_start_position_and_width(self, start_position, width, bit_value=None):
        self.validate_position_or_width(start_position, "Start position")
        self.validate_position_or_width(start_position, "Width")
        self.validate_bit_range(start_position + width)
        bit_value and self.validate_bit_value(bit_value)

    def validate_position(self, position):
        self.validate_position_or_width(position, "Position")