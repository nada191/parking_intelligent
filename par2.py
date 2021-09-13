#from numpy import place
#from numpy.distutils.fcompiler import none
from datetime import datetime,timedelta
import random
import threading
#from pip._internal.utils.outdated import SELFCHECK_DATE_FMT




class Parking :
    
    def __init__(self,n,l,choix=True,no=0,nr=0):
        self.no=no
        self.nr=nr
        self.nbLignes=n
        self.nbColonnes=l
        self.occupees={}  #un dictionnaire qui contient toutes les places occupees dans le parking
        self.reservees={} #un dictionnaire qui contient toutes les places reservees dans le parking
        self.libres=[]    #une liste qui contient toutes la places libre(non occupees et non reservees) dans le parking 
        for i in range(1,n*l+1):
            self.libres.append(i)
        if choix is False:
            # global no , nr
            #no=nr=0
            #no=input("Donnez le nombre des places que vous souhaitez etre occupees\n")
            #nr=input("Donnez le nombre des places que vous souhaitez etre reservees\n")
            
            
            
            i = 0
            while i < int(no):
                maint = datetime.now()        # la date actuelle du systeme
                m=random.randint(1,60*24)   # nombre aléatoire des minutes à ajouter
                s=random.randint(1,60*60*24)   # nombre aléatoire des secconde à ajouter
                date=maint-timedelta(minutes=m,seconds=s)    # la date d'entrée aléatoirement génerée
                date.isoformat(timespec='seconds')
                v = Voiture(str(random.randint(1,280000)),date)
                place = random.randint(1,n*l)  # génération d'une place aléatoire
                rep = self.occuper(v,place)
                if rep[0] is True:
                    i+=1
                else:
                    continue     
            j = 0
            while j < int(nr):
                maint = datetime.now()
                m=random.randint(1,60*24)   # nombre aléatoire des minutes à ajouter
                s=random.randint(1,60*60*24)   # nombre aléatoire des secconde à ajouter                
                date=maint+timedelta(minutes=m,seconds=s)
                date.isoformat(timespec='seconds')
                v = Voiture(str(random.randint(100000,280000)),date)
                place = random.randint(1,n*l)
                rep = self.reserver(place,v,date)
                if rep is True:
                    j+=1
                else:
                    continue 
           
           
           
           
        
    def reserver(self,place,voiture,date):  #méthode permettant de réserver une place (N.B: la voiture doit entrer dans le parking au plus 48h après la date de la réservation)  
        if place in self.libres  :
            voiture.date_res=date
            self.reservees[place]=voiture
            self.libres.remove(place)
            text ="la place {} est maintenant réservée pour votre voiture {}"
            print(text.format(place,voiture.matricule))
            return (True)
        elif place in self.occupees or place in self.reservees :
            text="la place {} est déjà occupée/réservée"
            print(text.format(place))
            return(False)
        else:
            print("la place saisie n'existe pas")
            return(False)
    
     
    def occuper(self,voiture,place): #méthode permettant de faire garer une voiture
        if self.MatriculeExiste(voiture.matricule)!=None:
            print("Veuillez verifier la matricule , cette voiture existe deja !")
            return(False,None)    
                
        if place in self.reservees and self.reservees[place].matricule==voiture.matricule:
            if (self.reservees[place].date_res > datetime.now()):
                print("Vous ne pouvez pas utiliser cette place maintenant ,veuillez choisir une autre !!")
                return(False,False)
            else:
                voiture.date_entree=datetime.now()
                self.occupees[place]=voiture
                self.reservees.pop(place)
                print("la place ",place,"est maintenant occupee par la voiture",voiture.matricule)
                return(True,True)
        elif place in self.libres :
            voiture.date_entree=datetime.now()
            self.occupees[place]=voiture
            self.libres.remove(place)
            text ="la place {} est maintenant occupee par votre voiture {}"
            print(text.format(place,voiture.matricule))
            return(True,None)
        elif place in self.occupees or place in self.reservees :
            text="la place {} est deja occupee/reservee"
            print(text.format(place))
            return(False,None)
        else:
            print("la place saisie n'existe pas") 
            return(False,None)
        
        
        
    
    def get_place_occupee(self,voiture):  #retourne le numéro de la place occupée par la voiture donnée
        
        for x,y in self.occupees.items():
            if y == voiture :
                return x  
            
            
            
            
    def vider(self,voiture):   #méthode permettant de faire sortir un voiture
        if voiture in self.occupees.values() :
            place=self.get_place_occupee(voiture)
            voiture.date_sortie=datetime.now()
            self.libres.append(place)
            #self.occupees.pop(place) 
            del self.occupees[place]
            text="la place {} est maintenant libre"
            print(text.format(place))
            return(self.calcul_tarif(voiture))
        else :
            text="la voiture {} n'occupe aucune place "
            print(text.format(voiture.matricule))
            return(False)
    
    
    def calcul_tarif(self,voiture):  #méthode por calculer le montant à payer avant de quitter le parking   
        d=voiture.date_sortie-voiture.date_entree
        nbHeures=d.total_seconds()/3600  #nbr des heures passées dans le parking
        if voiture in self.reservees.values():
            tarif=abs((nbHeures //2)-1)*0.500+nbHeures*1+3 # on a choisi de payer 1dt par heure et 2dt pour la réservation avec un ajout de 500 millimes pour chaque 2h passées )
        else :
            tarif=abs((nbHeures //2)-1)*0.500+nbHeures*1
        return round(tarif, 3)
 
    
        
    def annuler_reservation(self,voiture):  #méthode permettant d'annuler une réservation
        if voiture in self.reservees.values() :
            place=self.get_place_reservee(voiture)
            self.libres.append(place)
            self.reservees.pop(place)
            text="votre reservation de la place {} est annulee "
            print(text.format(place))
        else :
            text="Aucune reservation n'existe pour la voiture {}"
            print(text.format(voiture.matricule))
            
    def annulation_auto(self):    #permet l'annulation automatique (on a choisi que lorsqu'une voiture dépasse 2h de l'heure réservée ,la réservation sera automatiquement annulée)
        for i,j in self.reservees.items():
            if (j.date_res+timedelta(hours=2)):
                self.reservees.pop(i) 
                text="la reservation pour la voiture {} a ete automatiquement annulee (2h de retard)\n"
                print(text.format(j))
                
                
    def get_place_reservee (self,voiture): #retourne le numéro de la place réserée par la voiture donnée
        for x,y in self.reservees.items():
            if y == voiture :
                return x 
        
    def get_matricule(self,num): # si la place donnée est occupée ou réserver cette méthode retourne la matricule de la voiture , sinon elle retourne "Libre"
        ret="Libre"
        for x,y in self.occupees.items():
            if x==num:
                ret=y.matricule 
                break 
        
        for x,y in self.reservees.items():
            if x==num:
                ret=y.matricule 
                break 
        return ret
    
    
    def get_voiture_res(self,matricule): # retoune la voiture correspondante à la matricule donnée si cette voiture a reservée une place 
        voiture=None
        for i in self.reservees.values():
            if i.matricule==matricule:
                voiture=i
        return voiture 
    def MatriculeExiste(self,matricule):   #Cette méthode indique si une voiture existe déjà dans le parking 
        voiture=None
        for i in self.occupees.values() :
            if i.matricule == matricule :
                voiture=i
        return voiture
    
    def afficher(self): 
        print("Les places vides : " + format(len(self.libres)))
        print(self.libres)
        print("Les places occupees : " + format(len(self.occupees)))
        LO=[]
        for x in self.occupees :
            LO.append(x)
        print(LO)
        print("Les places reservees :" + format(len(self.reservees)))
        LR=[]
        for x in self.reservees :
            LR.append(x)
        print(LR)
        
        
        
        
    def calcul_distance(self,place): #methode permet de calculer la distance que doit parcourir une voiture pour arriver a une place donnee
        l=10 #largeur de la place
        L=20 #longeur de la place
        # l et L sont deux parametres que nous avons choisis pour representer la taille d'une place  
        if place%self.nbLignes!=0:  
            rg= (place // self.nbLignes)+1      # rg represente le rang de la colonne 
        else :
            rg= place // self.nbLignes
        r=rg%2  # on a besoin de ce reste pour savoir si on a passe par un chemin partage ou non 
        if rg==1 :
            d= (place-1)*l
        else :
            d=self.nbLignes*l+((rg//2)-1+rg-r)*L+(rg*self.nbLignes-place)*l
        
                 
        return d #distance parcourue jusqu'a la place 
    
    
    
    def place_plus_proche(self):  # cette methode permet de retouner comme resultat la plus proche place
        L=[] #contenant des tuples representant la place et la distance parcourue pour y arriver 
        proche=[] #contenant la/les plus proches places
        for x in self.libres :
            L.append( (x,self.calcul_distance(x)))
            
        def myFunc(e):
            return e[1]
        L.sort(key=myFunc) #trier les places selon la distance 
        #print(L)
        proche.append(L[0])
        for i in L:
            if i[1]==L[0][1] and i!=L[0] : #i[1] et non pas i 
                proche.append(i)
        print(proche)
        return proche 
        
   
    def printit(self):  # cette methode sera executer chaque seconde pour assurer l'annulation automatique
        threading.Timer(1.0,self.printit).start()
        self.annulation_auto()
    
    def OccPossible(self,matricule):   #cette methode indique si une voiture peut beneficier de sa reservation ou non 
        for i in self.reservees.values():
            if i.matricule == matricule and i.date_res <= datetime.now() :
                print("Bienvenue , Vous pouvez utiliser la place que vous avez reservee ")
                return True
        return False
    
class Voiture:
    def __init__(self,matricule,entree=None,sortie=None):  
        self.matricule=matricule 
        self.date_entree=entree
        self.date_sortie=sortie
        self.date_res=None
        