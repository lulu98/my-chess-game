from mygraphics import *
import math
'''TODO: 
- history table
- button to play back move
- implement chess algorithm / ai opponent
- starting menu to choose if opponent is ai or human player
- choose which colour you want to play
- en peasant
- if pawn reaches end of field, you should choose which chess_piece you want to continue
- option for rochade
'''

SIZE_OF_BOX = 103

class Chess_Piece:
	def __init__(self,x,y,path):
		self.path = path
		self.img = Image(Point(x,y),path)
		self.lowerX = self.img.anchor.x-(SIZE_OF_BOX/2)
		self.lowerY = self.img.anchor.y-(SIZE_OF_BOX/2)
		self.upperX = self.lowerX + SIZE_OF_BOX
		self.upperY = self.lowerY + SIZE_OF_BOX


class Chess_Game:
	def __init__(self):
		self.initialize_game_field()
		backgroundImage = Image(Point(412,412),"plain_chess_field.gif")
		self.win = GraphWin("My Chess Game",backgroundImage.getHeight(),backgroundImage.getWidth())
		self.win.setBackground('black')
		backgroundImage.draw(self.win)
		self.print_chess_field()
		turn = "white"

		game_over = False
		while (not(game_over)):
			print(turn + "'s turn.")
			location = self.win.getMouse()
			for row in range(0,len(self.chess_field)):
				for col in range(0,len(self.chess_field)):
					if(self.chess_field[row][col].path != "" and location.getX() >= self.chess_field[row][col].lowerX and location.getX() <= self.chess_field[row][col].upperX and location.getY() >= self.chess_field[row][col].lowerY and location.getY() <= self.chess_field[row][col].upperY):
						print("1: ",self.chess_field[row][col].path)
						location2 = self.win.getMouse()
						if(location2.getX() != location.getX() or location2.getY() != location.getY()):
							for row2 in range(0,len(self.chess_field)):
								for col2 in range(0,len(self.chess_field)):
									if(location2.getX() >= self.chess_field[row2][col2].lowerX and location2.getX() <= self.chess_field[row2][col2].upperX and location2.getY() >= self.chess_field[row2][col2].lowerY and location2.getY() <= self.chess_field[row2][col2].upperY):
										print("2: ",self.chess_field[row2][col2].path)
										if(turn in self.chess_field[row][col].path and self.legal_move(row,col,row2,col2)):
											if("king" in self.chess_field[row2][col2].path):
												game_over = True
											else:
												self.chess_field[row2][col2].img.undraw()
												self.chess_field[row2][col2] = Chess_Piece(self.chess_field[row2][col2].img.anchor.x,self.chess_field[row2][col2].img.anchor.y,self.chess_field[row][col].path)
												self.chess_field[row2][col2].img.draw(self.win)
												self.chess_field[row][col].img.undraw()
												self.chess_field[row][col] = Chess_Piece(self.chess_field[row][col].img.anchor.x,self.chess_field[row][col].img.anchor.y,"")
												self.chess_field[row][col].img.draw(self.win)
											if(turn == "white"):
												turn = "black"
											else:
												turn = "white"								
											
			time.sleep(0.1)
		print("Game over!")
		if(turn == "white"):
			print("Black player is the winner!")
		else:
			print("White player is the winner!")
		time.sleep(1)
		win.close()

	def legal_move(self,row,col,row2,col2):
		is_legal_move = True
		if("pawn" in self.chess_field[row][col].path):
			if("white" in self.chess_field[row][col].path):
			#legal move for white pawn
				if(not((row == row2+1 and col == col2 and self.chess_field[row2][col2].path == "") or (row == row2+1 and (col == col2+1 or col == col2-1) and self.chess_field[row2][col2].path != ""))):
					is_legal_move = False
				if(row == 6 and row == row2+2 and col == col2 and self.chess_field[row2][col2].path == "" and self.chess_field[row-1][col].path == ""):
					is_legal_move = True
			elif("black" in self.chess_field[row][col].path):
				if(not((row == row2-1 and col == col2 and self.chess_field[row2][col2].path == "") or (row == row2-1 and (col == col2+1 or col == col2-1) and self.chess_field[row2][col2].path != ""))):
					is_legal_move = False
				if(row == 1 and row == row2-2 and col == col2 and self.chess_field[row2][col2].path == "" and self.chess_field[row+1][col].path == ""):
					is_legal_move = True
		elif("knight" in self.chess_field[row][col].path):
			if(not((col2 == col-2 and row2 == row+1) or (col2 == col-1 and row2 == row+2) or (col2 == col+1 and row2 == row+2) or (col2 == col+2 and row2 == row+1)
				or (col2 == col+2 and row2 == row-1) or (col2 == col+1 and row2 == row-2) or (col2 == col-1 and row2 == row-2) or (col2 == col-2 and row2 == row-1))):
				is_legal_move = False
		elif("rook" in self.chess_field[row][col].path):
			if(not(self.legal_rook_move(row,col,row2,col2))):
				is_legal_move = False
		elif("bishop" in self.chess_field[row][col].path):
			if(not(self.legal_bishop_move(row,col,row2,col2))):
				is_legal_move = False
		elif("queen" in self.chess_field[row][col].path):
			if(not(self.legal_rook_move(row,col,row2,col2) or self.legal_bishop_move(row,col,row2,col2))):
				is_legal_move = False
		elif("king" in self.chess_field[row][col].path):
			if(not((math.fabs(row2-row) == 1 or row == row2) and (math.fabs(col2-col) == 1 or col2 == col))):
				is_legal_move = False

		if(self.chess_field[row][col].path == ""):
			is_legal_move = False
		if(self.chess_field[row2][col2].path != ""):
			if(("white" in self.chess_field[row][col].path and "white" in self.chess_field[row2][col2].path) or ("black" in self.chess_field[row][col].path and "black" in self.chess_field[row2][col2].path)):
				is_legal_move = False

		return is_legal_move

	def legal_rook_move(self,row,col,row2,col2):
		is_legal_move = True
		if(not((col2 == col or row2 == row))):
			is_legal_move = False
		for i in range(row2+1,row):
			if self.chess_field[i][col2].path != "":
				is_legal_move = False
		for i in range(row+1,row2):
			if self.chess_field[i][col2].path != "":
				is_legal_move = False
		for i in range(col+1,col2):
			if self.chess_field[row2][i].path != "":
				is_legal_move = False
		for i in range(col2+1,col):
			if self.chess_field[row2][i].path != "":
				is_legal_move = False
		return is_legal_move

	def legal_bishop_move(self,row,col,row2,col2):
		is_legal_move = True
		if(not(math.fabs(row2-row) == math.fabs(col2-col))):
			is_legal_move = False
		if(col2 > col and row2 < row):
			for i in range(1,col2-col):
				if self.chess_field[row-i][col+i].path != "":
					is_legal_move = False
		elif(col2 < col and row2 < row):
			for i in range(1,col-col2):
				if self.chess_field[row2+i][col2+i].path != "":
					is_legal_move = False
		elif(col2 < col and row2 > row):
			for i in range(1,col-col2):
				if self.chess_field[row+i][col-i].path != "":
					is_legal_move = False
		elif(col2 > col and row2 > row):
			for i in range(1,col2-col):
				if self.chess_field[row+i][col+i].path != "":
					is_legal_move = False
		return is_legal_move
				

	def print_chess_field(self):
		for row in self.chess_field:
			for elem in row:
				if(elem.path != ""):
					elem.img.draw(self.win)


	def initialize_game_field(self):
		self.chess_field = []
		firstrow = [Chess_Piece(52,52,"black_rook.gif"),Chess_Piece(154,52,"black_knight.gif"),Chess_Piece(256,52,"black_bishop.gif"),Chess_Piece(358,52,"black_queen.gif"),
		Chess_Piece(460,52,"black_king.gif"),Chess_Piece(562,52,"black_bishop.gif"),Chess_Piece(664,52,"black_knight.gif"),Chess_Piece(766,52,"black_rook.gif")]
		secondrow = []
		for i in range(0,8):
			secondrow.append(Chess_Piece(52 + i*103,155,"black_pawn.gif"))
		seventhrow = []
		for i in range(0,8):
			seventhrow.append(Chess_Piece(52 + i*103,670,"white_pawn.gif"))
		
		eighthrow = [Chess_Piece(52,773,"white_rook.gif"),Chess_Piece(154,773,"white_knight.gif"),Chess_Piece(256,773,"white_bishop.gif"),Chess_Piece(358,773,"white_queen.gif"),
		Chess_Piece(460,773,"white_king.gif"),Chess_Piece(562,773,"white_bishop.gif"),Chess_Piece(664,773,"white_knight.gif"),Chess_Piece(766,773,"white_rook.gif")]
		self.chess_field.append(firstrow)
		self.chess_field.append(secondrow)
		for row in range(2,6):
			onerow = []
			for col in range(0,8):
				onerow.append(Chess_Piece(52+col*103,52 + row * 103,""))
			print(onerow[0].img.anchor.x)
			self.chess_field.append(onerow)
		self.chess_field.append(seventhrow)
		self.chess_field.append(eighthrow)


demo = Chess_Game()
