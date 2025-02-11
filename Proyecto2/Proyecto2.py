'''
Code adapted from GitHubGist:
https://gist.github.com/JonCooperWorks/5314103
'''

import random



'''
Euclid's algorithm for determining the greatest common divisor
Use iteration to make it faster for larger integers
'''
def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a


'''
Euclid's extended algorithm for finding the multiplicative inverse of two numbers
'''
def multiplicative_inverse(e, phi):
    d = 0
    x1 = 0
    x2 = 1
    y1 = 1
    temp_phi = phi
    
    while e > 0:
        temp1 = temp_phi/e
        temp2 = temp_phi - temp1 * e
        temp_phi = e
        e = temp2
        
        x = x2- temp1* x1
        y = d - temp1 * y1
        
        x2 = x1
        x1 = x
        d = y1
        y1 = y
    
    if temp_phi == 1:
        return d + phi

'''
Tests to see if a number is prime.
'''
def is_prime(num):
    if num == 2:
        return True
    if num < 2 or num % 2 == 0:
        return False
    for n in xrange(3, int(num**0.5)+2, 2):
        if num % n == 0:
            return False
    return True

'''
Generatung public and private key
'''
def generate_keypair(p, q):
    if not (is_prime(p) and is_prime(q)):
        raise ValueError('Both numbers must be prime.')
    elif p == q:
        raise ValueError('p and q cannot be equal')
    
    # 1) n = p*q
    n = p * q

    # 2) Calculate Euler fucntion (Phi is the coefficient of n)
    phi = (p-1) * (q-1)

    # 3) Choose an integer e such that e and phi(n) are coprime
    e = random.randrange(1, phi)

    # 3.1) Use Euclid's Algorithm to verify that e and phi(n) are comprime
    g = gcd(e, phi)
    while g != 1:
        e = random.randrange(1, phi)
        g = gcd(e, phi)

    # 4) Use Extended Euclid's Algorithm to generate the private key
    d = multiplicative_inverse(e, phi)
    
    #Return public and private keypair
    #Public key is (e, n) and private key is (d, n)
    return ((e, n), (d, n))

'''
Encrypting a message
'''
def encrypt(pk, plaintext):
    #Unpack the key into it's components
    key, n = pk
    #Convert each letter in the plaintext to numbers based on the character using a^b mod m
    # C    =       m      ^  e (mod n)
    cipher = [(ord(char) ** key) % n for char in plaintext]
    #Return the array of bytes
    return cipher

'''
Decrypting a message
'''
def decrypt(pk, ciphertext):
    #Unpack the key into its components
    key, n = pk
    #Generate the plaintext based on the ciphertext and key using a^b mod m
    # m   =       c    ^   d (mod n)
    plain = [chr((char ** key) % n) for char in ciphertext]
    #Return the array of bytes as a string
    return ''.join(plain)
    

if __name__ == '__main__':
    '''
    Detect if the script is being run directly by the user
    '''
    print "RSA Encrypter/ Decrypter"
    print "Calderon Fernandez Gabriel" 
    print "Cova Pachecho Felipe de Jesus"
    
    '''
    Asigna un numero aleatorio a las dos variables auxiliares
    '''
    aux1 = random.randint(2,100)
    aux2 = random.randint(2,100)

    '''
    Checa si el numero es primo, si no es primo selecciona otro hasta que lo sea 
    y se lo asigna a p.
    '''
    while is_prime(aux1) == False:
        aux1 = random.randint(2,100)
    else:
        p = aux1
        print "Your first prime number is:",p

    #p = int(raw_input("Enter a prime number (17, 19, 23, etc): "))
    
    '''
    Checa si el numero es primo y que no sea igual a p, si no es primo o es igual a p,
    selecciona otro hasta que sea primo y diferente de p y se lo asigna a q.
    '''
    while is_prime(aux2) == False or aux1 == aux2:
        aux2 = random.randint(2,100)
    else:
        q = aux2
        print "Your second prime number is:",q

    #q = int(raw_input("Enter another prime number (Not one you entered above): "))
    
    print "Generating your public/private keypairs now . . ."
    public, private = generate_keypair(p, q)
    print "Your public key is ", public ," and your private key is ", private
    message = raw_input("Enter a message to encrypt with your private key: ")
    encrypted_msg = encrypt(private, message)
    print "Your encrypted message is: "
    print ''.join(map(lambda x: str(x), encrypted_msg))
    print "Decrypting message with public key ", public ," . . ."
    print "Your message is:"
    print decrypt(public, encrypted_msg)