from cgi import test
from random import *
from collections import Counter
import sqlite3
import inquirer
from datetime import *

class ConnectSql():
    try:
        conn = sqlite3.connect('database/db.sqlite')
        cur = conn.cursor()
        print("Base de données crée et correctement connectée à SQLite")
    except sqlite3.Error as error:
        print("Erreur lors de la connexion à SQLite", error)

class SingletonFactory:
    __instance = None
    @staticmethod
    def get_instance() -> ConnectSql:
        if SingletonFactory.__instance is None :
            print("Création du service")
            SingletonFactory.__instance = ConnectSql()
        return SingletonFactory.__instance

class ResumeFactory:
    def run(self, *args):
        if (len(args) == 2):
            Game().WhichRoll(args[0], args[1])
        if(len(args) == 4):
            Game().WhichRollResume(args[0], args[1], args[2], args[3])
        
class Request:
    
    def __init__(self, sql_instance):
        self.__instance__(sql_instance)
        
    def __instance__(self, sql_instance):
        self.sql = sql_instance
    
    def createGame(self):
        self.sql.cur.execute("""Insert into Score values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", (None, "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", 0, str(datetime.now())))
        self.sql.conn.commit()
        
    def resumeGame(self):
        loadGame = self.sql.cur.execute("""Select * From Roll inner join Score on Roll.idGame = Score.idScore where Score.statusPartie = 0""")
        self.sql.conn.commit()
        loadGame = loadGame.fetchall()
        return loadGame
    
    def getIdScore(self):
        idScore = self.sql.cur.execute("""Select idScore From Score where statusPartie = 0""")
        self.sql.conn.commit()
        idScore = idScore.fetchall()
        return idScore
    
    def Roll(self, choice, roll):
        idScore = self.getIdScore()
        print (idScore[0][0])
        self.sql.cur.execute("""Insert into Roll values (?, ?, ?, ?, ?, ?, ?, ?)""", (None, idScore[0][0], str(choice[0]), str(choice[1]), str(choice[2]), str(choice[3]), str(choice[4]), str(roll)))
        self.sql.conn.commit()
        
    def reRoll(self, choice, roll):
        self.sql.cur.execute("""UPDATE Roll SET resultDesOne = ?, resultDesTwo = ?, resultDesThree = ?, resultDesFour = ?, resultDesFive = ?, nbRollFait = ? where idLancer = (SELECT MAX(idLancer) FROM Roll)""", (str(choice[0]), str(choice[1]), str(choice[2]), str(choice[3]), str(choice[4]), str(roll - 1)))
        self.sql.conn.commit()
    
    def addScore(self, combi, score):
        self.sql.cur.execute("""UPDATE Score SET scoreTotal = ?, combinationOne = ?, combinationTwo = ?, combinationThree = ?, combinationFour = ?, combinationFive = ?, combinationSix = ?, combinationBrelan = ?, combinationSquare = ?, combinationFull = ?, combinationYams = ?, combinationChance = ?, combinationSmallSuite = ?, combinationBigSuite = ? where idScore = (SELECT MAX(idScore) FROM Score)""", (score, combi["1"], combi["2"], combi["3"], combi["4"], combi["5"], combi["6"], combi["brelan"], combi["carrés"], combi["full"], combi["yams"], combi["chance"], combi["petite suite"], combi["grande suite"]))
        self.sql.conn.commit()
     
    def finishGame(self, combi, score):
        self.sql.cur.execute("""UPDATE Score SET scoreTotal = ?, combinationOne = ?, combinationTwo = ?, combinationThree = ?, combinationFour = ?, combinationFive = ?, combinationSix = ?, combinationBrelan = ?, combinationSquare = ?, combinationFull = ?, combinationYams = ?, combinationChance = ?, combinationSmallSuite = ?, combinationBigSuite = ?, statusPartie = ? where idScore = (SELECT MAX(idScore) FROM Score)""", (score, combi["1"], combi["2"], combi["3"], combi["4"], combi["5"], combi["6"], combi["brelan"], combi["carrés"], combi["full"], combi["yams"], combi["chance"], combi["petite suite"], combi["grande suite"], 1))
        self.sql.conn.commit()

    def deleteGameInProgress(self):
        self.sql.cur.execute("""DELETE FROM Roll where idGame in (Select idGame from Roll INNER JOIN Score on Score.idScore = Roll.idGame where Score.statusPartie = 0)""")
        self.sql.cur.execute("""Delete From Score where statusPartie = 0""")
        self.sql.conn.commit()
    
    def gameHistory(self):
        idHistory = self.sql.cur.execute("""Select * From Score where statusPartie = 1""")
        self.sql.conn.commit()
        idHistory = idHistory.fetchall()
        return idHistory
        
class Menu:
    
    def __init__(self, sql_instance):
        self.__variable__(sql_instance)
    
    def __variable__(self, sql_instance):
        self.DiceRoll = []
        self.DiceWichRoll = []
        self.tabResume = []
        self.resumeDice = []
        self.resumeCombi = []
        self.resumeRoll = None
        self.resumeScore = None
        self.sql = sql_instance
        
        
    def chooseMenuLaunch(self, answers):
        if (answers["Menu"] == "Quitter"):
            self.quitGame()
        if (answers["Menu"] == "Nouvelle Partie"):
            self.launchGame()
        if (answers["Menu"] == "Reprendre"):
            self.resume()
        if (answers["Menu"] == "Historique"):
            self.historiqueGame()
    
    def getResume(self):
        for i in range (2, 7):
            self.resumeDice.append(int(self.tabResume[0][i]))
        self.resumeRoll = int(self.tabResume[0][7])
        for i in range (10, 22):
            print(Const.combi.keys[i])
        self.resumeCombi = {'1': int(self.tabResume[0][10]),
                            '2': int(self.tabResume[0][11]),
                            '3': int(self.tabResume[0][12]),
                            '4': int(self.tabResume[0][13]),
                            '5': int(self.tabResume[0][14]),
                            '6': int(self.tabResume[0][15]),
                            'brelan': int(self.tabResume[0][16]),
                            'full': int(self.tabResume[0][17]),
                            'carrés': int(self.tabResume[0][18]),
                            'yams': int(self.tabResume[0][19]),
                            'petite suite': int(self.tabResume[0][20]),
                            'grande suite': int(self.tabResume[0][21]),
                            'chance': int(self.tabResume[0][22])}
        self.resumeScore = int(self.tabResume[0][9])
    
    def resume(self):
        print(self.tabResume)
        self.resumeDice.clear()
        self.resumeCombi.clear()
        self.tabResume = Req.resumeGame()
        if (self.tabResume[0][7] < '3'):
            self.getResume()
            Resume.run(self.resumeDice, self.resumeRoll, self.resumeCombi, self.resumeScore)
        else:
            self.getResume()
            C.searchCombination(self.resumeDice, self.resumeCombi, self.resumeScore)
        
        
    def quitGame(self):
        self.sql.conn.close()
        exit()
    
    def launchGame(self):
        Req.deleteGameInProgress()
        Req.createGame()
        Game().LaunchGame(Constante.combi, Constante.score)
    
    def historiqueGame(self):
        History = Req.gameHistory()
        Game().showHistory(History)
    
    def MainMenu(self):
        questions = [
            inquirer.List('Menu',
                message="Que souhaitez vous faire ? ",
                choices=['Reprendre', 'Nouvelle Partie', 'Historique', 'Quitter'],
            ),
        ]
        answers = inquirer.prompt(questions)
        self.chooseMenuLaunch(answers)
    
    def chooseRollOrNot(self, answers, roll, valueModif, combi, score):
        if (answers["Menu"] == "Oui"):
            valueModif = self.ReRollMenu(valueModif, roll)
            print(valueModif)
            R.WhichDiceChange(valueModif, roll, combi, score)
        if (answers["Menu"] == "Non"):
            C.searchCombination(valueModif, combi, score)
    
    def chooseWhichReroll(self, answers, roll, choice):
        if (answers["Menu"] == []):
            print("Vous n'avez pas sélectionner de dés a relancé, veuillez choisir.")
            self.ReRollMenu(choice, roll)
        for v in answers["Menu"]:
           self.DiceWichRoll.append(v)
        print(self.DiceRoll)
        print(self.DiceWichRoll)
        return D.roll_indexes(self.DiceWichRoll, roll, choice)
    
    def chooseWhichCombination(self, combiPossible, answers, score):
        for k, v in combiPossible.items():
            if (k == answers["Menu"]):
                Constante.combi[str(k)] = v
                score  = score + v
                Req.addScore(Constante.combi, score)
                print (v)
                print (Constante.combi)
                print("prochain tours:")
                Game().LaunchGame(Constante.combi, score)
    
    def chooseWhichSacrifice(self, combiSacrifice, answers, score):
        for i in combiSacrifice:
            if (i == answers["Menu"]):
                Constante.combi[i] = "X"
                Req.addScore(Constante.combi, score)
                print("prochain tours:")
                Game().LaunchGame(Constante.combi, score)
    
    def RollMenu(self, valueModif, roll, combi, score):
        questions = [
            inquirer.List('Menu',
                message="Voulez vous relancer les dés ? ",
                choices=['Oui', 'Non'],
            ),
        ]
        answers = inquirer.prompt(questions)
        self.chooseRollOrNot(answers, roll, valueModif, combi, score)

    
    def ReRollMenu(self, choice, roll):
        print('-----------------------------')
        print(choice)
        questions = [
            inquirer.Checkbox('Menu',
                message="Quel(s) dé(s) voulez-vous relancer (Espace pour en choisir plusieurs) ?",
                choices=['1', '2', '3', '4', '5'],
            ),
        ]
        answers = inquirer.prompt(questions)
        self.DiceRoll = self.chooseWhichReroll(answers, roll, choice)
        print('jendbdz')
        print (self.DiceRoll)
        return self.DiceRoll
    
    def ChooseCombination(self, combiPossible, score):
        print (combiPossible)
        questions = [
            inquirer.List('Menu',
                message="Quel combinaison souhaitez-vous faire ?",
                choices= combiPossible,
            ),
        ]
        answers = inquirer.prompt(questions)
        self.chooseWhichCombination(combiPossible, answers, score)

    
    def ChooseSacrifice(self, combiSacrifice, score):
        questions = [
            inquirer.List('Menu',
                message="Quel combinaison souhaitez-vous sacrifier ?",
                choices= combiSacrifice,
            ),
        ]
        answers = inquirer.prompt(questions)
        self.chooseWhichSacrifice(combiSacrifice, answers, score)
        
class Game:

    def __init__(self):
        self.__variable__()
    
    def __variable__(self):
        self.rollDice = []
        self.roll = 1
        
    def rollAllDice(self):
        self.rollDice = D.rollAll()
    
    def rollOrNot(self):
        Req.Roll(self.rollDice, self.roll)
    
    def WhichRoll(self, combi, score):
        self.rollAllDice()
        self.rollOrNot()
        print (self.rollDice)
        R.WhichDiceChange(self.rollDice, self.roll, combi, score)
    
    def WhichRollResume(self, resumeDice, resumeRoll, resumeCombi, resumeScore):
        R.WhichDiceChange(resumeDice, resumeRoll, resumeCombi, resumeScore)
    
        
    def LaunchGame(self, combi, score):
        self.rollDice.clear()
        Resume.run(combi, score)
        # self.WhichRoll(combi, score)

    def showHistory(self, historique):
        for i in historique:
            print (i)

class Roll:
    
    def __init__(self):
        self.__variable__()
        
    def __variable__(self):
        self.maxRoll = 3
    
    def WhichDiceChange(self, choice, roll, combi, score):
        print(choice)
        print ("Nombre de lancer effectué: " + str(roll))
        if (roll <= self.maxRoll):
            roll += 1
            M.RollMenu(choice, roll, combi, score)
        if (roll >= self.maxRoll):
            print('Vous ne pouvez plus lancer vos dés veuillez choisir la combinaison que vous souhaitez faire')
            roll = 1
            C.searchCombination(choice, combi, score)

class Dices:
    
    def __init__(self):
        self.__variable__()
        self.diceAppend()
            
    def diceAppend(self):
        for i in range (0, 5):
            self.dices.append(Dice())
    
    def __variable__(self):
        self.dices = []
        self.TabDice = []
        self.dices.clear()
        
    def rollAll(self):
        self.TabDice.clear()
        for i in range (len(self.dices)):
            self.TabDice.append(self.dices[i].roll())
        return self.TabDice

    def roll_indexes(self, index, roll, choice):
        print('ok')
        print(index)
        print('ok')
        print (choice)
        self.TabDice = choice
        for i in index:
            self.TabDice[int(i) - 1] = self.dices[int(i) - 1].roll()
        Req.reRoll(self.TabDice, roll)
        print('test')
        print (self.TabDice)
        print(choice)
        return choice

class Dice:
    
    def __init__(self):
        self.__variable__()
        
    def __variable__(self):
        self.face_dice = 6
        self.value = None
    
    def roll(self):
        self.value = randint(1, self.face_dice)
        return self.value

class Combination:
    
    def __init__(self, sql_instance):
        self.__variable__(sql_instance)
    
    def __variable__(self, sql_instance):
        self.resultDice = None
        self.combi_dispo = {}
        self.nbSuites = []
        self.nbDoublon = []
        self.nbBrelan = []
        self.combiSacrifice = []
        self.calcul = 0
        self.sql = sql_instance

    def clearTab(self):
        self.combi_dispo.clear()
        self.nbSuites.clear()
        self.nbBrelan.clear()
        self.nbDoublon.clear()
    
    def isNumber(self, i, combi) :
        if (self.count[i] >= 0 and (combi[str(i)] != "X" and combi[str(i)] == 0)):
            self.calcul = i * self.count[i]
            self.combi_dispo[i] = self.calcul
            self.nbSuites.append(i)
    
    def isDoublon(self, i, TabDice) :
        if (self.count[i] == 2):
            self.nbDoublon.append(i)
            TabDice.remove(i)
    
    def isBrelan(self, i, combi) :
        if (self.count[i] == 3 and (combi['brelan'] != "X" and combi['brelan'] == 0)):
            self.calcul = i * 3
            self.combi_dispo["brelan"] = self.calcul
            self.nbBrelan.append(i)
    
    def isSquare(self, i, combi):
        if (self.count[i] == 4 and (combi['carrés'] != "X" and combi['carrés'] == 0)):
            self.calcul = i * 4
            self.combi_dispo["carrés"] = self.calcul
    
    def isFull(self, i, combi):
        if (self.nbDoublon != [] and self.nbBrelan != [] and (combi['full'] != "X" and combi['full'] == 0)):
            self.combi_dispo["full"] = 25
    
    def isYams(self, i, combi):
        if (self.count[i] == 5 and (combi['yams'] != "X" and combi['yams'] == 0)):
            self.combi_dispo["yams"] = 50
    
    def isLittleSuite(self, combi):
        if ((1 in self.nbSuites and 2 in self.nbSuites and 3 in self.nbSuites and 4 in self.nbSuites) or (2 in self.nbSuites and 3 in self.nbSuites and 4 in self.nbSuites and 5 in self.nbSuites) or (3 in self.nbSuites and 4 in self.nbSuites and 5 in self.nbSuites and 6 in self.nbSuites) and (combi['petite suite'] != "X" and combi['petite suite'] == 0)): 
            self.combi_dispo["petite suite"] = 25
    
    def isBigSuite(self, combi):
        if ((1 in self.nbSuites and 2 in self.nbSuites and 3 in self.nbSuites and 4 in self.nbSuites and 5 in self.nbSuites) or (2 in self.nbSuites and 3 in self.nbSuites and 4 in self.nbSuites and 5 in self.nbSuites and 6 in self.nbSuites) and (combi['grande suite'] != "X" and combi['grande suite'] == 0)):
            self.combi_dispo["grande suite"] = 30
    
    def isChance(self, i, combi):
        if (combi['chance'] != "X" and combi['chance'] == 0):
            self.calcul = self.calcul + i
            self.combi_dispo["chance"] = self.calcul
    
    def choiceCombination(self, TabDice, combi, score):
        self.resultDice = self.enterCombinaison(self.combi_dispo, TabDice, combi, score)
        return self.resultDice
        
    def searchCombination(self, TabDice, combi, score):
        print (TabDice)
        self.clearTab()
        TabDice.sort()
        self.count = Counter(TabDice)
        for i in TabDice:
            self.isNumber(i, combi)
            self.isDoublon(i, TabDice)
            self.isBrelan(i, combi)
            self.isSquare(i, combi)
            self.isFull(i, combi)
            self.isYams(i, combi)
            self.isLittleSuite(combi)
            self.isBigSuite(combi)
            self.isChance(i, combi) 
        return self.choiceCombination(TabDice, combi, score)

    def chooseCombiSacrifice(self, score):
            print (self.combiSacrifice)
            M.ChooseSacrifice(self.combiSacrifice, score)
    
    def chooseResult(self, combiPossible, score):
        print(combiPossible)
        M.ChooseCombination(combiPossible, score)
    
    def FinishGame(self, score, combi):
            if score >= 63:
                score  = score + 35
            print("plus de combinaison possible parti finis")
            print("Votre score final est de : " + str(score) + " points")
            Req.finishGame(combi, score)
            self.sql.conn.close()
            exit()
    
    def appendListSacrifice(self, combi):
        for k, v in combi.items():
            if (combi[k] == 0):
                self.combiSacrifice.append(k)

    def enterCombinaison(self, combiPossible, TabDice, combi, score):
        self.combiSacrifice.clear()
        self.appendListSacrifice(combi)
                
        if (not combiPossible and self.combiSacrifice != []):
            self.chooseCombiSacrifice(score)
        
        if (self.combiSacrifice == [] and not combiPossible):
            self.FinishGame(score, combi)
        
        self.chooseResult(combiPossible, score)
               
class Constante :
    combi = {'1': 0,
         '2': 0,
         '3': 0,
         '4': 0,
         '5': 0,
         '6': 0,
         'brelan': 0,
         'full': 0,
         'carrés': 0,
         'yams': 0,
         'petite suite': 0,
         'grande suite': 0,
         'chance': 0}
    score = 0
    Text = None
    
    def printText(self, text):
        print(text)  
 
       
S = SingletonFactory()       
D = Dices()
C = Combination(S.get_instance()) 
R = Roll()
M = Menu(S.get_instance())
Req = Request(S.get_instance())
Resume = ResumeFactory()
Const = Constante()
M.MainMenu()