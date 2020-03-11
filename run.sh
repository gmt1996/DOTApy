#!/bin/bash

nomeCitta="Pisa"
meseInizio="'marzo 2020'"
numeroMesi=6
python estrazioneUrl.py -c $nomeCitta -d $meseInizio -m $numeroMesi
python estrazioneInfoHotel.py -c $nomeCitta
python NomePrezzoAnno.py
