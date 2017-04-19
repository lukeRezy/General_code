


from tkinter import *

def ask_box(all_dir):
    
    go_to_dirs = []
    
    class Application(Frame):
    
        def createQuit(self):
            self.QUIT = Button(self)
            self.QUIT["text"] = "OK"
            self.QUIT["fg"]   = "red"
            self.QUIT["command"] =  root.destroy
    
            self.QUIT.pack({"anchor": "se"})
            
        def createCheckBox(self, directories):
            
            count = 0
            
            for one_dir in all_dir:
                directories[count] = IntVar()
                self.ChkBox = Checkbutton(self)
                self.ChkBox["text"] = one_dir
                self.ChkBox["variable"] = directories.get(count)
                self.ChkBox["onvalue"] = 1
                self.ChkBox["offvalue"] = 0
                self.ChkBox["height"] = 5
                self.ChkBox["height"] = 5
                self.ChkBox["width"] = 20
        
                self.ChkBox.grid(row=count, column=0, sticky=N+S)
                self.ChkBox.pack()
                count+=1            
    
        def __init__(self, master=None):
            Frame.__init__(self, master)
            Application.directories = {}
            
            self.grid_rowconfigure(0, weight=1)
            self.grid_columnconfigure(0, weight=1)            
            
            self.pack({"anchor": "nw"})
            self.createCheckBox(self.directories)
            self.createQuit()
    
    root = Tk()
    root.resizable(width=False, height=False)
    root.title("Select directories to monitor:")
    
    myframe=Frame(root,relief=GROOVE,bd=1)
   
    myframe.grid_rowconfigure(0, weight=1)
    myframe.grid_columnconfigure(0, weight=1)
    
    yscrollbar = Scrollbar(myframe)
    yscrollbar.grid(row=0, column=1, sticky=N+S)
    
    canvas = Canvas(myframe, bd=0, yscrollcommand=yscrollbar.set)
    
    canvas.grid(row=0, column=0, sticky=N+S+E+W)
    yscrollbar.config(command=canvas.yview)    

    frame=Application(master=canvas)
    canvas.create_window(0, 0, window=frame, anchor="w")
    
    width_canv = -10
    height_root = 25
    
    if len(all_dir) < 3:
        width_canv -= len(all_dir) * 40
        height_root += len(all_dir) * 100
        canvas.configure(scrollregion=(0, width_canv, 0, (height_root + width_canv)))
        root.geometry('{}x{}'.format(500, height_root))
        canvas.config(width = 500, height = height_root)
    else:
        width_canv -= len(all_dir) * 45
        height_root += len(all_dir) * 92
        canvas.configure(scrollregion=(0, width_canv, 0, (height_root + width_canv)))
        root.geometry('{}x{}'.format(500, 225))
        canvas.config(width = 500, height = height_root)       
        
        
    canvas.xview_moveto(0)
    canvas.yview_moveto(0)
                    
    myframe.bbox('all')
    myframe.pack()

    root.lift()
    root.attributes('-topmost',True)
    root.after_idle(root.attributes,'-topmost',False)
    root.mainloop()
    
    for key in Application.directories.items():
        if key[1].get() == 1:
            go_to_dirs.append(all_dir[key[0]])
    
    return(go_to_dirs)

if __name__ == '__main__':
    #all_dir = ["helloyep"]
    #all_dir = ["helloyep", "yeana"]
    all_dir = ["helloyep", "yeana", "bazinga"]
    #all_dir = ["helloyep", "yeana", "bazinga", "youza"]
    #all_dir = ["helloyep", "yeana", "bazinga", "youza", "bingodingo", "jjjj", "kkkk",1,2,3,4,5,6,7,8,9,0,1,2,3,4,5,67,8,9,7]
    check_dirs = ask_box(all_dir)
    print(check_dirs)