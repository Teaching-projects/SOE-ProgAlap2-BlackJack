import json
from random import shuffle

class Deck:
    """Egy francia kártya paklit definiáló osztály."""
    def __init__(self, deck_count:int) -> None:
        """
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
    """A kézben lévő kártyákat definiálja.
    >>> h = Hand()
    >>> h.add_card(('♥', 'Q', 10))
    >>> h.add_card(('♥', '4', 4))
    >>> h.get_score()
    14
    >>> h.add_card(('♣', '2', 2))
    >>> h.get_score()
    16
    >>> h.is_blackjack()
    False
    >>> h.is_bust()
    False
    >>> h = Hand()
    >>> h.add_card(('♥', 'J', 10))
    >>> h.add_card(('♣', 'A', 11))
    >>> h.is_blackjack()
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
    >>> h.is_bust()
    True
    >>> h.add_card(('♥', '5', 5))
    >>> h.get_score()
    23
    >>> h = Hand()
    >>> h.add_card(('♥', 'A', 11))
    >>> h.add_card(('♠', '4', 4))
    >>> h.add_card(('♦', '2', 2))
    >>> h.is_soft()
    True
    >>> h.add_card(('♣', '5', 5))
    >>> h.is_soft()
    False
    >>> h.is_pair()
    False
    >>> h.get_score()
    12
    >>> h = Hand()
    >>> h.add_card(('♦', '7', 7))
    >>> h.add_card(('♠', '7', 7))
    >>> h.is_pair()
    True
    """
    def __init__(self) -> None:
        self._cards = []
        self._score = 0
        self.stand = False

    def get_cards(self) -> list: 
        """A kézben lévő lapokat adja vissza.
        
        Returns:
            list: A lapok listája.
        """
        return self._cards

    def get_card_values(self) -> list:
        """A kézben lévő lapok értékeit adja vissza.
        
        Returns:
            list: A lapok értékeinek a listája.
        """
        return [card[2] for card in self._cards]

    def _sum_score(self) -> None:
        """Összeadja a kézben lévő kártyák értékét, figyelembe véve az előnyösebb ász értéket."""
        self._score = sum(self.get_card_values())
        if self.is_in_ace():
            self._soft = True
            if self.is_bust(): 
                self._score -= 10
                self._soft = False

    def add_card(self, card:tuple) -> None:
        """Felvesz egy kártyát a kézbe, ha a kezében lévő érték kisebb, mint 21.

        Args:
            card (Card): Egy kártya, ami a kézbe kerül.
        """
        if self._score < 21: self._cards.append(card)
        self._sum_score()

    def pop_card(self) -> None:
        """Kivesz egy kártyát a pakliból."""
        self._cards.pop()

    def is_normal21(self) -> bool:
        """Megnézi, hogy a kéz értéke 21-e.
        
        Returns:
            bool: Ha 21 a kézben lévő kártyák értéke, akkor True-val tér vissza, különben meg False értékkel.
        """
        return self._score == 21

    def is_blackjack(self) -> bool:
        """Megnézi, hogy a kéz értéke 21-e.

        Returns: 
            bool: Ha 21 a kézben lévő első két kártya értéke, akkor Blackjack van és True-val tér vissza, különben meg False értékkel.
        """
        return self.is_normal21() and len(self._cards) == 2

    def is_bust(self) -> bool:
        """Megnézi, hogy a kéz értéke meghaladja-e a 21-et.
        
        Returns:
            bool: Ha a kéz értéke nagyobb, mint 21, akkor True-val tér vissza, különben meg False értékkel.
        """
        return self._score > 21
    
    def is_pair(self) -> bool:
        """Megnézi, hogy a játékos első két lapja párt alkot-e.
        
        Returns: 
            bool: Ha az első két lap értéke megegyezik, akkor True-val, különben meg False-al tér vissza.
        """
        return len(set(self.get_card_values())) == 1 and len(self._cards) == 2

    def is_in_ace(self) -> bool:
        """Megnézi, hogy van-e ász kártya a kézben.
        
        Returns:
            bool: Ha a kézben van ász, akkor True-val tér vissza, különben meg False értékkel.
        """
        return 11 in self.get_card_values()

    def is_soft(self) -> bool:
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

    def get_moves(self) -> list:
        moves = []
        if not self.stand: 
            moves.extend(['s', 'h'])
            if len(self._cards) == 2 and not self.is_split_hand: moves.append('d')
            if self.is_pair() and not self.is_split_hand: moves.append('sp')
        return moves
    
class Player_hand(Hand):
    def __init__(self, bet:int=0) -> None:
        super().__init__()
        self._bet = bet
        self.is_split_hand = False

    def add_bet(self, size): 
        self._bet += size

    def multiplication(self, multiplier):
        self._bet *= multiplier

    def get_bet(self):
        size = self._bet
        self._bet = 0
        return size

    def get_bet_value(self):
        return self._bet
    
class Player:
    """
    >>> p = Player(1000)
    >>> p.make_hand()
    >>> p.main_hand.add_card(('♦', '5', 5))
    >>> p.main_hand.add_card(('♣', '5', 5))
    >>> p.get_chips_value()
    1000
    >>> bet = 100
    >>> p.get_chips(bet)
    >>> p.main_hand.add_bet(bet)
    >>> p.get_chips_value()
    900
    >>> p.split()
    >>> p.get_chips_value()
    800
    >>> p.main_hand.get_cards()
    [('♦', '5', 5)]
    >>> p.split_hand.get_cards()
    [('♣', '5', 5)]
    >>> p.main_hand.get_bet_value()
    100
    >>> p.split_hand.get_bet_value()
    100
    >>> p.split_hand.multiplication(0)
    >>> p.won_bet(p.split_hand)
    >>> p.won_bet(p.main_hand)
    >>> p.main_hand.get_bet_value()
    0
    >>> p.get_chips_value()
    900
    >>> p = Player(1000)
    >>> p.make_hand()
    >>> p.main_hand.add_card(('♦', '7', 7))
    >>> p.main_hand.add_card(('♦', '4', 4))
    >>> bet = 60
    >>> p.get_chips(bet)
    >>> p.main_hand.add_bet(bet)
    >>> p.double(p.main_hand)
    >>> p.main_hand.get_bet_value()
    120
    >>> p.get_chips_value()
    880
    """
    def __init__(self, chips:int) -> None:
        self._chips = chips

    def make_hand(self):
        self.main_hand = Player_hand()

    def get_chips(self, size):
        self._chips -= size

    def add_chips(self, size):
        self._chips += size

    def get_chips_value(self):
        return self._chips

    def place_bet(self, hand:Player_hand, min_bet:int, max_bet:int) -> int:
        """A játékos megadja a tétet.
        
        Returns:
            int: A tét, amivel a játékos játszik.
        """
        bet = self.get_bet(min_bet, max_bet)
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
    
    def split(self):
        """Ha a játékos első két lapja egy párt alkot (például 5–5 vagy Q–Q), akkor ezt kettéoszthatja,
        ezzel két „kezet” hoz létre, valamint mindkettőre azonos tétet tehet meg, azaz a tét duplázódik.
        Mindkét lapra külön leosztás szerint kérhet lapot.
        """
        bet = self.main_hand.get_bet_value()
        self.split_hand = Player_hand(bet)
        self.get_chips(bet)
        card = self.main_hand.get_cards()[1]
        self.main_hand.pop_card()
        self.split_hand.add_card(card)
        self.main_hand.is_split_hand = True
        self.split_hand.is_split_hand = True

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
        return (self.hand.get_score() > 16) or self.hand.is_bust()
    
class Game:
    def __init__(self, min_bet:int, max_bet:int, deck_count:int) -> None:
        self._deck = Deck(deck_count)
        self._min_bet = min_bet
        self._max_bet = max_bet

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
        if hand.is_bust(): self.lost(hand)
        elif hand.is_normal21(): self.normal_won(hand)

    def move(self, hand:Player_hand, move) -> None:
        if self._valid_move(hand.get_moves(), move): raise Exception('Wrong move')
        else:
            if move == 'h': 
                hand.add_card(self.deal_card())
            elif move == 's': 
                hand.stand = True
            elif move == 'd':
                self._player.double(hand)
                hand.add_card(self.deal_card())
                hand.stand = True
            elif move == 'sp': 
                self._player.split()
                self._player.main_hand.add_card(self.deal_card())
                self._player.split_hand.add_card(self.deal_card())

    def _valid_move(self, moves, move):
        return move not in moves

    def dealer_move(self):
        while not self._dealer.stand():
            self._dealer.hand.add_card(self.deal_card())

    def setup(self) -> None:
        """A játékmenet kezdete. Először a játékosnak oszt lapot az osztó, majd magának és ezt megteszi mégegyszer.
        Ezután 4 kimenetele lehet a játéknak:
            - A játékosnak és az osztónak is blackjackje van, ilyenkor döntetlen van és a játékos visszakapja a tétet.
            - Csak a játékosnak van blackjackje, ekkor a tét mellett annak másfélszeresét is megkapja a játékos. 
            - Csak az osztónak van blackjackje, ekkor a játékos vesztett.
            - Senkinek sincs blackjackje, ekkor folytatódik a játék.
        """
        self._game_over = False
        self._dealer = Dealer()
        self._player.place_bet(self._player.main_hand, self._min_bet, self._max_bet)
        self._player.main_hand.add_card(self.deal_card())
        self._dealer.hand.add_card(self.deal_card())
        self._player.main_hand.add_card(self.deal_card())
        self._dealer.hand.add_card(self.deal_card())
        if self._player.main_hand.is_blackjack() and self._dealer.hand.is_blackjack(): 
            self._player.main_hand.stand = True
            self.game_over()
        elif self._player.main_hand.is_blackjack() and not self._dealer.hand.is_blackjack(): 
            self.blackjack_won(self._player.main_hand)
            self.game_over()
        elif self._dealer.hand.is_blackjack(): 
            self.lost(self._player.main_hand)
            self.game_over()

    def blackjack_won(self, hand:Player_hand):
        hand.stand = True
        hand.multiplication(2.5)
        
    def normal_won(self, hand:Player_hand):
        hand.stand = True
        hand.multiplication(2)

    def lost(self, hand:Player_hand):
        hand.stand = True
        hand.multiplication(0)

    def game_over(self): 
        self._player.won_bet(self._player.main_hand)
        if self._player.main_hand.is_split_hand: self._player.won_bet(self._player.split_hand)
        self._game_over = True
        print(f'Dealer: {self._dealer.hand.get_cards()} értéke: {self._dealer.hand.get_score()}\nPlayer: {self._player.main_hand.get_cards()} {self._player.split_hand.get_cards() if self._player.main_hand.is_split_hand else ""} értéke: {self._player.main_hand.get_score()} | {self._player.split_hand.get_score() if self._player.main_hand.is_split_hand else ""} \nChips:{self._player._chips} \n')
        
    def _is_draw(self, hand:Player_hand):
        return (hand.is_normal21() and self._dealer.hand.is_normal21()) or (hand.get_score() == self._dealer.hand.get_score() and not self._dealer.hand.is_bust()) or (hand.is_bust() and self._dealer.hand.is_bust())

    def _is_won(self, hand:Player_hand):
        return (hand.is_normal21() and not self._dealer.hand.is_normal21()) or (hand.get_score() > self._dealer.hand.get_score() and not hand.is_bust()) or (self._dealer.hand.is_bust() and not hand.is_bust())

    def _check_player_after_dealer_move(self, hand:Player_hand):
        if self._is_draw(hand): hand.stand = True
        elif self._is_won(hand): self.normal_won(hand) 
        else: self.lost(hand)

    def move_and_check(self, hand:Player_hand):
        while not hand.stand:
            self.move(hand, self._player.get_move(hand, self._dealer.hand.get_cards()[0]))  
            self.check_hand(hand)

    def round(self) -> None:
        self._dealer = Dealer()
        self._player.make_hand()
        self.setup()
        while not self._game_over:
            self.move_and_check(self._player.main_hand) 
            if self._player.main_hand.is_split_hand: self.move_and_check(self._player.split_hand)      
            self.dealer_move()
            self._check_player_after_dealer_move(self._player.main_hand)
            if self._player.main_hand.is_split_hand: self._check_player_after_dealer_move(self._player.split_hand)
            self.game_over()
            
    def get_player_chips_value(self): return self._player.get_chips_value()

    def get_game_status(self):
        return {
            'dealer': self._dealer.hand,
            'player': self._player.main_hand,
            'split_hand': self._player.split_hand if self._player.main_hand.is_split_hand else ''
        }    

if __name__ == '__main__':
    import doctest
    doctest.testmod()
