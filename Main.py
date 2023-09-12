#find all possible moves in the position
#Evaluate them to see if they win/lose material
#figure out how to get legal moves

#how to get depth=1
#finish-by adding visual  display
#first photopea
#then blit board
#then compare if move is in legal moves
#finish class square
#finish castling
import chess
import random
import pygame
w=600
square_size=560/8
class Square:
    def __init__(self,square,image):
        self.square=square
        self.xbound=(ord(square[0])-97)*square_size+20
        self.ybound=(8-square[1])*square_size+20
        self.image=image
WK=pygame.transform.scale(pygame.image.load('WK.png'), (square_size,square_size))
WQ=pygame.transform.scale(pygame.image.load('WQ.png'), (square_size,square_size))
WB=pygame.transform.scale(pygame.image.load('WB.png'), (square_size-10,square_size-10))
WKN=pygame.transform.scale(pygame.image.load('WKN.png'), (square_size,square_size))
WP=pygame.transform.scale(pygame.image.load('WP.png'), (square_size,square_size))
WR=pygame.transform.scale(pygame.image.load('WR.png'), (square_size,square_size))

BK=pygame.transform.scale(pygame.image.load('BK.png'), (square_size,square_size))
BQ=pygame.transform.scale(pygame.image.load('BQ.png'), (square_size,square_size))
BB=pygame.transform.scale(pygame.image.load('BB.png'), (square_size,square_size))
BKN=pygame.transform.scale(pygame.image.load('BKN.png'), (square_size,square_size))
BP=pygame.transform.scale(pygame.image.load('BP.png'), (square_size,square_size))
BR=pygame.transform.scale(pygame.image.load('BR.png'), (square_size,square_size))
squares={Square(("a",1),WR),Square(("b",1),WKN),Square(("c",1),WB),Square(("d",1),WQ),Square(("e",1),WK),Square(("f",1),WB),Square(("g",1),WKN),Square(("h",1),WR),Square(("a",8),BR),Square(("b",8),BKN),Square(("c",8),BB),Square(("d",8),BQ),Square(("e",8),BK),Square(("f",8),BB),Square(("g",8),BKN),Square(("h",8),BR)}
for i in range(1,9):
    squares.add(Square((chr(96+i),2),WP))
    squares.add(Square((chr(96+i),7),BP))
for i in range(3,7):
    for j in range(8):
        squares.add(Square((chr(97+j),i),None))
Board=pygame.transform.scale(pygame.image.load('chessboard.png'), (w,w))
def MaterialBalance(pos):
    whiteMaterial=0
    blackMaterial=0
    for square in range(64):
        piece=pos.piece_at(square)
        if piece:
            if piece.color:
                if piece.piece_type==1:
                    whiteMaterial+=10
                    
                    if square>=48 and square<56:
                        whiteMaterial+=5
                    if square>=40 and square<48:
                        whiteMaterial+=2
                    if square==27 or square==28:
                        whiteMaterial+=2
                    if square==35 or square==36:
                        whiteMaterial+=2.5
                    if square==11 or square==12:
                        whiteMaterial-=2
                    
                if piece.piece_type==2:
                    whiteMaterial+=30
                    if (square>=0 and square<8) or (square>=56):
                        whiteMaterial-=3
                    for i in range(0,8):
                        if square==i*8:
                            whiteMaterial-=3
                        if square==i*8+7:
                            whiteMaterial-=3
                if piece.piece_type==3:
                    whiteMaterial+=30
                if piece.piece_type==4:
                    whiteMaterial+=50
                    if square>=48 and square<56:
                        whiteMaterial+=1
                if piece.piece_type==5:
                    whiteMaterial+=90
                if piece.piece_type==6:
                    whiteMaterial+=900
                    if square>=16:
                        whiteMaterial-=3
                    if square==0 or square==1 or square==6 or square==7 or square==8 or square==9 or square==14 or square==15:
                        whiteMaterial+=2
            else:
                if piece.piece_type==1:
                    blackMaterial+=10
                    if square>=8 and square<16:
                        blackMaterial+=5
                    if square==35 or square==36:
                        blackMaterial+=2
                    if square==28 or square==29:
                        blackMaterial+=2.5
                    if square>=16 and square<24:
                        blackMaterial+=2
                    if square==51 or square==52:
                        blackMaterial-=2
                if piece.piece_type==2:
                    blackMaterial+=30
                    if (square>=0 and square<8) or (square>=56):
                        blackMaterial-=3
                    for i in range(0,8):
                        if square==i*8:
                            blackMaterial-=3
                        if square==i*8+7:
                            blackMaterial-=3
                if piece.piece_type==3:
                    blackMaterial+=30
                if piece.piece_type==4:
                    blackMaterial+=50
                    if square>=8 and square<16:
                        blackMaterial+=1
                if piece.piece_type==5:
                    blackMaterial+=90
                if piece.piece_type==6:
                    blackMaterial+=900
                    if square<47:
                        blackMaterial-=3
                    for i in range(2):
                        if square==8*i or square==1+8*i or square==6+8*i or square==7+8*i:
                            blackMaterial+=2
    return whiteMaterial-blackMaterial

def randomMove():
    return random.choice(legalmoves)

class SearchTree():
    def __init__(self,pos):
        self.tree=[pos]
        self.continuations=[]

def depth1Algo(pos):
    eval=None
    bestmove=None
    legalmoves=list(pos.legal_moves)
    moves=captures+rest
    for move in legalmoves:
        if eval==None:
            board.push(move)
            eval=MaterialBalance(pos)/10
            board.pop()
            bestmove=move
        if board.turn:
            board.push(move)
            evalOfMove=MaterialBalance(pos)
            if eval<evalOfMove:
                eval=MaterialBalance(pos)
                bestmove=move
        else:
            board.push(move)
            evalOfMove=MaterialBalance(pos)
            if eval>evalOfMove:
                eval=MaterialBalance(pos)
                bestmove=move
        board.pop()
    return (bestmove,eval)
def minimax(pos,depth, maxPlayer,alpha,beta):
    if depth==0:
        eval=MaterialBalance(pos)/10
        return (eval,[])
    legalmoves=list(pos.legal_moves)
    bestMoves=[]
    if maxPlayer:
        bestEval=-1000
        for move in legalmoves:
            pos.push(move)
            """h=hash(pos.board_fen())
            if h in hashes:
                break
            else:
                hashes.add(hash)"""
            Res=minimax(pos, depth-1, not maxPlayer,alpha,beta)
            moveEval=Res[0]
            moveMoves=Res[1]
            if bestEval<moveEval:
                bestEval=moveEval
                bestMoves=[move]+moveMoves
            pos.pop()
            if bestEval>=beta:
                break
            alpha=max(alpha, bestEval)
        if not legalmoves:
            bestEval=0
        return (bestEval,bestMoves)
    else:
        bestEval=1000
        for move in legalmoves:
            pos.push(move)
            h=hash(pos.board_fen())
            """if h in hashes:
                break
            else:
                hashes.add(hash)"""
            Res=minimax(pos, depth-1, not maxPlayer, alpha, beta)
            moveEval=Res[0]
            moveMoves=Res[1]
            if bestEval>moveEval:
                bestEval=moveEval
                bestMoves=[move]+moveMoves
            pos.pop()
            if bestEval<=alpha:
                break
            beta=min(beta,bestEval)
        if not legalmoves:
            bestEval=0
        return (bestEval,bestMoves)
if __name__=='__main__':
    pygame.init()
    board=chess.Board()
    hashes=set()
    
    #board.push(chess.Move.from_uci('e2e4'))
    Game=True
    screen=pygame.display.set_mode((w,w))
    selected=None
    while Game:
        screen.blit(Board,(0,0))
        green=(0,255,0)
        if selected:
            screen.fill(green,(selected.xbound,selected.ybound,square_size,square_size))
        for i in squares:
            if i.image:
                screen.blit(i.image,(i.xbound,i.ybound))
        for event in pygame.event.get():
            if event.type==pygame.MOUSEBUTTONUP:
                #print(selected)
                mousePos=pygame.mouse.get_pos()
                for i in squares:
                    if mousePos[0]>i.xbound and mousePos[0]<i.xbound+square_size and mousePos[1]>i.ybound and mousePos[1]<i.ybound+square_size:
                        loc=i.square
                        legalmoves=list(board.legal_moves)
                        if selected:
                            if loc==selected.square:
                                selected=None
                                break
                            promotion=False
                            smove=str(selected.square[0]+str(selected.square[1])+loc[0]+str(loc[1]))
                            move=chess.Move.from_uci(smove)
                            pmove=smove+"q"
                            pmove=chess.Move.from_uci(pmove)
                            if pmove in legalmoves:
                                move=pmove
                                promotion=True
                                
                            #print(move in legalmoves)
                            #print(legalmoves)
                            if move in legalmoves:
                                Kcastling=False
                                if smove[0]=="e" and smove[2]=="g" and selected.image==WK:
                                    Kcastling=True
                                if Kcastling:
                                    for s in squares:
                                        if s.square[0]=="h" and s.square[1]==1:
                                            s.image=None
                                        if s.square[0]=="f" and s.square[1]==1:
                                            s.image=WR
                                Qcastling=False
                                if smove[0]=="e" and smove[2]=="c" and selected.image==WK:
                                    Qcastling=True
                                if Qcastling:
                                    for s in squares:
                                        if s.square[0]=="a" and s.square[1]==1:
                                            s.image=None
                                        if s.square[0]=="d" and s.square[1]==1:
                                            s.image=WR
                                i.image=selected.image
                                if promotion:
                                    i.image=WQ
                                selected.image=None
                                board.push(move)
                                CM=minimax(board,4,False,-1000,1000)
                                try:
                                    CM=CM[1][0]
                                except:
                                    print("Game Over")
                                    Game=False
                                    break
                                ComputerMove=CM.uci() #string
                                promotion=False
                                if len(ComputerMove)==5:
                                    promotion=True
                                #print(ComputerMove[1])
                                for i in squares:
                                    if i.square[0]==ComputerMove[0] and i.square[1]==int(ComputerMove[1]):
                                        selected=i
                                        break
                                for i in squares:
                                    if i.square[0]==ComputerMove[2] and i.square[1]==int(ComputerMove[3]):
                                        i.image=selected.image
                                        selected.image=None
                                        if promotion:
                                            i.image=BQ
                                        break
                                Kcastling=False
                                if smove[0]=="e" and smove[2]=="g" and selected.image==BK:
                                    Kcastling=True
                                if Kcastling:
                                    for s in squares:
                                        if s.square[0]=="h" and s.square[1]==8:
                                            s.image=None
                                        if s.square[0]=="f" and s.square[1]==8:
                                            s.image=BR
                                Qcastling=False
                                if smove[0]=="e" and smove[2]=="c" and selected.image==BK:
                                    Qcastling=True
                                if Qcastling:
                                    for s in squares:
                                        if s.square[0]=="a" and s.square[1]==8:
                                            s.image=None
                                        if s.square[0]=="d" and s.square[1]==8:
                                            s.image=BR
                                board.push(CM)
                            selected=None
                        else:
                            if i.image:
                                selected=i
                                
            if event.type== pygame.QUIT:
                Game=False
        pygame.display.update()
        
    #searchTree=SearchTree(board)
    #print(depth1Algo(board))
    #print(minimax(board,4,True,-1000,1000))
    #next implement castling for bot
