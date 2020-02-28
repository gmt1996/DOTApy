#!/bin/bash

nomeCitta="Pisa"
meseInizio="marzo 2020"
numeroMesi=6
python3 estrazioneUrlCalFin.py $nomeCitta $meseInizio $numeroMesi
python3 estrazioneInfoHotel.py $nomeCitta
python3 NomePrezzoAnno.py
