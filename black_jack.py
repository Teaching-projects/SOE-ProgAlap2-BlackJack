import json
import random

class Card:
    """
    >>> c1 = Card('♥', '7', 7)
    >>> c1.get_value()
    7
    >>> c2 = Card('♠', 'K', 10)
    >>> c2.get_value()
    10
    """
    def __init__(self, suit:str, name:str, value:int) -> None:
        """Egy egyszerű francia kártya tulajdonságait definiáló osztály.

        Args:
            suit (str): A kártya színe.
            name (str): A kártya neve.
            value (int): A kártya értéke
        """
        self.suit = suit
        self.name = name
        self._value = value

    def get_value(self):
        return self._value

class Deck: 
    def __init__(self, deck_count:int) -> None:
        """Egy francia kártya paklit definiáló osztály, ahol több pakli is megadható.

        Args:
            deck_count (int): A paklik száma.
        """
        self._deck = []
        for i in range(deck_count): self._deck.extend(self._make_a_deck())
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
        random.shuffle(self._deck)
    
    def get_a_card(self) -> Card:
        card = self._deck[0]
        self._deck.pop(0)
        return card

class Hand:
    """
    >>> h = Hand()
    >>> h.set_card(Card('♥', 'Q', 10))
    >>> h.get_hand_value()
    10
    >>> h.set_card(Card('♥', '4', 4))
    >>> h.set_card(Card('♣', '2', 2))
    >>> h.get_hand_value()
    16
    >>> h.blackjack()
    False
    >>> h.set_card(Card('♥', '5', 5))
    >>> h.get_hand_value()
    21
    >>> h.blackjack()
    True
    >>> h.set_card(Card('♦', '2', 2))
    >>> h.get_hand_value()
    21
    """
    def __init__(self) -> None:
        """A kézben lévő kártyákat definiálja."""
        self._cards = []
    
    def set_card(self, card:Card):
        """Felvesz egy kártyát a kézbe, ha a kezében lévő érték kisebb, mint 21.

        Args:
            card (Card): Egy kártya, ami a kézbe kerül.
        """
        if self.get_hand_value() < 21: self._cards.append(card)

    def get_hand_value(self) -> int:
        """A kézben lévő érték.

        Returns: 
            int: A kézben lévő kártyák értékének az összegével tér vissza.
        """
        return sum(card.get_value() for card in self._cards)

    def blackjack(self) -> bool:
        """Megnézi, hogy a kéz értéke 21-e.

        Returns: 
            bool: Ha 21 a kézben lévő kártyák értéke akkor Blackjack van és True-val tér vissza, különben meg False értékkel
        """
        return self.get_hand_value() == 21

class Player:
    def __init__(self, chips:int) -> None:
        self._chips = chips
        self._bet = None
        self._hand = Hand()

class Game:
    def __init__(self, chips:int, deck_count:int=6) -> None:
        self._player = Player(chips)
        self._deck = Deck(deck_count)

if __name__ == '__main__':
    import doctest
    doctest.testmod()