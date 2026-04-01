awk '
BEGIN{ FS=","}
{
$4=="Tic-Tac-Toe" {tw[$1]+=1;tl[$2]+=1;tu[$1]=0;tu[$2]=0}
$4=="Othello" {ow[$1]+=1;ol[$2]+=1;tu[$1]=0;tu[$2]=0}
$4=="Connect4" {cw[$1]+=1;cl[$2]+=1;tu[$1]=0;tu[$2]=0}

}
END{}
