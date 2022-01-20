# ACRCloudTest
Script python per il riconoscimento automatico di contenuti

Riconosce un mp3 anonimo sistemando i suoi tag ID3.
maurizio.conti@fablabromagna.org  - 4 gennaio 2022

Si basa su un esempio trovato nell'SDK di acrcloud.com
https://github.com/acrcloud/acrcloud_sdk_python

Per l'editing di tag ID3 utilizzo la lib python mutagen
https://mutagen.readthedocs.io/en/latest/user/id3.html

# Istruzioni

Attivare un account su acrcloud.com

Aggiungere alla dashboard un progetto di decodifica audio (free per 14 giorni)
https://console.acrcloud.com/avr?region=eu-west-1#/projects/online

Inserire i brani nella sotto cartella ./mp3
Lancia python3 .\decode.py

I file decodificati vengono taggati e rinominati sul posto (usare una copia, non si sa mai)
