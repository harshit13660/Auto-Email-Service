#---------------------------------------------Modules------------------------------------------------#

from email import message
from email.message import EmailMessage
import smtplib
from tkinter import *
from tkinter import filedialog
import pandas as pd
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from PIL import ImageTk
import os
import io
import threading
from tkinter import messagebox
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

os.chdir(f"{os.getcwd()}\\data")
#---------------------------------------------Window Setup-------------------------------------------#
root = Tk()
root.geometry("604x400")
root.title('Auto Certificate Distribution')
root.resizable(width=False, height=False)

bg = Image.open('back.jpg')
resized = bg.resize((600, 400), Image.ANTIALIAS)
img_backg = ImageTk.PhotoImage(resized)
back_img = Label(root, image=img_backg)
back_img.place(x=0, y=0)

#---------------------------------------initialization------------------------------------------#

prew_img = Image.open('prew_b.png')
resize_prew_img = prew_img.resize((90, 90))
final_prew = ImageTk.PhotoImage(resize_prew_img)

file_prew_img = Image.open('file_prew.png')
resize_file_prew_img = file_prew_img.resize((90, 90))
final_file_prew_img = ImageTk.PhotoImage(resize_file_prew_img)

send_img = Image.open('send.jpg')
resize_send_img = send_img.resize((70, 70))
final_send_img = ImageTk.PhotoImage(resize_send_img)

peopl_list = []
x=0
y=0
x1=0
y1=0

#-------------------------------------------Functions---------------------------------------------#

def file_but():
    global del_up_lab

    def del_frame():
        root.file_csv = ""
        up_frame.destroy()
        F_preview.pack_forget()
        file_button.place(x=295, y=75)
        send_button.place_forget()
        peopl_list.clear()
        track_label.place_forget()

    root.file_csv = filedialog.askopenfile(
        initialdir='C:\Program Files', title="Select a File ", filetypes=[("Excel files", ".xlsx .xls")])
    ex_file = pd.ExcelFile(root.file_csv.name)
    lo = ex_file.parse('Sheet1')
    for i, j in lo.iterrows():
        raw = {i: {"name": j.Name, "course": j.Course, "email": j.Email}}
        peopl_list.append(raw)
    print(peopl_list)
    up_frame = Frame(root, width=100, height=100, background='#08559f')
    up_frame.place(x=200, y=75)

    up_lab=Label(up_frame, text=root.file_csv.name, background='#08559f',fg='white')
    up_lab.grid(row=0, column=0,)

    del_up_lab=Button(up_frame, text="X", command=del_frame, padx=10, background='#08559f',fg='white')
    del_up_lab.grid(row=0, column=2, padx=10, pady=10)

    F_preview.config(command=lambda: fil_prew(root.file_csv.name))
    F_preview.pack(side=RIGHT, anchor=SE, padx=20, pady=20)

    file_button.pack_forget()
    send_button.place(x=260,y=150)


def prew(certi_para,x_offset,y_offset,x1_offset,y1_offest):
    global x,y,x1,y1
    x=x_offset
    y=y_offset
    x1=x1_offset
    y1=y1_offest
    img=Image.open(certi_para)
    I1=ImageDraw.Draw(img)
    myFont=ImageFont.truetype('Sail-Regular.ttf', 40,)
    I1.text((x, y), "Toshika Varshney", font=myFont, fill=(0, 0, 0))
    I1.text((x1, y1), "Resume Builder", font=myFont, fill=(0, 0, 0))
    img.show()

def final_name_set(certi_para,x,y,x1,y1,name,cour):
    img=Image.open(certi_para).convert('RGB')
    I1=ImageDraw.Draw(img)
    myFont=ImageFont.truetype('Sail-Regular.ttf', 40,)
    I1.text((x, y), name, font=myFont, fill=(0, 0, 0))
    I1.text((x1, y1), cour, font=myFont, fill=(0, 0, 0))
    # rgb_im = img.convert('RGB')
    buffer = io.BytesIO()
    img.save(buffer, format='JPEG', quality=100)
    desiredObject = buffer.getbuffer()
    return desiredObject


def fil_prew(file):
    os.startfile(file)


def up_cert():
    global f_loc
    root.file_certi=filedialog.askopenfile(
        initialdir='C:\Program Files', title="Select a File ", filetypes=[("jpg", "jpg , png")])
    f_loc=root.file_certi.name
    c_preview.config(command=lambda: prew(root.file_certi.name,x,y,x1,y1))
    c_preview_frame.pack(side=LEFT, anchor=S, padx=10, pady=10)

def set_xy_func(x,y,x1,y1):
    lis=[x,y,x1,y1]
    for i in lis:
        if i.isdigit()==False:
            x_Entry.delete(0,END)
            y_Entry.delete(0,END)
            x1_Entry.delete(0,END)
            y1_Entry.delete(0,END)
            break
        else:
            c_preview.config(command=lambda:prew(f_loc,int(x),int(y),int(x1),int(y1)))


def send_func():
    

    def set_sub_content(win,s,c):
        global sub,cont
        sub=s
        cont=c
        print(s,c)
        threading.Thread(target=lambda:finally_send(win)).start()
        


    def get_sub_con(top):
        top.destroy()
        top_window=Toplevel()
        top_window.geometry("604x300")
        top_window.title('Email-Configure')
        top_window.resizable(height=False,width=False)

        top_window.config(background='#075198')

        email_sub_lab=Label(top_window,text="Subject:",background="#075198",fg='white',font="Helvetica 16")
        email_sub_lab.pack()
        email_sub_entry=Text(top_window, height = 4, width = 52,font="Helvetica 12")
        email_sub_entry.pack()

        email_content_lab=Label(top_window,text="Content:",background="#075198",fg='white',font="Helvetica 16")
        email_content_lab.pack()
        email_content_entry=Text(top_window, height = 4, width = 52,font="Helvetica 12")
        email_content_entry.pack()

        sub_content_button=Button(top_window,text="Update",command=lambda:set_sub_content(top_window,email_sub_entry.get("1.0",END),email_content_entry.get("1.0",END)),background="#075198",fg='white',font="Helvetica 12",)
        sub_content_button.pack(pady=5)




    def server_login(em,pas):
        global email_from,server
        email_from=em
        server=smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        try:
            server.login(em, pas)
            get_sub_con(top_window)
            
        except Exception as e:
            display_login_response.config(text="Login Failed")
            display_login_response.pack()


    top_window=Toplevel()
    top_window.geometry("604x250")
    top_window.title('Email-Configure')
    top_window.resizable(height=False,width=False)

    top_window.config(background='#075198')




    top_email_label=Label(top_window,text="Email:",background="#075198",fg='white',font="Helvetica 16")
    top_email_label.pack(pady=5)
    top_email_entry=Entry(top_window,width=50,font="Helvetica 12")
    top_email_entry.pack(pady=5)

    top_pass_label=Label(top_window,text="Password:",background="#075198",fg='white',font="Helvetica 16")
    top_pass_label.pack(pady=5)
    top_pass_entry=Entry(top_window,width=50,font="Helvetica 12")
    top_pass_entry.pack(pady=5)

    top_login_button=Button(top_window,text="Login",command=lambda:server_login(top_email_entry.get(),top_pass_entry.get()),background="#075198",fg='white',font="Helvetica 16")
    top_login_button.pack(pady=5)

    display_login_response=Label(top_window)

    def finally_send(win):
        
        check_ackn=messagebox.askokcancel(title="Are You Sure?",message="Are You Sure To send Emails? Please Double Ckeck!",parent=win)
        if check_ackn==True:
            win.destroy()
            del_up_lab.config(state=DISABLED)
            send_button.config(state=DISABLED)
            F_preview.config(state=DISABLED)
            upload_certi.config(state=DISABLED)
            c_preview.config(state=DISABLED)
            set_xy.config(state=DISABLED)
            
            for data in peopl_list:
                for key,val in data.items():
                    name=val['name']
                    course=val['course']
                    email=val['email']
                    image_buffer=final_name_set(f_loc,x,y,x1,y1,name,course)
                    track_label.config(text=f"{int(key)+1} of {len(peopl_list)} remaining")
                    track_label.place(x=260,y=240)

#tomarharsh8@gmail.com
#13660$$##@@
                    msg = MIMEMultipart()
                    msg['From'] = email_from
                    msg['To'] = email
                    msg['Subject'] = sub

                    body = cont
                    msg.attach(MIMEText(body,'plain'))

    
                    part = MIMEBase('application','octet-stream')
                    part.set_payload(image_buffer)
                    encoders.encode_base64(part)
                    part.add_header('Content-Disposition',"attachment; filename= "+"Certificate.jpg")

                    msg.attach(part)
                    text = msg.as_string()
                    server.sendmail(email_from,email,text)
            
            server.quit()    
            track_label.config(text="Comleted")
            track_label.place(x=260,y=240)
            del_up_lab.config(state=ACTIVE)
            F_preview.config(state=ACTIVE)
            upload_certi.config(state=ACTIVE)
            c_preview.config(state=ACTIVE)
            set_xy.config(state=ACTIVE)


#-----------------------------------------------Labels--------------------------------------------------------#

top_Lab=Label(root, text="Upload Excel file",
              font="Helvetica 15 underline", background='#0a70d4', fg='white')
top_Lab.pack(pady=20)

file_button=Button(root, text="Upload", command=file_but,
                   background='#0a70d4', fg='white')
file_button.pack()

upload_certi=Button(root, text="Upload Certificate",
                    command=up_cert, background='#0a70d4', fg='white')
upload_certi.place(x=50, y=50)

c_preview_frame=Frame(root, background='#053460')
c_preview=Button(c_preview_frame, image=final_prew, command=lambda: prew(root.file_certi.name,x,y,x1,y1), background='#053460', fg='white', borderwidth=0, activebackground="#031e39")
c_preview.grid(row=0, column=0)

Adjust_frame=LabelFrame(c_preview_frame, text='Adjust',
                        background='#053460', fg='white', borderwidth=0)
Adjust_frame.grid(row=0, column=1)
x_value=Label(Adjust_frame, text='X:', background='#053460', fg='white')
x_value.grid(row=0, column=0)
x_Entry=Entry(Adjust_frame, width=20)
x_Entry.grid(row=0, column=1)

y_value=Label(Adjust_frame, text='Y:', background='#053460', fg='white')
y_value.grid(row=1, column=0)
y_Entry=Entry(Adjust_frame, width=20)
y_Entry.grid(row=1, column=1)

x1_value=Label(Adjust_frame, text='X1:', background='#053460', fg='white')
x1_value.grid(row=2, column=0)
x1_Entry=Entry(Adjust_frame, width=20)
x1_Entry.grid(row=2, column=1)

y1_value=Label(Adjust_frame, text='Y1:', background='#053460', fg='white')
y1_value.grid(row=3, column=0)
y1_Entry=Entry(Adjust_frame, width=20)
y1_Entry.grid(row=3, column=1)

set_xy=Button(Adjust_frame, text="Set", command=lambda:set_xy_func(x_Entry.get(),y_Entry.get(),x1_Entry.get(),y1_Entry.get()))
set_xy.grid(row=2, column=2, padx=10)

F_preview=Button(root, image=final_file_prew_img, command=lambda: fil_prew(
    root.file_csv), background='#031e39', fg='white', borderwidth=0, activebackground="#031e39")

send_button=Button(root,image=final_send_img,command=lambda:threading.Thread(target=send_func).start(),background="#0860b7")

track_label=Label(root,text=None)

root.mainloop()
