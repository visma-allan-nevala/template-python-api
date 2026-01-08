#!/usr/bin/env python3
"""
Generate Secure API Keys.

This script generates cryptographically secure API keys for authentication.

Usage:
    python scripts/generate_api_keys.py                    # Generate 1 key
    python scripts/generate_api_keys.py --count 5          # Generate 5 keys
    python scripts/generate_api_keys.py --prefix myapp     # Custom prefix

Output:
    Keys are printed to stdout. Add them to your API_KEYS environment variable.

Example:
    $ python scripts/generate_api_keys.py --count 2 --prefix api
    api_Rk9Y2mX8dH3pN7qW1vT6bC4jL0sF5aE9gI2uO8yA1xZ3
    api_Hm4Kp7Qw2Ej9Rx1Tb6Yc3Vf0Ln5Sg8Di4Uo7Ai2Ox6Za
"""

import argparse
import secrets
import string


def generate_api_key(prefix: str = "api", length: int = 32) -> str:
    """
    Generate a secure API key.

    Parameters
    ----------
    prefix : str
        Prefix for the key (default: "api")
    length : int
        Length of the random portion (default: 32)

    Returns
    -------
    str
        Generated API key in format: {prefix}_{random_string}
    """
    # Use URL-safe characters
    alphabet = string.ascii_letters + string.digits
    random_part = "".join(secrets.choice(alphabet) for _ in range(length))
    return f"{prefix}_{random_part}"


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate secure API keys for authentication",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    %(prog)s                        # Generate 1 key with default prefix
    %(prog)s --count 5              # Generate 5 keys
    %(prog)s --prefix myapp         # Use custom prefix
    %(prog)s --length 48            # Longer random portion
        """,
    )
    parser.add_argument(
        "--count",
        "-c",
        type=int,
        default=1,
        help="Number of keys to generate (default: 1)",
    )
    parser.add_argument(
        "--prefix",
        "-p",
        type=str,
        default="api",
        help="Prefix for the API key (default: api)",
    )
    parser.add_argument(
        "--length",
        "-l",
        type=int,
        default=32,
        help="Length of random portion (default: 32)",
    )

    args = parser.parse_args()

    print(f"# Generated {args.count} API key(s) with prefix '{args.prefix}'")
    print("# Add to API_KEYS environment variable (comma-separated)")
    print()

    keys = [generate_api_key(args.prefix, args.length) for _ in range(args.count)]

    for key in keys:
        print(key)

    if args.count > 1:
        print()
        print("# Combined for .env file:")
        print(f"API_KEYS={','.join(keys)}")


if __name__ == "__main__":
    main()
