import unittest
from unittest.mock import patch
import pygame
import cv2

from main import App

class TestApp(unittest.TestCase):
    def setUp(self):
        self.instance = App()

    def test_init(self):
        self.assertIsNotNone(self.instance.arena)
        self.assertIsNotNone(self.instance.ball1)
        self.assertIsNotNone(self.instance.left_paddle)
        self.assertIsNotNone(self.instance.right_paddle)
        self.assertIsNotNone(self.instance.scorer)
        self.assertEqual(len(self.instance.components), 5)

        self.assertIsInstance(self.instance.cap, cv2.VideoCapture)

        self.assertIsNotNone(self.instance.graphic)
        self.assertIsNotNone(self.instance.menu_animation)

        self.assertIsNotNone(self.instance.hand_tracker)
        self.assertIsNotNone(self.instance.face_tracker)

        self.assertIsNotNone(self.instance.menu)
        self.assertIsNotNone(self.instance.one_player)
        self.assertIsNotNone(self.instance.two_player)
        self.assertIsNotNone(self.instance.state_manager)
        self.assertIsInstance(self.instance.clock, pygame.time.Clock)
        self.assertTrue(self.instance.is_running)

    @patch.object(App, 'exit_game')
    def test_app_closes_when_exit_is_selected(self, mock_exit_game):
        self.instance.is_running = False
        self.instance.run()  # assuming you have a run method that runs the game loop
        mock_exit_game.assert_called_once()


if __name__ == '__main__':
    unittest.main()