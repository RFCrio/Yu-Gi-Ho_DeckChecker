from DeckChecker_model import DeckRepository, YgoprodeckAPI, MAX_COPIES
from DeckChecker_view import ConsoleView


class DeckController:
    def __init__(self, repo: DeckRepository, api: YgoprodeckAPI, view: ConsoleView):
        self.repo = repo
        self.api = api
        self.view = view

    def run(self) -> None:
        actions = {
            '1': self.add_card,
            '2': self.list_cards,
            '3': self.change_quantity,
            '4': self.show_banlist,
        }
        while True:
            choice = self.view.show_menu()
            if choice == '0':
                self.view.message("Closing Yu-Gi-Oh! Deck Checker.")
                break
            action = actions.get(choice)
            if action:
                action()
                self.view.clear()
            else:
                self.view.message("Invalid choice. Please enter a number between 0 and 4.")
                self.view.pause()
                self.view.clear()

    def add_card(self) -> None:
        v = self.view
        name = v.ask("Enter the card name: ")
        if not name:
            v.message("Please enter a valid card name.")
            return v.pause()

        card = self.api.get_card_by_name(name)
        if card is None:
            v.message("Card not found. Please try using card ID.")
            card_id = v.ask("Enter the card ID: ")
            card = self.api.get_card_by_id(card_id) if card_id else None

        if card is None:
            v.message("Card not found. Please try again.")
            return v.pause()

        if card.ban_tcg and not v.confirm(
                f"This card is {card.ban_tcg}. Are you sure you want to add it to the deck checker?"):
            v.message("Card not added.")
            return v.pause()

        if not card.is_complete():
            v.message("Incomplete card data.")
            return v.pause()

        owned = self.repo.count(card.name)
        remaining = MAX_COPIES - owned
        if remaining <= 0:
            v.message(f"Maximum number of {card.name} cards reached.")
            return v.pause()

        v.message(f"You already have {owned} copies of {card.name}. "
                  f"You can add {remaining} more copies.")
        copies = v.ask_int(f"How many copies of {card.name} would you like to add? (Max {remaining}): ")
        if copies is None:
            v.message("Invalid input. Please enter a valid number.")
            return v.pause()
        if not 0 <= copies <= remaining:
            v.message(f"Invalid number of copies. Please enter a number between 0 and {remaining}.")
            return v.pause()

        self.repo.add(card, copies)
        v.message(f"{copies} copies of {card.name} added to the deck checker.")
        v.pause()

    def list_cards(self) -> None:
        cards = self.repo.load()
        if not cards:
            self.view.message("No cards in the deck checker.")
        else:
            self.view.show_cards(cards)
        self.view.pause()

    def change_quantity(self) -> None:
        v = self.view
        name = v.ask("Enter the card name you want to change the quantity of: ")
        current = self.repo.count(name)
        if current == 0:
            v.message(f"No copies of {name} found in the deck checker.")
            return v.pause()

        v.message(f"You currently have {current} copies of {name}.")
        new_qty = v.ask_int(f"Enter the new quantity for {name} (0 to remove all): ")
        if new_qty is None:
            v.message("Invalid input. Please enter a valid number.")
            return v.pause()
        if not 0 <= new_qty <= MAX_COPIES:
            v.message(f"Invalid quantity. Please enter a number between 0 and {MAX_COPIES}.")
            return v.pause()

        self.repo.set_quantity(name, new_qty)
        if new_qty == 0:
            v.message(f"All copies of {name} removed from the deck checker.")
        else:
            v.message(f"The quantity of {name} has been updated to {new_qty}.")
        v.pause()

    def show_banlist(self) -> None:
        entries = self.api.get_tcg_banlist()
        if entries is None:
            self.view.message("Error to show Ban List")
            return self.view.pause()
        self.view.show_banlist(entries)
        self.view.pause()
