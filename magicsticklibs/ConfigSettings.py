if __name__=='__main__':
	from LineNumber import LineMain
	from ScrollBar import Scrollbar
	from StationeryFunctions import StationeryFunctions
	from PopupMenu import Popup
	from FIndAndReplace import FindReplaceFunctions
	from FileHandler import FileHandler
	from FontChooser import FontChooser
	from Settings import Configuration
	from ColorLight import ColorLight
	from MenuBarHandler import MenuBar
	from autotyping import AutoWrite
	from interpretar import InterpreterFunctions
else:
	from .LineNumber import LineMain
	from .ScrollBar import Scrollbar
	from .StationeryFunctions import StationeryFunctions
	from .PopupMenu import Popup
	from .FIndAndReplace import FindReplaceFunctions
	from .FileHandler import FileHandler
	from .FontChooser import FontChooser
	from .Settings import Configuration
	from .ColorLight import ColorLight
	from .MenuBarHandler import MenuBar
	from .autotyping import AutoWrite
	from .interpretar import InterpreterFunctions

class Connect:
	def __init__(self, pad):
		self.pad = pad
		self.modules_connections()


	def modules_connections(self):
		LineMain(self.pad)
		Scrollbar(self.pad)
		StationeryFunctions(self.pad)
		Popup(self.pad)
		FindReplaceFunctions(self.pad)
		InterpreterFunctions(self.pad)
		FileHandler(self.pad)
		FontChooser(self.pad)
		Configuration(self.pad)
		ColorLight(self.pad)
		MenuBar(self.pad)
		#AutoWrite(self.pad)
		return