#!/usr/bin/env python3
"""
Rotate API Keys.

This script helps with API key rotation by generating new keys and providing
instructions for zero-downtime rotation.

Usage:
    python scripts/rotate_api_keys.py

Rotation Process:
    1. Generate new key(s)
    2. Add new key(s) to API_KEYS (alongside existing keys)
    3. Deploy application
    4. Update clients to use new key(s)
    5. Remove old key(s) from API_KEYS
    6. Deploy application again

This ensures no service interruption during rotation.
"""

import argparse
import os
import secrets
import string
from datetime import datetime


def generate_api_key(prefix: str = "api", length: int = 32) -> str:
    """Generate a secure API key."""
    alphabet = string.ascii_letters + string.digits
    random_part = "".join(secrets.choice(alphabet) for _ in range(length))
    return f"{prefix}_{random_part}"


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Rotate API keys with zero-downtime process",
    )
    parser.add_argument(
        "--prefix",
        "-p",
        type=str,
        default="api",
        help="Prefix for new API key (default: api)",
    )
    parser.add_argument(
        "--count",
        "-c",
        type=int,
        default=1,
        help="Number of new keys to generate (default: 1)",
    )

    args = parser.parse_args()

    # Get current keys from environment
    current_keys = os.environ.get("API_KEYS", "").split(",")
    current_keys = [k.strip() for k in current_keys if k.strip()]

    print("=" * 60)
    print("API Key Rotation")
    print("=" * 60)
    print()
    print(f"Timestamp: {datetime.now().isoformat()}")
    print()

    # Show current keys (masked)
    print("Current Keys:")
    if current_keys:
        for key in current_keys:
            masked = key[:8] + "..." + key[-4:] if len(key) > 12 else "****"
            print(f"  - {masked}")
    else:
        print("  (No API_KEYS environment variable set)")
    print()

    # Generate new keys
    new_keys = [generate_api_key(args.prefix) for _ in range(args.count)]

    print("New Keys Generated:")
    for key in new_keys:
        print(f"  {key}")
    print()

    # Show rotation instructions
    print("-" * 60)
    print("ROTATION STEPS:")
    print("-" * 60)
    print()
    print("1. ADD new key(s) to API_KEYS (keep existing keys):")
    all_keys = current_keys + new_keys
    print(f"   API_KEYS={','.join(all_keys)}")
    print()
    print("2. DEPLOY application with updated API_KEYS")
    print()
    print("3. UPDATE all clients to use new key(s)")
    print()
    print("4. VERIFY clients are using new keys (check logs)")
    print()
    print("5. REMOVE old key(s) from API_KEYS:")
    print(f"   API_KEYS={','.join(new_keys)}")
    print()
    print("6. DEPLOY application again")
    print()
    print("-" * 60)
    print("IMPORTANT: Do NOT skip steps or rotate too quickly!")
    print("Allow time for clients to update between steps.")
    print("-" * 60)


if __name__ == "__main__":
    main()
