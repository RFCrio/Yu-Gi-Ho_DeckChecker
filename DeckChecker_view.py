import os

from DeckChecker_model import Card


class ConsoleView:
    def ask(self, prompt: str) -> str:
        return input(prompt).strip()

    def ask_int(self, prompt: str):
        """Retorna int ou None se a entrada for inválida."""
        try:
            return int(input(prompt))
        except ValueError:
            return None

    def confirm(self, prompt: str) -> bool:
        return input(f"{prompt} (y/n): ").strip().lower() != 'n'

    def pause(self) -> None:
        input("Press Enter to continue...")

    def message(self, text: str) -> None:
        print(text)

    def clear(self) -> None:
        try:
            from IPython.display import clear_output
            clear_output(wait=True)
        except ImportError:
            os.system('cls' if os.name == 'nt' else 'clear')

    def show_menu(self) -> str:
        print("\nYu-Gi-Oh! Deck Checker Menu:")
        print("1. Add a card to the deck checker")
        print("2. List all cards in the deck checker")
        print("3. Change the quantity of a card")
        print("4. Show ban list")
        print("0. Exit")
        return input("Enter your choice (0-4): ")

    def show_cards(self, cards: list[Card]) -> None:
        def f(v):
            return '-' if v is None else v

        print("Cards in the deck checker:")
        for c in cards:
            print(f"Name: {c.name}, Type: {c.type}, ATK: {f(c.atk)}, "
                  f"DEF: {f(c.defense)}, Level: {f(c.level)}, "
                  f"Race: {c.race}, Attribute: {f(c.attribute)}")

    def show_banlist(self, entries: list[tuple[str, str]]) -> None:
        for name, status in entries:
            print(f"{name}: {status}")
