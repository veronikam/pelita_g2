# -*- coding: utf-8 -*-

# (Specifying utf-8 is always a good idea in Python 2.)

from pelita.player import AbstractPlayer
from pelita.datamodel import north, south, west, east, stop
from pelita.graph import AdjacencyList, manhattan_dist

# use relative imports for things inside your module
from .utils import utility_function


class FranziPlayer(AbstractPlayer):
    """ Basically a really awesome player. """

    def __init__(self, priority_dir='up', w_danger=-10, w_eat=3, w_pdir=1, w_defend=10):
        """
        Attributes:
            - priority_dir: which direction to favor ('up' or 'down')
            - w_danger: how important it is to avoid enemy destroyers
            - w_eat: how important it is to eat the enemy's food
            - w_pdir: how important it is to go into the favored direction
            - w_defend: how important it is to kill enemy harvesters
        """
        if priority_dir == 'up':
            self.priority_dir = north
        elif priority_dir == 'down':
            self.priority_dir = south
        else:
            raise RuntimeWarning("Invalid priority_dir, use either up or down!")
            self.priority_dir = None
        self.save_dist = 5
        self.w_danger = w_danger
        self.w_eat = w_eat
        self.w_pdir = w_pdir
        self.w_defend = w_defend
        self.adjacency = None # to store an adjacency list with all possible positions 

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

    def compute_pos_min_dists(self, pos, dangerous_enemy_pos, killable_enemy_pos, food_pos):
        """
        Inputs:
            - pos: for which position the distances should be computed
            - dangerous_enemy_pos: a list of positions for dangerous enemies (if any)
            - killable_enemy_pos: a list of positions for killable enemies (if any)
            - food_pos: a list of positions for eatable food (if any)
        Returns:
            - min_dists: a list with 3 distances: maze distance to the closest
                -- dangerous enemy
                -- killable enemy
                -- eatable piece of food
              the distance is 0 if there is no position given for one of the things
              (or the distance is actually 0, i.e. the bot is on this spot)
        """
        if dangerous_enemy_pos:
            min_dist_to_dangerous_enemy = min([len(self.shortest_path(pos, i_pos)) 
                                               for i_pos in dangerous_enemy_pos])
        else:
            min_dist_to_dangerous_enemy = 0
        if killable_enemy_pos:
            min_dist_to_killable_enemy = min([len(self.shortest_path(pos, i_pos)) 
                                               for i_pos in killable_enemy_pos])
        else:
            min_dist_to_killable_enemy = 0
        if food_pos:
            min_dist_to_food = min([len(self.shortest_path(pos, i_pos)) 
                                               for i_pos in food_pos])
        else:
            min_dist_to_food = 0
        return [min_dist_to_dangerous_enemy, min_dist_to_killable_enemy, min_dist_to_food]

    def compute_pos_min_dists_simple(self, pos, dangerous_enemy_pos, killable_enemy_pos, food_pos):
        """
        Inputs:
            - pos: for which position the distances should be computed
            - dangerous_enemy_pos: a list of positions for dangerous enemies (if any)
            - killable_enemy_pos: a list of positions for killable enemies (if any)
            - food_pos: a list of positions for eatable food (if any)
        Returns:
            - min_dists: a list with 3 distances: manhattan distance to the closest
                -- dangerous enemy
                -- killable enemy
                -- eatable piece of food
              the distance is 0 if there is no position given for one of the things
              (or the distance is actually 0, i.e. the bot is on this spot)
        """
        if dangerous_enemy_pos:
            min_dist_to_dangerous_enemy = min([len(self.shortest_path(self.current_pos, pos)) 
                                               for pos in dangerous_enemy_pos])
        else:
            min_dist_to_dangerous_enemy = 0
        if killable_enemy_pos:
            min_dist_to_killable_enemy = min([len(self.shortest_path(self.current_pos, pos)) 
                                               for pos in killable_enemy_pos])
        else:
            min_dist_to_killable_enemy = 0
        if food_pos:
            min_dist_to_food = min([len(self.shortest_path(self.current_pos, pos)) 
                                               for pos in food_pos])
        else:
            min_dist_to_food = 0
        return [min_dist_to_dangerous_enemy, min_dist_to_killable_enemy, min_dist_to_food]

    def get_move(self):
        # get to know something about our surroundings
        dangerous_enemy_pos = [bot.current_pos
            for bot in self.enemy_bots if bot.is_destroyer]
        killable_enemy_pos = [bot.current_pos
            for bot in self.enemy_bots if bot.is_harvester]
        # compute how good our current position is
        curr_min_dists = self.compute_pos_min_dists(self.current_pos, 
                              dangerous_enemy_pos, killable_enemy_pos, self.enemy_food)
        #print curr_min_dists
        rated_moves = {}
        for move, new_pos in list(self.legal_moves.items()):
            # filter out obviously stupid moves
            if (move == stop or
                new_pos in dangerous_enemy_pos):
                continue
            # compute the goodness of the new position
            else:
                # new distances
                new_min_dists = self.compute_pos_min_dists(new_pos, dangerous_enemy_pos,
                                      killable_enemy_pos, self.enemy_food)
                #print "Move: %r - %r"%(move, new_min_dists)
                ## compute the score of the move
                # improvement in terms of getting closer to food
                score = self.w_eat*(curr_min_dists[2]-new_min_dists[2])
                # improvement in terms of getting further away from danger
                # only relevant if we're actually close
                if new_min_dists[0] < self.save_dist:
                    score += self.w_danger*(curr_min_dists[0]-new_min_dists[0])
                # improvement in terms of getting closer to killable enemies
                score += self.w_defend*(curr_min_dists[1]-new_min_dists[1])
                # is this our preferred direction?
                if move == self.priority_dir:
                    score += self.w_pdir
                rated_moves[move] = score
        if rated_moves:
            best_move = max(rated_moves.keys(), key=rated_moves.get)
            # is this move especially cool?
            if self.legal_moves[best_move] in self.enemy_food:
                self.say("OmNomNom")
            elif self.legal_moves[best_move] in killable_enemy_pos:
                self.say("MUHAHAHAHAHA!!!")
            return best_move
        else:
            # we ran out of smart moves
            self.say(">.<")
            return stop

