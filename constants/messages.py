from constants import mail_data
from config import config

# DISCORD
MAIL_KO = "La commande $setmail doit être suivie de 0 (non envoyé) ou 1 (déjà envoyé)"
MAIL_OFF = "Le mail est considéré comme non envoyé, l'envoie automatique est activé"
UNKNOWN_EXTENSION = "Extension du fichier non reconnue. Fichier non pris en compte"
STARTED_KO = "La commande $started doit être suivie de \"on\", \"off\", 0 ou 1"
DEBUG_KO = "La commande $debug doit être suivie de \"on\", \"off\", 0 ou 1"
MAIL_ON = "Le mail est considéré comme déjà envoyé et ne sera pas renvoyé"

DB_INIT = "La base de données à été complètement réinitialisée"
MAIL_SEND = "Le mail a été envoyé à l'adresse " + mail_data.MAIL_TO
OFFSET_KO = "La commande $offset doit être suivi de 3 entiers"
OFFSET_OK = "Les offsets ont été définis sur O_A, O_B et O_C"
FILE_TREATED = "Fichier traité par le " + config.PC_NAME
DB_DELETE = "Les coureurs ont été supprimés de la base"
DEBUG_OFF = "Le débug a été désactivé"
STARTED_OFF = "La course est arrêtée"
STARTED_ON = "La course est démarée"
DEBUG_ON = "Le débug a été activé"
OK = "Ok " + config.PC_NAME

# PRINT
CLASSIC_START = "Programme démarré en mode classique"
DEBUG_START = "Programme démarré en mode débug"

# CMD
CMD = "Commandes disponibles :\n\n\
    $mail : Envoie un mail contenant le fichier word des récompenses.\n\
    $delete : Supprime les coureurs de la base de données.\n\
    $init : Initialise la base de données.\n\
    $debug [on/off/0/1] : Active ou desactive le debug.\n\
    $offset [offset_a offset_b offset_c] : Defini les offsets.\n\
    $setmail [0/1] : Enregistre le mail comme déjà envoyé ou non\n\
    $started [on/off/0/1] : Démarrer ou arrêter la course\n\
    $test : Lance un appel aux bots connectés.\n\
    $clear [nombre] : Supprime les messages dans le channel.\n\
    $cmd : Affiche les commandes"