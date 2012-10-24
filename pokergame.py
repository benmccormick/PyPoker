from random import shuffle
import random
import hand


class PokerGame:

    CHECK = "Check"
    CALL = "Call"
    RAISE = "Raise"
    FOLD = "Fold"

    def setUpDeck(self, hand):
        self.deck = hand.setDeck()

    def setUpStack(self, stack):
        self.stack = stack

    def isDecentHand(self, card1, card2, test):
        return ((test.numVal(card1) == test.numVal(card2)) or
                (test.numVal(card1) > 6 and test.numVal(card2) > 6) or
                (test.numVal(card1) + test.numVal(card2) > 16))

    def handDist(self, hand, winningHands):
        type = hand[0]
        if type in winningHands:
            winningHands[type] = winningHands[type] + 1
        else:
            winningHands[type] = 1

    def getHandStrength(self, card1, card2, numplayers, flop=[], turn=[], river=[]):
        winningHands = {}
        test = hand.HandFunctions()
        score = 0
        loops = 1000
        for index in range(loops):
            hands = []
            self.setUpDeck(test)
            self.deck.remove(card1)
            self.deck.remove(card2)
            shuffle(self.deck)
            others = flop + turn + river
            for card in others:
                self.deck.remove(card)
            for playnum in range(numplayers - 1):
                hands.append([self.deck.pop(), self.deck.pop()])
            others = others + self.deck[len(others):5]
            isBestHand = True
            samecount = 1
            for playnum in range(numplayers - 1):
                myHand = test.whatIsIt([card1] + [card2] + others)
                c1 = hands[playnum][0]
                c2 = hands[playnum][1]
                otherHand = test.whatIsIt(hands[playnum] + others)
                res = test.compareHands(myHand, otherHand)
                if res < 0:
                    if (self.isDecentHand(c1, c2, test)):
                        self.handDist(otherHand, winningHands)
                        isBestHand = False
                elif res == 0:
                    samecount += 1
            if isBestHand:
                self.handDist(myHand, winningHands)
                score += 1 / samecount
        return score / loops

    def getPotOdds(self, bet, pot):
            if bet == 0:
                return 0
            else:
                return bet / (pot + bet)

    def getROR(self, strength, potodds):
        if potodds == 0:
            return -1
        return strength / potodds

    def getRec(self, card1, card2, bet, pot, players,
                          flop=[], turn=[], river=[]):
        hs = self.getHandStrength(card1, card2, players, flop, turn, river)
        potodds = self.getPotOdds(bet, pot)
        ror = self.getROR(hs, potodds)
        dist = random.random()
        if ror == -1:
            if hs < 0.3 or dist < 0.7:
                return self.CHECK +  " " + str(ror) + " " + str(hs)
            else:
                return self.RAISE +  " " + str(ror) + " " + str(hs)
        elif ror < 0.8:
            if dist < 0.95:
                return self.FOLD +  " " + str(ror) + " " + str(hs)
            else:
                return self.RAISE +  " " + str(ror) + " " + str(hs)
        elif ror < 1:
            if dist < 0.80:
                return self.FOLD +  " " + str(ror) + " " + str(hs)
            elif dist < 0.85:
                return self.CALL +  " " + str(ror) + " " + str(hs)
            else:
                return self.RAISE +  " " + str(ror) + " " + str(hs)
        elif ror < 1.3:
            if dist < 0.60:
                return self.CALL +  " " + str(ror) + " " + str(hs)
            else:
                return self.RAISE +  " " + str(ror) + " " + str(hs)
        else:
            if dist < 0.30:
                return self.CALL +  " " + str(ror) + " " + str(hs)
            else:
                return self.RAISE +  " " + str(ror) + " " + str(hs)




def main():
    game = PokerGame()
    print("Aces " + str(game.getRec("H14", "C14", 20, 60, 5)))

    print("Aces with bad flop " + str(game.getRec("H14", "C14", 20, 60, 5, ["D10", "D9", "D8"],["D7"],["C5"])))

if __name__ == "__main__":
    main()
