#!/usr/bin/env bash
function court() {
  case "${1}" in

      "G" | "g")
          echo "The defendant is guilty."
          ;;
      "N" | "n")
          echo "The defendant is not guilty."
          ;;
      "P" | "p")
          echo "The trial has been postponed."
          ;;
      *)
          echo "Order Order!"
          ;;

  esac
    # put your code here
}
