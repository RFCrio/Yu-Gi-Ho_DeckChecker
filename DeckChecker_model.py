import json
import os
from dataclasses import dataclass, replace
from typing import Optional

import requests

MAX_COPIES = 3
API_URL = 'https://db.ygoprodeck.com/api/v7/cardinfo.php'
TIMEOUT = 10


@dataclass
class Card:
    name: str
    type: Optional[str] = None
    desc: Optional[str] = None
    atk: Optional[int] = None
    defense: Optional[int] = None
    level: Optional[int] = None
    race: Optional[str] = None
    attribute: Optional[str] = None
    ban_tcg: Optional[str] = None  # não é salvo no JSON

    def is_complete(self) -> bool:
        # Magia/Armadilha não têm ATK/DEF/Level/Attribute
        return bool(self.name and self.type and self.desc and self.race)

    def to_dict(self) -> dict:
        return {
            'name': self.name, 'type': self.type, 'desc': self.desc,
            'atk': self.atk, 'def': self.defense, 'level': self.level,
            'race': self.race, 'attribute': self.attribute,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Card":
        return cls(
            name=data['name'], type=data.get('type'), desc=data.get('desc'),
            atk=data.get('atk'), defense=data.get('def'),
            level=data.get('level'), race=data.get('race'),
            attribute=data.get('attribute'),
        )

    @classmethod
    def from_api(cls, data: dict) -> "Card":
        card = cls.from_dict(data)
        card.ban_tcg = data.get('banlist_info', {}).get('ban_tcg')
        return card


class YgoprodeckAPI:
    def _get(self, params: dict) -> Optional[list]:
        try:
            response = requests.get(API_URL, params=params, timeout=TIMEOUT)
        except requests.RequestException:
            return None
        if response.status_code != 200:
            return None
        return response.json().get('data')

    def get_card_by_name(self, name: str) -> Optional[Card]:
        data = self._get({'name': name})
        return Card.from_api(data[0]) if data else None

    def get_card_by_id(self, card_id: str) -> Optional[Card]:
        data = self._get({'id': card_id})
        return Card.from_api(data[0]) if data else None

    def get_tcg_banlist(self) -> Optional[list[tuple[str, str]]]:
        data = self._get({'banlist': 'tcg'})
        if data is None:
            return None
        return [(c['name'], c['banlist_info']['ban_tcg']) for c in data]


class DeckRepository:
    def __init__(self, path: str = 'Checker.json'):
        self.path = path

    def load(self) -> list[Card]:
        if not os.path.exists(self.path):
            return []
        with open(self.path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return [Card.from_dict(c) for c in data.get('cards', [])]

    def save(self, cards: list[Card]) -> None:
        with open(self.path, 'w', encoding='utf-8') as f:
            json.dump({'cards': [c.to_dict() for c in cards]},
                      f, indent=4, ensure_ascii=False)

    def count(self, name: str) -> int:
        return sum(1 for c in self.load() if c.name.lower() == name.lower())

    def add(self, card: Card, copies: int) -> None:
        cards = self.load()
        cards.extend(replace(card) for _ in range(copies))
        self.save(cards)

    def set_quantity(self, name: str, quantity: int) -> None:
        cards = self.load()
        same = [c for c in cards if c.name.lower() == name.lower()]
        others = [c for c in cards if c.name.lower() != name.lower()]
        if quantity > 0 and same:
            others.extend(replace(same[0]) for _ in range(quantity))
        self.save(others)
