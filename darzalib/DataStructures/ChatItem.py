from .IDataStructure import IDataStructure

class ChatItem(IDataStructure):

    def __init__(self, color, ownerID, text):
        self.color = color
        self.ownerID = ownerID
        self.text = text

    def PrintString(self):
        super().PrintString()