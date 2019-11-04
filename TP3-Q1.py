import socket, optparse, sys
from socketUtil import recv_msg, send_msg
from cryptoModule import entierAleatoire, trouverNombrePremier, exponentiationModulaire

parser = optparse.OptionParser()
parser.add_option("-s", "--server", action="store_true", dest="serveur", default=False)
parser.add_option("-a", "--address", action="store", dest="address", default="localhost") #TODO: remplace -a par -d ou c'est différent?
parser.add_option("-d", "--destination", action="store", dest="destination")
parser.add_option("-p", "--port", action="store", dest="port", type=int, default=-1)
opts = parser.parse_args(sys.argv[1:])[0]

if opts.destination and opts.serveur:
    raise Exception("L'application ne peut pas utiliser -d et -s simultanément.")

if opts.port == -1:
    raise Exception("L'option -p est obligatoire.")

#TODO: retourner un message d'erreur significatif s'il y a une erreur
#TODO: chaque message d'erreur (et sa date et heure) doit être écrit dans le fichier Error.log
if opts.serveur: # mode serveur
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    serversocket.bind((opts.address, opts.port))
    serversocket.listen(5)
    
    while True:
        (s, address) = serversocket.accept()
        
        #create a,b p
        a = trouverNombrePremier()
        b = entierAleatoire(a)
        p = entierAleatoire(a)

        #create public key
        server_public_key = exponentiationModulaire(b, p, a)

        send_msg(s, str(a)) # send a
        send_msg(s, str(b)) # send b
        send_msg(s, str(server_public_key)) # send public key
        
        # receive client public key
        client_public_key = int(recv_msg(s))

        #calculate shared key
        shared_key = exponentiationModulaire(client_public_key, p, a)
        print(shared_key)

        s.close()

else: # mode client
    destination = (opts.destination, opts.port)

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(destination)

    a = int(recv_msg(s)) # receive a
    b = int(recv_msg(s)) # receive b

    #create q
    q = entierAleatoire(a)

    #Create public key
    client_public_key = exponentiationModulaire(b, q, a)

    # receive server public key
    server_public_key = int(recv_msg(s)) 

    #send public key
    send_msg(s, str(client_public_key))

    #calculate shared key
    shared_key = exponentiationModulaire(server_public_key, q, a)
    print(shared_key)

    s.close()
