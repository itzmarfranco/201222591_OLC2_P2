if __name__=='__main__':
	from Graphics import Tkinter as tk

else:
	from .Graphics import Tkinter as tk

class InterpreterFunctions:
    def __init__(self, text):
        self.text = text
        self.create_binding_keys()
        self.binding_functions_config()
        self.join_function_with_main_stream()

    def create_binding_keys(self):
        for key in ["<Control-r>","<Control-R>"]:
            self.text.master.bind(key, self.interpretar)
        return

    def join_function_with_main_stream(self):
        self.text.storeobj['Interpretar']   =  self.interpretar
        return

    def binding_functions_config(self):
        self.text.tag_configure("sel", background="skyblue")
        self.text.configure(undo=True,autoseparators=True, maxundo=-1)
        return

    def interpretar(self, event=None):
        #showinfo("Notepad","Interpretando...")
        from .grammar import analize
        #from .gramatica_ast import analizador_ast

        text = self.text.get("1.0",'end')
        
        ast = analize(text)
        #salida_ast = analizador_ast(entrada)

        return

if __name__ == '__main__':
    root = Tkinter.Tk()
    pad = Tkinter.Text(root,wrap='none')
    pad.storeobj = {}
    InterpreterFunctions(pad)
    pad.pack()
    root.mainloop()
