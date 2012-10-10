class Constants:
    suits = ['H', 'S', 'C', 'D']
    none = "High Card"
    pair = "1 Pair"
    twopair = "2 Pair"
    three = "Three of a kind"
    straight = "Straight"
    flush = "Flush"
    house = "Full House"
    four = "Four of a kind"
    sflush = "Straight Flush"
    rankings = {none: 0, pair: 1, twopair: 2, three: 3, straight: 4,
                flush: 5, house: 6, four: 7, sflush: 8}

    # class seems to need a method to exist
    def getConstants(self):
        return self
