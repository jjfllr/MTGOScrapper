class Match:
    player1 = ""
    player2 = ""
    result = ""

    def __init__(self, player1="", player2="", result=""):
        self.player1 = player1
        self.player2 = player2
        self.result = result

    def set_player1(self, player):
        if not isinstance(player, str):
            raise ValueError('Parameter is not str')
        else:
            self.player1 = player

    def get_player1(self):
        return self.player1

    def set_player2(self, player):
        if not isinstance(player, str):
            raise ValueError('Parameter is not str')
        else:
            self.player2 = player

    def get_player2(self):
        return self.player2

    def set_result(self, result):
        if not isinstance(result, str):
            raise ValueError('Parameter is not str')
        else:
            self.result = result

    def get_result(self):
        return self.result

    def get_players(self):
        return [self.player1, self.player2]