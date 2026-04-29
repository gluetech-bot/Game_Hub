chkusr() { if cut -d " " -f1 users.tsv| grep -q "^$1$"  ; then           
return 0 ;                                                                                                           
else   read -p "This username doesn't exists . Do you want to register and update the users.tsv . If you want to register, please enter yes or else no : " regis
    if [[ $regis == "yes" ]] ; then
            register $1
    else
      exit
    fi
    return 1 ;
fi
}
#register() function creates new user and it's password and stores it in users.tsv,password is hashed.
register() {
#      read -p "Please enter new username : " newuser
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
      hashpass=$(echo $newpass | sha256sum | cut -d " " -f 1)
      echo "$1 $hashpass" >> users.tsv
       echo -e "\e[32m$user1 is now registered\e[0m"
      return 0;
}
#chkpass() function verifies the password entered.
chkpass() {
while true
do
read -p $'\e[33mEnter  password of "'$1$'": \e[0m' pass
hashpass=$(echo $pass | sha256sum | cut -d " " -f 1)
if [[ $hashpass == $(awk -v val="$1" 'val==$1{print $2}' users.tsv) ]] ; then
    return 0 ;
  else
    echo -e "\e[31mThe password entered is wrong , please try again\e[0m"
  fi
done
}

read -p $'\e[33mPlayer 1 , Enter your username : \e[0m' user1
chkusr $user1
chkpass $user1
while true
do
read -p $'\e[33mPlayer 2 , Enter your username : \e[0m' user2
if [[ $user1 != $user2 ]] ;then
     break
else
 echo -e "\e[31mEnter different username\e[0m"
fi
done
chkusr $user2
chkpass $user2

python3 game.py $user1 $user2