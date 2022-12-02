#Importing all the Neccessary module
from tkinter import *
import os
from tkinter import ttk
import glob
import shutil
import ImageTk

#Create Function to clear the files in panel
def clear_dir(k):
    if k==1:
            local_cf.destroy()
            local_df.destroy()
            local_ef.destroy()
            k=0
    else:
        for i in cl_item:
            i.destroy()
        
#change the background of the files
def chg_bg(e,x,y,z):
    try:
        x.config(bg='#8cd3ff')
        y.config(bg='#8cd3ff')
        z.config(bg='#8cd3ff')
    except:
        x.config(bg='#8cd3ff')
        y=os.path.getsize(y)
        size=int(y/(1024*1024))
        if y==0:
            file_name_lbl.config(text=f'NAME: {z}')
        else:
            file_name_lbl.config(text=f'NAME: {z}')

#rechange the background of the files
def bck_bg(e,x,y,z):
    try:
        x.config(bg='systembuttonface')
        y.config(bg='systembuttonface')
        z.config(bg='systembuttonface')
    except:
        x.config(bg='systembuttonface')
        file_name_lbl.config(text='')
            
#Create Functions to back to the directory
def undo_dir(e,x):
    global undo_e
    clear_dir(k=0)
    undo_x=x
    try:
        if undo[0]==undo[1]:
            undo.remove(x)
            undo.remove(undo_x)
            goto()
        elif undo[0]!=undo[1]:
            x=undo[-2]
            undo.remove(x)
            undo.remove(undo_x)
            change_dir(e,x,y=0,k=0)
    except:
        undo.remove(x)
        goto()
#Execute the files if it is movie or music and any other files containg extention otherwise it goes to the directory
def execute_dir(e,x,y,z,k):
    if '.' in y:
        os.startfile(z)
    else:
        change_dir(e,x,y,k=0)

#Create the element to display in panel
def change_dir(e,x,y,k):
    global cl_item,cl_item_name
    clear_dir(k)
    row=0
    column=0
    cl_item=[]
    cl_item_name=[]
    undo.append(x)
    undo_btn.bind('<Button-1>',lambda e,x=x,y=0:undo_dir(e,x))
    for item in glob.glob(f'{x}\\*'):
        item_dir=item
        item_name=item.replace(f'{x}\\','')
        #assigning the image to the label
        if '.' in item_name:
            img=image_blanck
        if '.png' in item_name or '.jpg' in item_name :
            img=image_png
        elif '.pdf' in item_name:
            img=image_pdf
        elif '.zip' in item_name:
            img=image_zip
        elif '.txt' in item_name:
            img=image_txt
        elif '.mkv' in item_name or '.mp4' in item_name or '.MKV' in item_name:
            img=image_video
        elif '.mp3' in item_name or '.MP3' in item_name:
            img=image_music
        elif '.py' in item_name or '.pyz' in item_name:
            img=image_py
        elif '.' not in item_name:
            img=image_folder
        item=item_name[0:6]+'\n'+item_name[6:12]+'\n'+item_name[12:18]+'\n'
        item=Label(canva,image=img,text=item,width=40,height=90,compound='top')
        item.grid(row=row,column=column,padx=10,pady=10)
        #binding the label
        item.bind('<Enter>',lambda e,x=item,y=item_dir,z=item_name:chg_bg(e,x,y,z))
        item.bind('<Leave>',lambda e,x=item,y=item_dir,z=None,:bck_bg(e,x,y,z))
        item.bind('<Double-1>',lambda e,x=f'{x}/{item_name}',y=item_name,z=item_dir,k=0:execute_dir(e,x,y,z,k))
        #win.update() is neccessary because it save the data of the variable
        win.update()
        #To assign the place of the labels
        column+=1
        cl_item.append(item)
        cl_item_name.append(item_name)
        if column==20:
            row+=1
            column=0
        
        
        
        
#To create the Window
win=Tk()
win.title("Filemanager")
win.state('zoomed')
win.resizable(False,False)

#Importing image to the program
image_folder='assets/folder.png'
image_music='assets/music file.png'
image_pdf='assets/pdf.png'
image_txt='assets/txt.png'
image_video='assets/video.png'
image_zip='assets/zip.png'
image_undo='assets/undo.png'
image_png='assets/png.png'
image_blanck='assets/blanck.png'
image_py='assets/py.png'

#scroll bar
scroll_r=ttk.Scrollbar(win)
scroll_r.pack(side=RIGHT,fill=Y)

scroll_d=ttk.Scrollbar(win,orient=HORIZONTAL)
scroll_d.pack(side=BOTTOM,fill=X)

#creating canvas
canvas=Canvas(win,yscrollcommand=scroll_r.set,xscrollcommand=scroll_d.set)
canvas.pack(fill=BOTH,expand=1)

canva=Frame(canvas)
#binding the canvas to scrollbar
canva.bind('<Configure>',lambda e:canvas.configure(scrollregion=canvas.bbox('all')))

canvas.create_window((0,0),window=canva,anchor='nw')

scroll_r.config(command=canvas.yview)
scroll_d.config(command=canvas.xview)
#creating the file for file information 
file_info_frame=Frame(win)
file_info_frame.place(x=0,y=675)

undo_btn_frame=Frame(file_info_frame)
undo_btn_frame.pack(side=LEFT)
undo_btn_frame2=Frame(undo_btn_frame)
undo_btn_frame2.pack(side=RIGHT)
file_name_lbl=Label(undo_btn_frame2)
file_name_lbl.pack(side=LEFT)

image_folder=PhotoImage(file=image_folder)
image_music=PhotoImage(file=image_music)
image_pdf=PhotoImage(file=image_pdf)
image_txt=PhotoImage(file=image_txt)
image_video=PhotoImage(file=image_video)
image_zip=PhotoImage(file=image_zip)
image_undo=PhotoImage(file=image_undo)
image_png=PhotoImage(file=image_png)
image_py=PhotoImage(file=image_py)
image_blanck=PhotoImage(file=image_blanck)

undo=[]

undo_btn=Label(undo_btn_frame,text='UNDO',image=image_undo,compound='top')
undo_btn.pack(side=LEFT,expand=1)


def goto():
    global local_cf,local_df,local_ef
    #local disk c
    local_cf=Frame(canva,border=2)
    local_cf.grid(row=0,column=0,pady=20,padx=20)
    loc_c=Label(local_cf,text='Local Disk(C):',fg='black')
    loc_c.pack()
    #configure storage of local disk c
    total_c,used_c,free_c=shutil.disk_usage("C:/")
    total_c=total_c //(2**30)
    used_c=used_c//(2**30)
    free_c=free_c//(2**30)
    #progressbar for local disk c
    pro_c=ttk.Progressbar(local_cf,orient=HORIZONTAL,length=200,maximum=total_c,value=used_c)
    pro_c.pack()
    local_c_stor=Label(local_cf,text="%d GB free of %d GB"%(free_c,total_c))
    local_c_stor.pack()
    #binding local disk to c
    local_cf.bind('<Enter>',lambda e,x=local_cf,y=loc_c,z=local_c_stor:chg_bg(e,x,y,z))
    local_cf.bind('<Leave>',lambda e,x=local_cf,y=loc_c,z=local_c_stor:bck_bg(e,x,y,z))
    loc_c.bind('<Double-1>',lambda e,x='C:',y=1,k=1:change_dir(e,x,y))
    local_c_stor.bind('<Double-1>',lambda e,x='C:',y=1,k=1:change_dir(e,x,y,k))
    pro_c.bind('<Double-1>',lambda e,x='C:',y=1,k=1:change_dir(e,x,y,k))
    local_cf.bind('<Double-1>',lambda e,x='C:',y=1,k=1:change_dir(e,x,y,k))

    #local disk d
    local_df=Frame(canva,border=2)
    local_df.grid(row=0,column=1,pady=20,padx=20)
    loc_d=Label(local_df,text='Local Disk(D):',fg='black')
    loc_d.pack()

    #configure storage of local disk d
    total_d,used_d,free_d=shutil.disk_usage("D:/")
    total_d=total_d //(2**30)
    used_d=used_d//(2**30)
    free_d=free_d//(2**30)
    #progressbar for local disk d
    pro_d=ttk.Progressbar(local_df,orient=HORIZONTAL,length=200,maximum=total_d,value=used_d)
    pro_d.pack()
    local_d_stor=Label(local_df,text="%d GB free of %d GB"%(free_d,total_d))
    local_d_stor.pack()
    #binding local disk d to mouse
    local_df.bind('<Enter>',lambda e,x=local_df,y=loc_d,z=local_d_stor:chg_bg(e,x,y,z))
    local_df.bind('<Leave>',lambda e,x=local_df,y=loc_d,z=local_d_stor:bck_bg(e,x,y,z))
    loc_d.bind('<Double-1>',lambda e,x='D:',y=1,k=1:change_dir(e,x,y,k))
    local_d_stor.bind('<Double-1>',lambda e,x='D:',y=1,k=1:change_dir(e,x,y,k))
    pro_d.bind('<Double-1>',lambda e,x='D:',y=1,k=1:change_dir(e,x,y,k))
    local_df.bind('<Double-1>',lambda e,x='D:',y=1,k=1:change_dir(e,x,y,k))
    
    #local disk e
    local_ef=Frame(canva,border=2)
    local_ef.grid(row=0,column=2,pady=20,padx=20)
    loc_e=Label(local_ef,text='Local Disk(E):',fg='black')
    loc_e.pack()

    #configure storage of local disk e
    total_e,used_e,free_e=shutil.disk_usage("E:/")
    total_e=total_e //(2**30)
    used_e=used_e//(2**30)
    free_e=free_e//(2**30)
    #progressbar for local disk e
    pro_e=ttk.Progressbar(local_ef,orient=HORIZONTAL,length=200,maximum=total_e,value=used_e)
    pro_e.pack()
    local_e_stor=Label(local_ef,text="%d GB free of %d GB"%(free_e,total_e))
    local_e_stor.pack()
    #binding local disk e to mouse
    local_ef.bind('<Enter>',lambda e,x=local_ef,y=loc_e,z=local_e_stor:chg_bg(e,x,y,z))
    local_ef.bind('<Leave>',lambda e,x=local_ef,y=loc_e,z=local_e_stor:bck_bg(e,x,y,z))
    loc_e.bind('<Double-1>',lambda e,x='E:',y=1,k=1:change_dir(e,x,y,k))
    local_e_stor.bind('<Double-1>',lambda e,x='E:',y=1,k=1:change_dir(e,x,y,k))
    pro_e.bind('<Double-1>',lambda e,x='E:',y=1,k=1:change_dir(e,x,y,k))
    local_ef.bind('<Double-1>',lambda e,x='E:',y=1,k=1:change_dir(e,x,y,k))
    
goto()
