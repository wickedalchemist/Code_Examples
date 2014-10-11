###
# see http://www.codeskulptor.org/#user28_QHAuziDKIf8rIQM_0.py for interactive game
###
##############
#
# BLACKJACK: To play- Use the buttons at left to hit/stand
# 			on your hand. Once you stand, the dealer then
#			will hit if their hand total is <17. If the dealer
#			wins the score will be by incremented by -1, if you
#			win, by +1. To play another hand, hit the deal button.
#
##############

import simplegui
import random

# load card images - 949x392 - source: jfitz.com
CARD_SIZE = (73, 98)
CARD_CENTER = (36.5, 49)
card_images = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/cards.jfitz.png")

CARD_BACK_SIZE = (71, 96)
CARD_BACK_CENTER = (35.5, 48)
card_back = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/card_back.png")    

# initialize global variables
in_play = False
outcome = ""
score = 0

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


# define card class
class Card:
    '''
    Assign suit, rank, and image atributes to cards
    '''
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        '''
        Pull correct card image rectange from the tiled card image to draw on canvas
        '''
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, 
                          [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        
        
# define hand class
class Hand:
    def __init__(self):
        # create Hand object
        self.hand=[]

    def __str__(self):
    # return a string representation of a hand
        return str(self.hand)

    def add_card(self,card):
        # add a card object to a hand
        return self.hand.append(str(card))	
    
    def get_value(self):
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
        # compute the value of the hand
        card_values=[]
        hand_value=[]
        ranks=[]
        aces=0
        for this_card in self.hand:
            suit=this_card[0]
            rank=this_card[1]
            if this_card[1] == 'A':
                aces += 1
            card_values.append(VALUES[rank])
        hand_value=sum(card_values)            
        if aces == 0:
            return hand_value            
        else:             
            if hand_value+10 < 21:
                return hand_value+10
            else:
                return hand_value
   
    def draw(self, canvas, pos):
        '''
        Draw card (as defined through card class) on canvas
        '''
        for card in self.hand:
            tmp=Card(card[0],card[1])
            pos=[self.hand.index(card)*100+50,pos[1]]
            tmp.draw(canvas, pos)
                      
# define deck class 
class Deck:
    '''
    Create deck of card objects, shuffle them for unique games. 
    Create function to deal card from deck and remove so it's not drawn again.
    '''
    def __init__(self):
        # create a Deck object (all 52 cards)
        self.deck=[]
        for suit in SUITS:
            for rank in RANKS:
                self.deck.append(suit+rank)
                
    def shuffle(self):
        # shuffle the deck 
        random.shuffle(self.deck)
        return self.deck

    def deal_card(self):
        # deal a card object from the deck
        this_suit=self.deck[0][0]	
        this_rank=self.deck[0][1]
        #remove card from deck once dealt
        self.deck.pop(0)
        delt=Card(str(this_suit),str(this_rank))
        return delt
        
    def __str__(self):
        return str(self.deck)

    
#GLOBAL VARIABLES
deck = Deck()
player_hand_value=0
dealer_hand_value=0
score=0
outcome=''
message=''
front=True
 
#define event handlers for buttons
def deal():
    global outcome, message, in_play, deck, player_hand, dealer_hand, score
    #create player/dealer hands
    player_hand=Hand()
    dealer_hand=Hand()
    deck.shuffle()
    #Deal initial cards
    p1 = deck.deal_card()
    p2 = deck.deal_card()
    player_hand.add_card(p1)
    player_hand.add_card(p2)
    d1 = deck.deal_card()
    d2 = deck.deal_card()
    dealer_hand.add_card(d1)
    dealer_hand.add_card(d2)
    #Ask player for move
    message='Hit or Stand?' 
    # Take off point for dealing while already in a game
    if in_play == True:
        score -= 1
    in_play = True
    outcome=''

def hit():
     # if the hand is in play, hit the player
    global in_play, player_hand, player_hand_value, score, outcome, message
    if in_play == True:
        #add card to dealer hand
        p3=deck.deal_card()
        player_hand.add_card(p3)      
        player_hand_value=player_hand.get_value()
        # score player hand, evaluate if >21, assign game score accordingly
        # change message/outcome to be printed on canvas
        # change in_play Boolean to False for bust
        if player_hand_value > 21:
            in_play=False
            score -= 1
            outcome='You BUSTED!'
            message='New Deal?'
       
def stand():
    '''
    Define rules for dealer's hand- If <17 then hit the deck, ties go to player. Assign game score accordingly.
    '''
    global score, dealer_hand_value, outcome,message, in_play
    in_play=False
    #Get dealer hand value
    dealer_hand_value=dealer_hand.get_value()
    while dealer_hand_value < 17:
        d3=deck.deal_card()
        dealer_hand.add_card(d3)
        dealer_hand_value = dealer_hand.get_value()
    if dealer_hand_value > 21:
        outcome= 'DEALER BUSTS'
    elif dealer_hand_value > player_hand_value:
        score -= 1
        outcome='DEALER WINS'
    else:
        outcome='PLAYER WINS'
        score += 1
    message='New Deal?'
        

# draw handler    
def draw(canvas):
    global in_play, front
    # draw labels
    canvas.draw_text('Blackjack', [50, 75], 50, 'Black')
    canvas.draw_text('Dealer', [50,175], 30, 'Black')
    canvas.draw_text('Player', [50, 375], 30, 'Black')
    canvas.draw_text('Score', [300, 175], 30, 'Black')
    canvas.draw_text(str(score), [400, 175], 30, 'Black')
    #draw hands
    player_hand.draw(canvas, [0,400])
    dealer_hand.draw(canvas, [0,200])
    if in_play == True:
        canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE,
                          [50 + CARD_CENTER[0], 200 + CARD_CENTER[1]], CARD_SIZE) 
    #draw outcome message
    canvas.draw_text(outcome, [250, 125], 30, 'Maroon')
    canvas.draw_text(message, [50,125], 30, 'Black')

#    canvas.draw_text(message, [300,375], 30, 'Black')


# initialization frame
frame = simplegui.create_frame("Blackjack", 550, 550)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)


# get things rolling
deal()
frame.start()


# remember to review the gradic rubric
