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
