from random import shuffle
from itertools import chain
from functools import lru_cache

class PokerCard:
    values = {'2':2,'3':3,'4':4,'5':5,'6':6,'7':7,'8':8,'9':9,'T':10,'J':12,'Q':13,'K':14,'A':15}
    suites = ['S','H','D','C']

    def __init__(self, card):
        # no card validation for better performance
        self.value = card[0]
        self.suite = card[1]

    def __lt__(self, card):
        return self.values[self.value] < self.values[card.value]

class Hand:
    def __repr__(self):
        return self.__class__.__name__

class HighCard(Hand):
    def __init__(self):
        self.rank = 1
        self.cards = []

    def __lt__(self, other):
        myCards = self.allCards()
        cardCards = other.allCards()

        for i in range(0, 5):
            if myCards[i] < cardCards[i]:
                return True 
            if myCards[i] > cardCards[i]:
                return False
        return False
    
    @lru_cache(None)
    def allCards(self):
        return sorted(self.cards, reverse=True)

    def Draw(self, card):
        pc = PokerCard(card)
        # check for pair
        if next((c for c in self.cards if c.value == pc.value), None) != None:
            self.cards.append(pc)
            return Pair(self.cards, pc)

        self.cards.append(pc)

        if len(self.cards) == 5:
            ## check for flush
            isFlush = next((c for c in self.cards[:-1] if c.suite != pc.suite), None) == None
            ## check for straight
            cards = sorted(self.cards)
            valueList = list(PokerCard.values)
            firstCardIdx = valueList.index(cards[0].value)
            isStraight = True
            for i in range(0, 5):
                if cards[i].value != valueList[firstCardIdx + i]:
                    isStraight = False
                    break

            # check for low straight
            if (cards[0].value == '2' and 
                cards[1].value == '3' and 
                cards[2].value == '4' and
                cards[3].value == '5' and
                cards[4].value == 'A'):
                isStraight = True

            if isFlush and isStraight:
                return StraightFlush(self.cards)
            if isFlush:
                return Flush(self.cards)
            if isStraight:
                return Straight(self.cards)

        return self

class Pair(Hand):

    def __init__(self, cards, pair):
        self.rank = 2
        self.cards = cards
        self.pair = pair

    def __lt__(self, card):
        if self.pair < card.pair:
            return True
        if self.pair > card.pair:
            return False

        myOtherCards =  self.otherCards()
        cardOtherCards = card.otherCards()
        for i in range(3):
            if myOtherCards[i] < cardOtherCards[i]:
                return True
            if myOtherCards[i] > cardOtherCards[i]:
                return False
        return False
    
    @lru_cache(None)
    def otherCards(self):
        return sorted([c for c in self.cards if c.value != self.pair.value], reverse=True)

    def Draw(self, card):
        pc = PokerCard(card)

        # check for 3 of a kind 
        if self.pair.value == pc.value :
            self.cards.append(pc)
            return ThreeOfKind(self.cards, pc)

        # check for second pair
        pair2 = next((c for c in self.cards if c.value != self.pair.value and c.value == pc.value), None)
        if (pair2 != None):
            self.cards.append(pc)
            return TwoPairs(self.cards, self.pair, pc)

        self.cards.append(pc)
        return self

class TwoPairs(Hand):

    def __init__(self, cards, pair1, pair2):
        self.rank = 3
        self.cards = cards 
        self.pair1 = pair1
        self.pair2 = pair2

    def __lt__(self, card):
        myPairs = self.pairs()
        cardPairs = card.pairs() 
        for i in range(2):
            if myPairs[i] < cardPairs[i]:
                return True
            if myPairs[i] > cardPairs[i]:
                return False

        return self.otherCard() < card.otherCard()
    
    @lru_cache(None)
    def otherCard(self):
        return next((c for c in self.cards if c.value != self.pair1.value and c.value != self.pair2.value), None)

    def pairs(self):
        return sorted([self.pair1, self.pair2], reverse=True)

    def Draw(self, card):
        pc = PokerCard(card)
        # check for full house
        pair3 = next((c for c in self.cards if c.value == pc.value), None)
        if pair3 != None:
            self.cards.append(pc)
            return FullHouse(self.cards, 
                pc, self.pair2 if pc.value == self.pair1.value else self.pair1)
 
        self.cards.append(pc)
        return self

class ThreeOfKind(Hand):

    def __init__(self, cards, pair):
        self.rank = 4
        self.cards = cards
        self.pair = pair 

    def __lt__(self, card):
        if self.pair < card.pair:
            return True
        if self.pair > card.pair:
            return False
        
        myOtherCards =  self.otherCards()
        cardOtherCards = card.otherCards()
        for i in range(3):
            if myOtherCards[i] < cardOtherCards[i]:
                return True
            if myOtherCards[i] > cardOtherCards[i]:
                return False
        return False
    
    @lru_cache(None)
    def otherCards(self):
        return sorted([c for c in self.cards if c.value != self.pair.value], reverse=True)

    def Draw(self, card):
        pc = PokerCard(card)
        
        # Check for FourOfKind
        if self.pair.value == pc.value:
            self.cards.append(card)
            return FourOfKind(self.cards, pc)
        
        # Check for FullHouse 
        if len(self.cards) == 4:
            pair = next((c for c in self.cards 
                if c.value != self.pair.value and c.value == pc.value), None)
            if pair != None:
                self.cards.append(pc)
                return FullHouse(self.cards, self.pair, pc)

        self.cards.append(pc)
        return self

class FourOfKind(Hand):

    def __init__(self, cards, pair):
        self.rank = 8
        self.cards = cards
        self.pair = pair 
    
    def __lt__(self, card):
        if self.pair < card.pair:
            return True
        if self.pair > card.pair:
            return False
        return self.otherCard() < card.otherCard()
    
    @lru_cache(None)
    def otherCard(self):
        return next((c for c in self.cards if c.value != self.pair.value), None)

    def Draw(self, card):
        pc = PokerCard(card)
        self.cards.append(card)
        return self

class FullHouse(Hand):

    def __init__(self, cards, tree, two):
        self.rank = 7
        self.cards = cards
        self.tree = tree
        self.two = two 
    
    def __lt__(self, card):
        if self.tree < card.tree:
            return True
        if self.tree > card.tree:
            return False
        if self.two < card.two:
            return True

        return False

    def Draw(self, card):
        raise ValueError("This should not be possible")

class Straight(Hand):

    def __init__(self, cards):
        self.rank = 5
        self.cards = cards

    def __lt__(self, card):
        return self.allCards()[0] < card.allCards()[0]
    
    @lru_cache(None)
    def allCards(self):
        sortedCards = sorted(self.cards, reverse=True)
        if sortedCards[0].value == "A" and sortedCards[4].value == '2':
            sortedCards.append(sortedCards.pop(0))
            return sortedCards

        return sortedCards

    def Draw(self, card):
        raise ValueError("This should not be possible")

class Flush(Hand):

    def __init__(self, cards):
        self.rank = 6
        self.cards = cards
        
    def __lt__(self, card):
        myCards = self.allCards()
        cardCards = card.allCards()

        for i in range(0, 5):
            if myCards[i] < cardCards[i]:
                return True 
            if myCards[i] > cardCards[i]:
                return False
        return False
    
    @lru_cache(None)
    def allCards(self):
        return sorted(self.cards,reverse=True)

    def Draw(self, card):
        raise ValueError("This should not be possible")

class StraightFlush(Hand):

    def __init__(self, cards):
        self.rank = 9
        self.cards = cards
    
    def __lt__(self, card):
        return self.allCards()[0] < card.allCards()[0]

    @lru_cache(None)
    def allCards(self):
        sortedCards = sorted(self.cards, reverse=True)
        if sortedCards[0].value == "A" and sortedCards[4].value == '2':
            sortedCards.append(sortedCards.pop(0))
            return sortedCards

        return sortedCards

    def Draw(self, card):
        raise ValueError("This should not be possible")


class PokerHand(object):

    def __repr__(self):  return self.hand

    def __init__(self, hand):
        self.value = None
        self.hand = hand
        self.calcValue()
        # Your code below:
    def __lt__(self, hand):
        if self.value.rank == hand.value.rank:
            return self.value > hand.value
        return self.value.rank > hand.value.rank

    def calcValue(self):
        r = HighCard()
        for card in self.hand.split():
            r = r.Draw(card.upper())
        self.value = r

