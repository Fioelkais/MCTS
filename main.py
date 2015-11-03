import cmd
from convert import *
from GS import *
from init import *
class Prompt(cmd.Cmd):
    prompt = ''

    a=GoState(4)
    size=4
    komi=6.5
    a.points2=komi

    # ----- basic turtle commands -----
    def do_printsomething(self, arg):
        'Move the turtle forward by the specified distance:  FORWARD 10'
        print(arg)


    def do_bye(self, arg):
        'Stop recording, close the turtle window, and exit:  BYE'
        print('Thank you for using Turtle')
        return True

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
        print(arg)
        test=arg.split(" ")
        print(test[0])
        print(test[1])
        letter = ''.join([i for i in test[1] if not i.isdigit()])
        print (letter)
        number = ''.join([i for i in test[1] if i.isdigit()])
        print (number)
        print(gtptoint(letter,int(number)))
        if test[0]=="B":
            self.a.playerJustMoved=2
            self.a.DoMove(gtptoint(letter,int(number)))
        if test[0]=="W":
            self.a.playerJustMoved=1
            self.a.DoMove(gtptoint(letter,int(number)))
        print('='+'\n')

    def do_genmove(self,arg):
        if(arg=='w'):
            self.a.playerJustMoved=1
            move=UCT(rootstate = self.a, itermax = 1, verbose = False)
            self.a.DoMove(move)
            result = inttogtp(move[0],move[1])
            result2 =str(result[0])+str(result[1])
            print('= '+result2 +'\n')
        if (arg=='b'):
            self.a.playerJustMoved=2
            move=UCT(rootstate = self.a, itermax = 1, verbose = False)
            self.a.DoMove(move)
            result=inttogtp(move[0],move[1])
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
        print('= MCTSTV')
        print('')

    def do_protocol_version(self,arg):
        print('= 2')
        print('')

    def do_list_commands(self,arg):
        print('= genmove'+ '\n' +'genmove_black'+ '\n'+'genmove_white'+ '\n'+'black'+ '\n'+'white'+ '\n'+'play'+ '\n'+'version'+ '\n'+'name'+ '\n'+'boardsize'+ '\n'+'clear_board'+ '\n')

if __name__ == '__main__':
    Prompt().cmdloop()