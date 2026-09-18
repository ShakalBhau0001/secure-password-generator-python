import argparse
import secrets
import string
import sys
from pathlib import Path

MIN_LENGTH = 12
MAX_LENGTH = 128
DEFAULT_PASSWORD_LENGTH = 16
MIN_WORDS = 6
MAX_WORDS = 20
DEFAULT_WORDS = 6
SPECIAL = "!@#$%^&*()-_=+"
LOWERCASE = string.ascii_lowercase
UPPERCASE = string.ascii_uppercase
DIGITS = string.digits
ALL_CHARS = LOWERCASE + UPPERCASE + DIGITS + SPECIAL
WORDLIST_PATH = Path(__file__).resolve().parent / "assets" / "eff_large_wordlist.txt"


def load_wordlist():
    if not WORDLIST_PATH.is_file():
        raise FileNotFoundError(f"Diceware wordlist not found: {WORDLIST_PATH}")

    words = []
    with WORDLIST_PATH.open(
        "r",
        encoding="utf-8",
    ) as file:
        for line in file:
            line = line.strip()

            if not line:
                continue

            parts = line.split()
            if len(parts) >= 2:
                word = parts[-1]
                words.append(word)

    if len(words) != 7776:
        raise ValueError(f"Invalid Diceware wordlist. Expected 7776 words, found {len(words)}.")

    if len(set(words)) != len(words):
        raise ValueError("Invalid Diceware wordlist: duplicate words detected.")

    return words


def generate_password(length):
    if length < MIN_LENGTH or length > MAX_LENGTH:
        raise ValueError(f"Password length must be between {MIN_LENGTH} and {MAX_LENGTH}.")

    password = [
        secrets.choice(LOWERCASE),
        secrets.choice(UPPERCASE),
        secrets.choice(DIGITS),
        secrets.choice(SPECIAL),
    ]

    for _ in range(length - 4):
        password.append(secrets.choice(ALL_CHARS))

    secrets.SystemRandom().shuffle(password)
    return "".join(password)


def generate_passphrase(words):
    if words < MIN_WORDS or words > MAX_WORDS:
        raise ValueError(f"Number of words must be between {MIN_WORDS} and {MAX_WORDS}.")

    wordlist = load_wordlist()
    return "-".join(secrets.choice(wordlist) for _ in range(words))


def create_parser():
    parser = argparse.ArgumentParser(description=("Secure random password and Diceware passphrase generator"))
    subparsers = parser.add_subparsers(
        dest="mode",
        required=True,
    )

    password_parser = subparsers.add_parser(
        "pwd",
        help="Generate a secure random password",
    )

    password_parser.add_argument(
        "-l",
        "--length",
        type=int,
        default=DEFAULT_PASSWORD_LENGTH,
        help=(f"Password length (default: {DEFAULT_PASSWORD_LENGTH})"),
    )

    passphrase_parser = subparsers.add_parser(
        "phr",
        help="Generate a secure Diceware passphrase",
    )

    passphrase_parser.add_argument(
        "-w",
        "--words",
        type=int,
        default=DEFAULT_WORDS,
        help=(f"Number of words (default: {DEFAULT_WORDS})"),
    )
    return parser


def main():
    parser = create_parser()
    args = parser.parse_args()
    try:
        if args.mode == "pwd":
            secret_value = generate_password(args.length)
            print("\nGenerated Password:")
            print(secret_value)
        elif args.mode == "phr":
            secret_value = generate_passphrase(args.words)
            print("\nGenerated Passphrase:")
            print(secret_value)
    except FileNotFoundError as e:
        print(f"\nError: {e}")
        sys.exit(1)
    except ValueError as e:
        print(f"\nError: {e}")
        sys.exit(1)
    except OSError as e:
        print(f"\nFile system error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
