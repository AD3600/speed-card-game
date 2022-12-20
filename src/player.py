class Player(object):

    def __init__(self, id, hand, other_cards):
        self.id = id
        self.hand = hand
        self.other_cards = other_cards

    def has_card(self, card):
        return card in self.hand