
from pelita.player import SimpleTeam
from pelita.layout import get_random_layout
from pelita.game_master import GameMaster

from demo_player import DrunkPlayer
from franzi_player import FranziPlayer
from players.FoodEatingPlayer import FoodEatingPlayer
from players.SmartRandomPlayer import SmartRandomPlayer


class Simulation():

    def __init__(self, teams, n_sim, game_time=300, seed=20):
        # do (only) initializations here
        self.teams = teams
        self.n_sim = n_sim
        self.game_time = game_time
        self.seed = seed        
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
                
        f = open("stats.txt", 'w')
        
        f.write(str(self.stats)+"\n")
        print self.stats
        
        #---Number of winnig times
        n_win = "Number of games won by team 0: %d, team1: %d" %(self.score[0], self.score[1])        
        print n_win
        f.write(n_win+"\n")
        
        #---Average rounds
        av_rounds = float(sum(self.stats["rounds"]))/self.n_sim
        rounds_str = "Average rounds: %d" %(av_rounds)        
        print rounds_str
        f.write(rounds_str+"\n")


        #---Average food eaten
        av_food0 = float(sum(self.stats["food_eaten"]["t0"]))/float(self.n_sim)
        av_food1 = float(sum(self.stats["food_eaten"]["t1"]))/float(self.n_sim)
        food_string = "Average food eaten by team 0: %2f, team1: %2f" %(av_food0, av_food1)        
        print food_string
        f.write(food_string+"\n")
        
        #---Sum of time outs
        sum_timeouts0 = sum(self.stats["timeout_teams"]["t0"])
        sum_timeouts1 = sum(self.stats["timeout_teams"]["t1"])
        timeout_string = "Timeouts by team 0: %d, team1: %d" %(sum_timeouts0, sum_timeouts1)        
        print timeout_string
        f.write(timeout_string+"\n")
        
        #---Average time
        av_time0 = float(sum(self.stats["team_time"]["t0"]))/float(self.n_sim)
        av_time1 = float(sum(self.stats["team_time"]["t1"]))/float(self.n_sim)
        time_string = "Average game time for team0: %2f, team1: %2f" %( av_time0,  av_time1)        
        print time_string
        f.write(time_string+"\n") 

        #---Average times killed
        av_killed0 = float(sum(self.stats["times_killed"]["t0"]))/float(self.n_sim)
        av_killed1 = float(sum(self.stats["times_killed"]["t1"]))/float(self.n_sim)
        killed_string = "Average times killed for team 0: %2f, team1: %2f" %(av_killed0, av_killed1)        
        print killed_string
        f.write(killed_string+"\n")       
        
        
        
        f.close()
                

if __name__ == "__main__":
    # define teams as dict: team name, 2 players
    # teams = {"FoodEaters": [FoodEatingPlayer(), FoodEatingPlayer()],
    #          "SmartRandom": [SmartRandomPlayer(), SmartRandomPlayer()]}
    teams = {"FranziTest": [FoodEatingPlayer(), FoodEatingPlayer()],
             "SmartRandom": [FoodEatingPlayer(), FoodEatingPlayer()]}
    # initialize simulation  
    sim = Simulation(teams, 10)
    # actually run the simulation
    sim.run_simulation()
    sim.get_stats()
    
    
    print "Good game! Final score", sim.score
