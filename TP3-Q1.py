import socket, optparse, sys
from cryptoModule import entierAleatoire, trouverNombrePremier, exponentiationModulaire

from socketUtil import recv_msg, send_msg


# Début du code
# 1. S'échanger a et b
# A génère p B génere q
# 2. Calculer les clés A et B
# 3. S'échanger A et B
# 4. Calculer k
# 

a = trouverNombrePremier()
b = entierAleatoire(a)

def cle_envoyée(a, b, p_ou_q):
    A_ou_B = exponentiationModulaire(b, p_ou_q, a)
    return A_ou_B

def calcul_cle_partage(A_ou_B, p_ou_q, a):
    k = exponentiationModulaire(A_ou_B, p_ou_q, a)
    return k

def sequenceA(a, b):
    p = entierAleatoire(a)
    A = cle_envoyée(a, b, p)
    # Envoie de la clé à B
    
    # Reception de la clé B
    
    B = None

    k = calcul_cle_partage(B, p, a)
    return k

def sequenceB(a, b):
    q = entierAleatoire(a)
    B = cle_envoyée(a, b, q)
    # Envoie de la clé à A
    
    # Reception de la clé A
    
    A = None

    k = calcul_cle_partage(A, q, a)
    return k

def main():
    #choisissez l’adresse avec l’option -a et le port avec -p
    parser = optparse.OptionParser()
    parser.add_option("-s", "--server", action="store_true", dest="serveur", default=False)
    parser.add_option("-a", "--address", action="store", dest="address", default="localhost")
    parser.add_option("-p", "--port", action="store", dest="port", type=int, default=1337)
    opts = parser.parse_args(sys.argv[1:])[0]

    if opts.serveur: #mode serveur
        serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        serversocket.bind(("localhost", opts.port))
        serversocket.listen(5)
        
        while True:
            (s, address) = serversocket.accept()
            a = trouverNombrePremier()
            b = entierAleatoire(a)
            

            send_msg(s, a+b)#
            
            clé_B = recv_msg(s)
            
            send_msg(s, "Enchante, " + nom)
            s.close()
    else: #mode client
        destination = (opts.address, opts.port)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(destination)
        print(recv_msg(s))
        send_msg(s, input())
        print(recv_msg(s))
        s.close()