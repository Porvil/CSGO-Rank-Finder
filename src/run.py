import sys
from PyQt5.QtWidgets import * 
from PyQt5.QtGui import QFont
from PyQt5.Qt import *
from PyQt5 import uic

from backend import getRanks
from utils import *

"""
GUI class
"""
class Ui(QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi(getUIFilePath(), self)
        
        self.setWindowIcon(QIcon(getIconFilePath()))
        # icon = QIcon()
        # icon.addFile(u"csgo.ico", QSize(), QIcon.Normal, QIcon.Off)
        
        # output variable to hold PrettyTableString
        self.output = ""
        
        # get UI references from .ui file and do initializations for UI elements
        self.getUiReferences()
        self.initUI()
        
        # show the GUI
        self.show()
    
    """
    gets UI references from .ui file
    """
    def getUiReferences(self):
        # Push Button
        self.pb_addFriends = self.findChild(QPushButton, 'pb_addFriends')
        self.pb_copyRanks  = self.findChild(QPushButton, 'pb_copyRanks')
        self.pb_clear = self.findChild(QPushButton, 'pb_clear')
        self.pb_showRanks  = self.findChild(QPushButton, 'pb_showRanks')
        
        # Line Edit
        self.le_status  = self.findChild(QLineEdit, 'le_status')
        
        # Text Edit
        self.te_input  = self.findChild(QTextEdit, 'te_input')
        
        # Table Widget
        self.tw_output  = self.findChild(QTableWidget, 'tw_output')
    
    """
    initializations all UI elements
    """
    def initUI(self):
        self.initButtonFunctions()
        self.initTableWidget()
        
        self.le_status.setText(INIT_STATUS) 
        self.te_input.setPlaceholderText(TEXT_PLACEHOLDER) 
    
    """
    sets Row in TableWidget based on player data
    """
    def inflateRowWithPlayerData(self, row, player):
        labels = [
                    self.getTextLabel(player.name),
                    self.getImageLabel(getRankImagePath(player.curRank)),
                    self.getImageLabel(getRankImagePath(player.bestRank)),
                    self.getTextLabel(str(player.totalWins)),
                    self.getTextLabel(str(player.HS)),
                    self.getTextLabel(str(player.KD))
                ]
        
        for i in range(NO_OF_COLUMNS):
            self.tw_output.setCellWidget(row, i, labels[i])
    
    """
    returns TextLabel based on string
    """
    def getTextLabel(self, string):
        label = QLabel()
        label.setAlignment(Qt.AlignCenter)
        label.setText(string)
        return label
    
    """
    returns ImageLabel based on imagePath
    """
    def getImageLabel(self, imagePath):
        label = QLabel() 
        pixmap = QPixmap(imagePath)
        label.setPixmap(pixmap)
        label.setScaledContents(True)
        return label
    
    """
    connect all PushButtons to their functions
    """
    def initButtonFunctions(self):
        self.pb_addFriends.clicked.connect(self.click_pb_addFriends)
        self.pb_copyRanks.clicked.connect(self.click_pb_copyRanks)
        self.pb_clear.clicked.connect(self.click_pb_clear)
        self.pb_showRanks.clicked.connect(self.click_pb_showRanks)
    
    """
    initializes TableWidget
    """
    def initTableWidget(self):
        self.tw_output.setColumnCount(NO_OF_COLUMNS)
        self.tw_output.setHorizontalHeaderLabels(HEADER_LABELS)
        self.tw_output.verticalHeader().hide()
        
        font = QFont()
        font.setBold(True)
        
        for i in range(NO_OF_COLUMNS):
            self.tw_output.horizontalHeader().resizeSection(i, HEADER_LABEL_SIZES[i])
            self.tw_output.horizontalHeaderItem(i).setFont(font)
    
    """
    based on "te_input", appends friend id's to blocklist file
    """
    def click_pb_addFriends(self):
        newFriends = []
        currentInput = self.te_input.toPlainText()
        
        for line in currentInput.split():
            for data in line.split():
                try:
                    newFriends.append(int(data))
                except:
                    if data.startswith("STEAM_"):
                        steamId64 = steamIdToSteamId64(data)
                        if steamId64 != -1:
                            newFriends.append(steamId64)
        
        if len(newFriends) == 0:
            self.le_status.setText(WRONG_FRIENDS_TEXT)
        else:
            self.le_status.setText(FRIENDS_ADDED)
        
        writeFriendsFile(newFriends)
    
    """
    copies rank data to clipboard
    """
    def click_pb_copyRanks(self):
        sendClipboardData(self.output)
    
    """
    clears everything
    """
    def click_pb_clear(self):
        self.output = ""
        self.le_status.setText(INIT_STATUS)
        self.te_input.setText("")
        self.clearTableWidget()
    
    """
    based on "te_input", finds rank data for every player(except blocklist) and shows data in TableWidget
    """
    def click_pb_showRanks(self):
        currentInput = getClipboardData()
        sendClipboardData("")
        self.te_input.setText(currentInput)
        
        players = getRanks(currentInput)
        
        self.clearTableWidget()
        
        if len(players) == 0:
            self.le_status.setText(WRONG_INPUT_TEXT)
        else:
            self.tw_output.setRowCount(len(players))
            
            for i in range(len(players)):
                self.inflateRowWithPlayerData(i, players[i])
            
            self.output = getPrettyTableString(players)
            self.le_status.setText(RANKS_FOUND)
    
    """
    clears TableWidget
    """
    def clearTableWidget(self):
        while self.tw_output.rowCount() > 0:
            self.tw_output.removeRow(0)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Ui()
    app.exec_()