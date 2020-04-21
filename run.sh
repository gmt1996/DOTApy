#!/bin/bash

nomeCitta="Pisa"
meseInizio="'marzo 2020'"
numeroMesi=6
numeroRecensioni=0
python estrazioneUrl.py -c $nomeCitta -d $meseInizio -m $numeroMesi
python estrazioneInfoHotelRec.py -c $nomeCitta -nr $numeroRecensioni
python estrazionePrezzo.py
