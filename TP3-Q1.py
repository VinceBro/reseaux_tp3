# Rédigé par Vincent Breault (111 226 718) et Benjamin Girard (111 237 203)
import socket, optparse, sys
from socketUtil import recv_msg, send_msg
from cryptoModule import entierAleatoire, trouverNombrePremier, exponentiationModulaire
from datetime import datetime

parser = optparse.OptionParser()
parser.add_option("-s", "--server", action="store_true", dest="serveur", default=False)
parser.add_option("-d", "--destination", action="store", dest="destination")
parser.add_option("-p", "--port", action="store", dest="port", type=int, default=-1)
opts = parser.parse_args(sys.argv[1:])[0]

def write_exception(e):
    with open('Error.log', 'a') as f:
        f.write(f"{datetime.now()} {e}")
    raise e

def main():
    if opts.destination and opts.serveur:
        write_exception(Exception("L'application ne peut pas utiliser -d et -s simultanément."))

    if opts.port == -1:
        write_exception(Exception("L'option -p est obligatoire."))

    #TODO: retourner un message d'erreur significatif s'il y a une erreur
    #TODO: chaque message d'erreur (et sa date et heure) doit être écrit dans le fichier Error.log
    try:
        if opts.serveur: # mode serveur
            print("###############################################################")
            print("Demarrage du serveur ...")
            serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            serversocket.bind(("localhost", opts.port))
            serversocket.listen(5)
            print(f"Ecoute sur le port : {opts.port}")
            
            while True:
                (s, address) = serversocket.accept()
                print('1e connexion au serveur')
                print('----------------------------------------------------------')

                #create a,b p
                a = trouverNombrePremier()
                b = entierAleatoire(a)
                p = entierAleatoire(a)
                

                #create public key
                server_public_key = exponentiationModulaire(b, p, a)

                print(f"Envoi du modulo : {a}")
                print(f"Envoi de la base : {b}")
                print('----------------------------------------------------------')
                print(f'Cle privee : {p}')
                print(f'Cle publique a envoyer : {server_public_key}')

                send_msg(s, str(a)) # send a
                send_msg(s, str(b)) # send b
                send_msg(s, str(server_public_key)) # send public key

                # receive client public key
                client_public_key = int(recv_msg(s))

                print(f'Cle publique recue : {client_public_key}')


                #calculate shared key
                shared_key = exponentiationModulaire(client_public_key, p, a)
                print(f"Cle partagee : {shared_key}")
                print("au serveur")

                print("###############################################################")
                s.close()

        else: # mode client
            if not opts.destination:
                write_exception(Exception("Le client doit spécifier une destination en utilisant -d."))
            
            print("###############################################################")
            destination = (opts.destination, opts.port)

            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect(destination)

            a = int(recv_msg(s)) # receive a
            print(f"Reception du modulo : {a}")
            b = int(recv_msg(s)) # receive b
            print(f'Reception de la base : {b}')
            
            print('----------------------------------------------------------')
            #create q
            q = entierAleatoire(a)

            print(f'Cle privee : {q}')
            #Create public key
            client_public_key = exponentiationModulaire(b, q, a)

            print(f'Cle publique a envoyer : {client_public_key}')
            
            # receive server public key
            server_public_key = int(recv_msg(s)) 
            print(f'Cle publique recue : {server_public_key}')

            #send public key
            send_msg(s, str(client_public_key))

            #calculate shared key
            shared_key = exponentiationModulaire(server_public_key, q, a)
            print(f"Cle partagee : {shared_key}")

            print("###############################################################")
            s.close()
    except Exception as e:
        write_exception(e)

if __name__ == "__main__":
    main()