from cachesimulator.MSI import *
from cachesimulator.config import LINE_SIZE
from cachesimulator.statistics import Statistic

class Line():
    def __init__(self):
        # initalise cache to be invalid
        self.state = INVALID
        self.tag = -1 
        self.dirty = False
        self.valid = False

    def read(self, tag):
        self.tag = tag
        self.state = SHARED
        self.valid = True
        self.dirty = False
        Statistic.cache_access()

    def write(self, tag):
        self.tag = tag
        self.dirty = True
        self.valid = True
        self.state = MODIFIED
        Statistic.cache_access()

    def invalidate(self):
        self.state = INVALID

    def set_state(self, state):
        self.state = state
        Statistic.cache_probe()
        
    # -- Setters and Getters --
    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, val):
        self._state = val

    @property
    def tag(self):
        return self._tag

    @tag.setter
    def tag(self, val):
        self._tag = val

    @property
    def dirty():
        return self._dirty

    @dirty.setter
    def dirty(self, val):
        self._dirty = val

    @property
    def valid(self):
        return self._valid

    @valid.setter
    def valid(self, val):
        self._valid = val
