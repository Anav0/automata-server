class Loger:
    def __init__(self,filePath):
        self.filePath = filePath

    def log(self, str):
        with open(self.filePath, 'a') as file:
            file.write(str+"\n")

    def clear(self):
        with open(self.filePath, 'w') as file:
            file.write("")
