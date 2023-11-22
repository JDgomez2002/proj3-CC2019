# Teoria de computacion CC2019
# Gonzalo Santizo 
# Jose Daniel Gomez

import copy
import yaml

class Colors:
  CLEAR = '\033[0m'
  RED = '\033[91m'
  GREEN = '\033[92m'
  BLUE = '\033[94m'
  BOLD = '\033[1m'
  UNDERLINE = '\033[4m'

class Tape(object):
  blankSymbol = " "
  def __init__(self, stringTape = "", blank=" "):
    self.__tape = dict((enumerate(stringTape)))
    Tape.blankSymbol = blank

  def __str__(self):
    s = ""
    minimumUsedIndex = min(self.__tape.keys()) 
    maximumUsedIndex = max(self.__tape.keys())
    for i in range(minimumUsedIndex, maximumUsedIndex+1):
      s += self.__tape[i]
    return s

  def __getitem__(self,index):
    if index in self.__tape:
      return self.__tape[index]
    else:
      return Tape.blankSymbol

  def __setitem__(self, pos, char):
    self.__tape[pos] = char

class TuringMachine(object):

  def __init__(
    self,
    tapes = list[str],
    blankSymbol = " ",
    initialState = "",
    finalStates = None,
    transitionFunction = None,
    acceptedStates = None
  ):
    self.__init = initialState
    self.tapes = tapes
    self.__curr = 0
    self.__blankSymbol = blankSymbol
    self.__tape = Tape(tapes[self.__curr],self.__blankSymbol)
    self.__headPosition = 0
    self.__currentState = initialState
    self.__immediate_description = None
    self.__acceptedStates = acceptedStates
    if transitionFunction == None:
      self.__transitionFunction = {}
    else:
      self.__transitionFunction = transitionFunction
    if finalStates == None:
      self.__finalStates = set()
    else:
      self.__finalStates = set(finalStates)
  
  def nextStringAvailable(self):
    self.__curr += 1
    if self.__curr < len(self.tapes):
      self.__tape = Tape(self.tapes[self.__curr],self.__blankSymbol)
      self.__headPosition = 0
      self.__currentState = self.__init
      self.__immediate_description = None
      return True
    else:
      return False

  def getTape(self): 
    return str(self.__tape)
  
  
  def step(self):
    char_under_head = self.__tape[self.__headPosition]
    self.generateDescription(True)
    x = (self.__currentState, char_under_head)
    if x in self.__transitionFunction:
      y = self.__transitionFunction[x]
      self.__tape[self.__headPosition] = y[1]
      if y[2] == "R":
        self.__headPosition += 1
      elif y[2] == "L":
        self.__headPosition -= 1
      self.__currentState = y[0]        
    self.generateDescription(False)

  def final(self):
    if self.__currentState in self.__finalStates:
      return True
    else:
      return False

  def generateDescription(self, first:bool):
    if (first):
      self.__immediate_description = copy.deepcopy(self.__tape)
      self.__immediate_description[self.__headPosition]= Colors.RED +  self.__currentState + Colors.CLEAR +self.__immediate_description[self.__headPosition]
    else:
      immediate_description = copy.deepcopy(self.__tape)
      immediate_description[self.__headPosition]= Colors.RED +  self.__currentState + Colors.CLEAR+self.__immediate_description[self.__headPosition]
      print(str(self.__immediate_description)+" -> "+str(immediate_description))

  def runMachine(self):
    machineNumber = self.__curr
    if machineNumber == 0:
      machineNumber = 0

    initialTape = "\nInput -> " + Colors.GREEN + self.getTape() + Colors.CLEAR
    print(Colors.BOLD + "\n$ String #" + str(machineNumber+1) + ": " + Colors.CLEAR + Colors.UNDERLINE + self.getTape() + Colors.CLEAR + "\n" )
    
    while not self.final():
      self.step()

    print(initialTape)
    print("Output ->", end=" ")
    tape = self.getTape()
    tape = tape.replace(self.__blankSymbol, '')
    print(Colors.GREEN + tape + Colors.CLEAR)

    if (self.__acceptedStates):
      if self.__currentState in self.__acceptedStates:
        print(Colors.BLUE + "Accepted string!" + Colors.CLEAR)
      else:
        print(Colors.RED + "String not accepted!" + Colors.CLEAR)

    machineNumber += 1

    if self.nextStringAvailable():
      print("\n************************************************")
      self.runMachine()
    else:
      print()
      return # end of the machine

def createTuringMachine(filename) -> TuringMachine:
  with open(filename, 'r') as yaml_file:
    data = yaml.load(yaml_file, Loader = yaml.FullLoader)
    initial = data['q_states']['initial']
    final = {val for val in data['q_states']['final']}
    acc = {val for val in data['q_states']['accept']}
    blankSymbol = data['blank']
    transitionFunction = {}
    simulationStrings = data['simulation_strings']
    for params in data['delta']:
      transitionFunction[(params['params']['initial_state'], params['params']['tape_input'])] = (params['output']['final_state'], params['output']['tape_output'], params['output']['tape_displacement'])
    return TuringMachine(simulationStrings, blankSymbol, initial, final, transitionFunction, acc)

# MAIN
print("\n************************************************")
print("************ TURING MACHINE 1 ******************")
print("************************************************")
turingMachine1 = createTuringMachine("./TM1.yaml")
turingMachine1.runMachine()

print("************************************************")
print("************ TURING MACHINE 2 ******************")
print("************************************************")
turingMachine2 = createTuringMachine("./TM2.yaml")
turingMachine2.runMachine()

print("************************************************\n")
