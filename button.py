from graphics import *
import time
from threading import Thread

class Buttons:
    def __init__(self,win):
        self.buttons = []
        self.win

    def add_button(self,x1,y1,x2,y2,text):
        btn = Button(x1,y1,x2,y2,text,self.win)
        self.buttons.append(btn)

class Button:
    def __init__(self,x1,y1,x2,y2,text,win):
        self.win = win
        self.btn = Rectangle(Point(x1, y1), Point(x2,y2))
        self.btn.draw(self.win)
        self.txt = Text(Point(self.btn.getCenter().getX(), self.btn.getCenter().getY()), text)
        self.txt.draw(self.win)

    def is_clicked(self,x,y):
        if(x != None and y != None and x >= self.btn.getP1().getX() and x <= self.btn.getP2().getX() and y >= self.btn.getP1().getY() and y <= self.btn.getP2().getY()):
            return True
        return False

class Move_Entry:
    def __init__(self,x1,y1,x2,y2,text,win):
        self.win = win
        self.text = text
        self.index = 0
        self.outer_box = Rectangle(Point(x1, y1), Point(x2, y2))
        self.entry = Text(Point(self.outer_box.getCenter().getX(),y1+(y2-y1)/6),self.text[self.index])
        self.btn_increase = Button(x1 + 5, y1 + (y2-y1) / 3 + 10, x2 - 5, y1 + 2 * (y2-y1) / 3 - 10, "+", self.win)
        self.btn_decrease = Button(x1 + 5, y1 + 2 * (y2-y1) / 3 + 10, x2 - 5, y2-10, "-", self.win)
        self.outer_box.draw(self.win)
        self.entry.draw(self.win)

    def increase(self):
        if(self.index < len(self.text)-1):
            self.index += 1
            self.entry.setText(self.text[self.index])

    def decrease(self):
        if(self.index > 0):
            self.index -= 1
            self.entry.setText(self.text[self.index])

    def is_clicked(self,x,y):
        if(self.is_increase(x,y) or self.is_decrease(x,y)):
            return  True
        return False

    def is_increase(self,x,y):
        return self.btn_increase.is_clicked(x,y)

    def is_decrease(self,x,y):
        return self.btn_decrease.is_clicked(x,y)

    def get_text(self):
        return self.entry.getText()

    def reset(self):
        self.index = 0
        self.entry.setText(self.text[self.index])
