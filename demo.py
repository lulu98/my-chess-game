from graphics import *
import speech_rec
import math
from button import *
'''TODO: 
- history table
- button to play back move
- timer
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
		self.stop_flag = False
		self.initialize_game_field()
		self.initialize_gui()
		self.print_chess_field()
		self.version_classic()
		#self.version_voice_control()

	def initialize_gui(self):
		backgroundImage = Image(Point(412, 412), "plain_chess_field.gif")
		self.win = GraphWin("My Chess Game", backgroundImage.getWidth() + 500, backgroundImage.getHeight() + 25)
		self.win.setBackground('gray')
		backgroundImage.draw(self.win)
		for i in range(0, len(self.chess_field)):
			txt = Text(Point(i * SIZE_OF_BOX + SIZE_OF_BOX / 2, backgroundImage.getHeight() + 10), chr(i + 65))
			txt.draw(self.win)
			txt2 = Text(Point(backgroundImage.getWidth() + 10, i * SIZE_OF_BOX + SIZE_OF_BOX / 2), 8 - i)
			txt2.draw(self.win)
		self.exit_btn = Button(backgroundImage.getWidth() + 150, 700, backgroundImage.getWidth() + 300, 750, "Exit",self.win)
		self.enter_btn = Button(backgroundImage.getWidth() + 150,600, backgroundImage.getWidth()+300,650,"Enter",self.win)
		txt1 = Text(Point(backgroundImage.getWidth()+100,20),"Start Position:")
		txt1.draw(self.win)
		txt2 = Text(Point(backgroundImage.getWidth()+100,270),"End Position:")
		txt2.draw(self.win)
		self.first_move_x_position = Move_Entry(backgroundImage.getWidth() + 50, 50, backgroundImage.getWidth() + 200, 250, ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'], self.win)
		self.first_move_y_position = Move_Entry(backgroundImage.getWidth() + 250, 50, backgroundImage.getWidth() + 400, 250, ['1', '2', '3', '4', '5', '6', '7', '8'], self.win)
		self.second_move_x_position= Move_Entry(backgroundImage.getWidth() + 50, 300, backgroundImage.getWidth() + 200, 500, ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'], self.win)
		self.second_move_y_position = Move_Entry(backgroundImage.getWidth() + 250, 300, backgroundImage.getWidth() + 400, 500, ['1', '2', '3', '4', '5', '6', '7', '8'], self.win)

	def move_entry_to_position(self,entry):
		entry = entry.lower()
		if(entry == "a" or entry == "b" or entry == "c" or entry == "d" or entry == "e" or entry == "f" or entry == "g" or entry == "h"):
			return ord(entry) - 97
		elif(entry == "1" or entry == "2" or entry == "3" or entry == "4" or entry == "5" or entry == "6" or entry == "7" or entry == "8"):
			return 8-int(entry)

	def button_clicked(self,x,y):
		if(self.exit_btn.is_clicked(x,y)):
			sys.exit()
		elif(self.enter_btn.is_clicked(x,y)):
			row = self.move_entry_to_position(self.first_move_y_position.get_text())
			col = self.move_entry_to_position(self.first_move_x_position.get_text())
			row2 = self.move_entry_to_position(self.second_move_y_position.get_text())
			col2 = self.move_entry_to_position(self.second_move_x_position.get_text())

			print(row, col)
			if (row != None and col != None and self.chess_field[row][col].path != ""):
				print("1: ", self.chess_field[row][col].path)
				print(row2, col2)
				if (row2 != None and col2 != None and (row != row2 or col != col2)):
					print("2: ", self.chess_field[row2][col2].path)
					self.perform_move(row,col,row2,col2)

			self.first_move_x_position.reset()
			self.second_move_x_position.reset()
			self.first_move_y_position.reset()
			self.second_move_y_position.reset()
		elif(self.first_move_x_position.is_clicked(x, y)):
			if self.first_move_x_position.is_increase(x, y):
				self.first_move_x_position.increase()
			elif self.first_move_x_position.is_decrease(x, y):
				self.first_move_x_position.decrease()
		elif (self.first_move_y_position.is_clicked(x, y)):
			if self.first_move_y_position.is_increase(x, y):
				self.first_move_y_position.increase()
			elif self.first_move_y_position.is_decrease(x, y):
				self.first_move_y_position.decrease()
		elif (self.second_move_x_position.is_clicked(x, y)):
			if self.second_move_x_position.is_increase(x, y):
				self.second_move_x_position.increase()
			elif self.second_move_x_position.is_decrease(x, y):
				self.second_move_x_position.decrease()
		elif (self.second_move_y_position.is_clicked(x, y)):
			if self.second_move_y_position.is_increase(x, y):
				self.second_move_y_position.increase()
			elif self.second_move_y_position.is_decrease(x, y):
				self.second_move_y_position.decrease()

	def version_classic(self):
		self.turn = "white"
		self.game_over = False
		while (not (self.game_over)):
			print(self.turn + "'s turn.")
			self.one_step()

		print("Game over!")
		if (self.turn == "white"):
			print("Black player is the winner!")
		else:
			print("White player is the winner!")
		time.sleep(1)
		self.win.close()

	def one_step(self):
		location = self.win.getMouse()
		self.button_clicked(location.getX(), location.getY())
		if (not self.enter_btn.is_clicked(location.getX(), location.getY())):
			for row in range(0, len(self.chess_field)):
				for col in range(0, len(self.chess_field)):
					if (self.chess_field[row][col].path != "" and location.getX() >= self.chess_field[row][col].lowerX and location.getX() <= self.chess_field[row][col].upperX and location.getY() >=self.chess_field[row][col].lowerY and location.getY() <= self.chess_field[row][col].upperY):
						print("1: ", self.chess_field[row][col].path)
						self.calculate_move(row,col,location)

	def calculate_move(self,row,col,location):
		location2 = self.win.getMouse()
		self.button_clicked(location2.getX(), location2.getY())
		if (not (self.enter_btn.is_clicked(location2.getX(),location2.getY())) and location2.getX() != location.getX() or location2.getY() != location.getY()):
			for row2 in range(0, len(self.chess_field)):
				for col2 in range(0, len(self.chess_field)):
					if (location2.getX() >= self.chess_field[row2][col2].lowerX and location2.getX() <=self.chess_field[row2][col2].upperX and location2.getY() >= self.chess_field[row2][col2].lowerY and location2.getY() <= self.chess_field[row2][col2].upperY):
						print("2: ", self.chess_field[row2][col2].path)
						self.perform_move(row,col,row2,col2)

	def perform_move(self,row,col,row2,col2):
		if (self.turn in self.chess_field[row][col].path and self.legal_move(row, col, row2, col2)):
			if ("king" in self.chess_field[row2][col2].path):
				self.game_over = True
			else:
				self.chess_field[row2][col2].img.undraw()
				self.chess_field[row2][col2] = Chess_Piece(self.chess_field[row2][col2].img.anchor.x,self.chess_field[row2][col2].img.anchor.y,self.chess_field[row][col].path)
				self.chess_field[row2][col2].img.draw(self.win)
				self.chess_field[row][col].img.undraw()
				self.chess_field[row][col] = Chess_Piece(self.chess_field[row][col].img.anchor.x,self.chess_field[row][col].img.anchor.y, "")
				self.chess_field[row][col].img.draw(self.win)
			if (self.turn == "white"):
				self.turn = "black"
			else:
				self.turn = "white"

	def version_voice_control(self):
		turn = "white"
		game_over = False
		while (not (game_over)):
			print(turn + "'s turn.")
			row, col = speech_rec.get_position()
			print(row,col)
			if (row != None and col != None and self.chess_field[row][col].path != ""):
				print("1: ", self.chess_field[row][col].path)
				row2, col2 = speech_rec.get_position()
				print(row2,col2)
				if (row2 != None and col2 != None and (row != row2 or col != col2)):
					print("2: ", self.chess_field[row2][col2].path)
					if (turn in self.chess_field[row][col].path and self.legal_move(row, col, row2, col2)):
						if ("king" in self.chess_field[row2][col2].path):
							game_over = True
						else:
							self.chess_field[row2][col2].img.undraw()
							self.chess_field[row2][col2] = Chess_Piece(self.chess_field[row2][col2].img.anchor.x,self.chess_field[row2][col2].img.anchor.y,self.chess_field[row][col].path)
							self.chess_field[row2][col2].img.draw(self.win)
							self.chess_field[row][col].img.undraw()
							self.chess_field[row][col] = Chess_Piece(self.chess_field[row][col].img.anchor.x,self.chess_field[row][col].img.anchor.y, "")
							self.chess_field[row][col].img.draw(self.win)
						if (turn == "white"):
							turn = "black"
						else:
							turn = "white"

			time.sleep(0.1)
		print("Game over!")
		if (turn == "white"):
			print("Black player is the winner!")
		else:
			print("White player is the winner!")
		time.sleep(1)
		self.win.close()

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
		self.history_table = []
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
			self.chess_field.append(onerow)
		self.chess_field.append(seventhrow)
		self.chess_field.append(eighthrow)



demo = Chess_Game()
