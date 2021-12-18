import sys
from PyQt5.QtWidgets import * 
from PyQt5.QtGui import QFont
from PyQt5.Qt import *
from PyQt5 import uic

from settings import Settings
from backend import *
from utils import *
from multithreading import *

"""
GUI class
"""
class Ui(QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi(getUIFilePath(), self)
        
        # set app icon
        self.setWindowIcon(QIcon(getIconFilePath()))
        
        # global variables
        self.output = ""
        self.initial = True
        self.excludeFriends = True
        self.autoFindRank = True
        self.autoCopyOutput = True
        
        # get UI references from .ui file and do initializations for UI elements
        self.getUiReferences()
        self.initUI()
        
        # multithreading thread pool
        self.threadpool = QThreadPool()
        
        # show the GUI
        self.show()
        
        # if autoFindRank is enabled, automatically pastes clipboard data and starts rank search
        if self.autoFindRank:
            currentInput = getClipboardData()
            self.te_input.setText(currentInput)
            self.click_pb_showRanks()
    
    """
    gets UI references from .ui file
    """
    def getUiReferences(self):
        # Push Button
        self.pb_clearInput  = self.findChild(QPushButton, 'pb_clearInput')
        self.pb_pasteInput  = self.findChild(QPushButton, 'pb_pasteInput')
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
        
        # CheckBox
        self.cb_friends  = self.findChild(QCheckBox, 'cb_friends')
        self.cb_autoStart  = self.findChild(QCheckBox, 'cb_autoStart')
        self.cb_autoCopy  = self.findChild(QCheckBox, 'cb_autoCopy')
        
        # ProgressBar
        self.progressBar  = self.findChild(QProgressBar, 'progressBar')
    
    """
    initializes all UI elements
    """
    def initUI(self):
        self.le_status.setText(INIT_STATUS) 
        self.te_input.setPlaceholderText(TEXT_PLACEHOLDER)
        
        self.initButtonFunctions()
        self.initButtonIconAndHoverText()
        self.initTableWidget()
        self.initSettingsUI()
    
    """
    connect all PushButtons to their functions
    """
    def initButtonFunctions(self):
        self.pb_addFriends.clicked.connect(self.click_pb_addFriends)
        self.pb_copyRanks.clicked.connect(self.click_pb_copyRanks)
        self.pb_clear.clicked.connect(self.click_pb_clear)
        self.pb_showRanks.clicked.connect(self.click_pb_showRanks)
        self.pb_clearInput.clicked.connect(self.click_pb_clearInput)
        self.pb_pasteInput.clicked.connect(self.click_pb_pasteInput)
    
    """
    sets button icon and hover text
    """
    def initButtonIconAndHoverText(self):
        self.pb_clearInput.setIcon(QIcon(getButtonIconFilePath(CLEAR_FILENAME)))
        self.pb_clearInput.setIconSize(QSize(32, 32))
        self.pb_clearInput.setToolTip("Clear input")
        
        self.pb_pasteInput.setIcon(QIcon(getButtonIconFilePath(PASTE_FILENAME)))
        self.pb_pasteInput.setIconSize(QSize(32, 32))
        self.pb_pasteInput.setToolTip("Paste input")
        
        self.pb_showRanks.setIcon(QIcon(getButtonIconFilePath(SEARCH_FILENAME)))
        self.pb_showRanks.setIconSize(QSize(64, 64))
        self.pb_showRanks.setToolTip("Search ranks")
        
        self.pb_addFriends.setIcon(QIcon(getButtonIconFilePath(FRIEND_FILENAME)))
        self.pb_addFriends.setIconSize(QSize(64, 64))
        self.pb_addFriends.setToolTip("Add friends to blacklist")
        
        self.pb_clear.setIcon(QIcon(getButtonIconFilePath(CLEAR_FILENAME)))
        self.pb_clear.setIconSize(QSize(64, 64))
        self.pb_clear.setToolTip("Clear all")
        
        self.pb_copyRanks.setIcon(QIcon(getButtonIconFilePath(COPY_FILENAME)))
        self.pb_copyRanks.setIconSize(QSize(64, 64))
        self.pb_copyRanks.setToolTip("Copy ranks to clipboard")
    
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
    initializes settings from "settings.cfg" file and set global variables
    """
    def initSettingsUI(self):
        settings = readSettingsFile()
        self.excludeFriends = settings.excludeFriends
        self.autoFindRank = settings.autoFindRank
        self.autoCopyOutput = settings.autoCopyOutput
        
        self.cb_friends.setChecked(settings.excludeFriends)
        self.cb_autoStart.setChecked(settings.autoFindRank)
        self.cb_autoCopy.setChecked(settings.autoCopyOutput)
        writeSettingsFile(settings)
        
        self.cb_friends.stateChanged.connect(self.stateChanged)
        self.cb_autoStart.stateChanged.connect(self.stateChanged)
        self.cb_autoCopy.stateChanged.connect(self.stateChanged)
    
    """
    sets row in TableWidget based on player data
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
    clears "te_input" text
    """
    def click_pb_clearInput(self):
        self.te_input.setText("")
    
    """
    pastes clipboard data to "te_input"
    """
    def click_pb_pasteInput(self):
        currentInput = getClipboardData()
        self.te_input.setText(currentInput)
    
    """
    based on "te_input", appends friend id's to blacklist file
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
        self.progressBar.setValue(0)
        self.clearTableWidget()
    
    """
    based on "te_input", finds rank data for every player(except blacklist) and shows data in TableWidget
    """
    def click_pb_showRanks(self):
        currentInput = self.te_input.toPlainText()
        currentInput = currentInput.strip()
        
        if len(currentInput) == 0:
            return
        
        self.clearTableWidget()
        
        worker = Worker(self.processStatus, currentInput)
        worker.signals.result.connect(self.processStatusReturn)
        worker.signals.finished.connect(self.processStatusFinished)
        worker.signals.progress.connect(self.processStatusProgress)
        
        self.threadpool.start(worker)
    
    """
    based on changes on checkboxes, save new settings to "settings.cfg" file
    """
    def stateChanged(self):
        excludeFriends = self.cb_friends.isChecked()
        autoFindRank = self.cb_autoStart.isChecked()
        autoCopyOutput = self.cb_autoCopy.isChecked()
        
        settings = Settings(excludeFriends, autoFindRank, autoCopyOutput)
        writeSettingsFile(settings)
        
        self.excludeFriends = settings.excludeFriends
        self.autoFindRank = settings.autoFindRank
        self.autoCopyOutput = settings.autoCopyOutput
    
    """
    disable/enable all bottom 4 buttons based on state
    """
    def changeButtonState(self, state):
        self.pb_addFriends.setEnabled(state)
        self.pb_copyRanks.setEnabled(state)
        self.pb_clear.setEnabled(state)
        self.pb_showRanks.setEnabled(state)
    
    """
    clears TableWidget
    """
    def clearTableWidget(self):
        while self.tw_output.rowCount() > 0:
            self.tw_output.removeRow(0)
    
    # Multithreading Functions below
    def processStatus(self, status, progress_callback):
        self.changeButtonState(False)
        friends = []
        if self.excludeFriends:
            friends = readFriendsFile()
        Ids = extractSteam64Ids(status)
        
        print("excludeFriends = ", self.excludeFriends)
        print("Ids = ", Ids)
        print("friends = ", friends)
        
        return (Ids, friends)
    
    def processStatusReturn(self, data):
        Ids, friends = data
        
        # Pass the function to execute
        worker = Worker(self.processRanks, Ids, friends) # Any other args, kwargs are passed to the run function
        worker.signals.result.connect(self.processRanksReturn)
        worker.signals.finished.connect(self.processRanksFinished)
        worker.signals.progress.connect(self.processRanksProgress)
        
        self.threadpool.start(worker)
    
    def processStatusFinished(self):
        print("processStatusFinished")
    
    def processStatusProgress(self, data):
        progress, output = data
        print("%f%% done" % progress , output)
    
    # get ranks
    def processRanks(self, Ids, friends, progress_callback):
        players = []
        no = len(Ids)
        i = 0
        for id in Ids:
            player = getPlayerRank(id, friends)
            if player != None:
                players.append(player)
            i+=1
            progress_callback.emit((i*100/no, player))
        
        return players
    
    def processRanksReturn(self, data):
        print("processRanksReturn")
        if len(data) == 0:
            if self.initial == False:
                if self.excludeFriends:
                    self.le_status.setText(WRONG_INPUT_TEXT_F)
                else:
                    self.le_status.setText(WRONG_INPUT_TEXT)
            else:
                self.click_pb_clear()
        else:
            self.output = getPrettyTableString(data)
            self.le_status.setText(RANKS_FOUND)
            if self.autoCopyOutput:
                self.click_pb_copyRanks()
        
        self.initial = False
        self.changeButtonState(True)
    
    def processRanksFinished(self):
        print("processRanksFinished")
    
    def processRanksProgress(self, data):
        progress, output = data
        self.progressBar.setValue(int(progress))
        if output != None:
            i = self.tw_output.rowCount()
            self.tw_output.setRowCount(i+1)
            self.inflateRowWithPlayerData(i, output)
        
        print("%f%% done - {" % progress , output, "}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Ui()
    app.exec_()