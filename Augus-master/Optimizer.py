# module that defines the optimization rules

import re

from graphviz import Digraph
import pydotplus

# list with all optimitations made
optimizations = []

def removeSpaces(lines):
    aux = []
    for l in lines:
        aux.append(re.sub(r"\s+", "", l))
    return aux

def rule1():
    # t2 = b
    # b = t2 -> t2 = b
    file1 = open('un-optimized.augus', 'r') 
    lines = file1.readlines()
    # remove all spaces
    newLines = removeSpaces(lines)
    file1.close()
    # search in code for that pattern
    m1 = 0
    m2 = 1
    result = open('un-optimized.augus', 'w')

    while m2 < len(newLines):
        line1 = newLines[m1].strip()
        line2 = newLines[m2].strip()
        # if it is assignment, both must end in ; and have = in [1]
        l1 = line1.split(';')[0].split('=')
        l2 = line2.split(';')[0].split('=')
        try:
            if l1[0] == l2[1] and l1[1] == l2[0]:
                global optimizations
                optimizations.append('Se aplicó la regla 1 de optimización.')
                print('Se aplicó la regla 1 de optimización.')
                result.write(lines[m1])
                #result.write('\n')
                m1 +=2
                m2 +=2
                continue
            else:
                result.write(lines[m1].strip()) #OK
                result.write('\n')
        except:
            result.write(lines[m1].strip()) #OK
            result.write('\n')
        
        m1 +=1
        m2 +=1
    result.write(lines[len(lines)-1])
    result.close()
    return

def rule2():
    file1 = open('un-optimized.augus', 'r') 
    lines = file1.readlines()
    # remove all spaces
    #newLines = removeSpaces(lines)
    file1.close()
    m1 = 0
    result = open('un-optimized.augus', 'w')
    while m1 < len(lines):
        try:
            line = lines[m1].split(' ')
            goto = line[0]
            label1 = line[1].split(';')[0]
            #print (goto)
            #print (label1)
            if (goto == 'goto'):
                m2 = m1+1
                while m2 < len(lines):
                    line2 = lines[m2].strip().split(';')[0].split(':')[0]
                    if line2 == label1:
                        global optimizations
                        optimizations.append('Se aplicó la regla 2 de optimización.')
                        print('Se aplicó la regla 2 de optimización.')
                        #result.write(label1 + ':\n')
                        m1 = m2-1
                        break
                    else:
                        pass
                    m2 += 1
            else:
                result.write(line)
            
        except:
            result.write(lines[m1])
        
        m1 += 1
    result.close()
    return






def optimitationReport(op):
    # Reporte de optimizacion
    dotDataReport = 'digraph{tbl[shape=plaintext\nlabel=<<table><tr><td colspan=\'1\'>Reporte de optimizaciones</td></tr>'
    dotDataReport = dotDataReport + '<tr><td>Regla aplicada</td></tr>'
    for x in op:
        dotDataReport += '<tr><td>' + x + '</td></tr>'
    dotDataReport += '</table>>];}'

    reportGraph = pydotplus.graph_from_dot_data(dotDataReport)
    reportGraph.write_pdf('Reporte_optimizacion.pdf')


def optimize():
    #call all the rules
    rule1()
    rule2()
    global optimizations
    optimitationReport(optimizations)

optimize()