"""
Utilities package.

This package contains helper functions and utilities used across the application.
Utilities should be pure functions or simple classes without business logic.

Guidelines
----------
1. Keep utilities stateless when possible
2. Write pure functions that are easy to test
3. Group related utilities in modules
4. Avoid circular imports

Example Modules
---------------
- `datetime_utils.py`: Date/time formatting and parsing
- `string_utils.py`: String manipulation helpers
- `validation_utils.py`: Common validation functions
- `crypto_utils.py`: Hashing and encryption helpers

Usage
-----
Import specific utilities::

    from src.utils.datetime_utils import format_date, parse_date
    from src.utils.string_utils import slugify, truncate

Example Utility Module
----------------------
Create `datetime_utils.py`::

    from datetime import datetime, timezone

    def utc_now() -> datetime:
        '''Get current UTC time.'''
        return datetime.now(timezone.utc)

    def format_iso(dt: datetime) -> str:
        '''Format datetime as ISO 8601 string.'''
        return dt.strftime("%Y-%m-%dT%H:%M:%SZ")

    def parse_iso(s: str) -> datetime:
        '''Parse ISO 8601 datetime string.'''
        return datetime.fromisoformat(s.replace("Z", "+00:00"))

Testing
-------
Utilities should have comprehensive unit tests::

    def test_format_iso():
        dt = datetime(2024, 1, 15, 10, 30, 0, tzinfo=timezone.utc)
        assert format_iso(dt) == "2024-01-15T10:30:00Z"

    def test_parse_iso():
        result = parse_iso("2024-01-15T10:30:00Z")
        assert result.year == 2024
        assert result.month == 1
"""
