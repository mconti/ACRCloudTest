'''

Riconosce un mp3 anonimo sistemando i suoi tag ID3.
maurizio.conti@fablabromagna.org  - 4 gennaio 2022

Si basa su un esempio trovato nell'SDK di acrcloud.com
https://github.com/acrcloud/acrcloud_sdk_python

dopo aver creato un account su acrcloud
e aver creato un progetto di decodifica audio (free per 14 giorni) sulla loro dashboard
https://console.acrcloud.com/avr?region=eu-west-1#/projects/online


Per l'editing di tag ID3 utilizzo la lib python mutagen
https://mutagen.readthedocs.io/en/latest/user/id3.html


si usa cosi:
- si inseriscono i brani nella sotto cartella ./mp3 (usare una copia, non si sa mai)
- si lancia
python3 .\decode.py

i file decodificati rimangono nella cartella ./mp3 con un nuovo nome

'''

import os, sys
from acrcloud.recognizer import ACRCloudRecognizer
from mutagen.easyid3 import EasyID3
import json

 # il nome di un brano può avere caratteri non compatibili con il file system.
 # qui lo sistema...
def normalizeName( audio ):
    nuovoFileName = "_" + audio["artist"][0] + " - " + audio["title"][0] + " - (" + audio["date"][0] + ")" 
    nuovoFileName = nuovoFileName.replace("[", "(")
    nuovoFileName = nuovoFileName.replace("]", ")")
    nuovoFileName = nuovoFileName.replace('"', "")
    nuovoFileName = nuovoFileName.replace('?', "")
    nuovoFileName = nuovoFileName.replace(':', "-")
    nuovoFileName = nuovoFileName.replace('/', "-")
    nuovoFileName = nuovoFileName.replace('*', "-")

    if len(nuovoFileName + ".mp3") >= 79:
        nuovoFileName = nuovoFileName[0:74] 
        
    print( len (nuovoFileName ))
    return nuovoFileName + ".mp3"

# Qui arriva il nome di un file e il json con tutti i dati riconosciuti da acrcloud (result)
# Noi apriamo il file con la lib ID3 (tag MP3...) e cerchiamo di sistemare i TAG MP3 con i dati di acrcloud
def getAudio( nomeFile, result ):

    try:
        audio = EasyID3( nomeFile )
        audio["genre"] = ""
        audio["date"] = ""
        audio["album"] = ""

        json_load = ( json.loads(result) )
        if json_load['status']['code'] == 0:
            try:
                jsonBase = json_load['metadata']['music'][0]

                if 'artists' in jsonBase:
                    audio["artist"] = jsonBase['artists'][0]['name']

                if 'title' in jsonBase:
                    audio["title"] = jsonBase['title']
                
                if 'genres' in jsonBase:
                    audio["genre"] = jsonBase['genres'][0]['name']

                if 'release_date' in jsonBase:
                    audio["date"] = jsonBase['release_date'].split("-")[0]

                if 'album' in jsonBase:
                    audio["album"] = jsonBase['album']['name']
                
                #audio["label"] = jsonBase['label']


            except Exception as exception:
                print("Errore...")
                print( type(exception).__name__ )

            return audio

    except Exception as exception:
        print("Errore...")
        print( type(exception).__name__ )

    return None
    

## oggetto da passare durante le chiamate a acrcloud...
config = {
    
    # Account gratuito per 14 giorni creato con liste@mauriz...
    'host':'identify-eu-west-1.acrcloud.com',
    'access_key':'0a71136618f439ffdacf78dcf145dc20', 
    'access_secret':'NSCqAf32lt4B85XSfJTgcl2zy7JCEtVfrXS8FnDK',
    'timeout':4 # seconds
}


''' Ecco il decodificatore acrcloud per file:
    Audio: mp3, wav, m4a, flac, aac, amr, ape, ogg ...
    Video: mp4, mkv, wmv, flv, ts, avi ...'''
re = ACRCloudRecognizer(config)


# -----------------------------
# il processo di decodifica inizia qui, scansionando la directory Mp3 alla ricerca di file .mp3
# -----------------------------
with os.scandir('mp3/') as entries:
    for entry in entries:
        fileName, fileExt = os.path.splitext( entry )
        fileName = os.path.basename( entry )

        # apre solo quelli che non sono già stati elaborati... (che iniziano per _)
        if( fileExt == ".mp3" and not fileName.startswith("_") ):
            #print()
            #print("----" + fileName )
            nome = 'mp3/' + entry.name
            
            # decodifica il file con acrcloud
            result = re.recognize_by_file(nome, 0)
            
            # crea un oggetto ID3 con tutti i parametri trovati da acrcloud
            audio = getAudio( nome, result )

            if audio is not None:
                # Se è andata dritta, lo salva
                audio.save()

                # poi lo rinomina (eliminando dail filename i caratteri non corretti per il file system)
                nuovoFileName = normalizeName( audio )

                # i file codificati hanno un underscore all'inizio per riconoscerli.
                nuovoFileName = "_" + nuovoFileName
                print( nuovoFileName )

                # usa il rename per spostare il file nella cartella mp3/
                try:
                    os.rename(nome, 'mp3/' +  nuovoFileName )

                except FileExistsError:
                    # questa parte va messa a posto.
                    # in caso di doppioni o di file già processati etc, non si comporta proprio bene.
                    # per ora aggiunge un ulteriore  underscore davanti al file
                    nuovoFileName = "_" + nuovoFileName
                    try:
                        os.rename(nome, 'mp3/' +  nuovoFileName )
                        print( nuovoFileName )
                    except FileExistsError:
                        print("?? " + nuovoFileName + " (esiste gia in questa cartella)")

            else:
                print( "?? " + fileName + " (non riconosciuto)")