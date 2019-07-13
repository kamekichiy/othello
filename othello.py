# coding: utf-8

# -------------------------------------------------------------
#  import section
# -------------------------------------------------------------

    # None

# -------------------------------------------------------------
#  Class section
# -------------------------------------------------------------

class Board:
    '''オセロのボード（板）を司るクラス。

    ボードにある石の状態を記憶し、移動する。
    棋譜を記録する。
    その石が置けるのか。結果、どちらが勝ったのか判断する機能も持つ。
    '''

    black = 1
    white = 2
    space = 0
    outside = 3



    def __init__(self):
        ''' ボードの初期化

        record list 棋譜を記録する
        moves int 何手目なのか
        position list ボードの各位置の状態
                0 空
                1 黒の石がある
                2 白の石がある
                3 ボードの外側
        '''
        self.record = []
        self.moves = 0
        self.area = [
            3, 3, 3, 3, 3, 3, 3, 3, 3, 3,
            3, 0, 0, 0, 0, 0, 0, 0, 0, 3,
            3, 0, 0, 0, 0, 0, 0, 0, 0, 3,
            3, 0, 0, 0, 0, 0, 0, 0, 0, 3,
            3, 0, 0, 0, 2, 1, 0, 0, 0, 3,
            3, 0, 0, 0, 1, 2, 0, 0, 0, 3,
            3, 0, 0, 0, 0, 0, 0, 0, 0, 3,
            3, 0, 0, 0, 0, 0, 0, 0, 0, 3,
            3, 0, 0, 0, 0, 0, 0, 0, 0, 3,
            3, 3, 3, 3, 3, 3, 3, 3, 3, 3,
            ]



    def put(self,color, position):
        '''positionに石を置き、石に挟まれた物をひっくり返す。

        Parameters
        ----------
        color : int
            置きたい石の色
        position : int
            置きたい場所 (0 ~ 99)

        Returns
        -------
        bool
            True 成功, False それ以外
        '''
        poslist = self.can_put(color,position)
        if len(poslist) == 0:
            return False
        else:
            self.area[position] = color
            for i in poslist:
                self.area[i] = color
            return True



    def can_put(self,color, position):
        """positionで指定したところに、colorの石が置けるのか判定する。

        Parameters
        ----------
        color : int
            置きたい石の色
        position : int
            置きたい場所 (0 ~ 99)

        Returns
        -------
        list
            置くことができるとき、返すことができる石の位置をlistで応答。置けないときは空のlist
        """

        """置くことができる場所のリストを初期化"""
        putableList = []

        """先ずはそこは空きなのか"""
        if self.area[position] != 0 or self.area[position] == 3:
            return putableList   #カラッポを応答

        """八方を順に調べる
        
            順に調べた結果を、putableListに追加していく
        """
        for i in range(8):
            putableList.extend(self.sub_can_put(color,position,i))

        """調べ終わったら結果を応答する"""
        return putableList



    def sub_can_put(self,color, position,direction):
        """ positionで指定したところに、colorの石が置けるのか,directionの方向のみ判定する。

            can_putからのみ呼ばれることを前提としている。
            positionで指定したところは、カラっぽではないはず。

        Parameters
        ----------
        color : int
            置きたい石の色
        position : int
            置きたい場所 (0 ~ 99)
        direction
            調査したい方向
            0:上 1:右上 2: 右 3:右下 4:下 5:左下 6:左 7:左上

        Returns
        -------
        list
            置くことができるとき、返すことができる石の位置をlistで応答。置けないときは空のlist

        """
        me = color
        if me == 1:  #black
            you = 2
        else:
            you = 1

        putableList = []

        """移動するときの差分を設定"""
        if direction == 0:
            diff = -10
        elif direction == 1:
            diff = -9
        elif direction == 2:
            diff = 1
        elif direction == 3:
            diff = 11
        elif direction == 4:
            diff = 10
        elif direction == 5:
            diff = 9
        elif direction == 6:
            diff = -1
        elif direction == 7:
            diff = -11
        else:       #変な値を指定してきたらカラっぽ返す
            return putableList

        """差分の一つ目、つまりdirectionで指定した隣の色を判定し、対戦相手の色なら先に行く
            それ以外なのならカラッポのリストを応答して終わり"""
        for i in range(1,8):

            j = position + diff * i
            if j > 99 or i < 0 :
                return []

            if self.area[j] == you:
                putableList.append(j)
            elif self.area[j] == me:
                break
            else:
                putableList = []
                break

        return putableList



    def decision_winner(self):
        """黒と白のどちらが勝ったのか判定する。
        ゲームが終わっているかどうかは関係なく。石の多いほうを応答する。

        Returns
        -------
        int
            1 黒の勝ち, 2 白の勝ち
        """
        pass

    def decision_color(self, color):
        """パラメータで指定した石が置ける場所はあるのか(パスなのか)判定する。

        Parameters
        ----------
        color : int
            置きたい石の色
        Returns
        -------
        bool
            True 置ける, False パス

        """
        for i in range(100):
            if self.can_put(color,i):
                return True

        return False

    def an(self,a1):
        """ a1形式で指定した石の位置を、配列へと変換する。

        Parameters
        ----------
        a1 : str
            ボード上の場所をa1形式で指定する
        Returns
        -------
        int
            変換後の配列の値

        """
        alphabet = {"a":1,"b":2,"c":3,"d":4,"e":5,"f":6,"g":7,"h":8}

        str1=a1[0]
        str2=a1[1]

        return int(alphabet[str1]) + int(str2) * 10

    def na(self,num):
        """ 配列の数字を、a1形式へと変換する。

        Parameters
        ----------
        num : int
            ボード上の場所を配列で指定する
        Returns
        -------
        str
           変換後のa1形式の値
        """
        alphabet = [None,"a","b","c","d","e","f","g","h",None]

        return  alphabet[num % 10] + str(num/10)


class Player:
    """ オセロのプレーヤー

    Attributes
    ----------
    color : int
        プレーヤーの石の色
    species : int
        プレーヤーの種族 1 人間, 2 コンピュータ
    """

    def __init__(self, color, species):
        self.color = color
        self.species = species

class Human(Player):
    """ 「人間」のプレーヤー

    人間のプレーヤー用のコードをここに書く
    """

    def put_stone(self, board):
#        print("Human is put", self.color)
        while True:
            s = str(input("どこに石を置きますか : "))

            if s[0] in ("a", "b", "c", "d", "e", "f", "g", "h") \
                and int(s[1]) in range(1,9):
                return board.an(s)
            else:
                print("a1 の形式で入力してください。")



class Computer(Player):
    """ 「コンピュータ」のプレーヤー

    コンピュータのプレーヤー用のコードをここに書く
    """

    def put_stone(self, board):
        print("Computer is put", self.color)



def display_board(board):
    """boardをコンソールへ出力する

    Parameters
    ----------
    board
        出力したいBoardクラス
    Returns
    -------
        なし
    """
    displayHeader()
    for n in range(1,9):
        displayLine(board, n)
    displayFooter()

def displayHeader():
    print("")
    print("   - othello -")
    print("  a b c d e f g h ")

def displayLine(board, l):
    p = l * 10 + 1
    line = "%d %s %s %s %s %s %s %s %s" % (l,
                                           getStone(board.area[p]),
                                           getStone(board.area[p + 1]),
                                           getStone(board.area[p + 2]),
                                           getStone(board.area[p + 3]),
                                           getStone(board.area[p + 4]),
                                           getStone(board.area[p + 5]),
                                           getStone(board.area[p + 6]),
                                           getStone(board.area[p + 7]))
    print(line)

def displayFooter():
    print("")


def getStone(i):
    if i == 1:
        return "●"
    elif i == 2:
        return "◯"
    else:
        return "_"

def display_menu():
    """オセロのメニューを出力する

    Returns
    -------
    nothing
    """

    print("")
    print("### Othello ####################################")
    print("")
    print("- menu -")
    print("1. 黒:人間      vs 白:人間")
    print("2. 黒:人間　　　 vs 白:プログラム")
    print("3. 黒:プログラム vs 白:人間")
    print("4. 黒:プログラム vs 白:プログラム")
    print("q. 終了")
    print("")
    print("#################################################")
    print("")
    print('ゲームを開始するときは「1〜4」を選んでください。')
    print('ゲームを終了するときは「Q」を選んでください。')
    print("")


def menu():
    """オセロのメニューを出力して、選択結果を応答する。

    Returns
    -------
    m : str
    メニューの選択結果
    """

    m = 0

    while True:
        display_menu()
        m = str(input("選択してください : "))
        if m in ("1", "2", "3", "4", "q"):
            return m
        else:
            print("1,2,3,4 のどれかを入力してください。")
            print("終了するには　q を入力してください。")


def game_loop(player1, player2):
    """オセロゲームのメインとなるループ

    各プレーヤーが交互に手を打ち、最終的に打てるところがなくなるまでループする。

    Parameters
    ----------
    player1 : object Player
        黒担当のプレーヤー
    player2 : object Player
        白担当のプレーヤー

    Returns
    -------
    Nothing

    """

    black = 1
    white = 2

    man = 1
    pc = 2

    turn = 1

    board = Board()
    p1 = player1
    p2 = player2

    while True:
        display_board(board)
        print("次は %s の番です。" % getStone(turn))
        if turn == black:
            if board.decision_color(black):
                while True:
                    pos = p1.put_stone(board)
                    if board.can_put(black, pos):
                        board.put(p1.color, pos)
                        break
            else:
                if board.decision_color(white):
                    continue
                else:
                    game_over()
            turn = white
        else:
            if board.decision_color(white):
                while True:
                    pos = p1.put_stone(board)
                    if board.can_put(white, pos):
                        board.put(p2.color, pos)
                        break
            else:
                if board.decision_color(black):
                    continue
                else:
                    game_over()
            turn = black

def game_over():
    print("GameOver")
    exit()

def player_call(s):

    if s == "1" :
        p1 = Human(1,1)
        p2 = Human(2,1)
        return p1, p2
    elif s == "2":
        p1 = Human(1,1)
        p2 = Computer(2,1)
        return p1, p2
    elif s == "3":
        p1 = Computer(1,1)
        p2 = Human(2,1)
        return p1, p2
    elif s == "4":
        p1 = Computer(1,1)
        p2 = Computer(2,1)
        return p1, p2
    else:
        return None, None

def start():
    mode = menu()
    if mode in ("1", "2", "3", "4"):
        player1, player2 = player_call(mode)
        game_loop(player1, player2)
    else:
        exit()


def main():

    start()


if __name__ == "__main__":
    # execute only if run as a script
    main()


# end of code.
