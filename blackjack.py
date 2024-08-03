import random

#Global variables
suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')  # Chất bài
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')  # Thứ tự bài
values = {'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5, 'Six': 6, 'Seven': 7, 'Eight': 8, 'Nine': 9, 'Ten': 10, 'Jack': 10, 'Queen': 10, 'King': 10, 'Ace': 11}

playing = True

class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return self.rank + ' of ' + self.suit

class Deck:
    def __init__(self):
        self.deck = []
        for suit in suits:
            for rank in ranks:
                self.deck.append(Card(suit, rank))
        self.shuffle()
        
    def __str__(self):
        deck_comp = ''
        for card in self.deck:
            deck_comp += '\n' + card.__str__()
        return 'The deck has : ' + deck_comp

    def shuffle(self):
        random.shuffle(self.deck)
    
    def deal(self):
        if len(self.deck) == 0:
            self.__init__()  # Reinitialize the deck when it runs out of cards
        return self.deck.pop()

class Hand:
    def __init__(self):
        self.cards = []
        self.value = 0
        self.aces = 0
    
    def add_card(self, card):
        # card được truyền vào được lấy từ Deck.deal() có nghĩa là single card
        self.cards.append(card)
        self.value += values[card.rank]

        # track ace 
        if card.rank == 'Ace':
            self.aces += 1
    
    def adjust_for_ace(self):
        # nếu tổng giá trị lớn hơn 21 và có một con át 
        # thì hãy thay đổi át của tôi thành 1 thay vì 11
        while self.value > 21 and self.aces > 0:
            self.value -= 10
            self.aces -= 1

class Chip:
    def __init__(self, total):
        self.total = total
        self.bet = 0
    
    def win_bet(self):
        self.total += self.bet
    
    def lose_bet(self):
        self.total -= self.bet

def take_bet(chips):
    while True:
        try:
            chips.bet = int(input('Please enter amount you want to bet: '))
        except ValueError:
            print('Sorry, please provide an integer.')
        else:
            if chips.bet > chips.total:
                print(f'Sorry, you do not have enough chips! You have: {chips.total}')
            else:
                break

def hit(deck, hand):
    single_card = deck.deal()
    hand.add_card(single_card)
    hand.adjust_for_ace()

def hit_or_stand(deck, hand):
    global playing  # điều khiển vòng lặp while 
    while True:
        x = input('Please enter Hit or Stand? h or s: ')
        if x[0].lower() == 'h':
            hit(deck, hand)
        elif x[0].lower() == 's':
            print("Player stands, Dealer's turn.")
            playing = False
        else:
            print("Sorry, I don't understand.")
            continue
        break

def show_some(player, dealer):
    print("\nDealer's hand:")
    print("First card hidden")
    print(dealer.cards[1])
    # show all (2 cards) of players' hand/cards
    print("\nPlayer's hand:")
    for card in player.cards:
        print(card)

def show_all(player, dealer):
    # show all the dealer cards
    print("\nDealer's hand:")
    for card in dealer.cards:
        print(card)
    print(f"Value of Dealer's hand is: {dealer.value}")
    # show all the player cards
    print("\nPlayer's hand:")
    for card in player.cards:
        print(card)
    print(f"Value of Player's hand is: {player.value}")

def player_busts(player, dealer, chips):
    print('Bust Player!')
    chips.lose_bet()

def player_win(player, dealer, chips):
    print('Player wins!')
    chips.win_bet()

def dealer_busts(player, dealer, chips):
    print('Player wins, Dealer busts!')
    chips.win_bet()

def dealer_win(player, dealer, chips):
    print('Dealer wins!')
    chips.lose_bet()

def push(player, dealer):
    print('Player and Dealer tie!')

while True:
    # Welcome 
    print('Welcome to BlackJack')

    # Create deck and shuffle, deal two cards to each player
    deck = Deck()

    player_hand = Hand()
    player_hand.add_card(deck.deal())
    player_hand.add_card(deck.deal())

    dealer_hand = Hand()
    dealer_hand.add_card(deck.deal())
    dealer_hand.add_card(deck.deal())

    # Setup player chips
    player_chips = Chip(100)

    # Prompt the player for their bet
    take_bet(player_chips)

    # Show cards
    show_some(player_hand, dealer_hand)

    while playing:
        # Prompt the player to hit or stand
        hit_or_stand(deck, player_hand)

        # Show cards (but keep one dealer card hidden)
        show_some(player_hand, dealer_hand)
        
        # If player's hand exceeds 21, run player_busts() and break out of the loop
        if player_hand.value > 21:
            player_busts(player_hand, dealer_hand, player_chips)
            break

        # If player hasn't busted, play dealer's hand until dealer reaches 17
        if player_hand.value <= 21:
            while dealer_hand.value < 17:
                hit(deck, dealer_hand)

        # Show all cards
        show_all(player_hand, dealer_hand)

        # Run different winning scenarios
        if dealer_hand.value > 21:
            dealer_busts(player_hand, dealer_hand, player_chips)
        elif dealer_hand.value > player_hand.value:
            dealer_win(player_hand, dealer_hand, player_chips)
        elif dealer_hand.value < player_hand.value:
            player_win(player_hand, dealer_hand, player_chips)
        else:
            push(player_hand, dealer_hand)
        
        # Inform player of their chip total
        print(f'\nPlayer total chips: {player_chips.total}')

        # Ask to play again
        new_game = input('Would you like to play again? y/n: ')
        if new_game[0].lower() == 'y':
            playing = True
            continue
        elif new_game[0].lower() == 'n':
            playing = False
            break
    if not playing:
        break
