# -*- coding: utf-8 -*-

# (Specifying utf-8 is always a good idea in Python 2.)

from pelita.player import AbstractPlayer
from pelita.datamodel import stop
from pelita.graph import AdjacencyList, NoPathException, diff_pos

# use relative imports for things inside your module
from .utils import utility_function

class DrunkPlayer(AbstractPlayer):
    """ Basically a clone of the RandomPlayer. """

    def __init__(self):
        # Do some basic initialisation here. You may also accept additional
        # parameters which you can specify in your factory.
        # Note that any other game variables have not been set yet. So there is
        # no ``self.current_uni`` or ``self.current_state``
        self.sleep_rounds = 0

    def set_initial(self):
        # Now ``self.current_uni`` and ``self.current_state`` are known.
        # ``set_initial`` is always called before ``get_move``, so we can do some
        # additional initialisation here

        # Just printing the universe to give you an idea, please remove all
        # print statements in the final player.
        print self.current_uni.pretty

    def check_pause(self):
        # make a pause every fourth step because whatever :)
        if self.sleep_rounds <= 0:
            if self.rnd.random() > 0.75:
                self.sleep_rounds = 3

        if self.sleep_rounds > 0:
            self.sleep_rounds -= 1
            self.say("I am confused. Very confused.")
            return stop

    def get_move(self):
        utility_function()
        for i in range(10):
            print self.enemy_bots[0].current_pos
        print " "
        self.check_pause()

        # legal_moves returns a dict {move: position}
        # we always need to return a move
        possible_moves = self.legal_moves.keys()
        # selecting one of the moves
        return self.rnd.choice(possible_moves)

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
            self.next_food = self.rnd.choice(self.enemy_food)

        try:
            next_pos = self.goto_pos(self.next_food)
            move = diff_pos(self.current_pos, next_pos)
            return move
        except NoPathException:
            return datamodel.stop
