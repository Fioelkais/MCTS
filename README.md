# MCTS
MCTS applied to Go

TODO

Retirer le pass , il crée des problèmes  : si plus de moves possible -> pass, si 2 pass ->over OK
Still problematique ? verifier fin de partie parfois étrange


Redaction :
Bibli
Conclu
Intro ajouter complexité

Expériences :

Tester contre autre bot
tester temps
tester joseki(pour différents nombre iter, calculer le % de bonne décisions)

sur ce joseki :
00120
00122
00120
11222
22220
99% de bon choix : 1,0

cor=0
for i in range (100):
    a=GoState(5)
    a.DoMove((0,2))
    a.DoMove((0,3))
    a.DoMove((1,2))
    a.DoMove((1,3))
    a.DoMove((2,2))
    a.DoMove((2,3))

    a.DoMove((3,0))
    a.DoMove((3,2))
    a.DoMove((3,1))
    a.DoMove((3,3))

    a.playerJustMoved=1
    a.DoMove((4,0))
    a.playerJustMoved=1
    a.DoMove((4,1))
    a.playerJustMoved=1
    a.DoMove((4,2))
    a.playerJustMoved=1
    a.DoMove((4,3))
    a.playerJustMoved=1
    a.DoMove((3,4))
    a.playerJustMoved=1
    a.DoMove((1,4))

    #a.DoMove((2,1))

    m=UCT(rootstate = a, itermax = 1000, verbose = False)
    if m==((1,0)):
        cor+=1
print(cor/100)


Montrer qu'a temps égal, Final bat UFSEt par exemple



