#Pedro Esteves 83541 Tomas Silva 83862 Grupo 99 Alameda
import copy
from search import*
from utils import*

# TAI content
#e devera ser algo deste genero: M[x][y]
#Uma posicao da matriz para saber se esta vazia ou preenchida.
def c_peg ():
 return "O"
def c_empty ():
 return "_"
def c_blocked ():
 return "X"
def is_empty (e):
 return e == c_empty()
def is_peg (e):
 return e == c_peg()
def is_blocked (e):
 return e == c_blocked()


#Isto deve dar jeito quando precisarmos de saber as posicoes
#adjacentes a uma celula.
 # TAI pos
# Tuplo (l, c)
def make_pos (l, c):
 return (l, c)
def pos_l (pos):
 return pos[0]
def pos_c (pos):
 return pos[1]

 # TAI move
#um move tem a posicao inicial e final.
# Lista [p_initial, p_final]
def make_move (i, f):
 return [i, f]
def move_initial (move):
 return move[0]
def move_final (move):
 return move[1]

def board_perform_move(board,move):
    actualPos = move[0]
    nextPos = move[1]
    direc = ""                                     #Da a direccao do movimento

    if (pos_l(actualPos) == pos_l(nextPos)):       #O eixo x e igual
        tmp = pos_c(nextPos) - pos_c(actualPos)    #Significa que moveu-se para baixo.
        if tmp == 2 :
            direc = "D"
        elif tmp == -2:
            direc = "E"
    else:
        tmp = pos_l(nextPos) - pos_l(actualPos)
        if tmp == 2 :
            direc = "B"
        elif tmp == -2:
            direc = "C"

    return update_board(board,actualPos,direc)

def update_board(b,actualPos,dir):

    b[pos_l(actualPos)][pos_c(actualPos)] = "_"             #Apagar a bola da posicao onde ela estava.
    if dir == "D":
        b[pos_l(actualPos)][pos_c(actualPos) + 1 ] = "_"    #Apagar a bola por onde vai dar o salto.
        b[pos_l(actualPos)][pos_c(actualPos) + 2 ] = "O"    #Fazer aparecer a bola na nova posicao.

    elif dir == "E":
        b[pos_l(actualPos)][pos_c(actualPos) - 1 ] = "_"    #Apagar a bola por onde vai dar o salto.
        b[pos_l(actualPos)][pos_c(actualPos) - 2 ] = "O"    #Fazer aparecer a bola na nova posicao.
    elif dir == "B":
        b[pos_l(actualPos) +1][pos_c(actualPos)] = "_"      #Apagar a bola por onde vai dar o salto.
        b[pos_l(actualPos) +2][pos_c(actualPos)] = "O"      #Fazer aparecer a bola na nova posicao.
    else:
        b[pos_l(actualPos) -1][pos_c(actualPos)] = "_"   #Apagar a bola por onde vai dar o salto.
        b[pos_l(actualPos) -2][pos_c(actualPos)] = "O"   #Fazer aparecer a bola na nova posicao.

    return b;


#Mudar a estrategia de procura. Antes estava a ver todas as celulas e os seus vizinhos para
#ver se havia movs disponiveis, a forma eficiente e considerar apenas as celulas vazias e ver se ha algum move
#que va para la.
def board_moves(b):
    contador = 0
    moves = []
    for x in range(0,len(b)):
        for y in range(0, len(b[x])):
            tmp = []
            if is_empty(b[x][y]):
                tmp = get_moves((x,y),b)             #Guarda em tmp os movs possiveis a partir de uma celula.
                if len(tmp) != 0 :
                    for z in range(0,len(tmp)):
                        move = [tmp[z],make_pos(x,y)]
                        moves.append(move)
    return moves

#Devolve os moves de uma celula.
#Apenas retorna 0 se nao houver moves validos
def get_moves(cell,board):
    moves = []
    tmp = get_left_moves(cell,board)
    if tmp != 0:
        moves.append(tmp)
    tmp = get_right_moves(cell,board)
    if tmp != 0:
        moves.append(tmp)

    tmp = get_top_moves(cell,board)
    if tmp != 0:
        moves.append(tmp)

    tmp = get_down_moves(cell,board)
    if tmp != 0:
        moves.append(tmp)
    return moves


#Lembrar que a cell e a cell destino (Por isso para entrar aqui ja sabemos que esta vazia).
#Portanto o move da esquerda e um salto da esquerda para a cell.
#O move da direita e um salto da direita para a cell.
#O move do top e um salto de cima para a a cell.
#O move do down e um salto de baixo para a cell.
def get_left_moves(cell,board):
    if pos_c(cell) >= 2  \
    and is_peg(board[pos_l(cell)][pos_c(cell) -1]) and is_peg(board[pos_l(cell)][pos_c(cell) -2]):
        return make_pos(pos_l(cell),pos_c(cell)-2)
    return 0


def get_right_moves(cell,board):
    if pos_c(cell) < len(board[0]) - 2 \
     and is_peg(board[pos_l(cell)][pos_c(cell) + 1]) and is_peg(board[pos_l(cell)][pos_c(cell)+2]):
        return make_pos(pos_l(cell),pos_c(cell)+2)
    return 0

def get_top_moves(cell,board):
    if pos_l(cell) >= 2 \
     and is_peg(board[pos_l(cell) -1][pos_c(cell)]) and is_peg(board[pos_l(cell) -2][pos_c(cell)]):
        return make_pos(pos_l(cell) -2 ,pos_c(cell))
    return 0

def get_down_moves(cell,board):
    if pos_l(cell) < len(board) -2 \
     and is_peg(board[pos_l(cell) +1][pos_c(cell)]) and is_peg(board[pos_l(cell) +2][pos_c(cell)]):
        return make_pos(pos_l(cell) +2 ,pos_c(cell))
    return 0


#Um estado deve ser representado por uma classe com pelo menos um
#slot chamado board em que é armazenada a configuração do tabuleiro
#a que o estado corresponde.
class sol_state:

    def __init__(self,board):
        self.board = board

    def getBoard(self):
        return self.board

    def __lt__(self, other):
        return self.board < other.board


def greedy_search(problem, h=None):
    h = memoize(h or problem.h, 'h')
    return best_first_graph_search(problem, h)


#Note to self: Python OOP has some differences when compared to Java.
#All class methods should have an attribute "self" to indicate that the method belongs
#indeed to the class and not to the function.

#This "(Problem)" is the equivalent to Java "extends".
class solitaire(Problem):

    def __init__(self,board):
        state = sol_state(board)
        super(solitaire, self).__init__(state)


    def actions(self,state):
        return board_moves(state.getBoard())


    def result(self,state,action):
       tmp = copy.deepcopy(state.getBoard())
       res = board_perform_move(tmp,action)
       return sol_state(res)


    def h(self,node):

        b = node.state.board
        counter = 0
        preCounter = 0
        n_col = len(b[0]) -1       #index max colunas
        n_lin = len(b) -1          #index max linhas



        #Boards que geram mais moves sao melhores que
        #Boards que nao geram moves.
        filhosMoves = board_moves(b)
        preCounter = - 1 * len(filhosMoves)

#-------------------------------------------------------------

        for x in range(0, n_col):

            #linha de cima
            if(b[0][x]) == "O":
                counter += 1
                
            #Segunda linha.
            #Estes "O" vao ser ainda mais dificeis de remover
            #Porque isso sofrem uma penalizacao ainda maior.
            if(b[0][x]) == "X":
                if(b[1][x]) == "O":
                    counter += 1

            #linha de baixo
            if(b[n_lin][x]) == "O":
                counter += 1
                
            if(b[n_lin][x]) == "X":
                if(b[n_lin-1][x]) == "O":
                    counter += 1

        #Pecas nos cantos sao piores para remover
        #por isso sao penalizadas.
        for y in range(0,n_lin):

            #linha da direita
            if(b[y][n_col]) == "O":
                counter += 1
                
            if(b[y][n_col]) == "X":
                if(b[y][n_col-1]) == "O":
                    counter += 1

            #linha da esquerda
            if(b[y][0]) == "O":
                counter += 1
            
            if(b[y][0]) == "X":
                if(b[y][1]) == "O":
                    counter += 1


        #Tabuleiros com menos pecas "O" sao melhores.
        posCounter = 0
        for x in range(0,n_lin):
            for y in range(0, n_col):
                if b[x][y] != "O":
                    posCounter -=1

        #Sao dadas diferentes ponderacoes as sub-heuristicas 
        #para a heuristica composta "res"
        res =  counter*1.5 +  preCounter + posCounter*2 

        return res



    #Esta no enunciado e foi relembrado numa aula pratica
    #que uma configuracao do board e solucao se apenas tiver uma peca.
    def goal_test(self, state):
        count = 0;
        for x in range(0,len(state.getBoard())):
            for y in range(0,len(state.getBoard()[0])):
                if is_peg(state.getBoard()[x][y]):
                    count+=1;

        #Se so sobra uma peca entao e pq a solucao foi achada
        if count == 1 :
            return True
        return False
#