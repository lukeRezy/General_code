


from tkinter import *

def ask_box(all_dir):
    
    go_to_dirs = []
    
    class Application(Frame):
    
        def createQuit(self):
            self.QUIT = Button(self)
            self.QUIT["text"] = "OK"
            self.QUIT["fg"]   = "red"
            self.QUIT["command"] =  self.quit
    
            self.QUIT.pack({"anchor": "se"})
            
        def createCheckBox(self, directories):
            
            count = 0
            
            for one_dir in all_dir:
                directories[count] = IntVar()
                self.ChkBox = Checkbutton(self)
                self.ChkBox["text"] = all_dir[count]
                self.ChkBox["variable"] = directories.get(count)
                self.ChkBox["onvalue"] = 1
                self.ChkBox["offvalue"] = 0
                self.ChkBox["height"] = 5
                self.ChkBox["height"] = 5
                self.ChkBox["width"] = 20
        
                self.ChkBox.pack()
                count+=1            
    
        def __init__(self, master=None):
            Frame.__init__(self, master)
            Application.directories = {}
            self.pack()
            self.createCheckBox(self.directories)
            self.createQuit()
    
    root = Tk()
    app = Application(master=root)
    root.lift()
    root.attributes('-topmost',True)
    root.after_idle(root.attributes,'-topmost',False)
    root.mainloop()
    root.destroy()
    
    for key in Application.directories.items():
        if key[1].get() == 1:
            go_to_dirs.append(all_dir[key[0]])    
    
    return(go_to_dirs)

if __name__ == '__main__':
    all_dir = ["hello/yep", "goodbuy/nope"]
    check_dirs = ask_box(all_dir)
    print(check_dirs)