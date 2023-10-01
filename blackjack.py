import random

suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8, 'Nine':9, 'Ten':10, 'Jack':10,
         'Queen':10, 'King':10, 'Ace':11}

playing = True

class Card():
    
    #Creates every card in a deck
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
    
    def __str__(self):
        return self.rank + ' of ' + self.suit

class Deck:
    
    #Create new deck
    def __init__(self):
        self.deck = []
        for suit in suits:
            for rank in ranks:
                self.deck.append(Card(suit,rank))
    
    def __str__(self):
        deck_comp = ''
        for card in self.deck:
            deck_comp += '\n' + card.__str__()
        return 'The deck has: ' + deck_comp

    def shuffle(self):
        random.shuffle(self.deck)

    #Deal cards to the player and dealer  
    def deal(self):
        single_card = self.deck.pop()
        return single_card

class Hand:

    def __init__(self):
        self.cards = []  # start with an empty list as we did in the Deck class
        self.value = 0   # start with zero value
        self.aces = 0    # add an attribute to keep track of aces
    
    #Add cards to your hand as you hit or stand
    def add_card(self,card):
        self.cards.append(card)
        self.value += values[card.rank]
        
        if card.rank == 'Ace':
            self.aces += 1
    
    def adjust_for_ace(self):
        
        #If total value > 21 and I still have an ace
        #Than change my ace to be 1 instead of 11
        while self.value > 21 and self.aces:
            self.value -= 10
            self.aces -= 1
          
class Chips:
    
    #Keeps track of a player's chips based on win or loss of bets
    def __init__(self, total = 100):
        self.total = total  
        self.bet = 0
        
    def win_bet(self):
        self.total += self.bet
    
    def lose_bet(self):
        self.total -= self.bet

def take_bet(chips):
    
    while True:
        
        try:
            chips.bet = int(input("How many chips would you like to bet? "))
        except:
            print('Sorry please provide an integer ')
        else:
            if chips.bet > chips.total:
                print(f'Sorry, you do not have enough chips. You have: {chips.total}')
            else:
                break

def hit(deck,hand):
    
    hand.add_card(deck.deal())
    hand.adjust_for_ace()

def hit_or_stand(deck,hand):
    global playing  # to control an upcoming while loop
    
    while True:
        x = input('Hit or stand? (H or S)')
        
        if x[0].upper() == 'H':
            hit(deck,hand)
            
        elif x[0].upper() == 'S':
            print('\nPlayer stands. Dealer is Playing')
            playing = False
        
        else:
            print('Sorry, please try again.')
            continue
        break

def show_some(player,dealer):
    
    # Show only ONE of the dealer's card
    print("\nDealer's Hand: ")
    print("  First card hidden")
    print(f'  {dealer.cards[1]}')
    
    # Show all (2 cards) of the player's hand/cards
    print("\nPlayer's hand: ", *player.cards, sep = '\n  ')
    
def show_all(player,dealer):
    
    #Show all the dealer cards
    print("\nDealer's hand: ", *dealer.cards, sep = '\n  ')
        
    #Calculate and display value
    print(f"Value of Dealer's hand is {dealer.value}")
    
    #Show all the players cards
    print("\nPlayer's hand: ", *player.cards, sep = '\n  ')
          
    #Calculate and display value
    print(f"Value of Player's hand is {player.value}")

def player_busts(player,dealer,chips):
    print("\nPlayer busts! Dealer wins!")
    chips.lose_bet()

def player_wins(player,dealer,chips):
    print("\nPlayer wins!")
    chips.win_bet()

def dealer_busts(player,dealer,chips):
    print("\nDealer busts! Player wins!")
    chips.win_bet()
    
def dealer_wins(player,dealer,chips):
    print("\nDealer wins!")
    chips.lose_bet()
    
def push(player,dealer):
    print('\nDealer and Player tie. Push!')

while True:
    # Print an opening statement
    print('\nWelcome to BlackJack!')
    
    # Create & shuffle the deck, deal two cards to each player
    deck = Deck()
    deck.shuffle()
    
    player_hand = Hand()
    player_hand.add_card(deck.deal())
    player_hand.add_card(deck.deal())
    
    dealer_hand = Hand()
    dealer_hand.add_card(deck.deal())
    dealer_hand.add_card(deck.deal())
        
    # Set up the Player's chips
    
    player_chips = Chips()
    # Prompt the Player for their bet
    take_bet(player_chips)
    
    # Show cards (but keep one dealer card hidden)
    show_some(player_hand, dealer_hand)
    
    while playing:  # recall this variable from our hit_or_stand function
        
        # Prompt for Player to Hit or Stand
        hit_or_stand(deck,player_hand)
        
        # Show cards (but keep one dealer card hidden)
        show_some(player_hand, dealer_hand) 
        
        # If player's hand exceeds 21, run player_busts() and break out of loop
        if player_hand.value > 21:
            player_busts(player_hand, dealer_hand, player_chips)
            break

    # If Player hasn't busted, play Dealer's hand until Dealer reaches 17
    if player_hand.value <= 21:
        
        while dealer_hand.value < player_hand.value:
            hit(deck,dealer_hand)
    
        # Show all cards
        show_all(player_hand, dealer_hand)
        
        # Run different winning scenarios
        if dealer_hand.value > 21:
            dealer_busts(player_hand, dealer_hand, player_chips)
        
        elif dealer_hand.value > player_hand.value:
            dealer_wins(player_hand, dealer_hand, player_chips)
        
        elif dealer_hand.value < player_hand.value:
            player_wins(player_hand, dealer_hand, player_chips)
        
        else:
            push(player_hand, dealer_hand)
    
    # Inform Player of their chips total 
    print(f'\nPlayer total chips are at: {player_chips.total}')
    # Ask to play again
    new_game = input('Would you like to play another game? Y/N \n')
    
    if new_game[0].upper() == 'Y':
        playing = True
        continue
    else:
        print('Thank you for playing!')
        break