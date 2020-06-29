import tkinter as tk

class run():
    def __init__(self, root,board_view,seq_label,turn_label,board_label,result_label,possible_cell_list_label,judge_label\
                ,message_label,board,turn,seq,result,possible_cell_list,judge,message):
        self.root=root
        self.board_view=board_view
        self.seq_label=seq_label
        self.turn_label=turn_label
        self.board_label=board_label
        self.result_label=result_label
        self.possible_cell_list_label=possible_cell_list_label
        self.judge_label=judge_label
        self.message_label=message_label
        self.board=board
        self.turn=turn
        self.seq=seq
        self.result=result
        self.possible_cell_list=possible_cell_list
        self.judge=judge
        self.message=message
        self.root = root
        self.board_view = None
        self.seq_label = None
        self.turn_label = None
        self.board_label = None
        self.result_label = None
        self.possible_cell_list_label = None
        self.judge_label = None
        self.message_label = None
        self.board = None
        self.turn = 0
        self.seq = 1
        self.result = None
        self.possible_cell_list = None
        self.judge = None
        self.message = None
    def init_globals(self):
        self.board = [i for i in range(1,10)]
        self.turn = 0
        self.seq = 1
        self.result = []
        self.possible_cell_list = [i for i in range(1,10)]
        self.judge = "未定"
        self.message = ""
    def get_stone_by_turn(self):
        return( "○" if self.turn == 0 else "×" )
    def changed(self):
        self.seq_label[ "text" ] = f"手数 = {self.seq}"
        self.turn_label[ "text" ] ="手番 = {}".format( self.get_stone_by_turn() )
        self.board_label[ "text" ] = f"内部表現 = {self.board}"
        self.result_label[ "text" ] = f"三連箇所の検索結果 = {self.result}"
        self.possible_cell_list_label[ "text" ] = \
                                  f"  着手可能なセル = {self.possible_cell_list}"
        self.judge_label[ "text" ] = f"勝敗判定 = {self.judge}"
        self.message_label[ "text" ] = f"{self.message}"

    def is_int( self,data ):
        return( isinstance( data, int ) )

    def is_blank( self,position ):
        return( position >= 1 and position <=9 and self.is_int( self.board[position-1] ) )

    def toggle_turn(self):
        self.turn = (self.turn + 1) % 2

    def put_stone( self,position ):
        if self.is_blank( position ):
            self.board[position-1] = self.get_stone_by_turn()
            return( True )
        else:
            self.message = "エラー: 既に石が置かれているので，置けません."
            self.changed()
            return( False )

    def pass_turn(self):
        self.message = "  パスをします．"
        self.toggle_turn()
        self.seq += 1
        self.changed()

    def check_row_line( self,row ):
        p = (row-1)*3
        return(self.board[p] == self.board[p+1] == self.board[p+2] )

    def check_col_line( self,col ):
        p = col-1
        return(self.board[col-1] == self.board[3+p] == self.board[6+p] )

    def check_up_and_to_the_right_line(self):
        return(self.board[6] == self.board[4] == self.board[2] )

    def check_down_and_to_the_right_line(self):
        return(self.board[0] == self.board[4] == self.board[8] )

    def check_lines(self):
        self.result = []
        for row in range( 1, 4 ):
            if self.check_row_line( row ):
                self.result.append( f"横({row}行目)" )
        for col in range( 1, 4 ):
            if self.check_col_line( col ):
                self.result.append( f"縦({col}桁目)" )
        if self.check_up_and_to_the_right_line():
            self.result.append( "斜め上" )
        if self.check_down_and_to_the_right_line():
            self.result.append( "斜め下" )
        return( self.result )

    def check_possibilities(self):
        global possible_cell_list
        possible_cell_list = list( filter( self.is_int, self.board  ) )
        return( possible_cell_list )

    def init_root_window(self):
        import tkinter as tk
        self.root = tk.Tk()
        self.root.title( "三目並べ (Tic-Tac-Toe)" )
        self.root.geometry( "320x240+200+100" )
        return( self.root )

    def put_stone_with_seq_control( self,position ):
        if self.result != []:
            self.message = "エラー: 既に勝敗がついているので，石を置けません"
            self.changed()
            return

        if self.put_stone( position ):
            self.message = ""
            self.board_view[ position -1 ]["text"] = self.get_stone_by_turn()
            self.result = self.check_lines()
            self.possible_cell_list = self.check_possibilities()
            if self.result != []:
                self.judge = "!!三目並びました!! → " + self.get_stone_by_turn() + "の勝ち"
            elif possible_cell_list == []:
                self.judge = "!!引き分け!!"
            else:
                self.judge = "未定"
                self.toggle_turn()
                self.seq += 1
            self.changed()
        else:
            self.changed()
    def create_func_put_stone_pos(self, position ):
        def put_stone_positon_fixed():
            self.put_stone_with_seq_control( position )        
        return( put_stone_positon_fixed )

    def init_status_view_frame( self,parent ):

        status_view_frame = tk.Frame( parent )
        status_view_frame.pack( side=tk.TOP )

        self.seq_label = tk.Label( status_view_frame, text="" )
        self.seq_label.grid( row=0, column=0 )
        self.turn_label = tk.Label( status_view_frame,  text="" )
        self.turn_label.grid( row=0, column=1 )
        self.board_label = tk.Label( status_view_frame,  text="" )
        self.board_label.grid( row=2, column=0, columnspan=2 )
        self.result_label = tk.Label( status_view_frame,  text="" )
        self.result_label.grid( row=3, column=0, columnspan=2 )
        self.possible_cell_list_label = tk.Label( status_view_frame, text="" )
        self.possible_cell_list_label.grid( row=4, column=0, columnspan=2 )
        self.judge_label = tk.Label( status_view_frame,  text="" )
        self.judge_label.grid( row=5, column=0, columnspan=2 )
        self.message_label = tk.Label( status_view_frame,  text="" )
        self.message_label.grid( row=6, column=0, columnspan=2 )
        return( status_view_frame )

    def init_board_view_frame( self,parent ):

        board_view_frame = tk.Frame( parent )
        board_view_frame.pack( side=tk.TOP )

        self.board_view = []
        for i in range( 0, 9 ):
            button_title = "　"
            # button_title = str( i + 1 )
            button = tk.Button( board_view_frame, text=button_title,
                                command=self.create_func_put_stone_pos( i + 1 ) )
            button.grid( row=int(i/3), column=i%3 )
            self.board_view.append( button )

        return( board_view_frame )

    def init_view_frame( self,root ):
        view_frame = tk.Frame( self.root )
        view_frame.pack( side=tk.TOP )
        self.init_status_view_frame( view_frame )
        self.init_board_view_frame( view_frame )
        return( view_frame )

    def clear(self):
        self.init_globals()
        self.changed()
        for self.button in self.board_view:
            self.button["text"] = "　"

    def exit (self): 
        self.root.destroy()
    
    def init_control_frame( self,root ):
        control_frame = tk.Frame( self.root )
        control_frame.pack( side=tk.TOP )
        up_button = tk.Button( control_frame, text="パス", command=self.pass_turn )
        up_button.grid( row=0, column=0 )

        clear_button = tk.Button( control_frame, text="クリア", command=self.clear )
        clear_button.grid( row=0, column=1 )

        exit_button = tk.Button( control_frame, text="終了", command=self.exit )
        exit_button.grid( row=0, column=2 )
        return( control_frame )

    def init_components(self):
        self.root = self.init_root_window()
        view_frame = self.init_view_frame( self.root )
        control_frame = self.init_control_frame( self.root )
        self.changed()
go=run(0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0)
def main():
    go.init_globals()
    go.init_components()
    go.root.mainloop()
main()


