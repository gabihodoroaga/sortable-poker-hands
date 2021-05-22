from random import shuffle
from itertools import chain
from cards import *
import pytest


def test_basic():
    sorted_poker_hands = list(map(PokerHand, ["KS AS TS QS JS",
                                            "2H 3H 4H 5H 6H",
                                            "AS AD AC AH JD",
                                            "JS JD JC JH 3D",
                                            "2S AH 2H AS AC",
                                            "AS 3S 4S 8S 2S",
                                            "2H 3H 5H 6H 7H",
                                            "2S 3H 4H 5S 6C",
                                            "2D AC 3H 4H 5S",
                                            "AH AC 5H 6H AS",
                                            "2S 2H 4H 5S 4C",
                                            "AH AC 5H 6H 7S",
                                            "AH AC 4H 6H 7S",
                                            "2S AH 4H 5S KC",
                                            "2S 3H 6H 7S 9C"]))

    lstCopy = sorted_poker_hands.copy()
    shuffle(lstCopy)
    userSortedHands = chain(sorted(lstCopy))

    for hand in sorted_poker_hands:
        assert next(userSortedHands) == hand

def test_highcard_draw_should_return_pair():
    card = HighCard()
    card = card.Draw("KS")
    card = card.Draw("KH")
    assert type(card) is Pair

def test_highcard_draw_should_return_straight():
    card = HighCard()
    card = card.Draw("4S")
    card = card.Draw("5H")
    card = card.Draw("6C")
    card = card.Draw("7H")
    card = card.Draw("8H")
    assert type(card) is Straight

def test_highcard_draw_should_return_flash():
    card = HighCard()
    card = card.Draw("2H")
    card = card.Draw("5H")
    card = card.Draw("JH")
    card = card.Draw("7H")
    card = card.Draw("AH")
    assert type(card) is Flush

def test_highcard_draw_should_return_straight_flash():
    card = HighCard()
    card = card.Draw("TH")
    card = card.Draw("JH")
    card = card.Draw("QH")
    card = card.Draw("KH")
    card = card.Draw("AH")
    assert type(card) is StraightFlush

def test_pair_draw_should_return_twopairs():
    card = HighCard()
    card = card.Draw("KS")
    card = card.Draw("KH")
    card = card.Draw("QS")
    card = card.Draw("QD")
    assert type(card) is TwoPairs

def test_pair_draw_should_return_threeffkind():
    card = HighCard()
    card = card.Draw("KS")
    card = card.Draw("KH")
    card = card.Draw("KD")
    assert type(card) is ThreeOfKind

def test_twopairs_draw_should_return_fullhouse():
    card = HighCard()
    card = card.Draw("KS")
    card = card.Draw("KH")
    card = card.Draw("QS")
    card = card.Draw("QD")
    card = card.Draw("QH")
    assert type(card) is FullHouse

def test_threeofkind_draw_should_return_fullhouse():
    card = HighCard()
    card = card.Draw("2H")
    card = card.Draw("3S")
    card = card.Draw("3D")
    card = card.Draw("3H")
    card = card.Draw("2S")
    assert type(card) is FullHouse

def test_threeofkind_draw_should_return_fourofkind():
    card = HighCard()
    card = card.Draw("2H")
    card = card.Draw("3S")
    card = card.Draw("3D")
    card = card.Draw("3H")
    card = card.Draw("3C")
    assert type(card) is FourOfKind

# TODO: Add more edge cases
