import random
import sys
from enum import Enum
from queue import Queue
from typing import Set, List


class GameDifficulty(Enum):
    EASY = "EASY"
    MEDIUM = "MEDIUM"
    HARD = "HARD"


class Minesweeper:

    HIDDEN = '#'
    BLANK = '_'
    BOMB = '*'

    PCT_BOMBS = {GameDifficulty.EASY: 10,
                 GameDifficulty.MEDIUM: 20,
                 GameDifficulty.HARD: 30}

    def __init__(self, size: int, difficulty: GameDifficulty):
        self._board_size = size
        self._bomb_locs = self._create_bombs(self.PCT_BOMBS[difficulty])
        self._revealed = {}  # revealed index -> value to show

    def _create_bombs(self, pct_bombs: int) -> Set[int]:
        """
        Return a set of indices fpr as many bombs
        as indicated by pct_bombs (% total spaces).
        """
        num_spaces = self._board_size ** 2
        num_bombs = int((pct_bombs / 100) * num_spaces)
        bomb_idxs = set()
        free_spaces = list(range(num_spaces))
        while len(bomb_idxs) < num_bombs:
            bomb_space = random.choice(free_spaces)
            bomb_idxs.add(bomb_space)
            free_spaces.remove(bomb_space)
        return bomb_idxs

    def build_board_repr(self) -> List[List[str]]:
        board_repr = []
        for i in range(self._board_size ** 2):
            symbol = self._revealed.get(i, self.HIDDEN)
            if not i % self._board_size:
                board_repr.append([symbol])
            else:
                board_repr[-1].append(symbol)
        return board_repr

    def reveal_for_chosen(self, chosen: int):
        """Add chosen symbol to self._revealed, adding
        all blanks encountered and their neighbors"""
        to_check = Queue()
        to_check.put(chosen)
        while not to_check.empty():
            cur = to_check.get()
            cur_symbol = self.calc_symbol(cur)
            self._revealed[cur] = cur_symbol
            if cur_symbol == self.BLANK:
                for n in self.get_neighbors(cur):
                    if n not in self._revealed:
                        to_check.put(n)

    def calc_symbol(self, i: int) -> str:
        """Return the symbol to show for the space at index i"""
        if i in self._bomb_locs:
            return self.BOMB
        else:
            neighbors = self.get_neighbors(i)
            num_bomb_neighbors = len(neighbors & self._bomb_locs)
            return (str(num_bomb_neighbors)
                    if num_bomb_neighbors
                    else self.BLANK)

    def get_neighbors(self, i: int) -> Set[int]:
        """Return indices for all spaces adjacent to i"""
        neighbors = set()
        north = south = east = west = -1

        if i >= self._board_size:
            north = i - self._board_size
            neighbors.add(north)
        if i < self._board_size * (self._board_size - 1):
            south = i + self._board_size
            neighbors.add(south)
        if i % self._board_size:
            west = i - 1
            neighbors.add(west)
        if i % self._board_size != self._board_size - 1:
            east = i + 1
            neighbors.add(east)

        if north != -1:
            if east != -1:
                neighbors.add(north + 1)
            if west != -1:
                neighbors.add(north - 1)
        if south != -1:
            if east != -1:
                neighbors.add(south + 1)
            if west != -1:
                neighbors.add(south - 1)

        return neighbors

    @property
    def board_size(self) -> int:
        return self._board_size

    @property
    def bomb_locations(self) -> Set[int]:
        return self._bomb_locs

    def __str__(self):
        board_repr = self.build_board_repr()
        return '\n'.join([' '.join(row) for row in board_repr])


if __name__ == '__main__':
    board_size, diff = sys.argv[1:3]
    m = Minesweeper(int(board_size), GameDifficulty[diff.upper()])
    print(b)
