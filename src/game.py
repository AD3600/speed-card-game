from helpers import *
from player import Player
from warnings import warn


class Game(object):

    def __init__(self, player_1_id, player_2_id):
        self.game_id = player_1_id + player_2_id
        self.game_status = 'playing'

        deck = shuffle(create_deck())

        self.player_1_id = player_1_id
        self.player_2_id = player_2_id
        self.players = dict()
        self.players[player_1_id] = Player(player_1_id, deck[:5], deck[5:20])
        self.players[player_2_id] = Player(player_2_id, deck[20:25], deck[25:40]) 

        self.middle = (deck[40], deck[41])
        self.remaining = deck[42:]

    def validate_card(self, player_id, card, middle_card):
        if not self.players[player_id].has_card(card):
            return False
        return valid_card(card, middle_card)

    def other_player_id(self, player_id):
        if player_id not in [self.player_1_id, self.player_2_id]:
            warn('Game.other_player_id called on value that is not a player id')
            return
        return self.player_1_id if player_id == self.player_2_id else self.player_2_id

    def update_game_state(self, player_id, card, middle_card):
        player = self.players[player_id]
        other_player_id = self.other_player_id(player_id)
        if len(player.hand) == 1:
            self.game_status = 'win'
            player.hand.remove(card)
            return other_player_id
        new_card = player.other_cards.pop()
        player.hand[player.hand.index(card)] = new_card
        if len(self.remaining) == 0 or not self.exist_possible_move():
            self.game_status = 'tie'
        return other_player_id, new_card

    def exist_possible_move(self):
        for card in self.players[self.player_1_id].hand:
            if self.validate_card(self.player_1_id, card, self.middle[0]): return True
            if self.validate_card(self.player_1_id, card, self.middle[1]): return True
        for card in self.players[self.player_2_id].hand:
            if self.validate_card(self.player_2_id, card, self.middle[0]): return True
            if self.validate_card(self.player_2_id, card, self.middle[1]): return True
        return False
