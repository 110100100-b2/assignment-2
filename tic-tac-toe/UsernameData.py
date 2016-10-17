class UsernameData: #Helps us load the leader board
    
    def __init__(self): #constructor
        
        self.allGameData = []
        
    def loadCurrentData(self): #loads the data in the text file
                
        scFile = open("gameData.txt", "r")
                
        for line in scFile:
                    
            data = line.split()
            self.allGameData.append(data[0])
                
        scFile.close() 
        return self.allGameData    
             
    def addNewResult(self, userName): #adds a new result
        
        self.allGameData.append(userName)
    
    def syncFile(self): #writes the data in our list to the text file
        
        scFile = open("gameData.txt", "w")
        
        for i in range(len(self.allGameData)):
            
            scFile.write(self.allGameData[i] + "\n")
        
        scFile.close()
        
    def getTop5Players(self): #determines the top 5 players
        
        pop_dict = {}
        top5 = "Most Wins:\n\n"
            
        for i in range(len(self.allGameData)):
               
            if self.allGameData[i] not in pop_dict.keys():
                   
                pop_dict[self.allGameData[i]] = self.allGameData.count(self.allGameData[i])
        
        for i in range(5):
        
            maximum = max(pop_dict, key = pop_dict.get)
            top5 = top5 + str(i + 1) + ". " + maximum + " - " + str(pop_dict[maximum]) + "\n" 
            del pop_dict[maximum]        
            
        return top5