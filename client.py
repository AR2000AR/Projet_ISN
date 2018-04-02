from socketTools import *
from tkinter import *
from tkinter.messagebox import *
from socket import *
from tools import *
from logger import *
import threading,sys

#INIT=================================================================

#theme

option_theme=0


#mode nuit

if option_theme==0:
    theme="#60636d"
    ecriture="white"
    file_logo="logo-tchat-nuit.ppm"
    file_roue="roue.jpg"

    
#mode jour
    
if option_theme==1:
    theme="white"
    ecriture="black"
    file_logo='logo-tchat-jour.jpg'
    file_roue="roue.jpg"



#compte enregistré ?

create= False


#variable d'erreur de connection

wrong=0


#active le log

log=Log("log.txt",mode=LOG_REPLACE)


#temps d'attente max de connection au serveur (10sec)

setdefaulttimeout(10)


#---------------------------------- definition de la fenetre tkinter


#taille de la fenêtre, quand la taille est modifié, la mémorise avec event (plus bas)

taille='900x700'   

#def de la fenetre

def fenetre():
    global app
    app= Tk()
    app.title("CupChat",)
    app['bg']=theme


#enregistre la taille et la position de la fenetre modifiée par l'utilisateur
    
def taille_fenetre(event) :
    taille=app.geometry() #recupere la taille de la fenetre


#======================================================================

#---------------------------------- va chercher si un compte enregistré existe

def compte_enregistré() :
    create= False



#---------------------------------- 1ere page de "connxion en cours"

def connexion():
    
    if test==False:
        try:
            global client
            client = clientConnect()
            accueil()
            
        except:
            
            fenetre()
            app.minsize(width=300, height=325)
            
            titre_erreur= Label(app, text="Probléme de connexion avec le serveur", bg=theme,fg='Red',  font=("MV-Boli","bold"), justify=LEFT,width= 30 )
            titre_erreur.pack()

            app.mainloop()
    if test==True:
        accueil()

        
#---------------------------------- definition de la fenetre d'accueil

def accueil():

    fenetre()
    app.minsize(width=600, height=500)

#titre principal page d'accueil et logo
    
    logo= PhotoImage(file=file_logo)

    titre= Label(app, text="CupChat", bg=theme,fg=ecriture,  font=('Helvetica','80','bold')) #, image=logo, compound =RIGHT
    titre.pack()
    titre.place(anchor=N ,relx=0.5, rely=0.1)


#frame contenant la partie de l'identification
    
    fa= Frame(app, bg=theme)
    fa.pack()
    fa.place(anchor=N ,relx=0.5, rely=0.4)

#en cas d'ereur de connexion affiche un message rouge
    
    if wrong==2:
        titre_erreur= Label(fa, text="Désolé ce compte exite déja", bg=theme,fg='Red' ,  font="MV-Boli,bold", justify=LEFT,width= 30 )
        titre_erreur.pack()

    if wrong==1:
        titre_erreur= Label(fa, text="vous vous êtes trompé de mot de passe, ou de pseudo", bg=theme,fg='Red',  font=("MV-Boli","bold"), justify=LEFT,width= 30 )
        titre_erreur.pack()

#partie "identification"
        
    titre_login= Label(fa, text="Identifiant :", bg=theme,fg=ecriture,  font=("MV-Boli"), justify=LEFT,width= 30 )
    titre_login.pack()

    fa3= Frame(fa, bg="#4b4e56", pady=2, padx=2)
    fa3.pack()

    value = StringVar().set("")
    login = Entry(fa3, textvariable=value, width=30, font=("MV-Boli"), relief=FLAT)
    login.pack()

    espace= Frame(fa, bg=theme, height=40)
    espace.pack()


#le "mot de passe" en dessous
    
    titre_password= Label(fa, text="Mot de passe :", bg=theme,fg=ecriture,font=('MV-Boli'), justify=LEFT, width= 30 )
    titre_password.pack()

    fa2= Frame(fa, bg="#4b4e56", pady=2, padx=2)
    fa2.pack()

    value = StringVar().set("")
    password = Entry(fa2, textvariable=value,show="*", width=30, font=('MV-Boli'), relief=FLAT)
    password.pack()


#creation de compte
    
    def id_create():
        disable()
        print (password.get()+"\n"+login.get() )

        if test==False:
            client.send(bytes('<|ACCOUNT|>;<|CREATE|>;'+login.get()+";"+password.get(),"UTF-8"))
            
        app.destroy()
        new=True
        
        identification(new)


#autentification
        
    def id_auth():
        disable()
        print(password.get()+"\n"+login.get()) #####temporaire
        
        if test==False:
            client.send(bytes('<|ACCOUNT|>;<|AUTH|>;'+login.get()+";"+password.get(),"UTF-8"))
        app.destroy()
        new=False
    
        identification(new)


#desactive les boutons au moment de la connection
        
    def disable():
        bouton_valider.configure(state=DISABLED)
        bouton_créer.configure(state=DISABLED)
        bouton_quit.configure(state=DISABLED)


#frame des boutons de connection et de création de compte
        
    fbouton= Frame(fa, bg=theme, pady=30)
    fbouton.pack()

    
    fbouton_espace= Frame(fbouton, bg=theme, pady=20)
    fbouton_espace.pack()


#frames pour espacer entre les boutons espace entre les boutons

    frame_espace1=Frame(fbouton, pady=5, bg=theme)
    frame_espace1.pack()

    frame_espace2=Frame(fbouton, pady=5, bg=theme)
    frame_espace2.pack()

    
#si la souris passe sur le bouton (effet visuel)
    
    def enter(event):
        bouton_valider.configure(bg="#57609b")
        
    def enter1(event):
        bouton_créer.configure(bg="#57609b")


#quand la souris ressors du bouton (effet visuel)
        
    def leave(event):
        bouton_valider.configure(bg="#525a8e")

    def leave1(event):
        bouton_créer.configure(bg="#525a8e")

    
#bouton pour se connecter
    
    bouton_valider = Button(frame_espace1, text="Connection", command=id_auth, relief=FLAT, width=20,bg="#525a8e", fg=ecriture, font="40",pady=8, activebackground="#57609b", bd=0)
    bouton_valider.pack()

    bouton_valider.bind('<Enter>',enter )
    bouton_valider.bind('<Leave>',leave )

    
#bouton pour créer un compte
    
    bouton_créer = Button(frame_espace2, text="Inscription", command=id_create, relief=FLAT, width=20,bg="#525a8e", fg=ecriture, font="40",pady=8, activebackground="#57609b", bd=0)
    bouton_créer.pack()

    bouton_créer.bind('<Enter>',enter1 )
    bouton_créer.bind('<Leave>',leave1 )


#bouton pour quitter
    
    bouton_quit = Button(app, text="Quitter", command=app.destroy, relief=FLAT,bg=theme, activebackground=theme, bd=0, font="40")
    bouton_quit.pack()
    bouton_quit.place(anchor=SE,relx=1.0, rely=1.0)


    app.mainloop()

#---------------------------------- definition de l'identification avec du serveur
    
def identification(new):
    
    if test==True:
            app.destroy()
            appli()
            
    if test==False:
        
#recevoir la confirmation du serveur
        
        connect_accepte=reciveMsg(client,2048,theType=str)
        connect_accepte=connect_accepte.split(";")
        if new==True:
            if connect_accepte[1]=="DONE":
                
                log.write("",' compte créer avec succée')
                showinfo('votre compte à été créer !')
                appli()
            
            elif connect_accepte[1]=="EXIST":
                log.write("",'compte deja existant')
                print('Désolé ce compte exite déja')
                wrong=1

                accueil()

        else:
            if connect_accepte[1]=="<|ACCEPTED|>":
                log.write("",'conection reussi !')
                appli()
                
            elif connect_accepte[1]=="<|REJECTED|>":
                log.write("","Erreur de mot de passe, ou de pseudo")
                wrong=2
                accueil()

            else :
                log.write("","probléme avec le serveur")



#---------------------------------- application pricipale

def appli():

    fenetre()
    app.minsize(width=600, height=500)




#panneau latéral
    
    paneau_lateral= Frame(app, bg="#3e4047",width=100)
    paneau_lateral.pack(fill='y',side=LEFT)


#espace pour le nom du serveur

    paneau_serv= Frame(paneau_lateral, bg="#3e4047",width=100)
    paneau_serv.pack(fill='y',side=LEFT)

    
# bouton des option

    #roue= PhotoImage(file=file_roue)

    cadre_roue= Frame(paneau_lateral, bg="#3e4047")
    cadre_roue.pack(side=BOTTOM,fill='x' )

    cadre_roue1= Label(cadre_roue, bg="#3e4047",text="option",fg='#edf0f9',font=("MV-Boli","11","bold"),pady=6,padx=7)#,image=roue
    cadre_roue1.pack(side=RIGHT)


    



#cadre des messages
    
    cadre_principal= Frame(app, bg="pink",width=600-100)
    cadre_principal.pack(expand=1, fill='both',side=LEFT)


#cadre de l'envoie des message

    cadre_message= Frame(cadre_principal, bg=theme,pady=12,padx=12)
    cadre_message.pack(side=BOTTOM,fill='x' )
    
    cadre_message1= Frame(cadre_principal, bg=theme,pady=12,padx=12)
    cadre_message1.pack(side=BOTTOM,fill='x' )
    
    bouton_envoyer= Label(cadre_message1, bg="#747987",text="Envoyer",fg='#edf0f9',font=("MV-Boli","11","bold"),pady=6,padx=7)#,image=fléche
    bouton_envoyer.pack(side=RIGHT)

    value = StringVar().set("")
    send = Entry(cadre_message1, textvariable=value, relief=FLAT,font=("MV-Boli","15"), bg='#747987', width=30)
    send.pack(side=RIGHT,fill='both')

    
#cadre de l'historique
    
    cadre_history= Frame(cadre_principal, bg=theme)
    cadre_history.pack(side=BOTTOM,fill='both',expand=1)

    








# quand la taille est modifié, la mémorise avec event

    app.bind('<Configure>',taille_fenetre)



#envoie d'une demande d'historique au serveur
    
    if test==False:
        client.send(bytes('<|HISTORIQUE|>',"UTF-8"))
        
        newthread = thread_message()
        newthread.start()


    app.mainloop()




#---------------------------------- historique des option de l'utilisateur

def history():
    pass


#---------------------------------- gif affiché en parallele du thread principal

class thread_message(threading.Thread):  
    def run(self):
        while True:
            connect_accepte=reciveMsg(client,2048,theType=str)
            connect_accepte=connect_accepte.split(";")
            Label(cadre_history,text=connect_accepte).pack().place()
         

#================================================= lancement de la page d'attente, et connexion avec le serveur

#désactive la connection au serveur pour le besoin des tests

test=True

#connexion()

#172.18.144.187
#90.49.31.40
#51648
appli()

#=========================================A FAIRE :

# memorisation dans un fichier: la connexion automatique, le théme, la taille, le brouillon du message

# les messages

# envoyer des fichier

# reciveMsg()

# sendFile()

# reciveFile()

# recuperer historique des message

# fichier de langue ?

# The Message widget

# deconnexion

# fermer la connection

#lors de la connection fenetre en premier plan


#-------------------------------INUTILE POUR L'INSTANT



                
#------------------------------------ definition du gif des pages d'attentes
                
def gif(bon_gif):
    
     class gif1(Label):
         
         def __init__(self, master, filename, speed):
             
             self.speed = speed
             #speed: le delay en milliseconde entre chaques images cette fonction est là pour definir speed
             
             self.frames = [] # liste permettant de stocker les images du gif
             i = 0
             
             while True:
                 try:
                     p = PhotoImage(file=filename, format="gif - {}".format(i))
                     #prend les images que comprend le gif
                     
                 except TclError:
                     break #la boucle s'arrête
                    
                 self.frames.append(p) #on stock dans la liste les images du gif
                 i += 1

      
             super().__init__(master, image=self.frames[0])
             self.frame = 0

             def suite():
                 self.num_image = i #nombre d'image
             
####partie juste avant à charger
             
                 self.after(self.speed, self._animate) #fait attendre (vitesse) et appelle la fonction animate



      
                 def _animate(self):
             
                     # permet de faire une boucle allant de 1 à nombre max d'image
                     self.frame = (self.frame + 1) % self.num_image
             
                     self['image'] = self.frames[self.frame] #intégre l'image dans les options
                     self.after(self.speed, self._animate) #fait attendre (vitesse) et appelle la fonction animate crée ainsi un boucle

             fenetre()
             app.minsize(width=300, height=325)
             gif = gif1(app, filename=bon_gif, speed=40)
             gif.grid()
      
             app.mainloop()

     
             # on passe du premier gif au 2e pour la prochaine page d'attente
     
             bon_gif=file_gif[1] 

