#Deck Checker for Yu-Gi-Oh! cards.
import json
import os
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import urlopen

deck_checker = 'Checker.json'

def load_deck_checker():
    if os.path.exists(deck_checker):
        with open(deck_checker, 'r') as f:
            return json.load(f)
    else:
        return {}

def save_deck_checker(data):
    with open(deck_checker, 'w') as f:
        json.dump(data, f, indent=4)

def search_api(yugioh_name):
    query_key = 'id' if yugioh_name.isdigit() else 'fname'
    query = urlencode({query_key: yugioh_name})
    url = f'https://db.ygoprodeck.com/api/v7/cardinfo.php?{query}'
    try:
        with urlopen(url) as response:
            return json.load(response)
    except (HTTPError, URLError):
        return None

def add_card_to_checker(yugioh_name, card_data):
    Checker = load_deck_checker()

    name = input("Enter the card name: ")
    if not name:
        print("There are no cards with that name.")
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
    else:
        print("Card not found. Please try again.")
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