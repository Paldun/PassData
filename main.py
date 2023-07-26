###########################################################################################
import os
import mysql.connector
from mysql.connector import Error
from configparser import ConfigParser
from tkinter import messagebox, colorchooser

import requests
version = requests.get("https://raw.githubusercontent.com/Paldun/app-version/main/version.txt").text

Updater_cantfnd = 'The system cannot find the file Updater.exe.'

old_version_open = open("src/version.txt", "r")
old_version = old_version_open.read()

if version != old_version:
   old_version_open.close()
   try:
      updater1 = os.system('start Updater.exe')
      if updater1 == 1:
         os._exit(0)
   except:
      os._exit(0)
else:
   print("Nincsen elérhető frissétés!")

hiba = 0
parser = ConfigParser()
parser.read("config.ini")
saved_host = parser.get('login_data', 'host')
saved_database = parser.get('login_data', 'database')
saved_username = parser.get('login_data', 'username')
saved_password = parser.get('login_data', 'password')

#----------Settings import
bkg_color = parser.get('main_config', 'bkg_color')
font_color = parser.get('main_config', 'font_color')
buttn_color = parser.get('main_config', 'btn_color')
#----------Settings import to reg_win
reg_bkg_color = parser.get('reg_config', 'reg_bkg_color')
reg_font_color = parser.get('reg_config', 'reg_font_color')
reg_buttn_color = parser.get('reg_config', 'reg_btn_color')



def save_butto():
   get_host = fldhost.get()
   get_database = flddatabase.get()
   get_username = fldusername.get()
   get_passwd = fldpassword.get()

   parser = ConfigParser()
   parser.read("config.ini")
   parser.set('login_data', 'host', get_host)
   parser.set('login_data', 'database', get_database)
   parser.set('login_data', 'username', get_username)
   parser.set('login_data', 'password', get_passwd)

   with open('config.ini', 'w') as configfile:
      parser.write(configfile)
   
   ask = messagebox.showwarning(title="SIKERES - Mentés", message="Sikerült menteni az adatokat!")
   if ask == 'ok':
      os._exit(0)
   elif data.quit:
      os._exit(0)

def error_str():
   if hiba == 0:
      messagebox.showinfo(title="ÉRTESÍTÉS", message="Nem található hiba!")
   elif hiba == 1:
      messagebox.showerror(title="HIBA", message=f"Lépj kapcsoaltba a fejlesztővel!\n\nHibakód: {e}")


def data_setting():
   global fldhost, flddatabase, fldusername, fldpassword, data
   import tkinter as tk
   

   data = tk.Tk()
   data.overrideredirect(True)
   data.attributes('-topmost', True)
   data['bg']=reg_bkg_color


   data.geometry('335x180')
   data.resizable(width=False, height=False)
   data.title("PassData - MYSQL Login")
   data.iconbitmap('src/icon.ico')

   data.geometry('335x180')
   data.resizable(width=False, height=False)
   data.title("PassData - MYSQL Login")

   lblhost = tk.Label(data, text="Add meg a hosztot", fg=reg_font_color, bg=reg_bkg_color)
   lbldatabase = tk.Label(data, text="Add meg az adatázist", fg=reg_font_color, bg=reg_bkg_color)
   lblusername = tk.Label(data, text="Add meg a felhasználónevet", fg=reg_font_color, bg=reg_bkg_color)
   lblpassword = tk.Label(data, text="Add meg a jelszót", fg=reg_font_color, bg=reg_bkg_color)

   fldhost = tk.Entry(data)
   fldhost.insert(0, saved_host)
   flddatabase = tk.Entry(data)
   flddatabase.insert(0, saved_database)
   fldusername = tk.Entry(data)
   fldusername.insert(0, saved_username)
   fldpassword = tk.Entry(data)

   lblhost.place(x=5,y=5)
   lbldatabase.place(x=200,y=5)
   lblusername.place(x=5,y=80)
   lblpassword.place(x=200,y=80)

   fldhost.place(x=5,y=25)
   flddatabase.place(x=200,y=25)
   fldusername.place(x=5,y=105)
   fldpassword.place(x=200,y=105)

   save_button = tk.Button(data, text="Mentés", command=lambda:save_butto(), bg=reg_buttn_color)
   save_button.place(x=145,y=150)

   err_btn = tk.Button(data, text="Hiba", command=lambda:error_str(), bg=reg_buttn_color)
   err_btn.place(x=290,y=150)

   data.mainloop()

sql = """
   CREATE TABLE IF NOT EXISTS `data` (
      `id` int(11) NOT NULL AUTO_INCREMENT,
      `azonosito` text COLLATE utf8_hungarian_ci NOT NULL,
      `username` text COLLATE utf8_hungarian_ci NOT NULL,
      `password` text COLLATE utf8_hungarian_ci NOT NULL,
      `leírás` mediumtext COLLATE utf8_hungarian_ci DEFAULT NULL,
      PRIMARY KEY (`id`)
   ) ENGINE=InnoDB AUTO_INCREMENT=0 DEFAULT CHARSET=utf8 COLLATE=utf8_hungarian_ci;  
   """

try:
    db = mysql.connector.connect(host=saved_host,
                                         database=saved_database,
                                         user=saved_username,
                                         password=saved_password)
    if db.is_connected():
      mycursor = db.cursor() 
      try:
         mycursor.execute(sql)
         db.commit()
         hiba = 0
      except mysql.connector.Error as err:
         print(err)
         print("Error Code:", err.errno)
         print("SQLSTATE", err.sqlstate)
         print("Message", err.msg)
         messagebox.showinfo(err, f"Üzenet: {err.msg}")
except Error as e:
   print("Error while connecting to MySQL", e)
   hiba = 1
   data_setting()

try:
 db_auth = mysql.connector.connect(host=saved_host,
                                      database='phpmyadmin',
                                      user='auth',
                                      password='MqiTF2WTXxuQVleD')
 if db_auth.is_connected():
   auth_cursor = db_auth.cursor()
   auth_cursor.execute(f"SELECT * FROM pma__users WHERE username = '{saved_username}' AND usergroup = 'Owner';")
   records = auth_cursor.fetchall()
   recor_len = len(records)

   if recor_len == 0:
      is_admin = "no"
   elif recor_len == 1:
      is_admin = "yes"

except Error as e:
   print("Error while connecting to MySQL", e)
###########################################################################################

from configparser import ConfigParser
from tkinter import ttk, messagebox
import tkinter as tk
import pyperclip
import base64
import random
import string
import requests
version = requests.get("https://raw.githubusercontent.com/Paldun/app-version/main/version.txt").text


root = tk.Tk()

#------------------- Config
root.geometry('770x300')
root.resizable(width=False, height=False)
root.title("PassData")
root['bg']=bkg_color
root.iconbitmap('src/app.ico')


#------------------- START-UP CONFIG
def clear_screen():
   for widgets in root.winfo_children():
      widgets.destroy()

   create = tk.Button(root, text="Létlehozás", width=13, command=lambda:add_data(), bg=buttn_color)
   search = tk.Button(root, text="Jelszavak", width=13, command=lambda:passwords(), bg=buttn_color)
   delete = tk.Button(root, text="Törlés", width=13, command=lambda:delete_data(), bg=buttn_color)
   dbinfo = tk.Button(root, text="Adatbázis infó",  width=13, command=lambda:get_db_info(), bg=buttn_color)
   debug__mode = tk.Button(root, text="Egyéb beáll.", width=13, command=lambda:auth(), bg=buttn_color)
   db_setting = tk.Button(root, text="Újdonságok",  width=13, command=lambda:patchnotes(), bg=buttn_color)


   produced = tk.Label(root, text="Created by Ádám", bg=bkg_color, fg=font_color)

   #------------------- BUILD
   create.place(x=5, y=8)
   search.place(x=5, y=38)
   delete.place(x=5, y=68)
   dbinfo.place(x=5, y=98)
   db_setting.place(x=5,y=128)
   debug__mode.place(x=5, y=270)
   
   produced.place(x=5,y=154)

   #------------------- Vízjel

   versionlbl = tk.Label(text=version, fg="#C2C2C2", bg=bkg_color)
   versionlbl.place(x=685,y=1)

#------------------- DEFINATIONS

#------------------------------------------------------ Konzol Start

def ssh_connect():
   get_host = ent_host.get()
   get_name = ent_name.get()

   os.system(f'cmd /k ssh {get_name}@{get_host}')
 
def konzol_on():
   global ent_host, ent_name
   clear_screen()

   host_lbl = tk.Label(root, text='Add meg a hosztot', bg=bkg_color, fg=font_color)
   name_lbl = tk.Label(root, text='Add meg a user-t', bg=bkg_color, fg=font_color)

   host_lbl.place(x=120,y=15)
   name_lbl.place(x=120,y=75)

   ent_host = tk.Entry(root, width=17)
   ent_name = tk.Entry(root, width=17)

   ent_host.place(x=120,y=40)
   ent_name.place(x=120,y=100)

   csatlakozas_btn = tk.Button(root, text="Csatlakozás",  width=13, command=lambda:ssh_connect(), bg=buttn_color)
   csatlakozas_btn.place(x=120,y=140)

#------------------------------------------------------ Konzol End

def patchnotes():
   clear_screen()
   patchnotes = requests.get("https://raw.githubusercontent.com/Paldun/app-version/main/patchnotes.txt").text
   info = tk.Label(root, text=patchnotes, fg=reg_font_color, bg=reg_bkg_color)
   info.place(x=130,y=10)

def table_reset():

   YesOrNo_auth = messagebox.askyesno('Végleges formázás','Biztos vagy benne hogy formázod az adatokat? (Nem visszavonható!)', icon = 'warning')

   if YesOrNo_auth == True:
      mycursor.execute("TRUNCATE TABLE data;")
      sikertelen = tk.Label(text="SIKERTELEN - Törléa", fg="red", bg=bkg_color)
      sikertelen.place(x=5,y=245)
      format_sucess = tk.Label(root, text="A formázás sikeres!", bg=bkg_color)
      format_sucess.place(x=5,y=245)
   else:
      visszautasitva = tk.Label(text="SIKERES - Visszau.", fg="#00D425", bg=bkg_color)
      visszautasitva.place(x=5,y=245)  


def getusers():

   userget_cu = db.cursor()
   userget_cu.execute("FLUSH PRIVILEGES;")

   userget_cu.execute("SHOW COLUMNS FROM `mysql`.`user`;")


   for item in users.get_children():
      users.delete(item)
   try:
      userget_cu.execute("SELECT `user`, `host`, IF(LENGTH(password)>0, password, authentication_string) AS `password` FROM `mysql`.`user`;")
   except mysql.connector.errors.InternalError:
      print("Nincsen hozzá jogod!")
   except ValueError:
      print("Nincsen hozzá jogod!")
   records = userget_cu.fetchall()
   for i, (user, host, password) in enumerate(records, start=0):
      users.insert("", "end", values=(user, host, password))

def listuser():
   global users
   cols = ('Felhasználó', 'Hoszt', 'Jelszó')
   users = ttk.Treeview(root, columns=cols, show='headings')
   users.column('Felhasználó', anchor=tk.CENTER, width=20)
   users.column('Hoszt', anchor=tk.CENTER, width=150)
   users.column('Jelszó', anchor=tk.CENTER, width=150)

   for col in cols:
       users.heading(col, text=col)    
       users.place(x=405,y=10, height=280)
   getusers()

def adduser():
   pass


def removeuser():
   pass


def db_setting_s():
   user_add = tk.Button(root, text="Felh. hozzáadása",  width=13, command=lambda:adduser(), bg=buttn_color)
   user_remove = tk.Button(root, text="Felh. törlése",  width=13, command=lambda:removeuser(), bg=buttn_color)

   user_add.place(x=120,y=15)
   user_remove.place(x=225,y=15)
   listuser()

def debug():
   konzol = tk.Button(root, text="Konzol",  width=13, command=lambda:konzol_on(), bg=buttn_color)
   konzol.place(x=5,y=188)
   


def formazas():
   reset_database = tk.Button(root, text="Össz. jelszó törlése",  width=13, command=lambda:table_reset(), bg=buttn_color)
   reset_database.place(x=5,y=218)

def auth():
   clear_screen()
   if is_admin == "no":
      formazas()
   elif is_admin == "yes":
      debug()
      formazas()

def get_info_upload():
   hibacount = 0
   azonositoget = azonositofi.get()
   felhasznaloget = felhasznalofi.get()
   jelszoget = jelszofi.get()
   leirasget = leirasfi.get()

   upper_azonositoget = azonositoget.upper()

   if len(azonositoget) < 3 and hibacount == 0:
      tk.messagebox.showerror(title="HIBA - Azonosító", message="3 karakternél kevesebb! Kérlek bővisd ki vagy adj hozzá több karaktert!")
      hibacount += 1
   elif len(felhasznaloget) < 3 and hibacount == 0:
      tk.messagebox.showerror(title="HIBA - Felhasználónév/email", message="3 karakternél kevesebb! Kérlek bővisd ki vagy adj hozzá több karaktert!")
      hibacount += 1
   elif len(jelszoget) < 3 and hibacount == 0:
      tk.messagebox.showerror(title="HIBA - Jelszó", message="3 karakternél kevesebb! Kérlek bővisd ki vagy adj hozzá több karaktert!")
      hibacount += 1

   message_bytes = jelszoget.encode('ascii')
   base64_bytes = base64.b64encode(message_bytes)
   base64_message = base64_bytes.decode('ascii')

   if hibacount == 0 and len(azonositoget) > 3 and len(felhasznaloget) > 3 and len(jelszoget) > 3:
      sql = "INSERT INTO data (azonosito, username, password, leírás) VALUES (%s, %s, %s, %s)"
      value = (upper_azonositoget, felhasznaloget, base64_message, leirasget)

      mycursor.execute(sql, value)
      db.commit()

      sikertelen = tk.Label(text="[-]  SIKERTELEN - Feltöltasdasdés", fg=bkg_color, bg=bkg_color)
      sikertelen.place(x=300,y=275)

      sikeres = tk.Label(text="[-]  SIKERES - Feltöltés", fg="#00D425", bg=bkg_color)
      sikeres.place(x=300,y=275)
   else:
      sikertelen = tk.Label(text="[-]  SIKERTELEN - Feltöltés", fg="red", bg=bkg_color)
      sikertelen.place(x=300,y=275)

def random_pass_generate():
   def_lenght = 20

   kis_betul = string.ascii_lowercase
   nagy_beetuk = string.ascii_uppercase
   szamok = string.digits
   szimolumok = string.punctuation

   all = kis_betul + nagy_beetuk + szamok + szimolumok

   password_generated = random.sample(all, def_lenght)

   temp = "".join(password_generated)

   entry_text = tk.StringVar()
   entry_text.set(temp)
   jelszofi.configure(textvariable=entry_text)

def add_data():
   clear_screen()

   global azonositofi, felhasznalofi, jelszofi, leirasfi

   soveg1 = tk.Label(text="Azonosító", font="Ariel 11", bg=bkg_color, fg=font_color)
   soveg2 = tk.Label(text="Felhasználónév/email", font="Ariíel 11", bg=bkg_color, fg=font_color)
   soveg3 = tk.Label(text="Jelszó", font="Ariel 11", bg=bkg_color, fg=font_color)
   soveg4 = tk.Label(text="Leírás", font="Ariel 11", bg=bkg_color, fg=font_color)

   azonositofi = tk.Entry(root)
   felhasznalofi = tk.Entry(root)
   jelszofi = tk.Entry(root)
   leirasfi = tk.Entry(root)


   soveg1.place(x=160,y=18)
   soveg2.place(x=160,y=98)
   soveg3.place(x=380,y=18)
   soveg4.place(x=380,y=98)

   azonositofi.place(x=160,y=45, width=150)
   felhasznalofi.place(x=160,y=125, width=150)
   jelszofi.place(x=380,y=45, width=150)
   leirasfi.place(x=380,y=125, width=150)

   info_upload = tk.Button(root, text="Feltöltés", width=13, command=lambda:get_info_upload(), bg=buttn_color)
   random_pass = tk.Button(root, text="Generálás", width=13, command=lambda:random_pass_generate(), bg=buttn_color)

   random_pass.place(x=540,y=42)
   info_upload.place(x=650,y=270)



def torles_id():
   id_search = kerdezed_bekerese.get()

   egy_sam_lsit = ['1', '2', '3', '4', '5', '6', '7', '8', '9']

   if len(id_search) > 1 or id_search in egy_sam_lsit:
      YesOrNo = messagebox.askyesno('Végleges törlés','Biztos vagy benne hogy kitörlöd?', icon = 'warning')

      if YesOrNo == True:
         mycursor.execute(f"DELETE FROM data WHERE id = {id_search}")
         db.commit()

         sikertelen = tk.Label(text="[-]  SIKERTELEN - Törléasdass", fg=bkg_color, bg=bkg_color)
         sikertelen.place(x=450,y=275)

         sikeres = tk.Label(text="[-]  SIKERES - Törlés", fg="#00D425", bg=bkg_color)
         sikeres.place(x=450,y=275)
         # show()
      else:
         visszautasitva = tk.Label(text="[-]  SIKERES - Visszautasítás", fg="#00D425", bg=bkg_color)
         visszautasitva.place(x=450,y=275)  
   elif len(id_search) < 1 or id_search == '0':
      sikertelen = tk.Label(text="[-]  SIKERTELEN - Törlés", fg="red", bg=bkg_color)
      sikertelen.place(x=450,y=275)

def delete_data():
   global listBox, kerdezed_bekerese
   clear_screen()

   cols = ('Id', 'Azonosító')
   listBox = ttk.Treeview(root, columns=cols, show='headings')
   listBox.column('Id', anchor=tk.CENTER, width=20)
   listBox.column('Azonosító', anchor=tk.CENTER, width=150)

   for col in cols:
       listBox.heading(col, text=col)    
       listBox.place(x=125,y=10, height=280)
   # show()

   kerdezes = tk.Label(text="Add meg az id-t a törléshez", bg=bkg_color, fg=font_color)
   kerdezed_bekerese = tk.Entry()

   kerdezes.place(x=320,y=20)
   kerdezed_bekerese.place(x=320,y=45, width=120)

   search_send = tk.Button(text="Törlés", command=lambda:torles_id(), bg=buttn_color)
   search_send.place(x=450,y=43)

style=ttk.Style()
style.theme_use('clam')
style.configure("Treeview", background=bkg_color, fieldbackground=bkg_color)

def masolas():
   encoded_pass = tk.Label(text="Vágólapra másolva!", bg=bkg_color, font="Ariel 9 bold")
   encoded_pass.place(x=500,y=180)
   pyperclip.copy(decimal_converted_string)


def kereses_id():
   lezaroscanvas = tk.Canvas(width=300, height=330, bg=bkg_color, highlightthickness=0)
   lezaroscanvas.place(x=495,y=100)
   global decimal_converted_string
   id_search = kerdezed_bekerese.get()


   egy_sam_lsit = ['1', '2', '3', '4', '5', '6', '7', '8', '9']

   if len(id_search) > 1 or id_search in egy_sam_lsit:
      mycursor.execute(f"SELECT * FROM data WHERE id = {id_search}")
      sresult = mycursor.fetchall()
      for x in sresult:
         locked_pass = x[3]

         base64_converted_string = locked_pass.encode("ascii")
         decode = base64.b64decode(base64_converted_string)
         decimal_converted_string = decode.decode("ascii")  

         takaro = tk.Label(root, text="Nemkapodmeghehehehhehe", fg=bkg_color, bg=bkg_color)
         takaro.place(x=500,y=160)

         encoded_pass = tk.Label(root, text=f"A jelszó: {decimal_converted_string}", bg=bkg_color, font="Ariel 9 bold")
         encoded_pass.place(x=500,y=160)

         copy_btn = tk.Button(root, text="Másolás", compound = tk.CENTER ,command=lambda:masolas(), bg=buttn_color)
         copy_btn.place(x=625,y=180)

      sikertelen = tk.Label(text="[-]  SIKERTELEN - Lekérdezés", fg=bkg_color, bg=bkg_color)
      sikertelen.place(x=540,y=275)
      sikeres = tk.Label(text="[-]  SIKERES - Lekérdezés", fg="#00D425", bg=bkg_color)
      sikeres.place(x=540,y=275)
   elif len(id_search) < 1 or id_search == '0':
      sikertelen = tk.Label(text="[-]  SIKERTELEN - Lekérdezés", fg="red", bg=bkg_color)
      sikertelen.place(x=540,y=275)
   else:
      sikertelen = tk.Label(text="[-]  SIKERTELEN - Lekérdezés", fg="red", bg=bkg_color)
      sikertelen.place(x=540,y=275)

def save():
   hibacount = 0
   nevget = nevent.get()
   nevgetupper = nevget.upper()
   emailget = emailent.get()
   leirasget = leirasent.get()
   passget = passent.get()
   id_edit_int = int(id_edit)


   message_bytes = passget.encode('ascii')
   base64_bytes = base64.b64encode(message_bytes)
   save_pass = base64_bytes.decode('ascii')

   strnevgetupper = str(nevgetupper)
   stremailget = str(emailget)
   strleirasget = str(leirasget)
   strsave_pass = str(save_pass)

   if len(strnevgetupper) < 3 and hibacount == 0:
      tk.messagebox.showerror(title="HIBA - Azonosító", message="3 karakternél kevesebb! Kérlek bővisd ki vagy adj hozzá több karaktert!")
      hibacount += 1
   elif len(stremailget) < 3 and hibacount == 0:
      tk.messagebox.showerror(title="HIBA - Felhasználónév/email", message="3 karakternél kevesebb! Kérlek bővisd ki vagy adj hozzá több karaktert!")
      hibacount += 1
   elif len(strsave_pass) < 3 and hibacount == 0:
      tk.messagebox.showerror(title="HIBA - Jelszó", message="3 karakternél kevesebb! Kérlek bővisd ki vagy adj hozzá több karaktert!")
      hibacount += 1

   try:
      if hibacount == 0 and len(strnevgetupper) > 3 and len(stremailget) > 3 and len(strsave_pass) > 3:

         mycursor.execute(f"UPDATE `PassData`.`data` SET `azonosito`='{strnevgetupper}' WHERE  `id`={id_edit_int};")
         mycursor.execute(f"UPDATE `PassData`.`data` SET `username`='{stremailget}' WHERE  `id`={id_edit_int};")
         mycursor.execute(f"UPDATE `PassData`.`data` SET `password`='{strsave_pass}' WHERE  `id`={id_edit_int};")
         mycursor.execute(f"UPDATE `PassData`.`data` SET `leírás`='{strleirasget}' WHERE  `id`={id_edit_int};")
         db.commit()
         sikeres = tk.Label(text="[-]  SIKERES - Szerkesztés", fg="#00D425", bg=bkg_color)
         sikeres.place(x=550,y=257)
   except:
      messagebox.showerror(title="HIBA", message="Sikertelen szerkesztés!")

def edit_id():
   lezaroscanvas = tk.Canvas(width=300, height=330, bg=bkg_color, highlightthickness=0)
   lezaroscanvas.place(x=495,y=100)
   global nevent, emailent, leirasent, id_edit, passent
   id_edit = kerdezed_bekerese.get()

   egy_sam_lsit = ['1', '2', '3', '4', '5', '6', '7', '8', '9']

   if len(id_edit) > 1 or id_edit in egy_sam_lsit:
      mycursor.execute(f"SELECT * FROM data WHERE id = {id_edit}")
      edit_result = mycursor.fetchall()
      for x in edit_result:
         azonosiro = x[1]
         nev1 = azonosiro[0]
         nev2 = azonosiro[1:len(azonosiro)]
         lowernev = nev1 + nev2.lower()
         email_get = x[2]
         leiras = x[4]

         nevtxt = tk.Label(text="Azonosító:", fg=font_color, bg=bkg_color)
         emailtxt = tk.Label(text="Email:", fg=font_color, bg=bkg_color)
         leirastxt = tk.Label(text="Leírás:", fg=font_color, bg=bkg_color)
         passtxt = tk.Label(text="Jelszó:", fg=font_color, bg=bkg_color)

         nevtxt.place(x=500,y=128)
         emailtxt.place(x=500,y=168)
         leirastxt.place(x=500,y=208)
         passtxt.place(x=575,y=128)

         nevent = tk.Entry(root, width=11)
         emailent = tk.Entry(root, width=25)
         leirasent = tk.Entry(root, width=25)
         passent = tk.Entry(root, width=28)

         nevent.insert(0, lowernev)
         emailent.insert(0, email_get)
         leirasent.insert(0, leiras)

         nevent.place(x=500,y=150)
         emailent.place(x=500,y=190)
         leirasent.place(x=500,y=230)
         passent.place(x=575,y=150)

         save_btn = tk.Button(text="Mentés", command=lambda:save(), bg=buttn_color)
         save_btn.place(x=500,y=255)

   elif len(id_edit) < 1 or id_edit == '0':
      sikertelen = tk.Label(text="[-]  SIKERTELEN - Lekérdezés", fg="red", bg=bkg_color)
      sikertelen.place(x=540,y=275)
   else:
      sikertelen = tk.Label(text="[-]  SIKERTELEN - Lekérdezés", fg="red", bg=bkg_color)
      sikertelen.place(x=540,y=275)



class passwords:
   global show
   def __init__(self, *args, **kwargs):
      global listBox, kerdezed_bekerese, show
      clear_screen()

      cols = ('Id', 'Azonosító', 'Felhasználónév')
      listBox = ttk.Treeview(root, columns=cols, show='headings')
      listBox.column('Id', anchor=tk.CENTER, width=20)
      listBox.column('Azonosító', anchor=tk.CENTER, width=150)
      listBox.column('Felhasználónév', anchor=tk.CENTER, width=180)

      for col in cols:
         listBox.heading(col, text=col)    
         listBox.place(x=125,y=10, height=280)
      show()

      listBox.bind("<Double-1>", self.search)

      kerdezes = tk.Label(text="Add meg az id-t", bg=bkg_color, fg=font_color)
      kerdezed_bekerese = tk.Entry()

      kerdezes.place(x=500,y=20)
      kerdezed_bekerese.place(x=500,y=45, width=120)

      search_send = tk.Button(text="Keresés", command=lambda:kereses_id(), bg=buttn_color)
      search_send.place(x=625,y=43)
      edit_send = tk.Button(text="Szerkesztés", command=lambda:edit_id(), bg=buttn_color)
      edit_send.place(x=678,y=43)

      def search(self, event):
         item = self.tree.selection()
         print(self.tree.item(item,"text"))

      
      def show():
         for item in listBox.get_children():
            listBox.delete(item)
         mycursor = db.cursor()
         mycursor.execute("SELECT id, azonosito,username FROM data")
         records = mycursor.fetchall()
         for i, (id, azonosito, username) in enumerate(records, start=1):
            listBox.insert("", "end", values=(id, azonosito, username))

pressed = 0
def show_passwd(passnullbool = False):
   global pressed
   if passnullbool != True:
      if pressed == 0:
         conn_info2.configure(text=f"Jelszó: {saved_password}", bg=bkg_color)
         pressed += 1
      elif pressed == 1:
         conn_info2.configure(text=f"Jelszó: {csillag}", bg=bkg_color)
         pressed = 0


def save_bkg_color():
   parser = ConfigParser()
   parser.read("config.ini")
   ask_bkg_color = colorchooser.askcolor()
   str_ask_bkg_color = str(ask_bkg_color)
   str_ask_bkg_color_len = len(str_ask_bkg_color)

   lastfirst = str_ask_bkg_color_len - 9

   lastlast = str_ask_bkg_color_len - 2

   lol_working = str_ask_bkg_color[lastfirst:lastlast]

   if lol_working == "ne, Non":
      return save_bkg_color()
   else:
      parser.set('main_config', 'bkg_color', lol_working)
      with open('config.ini', 'w') as configfile:
         parser.write(configfile)
   

def save_font_color():
   parser = ConfigParser()
   parser.read("config.ini")
   ask_font_color = colorchooser.askcolor()

   str_ask_font_color = str(ask_font_color)
   str_ask_font_color_len = len(str_ask_font_color)

   lastfirst = str_ask_font_color_len - 9

   lastlast = str_ask_font_color_len - 2

   lol_working = str_ask_font_color[lastfirst:lastlast]

   if lol_working == "ne, Non":
      return save_font_color()
   else:
      parser.set('main_config', 'font_color', lol_working)

      with open('config.ini', 'w') as configfile:
         parser.write(configfile)

def save_bttn_color():
   parser = ConfigParser()
   parser.read("config.ini")
   ask_bttn_color = colorchooser.askcolor()

   str_ask_bttn_color = str(ask_bttn_color)
   str_ask_bkg_color_len = len(str_ask_bttn_color)

   lastfirst = str_ask_bkg_color_len - 9

   lastlast = str_ask_bkg_color_len - 2

   lol_working = str_ask_bttn_color[lastfirst:lastlast]

   if lol_working == "ne, Non":
      return save_bttn_color()
   else:
      parser.set('main_config', 'btn_color', lol_working)

      with open('config.ini', 'w') as configfile:
         parser.write(configfile)




#------------------- Reg_win_config
def reg_save_bkg_color():
   parser = ConfigParser()
   parser.read("config.ini")
   reg_ask_bkg_color = colorchooser.askcolor()
   str_ask_bkg_color = str(reg_ask_bkg_color)
   str_ask_bkg_color_len = len(str_ask_bkg_color)

   lastfirst = str_ask_bkg_color_len - 9

   lastlast = str_ask_bkg_color_len - 2

   lol_working = str_ask_bkg_color[lastfirst:lastlast]

   if lol_working == "ne, Non":
      return reg_save_bkg_color()
   else:
      parser.set('reg_config', 'reg_bkg_color', lol_working)

      with open('config.ini', 'w') as configfile:
         parser.write(configfile)


def reg_save_font_color():
   parser = ConfigParser()
   parser.read("config.ini")
   reg_ask_font_color = colorchooser.askcolor()

   str_ask_font_color = str(reg_ask_font_color)
   str_ask_font_color_len = len(str_ask_font_color)

   lastfirst = str_ask_font_color_len - 9

   lastlast = str_ask_font_color_len - 2

   lol_working = str_ask_font_color[lastfirst:lastlast]

   if lol_working == "ne, Non":
      return reg_save_font_color()
   else:
      parser.set('reg_config', 'reg_font_color', lol_working)

      with open('config.ini', 'w') as configfile:
         parser.write(configfile)


def reg_save_bttn_color():
   parser = ConfigParser()
   parser.read("config.ini")
   reg_ask_bttn_color = colorchooser.askcolor()

   str_ask_bttn_color = str(reg_ask_bttn_color)
   str_ask_bkg_color_len = len(str_ask_bttn_color)

   lastfirst = str_ask_bkg_color_len - 9

   lastlast = str_ask_bkg_color_len - 2

   lol_working = str_ask_bttn_color[lastfirst:lastlast]

   if lol_working == "ne, Non":
      return reg_save_bttn_color()
   else:
      parser.set('reg_config', 'reg_btn_color', lol_working)

      with open('config.ini', 'w') as configfile:
         parser.write(configfile)


def settings():
   conf_w = tk.Tk()

   vertical_line = tk.Canvas(conf_w, width=2, height=200, bg="black")
   vertical_line.place(x=147,y=0)

   conf_w.geometry('300x150')
   conf_w.resizable(width=False, height=False)
   conf_w.title("PassData - Beállítások")

   main_w = tk.Label(conf_w, text="Elsődleges ablak")
   main_w.place(x=30,y=7)

   lbl_bkg_color = tk.Button(conf_w, text="Háttérszín kiválasztása", command=lambda:save_bkg_color(), width=17)
   lbl_font_color = tk.Button(conf_w, text="Betü szín", command=lambda:save_font_color(), width=17)
   lbl_buttn_color = tk.Button(conf_w, text="Gomb szín", command=lambda:save_bttn_color(), width=17)

   lbl_bkg_color.place(x=10,y=30)
   lbl_font_color.place(x=10,y=70)
   lbl_buttn_color.place(x=10,y=110)

   main_w_login = tk.Label(conf_w, text="Bejelentkező ablak")
   main_w_login.place(x=174,y=7)

   reg_lbl_bkg_color = tk.Button(conf_w, text="Háttérszín kiválasztása", command=lambda:reg_save_bkg_color(), width=17)
   reg_lbl_font_color = tk.Button(conf_w, text="Betü szín", command=lambda:reg_save_font_color(), width=17)
   reg_lbl_buttn_color = tk.Button(conf_w, text="Gomb szín", command=lambda:reg_save_bttn_color(), width=17)

   reg_lbl_bkg_color.place(x=160,y=30)
   reg_lbl_font_color.place(x=160,y=70)
   reg_lbl_buttn_color.place(x=160,y=110)

   conf_w.mainloop()

def get_db_info():
   global conn_info2, info, db_info, csillag
   clear_screen()
   cursor = db.cursor()
   cursor.execute("select database();")
   record = cursor.fetchone()

   db_Info = db.get_server_info()
   info = tk.Label(root, text="Az adatbázis verziója: " + db_Info, bg=bkg_color, fg=font_color)
   db_info = tk.Label(root, text=f"Jelenleg a {record}-ba vagy bejelentkezve!", bg=bkg_color, fg=font_color)

   csillag = ''
   if saved_password == '':
         csillag = 'Nincsen megadott jelszó!'
         passnull = True
   else:
      passnull = False
      for i in range(len(saved_password)):
         csillag += '*'
      
   bejelentkezesi_adatok = tk.Label(root, text="A jelenlegi adatok a bejelentkezésről", bg=bkg_color, fg=font_color)
   conn_info1 = tk.Label(root, text=f"Felhasználónév: {saved_username}", bg=bkg_color, fg=font_color)
   conn_info2 = tk.Label(root, text=f"Jelszó: {csillag}", bg=bkg_color, fg=font_color)
   conn_info3 = tk.Label(root, text=f"Hoszt: {saved_host}", bg=bkg_color, fg=font_color)

   show_button = tk.Button(text="Show", command=lambda:show_passwd(passnull), bg=buttn_color)
   show_button.place(x=265,y=270)


   change_password_btn = tk.Button(root, text="Bejelentkezési adatok megváltoztatása", bg=buttn_color, command=lambda:data_setting())
   change_password_btn.place(x=555,y=270)

   setting = tk.Button(root, text="Beállítások", width=13, command=lambda:settings(), bg=buttn_color)
   setting.place(x=665,y=25)

   bejelentkezesi_adatok.place(x=120,y=200)
   conn_info1.place(x=120,y=230)
   conn_info2.place(x=120,y=250)
   conn_info3.place(x=120,y=270)

   info.place(x=120,y=10)
   db_info.place(x=120,y=30)
   
   default_lbl.destroy()

clear_screen()
#------------------- DEFAULT SETTINGS
default_lbl = tk.Label(text="Kérlek válassz az alábbi opciók közül!", font="Arial 11 italic bold", bg=bkg_color, fg=font_color)
default_lbl.place(x=305,y=130)

root.mainloop()