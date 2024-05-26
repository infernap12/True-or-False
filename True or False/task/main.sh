#!/usr/bin/env bash

#  write your code here
echo "Welcome to the True or False Game!"

curl --silent http://127.0.0.1:8000/download/file.txt -o ID_card.txt -s
cat ID_card
