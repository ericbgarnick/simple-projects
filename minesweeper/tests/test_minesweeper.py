from typing import Dict, Set
from unittest import TestCase

from minesweeper.minesweeper import Minesweeper, GameDifficulty


class TestMinesweeper(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.board_size = 5
        cls.num_spaces = cls.board_size ** 2
        cls.difficulty = GameDifficulty.EASY
        cls.m = Minesweeper(cls.board_size, cls.difficulty)

    def tearDown(self) -> None:
        self.m._bomb_locs = set()
        self.m._revealed = {}

    def test_create_board(self):
        self.assertEqual(self.m.board_size, self.board_size)

    def test_create_bombs(self):
        expected_num_bombs = int(Minesweeper.PCT_BOMBS[self.difficulty]
                                 / 100 * self.num_spaces)

        b = Minesweeper(self.board_size, self.difficulty)

        self.assertEqual(expected_num_bombs, len(b.bomb_locations))

    def get_neighbors_check(self, spots_to_check: Dict[int, Set[int]]):
        for spot, n in spots_to_check.items():
            neighbors = self.m.get_neighbors(spot)
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

    def test_build_board_repr_no_revealed(self):
        expected = [
            ['#' for _ in range(self.board_size)]
            for _ in range(self.board_size)
        ]
        actual = self.m.build_board_repr()

        self.assertEqual(len(expected), len(actual))
        for i, e_row in enumerate(expected):
            a_row = actual[i]
            self.assertListEqual(e_row, a_row)

    def test_build_board_repr_one_revealed(self):
        expected = [
            ['#' for _ in range(self.board_size)]
            for _ in range(self.board_size)
        ]

        self.m._revealed[0] = "_"
        expected[0][0] = '_'

        actual = self.m.build_board_repr()

        self.assertEqual(len(expected), len(actual))
        for i, e_row in enumerate(expected):
            a_row = actual[i]
            self.assertListEqual(e_row, a_row)

    def test_calc_symbol_bomb(self):
        pos = 0
        self.m._bomb_locs.add(pos)
        symbol = self.m.calc_symbol(pos)
        self.assertEqual(symbol, self.m.BOMB)

    def test_calc_symbol_blank(self):
        pos = 0
        symbol = self.m.calc_symbol(pos)
        self.assertEqual(symbol, self.m.BLANK)

    def test_calc_symbol_1(self):
        pos = 0
        self.m._bomb_locs.add(pos)
        symbol = self.m.calc_symbol(pos + 1)
        self.assertEqual(symbol, '1')

    def test_calc_symbol_8(self):
        self.m._bomb_locs |= {0, 1, 2, 5, 7, 10, 11, 12}
        symbol = self.m.calc_symbol(6)
        self.assertEqual(symbol, '8')

    def test_reveal_for_chosen_bomb(self):
        """
        * _ _ _ _
        _ _ _ _ _
        _ _ _ _ _
        _ _ _ _ _
        _ _ _ _ _
        """
        pos = 0
        self.m._bomb_locs.add(pos)
        self.m.reveal_for_chosen(pos)
        self.assertDictEqual(self.m._revealed, {pos: self.m.BOMB})

    def test_reveal_for_chosen_num(self):
        """
        * 1 _ _ _
        _ _ _ _ _
        _ _ _ _ _
        _ _ _ _ _
        _ _ _ _ _
        """
        self.m._bomb_locs.add(0)
        self.m.reveal_for_chosen(1)
        self.assertDictEqual(self.m._revealed, {1: '1'})

    def test_reveal_for_chosen_one_blank(self):
        """
        _ 2 * _ _
        2 5 * _ _
        * * * _ _
        _ _ _ _ _
        _ _ _ _ _
        """
        self.m._bomb_locs |= {2, 7, 10, 11, 12}
        self.m.reveal_for_chosen(0)

        expected = {0: self.m.BLANK, 1: '2', 5: '2', 6: '5'}

        self.assertDictEqual(self.m._revealed, expected)

    def test_reveal_for_chosen_two_blanks(self):
        """
        _ _ 2 * _
        2 3 5 * _
        * * _ * _
        _ _ _ _ _
        _ _ _ _ _
        """
        self.m._bomb_locs |= {3, 8, 10, 11, 12, 13}
        self.m.reveal_for_chosen(0)

        expected = {0: self.m.BLANK, 1: self.m.BLANK,
                    2: '2', 5: '2', 6: '3', 7: '5'}

        self.assertDictEqual(self.m._revealed, expected)
