class HighScores: #helps with leaderboard
    
    def __init__(self): #constructor
        
        self.usr = []
           
    def addNewResult(self, username, score): #adds a new result
            
        self.usr.append(username + "," + str(score) + ",")
        
    def loadData(self): #loads the data
        
        scFile = open("HighScores.txt", "r")
        
        for line in scFile:
            
            data = line.split(",")
            self.usr.append(data[0] + "," + data[1] + ",")
            
        scFile.close()
    
    def updateData(self): #updates the data
        
        scFile = open("HighScores.txt", "w")
        
        for i in range(len(self.usr)):
            
            scFile.write(self.usr[i] + "\n")
        
        scFile.close()
    
    def getTop5(self): #gets the leader board
        
        scores = []
        names = []
        pos = 0
        temp = "Leaderboard:\n\n"
        
        for i in range(len(self.usr)):
            
            data = self.usr[i].split(",")
            names.append(data[0])
            scores.append(int(data[1]))
            
        for j in range(5):
            
            maximum = max(scores)
            pos = scores.index(maximum)
            temp = temp + str(j + 1) + ". " + names[pos] + " - " + str(scores[pos]) + "\n"
            scores.remove(maximum)
            names.remove(names[pos])
        
        return temp
