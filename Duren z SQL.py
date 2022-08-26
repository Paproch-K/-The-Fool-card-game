from random import shuffle
from sys import exit
#from time import sleep
import sqlite3
from pandas import read_sql_query
# import mysql.connector
from numpy import ceil

# cnx = mysql.connector.connect(user='name', password='password',
#                               host='127.0.0.1',
#                               database='xxxxxxx')
# cnx.close()


con = sqlite3.connect("duren_baza.db", timeout=10)
con.row_factory = sqlite3.Row
cur = con.cursor()
cur.execute("""
    CREATE TABLE IF NOT EXISTS New_scores (
        id int,
        nazwa_gracza varchar(20),
        miejsce_gracza int DEFAULT '0', 
        UNIQUE(nazwa_gracza)
        )""")

class Card:
    suits = ["spades","hearts","diamonds","clubs"]
    values = [None, None,"2", "3","4", "5", "6", "7","8", "9", "10","Jack", "Queen","King", "Ace"]

    def __init__(self, v, s):
        """suit + value are ints"""
        self.value = v
        self.suit = s

    def __repr__(self):
        v = self.values[self.value] + " of " + self.suits[self.suit]
        return v
    
class Joker:
    
    jokers = ["Joker"]
    val = ["0"]
    
    def __init__(self, jokers, val):
        self.jokers = jokers
        self.val = val
    
    def __repr__(self):
        rep = 'Joker'
        return rep

class Deck:
    
    def __init__(self):
        self.cards = []
        self.cemetery = []
        
        for i in range(2, 15):
            for j in range(4):
                self.cards.append(Card(i,j))
                               
        for k in range (6):
          for l in range(1):
                self.cards.append(Joker(0,0))
            
        shuffle(self.cards)

class Game:
            
    global response
    slot, slot2, s, y, z, ww, kozyr, d, cemetery = ([] for i in range(9))
    reset, f, p, o, l, v, x, zasys, atak_gracza, shuf, cemet, ofiara, nie_ofiara, pas, kontur = (0 for i in range(15))  
    
    def __init__(self):
        self.deck = Deck()
        
        self.plnum = input("Podaj iloć graczy: ")
        self.plnum = int(self.plnum)
        
        for i in range (self.plnum):
            self.name = input("Podaj nazwę gracza: ")
            self.d.append(self.name)
            
        self.players = {k:[] for k in self.d}
        self.players_score = {k:6 for k in self.d}
        
        for i in range(len(self.players)):
            val = self.d[i]        
            cur.execute( "INSERT OR IGNORE INTO New_scores (nazwa_gracza) VALUES (?)",(val,) )                
            con.commit()
               
        print()    
        print(read_sql_query("SELECT nazwa_gracza AS Gracz, miejsce_gracza AS Punkty FROM New_scores", con)) 

        self.start = 1
        
        self.shuffle()
        print("Nowa tura")
    
    def winner(self):
        for i in range (len(self.players)):
            count = 0
            for j in range (len(self.players[self.d[i]])):
                if isinstance(self.players[self.d[i]][j], Joker):
                        count += 1
            if self.players_score[self.d[i]] == 0 or count >= self.players_score[self.d[i]]:
                print("Koniec gry. Zwycięzca: ", self.d[i])
                print("Wyniki:\n")
                val = self.d[i]
                cur.execute("""
                            UPDATE New_scores
                            SET punkty_gracza = punkty_gracza + 1
                            WHERE nazwa_gracza = (?))
                            """, (val))  
                cur.execute( """DELETE FROM New_scores WHERE miejsce_gracza = 0""")    
                con.commit()
                print(read_sql_query("SELECT nazwa_gracza AS Gracz, miejsce_gracza AS Punkty FROM New_scores", con))                
                close()
        return
                
    def shuffle(self):
        
        for i in range (self.plnum):
            for j in range (self.players_score[self.d[i]]):
                self.players[self.d[i]].append(self.deck.cards.pop())
                
        self.kozyr = self.deck.cards.pop()
        #self.kozyr = Joker(0,0)
        
        self.winner()
        if self.cemet == 1:
            self.cemet == 0
            return
        else:
            self.play_game()
    
    def player_turn(self):                                                  #wszyscy pasują

        if self.pas == (len(self.players)-1):
            self.bonus_round()
            self.kontur = 1
            self.o = self.ofiara  
            self.play_game()
        else:
            return            
        
    def match(self):
        
        for i in range(len(self.slot2)):
            t = self.slot2[i]
            if type(t) is Card:
                self.ww.append(Card.values[t.value])
        self.new_w = list(set(self.ww))
        self.attack()

    def play_game(self):
        
        self.ofiara = self.o
        
        if self.kontur == 1:
            self.l += 1
            if self.zasys == 0:
                if len(self.players[self.d[self.ofiara]]) == 0:               #punkt za wybronienie wszystkich kart            
                    self.players_score[self.d[self.ofiara]] -= 1 
                if self.f == 1:
                    print(self.players_score[self.d[self.ofiara]])            #punkt za wybronienie karty od krupiera na żądanie
                    self.players_score[self.d[self.ofiara]] -= 1
            if self.atak_gracza == 1:                                             #punkt za atak od innego gracza   
                    self.players_score[self.d[self.nie_ofiara]] -= 1 
            
            self.winner()
            
            self.zasys = 0
            self.atak_gracza = 0
            self.f = 0
            self.reset = 0
            self.s = []
            self.pas = 0
            self.kontur = 0
            if len(self.slot2) != 0:
                self.cemetery.append(self.slot2)
            self.slot2 = []
            self.ofiara += 1
            self.nie_ofiara = self.ofiara
            #self.odliczanie()
            print("Nowa tura")
            
            self.ww.clear()
            
            if self.cemet == 1:                                     #rozdanie kart graczom jeżeli talia podczas poprzedniej tury byłą tasowana
                self.shuffle()
                self.exchange()
            
            if self.ofiara > len(self.players):
                print("resecik")
                self.ofiara = 0
                self.nie_ofiara = 0
                self.o = 0
                
            for i in range (len(self.players)):
                if len(self.players[self.d[i]]) < self.players_score[self.d[i]]:
                    self.players[self.d[i]].append(self.deck.cards.pop())                    

        print("\nKrupier atakuje.")

        if len(self.deck.cards) == 0:                       #sprawdzenie czy talia nie jest pusta i przetasowanie jeli tak
            self.cemetery_shuffle()       
        self.slot.append(self.deck.cards.pop())
        self.slot = self.slot[-1:] + self.slot[:-1]
        self.defence()
        
    def attack(self):
        
        if (self.nie_ofiara > len(self.players)-1) or (self.o > len(self.players)-1):
            self.nie_ofiara = 0
            
        if self.ofiara == self.nie_ofiara:
            self.nie_ofiara += 1
        
        if self.f == 1 and self.reset == 0:
            self.nie_ofiara = self.ofiara + 1
            self.reset = 1
        
        
        # if (self.ofiara > len(self.players)-1) or (self.o > len(self.players)-1):
        #     self.ofiara = 0    

        # if self.ofiara == self.nie_ofiara:
        #     self.nie_ofiara += 1
            
        # print(self.nie_ofiara)
        # self.o = self.nie_ofiara
        
        # if self.o > len(self.d):
        #     self.o = 0

        self.player_turn()

        #print("\nGracz ", self.o + 1, " : ", self.d[self.o])
        # print("Tura (l): ", self.l + 1)
        # print("Pass: ", self.pas)
        
        # print("\nofiara: ", self.ofiara+1)
        # print("nie ofiara: ", self.nie_ofiara+1)
        
        self.h = self.players[self.d[self.o]]

        print("\nNastępny gracz - " + self.d[self.nie_ofiara] + ". Wybierz pass (p) lub atakuj kartą")
        
        print("\nKozyr to: ", self.kozyr)
        print("\nMożna zagrać: ", ', '.join([str(i) for i in self.new_w]))              #[str(i) for i in self.new_w]
        print("\nAtakuj "+self.d[self.nie_ofiara]+". Twoje karty to:\n")
        
        for (i, item) in enumerate(self.h, start=1):
            print(i, item)       
        
        m = "Wybierz kartę z ręki by zaatakować, albo spasuj (p):\n"

        while True:
            response = input(m)
            x = 0
            try:                                                        #if userinput.isdigit(): nie działa dla liczb ujemnych
                val = int(response)
            except ValueError:
                if response == 'q':  
                    close()
                
                elif response == 'p':
                    print("\nPasujesz")
                    self.pas += 1
                    self.player_turn()
                    self.attack()
                else:
                    x = 1
            if x == 1:
                continue

            if val <= len(self.players[self.d[self.nie_ofiara]]) and val > 0:
                    self.g = val - 1
                    self.atak_gracza = 1
                    self.loop2()

    def loop2(self):
                
                self.pas = 0
        
                if len(self.slot2) == 12 or self.p == 1:
                    self.p = 0
                    self.kontur = 1
                    self.o += 1
                    print("Koniec tury")
                    self.play_game()
                    
                self.y = self.h[self.g]
                self.new_w = set(self.ww)
                
                print("Gracz ", self.o + 1, " : ", self.d[self.o])
                print("Tura (l): ", self.l + 1)
                print("\nWybrałes: ",self.y)
                
                if type(self.y) is Card:                   
                    if str(self.y.value) in self.new_w:
                        self.ww.append(Card.values[self.y.value])
                        self.h.remove(self.y)
                        self.slot2.append(self.y)
                        print("Na stole są: ",self.slot2)
                        self.x = 1
                    else:
                        self.x = 0                
                else:
                    self.wybor()

                if self.x == 0:
                    print("Ni chuj się tak nie da")
                    self.attack()
                
                elif self.x == 1:
                    self.slot.append(self.y)
                    self.o = self.o - 1
                    self.nie_ofiara += 1
                    self.defence()            

    def wybor(self):
        print("Joker. Czas na wybór")
        self.h.remove(self.y)
        self.cemetery.append(self.y)
        print("\nWybierz kartę do ataku: \n")
        choise = self.deck.cards[-3:]
        for (i, item) in enumerate(choise, start=1):
            print(i, item)        
        while True:
            response = input()
            try:                                                        #if userinput.isdigit(): nie działa dla liczb ujemnych
                val = int(response)
                if val <= 3 and val > 0:
                    self.slot.append.choise.pop(val-1)
                    print("\nPodaj, którą z pozostałych kart odkładasz jako pierwszą na wierzch talii: \n")
                    response = input()
                    try:                                                        #if userinput.isdigit(): nie działa dla liczb ujemnych
                        val = int(response)
                        self.deck.cards.append.choise.pop(val-1)
                        self.deck.cards.append.choise.pop()
                        val = 0
                        self.nie_ofiara += 1
                        self.defence()
                    except ValueError:
                        print("Nie no, tak to nie ;(")
                    continue    
            except ValueError:
                print("\nZły wybór. Wybierz ponownie")
            continue
    
    def defence(self):
         
        # print(Game.cemetery)
        self.player_turn()

        if (self.ofiara > len(self.players)-1) or (self.o > len(self.players)-1):
                self.ofiara = 0            
                
        # if (self.nie_ofiara > len(self.players)-1) or (self.o > len(self.players)-1):
        #     self.nie_ofiara = 0
        # if self.ofiara == self.nie_ofiara:
        #     self.nie_ofiara += 1
                
        self.o = self.ofiara            
        self.z = self.slot[0]

        #print("\nGracz ", self.o + 1, " : ", self.d[self.o])
        # print("Tura (l): ", self.l + 1)
        # print("Pass: ", self.pas)
        
        print("\nWynik: ")
        for key, value in self.players_score.items():
            print(key, ' : ', value)
        
        # print("\nofiara: ", self.ofiara+1)
        # print("nie ofiara: ", self.nie_ofiara+1)
        
        if type(self.slot[0]) is Joker:
            print("\n\nZebrano Jokera!!!\n\n")
            #print("\nLicytacja!")
            #self.odliczanie()
            self.ssanie()           
            
        print("\nKozyr to: ", self.kozyr)
        print("Do pobicia: ", self.slot[0])
        print("\nBroń się "+self.d[self.o]+". Twoje karty to:\n")
        for (i, item) in enumerate(self.players[self.d[self.ofiara]], start=1):
            print(i, item)       
        
        m = "Wcisnij q by wyjsc. Wybierz karte z reki by się bronić:\n"
        
        while True:
            response = input(m)
            x = 0
            try:                                                        #if userinput.isdigit(): nie działa dla liczb ujemnych
                val = int(response)
            except ValueError:
                if response == 'q':  
                    close()
                elif response == 'p':
                    print("\nPasujesz i ssiesz")
                    self.kontur = 1
                    self.ssanie()
                else:
                    x = 1
            if x == 1:
                continue
            
            if val <= len(self.players[self.d[self.ofiara]]) and val > 0:
               self.g = val - 1
               self.loop()
            else:
                self.defence()            


    def loop(self):   
                                                                          #obrona
        self.h = self.players[self.d[self.o]]
        self.y = self.h[self.g]
        
        print("Gracz ", self.o + 1, " : ", self.d[self.o])
        print("Tura (l): ", self.l + 1)    
        
        print("\nWybrałes: ",self.h[self.g])
        
        if type(self.z) is Joker:
            print("Licytacja!")
        else:
            if type(self.y) is Card:
                if type(self.kozyr) is Joker:
                    if self.y.value > self.z.value:
                        self.h.remove(self.y)
                        self.slot2.append(self.y)
                        self.slot.remove(self.z)
                        self.slot2.append(self.z)
                        print("Na stole są: ",self.slot2)
                        self.x = 1
                    else:
                        self.x = 0
       
                elif self.z.suit == self.kozyr.suit:
                    if self.y.suit == self.kozyr.suit and self.y.value > self.z.value:
                        print("Kozyr bije")
                        self.h.remove(self.y)
                        self.slot2.append(self.y)
                        self.slot.remove(self.z)
                        self.slot2.append(self.z)
                        print("Na stole są: ",self.slot2)
                        self.x = 1
                        
                    else:
                        self.x = 0
                elif self.y.suit == self.kozyr.suit and self.z.suit != self.kozyr.suit:
                    self.h.remove(self.y)
                    self.slot2.append(self.y)
                    self.slot.remove(self.z)
                    self.slot2.append(self.z)
                    print("Na stole są: ",self.slot2)
                    self.x = 1
                elif self.y.suit == self.z.suit and self.y.value > self.z.value:
                    self.h.remove(self.y)
                    self.slot2.append(self.y)
                    self.slot.remove(self.z)
                    self.slot2.append(self.z)
                    print("Na stole są: ",self.slot2)
                    self.x = 1
                    
                else:
                    self.x = 0
                    self.defence()
                    
            else:
                print("Jocker rozjebal")
                self.h.remove(self.y)
                self.slot2.append(self.y)
                self.slot.remove(self.z)
                self.slot2.append(self.z)
                print("Na stole są: ",self.slot2)
                self.x = 1
                
        if self.x == 0:
            print("\nNi chuj się tak nie da")
            self.defence()
        else:
            print("Git\n")
            self.match()
                        
    def ssanie(self):
        self.slot2.extend(self.slot)
        self.slot.clear()
        self.players[self.d[self.ofiara]].extend(self.slot2)
        self.slot2.clear()
        self.zasys = 1
        self.kontur = 1
        if (self.nie_ofiara > len(self.players)-1) or (self.o > len(self.players)-1):
            self.nie_ofiara = 0
        
        self.play_game()

    # def odliczanie(self):
    #     print("Start za: ")
    #     for i in range (0,3):
    #         print(3-i, "!")
    #         sleep(1)
    #     self.ssanie()

    def bonus_round(self):
        if self.s == [] and self.f == 0:
            self.s = self.deck.cards[-1]
            print(self.s)
            if type(self.s) is Card:
                if self.s.value in self.new_w:
                    if len(self.deck.cards) == 0:                       #sprawdzenie czy talia nie jest pusta i przetasowanie jeli tak
                        self.cemetery_shuffle()
                    else:
                        self.deck.cards.pop()
                        self.defence()
                else:
                    while True:
                        response = input(self.d[self.ofiara] + ". Czy chcesz dodatkową kartę? T-tak lub N-nie\n")
                        
                        if response == "T":
                            if len(self.deck.cards) == 0:                       #sprawdzenie czy talia nie jest pusta i przetasowanie jeli tak
                                self.cemetery_shuffle()
                            else:
                                self.slot.append(self.deck.cards.pop())
                                print("Zaatakowano gracza")
                                self.pas = 0
                                self.f = 1                  #marker bonusowej rundy
                                response = ""
                                print(self.f)
                                self.defence()
                        elif response == "N":
                            self.s = []
                            return
                        else:
                            print("Nieprawidłowy wybór")
                            continue
            else:                     
                print("Rozdawanie po jednej karcie dla wszystkich - faza testów")             #testy - rozdanie kart do wyboru
                return
        else: return

    def cemetery_shuffle(self):
        if len(self.deck.cards) == 0:
            self.deck.cards.append(self.cemetery_shuffle())
            self.cemetery.clear()
            self.cemet = 1
            shuffle(self.deck.cards)
            return
        else: return

    def exchange(self):
        for i in range (self.plnum):
            wymiana = []
            while True:
                print("\Gracz: ", self.d[i])                
                m = "Wybierz kartę do wymiany (cyfra - jedna na raz) i zatwierdź wybór (Enter). Wcinij dowolny znak poza cyfrą, aby zakończyć wybór. \n"
                
                h = self.players[self.d[i]]
                x = int(ceil((self.players_score[self.d[i]])/2))
                
                for (i, item) in enumerate(h, start=1):
                    print(i, item) 
                response = input(m)
                
                if x == len(wymiana):
                    stop = 1
                
                try:                                                        #if userinput.isdigit(): nie działa dla liczb ujemnych
                    val = int(response)
                    if val <= x and val > 0:
                        wymiana.append(val-1)
                        cont = 1
                    else:
                        cont = 1
                        
                except ValueError:
                    if len(wymiana) != 0:
                        for i in range (len(wymiana)):
                            y = h[wymiana[i]]
                            h.remove(y)
                            h.append(self.deck.cards.pop())
                        stop = 1
                    else:
                        stop = 1
                    
                if stop == 1:
                    stop = 0
                    break
                
                elif cont == 1:
                    cont = 0
                    continue
        return      


def close():
    cur.execute("DELETE FROM New_scores WHERE miejsce_gracza = 0 ")
    con.commit()
    con.close()
    exit()


game = Game()
game.play_game()