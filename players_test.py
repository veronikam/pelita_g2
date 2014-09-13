
from pelita.player import SimpleTeam
from pelita.layout import get_random_layout
from pelita.game_master import GameMaster

from demo_player import DrunkPlayer
from franzi_player import FranziPlayer
from players.FoodEatingPlayer import FoodEatingPlayer
from players.SmartRandomPlayer import SmartRandomPlayer


class Simulation():

    def __init__(self, teams, n_sim, game_time=300, seed=20, fname = "stats.txt"):
        # do (only) initializations here
        self.teams = teams
        self.n_sim = n_sim
        self.game_time = game_time
        self.seed = seed 
        self.fname = fname       
        self.stats = {"winning_team": [], "food_eaten":{"t0":[],"t1":[]}, "rounds": [], "team_disqualified": [], "timeout_teams": {"t0":[],"t1":[]}, 
                        "team_time": {"t0":[],"t1":[]}, "bots_destroyed": [], "times_killed": {"t0":[],"t1":[]}, "score":{"t0":[],"t1":[]} }
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

            #import pdb; pdb.set_trace()            
            #Append statistics of the last game
            self.stats["winning_team"].append(self.gm.game_state["team_wins"])
            self.stats["food_eaten"]["t0"].append(self.gm.game_state["food_count"][0])
            self.stats["food_eaten"]["t1"].append(self.gm.game_state["food_count"][1])
            self.stats["rounds"].append(self.gm.game_state["round_index"])
            self.stats["bots_destroyed"].append(self.gm.game_state["bot_destroyed"])
            self.stats["timeout_teams"]["t0"].append(self.gm.game_state["timeout_teams"][0])
            self.stats["timeout_teams"]["t1"].append(self.gm.game_state["timeout_teams"][1])
            self.stats["team_time"]["t0"].append(self.gm.game_state["team_time"][0])
            self.stats["team_time"]["t1"].append(self.gm.game_state["team_time"][1])
            self.stats["times_killed"]["t0"].append(self.gm.game_state["times_killed"][0])
            self.stats["times_killed"]["t1"].append(self.gm.game_state["times_killed"][1])
            self.stats["score"]["t0"].append(self.gm.universe.teams[0].score)
            self.stats["score"]["t1"].append(self.gm.universe.teams[1].score)
	        
	    
            winner = self.stats["winning_team"][-1]
            
            if winner is not None: 
                self.score[winner] += 1
                win = "Team %r wins" %self.gm.universe.teams[winner].name
            else: 
                win = "None wins"

            print "%s game %i. Score so far %i:%i" %(win, game, self.score[0], self.score[1])
        
    
    def get_stats(self):
                
        self.f = open(self.fname, 'w')
        
        self.f.write(str(self.stats)+"\n")
        print self.stats
        
        #---Number of winnig times
        n_win = "Number of games won by team 0: %d, team1: %d" %(self.score[0], self.score[1])        
        print n_win
        self.f.write(n_win+"\n")
        
        #---Average rounds
        av_rounds = float(sum(self.stats["rounds"]))/self.n_sim
        rounds_str = "Average rounds: %d" %(av_rounds)        
        print rounds_str
        self.f.write(rounds_str+"\n")


        #---Average food eaten
        self.write_stats_line("Average food eaten by", "food_eaten")
        #---Sum of time outs
        self.write_stats_line("Timeouts by", "timeout_teams",
            is_average = None, is_float = None)
        #---Average time
        self.write_stats_line("Average game time for", "team_time")
        #---Sum of times killed
        self.write_stats_line("Bots killed of", "times_killed",
            is_average = None, is_float = None)
        
        self.f.close()

    def write_stats_line(self, title, key, is_average = True, is_float = True):
        
        sum0 = sum(self.stats[key]["t0"]); sum1 = sum(self.stats[key]["t1"])
        
        if is_average: 
            n = self.n_sim   
        else:
            n = 1
        
        if is_float:
            sum0 = float(sum0); sum1 = float(sum1); n = float(n)
        
        stats_line = title + " " + self.gm.universe.teams[0].name + ": " + \
            str(sum0/n) + ", " + self.gm.universe.teams[1].name  + ": " + str(sum1/n)
        
        print stats_line
        self.f.write(stats_line + "\n")
        

if __name__ == "__main__":
    # define teams as dict: team name, 2 players
    # teams = {"FoodEaters": [FoodEatingPlayer(), FoodEatingPlayer()],
    #          "SmartRandom": [SmartRandomPlayer(), SmartRandomPlayer()]}
    teams = {"FranziTest": [FoodEatingPlayer(), FoodEatingPlayer()],
             "SmartRandom": [FoodEatingPlayer(), FoodEatingPlayer()]}
    # initialize simulation  
    sim = Simulation(teams, 3)
    # actually run the simulation
    sim.run_simulation()
    sim.get_stats()
    
    
    print "Good game! Final score", sim.score
