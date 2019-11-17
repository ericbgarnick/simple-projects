from unittest import TestCase

from minesweeper.board import Board, GameDifficulty


class TestBoard(TestCase):
    def test_create_board(self):
        board_size = 5

        b = Board(board_size, GameDifficulty.EASY)

        self.assertEqual(b.board_size, board_size)

    def test_create_bombs(self):
        difficulty = GameDifficulty.EASY
        board_size = 5
        num_spaces = board_size ** 2
        expected_num_bombs = int(Board.PCT_BOMBS[difficulty]
                                 / 100 * num_spaces)

        b = Board(board_size, difficulty)

        self.assertEqual(expected_num_bombs, len(b.bomb_locations))
