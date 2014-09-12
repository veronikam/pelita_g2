#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pelita.player import SimpleTeam
from .demo_player import DrunkPlayer
from FoodEatingPlayer import FoodEatingPlayer 
from JakovPlayer import JakovPlayer
from .franzi_player import FranziPlayer

# (please use relative imports inside your module)
# The default factory method, which this module must export.
# It must return an instance of `SimpleTeam`  containing
# the name of the team and the respective instances for
# the first and second player.

def jakov_factory():
    return SimpleTeam("group2 Team", JakovPlayer(), DrunkPlayer())

def franzi_factory():
    return SimpleTeam("Franzi Team", FranziPlayer('up'), FranziPlayer('down'))
# For testing purposes, one may use alternate factory methods::
#
#     def alternate_factory():
#          return SimpleTeam("Our alternate Team", AlternatePlayer(), AlternatePlayer())
#
# To be used as follows::
#
#     $ ./pelitagame path_to/groupN/:alternate_factory

