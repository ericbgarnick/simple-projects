import random
import sys
from enum import Enum
from typing import Set, List


class GameDifficulty(Enum):
    EASY = "EASY"
    MEDIUM = "MEDIUM"
    HARD = "HARD"


class Board:

    PCT_BOMBS = {GameDifficulty.EASY: 10,
                 GameDifficulty.MEDIUM: 20,
                 GameDifficulty.HARD: 30}

    def __init__(self, size: int, difficulty: GameDifficulty):
        self._board_size = size
        self._bomb_locs = self._create_bombs(self.PCT_BOMBS[difficulty])
        self._guesses = {}  # guessed index -> value to show

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

    def _build_board_repr(self) -> List[List[str]]:
        board_repr = []
        for i in range(self._board_size ** 2):
            if i in self._bomb_locs:
                symbol = "*"
            else:
                symbol = self._guesses.get(i) or self._calc_symbol(i)
            if not i % self._board_size:
                board_repr.append([symbol])
            else:
                board_repr[-1].append(symbol)
        return board_repr

    def _calc_symbol(self, i: int) -> str:
        neighbors = self._get_neighbors(i)
        num_bomb_neighbors = len(neighbors & self._bomb_locs)
        return str(num_bomb_neighbors) if num_bomb_neighbors else '_'

    def _get_neighbors(self, i: int) -> Set[int]:
        neighbors = set()
        north = south = east = west = -1

        if i >= self._board_size:
            north = i - self._board_size
        if i < self._board_size * (self._board_size - 1):
            south = i + self._board_size
        if i % self._board_size:
            west = i - 1
        if i % self._board_size != self._board_size - 1:
            east = i + 1

        if north != -1:
            neighbors.add(north)
            if east != -1:
                neighbors.add(north + 1)
            if west != -1:
                neighbors.add(north - 1)
        if south != -1:
            neighbors.add(south)
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
        board_repr = self._build_board_repr()
        return '\n'.join([' '.join(row) for row in board_repr])


if __name__ == '__main__':
    board_size, difficulty = sys.argv[1:3]
    b = Board(int(board_size), GameDifficulty[difficulty.upper()])
    print(b)
