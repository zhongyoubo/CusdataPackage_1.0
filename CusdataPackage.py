from doctest import master
from select import select
import tkinter as tk
from tkinter import Button, ttk
from turtle import width
import openpyxl


class LoginFrame(tk.Frame):
    def __init__(self,master=None):
     #Frame 是父类，需主动调用父类的构造器
        super().__init__(master) #显示调用父类的构造方法
        print("LoginFrame init")
        self.pack(pady=10)
        self.master = master
        self.hostname = tk.StringVar()
        self.hostname.set(g_HostName)
        self.username = tk.StringVar()
        self.username.set(g_UserName)
        self.password = tk.StringVar()
        self.password.set(g_PassWord)

        self.createWidgets()

    def createWidgets(self):
        print("LoginFrame createWidgets")
        self.hostname_label = ttk.Label(self,text="HostName",width=10)
        self.hostname_label.grid(row=0,column=0,sticky="we")
        
        self.hostname_entry = ttk.Entry(self,textvariable=self.hostname)
        self.hostname_entry.grid(row=0,column=1,sticky="we")
        self.username_label = ttk.Label(self,text="UserName")
        self.username_label.grid(row=1,column=0,sticky="we",pady=5)
        
        self.username_entry = ttk.Entry(self,textvariable=self.username)
        self.username_entry.grid(row=1,column=1,sticky="we",pady=5)
        self.password_label = ttk.Label(self,text="Password")
        self.password_label.grid(row=2,column=0,sticky="we")
        
        self.password_entry = ttk.Entry(self,textvariable=self.password)
        self.password_entry.grid(row=2,column=1,sticky="we")
        self.login_button = ttk.Button(self,text="Login",command=self.login_check)
        self.login_button.grid(row=0,column=3,rowspan=3,sticky="ns",padx=20)

    def login_check(self):
        print("login check,hostname:",self.hostname.get(),"username:",self.username.get(),"password:",self.password.get())


class BuildFrame(tk.Frame): #继承Frame类
    def __init__(self,master=None):
        #Frame 是父类，需主动调用父类的构造器
        super().__init__(master) #显示调用父类的构造方法
        print("BuildFrame init")
        self.pack()
        self.master = master
        self.region = tk.StringVar()
        self.region.set(g_Region)
        self.version = tk.StringVar()
        self.version.set(g_Version)
        self.createWidgets()

    def createWidgets(self):
        print("BuildFrame createWidgets")
        self.region_label = ttk.Label(self,text="Region")
        self.region_label.grid(row=0,column=0,sticky="we")
        
        self.region_cbb = ttk.Combobox(self,textvariable=self.region,values=g_Region_List) #下拉列表的值
        self.region_cbb.bind("<<ComboboxSelected>>",self.select_region)
        self.region_cbb.grid(row=0,column=1,sticky="we")
        self.version_label = ttk.Label(self,text="Version")
        self.version_label.grid(row=1,column=0,sticky="we")
        
        self.version_cbb = ttk.Combobox(self,textvariable=self.version,values=list(g_Version_Path.keys()))
        self.version_cbb.bind("<<ComboboxSelected>>",self.select_version)
        self.version_cbb.grid(row=1,column=1,sticky="we")

        self.build_button = ttk.Button(self,text="Build",command=self.check_build)
        self.build_button.grid(row=0,column=3,padx=20)
        self.cancel_button = ttk.Button(self,text="Cancel",command=self.check_cancel)
        self.cancel_button.grid(row=1,column=3,padx=20)

    def select_region(self,event):
        print("Region",self.region.get(),"is selected")
        global g_Region
        g_Region = self.region.get()

    def select_version(self,event):
        print("Version",self.version.get(),"is Selected")
        global g_Version
        g_Version = self.version.get()

    def check_build(self):
        print("Start Build, Region:",g_Region," Version:",g_Version,"CodePath:",g_Version_Path[g_Version])
    
    def check_cancel(self):
        print("Cancel Build")
        

 #从DataConfig.xlsx获取信息
def loadDataConfig():
    wb = openpyxl.load_workbook("./DataConfig.xlsx")
    ws = wb.active
    global g_Region_List
    g_Region_List = ["AP","EU","SA","NA"]
    global g_HostName,g_UserName,g_PassWord,g_Project,g_Region,g_Version #软件或者tarball版本，如R0,R1
    g_HostName = ws["B1"].value
    g_UserName = ws["B2"].value
    g_PassWord = ws["B3"].value
    g_Project = ws["B4"].value
    g_Region = ws["B5"].value
    
    print("g_HostName:",g_HostName,"g_UserName:",g_UserName,"g_PassWord:",g_PassWord)
    print("g_Project:",g_Project,"g_Region:",g_Region)
    global g_Version_Path #软件版本与CodePath映射表
    g_Version_Path = {}
    for row in range(6,ws.max_row+1):
        print(ws[f"A{row}"].value,ws[f"B{row}"].value)
        v = ws[f"A{row}"].value
        p = ws[f"B{row}"].value
        g_Version_Path.update({v:p})
    print("g_Version_Path:",g_Version_Path)
    g_Version = list(g_Version_Path.keys())[0] #先默认在第一个软件版本路径





if __name__ == "__main__":
    print("lanuch application of 9216 Cusdata Package Tool")
    root = tk.Tk()
    screen_w,screen_h = root.maxsize()
    win_w = 400
    win_h = 180
    x,y = int((screen_w-win_w)/2),int((screen_h-win_h)/2)
    print("screen_w",screen_w,"screen_h",screen_h,"win_w",win_w,"win_h",win_h,"x",x,"y",y)
    root.geometry("{}x{}+{}+{}".format(win_w,win_h,x,y))
    root.title('9216 Cusdata Package Tool')
    loadDataConfig()
    login_frame = LoginFrame(master=root)
    build_frame = BuildFrame(master=root)

    root.mainloop()
