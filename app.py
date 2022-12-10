import argparse
from collections import Counter
import random
from typing import List

HOLE_IN_ONE = -5

def print_board():
    for i in range(NUM_PLAYERS):
        print(f'P{i}: ', end='')
        for j in range(i * CARDS_EACH, (i + 1) * CARDS_EACH):
            print(cards[j] if flipped[j] else '?' , end=' ')
        print()

def score(cards: List[int]):
    result = 0
    pairs = Counter()
    for i in range(0, len(cards), 2):
        c1 = cards[i]
        c2 = cards[i + 1]

        if c1 != c2 or c1 == c2 == HOLE_IN_ONE:
            result += c1 + c2
        if c1 == c2: 
            pairs.update([c1])

    result -= sum([x * 5 for x in pairs.values() if x >= 2])
    return result

# TODO: keep this data in an array [2] * NUM_PLAYERS
def player_flipped(pindex):
    return flipped[pindex * CARDS_EACH:(pindex + 1) * CARDS_EACH].count(True)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--players', type=int, default=2,  choices=range(2, 7))
    parser.add_argument('-c', '--cards',   type=int, default=8,  choices=[2, 4, 6, 8])
    parser.add_argument('-d', '--dupes',   type=int, default=8,  choices=[2, 4, 6, 8])
    parser.add_argument('-m', '--max',     type=int, default=13, choices=range(6, 13))
    parser.add_argument('-r', '--rounds',  type=int, default=9,  choices=range(1, 10))
    args = parser.parse_args()

    NUM_PLAYERS = args.players
    CARDS_EACH = args.cards
    NUM_DUPLICATES = args.dupes
    MAX_CARD_VALUE = args.max
    NUM_ROUNDS = args.rounds
    PLAYER_CARDS = NUM_PLAYERS * CARDS_EACH

    round_number = 0
    points = [0] * NUM_PLAYERS
    cards = list(range(MAX_CARD_VALUE)) * NUM_DUPLICATES + [HOLE_IN_ONE] * 4

    while(round_number < NUM_ROUNDS):
        print(f'----- ROUND {round_number} -----')
        flipped = [False] * PLAYER_CARDS

        for i in range(NUM_PLAYERS):
            to_flip = [int(x) for x in input(f'P{i}: Flip two cards [0, {CARDS_EACH - 1}]: ').split(' ')]
            for j in to_flip:
                flipped[(i * CARDS_EACH) + j] = True

        random.shuffle(cards)
        index = PLAYER_CARDS
        extra_turns = -1
        player_turn = round_number
        while(extra_turns != 0):
            my_card = player_turn * CARDS_EACH
            print_board()
            pile_or_deck = input(f'P{player_turn}: Swap {cards[index]} with [0, {CARDS_EACH - 1}]: ').lower()

            if pile_or_deck:
                swap_index = my_card + int(pile_or_deck)
                flipped[swap_index] = True
                cards[swap_index], cards[index] = cards[index], cards[swap_index]
            else: # Deck
                index += 1
                deck_input = input(f'P{player_turn}: Swap {cards[index]} with [0, {CARDS_EACH - 1}]: ')
                # TODO combine above prompt with -1 to not take card and also not flip
                if not deck_input and extra_turns < 0: # discard card from deck, dont both asking which to flip if it is their last turn
                    flipped_count = player_flipped(player_turn)
                    skip_prompt = ' (-1 to skip)' if flipped_count == CARDS_EACH - 1 else ''
                    flip_index = int(input(f'P{player_turn}: Flip a card [0, {CARDS_EACH - 1}]{skip_prompt}: '))
                    # TODO: range(-1 if flipped_count == CARDS_EACH - 1 else 0, CARD_EACH)
                    # TODO: also flipped[flip_index] must be false.
                    if flip_index != -1:
                        flipped[my_card + flip_index] = True
                else: # keep card from deck
                    swap_index = int(deck_input)
                    swap_index += my_card
                    flipped[swap_index] = True
                    cards[swap_index], cards[index] = cards[index], cards[swap_index]

            # check if cur player has all flipped.
            flipped_count = player_flipped(player_turn)
            # only set extra turns to countdown once.
            if flipped_count == CARDS_EACH and extra_turns < 0:
                extra_turns = NUM_PLAYERS

            if index >= len(cards) - 1: # reshuffle all non-player cards
                print('reshuffle deck needed')
                # swap cards[107] <--> NUM_PLAYERS *8
                # then shuffle subset of cards[NUM_PLAYERS *8 + 1:]
                exit()

            player_turn = (player_turn + 1) % NUM_PLAYERS
            extra_turns -= 1

        # add scores
        scores = [score(cards[x * CARDS_EACH:(x + 1) * CARDS_EACH]) for x in range(NUM_PLAYERS)]
        points = [x + y for x, y in zip(points, scores)]
        round_number += 1

    # All Rounds Completed.
    results = sorted(zip(range(NUM_PLAYERS), points), key=lambda x: x[1])
    for i, val in enumerate(results):
        print(f'{i}. P{val[0]}: {val[1]} Points')

    train = [1 if x == results[0][1] else 0 for x in points]
    print('Training Scores:', train)
