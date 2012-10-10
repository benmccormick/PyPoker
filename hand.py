import cardconstants


class HandFunctions():

    constants = cardconstants.Constants()

    def setDeck(self):
        deck = []
        for val in range(2, 15):
            deck.append('H' + str(val))
            deck.append('S' + str(val))
            deck.append('C' + str(val))
            deck.append('D' + str(val))
        return deck

    def numVal(self, card):
        return int(card[1:])

    # Assumes valid hands in form Hand-type, C1,...,C5
    # Returns 1 if the first hand is greater, -1 if the second is greater
    # and returns 0 if they're equal
    def compareHands(self, hand1, hand2):
        if (self.constants.rankings[hand1[0]] >
            self.constants.rankings[hand2[0]]):
            return 1
        elif (self.constants.rankings[hand1[0]] <
            self.constants.rankings[hand2[0]]):
            return -1
        else:
            for index in range(1, len(hand1)):
                if(hand1[index] != hand2[index]):
                    return (1 if (hand1[index] > hand2[index]) else -1)
            return 0

    #Given the cards that make up the core of the hand,
    #fill in with the remaining highest
    # Expects the hand type to be in the first slot
    def fillInHand(self, hand, oldcards):
        cards = [] + oldcards
        for card in hand:
            if card in cards:
                cards.remove(card)
        cards = sorted(cards, key=self.numVal, reverse=True)
        cardToAdd = 0
        while len(hand) < 6:
            hand.append(cards[cardToAdd])
            cardToAdd += 1
        return hand

    def getCardsFromVal(self, cards, val):
        hand = []
        for card in cards:
            if self.numVal(card) == val:
                hand.append(card)
        return hand

    def isFlush(self, cards):
        suits = self.constants.suits
        for suit in suits:
            counter = 0
            for card in cards:
                if card[0] == suit:
                    counter += 1
            if counter >= 5:
                for card in cards:
                    if card[0] != suit:
                        cards.remove(card)
                cards = sorted(cards, key=self.numVal)
                return [self.constants.flush] + cards[-5:]
        return False

    # Assumes that it is a flush and we know the suit
    def isStraightFlush(self, oldcards, suit):
        cards = sorted(oldcards, key=self.numVal, reverse=True)
        for card in cards:
            if card[0] != suit:
                cards.remove(card)
        return [self.constants.sflush] + self.isStraight(cards)[1:]

    def isStraight(self, cards):
        cards = sorted(cards, key=self.numVal, reverse=True)
        counter = 0
        for num in range(0, len(cards) - 1):
            if self.numVal(cards[num]) == self.numVal(cards[num + 1]) + 1:
                counter += 1
            elif self.numVal(cards[num]) != self.numVal(cards[num + 1]):
                counter = 0
            if counter == 4:
                return [self.constants.straight] + cards[num - 3:num + 2]
            # Special Case for Low Aces
            elif (counter == 3 and self.numVal(cards[num + 1]) == 2
                  and self.numVal(cards[0]) == 14):
                return ([self.constants.straight] + cards[num - 3:num + 1]
                        + [cards[0]])

        return False

    def getBestSets(self, cards):
        values = [0] * 15  # Initialize an array of 14 0s
        matches = {}
        hand = []
        for card in cards:
            values[self.numVal(card)] += 1
        for index in range(2, 15):
            # if 4, just return
            if values[index] == 4:
                for suit in self.constants.suits:
                    hand.append(suit + str(index))
                    hand = [self.constants.four] + hand
                hand = self.fillInHand(hand, cards)
                return hand
            elif values[index] == 3:
                matches['three'] = index
            elif values[index] == 2:
                if 'two1' in matches:
                    matches['two2'] = matches['two1']
                matches['two1'] = index
        # Determine what the combination is
        if 'three' in matches:
            if 'two1' in matches:
                hand = ([self.constants.house] +
                self.getCardsFromVal(cards, matches['three']) +
                self.getCardsFromVal(cards, matches['two1']))
            else:
                hand = ([self.constants.three] +
                self.getCardsFromVal(cards, matches['three']))
                hand = self.fillInHand(hand, cards)
        elif 'two1' in matches:
            if 'two2' in matches:
                hand = ([self.constants.twopair] +
                self.getCardsFromVal(cards, matches['two1']) +
                self.getCardsFromVal(cards, matches['two2']))
                hand = self.fillInHand(hand, cards)
            else:
                hand = ([self.constants.pair] +
                self.getCardsFromVal(cards, matches['two1']))
                hand = self.fillInHand(hand, cards)
        else:
            hand = [self.constants.none]
            hand = self.fillInHand(hand, cards)
        return hand

    def whatIsIt(self, cards):
        flush = self.isFlush(cards)
        bestSets = self.getBestSets(cards)
        straight = self.isStraight(cards)
        if flush:
            if bestSets and (bestSets[0] == self.constants.four):
                return bestSets
            else:
                if straight:
                    # if its a straight & flush, check if its a straight flush
                    # TODO: Make this less tightly coupled to card impl
                    sflush = self.isStraightFlush(cards, flush[1][0])
                    if sflush:
                        return sflush
                return flush
        if straight:
            return straight
        else:
            return bestSets


