# MCTS
MCTS applied to Go

TODO

Rajouter comme heuristique, ne pas jouer dans un oeil OK

Retirer le pass , il crée des problèmes  : si plus de moves possible -> pass, si 2 pass ->over OK


Another problem : si j'ai un oeil pour noir, je teste le move pour blanc, il est invalide, je le retire, plus tard j'ai encerlé le groupe noir, mais je ne peux plus jouer l'oeil vu qu'il a été retiré,
il faudrait le retirer d'une liste temporaire pas de l'original IMPORTANT ->TOujours à corriger ce problème là :

221111222
2.211112.<-------- il faudrait que 2 puisse passer pour permettre à noir de jouer voir le roll out
222111222
221111112
.21121111
222121.1.
222221111
222.221.1
.2.22111.


Pour le problème précédent, plutot garder les moves supprimés et quand un move trouvé, le remettre

Verifier que le getwinner renvoie correctement


