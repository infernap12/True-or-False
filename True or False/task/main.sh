#!/usr/bin/env bash

credentials="ID_card.txt"
questFile="question.txt"
scoreFile="scores.txt"

function welcome() {
    echo "Welcome to the True or False Game!"
}

function login() {
    curl --output $credentials --silent http://127.0.0.1:8000/download/file.txt

    user=$(grep -o '"username": "[^"]*' $credentials | grep -o '[^"]*$')
    pass=$(grep -o '"password": "[^"]*' $credentials | grep -o '[^"]*$')

    echo "Login message: "
    curl --silent --cookie-jar cookie.txt -u $user:$pass http://127.0.0.1:8000/login
    echo "Logged in successfully!"
}

function save_score() {
    local name=$1
    local score=$2
    local date=$(date '+%Y-%m-%d')
    echo "User: $name, Score: $score, Date: $date" >> $scoreFile
}

function question() {
    local score=0
    local correct_answers=0
    local words=("Perfect!" "Awesome!" "You are a genius!" "Wow!" "Wonderful!")

    while true; do
        # Connect to the API and retrieve the question and answer
        curl --silent --output $questFile --cookie cookie.txt http://127.0.0.1:8000/game

        local quest=$(grep -o '"question": "[^"]*' $questFile | grep -o '[^"]*$')
        local answ=$(grep -o '"answer": "[^"]*' $questFile | grep -o '[^"]*$')

        # Print the question and prompt for an answer
        echo "$quest"
        echo $answ
        read -rp "True or False? " playerRes

        # Normalize both the player's response and the answer from the API to lowercase
        playerRes=$(echo "$playerRes" | tr '[:upper:]' '[:lower:]')
        answ=$(echo "$answ" | tr '[:upper:]' '[:lower:]')

        # Compare the player's answer with the correct answer
        if [ "$playerRes" == "$answ" ]; then
            # Increment score and correct answers count
            score=$((score + 10))
            correct_answers=$((correct_answers + 1))

            # Select a random congratulatory message
            local random_index=$((RANDOM % ${#words[@]}))
            echo "${words[$random_index]}"
        else
            # Print the results and exit the loop
            echo "Wrong answer, sorry!"
            echo "$name, you have $correct_answers correct answer(s)."
            echo "Your score is $score points."
            save_score "$name" "$score"
            break
        fi
    done
}

function display_scores() {
    if [[ -f $scoreFile ]]; then
        echo "Player scores:"
        cat $scoreFile
    else
        echo "File not found or no scores in it!"
    fi
}

function reset_scores() {
    if [[ -f $scoreFile ]]; then
        rm $scoreFile
        echo "File deleted successfully!"
    else
        echo "File not found or no scores in it!"
    fi
}

function menu() {
    echo -e "0. Exit\n1. Play a game\n2. Display scores\n3. Reset scores\nEnter an option:"
    read -r option
}

welcome
login

while true; do
    menu
    case $option in
        0)
            echo "See you later!"
            exit 0
            ;;
        1)
            RANDOM=4096
            read -rp "What is your name? " name
            question
            ;;
        2)
            display_scores
            ;;
        3)
            reset_scores
            ;;
        *)
            echo "Invalid option. Please choose a valid option."
            ;;
    esac
done
