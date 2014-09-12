
from pelita.player import SimpleTeam
from pelita.layout import get_random_layout
from pelita.game_master import GameMaster

from .demo_player import DrunkPlayer
from players.FoodEatingPlayer import FoodEatingPlayer
from players.SmartRandomPlayer import SmartRandomPlayer


class Simulation():

    def __init__(self, teams, n_sim, game_time=300, seed=20):
        # do (only) initializations here
        self.teams = teams
        # self.team0 = SimpleTeam("team0", team0[0], team0[1])
        # self.team1 = SimpleTeam("team1", team1[0], team1[1])
        self.n_sim = n_sim
        self.game_time = game_time
        self.seed = seed        
        self.score = [0, 0]
        
    def run_simulation(self):
        # run the actual simulation for a defined amount of runs
        for game in range(self.n_sim):
            print "Game %i" %game            
            self.layout = get_random_layout(filter="normal_without_dead_ends")[1]
            self.gm = GameMaster(self.layout, number_bots=4, 
                                 game_time=self.game_time, seed=self.seed)
            for t in self.teams:
                self.gm.register_team(SimpleTeam(t, self.teams[t][0], self.teams[t][1]))
            self.gm.play()            
            winner = self.gm.game_state['team_wins']
            if winner is not None: 
                self.score[winner] += 1
                win = "Team %r wins" %self.gm.universe.teams[winner].name
            else: 
                win = "None wins"
                
            print "%s game %i. Score so far %i:%i" %(win, game, self.score[0], self.score[1])
            

if __name__ == "__main__":
    # define teams as dict: team name, 2 players
    teams = {"FoodEaters": [FoodEatingPlayer(), FoodEatingPlayer()],
             "SmartRandom": [SmartRandomPlayer(), SmartRandomPlayer()]}
    # initialize simulation  
    sim = Simulation(teams, 50)
    # actually run the simulation
    sim.run_simulation()
    print "Good game! Final score", sim.score
