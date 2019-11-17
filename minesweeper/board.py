import random
import sys
from enum import Enum
from typing import Set, List, Union


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

    def _create_bombs(self, pct_bombs: int) -> Set[int]:
        """
        Fill squares in self._board with as many bombs
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

    @property
    def board_size(self) -> int:
        return self._board_size

    @property
    def bomb_locations(self) -> Set[int]:
        return self._bomb_locs


if __name__ == '__main__':
    bsize = int(sys.argv[1])
    b = Board(bsize, GameDifficulty.EASY)
    print(b)
