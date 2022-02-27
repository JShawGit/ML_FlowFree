import pygame
""" Q Learn ----------------------------
    This file contains the RL algorithm.
"""



""" Q Learning ----------------------------
        Will learn how to connect the dots.
"""
class Q_Learn_Agent():
    def __init__(self, game, alpha, epsilon, gamma):
        self.game    = game
        self.alpha   = alpha
        self.epsilon = epsilon
        self.gamma   = gamma
""" ----------------------------------- """







