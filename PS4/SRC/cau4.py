def readFile(filename):
    input = open(filename, 'r')
    a = input.readline()
    a = a.replace("OR","")
    a = a.split()
    n = int(input.readline())
    KB =[]
    for i in range(n):
        line = input.readline()
        line = line.replace("OR","")
        line = line.split()
        s = []
        for i in line:
            s.append(i)
        KB.append(s)
    input.close()
    return KB, a

def findNegative(clause):
    result = []
    for i in clause:
        if '-' in i:
            temp = i.strip('-')
        else:
            temp = '-' + i
        result.append([temp])
    return result

def checkDuality(L1, L2):
    if L1 == '-' + L2 or L2 == '-' + L1:
        return 1
    return 0

def PL_RESOLVE( C1, C2):
    C1_temp = []
    C2_temp = []
    for i in C1:
        C1_temp.append(i)
    for i in C2:
        C2_temp.append(i)
    result = []
    for i in range(len(C1_temp)):
        for j in range(0,len(C2_temp)):
            if checkDuality(C1_temp[i], C2_temp[j]) == 1:
                C1_temp.remove(C1_temp[i])
                C2_temp.remove(C2_temp[j])
                for i in C1_temp:
                    result.append(i)
                for j in C2_temp:
                    if j not in C1_temp:
                        result.append(j)
                return result
    return 0

def checkTrueClause(clause):
    for i in clause:
        for j in clause:
            if checkDuality(i, j) == 1:
                return 1
    return 0

def filtTrueClause(abc):
    i = 0
    while i < len(abc):
        if checkTrueClause(abc[i]) == 1:
                abc.remove(abc[i])
                i = i - 1
        i = i + 1

def checkContain(X, Y):
    for i in Y:
        if i not in X:
            return 0
    return 1

def sortClause(clause):
    for i in range(len(clause) - 1):
        for j in range(i + 1, len(clause)):
            if clause[i][len(clause[i]) - 1] > clause[j][len(clause[j]) - 1]:
                clause[i], clause[j] = clause[j], clause[i]

def PL_RESOLUTION(KB, a):
    clause = KB.copy()
    for i in clause:
        sortClause(i)
    for i in findNegative(a):
        clause.append(i)
    new = []
    size = []
    size.append(0)
    while 1:
        resolvents = []
        for i in range(len(clause) - 1):
            for j in range(i+1, len(clause)):
                temp = PL_RESOLVE(clause[i], clause[j])
                if temp != 0:
                    sortClause(temp)
                    if temp not in clause and temp not in resolvents:
                        resolvents.append(temp)    
        filtTrueClause(resolvents)
        size.append(len(resolvents))
        for i in resolvents:
            new.append(i)
        if [] in resolvents:
            return 1,size, new
        if checkContain(clause, new) == 1:
            return 0,size, new
        for i in new:
            clause.append(i)

def writefile(filename, result,size, new):
    output = open(filename, 'w')
    flag = 0
    for i in range(len(size) - 1):
        flag = flag + size[i]
        output.write(str(size[i + 1]) + '\n')
        if flag < len(new):
            for j in new[flag: flag + size[i + 1]]:
                if len(j) == 0:
                    output.write('{}\n')
                else:
                    for k in range(0,(len(j) - 1)):
                        if j[k] == '':
                            output.write('{}')
                        else:
                            output.write(str(j[k]))
                        output.write(' OR ')
                    if j[len(j) -1] == '':
                        output.write('{}\n' )
                    else:
                        output.write(str(j[len(j) -1]) + '\n')
    if result == 1:
        output.write('YES')
    if result == 0:
        output.write('NO')
    output.close()

import os


def main():
    input_filename = './input/input1.txt'
    output_filename = './output/output1.txt'
    list = os.listdir('./input')
    number_files = len(list)
    for i in range(1, number_files + 1):
        input_filename = './input/input' + str(i) + '.txt'
        output_filename = './output/output' + str(i) + '.txt'
        KB,a = readFile(input_filename)
        result,size, new = PL_RESOLUTION(KB,a)
        writefile(output_filename, result,size, new)

if __name__== "__main__":
    main()