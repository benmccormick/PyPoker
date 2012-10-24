import unittest
import hand
import cardconstants

class TestSequenceFunctions(unittest.TestCase):

    ## Test Helper Methods ##

    def setUp(self):
        self.hand = hand.HandFunctions()
        self.constants = cardconstants.Constants()
        testhands = []
        #High Card
        testhands.append(self.hand.whatIsIt(['H14', 'C12', 'S3', 'H5', 'H6', 'S7', 'C10']))
        #Pair
        testhands.append(self.hand.whatIsIt(['H2', 'C3', 'S3', 'H5', 'H6', 'S7', 'C10']))
        #Two Pair
        testhands.append(self.hand.whatIsIt(['H2', 'C3', 'S3', 'D2', 'H6', 'S7', 'C10']))
        #Three of a Kind
        testhands.append(self.hand.whatIsIt(['H3', 'C3', 'S3', 'D2', 'H6', 'S7', 'C10']))
        #Straight
        testhands.append(self.hand.whatIsIt(['H2', 'H3', 'C4', 'H5', 'H6', 'S7', 'C10']))
        #Flush
        testhands.append(self.hand.whatIsIt(['H2', 'H3', 'C2', 'H5', 'H6', 'S7', 'H10']))
        #Full House
        testhands.append(self.hand.whatIsIt(['H2', 'C2', 'S3', 'D3', 'H3', 'S7', 'C10']))
        #Four of a Kind
        testhands.append(self.hand.whatIsIt(['H2', 'C2', 'S2', 'D2', 'H6', 'S7', 'C10']))
        #Straight Flush
        testhands.append(self.hand.whatIsIt(['H2', 'H3', 'H4', 'H5', 'H8', 'H7', 'H14']))
        self.testhands = testhands

    def handType(self, hand):
        if not hand:
            hand = [False]
        return hand[0]

    ## Hand ID Tests ##

    def test_straight_flush(self):
        hand = self.hand.whatIsIt(['H2', 'H3', 'H4', 'H5', 'H6', 'H7', 'H8'])
        self.assertEqual(self.handType(hand), self.constants.sflush)
        hand = self.hand.whatIsIt(['H2', 'H3', 'H4', 'H5', 'H8', 'H7', 'H14'])
        self.assertEqual(self.handType(hand), self.constants.sflush)

    def test_flush(self):
        hand = self.hand.whatIsIt(
            ['H2', 'H3', 'C2', 'H5', 'H6', 'S7', 'H10'])
        self.assertEqual(self.handType(hand), self.constants.flush)

    def test_straight(self):
        hand = self.hand.whatIsIt(
            ['H2', 'H3', 'C4', 'H5', 'H6', 'S7', 'C10'])
        self.assertEqual(self.handType(hand), self.constants.straight)
        hand = self.hand.whatIsIt(
            ['H2', 'H3', 'C4', 'H5', 'D8', 'C7', 'D14'])
        self.assertEqual(self.handType(hand), self.constants.straight)

    def test_full_house(self):
        hand = self.hand.whatIsIt(
            ['H2', 'C2', 'S3', 'D3', 'H3', 'S7', 'C10'])
        self.assertEqual(self.handType(hand), self.constants.house)

    def test_four(self):
        hand = self.hand.whatIsIt(
            ['H2', 'C2', 'S2', 'D2', 'H6', 'S7', 'C10'])
        self.assertEqual(self.handType(hand), self.constants.four)

    def test_three(self):
        hand = self.hand.whatIsIt(
            ['H3', 'C3', 'S3', 'D2', 'H6', 'S7', 'C10'])
        self.assertEqual(self.handType(hand), self.constants.three)

    def test_twopair(self):
        hand = self.hand.whatIsIt(
            ['H2', 'C3', 'S3', 'D2', 'H6', 'S7', 'C10'])
        self.assertEqual(self.handType(hand), self.constants.twopair)

    def test_pair(self):
        hand = self.hand.whatIsIt(
            ['H2', 'C3', 'S3', 'H5', 'H6', 'S7', 'C10'])
        self.assertEqual(self.handType(hand), self.constants.pair)

    def test_none(self):
        hand = self.hand.whatIsIt(
            ['H14', 'C12', 'S3', 'H5', 'H6', 'S7', 'C10'])
        self.assertEqual(self.handType(hand), self.constants.none)

    ## Hand Comparison Tests ##

    def test_hand_order(self):
        for lowhand in range(0, len(self.testhands)):
            for highhand in range(lowhand + 1, len(self.testhands)):
                self.assertEqual(self.hand.compareHands(
                                self.testhands[highhand],
                                self.testhands[lowhand]), 1)

    def test_self_equality(self):
        for hand in range(0, len(self.testhands)):
            samehand = self.testhands[hand]
            self.assertEqual(self.hand.compareHands(samehand, samehand), 0)

    def test_higher_card(self):
        hand1 = self.hand.whatIsIt(['H2', 'C2', 'S3', 'D3', 'H6', 'S7', 'C10'])
        hand2 = self.hand.whatIsIt(['H2', 'C2', 'S3', 'D3', 'H6', 'S8', 'C11'])
        hand3 = self.hand.whatIsIt(['H2', 'C2', 'S3', 'D3', 'H7', 'S8', 'C11'])
        hand4 = self.hand.whatIsIt(['H2', 'C2', 'S3', 'D3', 'H7', 'S8', 'C10'])
        self.assertEqual(self.hand.compareHands(hand2, hand1), 1)
        self.assertEqual(self.hand.compareHands(hand3, hand1), 1)
        self.assertEqual(self.hand.compareHands(hand4, hand1), 0)

    def test_higher_pairs(self):
        hand1 = self.hand.whatIsIt(['H6', 'C6', 'S5', 'D3', 'H11', 'S7', 'C10'])
        hand2 = self.hand.whatIsIt(['H14', 'C14', 'S5', 'D3', 'H11', 'S7', 'C10'])
        hand3 = self.hand.whatIsIt(['H2', 'C2', 'S4', 'D3', 'H7', 'S8', 'C11'])
        hand4 = self.hand.whatIsIt(['H2', 'C2', 'S3', 'D3', 'H7', 'S8', 'C10'])
        self.assertEqual(self.hand.compareHands(hand2, hand1), 1)
        self.assertEqual(self.hand.compareHands(hand3, hand1), -1)
        self.assertEqual(self.hand.compareHands(hand4, hand1), 1)

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestSequenceFunctions)
    unittest.TextTestRunner(verbosity=2).run(suite)
