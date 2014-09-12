# -*- coding: utf-8 -*-

from pelita import datamodel
from pelita.player import AbstractPlayer, SimpleTeam
from pelita.graph import AdjacencyList, NoPathException, diff_pos, manhattan_dist
from pelita.datamodel import CTFUniverse
from pelita.datamodel import stop



class JakovPlayer(AbstractPlayer):
    def set_initial(self):
        self.adjacency = AdjacencyList(self.current_uni.reachable([self.initial_pos]))
        self.next_food = None

    def goto_pos(self, pos):
        return self.adjacency.a_star(self.current_pos, pos)[-1]

    def get_move(self):
        
                
        # check, if food is still present
        if (self.next_food is None
                or self.next_food not in self.enemy_food):
            if not self.enemy_food:
                # all food has been eaten? ok. i’ll stop
                return datamodel.stop
            self.next_food = self.rnd.choice(self.enemy_food) # !!! to improve: not random from all enemy_food by from closest food

        # determine enemy positions dangerous & killable 
        dangerous_enemy_pos = [bot.current_pos
            for bot in self.enemy_bots if bot.is_destroyer]
                
        non_noisy_dangerous_enemy_pos = [bot.current_pos
            for bot in self.enemy_bots if (bot.is_destroyer and not bot.noisy)]
#        
        killable_enemy_pos = [bot.current_pos
            for bot in self.enemy_bots if bot.is_harvester]

        try:
            next_pos = self.goto_pos(self.next_food)
#            next_pos = self.rnd.choice([(0,1),(0,-1),(1,0),(-1,0)])
            move = diff_pos(self.current_pos, next_pos)
            
            my_adjecent_pos = self.adjacency.pos_within(self.current_pos,5)
            legal_moves = self.legal_moves
            # check if the next position is dangerous

            # list of dangerous enemy adecent positions                
#                dangerous_enemy_adj_pos = []        
            acceptable_adjecent_pos = list(my_adjecent_pos)        
#            for position in dangerous_enemy_pos:
            for position in non_noisy_dangerous_enemy_pos:
                dangerous_enemy_adj_pos = self.adjacency.pos_within(position,3)
                for enemy_adj_pos in dangerous_enemy_adj_pos:
                    if enemy_adj_pos in acceptable_adjecent_pos:                    
                        acceptable_adjecent_pos.remove(enemy_adj_pos)
                        
            # TODO: improve to -> escape to the direction oposite from the enemy
            if len(acceptable_adjecent_pos) == 0:
                return self.rnd.choice(list(legal_moves.keys()))
                
            if next_pos not in my_adjecent_pos:
                next_pos = self.rnd.choice(list(my_adjecent_pos))
                move = diff_pos(self.current_pos, next_pos)

            # Remove stop
#            try:
#                del legal_moves[datamodel.stop]
#            except KeyError:
#                pass
#            # now remove the move that would lead to the enemy
#            # unless there is no where else to go.
#            if len(legal_moves) > 1:
#                for (k,v) in legal_moves.items():
#                    if v in dangerous_enemy_pos:
#                        break
#                del legal_moves[k]
#            # just in case, there is really no way to go to:
#            if not legal_moves:
#                return datamodel.stop
#            # and select a move at random
#            return self.rnd.choice(list(legal_moves.keys()))
            
            
            # selecting one of the moves
#                while next_pos in dangerous_enemy_pos:
#                    move = self.rnd.choice(possible_moves)
#                    next_pos = (self.current_pos[0] + move[0],self.current_pos[1] + move[1])
            
                
            self.say("bla bla!")
            return move
        except NoPathException:
            return datamodel.stop
            
            
            
#    def get_move(self):
#        dangerous_enemy_pos = [bot.current_pos
#            for bot in self.enemy_bots if bot.is_destroyer]
#        killable_enemy_pos = [bot.current_pos
#            for bot in self.enemy_bots if bot.is_harvester]
#
#        smart_moves = []
#        for move, new_pos in list(self.legal_moves.items()):
#            if (move == stop or
#                new_pos in dangerous_enemy_pos):
#                continue # bad idea
#            elif (new_pos in killable_enemy_pos or
#                  new_pos in self.enemy_food):
#                return move # get it!
#            else:
#                smart_moves.append(move)
#
#        if smart_moves:
#            return self.rnd.choice(smart_moves)
#        else:
#            # we ran out of smart moves
#            return stop

def factory():
    return SimpleTeam("The Food Eating Players", FoodEatingPlayer(), FoodEatingPlayer())

