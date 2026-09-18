import secrets
import string
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
WORDLIST_PATH = (Path(__file__).resolve().parent/ "assets"/ "eff_large_wordlist.txt")


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
        raise ValueError("Invalid Diceware wordlist. "f"Expected 7776 words, found {len(words)}.")

    if len(set(words)) != len(words):
        raise ValueError("Invalid Diceware wordlist: ""duplicate words detected.")

    return words


def generate_password(length):
    if length < MIN_LENGTH or length > MAX_LENGTH:
        raise ValueError(
            f"Password length must be between "
            f"{MIN_LENGTH} and {MAX_LENGTH}."
        )

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
        raise ValueError(f"Number of words must be between "f"{MIN_WORDS} and {MAX_WORDS}.")

    wordlist = load_wordlist()
    return "-".join(secrets.choice(wordlist)for _ in range(words))


def show_menu():
    print("\n" + "=" * 45)
    print("       SECURE PASSWORD GENERATOR")
    print("=" * 45)
    print("[1] Generate Password")
    print("[2] Generate Passphrase")
    print("[3] Exit")
    print("=" * 45)


def password_menu():
    print("\n---- Generate Password ----")
    length_input = input(
        f"Enter password length "
        f"({MIN_LENGTH}-{MAX_LENGTH}) "
        f"[default: {DEFAULT_PASSWORD_LENGTH}]: "
    ).strip()

    if length_input == "":
        length = DEFAULT_PASSWORD_LENGTH
    else:
        try:
            length = int(length_input)
        except ValueError:
            print("\nError: Please enter a valid number.")
            return

    try:
        password = generate_password(length)
        print("\nGenerated Password:")
        print(password)
    except ValueError as error:
        print(f"\nError: {error}")


def passphrase_menu():
    print("\n---- Generate Passphrase ----")
    words_input = input(
        f"Enter number of words "
        f"({MIN_WORDS}-{MAX_WORDS}) "
        f"[default: {DEFAULT_WORDS}]: "
    ).strip()

    if words_input == "":
        words = DEFAULT_WORDS
    else:
        try:
            words = int(words_input)
        except ValueError:
            print("\nError: Please enter a valid number.")
            return

    try:
        passphrase = generate_passphrase(words)
        print("\nGenerated Passphrase:")
        print(passphrase)
    except FileNotFoundError as e:
        print(f"\nError: {e}")
    except ValueError as e:
        print(f"\nError: {e}")
    except OSError as e:
        print(f"\nFile system error: {e}")


def main():
    while True:
        show_menu()
        choice = input("Select option: ").strip()
        if choice == "1":
            password_menu()
        elif choice == "2":
            passphrase_menu()
        elif choice == "3":
            print("\nExiting.... See You Soon....")
            break
        else:
            print("\nError: Invalid option. ""Please select 1, 2, or 3.")


if __name__ == "__main__":
    main()
