awk '
BEGIN{ FS=","}
{
if($4=="Tic-Tac-Toe") {tw[$1]+=1;tl[$2]+=1;tu[$1]=0;tu[$2]=0}
if($4=="Othello") {ow[$1]+=1;ol[$2]+=1;ou[$1]=0;ou[$2]=0}
if($4=="Connect4") {cw[$1]+=1;cl[$2]+=1;cu[$1]=0;cu[$2]=0}

}
END{

for (g in tu){
        if(tl[g]!=0){printf "%s %d %d %.2f %s\n",g,tw[g],tl[g],tw[g]/tl[g],"Tic-Tac-Toe"}
        if(tl[g]==0){printf "%s %d %d %.2f %s\n",g,tw[g],tl[g],9999,"Tic-Tac-Toe"
}}
for (g in ou){
         if(ol[g]!=0){printf "%s %d %d %.2f %s\n",g,ow[g],ol[g],ow[g]/ol[g],"Othello"}
         if(ol[g]==0){printf "%s %d %d %.2f %s\n",g,ow[g],ol[g],9999,"Othello"
}}
for (g in cu){
        if(cl[g]!=0){printf "%s %d %d %.2f %s\n",g,cw[g],cl[g],cw[g]/cl[g],"Connect4"}
        if(cl[g]==0){printf "%s %d %d %.2f %s\n",g,cw[g],cl[g],9999,"Connect4"
}}
}' history.csv>inter.txt


if [[ $1 == "wins" ]]; then
        sort -nr -k2 inter.txt>sorted.txt
        printf "Tic-Tac-Toe:\n"
        printf "%-10s %-10s %-10s %-10s\n" "UserName" "Wins" "Loses" "w/l ratio"
        awk '{ if($5=="Tic-Tac-Toe")printf "%-10s %-10s %-10s %-10s\n",$1,$2,$3,$4} ' sorted.txt

        printf "Othello:\n"
        printf "%-10s %-10s %-10s %-10s\n" "UserName" "Wins" "Loses" "w/l ratio"
        awk '{ if($5=="Othello")printf "%-10s %-10s %-10s %-10s\n",$1,$2,$3,$4} ' sorted.txt

        printf "Connect4:\n"
        printf "%-10s %-10s %-10s %-10s\n" "UserName" "Wins" "Loses" "w/l ratio"
        awk '{ if($5=="Connect4")printf "%-10s %-10s %-10s %-10s\n",$1,$2,$3,$4} ' sorted.txt

fi
if [[ $1 == "loss" ]]; then
        sort -n -k3 inter.txt>sorted.txt
        printf "Tic-Tac-Toe:\n"
        printf "%-10s %-10s %-10s %-10s\n" "UserName" "Wins" "Loses" "w/l ratio"
        awk '{ if($5=="Tic-Tac-Toe")printf "%-10s %-10s %-10s %-10s\n",$1,$2,$3,$4} ' sorted.txt
        printf "Othello:\n"
        printf "%-10s %-10s %-10s %-10s\n" "UserName" "Wins" "Loses" "w/l ratio"
        awk '{ if($5=="Othello")printf "%-10s %-10s %-10s %-10s\n",$1,$2,$3,$4} ' sorted.txt
        printf "Connect4:\n"
        printf "%-10s %-10s %-10s %-10s\n" "UserName" "Wins" "Loses" "w/l ratio"
        awk '{ if($5=="Connect4")printf "%-10s %-10s %-10s %-10s\n",$1,$2,$3,$4} ' sorted.txt
fi
if [[ $1 == "ratio" ]]; then
        sort -nr -k4 inter.txt>sorted.txt
        printf "Tic-Tac-Toe:\n"
        printf "%-10s %-10s %-10s %-10s\n" "UserName" "Wins" "Loses" "w/l ratio"
        awk '{ if($5=="Tic-Tac-Toe")printf "%-10s %-10s %-10s %-10s\n",$1,$2,$3,$4} ' sorted.txt

         printf "Othello:\n"
        printf "%-10s %-10s %-10s %-10s\n" "UserName" "Wins" "Loses" "w/l ratio"
        awk '{ if($5=="Othello")printf "%-10s %-10s %-10s %-10s\n",$1,$2,$3,$4} ' sorted.txt

         printf "Connect4:\n"
        printf "%-10s %-10s %-10s %-10s\n" "UserName" "Wins" "Loses" "w/l ratio"
        awk '{ if($5=="Connect4")printf "%-10s %-10s %-10s %-10s\n",$1,$2,$3,$4} ' sorted.txt
fi        
        

        
