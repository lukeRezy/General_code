


from tkinter import *

class applicationQuitframe(Frame):
    
    def createQuit(self):
        self.QUIT = Button(self)#.grid(row = 1, column = 3)
        self.QUIT["text"] = "OK"
        self.QUIT["fg"]   = "red"
        self.QUIT["command"] =  self.quit

        self.QUIT.pack({"anchor": "se"})  
        
    def __init__(self, master=None):
        Frame.__init__(self, master, relief=GROOVE,width=50,height=100,bd=1)
        self.createQuit()

def myfunction(event):
    canvas.configure(scrollregion=canvas.bbox("all"),width=200,height=200)

if __name__ == '__main__':
    all_dir = ["hello/yep", "goodbuy/nope"]
    
    root=Tk()
    #sizex = 400
    #sizey = 300
    #posx  = 100
    #posy  = 100
    #root.wm_geometry("%dx%d+%d+%d" % (sizex, sizey, posx, posy))
    
    #myframe=Frame(root,relief=GROOVE,width=50,height=100,bd=1)
    myframe=applicationQuitframe
    myframe.place(x=10,y=10)
    
    canvas=Canvas(myframe)
    frame=Frame(canvas)
    myscrollbar=Scrollbar(myframe,orient="vertical",command=canvas.yview)
    canvas.configure(yscrollcommand=myscrollbar.set)
    
    myscrollbar.pack(side="right",fill="y")
    canvas.pack(side="left")
    canvas.create_window((0,0),window=frame,anchor='nw')
    frame.bind("<Configure>",myfunction)  
    
    root.lift()
    root.attributes('-topmost',True)
    root.after_idle(root.attributes,'-topmost',False)
    root.mainloop()
    #root.destroy()
    #print(check_dirs)
