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

def search_api_name(yugioh_name):
    url = f'https://db.ygoprodeck.com/api/v7/cardinfo.php?name={yugioh_name}'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return None

def search_api_id(yugioh_id):
    url = f'https://db.ygoprodeck.com/api/v7/cardinfo.php?id={yugioh_id}'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return None

def add_card_to_checker():
    Checker = load_deck_checker()

    name = input("Enter the card name: ").strip()
    if not name:
        print("Please enter a valid card name.")
        pause()
        return

    API_data = search_api_name(name)

    new_card = None
    type = None
    desc = None
    atk = None
    defn = None
    level = None
    race = None
    attribute = None

    if API_data:
        new_card = API_data
        for new_card in API_data['data']:
            
            type = new_card.get('type', None)
            desc = new_card.get('desc', None)
            atk = new_card.get('atk', None)
            defn = new_card.get('def', None)
            level = new_card.get('level', None)
            race = new_card.get('race', None)
            attribute = new_card.get('attribute', None)
            break

    if not new_card:
        print("Card not found. Please try using card ID.")
        name = None
        new_ID = input("Enter the card ID: ")
        API_data = search_api_id(new_ID)
        if API_data:
            new_card = API_data
            for new_card in API_data['data']:

                    name = new_card.get('name', None)
                    type = new_card.get('type', None)
                    desc = new_card.get('desc', None)
                    atk = new_card.get('atk', None)
                    defn = new_card.get('def', None)
                    level = new_card.get('level', None)
                    race = new_card.get('race', None)
                    attribute = new_card.get('attribute', None)
                    break

    if not new_card:
        print("Card not found. Please try again.")
        pause()
        return
    
    elif not type or not desc or not atk or not defn or not level or not race or not attribute:
        print("Incomplete card data.")
        pause()
        return

    if any(card['name'].lower() == name.lower() for card in Checker.get('cards', [])):
        print("Card already exists in the deck checker.")
        pause()
        return

    Duplicate = sum(1 for card in Checker.get('cards', []) if card['name'].lower() == name.lower())
    limit = 4 - Duplicate

    if Duplicate >= limit:
        print(f"Maximum number of {name} cards reached.")
        pause()
        return

    print(f"you already have {Duplicate} copies of {name}. You can add {limit} more copies.")

    try:
        copies_to_add = int(input(f"How many copies of {name} would you like to add? (Max {limit}): "))
        if copies_to_add < 1 or copies_to_add > limit:
            print(f"Invalid number of copies. Please enter a number between 1 and {limit}.")
            pause()
            return
        
    except ValueError:
        print("Invalid input. Please enter a valid number.")
        pause()
        return
    
    for i in range(copies_to_add):
        Checker.setdefault('cards', []).append({
            'name': name,
            'type': type,
            'desc': desc,
            'atk': atk,
            'def': defn,
            'level': level,
            'race': race,
            'attribute': attribute
        })
    save_deck_checker(Checker)
    print(f"{copies_to_add} copies of {name} added to the deck checker.")
    pause()
    return

def list_cards_in_checker():
    Checker = load_deck_checker()
    if not Checker.get('cards'):
        print("No cards in the deck checker.")
        pause()
        return
    print("Cards in the deck checker:")
    for card in Checker['cards']:
        print(f"Name: {card['name']}, Type: {card['type']}, ATK: {card['atk']}, DEF: {card['def']}, Level: {card['level']}, Race: {card['race']}, Attribute: {card['attribute']}")
    pause()
            

def change_quantity_of_card():
    Checker = load_deck_checker()
    name = input("Enter the card name you want to change the quantity of: ")
    cards = Checker.get('cards', [])
    current_quantity = sum(1 for card in cards if card['name'].lower() == name.lower())

    if current_quantity == 0:
        print(f"No copies of {name} found in the deck checker.")
        pause()
        return

    else:
        print(f"You currently have {current_quantity} copies of {name}.")
        try:
            new_quantity = int(input(f"Enter the new quantity for {name} (0 to remove all): "))
            if new_quantity < 0 or new_quantity > 4:
                print("Invalid quantity. Please enter a number between 0 and 4.")
                pause()
                return
        except ValueError:
            print("Invalid input. Please enter a valid number.")
            pause()
            return

        if new_quantity == 0:
            Checker['cards'] = [card for card in cards if card['name'].lower() != name.lower()]
            save_deck_checker(Checker)
            print(f"All copies of {name} removed from the deck checker.")
            pause()
            return

        else:
            Checker['cards'] = [card for card in cards if card['name'].lower() != name.lower()]
            for i in range(new_quantity):
                Checker.setdefault('cards', []).append({
                    'name': name,
                    'type': next((card['type'] for card in cards if card['name'].lower() == name.lower()), None),
                    'desc': next((card['desc'] for card in cards if card['name'].lower() == name.lower()), None),
                    'atk': next((card['atk'] for card in cards if card['name'].lower() == name.lower()), None),
                    'def': next((card['def'] for card in cards if card['name'].lower() == name.lower()), None),
                    'level': next((card['level'] for card in cards if card['name'].lower() == name.lower()), None),
                    'race': next((card['race'] for card in cards if card['name'].lower() == name.lower()), None),
                    'attribute': next((card['attribute'] for card in cards if card['name'].lower() == name.lower()), None)
                })
            save_deck_checker(Checker)
            print(f"The quantity of {name} has been updated to {new_quantity}.")
            pause()
            return

def clean_terminals():
    try:
        from IPython.display import clear_output
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
        print("0. Exit")
        choice = input("Enter your choice (0-3): ")

        if choice == '1':
            add_card_to_checker()
            clean_terminals()
        elif choice == '2':
            list_cards_in_checker()
            clean_terminals()
        elif choice == '3':
            change_quantity_of_card()
            clean_terminals()
        elif choice == '0':
            print("Closing Yu-Gi-Oh! Deck Checker.")
            break
        else:
            print("Invalid choice. Please enter a number between 0 and 3.")
            clean_terminals()
            pause()

menu()