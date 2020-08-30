#!/usr/bin/env python3

from multiprocessing import Queue
from threading import Thread
import string, random, time, threading

timeout = 60 #[segundos]

queue = Queue()
timeout_start = time.time();

def generador_cadenas(size=5, chars=string.ascii_uppercase):
    return ''.join(random.choice(chars) for _ in range(size))
    
def insert_in_queue ():
    while time.time() < timeout_start + timeout : 
        cadena_random = generador_cadenas()
        queue.put(cadena_random)
        #print("%s added at queue" % cadena_random)
    print("Acabando el trabajo") 
    
def comprobador ():
    
    cadenas_generadas = 0
    cadenas_repetidas = 0
    cadenas_nuevas = 0
    
    file_object = open('data.txt', 'a+')
    dataRepe = dict()

    #print("Reading elements from queue...")
    while not queue.empty():
         data = queue.get()
         #print("%s read from queue" % data)
         cadenas_generadas = cadenas_generadas + 1 
         if data in file_object.read():
            #print("The %s is in the file" %data)
            cadenas_repetidas = cadenas_repetidas + 1                     
            dataRepe[data] = dataRepe.get(data, 0) + 1  
         else:
            file_object.write(data)
            file_object.write('\n')
            cadenas_nuevas = cadenas_nuevas + 1   

    file_object.close()
    print("Se han generado un total de %d" % cadenas_generadas)
    print("Se han generado un total de %d cadenas repetidas" % cadenas_repetidas)
    print("Se han generado un total de %d cadenas nuevas" % cadenas_nuevas) 
    print(dataRepe)    

 
    
if __name__ == "__main__":
    try:
        threadA = Thread(target = insert_in_queue)
        threadB = Thread(target = insert_in_queue)
        threadC = Thread(target = insert_in_queue)

        threadA.start()
        threadB.start()
        threadC.start()

        threadA.join();
        threadB.join();
        threadC.join(); 
        
        comprobador()
 

        
     
    except KeyboardInterrupt: # If CTRL+C is pressed, exit cleanly:
            print("Exit")
            
            
