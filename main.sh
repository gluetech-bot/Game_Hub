chkusr() {
  if grep -q "$1" users.tsv ; then
    return 0 ;
  else 
    read -p $"This username doesn't exists . Do you want to register and update the users.tsv . If you want to , please enter yes or else no : " regis
    if [[ $regis == "yes" ]] ; then
      register
    else
      exit
    fi
    return 1 ;
  fi
}

register() {
      read -p "Please enter new username : " newuser
      while true 
      do
      read -p "Set password : " newpass
      read -p "Confirm password : " confpass
      if [[ $newpass == $confpass ]] ; then
        break
      else
        echo "Passwords do not match"
      fi
      done
      hashpass=$(echo $newpass | sha256sum | cut -d "	" -f 1)
      echo "$newuser	$hashpass" >> users.tsv
      echo "$newuser is now registered"
}

chkpass() {
while true
do
read -p "Enter your password : " pass
hashpass=$(echo $pass | sha256sum | cut -d "	" -f 1)
  if [[ $hashpass == $(grep "$1" users.tsv | cut -d "	" -f 2) ]] ; then
    return 0 ;
  else
    echo "The password entered is wrong , please try again"
  fi
done
}

read -p "Player 1 , Enter your username : " user1
chkusr $user1
chkpass $user1 

read -p "Player 2 , Enter your username : " user2
chkusr $user2
chkpass $user2

python3 game.py $user1 $user2
