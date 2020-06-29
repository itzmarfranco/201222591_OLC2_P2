import sys
import os
from graphviz import Graph

from magicsticklibs import Main

root = Main.TextPad_Window(className = " MinorC")
os.system('cls')
print('########################## Minor C ##########################')

f = open('3d.augus', 'w')
f.write('main:\n')
f.close()

f = open('3d.augus', 'a+')
f.write('label1:\n')
f.close()

root.mainloop()