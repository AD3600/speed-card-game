import random

suites = ['spades', 'hearts', 'clubs', 'diamonds']
ranks = ['ace', '2', '3', '4', '5', '6', '7',
         '8', '9', '10', 'jack', 'queen', 'king']


def create_deck():
    return [(suit, rank) for suit in suites
            for rank in ranks]


def shuffle(deck):
    random.shuffle(deck)
    return deck


def valid_card(card, middle_card):
    index = ranks.index(card[1])
    return middle_card[1] == ranks[(index + 1) % 13] or middle_card[1] == ranks[(index - 1) % 13]
