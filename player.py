class Player:
    def __init__(self, player_id: int, num_picks=0):
        self.player_id = player_id
        self.num_picks = num_picks

    def dec_num_picks(self) -> int:
        self.num_picks -= 1

        return self.num_picks

    def get_num_picks(self) -> int:
        return self.num_picks

    def get_player_id(self) -> int:
        return self.player_id
    

