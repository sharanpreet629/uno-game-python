#****UNO CARD GAME***
#Importing the libraries
import random
import os 

#User defined functions

#To generate the deck of cards
def buildDeck():
	deck = []
	colours = ["Red", "Green", "Yellow", "Blue"]
	values = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, "Draw Two", "Skip", "Reverse"]
	wilds = ["Wild", "Wild Draw Four"]

	for colour in colours:
		for value in values:
			cardVal = "{} {}".format(colour, value)
			deck.append(cardVal)
			if value != 0:
				deck.append(cardVal)

	for i in range(4):
		deck.append(wilds[0])
		deck.append(wilds[1])
	return deck 

#To draw numCards from the deck
def drawCards(numCards):
	cardsDrawn = [unoDeck.pop(0) for i in range(numCards)]
	'''
	for i in range(numCards):
		cardsDrawn.append(unoDeck.pop(0))
	'''
	return cardsDrawn

#To show the hand of the current player
def showHand(player, playerHand):
	print("It's {}'s turn".format(player))
	print("Your Hand:")
	print("---------------------------------")
	y = 1
	for card in playerHand:
		print("{}) {}".format(y, card))
		y += 1
	print("")

#To check if the user can play a card
def canPlay(colour, value, playerHand):
	for card in playerHand:
		if "Wild" in card:
			return True
		elif colour in card or value in card:
			return True
	return False

#for displaying Rules 

def showRules():
	#Clearing screen in Windows
	if os.name == 'nt': 
		_ = os.system('cls') 
		#Clearing screen in Mac and Linux(here, os.name is 'posix') 
	else: 
		_ = os.system('clear') 

	print("")
	print("This is a card game in which 2-5 players can play. To start the game we distribute 5-5 cards to every player from pile. The rest of the cards are placed in a Draw Pile face down. Next to the pile a space should be designated for a Discard Pile. The top card should be placed in the Discard Pile, and the game begins!")
	print("You have to match either by the number, color, or the symbol/Action. For instance, if the Discard Pile has a red card that is an 8 you have to place either a red card or a card with an 8 on it. You can also play a Wild card (which can alter current color in play).")
	print("Enter the number of the card you wish to play.")
	print("")

	temp = input("Enter --resume to resume the game: ")
	while temp != "--resume":
		temp = input("Invalid command. Type --resume to resume the game: ")
		checkInput(temp)

def checkInput(userInput):
    if userInput == "--help":
        showRules()
    elif userInput == "--resume":
        pass
    else:
        pass
    


#Main function
unoDeck = buildDeck()
random.shuffle(unoDeck)
discards = [] #List of discards
players = [] #List of cards for all players
playerNames = [] #Names of players
numPlayers = None
print("Enter --help to display the rules of the game\n")
#Getting players names and assigning five cards to each player
numPlayers = input("How many players? ")

while (numPlayers == "--help" or numPlayers == "--resume"):
    checkInput(numPlayers)
    numPlayers = input("How many players? ")

numPlayers = int(numPlayers)
for i in range(numPlayers):
	name = input("Enter player name: ")
	while name == "--help" or name == "--resume":
		checkInput(name)
		name = input("Enter Player name: ")


	playerNames.append(name)
	players.append(drawCards(5))
players[0].append("Wild Draw Four")


#Printing out the cards assigned to each player
print("\nThe cards are: ")
for (name, cards) in zip(playerNames, players):
	print("Player {} has {}".format(name, cards))
print("")


#Setting up the game
playerTurn = 0
playDirection = 1
playing = True
winner = ""
discards.append(unoDeck.pop(0))
splitCard = discards[0].split(" ", 1)
currentColour = splitCard[0]
if currentColour != "Wild":
	cardVal = splitCard[1]
else:
	cardVal = "Any"

#Main loop
while playing:
	print("")
	showHand(playerNames[playerTurn], players[playerTurn])
	print("Card on top of the discards pile:", discards[-1])

	#Checking if the player has a valid card
	if canPlay(currentColour, cardVal, players[playerTurn]):
		cardChosen = int(input("Enter the card you want to play: "))

		#Checking if the card picked is within the range
		while cardChosen > len(players[playerTurn]):
			cardChosen = int(input("Out of range. Enter the card you want to play: "))

		#Checking if the player picked a valid card
		while not canPlay(currentColour, cardVal, [players[playerTurn][cardChosen-1]]):
			cardChosen = int(input("Invalid card. Pick a different card: "))

		print("You played", players[playerTurn][cardChosen-1])
		print("\nYou played", players[playerTurn][cardChosen-1])
		discards.append(players[playerTurn].pop(cardChosen-1))

		showHand(playerNames[playerTurn], players[playerTurn])
		#showHand(playerNames[playerTurn], players[playerTurn])
		print("Card on top of the discards pile:", discards[-1])

		#Checking if any player won

		if len(players[playerTurn]) == 0:
			playing = False
			winner = playerNames[playerTurn]
		else:
			#Checking for special cards
			splitCard = discards[-1].split(" ", 1)
			currentColour = splitCard[0]
			if len(splitCard) == 1:
				cardVal = "Any"
			else:
				cardVal = splitCard[1]

			#In case player played the wild card
			if cardVal== "Any":

				colours = ["Red", "Green", "Yellow", "Blue"]
				for color in colours:
					print(color)
				option = input("Enter color which you want to pick?\n").title()
				if color not in colours:
					option_2 = input("please choose color from given options: ").title()
					currentColour = option_2
				else:
					currentColour = option


			#Checking for special cards 
			if cardVal == 'Reverse':
				playDirection = playDirection * -1
				print("The game is now in reverse")

			elif cardVal == 'Skip':
				playerTurn += playDirection
				if playerTurn >= numPlayers:
					playerTurn = 0
				elif playerTurn < 0:
					playerTurn = numPlayers - 1	
				print("{}'s turn is now skipped".format(playerNames[playerTurn]))

			elif cardVal == 'Draw Two':
				playerTurn += playDirection
				if playerTurn >= numPlayers:
					playerTurn = 0
				elif playerTurn < 0:
					playerTurn = numPlayers - 1	
				players[playerTurn].extend(drawCards(2))
				print("{} has to draw two cards".format(playerNames[playerTurn]))

			elif cardVal == 'Draw Four':
				playerTurn += playDirection
				if playerTurn >= numPlayers:
					playerTurn = 0
				elif playerTurn < 0:
					playerTurn = numPlayers - 1	
				players[playerTurn].extend(drawCards(4))
				print("{} has to draw four cards".format(playerNames[playerTurn]))

	else:
		input("Press enter to draw a card")
		players[playerTurn].extend(drawCards(1))

	#Next player's turn
	playerTurn += playDirection
	if playerTurn >= numPlayers:
		playerTurn = 0
	elif playerTurn < 0:
		playerTurn = numPlayers - 1


	
print("Game Over!")
print("{} is the winner!".format(winner))










