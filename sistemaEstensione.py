'''

Utility per rinominare i file aggiungendo l'estensione .mp3 alla fine del nme del file
maurizio.conti@fablabromagna.org - 4 gennaio 2022

Un errore nello script di decodifica ometteva l'estensione, rinominando in modo errato 500 files.
Con questo script ho sistemato la cosa.

'''

import os, sys

with os.scandir('mp3/') as entries:
    for entry in entries:
        fileName, fileExt = os.path.splitext( entry )
        fileName = os.path.basename( entry )

        if( fileExt != ".mp3" and fileName != "NonRiconosciuti" ):
            newFileName = fileName + '.mp3'
            os.rename( 'mp3/' + fileName, newFileName )
            #print( fileName )

