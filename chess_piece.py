from graphics import *

SIZE_OF_BOX = 103

class Chess_Piece:
	def __init__(self,x,y,path):
		self.path = path
		self.img = Image(Point(x,y),path)
		self.lowerX = self.img.anchor.x-(SIZE_OF_BOX/2)
		self.lowerY = self.img.anchor.y-(SIZE_OF_BOX/2)
		self.upperX = self.lowerX + SIZE_OF_BOX
		self.upperY = self.lowerY + SIZE_OF_BOX