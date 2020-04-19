import numpy as np
from copy import deepcopy


class Poker:
    deck = ['AS', 'AH', 'AC', 'AD', '2S', '2H', '2C', '2D', '3S', '3H', '3C', '3D', '4S', '4H', '4C', '4D', '5S', '5H',
            '5C', '5D', '6S', '6H', '6C', '6D', '7S', '7H', '7C', '7D', '8S', '8H', '8C', '8D', '9S', '9H', '9C', '9D',
            '10S', '10H', '10C', '10D', 'JS', 'JH', 'JC', 'JD', 'QS', 'QH', 'QC', 'QD', 'KS', 'KH', 'KC', 'KD']

    def __init__(self):
        pass

    def shuffle_deck(self):
        deck_copy = deepcopy(self.deck)
        np.random.shuffle(deck_copy)
        return deck_copy

    @staticmethod
    def make_royal_flush(cards):
        hands = {'spades': {'10S', 'JS', 'QS', 'KS', 'AS'},
                 'hearts': {'10H', 'JH', 'QH', 'KH', 'AH'},
                 'diamonds': {'10D', 'JD', 'QD', 'KD', 'AD'},
                 'clubs': {'10C', 'JC', 'QC', 'KC', 'AC'}}

        royal_flush = list()
        for suit in hands:
            if len(cards & hands[suit]) >= 3:
                royal_flush.append(hands['suit'])

        return royal_flush

    @staticmethod
    def make_straight_flush(cards):
        ranking = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        ranking_indices = dict()
        for card in cards:
            if card[0] == 'A':
                ranking_indices.update({'1{}'.format(card[-1]): 0})
                ranking_indices.update({'14{}'.format(card[-1]): 13})
            else:
                ranking_indices.update({card: ranking.index(card[0:-1])})

        straights = list()

        for index in ranking_indices:

            # Bias center
            possible_straight = [index]
            if ranking_indices[index] + 1 in ranking_indices.values():
                possible_straight.append('{}{}'.format(ranking[ranking_indices[index] + 1], index[-1]))

            if ranking_indices[index] + 2 in ranking_indices.values():
                possible_straight.append('{}{}'.format(ranking[ranking_indices[index] + 2], index[-1]))

            if ranking_indices[index] - 1 in ranking_indices.values():
                possible_straight.append('{}{}'.format(ranking[ranking_indices[index] - 1], index[-1]))

            if ranking_indices[index] - 2 in ranking_indices.values():
                possible_straight.append('{}{}'.format(ranking[ranking_indices[index] - 2], index[-1]))

            if len(set(possible_straight) & set(cards)) >= 3:
                straights.append(possible_straight)

            # Bias left
            possible_straight = [index]
            if ranking_indices[index] + 1 in ranking_indices.values():
                possible_straight.append('{}{}'.format(ranking[ranking_indices[index] + 1], index[-1]))

            if ranking_indices[index] - 1 in ranking_indices.values():
                possible_straight.append('{}{}'.format(ranking[ranking_indices[index] - 1], index[-1]))

            if ranking_indices[index] - 2 in ranking_indices.values():
                possible_straight.append('{}{}'.format(ranking[ranking_indices[index] - 2], index[-1]))

            if ranking_indices[index] - 3 in ranking_indices.values():
                possible_straight.append('{}{}'.format(ranking[ranking_indices[index] - 3], index[-1]))

            if len(set(possible_straight) & set(cards)) >= 3:
                straights.append(possible_straight)

            # Bias right
            possible_straight = [index]
            if ranking_indices[index] + 1 in ranking_indices.values():
                possible_straight.append('{}{}'.format(ranking[ranking_indices[index] + 1], index[-1]))

            if ranking_indices[index] + 2 in ranking_indices.values():
                possible_straight.append('{}{}'.format(ranking[ranking_indices[index] + 2], index[-1]))

            if ranking_indices[index] + 3 in ranking_indices.values():
                possible_straight.append('{}{}'.format(ranking[ranking_indices[index] + 3], index[-1]))

            if ranking_indices[index] - 1 in ranking_indices.values():
                possible_straight.append('{}{}'.format(ranking[ranking_indices[index] - 1], index[-1]))

            if len(set(possible_straight) & set(cards)) >= 3:
                straights.append(possible_straight)

        sorted_straights = list()
        for straight in straights:
            sorted_straights.append(sorted(straight))

        removal_indices = list()
        for index in range(1, len(sorted_straights)):
            if sorted_straights[index] == sorted_straights[index-1]:
                removal_indices.append(index)

        removal_indices = sorted(removal_indices, reverse=True)

        for index in removal_indices:
            del sorted_straights[index]

        high_card = 0
        for straight in sorted_straights:
            for card in straight:
                if card[0:-1] != 'A':
                    if card[0:-1] == 'J':
                        if 11 > high_card:
                            high_card = 11
                    elif card[0:-1] == 'Q':
                        if 12 > high_card:
                            high_card = 12
                    elif card[0:-1] == 'K':
                        if 13 > high_card:
                            high_card = 13
                    elif int(card[0:-1]) > high_card:
                        high_card = int(card[0:-1])

        if high_card == 11:
            high_card = 'J'
        elif high_card == 12:
            high_card = 'Q'
        elif high_card == 13:
            high_card = 'K'

        removal_indices = list()
        for index in range(len(sorted_straights)):
            if str(high_card) not in sorted_straights[index]:
                removal_indices.append(index)

        removal_indices = sorted(removal_indices, reverse=True)

        for index in removal_indices:
            del sorted_straights[index]

        return sorted_straights

    def get_flop(self):
        shuffled_deck = self.shuffle_deck()
        flop = shuffled_deck[0:3]
        return flop

    def get_flop_river(self):
        shuffled_deck = self.shuffle_deck()
        flop_river = shuffled_deck[0:4]
        return flop_river

    def get_flop_river_turn(self):
        shuffled_deck = self.shuffle_deck()
        flop_river_turn = shuffled_deck[0:5]
        return flop_river_turn

    def best_hand(self, cards=False, river=False, turn=False):
        if cards:
            if not 3 <= len(cards) <= 5:
                raise ValueError('Best hand can be found for 3, 4, or 5 input cards only')

        else:
            if turn:
                cards = self.get_flop_river_turn()
            elif river:
                cards = self.get_flop_river()
            else:
                cards = self.get_flop()

        if self.make_royal_flush(cards):
            return self.make_royal_flush(cards)