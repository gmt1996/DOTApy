#!/bin/bash

nomeCitta="Pisa"
meseInizio="'marzo 2020'"
numeroMesi=6
numeroRecensioni=0
python URIextractor.py -c $nomeCitta -d $meseInizio -m $numeroMesi
python InfoReviews.py -c $nomeCitta -nr $numeroRecensioni
python Prices.py
