import json
from random import shuffle

class Deck: 
    def __init__(self, deck_count:int) -> None:
        """Egy francia kártya paklit definiáló osztály.

        Args:
            deck_count (int): A paklik száma.
        """
        self._deck = []
        self._deck_count = deck_count
        self.deck_init()

    def deck_init(self) -> None:
        """Összekever annyi paklit amennyit megadtunk."""
        for _ in range(self._deck_count): self._deck.extend(self._make_a_deck())
        self.shuffle()

    def _make_a_deck(self) -> list:
        """Egy 52 lapos paklit hoz létre.
        
        Returns:
            list: A pakliban lévő kártyák listája.
        """
        deck = []
        with open('basic_data/cards.json') as f:
            data = json.load(f)
        for suit in data['suits']:
            for name in data['values'].keys(): deck.append((suit, name, data['values'][name]))
        return deck
        
    def shuffle(self) -> None:
        """Megkeveri a paklit."""
        shuffle(self._deck)

    def get_a_card(self) -> tuple:
        """Kivesz egy kártyát a pakliból."""
        card = self._deck[0]
        self._deck.pop(0)
        return card

    def out_of_card(self) -> bool:
        """Azt viszgálja, hogy elfogyott-e a lap a pakliból.
        
        Returns:
            bool: Ha nincs már kártya a pakliban, akkor True-val és ha van még, akkor False-al tér vissza.
        """
        return len(self._deck) == 0
    

class Hand:
    """
    >>> h = Hand()
    >>> h.add_card(('♥', 'Q', 10))
    >>> h.add_card(('♥', '4', 4))
    >>> h.get_score()
    14
    >>> h.add_card(('♣', '2', 2))
    >>> h.get_score()
    16
    >>> h.blackjack()
    False
    >>> h.bust()
    False
    >>> h.reset()
    >>> h.add_card(('♥', 'J', 10))
    >>> h.add_card(('♣', 'A', 11))
    >>> h.blackjack()
    True
    >>> h.get_score()
    21
    >>> h.add_card(('♦', '2', 2))
    >>> h.get_score()
    21
    >>> h.reset()
    >>> h.add_card(('♣', 'K', 10))
    >>> h.add_card(('♦', '9', 9))
    >>> h.add_card(('♦', 'A', 11))
    >>> h.get_score()
    20
    >>> h.add_card(('♥', '3', 3))
    >>> h.get_score()
    23
    >>> h.bust()
    True
    >>> h.add_card(('♥', '5', 5))
    >>> h.get_score()
    23
    >>> h.reset()
    >>> h.add_card(('♥', 'A', 11))
    >>> h.add_card(('♠', '4', 4))
    >>> h.add_card(('♦', '2', 2))
    >>> h.soft_hand()
    True
    >>> h.add_card(('♣', '5', 5))
    >>> h.soft_hand()
    False
    >>> h.pair()
    False
    >>> h.get_score()
    12
    >>> h.reset()
    >>> h.add_card(('♦', '7', 7))
    >>> h.add_card(('♠', '7', 7))
    >>> h.pair()
    True
    """
    def __init__(self) -> None:
        """A kézben lévő kártyákat definiálja."""
        self.reset()
    
    def reset(self) -> None:
        """Alaphelyzetbe állítja az osztályt"""
        self._cards = []
        self._score = 0
        self._soft_hand = True
        self.win = False

    def get_cards(self) -> list: 
        """A kézben lévő lapokat adja vissza.
        
        Returns:
            list: A lapok listája.
        """
        return self._cards

    def get_card_values(self):
        """A kézben lévő lapok értékeit adja vissza.
        
        Returns:
            list: A lapok értékeinek a listája.
        """
        return [card[2] for card in self._cards]

    def _sum_score(self) -> None:
        """Összeadja a kézben lévő kártyák értékét, figyelembe véve az előnyösebb ász értéket."""
        self._score = sum(self.get_card_values())
        if self.bust() and 11 in self.get_card_values(): 
            self._score -= 10
            self._soft_hand = False

    def add_card(self, card:tuple) -> None:
        """Felvesz egy kártyát a kézbe, ha a kezében lévő érték kisebb, mint 21.

        Args:
            card (Card): Egy kártya, ami a kézbe kerül.
        """
        if self._score < 21: self._cards.append(card)
        self._sum_score()

    def blackjack(self) -> bool:
        """Megnézi, hogy a kéz értéke 21-e.

        Returns: 
            bool: Ha 21 a kézben lévő első két kártya értéke, akkor Blackjack van és True-val tér vissza,
            különben meg False értékkel.
        """
        return self._score == 21 and len(self._cards) == 2

    def bust(self) -> bool:
        """Ha a lapok értéke meghaladja a 21-et."""
        return self._score > 21

    def pair(self) -> bool:
        """Megnézi, hogy a játékos első két lapja párt alkot-e.
        
        Returns: 
            bool: Ha az első két lap értéke megegyezik, akkor True-val, különben meg False-al tér vissza.
        """
        return len(set(self.get_card_values())) == 1 and len(self._cards) == 2

    def soft_hand(self) -> bool:
        """Az ász értéke lehet 1 vagy 11. akkor tekintendő az Ász értéke 1-nek,
        ha a lapok összértéke az Ász 11-es értékével számolva meghaladná a 21-et.
        
        Returns: 
            bool: Ha az ász kedvezőbb értéke 11, akkor True-val, különben meg False-al tér vissza.
        """
        return self._soft_hand
    
    def get_score(self) -> int:
        """A kézben lévő érték.

        Returns: 
            int: A kézben lévő kártyák értékének az összegével tér vissza.
        """
        return self._score
    
class Player_hand(Hand):
    def __init__(self, bet:int=0) -> None:
        super().__init__()
        self.bet = bet
    
    def split(self):
        self.split_hand = Player_hand(self.bet)

class Player:
    def __init__(self, chips:int) -> None:
        self._chips = chips
        self.hands = [Player_hand()]

    def place_bet(self) -> int:
        """A játékos megadja a tétet.
        
        Returns:
            int: A tét, amivel a játékos játszik.
        """
        bet = self.get_bet()
        self._chips -= bet
        self.hands[0].bet += bet

    def win_bet(self):
        for hand in self.hands:
            if hand.win:
                self._chips += round(hand.bet)
                hand.bet = 0

    def hit(self): 
        """A játékos tetszőleges számú lapot kérhet mindaddig, amíg a lapjainak összértéke meg nem haladja a 21-et."""
        pass

    def stand(self): 
        """A játékos ekkor nem kér több lapot, mert úgy ítéli meg, hogy megfelelő lapjai vannak a játék megnyerésére."""
        pass

    def double(self): 
        """Ha a játékos úgy ítéli meg, hogy az első két lapja elég erős ahhoz,
        hogy egy harmadik lappal megnyerje a játékot, akkor a Double bemondásával a tétet duplázza.
        A játékos a Double bemondása után már csak egy lapot kap, további lapot nem kérhet.
        """
        pass
    
    def split(self):
        """Ha a játékos első két lapja egy párt alkot (például 5–5 vagy Q–Q), akkor ezt kettéoszthatja,
        ezzel két „kezet” hoz létre, valamint mindkettőre azonos tétet tehet meg, azaz a tét duplázódik.
        Mindkét lapra külön leosztás szerint kérhet lapot.
        """
        self.hands.append(Player_hand(self.hand.bet))
        self.hands.append(Player_hand(self.hand.bet))

class Dealer:
    def __init__(self) -> None:
        self.hand = Hand()

    def get_move(self) -> str:
        if self.hand.get_score() < 17: return 'h'
        else: return 's'

class Game:
    def __init__(self, chips:int, min_bet:int, max_bet:int, deck_count:int) -> None:
        self._deck = Deck(deck_count)
        self._player = None
        self._dealer = Dealer()

    def deal_card(self) -> None:
        """Ha a elfogyott a pakli akkor újra keveri a kiment kártyákat és abból vesz egyet,
        ha van még kártya, akkor onnan vesz el
        """
        if self._deck.out_of_card(): 
            self._deck.deck_init()
            return self._deck.get_a_card()
        else:
            return self._deck.get_a_card()
    
    def check_hands(self):
        pass

    def setup(self) -> None:
        self._player.place_bet()
        self._player.hands[0].add_card(self.deal_card())
        self._dealer.hand.add_card(self.deal_card())
        self._player.hands[0].add_card(self.deal_card())
        self._dealer.hand.add_card(self.deal_card())
        if self._player.hands[0].blackjack(): 
            self._player.hands[0].bet *= 2.5
            self._player.hands[0].win = True
            self._player.win_bet()
        print(self._player.hands[0].bet)
    
    def round(self) -> None:
        print(self._player._chips)
        self.setup()
        print(self._player._chips)
    
    def main(self) -> None: pass

if __name__ == '__main__':
    import doctest
    doctest.testmod()
    