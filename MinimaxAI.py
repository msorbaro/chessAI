#Morgan Sorbaro
#11/3/17
#Chess Minimax program
#This program implements the minimax algorith to play chess

#imports
import chess
import math

#Node class to store values associated with states in the minimax algorithm
class minimax_node():
    #Node keeps track to the move and hte value associated with the move
    def __init__(self, value, move):
        self.value = value
        self.move = move

#Actual minimax AI class to compute the needed move for the program
class MinimaxAI():
    #takes a depth and starts a count so see how many times minimax was called
    def __init__(self, depth):
        self.depth = depth
        self.count = 0
        self.dictionary = {}

    #This method calls the method that will find the move. Iterative deepening can be used here or just the minimax algorithm
    def choose_move(self, board):
        #Example of using itereatice deeping to find the move
        move = self.iterative_deepening(board, self.depth).move

        #Example of using just the minimax algorithm to find the move
        #move = self.minimax(board, self.depth, True).move #call the algorithm
        #Print the depth and counts after the move has been selected
        print("Depth: " + str(self.depth) + " Count: " + str(self.count))
        self.count = 0 #reset the count

        #return the move that has been choosen
        return move

    #algorithm that chooses the move with iteratice deeping. Finds the best move from depth 1 - given depth
    def iterative_deepening(self, board, depth):
        best = -math.inf
        node = None
        #goes through each depth and finds the node that minimax returns at that depth
        for i in range(1, depth):
            curr = self.minimax(board, i, True) #gets node that minimax returns at assocaited depth
            print(str(curr.move) + "  " + str(curr.value))
            #Checks to see if the current value of the recently returned node is greater than the currently stored greatest node
            if curr.value > best:
                print("Changing best to: " + str(curr.move) )
                best = curr.value #if it is, update the best value
                node = curr #and update the current node

        return node #return node, which is the best node for all those depths


    #This is the minimax algorithm that searches to a speciifc depth and finds the best move for the AI
    def minimax(self, board, depth, maximizingPlayer):

        self.count = self.count + 1 #incrementing the count

        #Base case to stop recursion: game is over or depth has been reached
        if depth == 0 or board.is_game_over():
            return minimax_node(self.utility(board), None) #return the utility with that leaf node

        #If it is a max situation, find the max value between the returned node
        if maximizingPlayer:
            bestValue = -math.inf #start at negative infinity so everything is better
            action = None # no action to start

            #create a list of moves that are arranged by their utility
            movelist= self.rank_moves(list(board.legal_moves), board)

            #go through each of the potential moves and check the compared utilities
            for move in movelist:

                #add the move to the board
                board.push(move)
                v = 0 #initializing the value

                #if the board layout is in the hashtable, set v to the value
                if str(board) in self.dictionary.keys():
                    v = self.dictionary[str(board)]
                else:#otherwise calculate the value of that board using recursion
                    v = self.minimax(board, depth-1, False).value

                #find the max of the new value and the current max best vale
                if v > bestValue:
                    bestValue = v #reset best value is the current value is creater
                    action = move # set the move to be associated with this value
                board.pop() #undo the changes to the board object

            return minimax_node(bestValue, action) #return the node with the value and the action

        #min situation
        else:

            bestValue = math.inf #set best value to infinity so everything is less than it
            action = None #starting action is nothing

            #get the move list in the ranked order with value
            movelist= self.rank_moves(list(board.legal_moves), board)

            #for each move, calculate and compare the values
            for move in movelist:

                board.push(move) #push new move onto board
                v = 0 #initialize value holder

                #if the board is in the dictionary, set v to that value associated iwth it
                if str(board) in self.dictionary.keys():
                    v = self.dictionary[str(board)]
                else: #otherwise calculate the value with the minimax function recursion
                    v = self.minimax(board, depth - 1, False).value

                #if the value is less than the current best value (min)
                if v < bestValue:
                    bestValue = v #reset the best value to be hte current value
                    action = move #set the move to the cooresponding move

                board.pop() #undo the board action

            return minimax_node(bestValue, action) #return the right node

    #this function manipulates the list of moves and puts them in order of greatest utility
    def rank_moves(self, movelist, board):
        removeNode = minimax_node(math.inf, None) #node to instantiate the list but will be removed later
        sortedlist = [removeNode] #create list

        #Go through each move in the list of potentia moves
        for move in movelist:
            board.push(move) #put the move on the board

            #find the utility of the board at that current move
            v = self.utility(board)

            #if the v is less that the value of the top move then bring it to
            if v < sortedlist[0].value: #put the node at the front of the list so it will be accessed soon
                sortedlist.insert(0, minimax_node(v, move))
            else:  #add the node to the end because it is not an improvement node
                sortedlist.append(minimax_node(v, move))

            #undo the board changes
            board.pop()

        sortedlist.remove(removeNode) #remove the random temp node i made
        returnlist = [] #make a list to return of just the moves not hte whole nodes

        #add move and not just the node for each node in the list
        for move in sortedlist:
            returnlist.append(move.move)

        return returnlist #return the list


    #Calculates the utility of the board. Adds up all the pieces of the AI and subtracts other peices
    def utility(self, board):

        ##Adds all the black coordinates for all the pieces
        total = len(board.pieces(chess.BISHOP, chess.BLACK)) + len(board.pieces(chess.PAWN, chess.BLACK)) + \
                len(board.pieces(chess.KING, chess.BLACK)) + len(board.pieces(chess.QUEEN, chess.BLACK)) + \
                len(board.pieces(chess.ROOK, chess.BLACK)) + len(board.pieces(chess.KNIGHT, chess.BLACK))

        ##subtracts all teh white coordinates for all the pices
        total = total - len(board.pieces(chess.BISHOP, chess.WHITE)) - len(board.pieces(chess.PAWN, chess.WHITE)) - \
                len(board.pieces(chess.KING, chess.WHITE)) - len(board.pieces(chess.QUEEN, chess.WHITE)) - \
                len(board.pieces(chess.ROOK, chess.WHITE)) - len(board.pieces(chess.KNIGHT, chess.WHITE))

        return total #return total value