"""
   EE2703 Applied Programming Lab - 2022
        Assignment 2 by EE20B118
"""
import sys
from numpy import *
from math import *
import cmath
#Classes for passive elements
class Resistor:
    def __init__(self,name,node1,node2,value):
        self.name = name
        self.node1 = node1
        self.node2 = node2
        self.value = SI_conversion(value)
class Capacitor:
    def __init__(self,name,node1,node2,value):
        self.name = name
        self.node1 = node1
        self.node2 = node2
        self.value = SI_conversion(value)
class Inductor:
    def __init__(self,name,node1,node2,value):
        self.name = name
        self.node1 = node1
        self.node2 = node2
        self.value = SI_conversion(value)
#Classes for Independent sources
class Voltage_source:
    def __init__(self,name,node1,node2,value,phase = 0):
        self.name = name
        self.node1 = node1
        self.node2 = node2
        self.value = SI_conversion(value)
        self.phase = float(phase)
class Current_source:
    def __init__(self,name,node1,node2,value,phase = 0):
        self.name = name
        self.node1 = node1
        self.node2 = node2
        self.value = SI_conversion(value)
        self.phase = float(phase)
#Function defined to convert a number with prefixees to standard units
def SI_conversion(number):
    try:
        return(float(number))
    except ValueError:
        l = len(number)
        if number[l-1] == 'k':          #Kilo
            base = int(number[0:l-1])
            return base*1e3
        elif number[l-1] == 'M':        # Mega
            base = int(number[0:l-1])
            return base*1e6
        elif number[l-1] == 'm':        # Milli
            base = int(number[0:l-1])
            return base*1e-3
        elif number[l-1] == 'u':        # Micro
            base = int(number[0:l-1])
            return base*1e-6            
        elif number[l-1] == 'n':        # Nano
            base = int(number[0:l-1])
            return base*1e-9
        else:
            sys.exit("Please check the units.Valid prefixes are k,M,m,u,n")

if __name__ == "__main__":

    # checking number of command line arguments
    if len(sys.argv)!=2 :
        sys.exit("Usage: .py_file netlist_file")
    else:
        try:
            FileName = sys.argv[1]
            # checking if given netlist file is of correct type
            if (not FileName.endswith(".netlist")):
                print("Incorrect Format!\nEnter the correct format file")
            else:
            # initializing beginning and ending variables with negative numbers and frequency with zero

                beginning = -1
                ending = -2
                frequency = 0 

                with open (FileName, "r") as f:
                    lines = f.readlines()
                    for line in lines:
            #If .circuit and .end exists their line indexes overwrites beginning and ending 
                            if line[0:8] == ".circuit":
                                    beginning = lines.index(line)
                            elif line[0:4] == ".end":
                                    ending = lines.index(line)
            #If .ac is present, reading frequency from that line 
                            elif line[0:3] == ".ac":
                                    frequency = float(line.split()[2])
            #If any of the .circuit and .end doesnt exists or they are inverted, warning message is printed
                    if beginning >= ending or beginning < 0 or ending < 0:
                        sys.exit("Make sure to have .circuit and .end lines in the file in correct order.")
                    else:
                        Nodes = []
                        components = { 'Resistors': [], 'Capacitors': [], 'Inductors': [], 'IVS': [], 'ICS': [] }
                        for j in lines[beginning+1:ending]:
                            tokens = j.split('#')[0].split('\n')[0].split()
            #Storing nodes in Nodes list
                            Nodes.append(tokens[1])
                            Nodes.append(tokens[2])
            #Storing all the elements of the given circuit and their properties in components dictionary
                            if tokens[0][0] == 'R':
                                components['Resistors'].append(Resistor(tokens[0],tokens[1],tokens[2],tokens[3]))
                            elif tokens[0][0] == 'L':
                                components['Inductors'].append(Inductor(tokens[0],tokens[1],tokens[2],tokens[3]))
                            elif tokens[0][0] == 'C':
                                components['Capacitors'].append(Capacitor(tokens[0],tokens[1],tokens[2],tokens[3]))
                            elif tokens[0][0] == 'V' and tokens[3] == 'dc':
                                components['IVS'].append(Voltage_source(tokens[0],tokens[1],tokens[2],tokens[4]))
                            elif tokens[0][0] == 'V' and tokens[3] == 'ac':
                                if frequency != 0:
                                    components['IVS'].append(Voltage_source(tokens[0],tokens[1],tokens[2],tokens[4],tokens[5]))
            #If there is an ac source present and frequency is not mentioned, an error message is raised
                                else:
                                    sys.exit("Frequency not mentioned for AC source")
                            elif tokens[0][0] == 'I' and tokens[3] == 'dc':
                                components['ICS'].append(Current_source(tokens[0],tokens[1],tokens[2],tokens[4]))
                            elif tokens[0][0] == 'I'  and tokens[3] == 'ac':
                                if frequency != 0:
                                    components['ICS'].append(Current_source(tokens[0],tokens[1],tokens[2],tokens[4],tokens[5]))
                                else:
                                    sys.exit("Frequency not mentioned for AC source")
            #If elements other than R,L,C,V,I are given, an error message is raised
                            else:
                                sys.exit("Invalid component!")
            #Removing repeated nodes
                        Nodes = list(set(Nodes))
            #Creating a dictionary and assigning numbers to the nodes
                        Nodes_dict = {}
                        dummy = 0
                        for i in Nodes:
                            if i == 'GND':
                                Nodes_dict[i] = 0
                                dummy = dummy + 1
                            elif i.isalpha() and i.isdigit():
                                Nodes_dict[i] = int(i[1])
                            else:
                                Nodes_dict[i] = int(i)
            #If ground is not given in the netlist file
                        if dummy != 1:
                            sys.exit("Ground Node not mentioned")
                        else:
            # Angular Frequency omega = 2xpixfrequency
                            omega = 2*pi*frequency
                            total_nodes = len(Nodes)
                            total_VS = len(components['IVS'])
                            M = zeros((total_nodes+total_VS, total_nodes+total_VS), dtype = complex)
                            B = zeros((total_nodes+total_VS,1), dtype = complex)
                            M[0][0] = 1.0       #Ground node equation
            #Resistance connected between nodes j and k
                            for r in components['Resistors']:
                                if r.node1 != 'GND':
                                    M[Nodes_dict[r.node1]][Nodes_dict[r.node1]] += 1/r.value
                                    M[Nodes_dict[r.node1]][Nodes_dict[r.node2]] -= 1/r.value
                                if r.node2 != 'GND':
                                    M[Nodes_dict[r.node2]][Nodes_dict[r.node1]] -= 1/r.value
                                    M[Nodes_dict[r.node2]][Nodes_dict[r.node2]] += 1/r.value
            #Inductance connected between nodes j and k
                            for i in components['Inductors']:
                                if i.node1 != 'GND':
                                    M[Nodes_dict[i.node1]][Nodes_dict[i.node1]] += complex(0,-1/(omega*i.value))
                                    M[Nodes_dict[i.node1]][Nodes_dict[i.node2]] -= complex(0,-1/(omega*i.value))
                                if i.node2 != 'GND':
                                    M[Nodes_dict[i.node2]][Nodes_dict[i.node1]] -= complex(0,-1/(omega*i.value))
                                    M[Nodes_dict[i.node2]][Nodes_dict[i.node2]] += complex(0,-1/(omega*i.value))
            #Capacitance connected between nodes j and k
                            for c in components['Capacitors']:
                                if c.node1 != 'GND':
                                    M[Nodes_dict[c.node1]][Nodes_dict[c.node1]] += complex(0,omega*c.value)
                                    M[Nodes_dict[c.node1]][Nodes_dict[c.node2]] -= complex(0,omega*c.value)
                                if c.node2 != 'GND':
                                    M[Nodes_dict[c.node2]][Nodes_dict[c.node1]] -= complex(0,omega*c.value)
                                    M[Nodes_dict[c.node2]][Nodes_dict[c.node2]] += complex(0,omega*c.value)
            #Voltage sources connected between nodes j and k
                            for v in components['IVS']:
                                if v.node1 != 'GND':
                                    M[Nodes_dict[v.node1]][total_nodes+components['IVS'].index(v)] = 1.0
                                if v.node2 != 'GND':
                                    M[Nodes_dict[v.node2]][total_nodes+components['IVS'].index(v)] = -1.0
                                M[total_nodes+components['IVS'].index(v)][Nodes_dict[v.node1]] = -1.0
                                M[total_nodes+components['IVS'].index(v)][Nodes_dict[v.node2]] = 1.0
                                B[total_nodes+components['IVS'].index(v)] = complex((v.value/2)*cos(v.phase),(v.value/2)*sin(v.phase))
            #Current sources connected between nodes j and k
                            for i in components['ICS']:
                                if i.node1 != 'GND':
                                    B[Nodes_dict[i.node1]] = -1.0*complex((i.value/2)*cos(i.phase),(i.value/2)*sin(i.phase))
                                if i.node2 != 'GND':
                                    B[Nodes_dict[i.node2]] = complex((i.value/2)*cos(i.phase),(i.value/2)*sin(i.phase))
            #amplitude of the source is Vp-p(V peak to peak)/2
                            try:
                                X = linalg.solve(M,B)
                                dummy = 0
                                print("\nThe voltages at respective nodes are:\n")
                #Replacing GND with 0
                                Nodes.remove('GND')
                                Nodes.append('0')
                                Nodes.sort()
                                for n in Nodes:
                                    print("V",n," = ",X[dummy],sep='')
                                    dummy += 1
                                for v in components['IVS']:
                                    print("\nCurrent Through Voltage Source ",v.name," = ",X[dummy],sep='')
                                    dummy += 1
                            except linalg.LinAlgError:
                                print("Unable to solve the matrix!\nPlease check your input values.")
        #To avoid raising error for wrong files, use exception handling
        except IOError:
                print("Given file does not exist!")