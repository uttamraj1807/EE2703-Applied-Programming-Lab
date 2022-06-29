"""
   EE2703 Applied Programming Lab - 2022
        Assignment 1 by EE20B118
"""
import sys
#Defining a dictionary for each element names
elements = {
        "R" : "Resistor",
        "L" : "Inductor",
        "C" : "Capacitor",
        "V" : "Independent Volatge source",
        "I" : "Independent Current Source",
        "E" : "Voltage Controlled Voltage Source",
        "F" : "Voltage Controlled Current Source",
        "G" : "Current Controlled Voltage Source",
        "H" : "Current Controlled Current Source"
}
#Defining a function that analyze the tokens and determine the from node, the to node, the type of element and value
def line_to_tokens(Lines):
    Tokens = Lines.split('#')[0].split()
    # R, L, C, Independent Sources
    if(len(Tokens) == 4):
        elementName = elements[Tokens[0][0]]
        node1 = Tokens[1]
        node2 = Tokens[2]
        value = Tokens[3]
        print(f"""Type of element : {elementName}
node1 : {node1}
node2 : {node2}
value : {value}""" )

    # Current controlled sources
    elif(len(Tokens) == 5):
        elementName = elements[Tokens[0][0]]
        node1 = Tokens[1]
        node2 = Tokens[2]
        voltageSource = Tokens[3]
        value = Tokens[4]
        print(f"""Type of element : {elementName}
node1 : {node1}
node2 : {node2}
Voltage Source: {voltageSource}
value : {value}""")

    # Voltage controlled sources
    elif(len(Tokens) == 6):
        elementName = elements[Tokens[0][0]]
        node1 = Tokens[1]
        node2 = Tokens[2]
        voltageSourceNode1 = Tokens[3]
        voltageSourceNode2 = Tokens[4]
        value = Tokens[5]
        print(f"""Type of element : {elementName}
node1 : {node1}
node2 : {node2}
Voltage Source Node 1 : {voltageSourceNode1}
Voltage Source Node 2 : {voltageSourceNode2}
value : {value}""")
    else:
        return []

if __name__ == "__main__":

    # checking number of command line arguments
    if len(sys.argv)!=2 :
        sys.exit("Usage: .py_file netlist_file")
    else:
        try:
            FileName = sys.argv[1]
            # checking if given netlist file is of correct type
            if (not FileName.endswith(".netlist")):
                print("Enter the correct format file")
            else:
            # initializing beginning and ending variables with negative numbers 
                beginning = -1
                ending = -2
                with open (FileName, "r") as f:
                    lines = f.readlines()
                    for line in lines:
            #If .circuit and .end exists their line indexes overwrites beginning and ending 
                            if ".circuit"==line[0:8]:
                                    beginning = lines.index(line)
                            elif ".end" == line[0:4]:
                                    ending = lines.index(line)
            #If any of the .circuit and .end doesnt exists or they are inverted, warning message is printed
                    if beginning >= ending or beginning < 0 or ending < 0:
                            sys.exit("Make sure to have .circuit and .end lines in the file in correct order.")
                    else:
            #Removing the comments, reversing the lines and printing the lines in reverse order
                            print("\nReversing the lines and printing them in the reverse order:\n")
                            for i in reversed([' '.join(reversed(j.split('#')[0].split())) for j in lines[beginning+1:ending]]):
                                    print(i)
            #Printing the analysis of each lines
                            print("\nDeterming tokens in each line:\n")
                            for i in lines[beginning+1:ending]:
                                    line_to_tokens(i)
        #To avoid raising error for wrong files, use exception handling
        except IOError:
                print("Given file does not exist!")