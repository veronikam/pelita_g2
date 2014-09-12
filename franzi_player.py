# -*- coding: utf-8 -*-

from pelita.player import AbstractPlayer
from pelita.datamodel import north, south, west, east, stop
from pelita.graph import AdjacencyList

# use relative imports for things inside your module
#from .utils import utility_function


class FranziPlayer(AbstractPlayer):
    """ Basically a really awesome player. """

    def __init__(self, priority_dir='stop', w_pdir=1, w_mate=-2, w_danger=-20, w_eat=3, w_defend=10, save_dist=5.):
        """
        Attributes:
            - priority_dir: which direction to favor ('up' or 'down')
            - w_pdir: how important it is to go into the favored direction
            - w_mate: how important it is to stay within reasonable distance from the teammate
            - w_danger: how important it is to avoid enemy destroyers
            - w_eat: how important it is to eat the enemy's food
            - w_defend: how important it is to kill enemy harvesters
        """
        if priority_dir == 'up':
            self.priority_dir = north
        elif priority_dir == 'down':
            self.priority_dir = south
        else:
            raise RuntimeWarning("Invalid priority_dir, use either up or down!")
            self.priority_dir = None
        self.save_dist = float(save_dist)
        self.w_danger = w_danger
        self.w_eat = w_eat
        self.w_pdir = w_pdir
        self.w_mate = w_mate
        self.w_defend = w_defend
        self.adjacency = None  # to store an adjacency list with all possible positions 

    def set_initial(self):
        # Now ``self.current_uni`` and ``self.current_state`` are known.
        # ``set_initial`` is always called before ``get_move``, so we can do some
        # additional initialization here
        self.adjacency = AdjacencyList(self.current_uni.reachable([self.initial_pos]))
        # Just printing the universe to give you an idea, please remove all
        # print statements in the final player.
        print self.current_uni.pretty

    def shortest_path(self, pos1, pos2):
        """
        In the current maze, get the shortest path (list of positions) from pos1 to pos2
        The length of this list is the maze distance of both positions

        will raise according exceptions if the positions are not reachable, etc.
        """
        # using the a* search, you get a list of positions [pos2, ..., next_to_pos1]
        # ideally this path should be further pruned by removing unnecessary
        # detours introduced by using the manhattan distance as a heuristic
        return self.adjacency.a_star(pos1, pos2)

    def compute_min_dist(self, pos, other_pos):
        """
        Inputs:
            - pos: for which position the distances should be computed
            - other_pos: a list of other positions (if any)
        Returns:
            - min_dist: the maze distance to the closest other position in the
                given list to our pos
              the distance is 0 if there are no other positions given
              (or the distance is actually 0, i.e. the bot is on this spot)
        """
        if other_pos:
            return min([len(self.shortest_path(pos, i_pos)) 
                            for i_pos in other_pos])
        return 0


    def get_move(self):
        # get to know something about our surroundings
        dangerous_enemy_pos = [bot.current_pos for bot in self.enemy_bots if bot.is_destroyer]
        killable_enemy_pos = [bot.current_pos for bot in self.enemy_bots if bot.is_harvester]
        teammate_pos = [bot.current_pos for bot in self.team_bots if not bot==self.me]
        # compute how good our current position is
        curr_min_dist_food = self.compute_min_dist(self.current_pos, self.enemy_food)
        curr_min_dist_kill = self.compute_min_dist(self.current_pos, killable_enemy_pos)
        scored_moves = {}
        for move, new_pos in list(self.legal_moves.items()):
            # filter out obviously stupid moves
            if (move == stop or new_pos in dangerous_enemy_pos):
                continue
            # killing someone is always the best move
            elif new_pos in killable_enemy_pos:
                self.say("MUHAHAHAHAHA!!!")
                return move
            # compute the goodness of the new position
            else:
                ## compute the score of the move 
                # improvements should be a 1 field difference -- do negative values make sense?
                # improvement in terms of getting closer to food
                food_improve = curr_min_dist_food-self.compute_min_dist(new_pos, self.enemy_food)
                score = self.w_eat*max(0, food_improve)
                # improvement in terms of getting closer to killable enemies
                kill_improve = curr_min_dist_kill-self.compute_min_dist(new_pos, killable_enemy_pos)
                score += self.w_defend*max(0, kill_improve)
                # make sure to get away from immediate danger
                danger_dist = self.compute_min_dist(new_pos, dangerous_enemy_pos)
                if danger_dist < self.save_dist:
                    # the closer, the more dangerous
                    score += self.w_danger*(1 - danger_dist/self.save_dist) 
                # to avoid redundant behavior, stay away from teammates
                team_dist = self.compute_min_dist(new_pos, teammate_pos)
                if team_dist < self.save_dist:
                    # the closer, the more dangerous
                    score += self.w_mate*(1 - team_dist/self.save_dist)              
                # is this our preferred direction?
                if move == self.priority_dir:
                    score += self.w_pdir
                scored_moves[move] = score
        if scored_moves:
            best_move = max(scored_moves.keys(), key=scored_moves.get)
            # is this move especially cool?
            if self.legal_moves[best_move] in self.enemy_food:
                self.say("OmNomNom")
            return best_move
        else:
            # we ran out of smart moves
            self.say(">.<")
            return stop

