# tiny_flags
A lightweight Python package for efficient settings management and manipulation. Easily handle language preferences, settings, and other flag-based configurations using minimal memory.
Still under construction, but development package works as it should.

Features:
32-bit and 64-bit bitfield support (reserve one 32/64 bit integer in database tha)
Automatic bit position management
Boolean flags and multi-option settings
Ordered dictionary configuration
Type-safe operations
Memory efficient
Perfect for storing for example app settings that do not need indexing on DB.

Installation:
Install using pip:
pip install tiny_flags (not yet)

### How to use?

## Imports

Requires OrderedDict

from collections import OrderedDict
from tiny_flags import TinyFlags

## Define your settings
fields = OrderedDict([
    ('language', ['english', 'spanish', 'french']),  # Uses 2 bits
    ('dark_mode', False),                            # Uses 1 bit, initial value
    ('notifications', True)                          # Uses 1 bit, initial value
])

## Initialize manager
manager = TinyFlags(fields) # Default value is 32bit, but give True for 64bit, TinyFlags(fields, True)
manager.setup_fields() # calculates fields 

## Set values
manager.set_value('language', 'spanish')
manager.set_value('dark_mode', True)

## Get values
print(manager.get_value('language'))       # 'spanish'
print(manager.get_value('dark_mode'))      # True
print(manager.get_value('notifications'))  # True

## Detailed Usage


## Reading boolean flags
is_dark = manager.get_value('dark_mode')
Multi-option Settings
pythonCopy# Define options
fields = OrderedDict([
    ('theme', ['light', 'dark', 'system']),
    ('language', ['en', 'es', 'fr', 'de'])
])

## Testing and development
Setup Development Environment & clone the repository
git clone https://github.com/yourusername/tiny-flags.git
cd tiny-flags
Install requirements (just pytest atm)
pip install -e .
Running Tests
pytest tests/
Contributions are welcome

## License
Distributed under the MIT License. See LICENSE for more information.

## Todo
Set initial values for lists
Optimize validations
Add more option mappings possibilities
See if 32/64bit values should have a forced type
Test with actual DB (MongoDB 32/64 bit ints)
Clean up README.md
Add linting to project