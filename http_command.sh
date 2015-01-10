#!/bin/bash

alias wingo_login="http :5000/users/login email='sacha@labsquare.org' password='sacha' --session='wingo'"
alias wingo_logout="http :5000/users/logout --session='wingo'"
alias wingo_mynotes="http :5000/users/mynotes --session='wingo'"
alias wingo_pockets="http :5000/users/pockets --session='wingo'"