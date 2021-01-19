def display_title():
    print("Rank\tPlayer\t\t\t\t\tPoints\tOMWP\t\tGWP\t\t\tOGWP")


class Rank:
    rank = 0
    player = ""
    points = 0
    omwp = 0.0  # Opponents' Match-Win Percentage
    gwp = 0.0  # Game-Win Percentage
    ogwp = 0.0  # Oponnents' Game-Win Percentage

    def __init__(self, rank=0, player="", points=0, omwp=0.0, gwp=0.0, ogwp=0.0):
        self.rank = rank
        self.player = player
        self.points = points
        self.omwp = omwp
        self.gwp = gwp
        self.ogwp = ogwp

    def display_with_title(self):
        display_title()
        self.display()

    def display(self):
        print("{:02d}\t\t{: <20}\t{:02d}\t\t{:.4f}\t\t{:.4f}\t\t{:.4f}".format(self.rank, self.player, self.points, self.omwp, self.gwp, self.ogwp))

    def set_rank(self, place):
        if not isinstance(place, int):
            raise ValueError('Parameter is not int')
        else:
            self.rank = place

    def get_rank(self):
        return self.rank

    def set_player(self, player):
        if not isinstance(player, str):
            raise ValueError('Parameter is not str')
        else:
            self.rank = player

    def get_player(self):
        return self.player

    def set_points(self, points):
        if not isinstance(points, int):
            raise ValueError('Parameter is not int')
        else:
            self.rank = points

    def get_points(self):
        return self.points

    def set_omwp(self, percentage):
        if not isinstance(percentage, float):
            raise ValueError('Parameter is not float')
        else:
            self.omwp = percentage

    def get_omwp(self):
        return self.omwp

    def set_gwp(self, percentage):
        if not isinstance(percentage, float):
            raise ValueError('Parameter is not float')
        else:
            self.gwp = percentage

    def get_gwp(self):
        return self.gwp

    def set_ogwp(self, percentage):
        if not isinstance(percentage, float):
            raise ValueError('Parameter is not float')
        else:
            self.ogwp = percentage

    def get_ogwp(self):
        return self.ogwp
