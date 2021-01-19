class Deck:
    pilot = ""
    score = ""
    mainboard = []
    sideboard = []

    def __init__(self, pilot="", score="", mainboard=[], sideboard=[]):
        self.pilot = pilot
        self.score = score
        self.mainboard = mainboard
        self.sideboard = sideboard

    def display(self):
        print("pilot: " + self.pilot)
        print("score: " + self.score)
        print("Deck:")

        if self.mainboard:
            for item in self.mainboard:
                print("\t" + str(item[0]) + ' ' + item[1])
        print("Sideboard:")
        if self.sideboard:
            for item in self.sideboard:
                print("\t" + str(item[0]) + ' ' + item[1])