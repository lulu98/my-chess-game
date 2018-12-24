import copy
from chess_piece import *


class HistoryTable:
    def __init__(self,chess_field):
        self.turn = "white"
        self.original_field = []
        for row in range(0,len(chess_field)):
            one_row = []
            for col in range(0,len(chess_field)):
                one_row.append(Chess_Piece(chess_field[row][col].img.getAnchor().getX(),chess_field[row][col].img.getAnchor().getY(),chess_field[row][col].path))
            self.original_field.append(one_row)
        self.history_table = []

    def add_step(self,chess_field):
        new_chess_field = []
        for row in range(0,len(chess_field)):
            one_row = []
            for col in range(0,len(chess_field)):
                one_row.append(Chess_Piece(chess_field[row][col].img.getAnchor().getX(),chess_field[row][col].img.getAnchor().getY(), chess_field[row][col].path))
            new_chess_field.append(one_row)
        self.history_table.append(new_chess_field)
        print(len(self.history_table))
        if (self.turn == "white"):
            self.turn = "black"
        else:
            self.turn = "white"

    def go_back(self):
        chess_field = self.original_field
        player = "white"
        if(len(self.history_table) > 0):
            #self.history_table.pop()
            chess_field = self.history_table.pop()
            if (self.turn == "white"):
                player = "black"
            else:
                player = "white"
        self.turn = player
        return chess_field