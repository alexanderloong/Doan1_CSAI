from random import *
import random
import sys
n=int(sys.argv[1])
numberList = [1,0,0]

map_game=[]
file_output = open("inputmatrix.txt", mode = 'w')
for i in range(0,n):
  map_ex =""
  for j in range (0,n):
    map_ex+= str(random.choice(numberList)) + " "
  map_game.append(map_ex)

file_output.write(str(n)+" " + str(n )+'\n')

file_output.write(str(randrange(0,n)) +" " + str(randrange(0,n)) +'\n')

file_output.write(str(randrange(0,n))+" " + str(randrange(0,n)) +'\n')
for i in range (0,n):
  file_output.write(map_game[i]+'\n')

file_output.close()
