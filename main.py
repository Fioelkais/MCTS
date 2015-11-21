import cmd
from convert import *
#from GS import *
from GSUF import*
class Prompt(cmd.Cmd):
    prompt = ''
    file=None
    a=GoState(4)
    size=4
    komi=0
    a.points2=komi

    def do_boardsize(self,arg):
        print('=')
        print('')
        self.a.size=int(arg)
        self.size=int(arg)
        self.a.__init__(self.size)

    def do_clear_board(self,arg):
        print('=')
        print('')
        self.a.__init__(self.size)
        self.a.points2=self.komi

    def do_komi(self,arg):
        print('='+'\n')
        self.komi=int(arg)

    def do_play(self,arg):
        #print(arg)
        test=arg.split(" ")
        #print(test[0])
        #print(test[1])
        if(test[1]=="PASS"):
            if test[0]=="B":
                self.a.playerJustMoved=2
                self.a.DoMove((-1,-1))
            if test[0]=="W":
                self.a.playerJustMoved=1
                self.a.DoMove((-1,-1))
        else:

            letter = ''.join([i for i in test[1] if not i.isdigit()])
            #print (letter)
            number = ''.join([i for i in test[1] if i.isdigit()])
            #print (number)
            #print(gtptoint(letter,int(number)))
            if test[0]=="B":
                self.a.playerJustMoved=2
                self.a.DoMove(self.gtptoint(letter,int(number)))
            if test[0]=="W":
                self.a.playerJustMoved=1
                self.a.DoMove(self.gtptoint(letter,int(number)))
        print('='+'\n')

    def do_genmove(self,arg):
        if(arg=='w'):
            self.a.playerJustMoved=1
            move=UCT(rootstate = self.a, itermax = 1000, verbose = False)
            self.a.DoMove(move)
            result = self.inttogtp(move[0],move[1])
            if result[0]=="@" and result[1]==self.size+1:
                print('= PASS ' +'\n')
            else:
                result2 =str(result[0])+str(result[1])
                print('= '+result2 +'\n')
        if (arg=='b'):
            self.a.playerJustMoved=2
            move=UCT(rootstate = self.a, itermax = 1000, verbose = False)
            self.a.DoMove(move)
            result=self.inttogtp(move[0],move[1])
            if result[0]=="@" and result[1]==self.size+1:
                print('= PASS ' +'\n')
            else:
                result2 =str(result[0])+str(result[1])
                print('= '+result2 +'\n')


    def do_genmove_black(self,arg):
        print('= A1')

    def do_genmove_white(self,arg):
        print('= A1')


    def do_version(self,arg):
        print('= 1')
        print('')

    def do_name(self,arg):
        print('= V-Run')
        print('')

    def do_protocol_version(self,arg):
        print('= 2')
        print('')

    def do_list_commands(self,arg):
        print('= genmove'+ '\n' +'genmove_black'+ '\n'+'genmove_white'+ '\n'+'black'+ '\n'+'white'+ '\n'+'play'+ '\n'+'version'+ '\n'+'name'+ '\n'+'boardsize'+ '\n'+'clear_board'+ '\n')

    def do_quit(self,arg):
        self.close()
        return True

    def gtptoint(self,letter,number):
        x=self.a.size-number
        y= ord(letter)-65
        if(y>7):
            y=y-1
        return(x,y)
    def close(self):
        if self.file:
            self.file.close()
            self.file = None

    def inttogtp(self,x,y):
        if(y>=8):
            y=y+1
        letter=chr(y+65)
        number=self.a.size-x
        return(letter,number)

    def do_EOF(self):
        return True

if __name__ == '__main__':
    Prompt().cmdloop()

