class HighScores: #helps with leaderboard
    
    def __init__(self): #constructor, instead of using a dictionary, two lists are used. this is because the dictionary didn't allow for the same username to be present twice
        
        self.usr = []
        self.scores  = []
    
    def addNewResult(self, username, score): #adds a new result
            
        minimum = min(self.scores)
        pos = 0
            
        for i in range(len(self.scores)):
                
            if i == minimum:
                    
                pos = i
            
        if minimum < score:
                
            self.scores.remove(minimum)
            self.scores.append(score)
            del self.usr[pos]
            self.usr.append(username)
                
        
    def loadData(self): #loads the data
        
        scFile = open("HighScores.txt", "r")
        
        for line in scFile:
            
            data = line.split(",")
            self.usr.append(data[0])
            self.scores.append(int(data[1]))
            
        scFile.close()
    
    def updateData(self): #updates the data
        
        scFile = open("HighScores.txt", "w")
        
        for i in range(len(self.scores)):
            
            line = self.usr[i] + "," + str(self.scores[i]) + ","
            scFile.write(line + "\n")
        
        scFile.close()
    
    def getTop5(self): #gets the leader board
        
        ordName = []
        ordScore = []
        temp = "Leaderboard:\n\n"
        
        for i in range(len(self.scores)):
            
            maximum = max(self.scores)
            ordScore.append(maximum)
            pos = 0
            
            for j in range(len(self.scores)):
                
                if maximum == j:
                    
                    pos = j
            
            ordName.append(self.usr[pos])
            self.scores.remove(maximum)
            self.usr.remove(self.usr[pos])
            temp = temp + str(i + 1) + ". " + ordName[i] + " - " + str(ordScore[i]) + "\n"
            
        self.usr = ordName
        self.scores = ordScore
        return temp
        