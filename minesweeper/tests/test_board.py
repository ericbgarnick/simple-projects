from typing import Dict, Set
from unittest import TestCase

from minesweeper.board import Board, GameDifficulty


class TestBoard(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.board_size = 5
        cls.num_spaces = cls.board_size ** 2
        cls.difficulty = GameDifficulty.EASY
        cls.b = Board(cls.board_size, cls.difficulty)

    def test_create_board(self):
        self.assertEqual(self.b.board_size, self.board_size)

    def test_create_bombs(self):
        expected_num_bombs = int(Board.PCT_BOMBS[self.difficulty]
                                 / 100 * self.num_spaces)

        b = Board(self.board_size, self.difficulty)

        self.assertEqual(expected_num_bombs, len(b.bomb_locations))

    def get_neighbors_check(self, spots_to_check: Dict[int, Set[int]]):
        for spot, n in spots_to_check.items():
            neighbors = self.b.get_neighbors(spot)
            self.assertSetEqual(n, neighbors)

    def test_get_neighbors_corners(self):
        corners = {
            0: {1, 5, 6},
            4: {3, 8, 9},
            24: {19, 18, 23},
            20: {15, 16, 21}
        }

        self.get_neighbors_check(corners)

    def test_get_neighbors_edges(self):
        edges = {
            1: {0, 2, 5, 6, 7},
            9: {3, 4, 8, 13, 14},
            23: {22, 24, 17, 18, 19},
            15: {10, 20, 11, 16, 21}
        }

        self.get_neighbors_check(edges)

    def test_get_neighbors_middle(self):
        middle = {12: {6, 7, 8, 11, 13, 16, 17, 18}}

        self.get_neighbors_check(middle)
