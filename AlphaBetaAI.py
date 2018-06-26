#Morgan Sorbaro
#11/3/17
#Chess Minimax program
#This program implements the minimax algorith to play chess

#imports
import chess
import math

#Node class to store values associated with states in the minimax algorithm
class ABAI_Node():

    #keeps track of the value and the move
    def __init__(self, value, move):
        self.value = value
        self.move = move

#Actual alphabeta class to compute the needed move for the program
class AlphaBetaAI():

    #keeps track of the depth
    def __init__(self, depth):
        self.depth = depth
        self.count = 0
        self.dictionary = {}
        self.open_book = ["g8f6", "e7e6", "f8b4", "b8c6", "a7a6"]


    #This method calls the method that will find the move. Iterative deepening can be used here or just the minimax algorithm
    def choose_move(self, board):
        print(len(self.open_book))
        if len(self.open_book) > 0:
            print("heyg2g3")
            move = (self.open_book[0])
            self.open_book.remove(move)
            return board.parse_uci(move)

        #Example of using just the alphabeta algorithm to find the move
        move =  self.alphabeta(board, self.depth, -math.inf, math.inf, True).move

        print("Depth: " + str(self.depth) + " Count: " + str(self.count))
        self.count = 0 #reset the count

        #return the move that has been choosen
        return move

    #This is the alphabeta algorithm that searches to a speciifc depth and finds the best move for the AI
    def alphabeta(self, board, depth, alpha, beta, maximizingPlayer):

        self.count = self.count + 1  # incrementing the count

        #Base case to stop recursion: game is over or depth has been reached
        if depth == 0 or board.is_game_over():
            return ABAI_Node(self.utility(board), None) #return the utility with that leaf node

        #If it is a max situation, find the max value between the returned node
        if maximizingPlayer:
            v = -math.inf  #start at negative infinity so everything is better
            action = None # no action to start

            #create a list of moves that are arranged by their utility
            movelist= self.rank_moves(list(board.legal_moves), board)

            #go through each of the potential moves and check the compared utilities
            for move in movelist:

                board.push(move) # add the move to the board

                curr = None #current node

                # if the board layout is in the hashtable, set curr to the value
                if str(board) in self.dictionary.keys():
                    curr = self.dictionary[str(board)]
                else:  # otherwise calculate the value of that board using recursion
                    curr = self.alphabeta(board, depth - 1, alpha, beta, False)  # get the current point to use its values and moves

                #find the max of the new value and the current max best vale
                if curr.value > v:
                    v = curr.value #update v
                    action = move #update best move

                #if v is greater than alpha
                if v > alpha:
                    alpha = v #update alpha

                #if v is greater than beta
                if beta <= alpha:
                    board.pop()  #pop because need to make sure this happens
                    break #then break, wont be in here

                #pop
                board.pop()

            #return final node
            return ABAI_Node(v, action)


        else: #minimizing

            v = math.inf #set best value to infinity so everything is less than it
            action = None #starting action is nothing

            #get the move list in the ranked order with value
            movelist= self.rank_moves(list(board.legal_moves), board)

            #for each move, calculate and compare the values
            for move in movelist:

                #add the new move to board
                board.push(move)

                curr = None #current node

                # if the board layout is in the hashtable, set curr to the value
                if str(board) in self.dictionary.keys():
                    curr = self.dictionary[str(board)]
                else:  # otherwise calculate the value of that board using recursion
                    curr = self.alphabeta(board, depth - 1, alpha, beta, False)  # get the current point to use its values and moves

                #find the max of the new value and the current max best vale
                if curr.value < v:
                    v = curr.value #update v
                    action = move #update action

                #if v is less than beta, update beta
                if v < beta:
                    beta = v

                #if beta is less than or equal to alpha break
                if beta <= alpha:
                    board.pop() #pop board first to fix changes
                    break

                board.pop() #pop board out of break

            #return node
            return ABAI_Node(v, action)



    # this function manipulates the list of moves and puts them in order of greatest utility
    def rank_moves(self, movelist, board):
        removeNode = ABAI_Node(math.inf, None)  # node to instantiate the list but will be removed later
        sortedlist = [removeNode]  # create list

        # Go through each move in the list of potentia moves
        for move in movelist:
            board.push(move)  # put the move on the board

            # find the utility of the board at that current move
            v = self.utility(board)

            # if the v is less that the value of the top move then bring it to
            if v < sortedlist[0].value:  # put the node at the front of the list so it will be accessed soon
                sortedlist.insert(0, ABAI_Node(v, move))
            else:  # add the node to the end because it is not an improvement node
                sortedlist.append(ABAI_Node(v, move))

            # undo the board changes
            board.pop()

        sortedlist.remove(removeNode)  # remove the random temp node i made
        returnlist = []  # make a list to return of just the moves not hte whole nodes

         # add move and not just the node for each node in the list
        for move in sortedlist:
            returnlist.append(move.move)

        return returnlist  # return the list

    # Calculates the utility of the board. Adds up all the pieces of the AI and subtracts other peices
    def utility(self, board):

        ##Adds all the black coordinates for all the pieces
        total = len(board.pieces(chess.BISHOP, chess.BLACK)) + len(board.pieces(chess.PAWN, chess.BLACK)) + \
                len(board.pieces(chess.KING, chess.BLACK)) + len(board.pieces(chess.QUEEN, chess.BLACK)) + \
                len(board.pieces(chess.ROOK, chess.BLACK)) + len(board.pieces(chess.KNIGHT, chess.BLACK))

        ##subtracts all teh white coordinates for all the pices
        total = total - len(board.pieces(chess.BISHOP, chess.WHITE)) - len(board.pieces(chess.PAWN, chess.WHITE)) - \
                len(board.pieces(chess.KING, chess.WHITE)) - len(board.pieces(chess.QUEEN, chess.WHITE)) - \
                len(board.pieces(chess.ROOK, chess.WHITE)) - len(board.pieces(chess.KNIGHT, chess.WHITE))

        return total  # return total value

