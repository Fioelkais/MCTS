__author__ = 'tvandermosten'

def gtptoint(letter,number):
    x=19-number
    y= ord(letter)-65
    if(y>7):
        y=y-1
    return(x,y)


def inttogtp(x,y):
    if(y>=8):
        y=y+1
    letter=chr(y+65)
    number=19-x
    return(letter,number)