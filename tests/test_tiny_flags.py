from collections import OrderedDict

import pytest

from tiny_flags import TinyFlags
from tiny_flags.bitfield import BitField

# ── Fixtures ──


@pytest.fixture
def manager():
    fields = OrderedDict(
        [("language", ["english", "spanish", "french"]), ("dark_mode", False), ("notifications", True)]
    )
    return TinyFlags(fields)


@pytest.fixture
def bitfield_32():
    return BitField(bits64=False)


@pytest.fixture
def bitfield_64():
    return BitField(bits64=True)


# ── BitField unit tests ──


class TestBitField:
    def test_default_is_32_bits(self, bitfield_32):
        assert bitfield_32.bits == 32

    def test_64bit_mode(self, bitfield_64):
        assert bitfield_64.bits == 64

    def test_set_and_get_bit(self, bitfield_32):
        bitfield_32.set_bit(0, 1)
        assert bitfield_32.get_bit(0) == 1

        bitfield_32.set_bit(0, 0)
        assert bitfield_32.get_bit(0) == 0

    def test_set_and_get_bits(self, bitfield_32):
        bitfield_32.set_bits(0, 3, 0b101)
        assert bitfield_32.get_bits(0, 3) == 0b101

    def test_set_bits_clears_previous(self, bitfield_32):
        bitfield_32.set_bits(0, 4, 0b1111)
        bitfield_32.set_bits(0, 4, 0b0010)
        assert bitfield_32.get_bits(0, 4) == 0b0010

    def test_non_overlapping_regions(self, bitfield_32):
        bitfield_32.set_bits(0, 4, 0b1010)
        bitfield_32.set_bits(4, 4, 0b0101)
        assert bitfield_32.get_bits(0, 4) == 0b1010
        assert bitfield_32.get_bits(4, 4) == 0b0101

    def test_position_out_of_range(self, bitfield_32):
        with pytest.raises(ValueError, match="Position"):
            bitfield_32.set_bit(32, 1)

        with pytest.raises(ValueError, match="Position"):
            bitfield_32.get_bit(-1)

    def test_bit_range_overflow(self, bitfield_32):
        with pytest.raises(ValueError, match="Bit range exceeds"):
            bitfield_32.set_bits(30, 4, 0)

    def test_width_out_of_range(self, bitfield_32):
        with pytest.raises(ValueError, match="Width"):
            bitfield_32.set_bits(0, 32, 0)

    def test_64bit_high_positions(self, bitfield_64):
        bitfield_64.set_bit(63, 1)
        assert bitfield_64.get_bit(63) == 1
        assert bitfield_64.get_bit(0) == 0

    def test_str_32bit(self, bitfield_32):
        assert str(bitfield_32) == "0" * 32

    def test_str_64bit(self, bitfield_64):
        assert str(bitfield_64) == "0" * 64

    def test_str_with_value(self, bitfield_32):
        bitfield_32.set_bit(0, 1)
        result = str(bitfield_32)
        assert len(result) == 32
        assert result[-1] == "1"


# ── TinyFlags tests ──


class TestTinyFlagsBoolean:
    def test_initial_values(self, manager):
        assert manager.get_value("dark_mode") is False
        assert manager.get_value("notifications") is True

    def test_set_value(self, manager):
        manager.set_value("dark_mode", True)
        assert manager.get_value("dark_mode") is True

    def test_toggle_back(self, manager):
        manager.set_value("notifications", False)
        assert manager.get_value("notifications") is False
        manager.set_value("notifications", True)
        assert manager.get_value("notifications") is True


class TestTinyFlagsOptions:
    def test_initial_value_is_first_option(self, manager):
        assert manager.get_value("language") == "english"

    def test_set_valid_option(self, manager):
        manager.set_value("language", "spanish")
        assert manager.get_value("language") == "spanish"

    def test_set_invalid_option(self, manager):
        with pytest.raises(ValueError, match="Invalid value"):
            manager.set_value("language", "invalid_language")

    def test_two_option_list(self):
        fields = OrderedDict([("toggle", ["on", "off"])])
        manager = TinyFlags(fields)
        assert manager.bit_widths["toggle"] == 1
        assert manager.get_value("toggle") == "on"
        manager.set_value("toggle", "off")
        assert manager.get_value("toggle") == "off"

    def test_two_option_list_distinct_from_boolean(self):
        fields = OrderedDict([("flag", True), ("choice", ["yes", "no"])])
        manager = TinyFlags(fields)
        manager.set_value("flag", False)
        manager.set_value("choice", "no")
        assert manager.get_value("flag") is False
        assert manager.get_value("choice") == "no"


class TestTinyFlagsBitWidth:
    def test_bit_width_calculation(self):
        fields = OrderedDict(
            [
                ("two_options", ["a", "b"]),
                ("three_options", ["a", "b", "c"]),
                ("four_options", ["a", "b", "c", "d"]),
            ]
        )
        manager = TinyFlags(fields)
        assert manager.bit_widths["two_options"] == 1
        assert manager.bit_widths["three_options"] == 2
        assert manager.bit_widths["four_options"] == 2


class TestTinyFlagsPersistence:
    def test_bitfield_persistence(self):
        fields = OrderedDict([("option", ["a", "b", "c"]), ("flag", True)])
        manager = TinyFlags(fields)
        manager.set_value("option", "b")
        manager.set_value("flag", False)

        value = manager.bitfield.value

        new_manager = TinyFlags(fields)
        new_manager.bitfield.value = value

        assert new_manager.get_value("option") == "b"
        assert new_manager.get_value("flag") is False


class TestTinyFlagsValidation:
    def test_get_unknown_field(self):
        manager = TinyFlags(OrderedDict([]))
        with pytest.raises(ValueError, match="Unknown field"):
            manager.get_value("nonexistent")

    def test_set_unknown_field(self):
        manager = TinyFlags(OrderedDict([]))
        with pytest.raises(ValueError, match="Unknown field"):
            manager.set_value("nonexistent", True)

    def test_invalid_field_type(self):
        with pytest.raises(ValueError, match="must be boolean or list"):
            TinyFlags(OrderedDict([("bad", 42)]))

    def test_single_option_list(self):
        with pytest.raises(ValueError, match="at least 2 options"):
            TinyFlags(OrderedDict([("solo", ["only"])]))

    def test_empty_option_list(self):
        with pytest.raises(ValueError, match="at least 2 options"):
            TinyFlags(OrderedDict([("empty", [])]))


class TestTinyFlags64Bit:
    def test_64bit_mode(self):
        fields = OrderedDict([("flag", True)])
        manager = TinyFlags(fields, bits64=True)
        assert manager.bitfield.bits == 64

    def test_many_fields_64bit(self):
        options = [f"opt_{i}" for i in range(16)]
        fields = OrderedDict(
            [
                ("a", options),
                ("b", options),
                ("c", options),
                ("flag", False),
            ]
        )
        manager = TinyFlags(fields, bits64=True)
        manager.set_value("a", "opt_15")
        manager.set_value("c", "opt_7")
        manager.set_value("flag", True)
        assert manager.get_value("a") == "opt_15"
        assert manager.get_value("b") == "opt_0"
        assert manager.get_value("c") == "opt_7"
        assert manager.get_value("flag") is True
