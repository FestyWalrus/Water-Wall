import numpy as np
import pygame

bgImg = pygame.image.load('data/images/bg.png')
titleImg = pygame.image.load('data/images/title.png')
helpImg = pygame.image.load('data/images/help.png')

class Piece:

	def __placePiece(self, gameField, piece, rotation, xPos, yPos, rotated):
		
		shapeArray = np.rot90(self.shapes[piece], rotation, (1,0))

		shapeY = shapeArray.shape[0]
		shapeX = shapeArray.shape[1]
			

		for y in range(0, shapeY):
			for x in range(0, shapeX):
				try:
					if gameField.currentField[yPos + y, xPos + x] != b'*' and shapeArray[y,x] != b' ':
						return 1 #collision
					if shapeArray[y,x] != b' ' and xPos + x< 0:
						return 1 #hit left side
				except:
					if shapeArray[y,x] != b' ' and yPos + y > gameField.height - 1:
						return 1 #hit the floor
					if shapeArray[y,x] != b' ' and xPos + shapeX > gameField.width - 1:
						return 1 #hit right side

		gameField.reShow()
		for y in range(0, shapeY):
			for x in range(0, shapeX):
				try:
					if shapeArray[y,x] != b' ':
						gameField.playingField[yPos + y, xPos + x] = shapeArray[y,x] #place a cell
				except:
					pass
		return 0

	def __init__(self, gameField, pieceName, xPos, yPos):

		#tetris shapes
		self.shapes = {
			b'I': np.array([[' ',' ',' ',' '], ['I','I','I','I'], [' ',' ',' ',' '], [' ',' ',' ',' ']], dtype="S1", order='C'),
			b'J': np.array([['J',' ',' '], ['J','J','J'], [' ',' ',' ']], dtype="S1", order='C'),
			b'L': np.array([[' ',' ','L'], ['L','L','L'], [' ',' ',' ']], dtype="S1", order='C'),
			b'O': np.array([['O','O'], ['O','O']], dtype="S1", order='C'),
			b'S': np.array([[' ',' ',' '], [' ','S','S'], ['S','S',' ']], dtype="S1", order='C'),
			b'T': np.array([[' ','T',' '], ['T','T','T'], [' ',' ',' ']], dtype="S1", order='C'),
			b'Z': np.array([[' ',' ',' '], ['Z','Z',' '], [' ','Z','Z']], dtype="S1", order='C'),
			b'N': np.array([[' ',' '], [' ',' ']], dtype="S1", order='C') #null
		}

		self.pieceName = pieceName
		self.xPos = xPos
		self.yPos = yPos
		self.rotCount = 0

		self.shapeY = self.shapes[self.pieceName].shape[0]
		self.shapeX = self.shapes[self.pieceName].shape[1]

		self.__placePiece(gameField, self.pieceName, self.rotCount, self.xPos, self.yPos, False)

	def reset(self, pieceName, gameField, xPos, yPos):
		self.pieceName = pieceName
		self.xPos = xPos
		self.yPos = yPos
		self.rotCount = 0

		self.shapeY = self.shapes[self.pieceName].shape[0]
		self.shapeX = self.shapes[self.pieceName].shape[1]

		self.__placePiece(gameField, self.pieceName, self.rotCount, self.xPos, self.yPos, False)

	def rotateRight(self, gameField):
		origRotCount = self.rotCount
		origX = self.xPos
		origY = self.yPos

		self.rotCount += 1

		couldRotate = False
		for i in range(0, 4):
			if self.__placePiece(gameField, self.pieceName, self.rotCount, self.xPos, self.yPos, True) == 1:
				if self.xPos > 6:
					self.xPos -= 1
				elif self.xPos < 4:
					self.xPos +=1
			else:
				couldRotate = True

		if not couldRotate:
			self.rotCount = origRotCount
			self.xPos = origX
			self.yPos = origY
			self.__placePiece(gameField, self.pieceName, self.rotCount, self.xPos, self.yPos, True)

	def rotateLeft(self, gameField):
		origRotCount = self.rotCount
		origX = self.xPos
		origY = self.yPos

		self.rotCount -= 1

		couldRotate = False
		for i in range(0, 4):
			if self.__placePiece(gameField, self.pieceName, self.rotCount, self.xPos, self.yPos, True) == 1:
				if self.xPos > 6:
					self.xPos -= 1
				elif self.xPos < 4:
					self.xPos +=1
			else:
				couldRotate = True

		if not couldRotate:
			self.rotCount = origRotCount
			self.xPos = origX
			self.yPos = origY
			self.__placePiece(gameField, self.pieceName, self.rotCount, self.xPos, self.yPos, True)

	def dropOne(self, gameField):
		#Return 1 for a collision
		#Return 2 for a collision above the board (game over)
		#Return 3 for contact with another piece to start the lock timer

		distToBottom = (gameField.height - self.yPos) - self.shapeY

		#if distToBottom > 0:
		self.yPos += 1
		testPos = self.yPos + 1

		
		contactValue = self.__placePiece(gameField, self.pieceName, self.rotCount, self.xPos, testPos, False)
		returnValue = self.__placePiece(gameField, self.pieceName, self.rotCount, self.xPos, self.yPos, False)


		if returnValue == 1:
			if self.yPos < 5:
				return 2
			else:
				print("Lock")
				return 1
		if contactValue == 1:
			return 3
		#else:
			#return 1

	def right(self, gameField):
		self.xPos += 1
		if self.__placePiece(gameField, self.pieceName, self.rotCount, self.xPos, self.yPos, False) == 1:
			self.xPos -= 1
			self.__placePiece(gameField, self.pieceName, self.rotCount, self.xPos, self.yPos, False)

	def left(self, gameField):
		self.xPos -= 1
		if self.__placePiece(gameField, self.pieceName, self.rotCount, self.xPos, self.yPos, False) == 1:
			self.xPos += 1
			self.__placePiece(gameField, self.pieceName, self.rotCount, self.xPos, self.yPos, False)

		
class GameField:
	
	def __init__(self, width, height, screenWidthPx, screenHeightPx, marginPx, screenObj, scoreBoard):

		self.screenObj = screenObj
		self.scoreBoard = scoreBoard

		self.colors = {
			b' ': (50,50,50),
			b'*': (0,0,0),
			b'I': (0,255,255),
			b'O': (255,255,0),
			b'T': (255,0,200),
			b'S': (0,255,0),
			b'Z': (255,0,0),
			b'J': (0,0,255),
			b'L': (255,128,0),
			b'W': (255,255,255)
		}

		self.IImg = pygame.image.load('data/images/I.png')
		self.OImg = pygame.image.load('data/images/O.png')
		self.TImg = pygame.image.load('data/images/T.png')
		self.SImg = pygame.image.load('data/images/S.png')
		self.ZImg = pygame.image.load('data/images/Z.png')
		self.JImg = pygame.image.load('data/images/J.png')
		self.LImg = pygame.image.load('data/images/L.png')
		self.WImg = pygame.image.load('data/images/W.png')
		
		self.images = {
			b'I': self.IImg,
			b'O': self.OImg,
			b'T': self.TImg,
			b'S': self.SImg,
			b'Z': self.ZImg,
			b'J': self.JImg,
			b'L': self.LImg,
			b'W': self.WImg
		}

		

		self.marginPx = marginPx

		self.screenWidthPx = screenWidthPx
		self.screenHeightPx = screenHeightPx

		self.width = width
		self.height = height

		self.cellSize = (self.screenHeightPx - marginPx*2) / 20

		self.currentField = np.zeros((height, width), dtype='S1', order='C')
		self.currentField.fill(b'*')

		self.playingField = np.zeros((height, width), dtype='S1', order='C')
		np.copyto(self.playingField, self.currentField)

	def reset(self):
		self.currentField = np.zeros((self.height, self.width), dtype='S1', order='C')
		self.currentField.fill(b'*')

		self.playingField = np.zeros((self.height, self.width), dtype='S1', order='C')
		np.copyto(self.playingField, self.currentField)
		self.render()

	def applyField(self):
		np.copyto(self.currentField, self.playingField)

	def reShow(self):
		np.copyto(self.playingField, self.currentField)

	def checkLines(self, speedTime, screen, scoreBoard):
		pygame.time.set_timer(pygame.USEREVENT, 0)
		numLines = 0
		for row in range(4, self.height):
			pieceLocs = ~np.isin(self.currentField[row], [b'*'])
			#print(np.all(pieceLocs))
			if np.all(pieceLocs):

				''' Old, non-animated line indicator
				self.currentField[row].fill(b'W')
				self.reShow()	
				screen.blit(bgImg, (0,0))
				scoreBoard.render()
				self.render()
				pygame.display.update()
				pygame.time.delay(200)
				'''

				#New animated line indicator
				stopPoint = int((self.cellSize * self.width) / 2)
				for i in range(0, stopPoint):
					screen.blit(self.images[b'W'], (self.marginPx + (self.cellSize * (self.width / 2)) + i, self.marginPx + self.cellSize * (row - 4)))
					screen.blit(self.images[b'W'], (self.marginPx + (self.cellSize * (self.width / 2)) - i, self.marginPx + self.cellSize * (row - 4)))
					pygame.display.update() 
					pygame.time.wait(int(1 / stopPoint) ^ int(i / 30) )

				pygame.time.wait(100)

				self.currentField[row].fill(b'*')
				self.reShow()
				screen.blit(bgImg, (0,0))
				scoreBoard.render()
				numLines += 1
				self.render()
				pygame.display.update()

				for i in range(stopPoint, 0, -1):
					screen.blit(bgImg, (0,0))
					scoreBoard.render()
					self.render()

					if i == stopPoint - self.cellSize:
						print(2)
						np.copyto(self.currentField[3:row+1,0], self.currentField[2:row, 0])
						np.copyto(self.currentField[3:row+1,9], self.currentField[2:row, 9])
					if i == stopPoint - self.cellSize * 2:
						print(4)
						np.copyto(self.currentField[3:row+1,1], self.currentField[2:row, 1])
						np.copyto(self.currentField[3:row+1,8], self.currentField[2:row, 8])
					if i == stopPoint - self.cellSize * 3:
						print(6)
						np.copyto(self.currentField[3:row+1,2], self.currentField[2:row, 2])
						np.copyto(self.currentField[3:row+1,7], self.currentField[2:row, 7])
					if i == stopPoint - self.cellSize * 4:
						print(8)
						np.copyto(self.currentField[3:row+1,3], self.currentField[2:row, 3])
						np.copyto(self.currentField[3:row+1,6], self.currentField[2:row, 6])
					if i <= stopPoint - stopPoint + 1:
						print(10)
						np.copyto(self.currentField[3:row+1,4], self.currentField[2:row, 4])
						np.copyto(self.currentField[3:row+1,5], self.currentField[2:row, 5])


					self.reShow()

					for pos in range(0, i):
						screen.blit(self.images[b'W'], (self.marginPx + (self.cellSize * (self.width / 2)) + pos, self.marginPx + self.cellSize * (row - 4)))
						screen.blit(self.images[b'W'], (self.marginPx + (self.cellSize * (self.width / 2)) - pos, self.marginPx + self.cellSize * (row - 4)))

					pygame.display.update() 
					pygame.time.wait(int(1 / stopPoint) ^ int((i*-1) / 30) )

				pygame.event.clear()

				#np.copyto(self.currentField[3:row+1,0:10], self.currentField[2:row, 0:10])

				self.reShow()
				screen.blit(bgImg, (0,0))
				scoreBoard.render()
				self.render()
				pygame.display.update()
				pygame.time.wait(150)
		
		screen.blit(bgImg, (0,0))
		self.render()
		self.scoreBoard.addLines(numLines, self)
		scoreBoard.render()
		pygame.display.update()

		if numLines > 0:
			pygame.time.delay(1000)

		pygame.time.set_timer(pygame.USEREVENT, speedTime)
			

	def render(self):
		#cellSize is 23px

		#render the game board
		for row in range(4, self.height): #4 rows are hidden for pieces to spawn above the field
			for col in range(0, self.width):
				xPos = self.cellSize * col + self.marginPx
				yPos = (self.cellSize * row + self.marginPx) - self.cellSize * 4 #so the hidden cells don't shift the whole grid down
				if self.playingField[row][col] != b'*' and self.playingField[row][col] != b' ':
					#pygame.draw.rect(self.screenObj, self.colors[self.playingField[row][col]], pygame.Rect(xPos, yPos, self.cellSize - 2, self.cellSize - 2))
					self.screenObj.blit(self.images[self.playingField[row][col]], (xPos, yPos))

		#render the next piece area

		nextPieceWindowWidth = 130
		nextPieceWindowHeight = 150

		centeredX = self.nextPieceWindowX + (nextPieceWindowWidth - (self.cellSize * self.nextPieceShapeX)) / 2
		centeredY = self.nextPieceWindowY + (nextPieceWindowHeight - (self.cellSize * self.nextPieceShapeY)) / 2

		centeredY += 20

		for row in range(0, self.nextPieceShapeY):
			for col in range(0, self.nextPieceShapeX):
				xPos = centeredX + self.cellSize * col
				yPos = centeredY + self.cellSize * row
				if self.nextPiece[row][col] != b'*' and self.nextPiece[row][col] != b' ':
					#pygame.draw.rect(self.screenObj, self.colors[self.nextPiece[row][col]], pygame.Rect(xPos, yPos, self.cellSize - 2, self.cellSize - 2))
					self.screenObj.blit(self.images[self.nextPiece[row][col]], (xPos, yPos))

	def setNextPiece(self, nextPiece):
		self.nextPiece = nextPiece
		self.nextPieceShapeY = nextPiece.shape[0]
		self.nextPieceShapeX = nextPiece.shape[1]

		self.nextPieceWindowX = 270
		self.nextPieceWindowY = 50


class ScoreBoard:
	
	def __init__(self, screenObj, configObj):
		pygame.font.init()
		self.dFont = pygame.font.Font('data/fonts/LemonMilk.otf', 16)
		self.goFont = pygame.font.Font('data/fonts/LemonMilk.otf', 36)
		self.goFont2 = pygame.font.Font('data/fonts/LemonMilk.otf', 16)
		self.gameOverTextSurface = self.goFont.render("GAME OVER", False, (230,30,0))
		self.gameOverTextSurface2 = self.goFont2.render("Press F to pay respects", False, (230,30,0))
		self.gameOverTextSurface3 = self.goFont2.render("I mean play again", False, (230,30,0))



		self.screenObj = screenObj
		self.cfgObj = configObj
		self.nextPiece = b'?'

		self.score = 0
		self.level = 1
		self.lines = 0
		self.hiScore = self.cfgObj.getHiscore()
		self.bigTextActive = False

	def disableBigText(self):
		self.bigTextActive = False

	def render(self):
		scoreTextSurface = self.dFont.render('Score: ' + str(self.score), False, (255,255,255))
		self.screenObj.blit(scoreTextSurface, (280, 304))

		levelTextSurface = self.dFont.render('Level: ' + str(self.level), False, (255,255,255))
		self.screenObj.blit(levelTextSurface, (280, 334))

		linesTextSurface = self.dFont.render('Lines: ' + str(self.lines), False, (255,255,255))
		self.screenObj.blit(linesTextSurface, (280, 364))

		hiScoreTextSurface = self.dFont.render('Hi Score: ' + str(self.hiScore), False, (255,255,255))
		self.screenObj.blit(hiScoreTextSurface, (280, 424))

		nextPieceTextSurface = self.goFont2.render(b'Next Piece:', False, (255,255,255))
		self.screenObj.blit(nextPieceTextSurface, (287, 60))

	def writeHiScore(self):	
		self.cfgObj.writeHiscore(self.score)

	def setBigText(self, gameField, text, subText="", shaded=False):
		
		gameFieldShade = pygame.Surface((gameField.width * gameField.cellSize, (gameField.height - 4) * gameField.cellSize))
			

		if self.bigTextActive == False:
			for i in range(420, 27, -10):
				self.bigTextSurface = self.goFont.render(text, False, (30,230,0))
				self.subTextSurface = self.goFont2.render(subText, False, (30,230,0))

				self.screenObj.blit(bgImg, (0,0))
				gameField.render()
				self.render()

				if shaded:
					gameFieldShade.set_alpha(197 - ((i-27) // 2))
					gameFieldShade.fill((0,0,0))
					self.screenObj.blit(gameFieldShade, (0 + gameField.marginPx, 0 + gameField.marginPx))

				self.screenObj.blit(self.bigTextSurface, (i, 220))
				self.screenObj.blit(self.subTextSurface, (i + 7, 270))

				pygame.display.update()
		else:
			self.bigTextSurface = self.goFont.render(text, False, (30,230,0))
			self.subTextSurface = self.goFont2.render(subText, False, (30,230,0))

			self.screenObj.blit(bgImg, (0,0))
			gameField.render()
			self.render()

			if shaded:
				gameFieldShade.set_alpha(197)
				gameFieldShade.fill((0,0,0))
				self.screenObj.blit(gameFieldShade, (0 + gameField.marginPx, 0 + gameField.marginPx))

			self.screenObj.blit(self.bigTextSurface, (28, 220))
			self.screenObj.blit(self.subTextSurface, (35, 270))

			pygame.display.update()
		self.bigTextActive = True
		

	def addLines(self, numLines, gameField, isShaded = True):
		self.lines += numLines

		if numLines > 0:
			scoreToAdd = 20*numLines^2

			#render
			self.setBigText(gameField, str(numLines) + " LINES", subText="+" + str(scoreToAdd) + " POINTS!", shaded=isShaded)

			self.addScore(scoreToAdd)

	def addScore(self, amount):
		self.score += amount
		self.level = (self.score // 1000) + 1

	def gameOver(self, gameField):

		#pygame.draw.rect(self.screenObj, (255,255,255,50), pygame.Rect(0 + gameField.marginPx, 0 + gameField.marginPx, gameField.width * gameField.cellSize, gameField.height * gameField.cellSize))

		gameFieldShade = pygame.Surface((gameField.width * gameField.cellSize, (gameField.height - 4) * gameField.cellSize))
		gameFieldShade.set_alpha(200)
		gameFieldShade.fill((255,255,255))
		self.screenObj.blit(gameFieldShade, (0 + gameField.marginPx, 0 + gameField.marginPx))

		self.screenObj.blit(self.gameOverTextSurface, (28, 220))
		self.screenObj.blit(self.gameOverTextSurface2, (35, 270))
		self.screenObj.blit(self.gameOverTextSurface3, (60, 300))

	def titleScreen(self):
		self.screenObj.blit(titleImg, (0,0))


		titleScoreTextSurface = self.goFont2.render(str(self.cfgObj.getHiscore()), False, (255,255,255))
		self.screenObj.blit(titleScoreTextSurface, (178,136))

		pygame.display.update()

		while True:
			event = pygame.event.wait()
			if event.type == pygame.QUIT:
				quit()
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE:
					return
				if event.key == pygame.K_SLASH or event.key == pygame.K_QUESTION:
					self.screenObj.blit(helpImg, (0,0))
					pygame.display.update()
					while True:
						event = pygame.event.wait()
						if event.type == pygame.QUIT:
							quit()
						elif event.type == pygame.KEYDOWN:
							if event.key == pygame.K_SPACE:
								self.screenObj.blit(titleImg, (0,0))
								pygame.display.update()
								break

	def reset(self):
		self.score = 0
		self.level = 1
		self.lines = 0
		self.hiScore = self.cfgObj.getHiscore()

class ConfigFile:

	def __init__(self):
		try:
			self.cfgFile = open("data/config.txt", "r")
			self.cfgFileLines = self.cfgFile.readlines()
			self.cfgFile.close()
		except:
			self.cfgFile = open("data/config.txt", "w+")
			self.cfgFile.write("0\nMUSIC=ON\nSFX=ON")
			self.cfgFileLines = self.cfgFile.readlines()
			self.cfgFile.close()

	def applySettings(self, hiScore, musicEnabled, sfxEnabled):
		self.cfgFile = open("data/config.txt", "r")
		self.cfgFileLines = self.cfgFile.readlines()

		hiScore = int(self.cfgFileLines[0])

		if "MUSIC=OFF" in self.cfgFileLines[1]:
			musicEnabled = False
		else:
			musicEnabled = True

		if "SFX=OFF" in self.cfgFileLines[2]:
			sfxEnabled = False
		else:
			sfxEnabled = True

		self.cfgFile.close()

	def writeHiscore(self, hiScore):
		self.cfgFile = open("data/config.txt")
		self.cfgFileLines = self.cfgFile.read().splitlines()

		self.cfgFileLines[0] = str(hiScore)

		open('data/config.txt','w').write('\n'.join(self.cfgFileLines))
		self.cfgFile.close()

	def getHiscore(self):
		self.cfgFile = open("data/config.txt", "r")
		self.cfgFileLines = self.cfgFile.readlines()
		self.cfgFile.close()
		return int(self.cfgFileLines[0].rstrip())

	def writeMusic(self, musicEnabled):
		self.cfgFile = open("data/config.txt")
		self.cfgFileLines = self.cfgFile.read().splitlines()

		if musicEnabled:
			self.cfgFileLines[1] = "MUSIC=ON"
		else:
			self.cfgFileLines[1] = "MUSIC=OFF"

		open('data/config.txt','w').write('\n'.join(self.cfgFileLines))
		self.cfgFile.close()

	def writeSfx(self, sfxEnabled):
		self.cfgFile = open("data/config.txt")
		self.cfgFileLines = self.cfgFile.read().splitlines()

		if sfxEnabled:
			self.cfgFileLines[2] = "SFX=ON"
		else:
			self.cfgFileLines[2] = "SFX=OFF"

		open('data/config.txt','w').write('\n'.join(self.cfgFileLines))
		self.cfgFile.close()

	def getMusicConfig(self):
		self.cfgFile = open("data/config.txt", "r")
		self.cfgFileLines = self.cfgFile.readlines()
		self.cfgFile.close()

		musicEnabled = True

		if "MUSIC=OFF" in self.cfgFileLines[1]:
			musicEnabled = False

		return musicEnabled

	def getSfxConfig(self):
		self.cfgFile = open("data/config.txt", "r")
		self.cfgFileLines = self.cfgFile.readlines()
		self.cfgFile.close()

		sfxEnabled = True

		if "SFX=OFF" in self.cfgFileLines[2]:
			sfxEnabled = False

		return sfxEnabled