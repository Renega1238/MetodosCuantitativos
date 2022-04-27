'''
@authors:   Daniela Vignau León		        A01021698
            Roberto Gervacio Guendulay   	A01025780
            Héctor Alexis Reyes Manrique 	A01339607
            René García Avilés   		    A01654359

'''
import quantumrandom as qr
import numpy as np
import matplotlib.pyplot as plt


def formatClausula(clause):
    clause.replace("\n", "")
    clause = clause.split(" ")
    clause = [int(x) for x in clause]
    return clause


def getInstanceFromFile():
    inputFile = input("File name (without extension): ")
    inputFile = inputFile + ".txt"
    file = open(inputFile, 'r')
    line = file.readline()
    # seguir leyendo hasta que la línea deje de ser un comentario
    while line[0] == 'c':
        line = file.readline()
    numVariables = int(line.split(" ")[2])
    # al momento de separarlo por los ceros, hay que quitarle el último caracter que es un string vacío ''
    clauseString = file.read().split(" 0")[:-1]
    clauses = []
    for clausula in clauseString:
        clauses.append(formatClausula(clausula))
    return clauses, numVariables


def evaluateInstance(instance, booleanList):
    # contienen los índices de las clausulas que son verdaderas y las que son falsas para saber cuáles modificar
    trueClauses = []
    falseClauses = []
    satisfied = True

    # for(int i = 0; i < instance; i++)
    for indexClause in range(len(instance)):
        clause = instance[indexClause]
        currentResult = False
        # Cada valor de cada clausula
        for boolIndex in clause:
            if boolIndex < 0:
                boolIndex *= -1
                value = not booleanList[boolIndex - 1]
            else:
                value = booleanList[boolIndex - 1]
            currentResult = currentResult or value
        if currentResult:
            trueClauses.append(indexClause)
        else:
            falseClauses.append(indexClause)
            satisfied = False
    return satisfied, trueClauses, falseClauses


def generateRandomBitString(numVariables):
    # genera un numero random de n bits en forma de entero
    # hay que agregarle los ceros al principio porque al pasarlo de int a bin le quita los ceros de la izquierda
    binaryString = bin(int(qr.randint(0, 2**numVariables)))[2:]

    # Agregamos los ceros
    while binaryString.__len__() < numVariables:
        binaryString = "0" + binaryString
    return binaryString


def getBooleansFromBitString(bitString):
    booleanList = []
    for bit in bitString:
        if bit == "0":
            booleanList.append(False)
        else:
            booleanList.append(True)
    return booleanList


def getIndexOfFlippedBit(falseClauses, instance):
    randomFalseClause = int(qr.randint(0, falseClauses.__len__()))
    randomClauseNum = falseClauses[randomFalseClause]
    randomLiteral = int(qr.randint(0, 3))
    # fichero = open('ksatResult.txt','a') #Creamos el archivo resultante
    t = "\n[+] Random clause selected was > " + str(instance[randomClauseNum]) + ". At index: " + str(randomClauseNum + 1) + "\n"
    fichero.write(t)
    t1 = "\n[+] On that clause the random literal chosen was: " + str(instance[randomClauseNum][
        randomLiteral]) +  ". At index >" + str(randomLiteral + 1)
    fichero.write(t1)
    bitToFlip = instance[randomClauseNum][randomLiteral]
    if bitToFlip < 0:
        bitToFlip *= -1
    return bitToFlip


def flipBitString(bitToFlip, bitString):
    if bitString[bitToFlip - 1] == "1":
        newBit = "0"
    else:
        newBit = "1"
    str1 = bitString[:bitToFlip - 1]
    str2 = bitString[bitToFlip:]
    bitString = str1 + newBit + str2
    return bitString


if __name__ == '__main__':
    ksatInstance, numVariables = getInstanceFromFile()
    maxIterations = 3 * numVariables

    # Generamos un bitstring random -->
    bitString = generateRandomBitString(numVariables)
    # Regresamos una lista con valores Booleanos correspondientes al bitSting random
    booleanList = getBooleansFromBitString(bitString)

<<<<<<< HEAD
    fichero = open('05results.txt', 'w')
=======
    fichero = open('results_03.txt', 'w')
>>>>>>> 865c4895d31505dd38fe20e35f692a4d3b5c1c9f

    nFalseClauses = []
    
    # Primer bitstring
    fichero.write("[+] Bit string to be evaluated > " + str(bitString))
    satisfied, trueClauses, falseClauses = evaluateInstance(ksatInstance, booleanList)

    nFalseClauses.append(len(falseClauses))

    fichero.write("\n[+] The instance evaluated with the bit string was > " + str(satisfied))
    fichero.write("\n[+] The clauses that were false > " + str(falseClauses))
    fichero.write("\n[+] The clauses that were true > " + str(trueClauses))
    totalEvaluations = 0

    while not satisfied:
        n = 0
        while not satisfied and n < maxIterations:
            print(falseClauses)
            bitToFlip = getIndexOfFlippedBit(falseClauses, ksatInstance)
            fichero.write("\n[+] Bit flipped at index > " + str(bitToFlip))
            booleanList[bitToFlip - 1] = not booleanList[bitToFlip - 1]
            bitString = flipBitString(bitToFlip, bitString)
            fichero.write("\n-------------- Iteration #" + str(n) + " --------------")
            fichero.write("\n[+] New bit string to be evaluated > " +  str(bitString))

            # Evaluamos con la nueva list[] de booleanos, evalua sobre toda la instancia
            # clausula por clausula
            satisfied, trueClauses, falseClauses = evaluateInstance(ksatInstance, booleanList)

            nFalseClauses.append(len(falseClauses))

            fichero.write("\n[+] The clauses that were false > " + str(falseClauses))
            fichero.write("\n[+] The clauses that were true > "+ str(trueClauses))

            n += 1
        totalEvaluations += n
        if not satisfied:
            fichero.write("\n\n--+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+--")
            fichero.write("\n\n[+] After " +  str(n) + " iterations, the instance was not satisfied")
            bitString = generateRandomBitString(numVariables)
            booleanList = getBooleansFromBitString(bitString)
            fichero.write("\n[+] New initial random string > " + str(bitString))
            nFalseClauses = []
            satisfied, trueClauses, falseClauses = evaluateInstance(ksatInstance, booleanList)
            nFalseClauses.append(len(falseClauses))
            

    fichero.write("\n[+] After " + str(totalEvaluations) + " evaluations the solution was found")
    fichero.write("\n[+] Solution found > " + str(bitString))
    fichero.close()

    print("final graph: ", nFalseClauses)
    plt.plot(list(range(len(nFalseClauses))), nFalseClauses)
    plt.title("Random Walk")
<<<<<<< HEAD
    plt.savefig('05graph.png')
=======
    plt.savefig('graph_03.png')
>>>>>>> 865c4895d31505dd38fe20e35f692a4d3b5c1c9f
