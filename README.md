# tiny_flags

A lightweight Python package for efficient settings management using bitfields. Handle language preferences, feature flags, and other configurations using a single 32 or 64-bit integer.

### Features

* 32-bit and 64-bit bitfield support
* Automatic bit position management
* Boolean flags and multi-option settings
* Ordered dictionary configuration
* Zero runtime dependencies
* Type-checked with mypy strict mode

## Installation

```bash
pip install tiny_flags
```

## Quick Start

```python
from collections import OrderedDict
from tiny_flags import TinyFlags

# Define your settings
fields = OrderedDict([
    ('language', ['english', 'spanish', 'french']),  # Uses 2 bits
    ('dark_mode', False),                            # Uses 1 bit
    ('notifications', True)                          # Uses 1 bit
])

# Initialize (default 32-bit, pass bits64=True for 64-bit)
manager = TinyFlags(fields)

# Set values
manager.set_value('language', 'spanish')
manager.set_value('dark_mode', True)

# Get values
manager.get_value('language')        # 'spanish'
manager.get_value('dark_mode')       # True
manager.get_value('notifications')   # True

# Persist the entire state as a single integer
state = manager.bitfield.value       # e.g. 13

# Restore from that integer later
new_manager = TinyFlags(fields)
new_manager.bitfield.value = state
new_manager.get_value('language')    # 'spanish'
```

## How Bit Widths Work

| Field type | Bits used | Example |
|------------|-----------|---------|
| Boolean | 1 | `('dark_mode', False)` |
| 2 options | 1 | `('toggle', ['on', 'off'])` |
| 3-4 options | 2 | `('lang', ['en', 'es', 'fr'])` |
| 5-8 options | 3 | 8 options fit in 3 bits |
| 9-16 options | 4 | 16 options fit in 4 bits |

Option lists must have at least 2 items. Bit allocation is always based on powers of 2, so odd-count lists leave unused slots. Consider reserving those for future options.

## Design Considerations

**Order matters.** The `OrderedDict` key order determines bit positions. Changing the order after data is persisted will corrupt stored values. When evolving your schema:
- Add new fields at the end
- Don't remove fields — rename unused ones with a `_` prefix and ignore them

**Database storage.** The bitfield value is a single integer, making it efficient to store. However, you cannot query individual flags with database indexes — the index covers the whole integer. If you need complex queries on specific flags, store those as separate columns.

**32 vs 64-bit.** Default is 32-bit (up to 32 flags/option bits). Pass `bits64=True` for 64-bit support. Ensure your storage layer supports 64-bit integers before using this mode.

## Development

```bash
git clone https://github.com/FistOfTheNorthStar/tiny_flags
cd tiny_flags
pip install -e ".[dev]"
```

### Run checks

```bash
pytest --cov=tiny_flags           # tests + coverage
ruff check src/ tests/            # linting
mypy src/                         # type checking
```

Contributions are welcome.

## License

Distributed under the MIT License. See LICENSE for more information.
