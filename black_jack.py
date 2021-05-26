import json
import random

class Card:
    def __init__(self, suit:str, name:str, value:int) -> None:
        """Egy egyszerű francia kártya tulajdonságait definiáló osztály.

        Args:
            suit (str): A kártya színe.
            name (str): A kártya neve.
            value (int): A kártya értéke
        """
        self.suit = suit
        self.name = name
        self.value = value

class Deck: 
    def __init__(self, deck_count:int = 8) -> None:
        """Egy francia kártya paklit definiáló osztály, ahol több pakli is megadható.

        Args:
            deck_count (int): Megadható a paklik száma. Alapértelmezett 8 paklival játszák a játékot.
        """
        self.deck = []
        for i in range(deck_count): self.deck.extend(self._make_a_deck())
        self.shuffle()

    def _make_a_deck(self) -> list:
        """Egy 52 lapos paklit hoz létre"""
        deck = []
        with open('basics_data/cards.json') as f:
            data = json.load(f)
        for suit in data['suits']:
            for name in data['values'].keys(): deck.append(Card(suit, name, data['values'][name]))
        return deck
        
    def shuffle(self) -> None:
        """Megkeveri a paklit"""
        random.shuffle(self.deck)

class Player: pass
class Game: pass

if __name__ == '__main__': pass