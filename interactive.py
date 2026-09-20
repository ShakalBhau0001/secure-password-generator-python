import secrets
import string
from pathlib import Path

from rich import box
from rich.align import Align
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.rule import Rule
from rich.table import Table
from rich.text import Text

# Configuration
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


console = Console()


def print_banner():
    console.clear()
    banner = Text()
    banner.append("███████╗███████╗ ██████╗██████╗ ██╗    ██╗██████╗  ██████╗ ███████╗███╗   ██╗\n", style="bold cyan",)
    banner.append("██╔════╝██╔════╝██╔════╝██╔══██╗██║    ██║██╔══██╗██╔════╝ ██╔════╝████╗  ██║\n", style="bold cyan",)
    banner.append("███████╗█████╗  ██║     ██████╔╝██║ █╗ ██║██║  ██║██║  ███╗█████╗  ██╔██╗ ██║\n", style="bold blue",)
    banner.append("╚════██║██╔══╝  ██║     ██╔═══╝ ██║███╗██║██║  ██║██║   ██║██╔══╝  ██║╚██╗██║\n", style="bold blue",)
    banner.append("███████║███████╗╚██████╗██║     ╚███╔███╔╝██████╔╝╚██████╔╝███████╗██║ ╚████║\n", style="bold magenta",)
    banner.append("╚══════╝╚══════╝ ╚═════╝╚═╝      ╚══╝╚══╝ ╚═════╝  ╚═════╝ ╚══════╝╚═╝  ╚═══╝\n\n", style="bold magenta",)
    banner.append("Secure Password • Diceware Passphrase Generator",style="dim white",)
    console.print(
        Panel(
            Align.center(banner),
            border_style="cyan",
            box=box.DOUBLE_EDGE,
        )
    )


def divider(title=""):
    console.print(
        Rule(
            title,
            style="cyan",
        )
    )


def success(message):
    console.print(f"\n[bold green]✔[/bold green] {message}\n")


def error(message):
    console.print(f"\n[bold red]✘[/bold red] {message}\n")


def info(message):
    console.print(f"[bold yellow]ℹ[/bold yellow] {message}")


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

def menu():
    table = Table(
        title="Main Menu",
        title_style="bold cyan",
        box=box.DOUBLE_EDGE,
        border_style="cyan",
        padding=(0, 2),
    )
    table.add_column(
        "Option",
        justify="center",
        style="bold yellow",
    )
    table.add_column("Action",style="green",)
    table.add_row("1","🔒 Generate Password",)
    table.add_row("2","🔑 Generate Passphrase",)
    table.add_row("3","ℹ About",)
    table.add_row("0","🚪 Exit",)
    console.print(table)


def pwd_menu():
    divider("🔒 Generate Password")
    length_input = Prompt.ask(
        f"[bold cyan]Enter password length "
        f"({MIN_LENGTH}-{MAX_LENGTH}) "
        f"[default: {DEFAULT_PASSWORD_LENGTH}]: [/bold cyan]",
        default=str(DEFAULT_PASSWORD_LENGTH),
    ).strip()

    try:
        len = int(length_input)
        pwd = generate_password(len)
        success("Secure password generated successfully.")
        console.print(
            Panel(
                pwd,
                title="Generated Password",
                border_style="green",
                box=box.ROUNDED,
            )
        )
    except ValueError as exc:
        error(str(exc))


def phr_menu():
    divider("🔑 Generate Passphrase")
    words_input = Prompt.ask(
        f"[bold cyan]Enter number of words "
        f"({MIN_WORDS}-{MAX_WORDS}) "
        f"[default: {DEFAULT_WORDS}]: [/bold cyan]",
        default=str(DEFAULT_WORDS),
    ).strip()

    try:
        words = int(words_input)
        phr = generate_passphrase(words)
        success("Secure passphrase generated successfully.")
        console.print(
            Panel(
                phr,
                title="Generated Passphrase",
                border_style="green",
                box=box.ROUNDED,
            )
        )
    except (ValueError, FileNotFoundError) as exc:
        error(str(exc))



def about():
    divider("ℹ About Toolkit")
    table = Table(
        show_header=True,
        header_style="bold cyan",
        box=box.ROUNDED,
        border_style="cyan",
    )
    table.add_column("Property",style="yellow",)
    table.add_column("Value",style="green",)
    table.add_row("Purpose","Secure Password & Passphrase Generation",)
    table.add_row("Password RNG","Python secrets module",)
    table.add_row("Passphrase","Diceware",)
    table.add_row("Wordlist","EFF Large Wordlist",)
    table.add_row("Word Count",f"{MIN_WORDS}-{MAX_WORDS}",)
    table.add_row("Password Length",f"{MIN_LENGTH}-{MAX_LENGTH}",)
    table.add_row("Language","Python",)
    table.add_row("UI","Rich CLI",)
    console.print(table)


def main():
    while True:
        print_banner()
        menu()
        choice = Prompt.ask(
            "\n[bold cyan]Select Option[/bold cyan]",
            choices=["1", "2", "3", "0"],
            default="1",
        )
        if choice == "1":
            pwd_menu()
        elif choice == "2":
            phr_menu()
        elif choice == "3":
            about()
        elif choice == "0":
            console.print()
            console.print(
                Panel(
                    Align.center(
                        Text(
                            "See You Soon! | Stay safe, stay secure. 🕵️",
                            style="bold cyan",
                        )
                    ),
                    border_style="magenta",
                    box=box.DOUBLE_EDGE,
                )
            )
            break
        Prompt.ask("\n[dim]Press Enter to return to menu…[/dim]",default="",)


if __name__ == "__main__":
    main()
