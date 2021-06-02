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
    >>> h = Hand()
    >>> h.add_card(('♥', 'J', 10))
    >>> h.add_card(('♣', 'A', 11))
    >>> h.blackjack()
    True
    >>> h.get_score()
    21
    >>> h.add_card(('♦', '2', 2))
    >>> h.get_score()
    21
    >>> h = Hand()
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
    >>> h = Hand()
    >>> h.add_card(('♥', 'A', 11))
    >>> h.add_card(('♠', '4', 4))
    >>> h.add_card(('♦', '2', 2))
    >>> h.soft()
    True
    >>> h.add_card(('♣', '5', 5))
    >>> h.soft()
    False
    >>> h.pair()
    False
    >>> h.get_score()
    12
    >>> h = Hand()
    >>> h.add_card(('♦', '7', 7))
    >>> h.add_card(('♠', '7', 7))
    >>> h.pair()
    True
    >>> h = Hand()
    >>> h.add_card(('♠', '6', 6))
    >>> h.add_card(('♠', '10', 10))
    """
    def __init__(self) -> None:
        """A kézben lévő kártyákat definiálja."""
        self._cards = []
        self._score = 0
        self.stand = False
        self.won = False
        self.lost = False

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
        if self.in_ace():
            self._soft = True
            if self.bust(): 
                self._score -= 10
                self._soft = False

    def add_card(self, card:tuple) -> None:
        """Felvesz egy kártyát a kézbe, ha a kezében lévő érték kisebb, mint 21.

        Args:
            card (Card): Egy kártya, ami a kézbe kerül.
        """
        if self._score < 21: self._cards.append(card)
        self._sum_score()

    def pop_card(self):
        self._cards.pop()

    def normal21(self):
        return self._score == 21

    def blackjack(self) -> bool:
        """Megnézi, hogy a kéz értéke 21-e.

        Returns: 
            bool: Ha 21 a kézben lévő első két kártya értéke, akkor Blackjack van és True-val tér vissza,
            különben meg False értékkel.
        """
        return self.normal21() and len(self._cards) == 2

    def bust(self) -> bool:
        """Ha a lapok értéke meghaladja a 21-et."""
        return self._score > 21

    def in_game(self):
        return not(self.stand or self.lost or self.won)
    
    def pair(self) -> bool:
        """Megnézi, hogy a játékos első két lapja párt alkot-e.
        
        Returns: 
            bool: Ha az első két lap értéke megegyezik, akkor True-val, különben meg False-al tér vissza.
        """
        return len(set(self.get_card_values())) == 1 and len(self._cards) == 2

    def in_ace(self):
        return 11 in self.get_card_values()

    def soft(self) -> bool:
        """Az ász értéke lehet 1 vagy 11. akkor tekintendő az Ász értéke 1-nek,
        ha a lapok összértéke az Ász 11-es értékével számolva meghaladná a 21-et.
        
        Returns: 
            bool: Ha az ász kedvezőbb értéke 1, akkor True-val, különben meg False-al tér vissza.
        """
        return self._soft
    
    def get_score(self) -> int:
        """A kézben lévő érték.

        Returns: 
            int: A kézben lévő kártyák értékének az összegével tér vissza.
        """
        return self._score
    
class Player_hand(Hand):
    def __init__(self, bet:int=0) -> None:
        super().__init__()
        self._bet = bet

    def add_bet(self, size): 
        self._bet += size

    def multiplication(self, multiplier):
        self._bet *= multiplier

    def get_bet(self):
        size = self._bet
        self._bet = 0
        return size
    
class Player:
    """
    >>> p = Player(1000)
    >>> p.make_hand()
    >>> p.hands[0].bet = 20
    >>> p.hands[0].add_card(('♣', '4', 4))
    >>> p.hands[0].add_card(('♠', '4', 4))
    >>> len(p.hands)
    1
    >>> p.hands[0].get_cards()
    [('♣', '4', 4), ('♠', '4', 4)]
    >>> p.split(p.hands[0])
    >>> len(p.hands)
    2
    >>> p.hands[0].get_cards()
    [('♣', '4', 4)]
    >>> p.hands[1].get_cards()
    [('♠', '4', 4)]
    """
    def __init__(self, chips:int) -> None:
        self._chips = chips

    def make_hand(self):
        self.hands = [Player_hand()]

    def get_chips(self, size):
        self._chips -= size

    def add_chips(self, size):
        self._chips += size

    def place_bet(self, hand:Player_hand) -> int:
        """A játékos megadja a tétet.
        
        Returns:
            int: A tét, amivel a játékos játszik.
        """
        bet = self.get_bet()
        self.get_chips(bet)
        hand.add_bet(bet)

    def won_bet(self, hand:Player_hand) -> None:
        self.add_chips(round(hand.get_bet()))
    
    def double(self, hand:Player_hand): 
        """Ha a játékos úgy ítéli meg, hogy az első két lapja elég erős ahhoz,
        hogy egy harmadik lappal megnyerje a játékot, akkor a Double bemondásával a tétet duplázza.
        A játékos a Double bemondása után már csak egy lapot kap, további lapot nem kérhet.
        """
        bet = hand.get_bet()
        self.get_chips(bet)
        bet *= 2
        hand.add_bet(bet)
    
    def split(self, hand:Hand):
        """Ha a játékos első két lapja egy párt alkot (például 5–5 vagy Q–Q), akkor ezt kettéoszthatja,
        ezzel két „kezet” hoz létre, valamint mindkettőre azonos tétet tehet meg, azaz a tét duplázódik.
        Mindkét lapra külön leosztás szerint kérhet lapot.
        """
        card = hand.get_cards()[1]
        hand.pop_card()
        self.hands.append(Player_hand(hand.bet))
        self.hands[-1].add_card(card)

class Dealer:
    """
    >>> d = Dealer()
    >>> d.stand()
    False
    >>> d.hand.add_card(('♠', '7', 7))
    >>> d.hand.add_card(('♠', '4', 4))
    >>> d.stand()
    False
    >>> d.hand.add_card(('♦', '9', 9))
    >>> d.stand()
    True
    >>> d = Dealer()
    >>> d.hand.add_card(('♠', 'K', 10))
    >>> d.hand.add_card(('♦', '2', 2))
    >>> d.stand()
    False
    >>> d.hand.add_card(('♣', 'J', 10))
    >>> d.stand()
    True
    """
    def __init__(self) -> None:
        self.hand = Hand()

    def stand(self) -> str:
        return (self.hand.get_score() > 16) or self.hand.bust()
    
class Game:
    def __init__(self, min_bet:int, max_bet:int, deck_count:int) -> None:
        self._deck = Deck(deck_count)

    def set_player(self, player:Player):
        self._player = player

    def deal_card(self) -> None:
        """Ha a elfogyott a pakli akkor újra keveri a kiment kártyákat és abból vesz egyet,
        ha van még kártya, akkor onnan vesz el
        """
        if self._deck.out_of_card(): 
            self._deck.deck_init()
            return self._deck.get_a_card()
        else:
            return self._deck.get_a_card()

    def check_hand(self, hand:Player_hand):
        if hand.blackjack(): self.blackjack_won(hand)
        elif hand.bust(): self.lost(hand)
        elif hand.normal21(): self.normal_won(hand)

    def move(self, hand:Player_hand, move) -> None:
        if move == 'h': 
            hand.add_card(self.deal_card())
        elif move == 's': 
            hand.stand = True
        elif move == 'd': 
            self._player.double(hand)
            hand.add_card(self.deal_card())
            hand.stand = True
        elif move == 'sp': 
            if hand.pair(): 
                self._player.split(hand)
                self._player.hands[-1].add_card(self.deal_card())
                self._player.hands[-2].add_card(self.deal_card())
            else: raise Exception('Wrong move')

    def dealer_move(self):
        while not self._dealer.stand():
            self._dealer.hand.add_card(self.deal_card())

    def setup(self, main_hand:Player_hand) -> None:
        """A játékmenet kezdete. Először a játékosnak oszt lapot az osztó, majd magának és ezt megteszi mégegyszer.
        Ezután 4 kimenetele lehet a játéknak:
            - A játékosnak és az osztónak is blackjackje van, ilyenkor döntetlen van és a játékos visszakapja a tétet.
            - Csak a játékosnak van blackjackje, ekkor a tét mellett annak másfélszeresét is megkapja a játékos. 
            - Csak az osztónak van blackjackje, ekkor a játékos vesztett.
            - Senkinek sincs blackjackje, ekkor folytatódik a játék 
        """
        self._game_over = False
        self._dealer = Dealer()
        self._player.place_bet(main_hand)
        main_hand.add_card(self.deal_card())
        self._dealer.hand.add_card(self.deal_card())
        main_hand.add_card(self.deal_card())
        self._dealer.hand.add_card(self.deal_card())
        if main_hand.blackjack() and self._dealer.hand.blackjack(): 
            self.draw(main_hand)
            self.game_over()
        elif main_hand.blackjack() and not self._dealer.hand.blackjack(): 
            self.blackjack_won(main_hand)
            self.game_over()
        elif self._dealer.hand.blackjack(): 
            self.lost(main_hand)
            self.game_over()

    def blackjack_won(self, hand:Player_hand):
        hand.won = True
        hand.stand = True
        hand.multiplication(2.5)
        
    def normal_won(self, hand:Player_hand):
        hand.won = True
        hand.stand = True
        hand.multiplication(2)

    def draw(self, hand:Player_hand):
        hand.stand = True
        hand.multiplication(1)

    def lost(self, hand:Player_hand):
        hand.lost = True
        hand.stand = True
        hand.multiplication(0)

    def game_over(self): 
        self._game_over = True
        for hand in self._player.hands:
            self._player.won_bet(hand)

    def round(self) -> None:
        self._dealer = Dealer()
        self._player.make_hand()
        self.setup(self._player.hands[0])
        while not self._game_over:
            for hand in self._player.hands:
                if not hand.stand:
                    self.move(hand, self._player.get_move(hand, self._dealer.hand.get_cards()[0]))  
                    self.check_hand(hand)
            if False not in [hand.stand for hand in self._player.hands]: self.game_over()
            else:
                self.dealer_move()
                self.check_hand(self._dealer.hand)    
    
if __name__ == '__main__':
    import doctest
    doctest.testmod()
