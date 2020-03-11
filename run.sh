#!/bin/bash

nomeCitta="Pisa"
meseInizio="'marzo 2020'"
numeroMesi=6
python3 estrazioneUrl.py -c $nomeCitta -d $meseInizio -m $numeroMesi
python3 estrazioneInfoHotel.py -c $nomeCitta
python3 NomePrezzoAnno.py
