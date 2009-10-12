from direct.directbase import DirectStart
from direct.task.Task import *
from pandac.PandaModules import *
from direct.showbase.DirectObject import *

class Kontrollit(DirectObject):

   def __init__(self):
      
      self.accept("arrow_up" , self.KeyDo, [1])
      self.accept("arrow_up-repeat" , self.KeyDo, [2])
      self.accept("arrow_down" , self.KeyDo, [3])
      self.accept("arrow_down-repeat" , self.KeyDo, [4])
      self.accept("arrow_left" , self.KeyDo, [5])
      self.accept("arrow_left-repeat" , self.KeyDo, [6])
      self.accept("arrow_right" , self.KeyDo, [7])
      self.accept("arrow_right-repeat" , self.KeyDo, [8])
      
      
   def KeyDo(task, key):
   
      if key==1:
         print "Up"
      if key==2:
         print"Up repeat"
      if key==3:
         print "Down"
      if key==4:
         print"Down repeat"
      if key==5:
         print "Left"
      if key==6:
         print"Left repeat"
      if key==7:
         print "Right"
      if key==8:
         print"Right repeat"
      
      return Task.done