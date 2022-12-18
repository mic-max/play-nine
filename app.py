from collections import Counter
import random

def print_board():
    for i in range(NUM_PLAYERS):
        print(f'P{i} {points[i]} pts: ', end='')
        for j in range(i * CARDS_EACH, (i + 1) * CARDS_EACH):
            print(cards[j] if flipped[j] else '?' , end=' ')
        print()

if __name__ == '__main__':
    NUM_PLAYERS = 2
    CARDS_EACH = 8

    round_number = 0
    points = [0] * NUM_PLAYERS
    cards = list(range(13)) * 8 + [-5] * 4

    while(round_number < 9): # unfair since NUM_PLAYERS might not evenly divide
        flipped = [False] * NUM_PLAYERS * CARDS_EACH

        for i in range(NUM_PLAYERS):
            to_flip = [int(x) for x in input(f'P{i}: Flip two cards [0, {CARDS_EACH - 1}]: ').split(' ')]
            for j in to_flip:
                flipped[(i * CARDS_EACH) + j] = True

        random.shuffle(cards)
        index = NUM_PLAYERS * CARDS_EACH
        extra_turns = -1
        player_turn = round_number
        while(extra_turns != 0 and index < len(cards)):
            my_card = player_turn * CARDS_EACH
            print_board()
            pile_or_deck = input(f'P{player_turn}: Swap {cards[index]} with [0, {CARDS_EACH - 1}]: ')

            if pile_or_deck:
                swap_index = my_card + int(pile_or_deck)
                flipped[swap_index] = True
                cards[swap_index], cards[index] = cards[index], cards[swap_index]
            else: # Deck
                index += 1
                deck_input = input(f'P{player_turn}: Swap {cards[index]} with [0, {CARDS_EACH - 1}]: ')
                if not deck_input and extra_turns < 0: # discard card from deck, dont both asking which to flip if it is their last turn
                    # TODO combine above prompt with -1 to not take card and also not flip
                    flip_input = input(f'P{player_turn}: Flip a card [0, {CARDS_EACH - 1}]: ')
                    if flip_input:
                        flipped[my_card + int(flip_input)] = True
                else: # keep card from deck
                    swap_index = my_card + int(deck_input)
                    flipped[swap_index] = True
                    cards[swap_index], cards[index] = cards[index], cards[swap_index]

            if flipped[player_turn * CARDS_EACH:(player_turn + 1) * CARDS_EACH].count(True) == CARDS_EACH and extra_turns < 0:
                extra_turns = NUM_PLAYERS

            player_turn = (player_turn + 1) % NUM_PLAYERS
            extra_turns -= 1

        print_board()
        round_number += 1
        for i in range(NUM_PLAYERS):
            pairs = Counter()
            for j in range(0, CARDS_EACH, 2):
                c1 = cards[i * CARDS_EACH + j]
                c2 = cards[i * CARDS_EACH + j + 1]

                if c1 != c2 or c1 == c2 == -5:
                    points[i] += c1 + c2
                if c1 == c2:
                    pairs.update([c[i]])

            points[i] -= sum([x * 5 for x in pairs.values() if x > 1])

    results = sorted(zip(range(NUM_PLAYERS), points), key=lambda x: x[1])
    for i, val in enumerate(results):
        print(f'{i}. P{val[0]}: {val[1]} Points')
