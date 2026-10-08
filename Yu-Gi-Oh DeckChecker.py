#Deck Checker for Yu-Gi-Oh! cards.
import json
import os
import requests

deck_checker = 'Checker.json'

def load_deck_checker():
    if not os.path.exists(deck_checker):
        return {}
    with open(deck_checker, 'r') as f:
        return json.load(f)

def save_deck_checker(data):
    with open(deck_checker, 'w') as f:
        json.dump(data, f, indent=4)

def search_api(yugioh_name):
    url = f'https://db.ygoprodeck.com/api/v7/cardinfo.php?{yugioh_name}'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return None

def add_card_to_checker(yugioh_name, card_data):
    Checker = load_deck_checker()

    name = input("Enter the card name: ")
    if not name:
        print("Please enter a valid card name.")
        return

    API_data = search_api(yugioh_name)

    new_card = None
    type = None
    desc = None
    atk = None
    defn = None
    level = None
    race = None
    attribute = None

    if API_data:
        for card in API_data['data']:
            if card['name'].lower() == yugioh_name.lower():
                new_card = card
                type = card.get('type', None)
                desc = card.get('desc', None)
                atk = card.get('atk', None)
                defn = card.get('def', None)
                level = card.get('level', None)
                race = card.get('race', None)
                attribute = card.get('attribute', None)
                break

    if not new_card:
        print("Card not found. Please try using card ID.")
        new_ID = input("Enter the card ID: ")
        API_data = search_api(new_ID)
        if API_data:
            for card in API_data['data']:
                if card['id'] == new_ID:
                    new_card = card
                    type = card.get('type', None)
                    desc = card.get('desc', None)
                    atk = card.get('atk', None)
                    defn = card.get('def', None)
                    level = card.get('level', None)
                    race = card.get('race', None)
                    attribute = card.get('attribute', None)
                    break

        if not new_card:
            print("Card not found. Please try again.")
            return
    elif not type:
        print("Incomplete card data. Please try again.")
        return
    elif not desc:
        print("Card description is missing. Please try again.")
        return
    elif not atk:
        print("Card attack value is missing. Please try again.")
        return
    elif not defn:
        print("Card defense value is missing. Please try again.")
        return
    elif not level:
        print("Card level is missing. Please try again.")
        return
    elif not race:
        print("Card race is missing. Please try again.")
        return
    elif not attribute:
        print("Card attribute is missing. Please try again.")
        return

    
    if any(card['name'].lower() == yugioh_name.lower() for card in Checker.get('cards', [])):
        print("Card already exists in the deck checker.")
        return

    Duplicate = sum(1 for card in Checker.get('cards', []) if card['name'].lower() == yugioh_name.lower())
    limit = 4 - Duplicate

    if Duplicate >= limit:
        print(f"Maximum number of {yugioh_name} cards reached.")
        return

    print(f"you already have {Duplicate} copies of {yugioh_name}. You can add {limit} more copies.")
    try:
        copies_to_add = int(input(f"How many copies of {yugioh_name} would you like to add? (Max {limit}): "))
        if copies_to_add < 1 or copies_to_add > limit:
            print(f"Invalid number of copies. Please enter a number between 1 and {limit}.")
            return
    except ValueError:
        print("Invalid input. Please enter a valid number.")
        return
    for i in range(copies_to_add):
        Checker.setdefault('cards', []).append({
            'name': yugioh_name,
            'type': type,
            'desc': desc,
            'atk': atk,
            'def': defn,
            'level': level,
            'race': race,
            'attribute': attribute
        })
    save_deck_checker(Checker)
    print(f"{copies_to_add} copies of {yugioh_name} added to the deck checker.")


def list_cards_in_checker():
    Checker = load_deck_checker()
    if not Checker.get('cards'):
        print("No cards in the deck checker.")
        return
    print("Cards in the deck checker:")
    for card in Checker['cards']:
        print(f"Name: {card['name']}, Type: {card['type']}, ATK: {card['atk']}, DEF: {card['def']}, Level: {card['level']}, Race: {card['race']}, Attribute: {card['attribute']}")

def change_quantity_of_card(yugioh_name, new_quantity):
    Checker = load_deck_checker()
    cards = Checker.get('cards', [])
    current_quantity = sum(1 for card in cards if card['name'].lower() == yugioh_name.lower())
    if current_quantity == 0:
        print(f"No copies of {yugioh_name} found in the deck checker.")
        return
    if new_quantity < 0 or new_quantity > 4:
        print("Invalid quantity. Please enter a number between 0 and 4.")
        return
    if new_quantity > current_quantity:
        limit = 4 - current_quantity
        if new_quantity - current_quantity > limit:
            print(f"Cannot add more than {limit} copies of {yugioh_name}.")
            return
        for h in range(new_quantity - current_quantity):
            Checker.setdefault('cards', []).append(next(card for card in cards if card['name'].lower() == yugioh_name.lower()))
    elif new_quantity < current_quantity:
        cards_to_remove = current_quantity - new_quantity
        removed_count = 0
        for i in range(len(cards) - 1, -1, -1):
            if cards[i]['name'].lower() == yugioh_name.lower() and removed_count < cards_to_remove:
                del cards[i]
                removed_count += 1
    save_deck_checker(Checker)
    print(f"Quantity of {yugioh_name} updated to {new_quantity}.")

def remove_card_from_checker(yugioh_name):
    Checker = load_deck_checker()
    try:
        card_name = input("Enter the card name to remove: ")
    except EOFError:
        print("No input provided. Exiting the removal process.")
        return

    new_deck = [card for card in Checker.get('cards', []) if card['name'].lower() != card_name.lower()]
    if len(new_deck) == len(Checker.get('cards', [])):
        print(f"No copies of {card_name} found in the deck checker.")
        return
    else:
        Checker['cards'] = new_deck
        save_deck_checker(Checker)
        print(f"All copies of {card_name} removed from the deck checker.")

def clean_terminals():
    try:
        from IPython .display import clear_output
        clear_output(wait=True)
    except ImportError:
        os.system('cls' if os.name == 'nt' else 'clear')

def pause():
    input("Press Enter to continue...")

def menu():
    while True:
        print("\nYu-Gi-Oh! Deck Checker Menu:")
        print("1. Add a card to the deck checker")
        print("2. List all cards in the deck checker")
        print("3. Change the quantity of a card")  
        print("4. Remove a card from the deck checker")
        print("0. Exit")
        choice = input("Enter your choice (0-4): ")

        if choice == '1':
            yname = input("Enter your card: ")
            quantity = input("Enter the quantity: ")
            add_card_to_checker(yname, quantity)
            clean_terminals()
            pause()
        elif choice == '2':
            list_cards_in_checker()
            clean_terminals()
            pause()
        elif choice == '3':
            yname = input("Enter your card: ")
            quantity = input("Enter the quantity: ")
            change_quantity_of_card(yname, quantity)
            clean_terminals()
            pause()
        elif choice == '4':
            yname = input("Enter your card: ")
            remove_card_from_checker(yname)
            clean_terminals()
            pause()
        elif choice == '0':
            print("Closing Yu-Gi-Oh! Deck Checker.")
            break
        else:
            print("Invalid choice. Please enter a number between 0 and 4.")
            clean_terminals()
            pause()
