from PyQt5.QtWidgets import QTableWidgetItem, QFileDialog,\
    QMenuBar, QMenu, QAction, QTableWidget, QPushButton, QFrame, QVBoxLayout,\
    QHBoxLayout, QWidget, QDesktopWidget, QMainWindow, QAbstractItemView
from PyQt5.QtCore import QSize, QEvent
import Function.ConstantValues as CVs
import Function.TreatPathName as TPN
import Gui.DialogFrame as Dialog
import time

class UiMainWindow:
    def __init__(self):
        self.QMW = QMainWindow()
        self.TFIs = TPN.TreatFileInfos()
        self.VFF = TPN.ValueForFunction()
        #self.QMW.setFixedSize(mainFrameSize)
        self.setMainWindow()
        self.setWidgets()
        self.QMW.eventFilter = self.eventFilter #파일을 드래그&드롭으로 읽기 위한 필터
        
        self.QMW.show()

    #메인 윈도우의 크기, 위치 설정 메소드
    def setMainWindow(self):
        size_screen = QDesktopWidget().screenGeometry().size()
        size_mainFrame = QSize(CVs.SIZE_WIDTH_MAINFRAME, CVs.SIZE_HEIGHT_MAINFRAME)
        self.QMW.setMinimumSize(size_mainFrame)
        self.QMW.move(int((size_screen.width()-size_mainFrame.width())/2), int((size_screen.height()-size_mainFrame.height())/2))
        self.QMW.setWindowTitle(CVs.STR_MAINWINDOW)

    #메인윈도우 내 위젯 설정 메소드
    def setWidgets(self):
        size_fixedWidget = QSize(CVs.SIZE_WIDTH_MFWIDGETS, CVs.SIZE_HEIGHT_MFWIDGETS)
        
        self.widget_central = QWidget(self.QMW)
        self.layout_base = QHBoxLayout(self.widget_central)
        self.layout_firstFloor = QVBoxLayout()

        self.button_confirmNewName = QPushButton(CVs.STR_CONFIRMNEWNAME, self.widget_central)
        self.button_confirmNewName.setMinimumSize(size_fixedWidget)
        self.button_confirmNewName.setMaximumSize(size_fixedWidget)
        self.button_confirmNewName.clicked.connect(self.callDialogCNN)

        self.button_undoChange = QPushButton(CVs.STR_UNDOCHANGED, self.widget_central)
        self.button_undoChange.setMinimumSize(size_fixedWidget)
        self.button_undoChange.setMaximumSize(size_fixedWidget)
        self.button_undoChange.clicked.connect(self.callDialogUC)
        
        self.line_horizontal = QFrame(self.QMW)
        self.line_horizontal.setFrameShape(QFrame.HLine)
        self.line_horizontal.setFrameShadow(QFrame.Raised)
        
        self.button_up = QPushButton(CVs.STR_UP, self.widget_central)
        self.button_up.setMinimumSize(size_fixedWidget.width(), int(size_fixedWidget.height()/3*2))
        self.button_up.setMaximumSize(size_fixedWidget.width(), int(size_fixedWidget.height()/3*2))
        self.button_up.clicked.connect(self.upFileInfo)
        
        self.button_down = QPushButton(CVs.STR_DOWN, self.widget_central)
        self.button_down.setMinimumSize(size_fixedWidget.width(), int(size_fixedWidget.height()/3*2))
        self.button_down.setMaximumSize(size_fixedWidget.width(), int(size_fixedWidget.height()/3*2))
        self.button_down.clicked.connect(self.downFileInfo)
        
        self.line_horizontal2 = QFrame(self.QMW)
        self.line_horizontal2.setFrameShape(QFrame.HLine)
        self.line_horizontal2.setFrameShadow(QFrame.Raised)

        self.button_RBC = QPushButton(CVs.STR_RBC, self.widget_central)
        self.button_RBC.setMinimumSize(size_fixedWidget)
        self.button_RBC.setMaximumSize(size_fixedWidget)
        self.button_RBC.clicked.connect(self.callDialogRBC)
        
        self.button_RBC.setEnabled(False)
        self.button_RFO = QPushButton(CVs.STR_RFO, self.widget_central)
        self.button_RFO.setMinimumSize(size_fixedWidget)
        self.button_RFO.setMaximumSize(size_fixedWidget)
        self.button_RFO.clicked.connect(self.callDialogRFO)

        self.button_AN = QPushButton(CVs.STR_AN, self.widget_central)
        self.button_AN.setMinimumSize(size_fixedWidget)
        self.button_AN.setMaximumSize(size_fixedWidget)
        self.button_AN.clicked.connect(self.callDialogAN)

        self.button_AS = QPushButton(CVs.STR_AS, self.widget_central)
        self.button_AS.setMinimumSize(size_fixedWidget)
        self.button_AS.setMaximumSize(size_fixedWidget)
        self.button_AS.clicked.connect(self.callDialogAS)

        self.button_RS = QPushButton(CVs.STR_RS, self.widget_central)
        self.button_RS.setMinimumSize(size_fixedWidget)
        self.button_RS.setMaximumSize(size_fixedWidget)
        self.button_RS.clicked.connect(self.callDialogRS)
        
        self.button_RAN = QPushButton(CVs.STR_RAN, self.widget_central)
        self.button_RAN.setMinimumSize(size_fixedWidget)
        self.button_RAN.setMaximumSize(size_fixedWidget)
        self.button_RAN.clicked.connect(self.callDialogRAN)
        
        self.button_SNN = QPushButton(CVs.STR_SNN, self.widget_central)
        self.button_SNN.setMinimumSize(size_fixedWidget)
        self.button_SNN.setMaximumSize(size_fixedWidget)
        self.button_SNN.clicked.connect(self.callDialogSNN)

        self.columnNames = [CVs.STR_OLDNAME, CVs.STR_NEWNAME, CVs.STR_PATH, CVs.STR_MODIFIEDDATE, CVs.STR_SIZE]
        self.widget_table = QTableWidget(self.widget_central)
        mimeTypes = ["text/uri-list"]
        mimeTypes.extend(self.widget_table.mimeTypes())
        self.widget_table.mimeTypes = lambda: mimeTypes
        
        self.widget_table.setCornerButtonEnabled(True)
        self.widget_table.setAcceptDrops(True)
        self.widget_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        
        self.widget_table.setColumnCount(len(self.columnNames))
        self.widget_table.setHorizontalHeaderLabels(self.columnNames)
        
        self.widget_table.resizeColumnsToContents()
        self.widget_table.horizontalHeader().setSectionsMovable(True)
        self.widget_table.horizontalHeader().setCascadingSectionResizes(False)
        self.widget_table.viewport().installEventFilter(self.QMW)
        self.widget_table.cellDoubleClicked.connect(self.callDialogSNN)
        #self.widget_table.setSortingEnabled(True) #정렬 후 파일 입력하면 오류
        self.widget_table.horizontalHeader().sectionClicked.connect(self.test)


        self.action_openFiles = QAction(CVs.STR_ACTIONOPENFILES, self.QMW)
        self.action_openFiles.triggered.connect(self.openFiles)
        
        self.action_addFiles = QAction(CVs.STR_ACTIONADDFILES, self.QMW)
        self.action_addFiles.triggered.connect(self.addFiles)

        self.action_openFolder = QAction(CVs.STR_ACTIONOPENFOLDER, self.QMW)
        self.action_openFolder.triggered.connect(self.openFolder)

        self.action_addFolder = QAction(CVs.STR_ACTIONADDFOLDER, self.QMW)
        self.action_addFolder.triggered.connect(self.addFolder)
        
        self.action_cleanFile = QAction(CVs.STR_ACTIONCLEANFILE, self.QMW)
        self.action_cleanFile.triggered.connect(self.cleanFileInfos)
        

        self.action_quit = QAction(CVs.STR_ACTIONQUIT, self.QMW)
        self.action_quit.triggered.connect(self.closeMainWindow)

        self.menu_file = QMenu(CVs.STR_FILE, self.QMW)
        self.menu_file.addAction(self.action_openFiles)
        self.menu_file.addAction(self.action_addFiles)
        self.menu_file.addSeparator()
        self.menu_file.addAction(self.action_openFolder)
        self.menu_file.addAction(self.action_addFolder)
        self.menu_file.addSeparator()
        self.menu_file.addAction(self.action_cleanFile)
        self.menu_file.addSeparator()
        self.menu_file.addAction(self.action_quit)

        self.menuBar = QMenuBar(self.QMW)
        self.menuBar.addAction(self.menu_file.menuAction())
        
        #self.statusbar = QStatusBar(self.QMW)

        self.layout_firstFloor.addWidget(self.button_confirmNewName)
        self.layout_firstFloor.addWidget(self.button_undoChange)
        self.layout_firstFloor.addWidget(self.line_horizontal)
        self.layout_firstFloor.addWidget(self.button_up)
        self.layout_firstFloor.addWidget(self.button_down)
        self.layout_firstFloor.addWidget(self.line_horizontal2)
        self.layout_firstFloor.addWidget(self.button_RBC)
        self.layout_firstFloor.addWidget(self.button_RFO)
        self.layout_firstFloor.addWidget(self.button_AN)
        self.layout_firstFloor.addWidget(self.button_AS)
        self.layout_firstFloor.addWidget(self.button_RS)
        self.layout_firstFloor.addWidget(self.button_RAN)
        self.layout_firstFloor.addWidget(self.button_SNN)
        
        self.layout_base.addLayout(self.layout_firstFloor)
        self.layout_base.addWidget(self.widget_table)
        
        self.QMW.setCentralWidget(self.widget_central)
        self.QMW.setMenuBar(self.menuBar)
        #self.QMW.setStatusBar(self.statusbar)
        
        self.setButtonsEnabled(False)



    def test(self):
        if self.widget_table.rowCount() == 0:
            pass
        else:
            b= self.widget_table.currentColumn()
            a=self.widget_table.horizontalHeaderItem(b).text()
            print(b, a, "teset")
        
        '''if r.rt==QDialog.Accepted:
            r=r.setValue()
            if len(r) > 0:
                self.setInfosFromFiles([r])
        elif r.rt==QDialog.Rejected:
            pass'''
        pass
        


    def closeMainWindow(self):
        self.QMW.close()

    #드래그&드랍으로 파일을 읽기위한 eventFilter, 원본 eventFilter에 override
    def eventFilter(self, source, event): 
        resultOpen = []
        if (event.type() == QEvent.Drop):
            for url in event.mimeData().urls():
                resultOpen.append(url.toLocalFile())
            self.setInfosFromFiles(resultOpen)
            return True
        return QMainWindow().eventFilter(source, event)

    #버튼들을 활성/비활성화 하는 메소드, 매개변수 : bool
    def setButtonsEnabled(self,trueOrFalse):
        self.button_confirmNewName.setEnabled(trueOrFalse)
        self.button_undoChange.setEnabled(trueOrFalse)
        self.button_up.setEnabled(trueOrFalse)
        self.button_down.setEnabled(trueOrFalse)
        self.button_RBC.setEnabled(trueOrFalse)
        self.button_RFO.setEnabled(trueOrFalse)
        self.button_AN.setEnabled(trueOrFalse)
        self.button_AS.setEnabled(trueOrFalse)
        self.button_RS.setEnabled(trueOrFalse)
        self.button_RAN.setEnabled(trueOrFalse)
        self.button_SNN.setEnabled(trueOrFalse)

    #테이블에 파일 정보를 출력하는 메소드, 매개변수 : class 'TreatFileInfos'
    def setTable(self, TFIs):
        self.widget_table.clear()
        self.widget_table.setColumnCount(len(self.columnNames))
        self.widget_table.setHorizontalHeaderLabels(self.columnNames)
        self.widget_table.setRowCount(len(TFIs.infosIndex))
        for rowIndex, infoIndex in enumerate(TFIs.infosIndex):
            #item_firstColumn = QTableWidgetItem(TFIs.fileInfos[infoIndex].oldName + TFIs.fileInfos[infoIndex].suffix) # 셀 수정 방지, setFlags(ItemIsEnabled)는 수정안됨 + 셀 다중 선택 안됨
            #item_firstColumn.setFlags(item_firstColumn.flags() ^ Qt.ItemIsEditable) 출처 : https://stackoverflow.com/questions/2574115/how-to-make-a-column-in-qtablewidget-read-only
            self.widget_table.setItem(rowIndex, 0, QTableWidgetItem(TFIs.fileInfos[infoIndex].oldName + TFIs.fileInfos[infoIndex].suffix))
            self.widget_table.setItem(rowIndex, 1, QTableWidgetItem(TFIs.fileInfos[infoIndex].newName + TFIs.fileInfos[infoIndex].suffix))
            self.widget_table.setItem(rowIndex, 2, QTableWidgetItem(str(TFIs.fileInfos[infoIndex].path)))
            self.widget_table.setItem(rowIndex, 3, QTableWidgetItem(TFIs.fileInfos[infoIndex].modifiedDate))
            self.widget_table.setItem(rowIndex, 4, QTableWidgetItem(TFIs.fileInfos[infoIndex].size))
        self.widget_table.resizeColumnsToContents()
        self.widget_table.resizeRowsToContents()

    #파일/폴더 경로를 받아서 세부정보를 얻는 메소드에 전달하는 메소드, 매개변수 : tuple/list/str:경로, bool:기존 파일정보 삭제여부
    def setInfosFromFiles(self, resultPaths, isClear = False):
        if len(resultPaths) > 0 :# pathlib은 공백이 들어가면 현재폴더로 인식하므로 제외
            if isClear:
                self.cleanFileInfos()
            addNum = len(self.TFIs.fileInfos)
            if type(resultPaths) != type(()):
                if type(resultPaths) != type([]):
                    resultPaths = ([resultPaths], False)
                elif type(resultPaths) == type([]):
                    resultPaths = (resultPaths, False)
            resultDiff = self.TFIs.differentiateFileFolder(resultPaths)
            if (resultDiff == 0) and (len(self.TFIs.fileInfos) - addNum) > 0:
                self.setTable(self.TFIs)
                self.setButtonsEnabled(True)
            elif (len(self.TFIs.fileInfos) - addNum) == 0: #폴더 내부에 파일이 없는 경우 에러 발생
                Dialog.DialogMessage(self.QMW, CVs.MSG_ERROR_ERRORTITLE, CVs.MSG_ERROR_NOFILEINPATH)
            else:
                Dialog.DialogMessage(self.QMW, CVs.MSG_ERROR_ERRORTITLE, resultDiff, True)

    #새로 파일을 여는 메소드, 기존 리스트 삭제
    def openFiles(self):
        resultDialog = QFileDialog.getOpenFileNames(None,CVs.STR_OPENFILES)[0]
        self.setInfosFromFiles(resultDialog, True)

    #기존 리스트에 파일을 추가하는 메소드
    def addFiles(self):
        #getOpenFileNames(resultDialog) a에 self.QMW 넣으면 Modal 없으면 Modaless
        #Modaless여도 main의 버튼이나 종료 버튼은 작동 안함
        resultDialog = QFileDialog.getOpenFileNames(None,CVs.STR_ADDFILES)[0]
        self.setInfosFromFiles(resultDialog)

    #새로 폴더 내 파일을 여는 메소드, 기존 리스트 삭제
    def openFolder(self):
        #resultDialog = QFileDialog.getExistingDirectory(None,CVs.STR_OPENFOLDER)
        resultDialog = Dialog.GetOpenFolder(None, None, None, CVs.STR_OPENFOLDER).setValue()
        self.setInfosFromFiles(resultDialog, True)

    #기존 리스트에 폴더 내 파일을 추가하는 메소드
    def addFolder(self):
        #resultDialog = QFileDialog.getExistingDirectory(None,CVs.STR_ADDFOLDER)
        resultDialog = Dialog.GetOpenFolder(None, None, None, CVs.STR_ADDFOLDER).setValue()
        self.setInfosFromFiles(resultDialog)

    #전체 초기화
    def cleanFileInfos(self):
        self.TFIs.removeInfos()
        self.VFF.init()
        self.setTable(self.TFIs)
        self.setButtonsEnabled(False)
    
    #테이블에서 선택한 아이템들의 행,열 구하기위한 메소드
    def getCurrentItems(self):
        currentRows = []
        currentColumns = []
        for itemIndex in self.widget_table.selectedItems():
            if currentRows.count(itemIndex.row()) == 0:
                    currentRows.append(itemIndex.row())
            if currentColumns.count(itemIndex.column()) == 0:
                    currentColumns.append(itemIndex.column())
        currentItmes = [sorted(currentRows), sorted(currentColumns)]
        return currentItmes

    #테이블에서 선택한 아이템을 위로 한칸 옮기는 메소드
    def upFileInfo(self):
        currentItems = self.getCurrentItems()
        if currentItems[0].count(0) > 0 or len(currentItems[0]) == 0:
            pass
        else:
            self.widget_table.clearSelection()
            for row in currentItems[0]:
                for column in currentItems[1]:
                        self.widget_table.item(row - 1,column).setSelected(True)
    
            if len(currentItems[0]) < len(self.TFIs.infosIndex):
                self.TFIs.moveFileInfo(True, currentItems[0])
                self.setTable(self.TFIs)

    #테이블에서 선택한 아이템을 아래로 한칸 옮기는 메소드
    def downFileInfo(self):
        currentItems = self.getCurrentItems()
        if currentItems[0].count(len(self.TFIs.infosIndex) - 1) > 0 or len(currentItems[0]) == 0:
            pass
        else:
            self.widget_table.clearSelection()
            for row in currentItems[0]:
                for column in currentItems[1]:
                        self.widget_table.item(row + 1,column).setSelected(True)
    
            if len(currentItems[0]) < len(self.TFIs.infosIndex):
                self.TFIs.moveFileInfo(False, currentItems[0])
                self.setTable(self.TFIs)

#버튼과 연관된 Dialog를 여는 메소드들
    def callDialogCNN(self):
        Dialog.DialogConfirmNewName(self.QMW, self.TFIs, self.VFF)
        self.setTable(self.TFIs)

    def callDialogUC(self):
        Dialog.DialogUndoChanged(self.QMW, self.TFIs, self.VFF)
        self.setTable(self.TFIs)

    def callDialogRBC(self):
        Dialog.DialogRemoveBetweenChar(self.QMW, self.TFIs, self.VFF)
        self.setTable(self.TFIs)

    def callDialogRFO(self):
        Dialog.DialogRemoveFollowOrder(self.QMW, self.TFIs, self.VFF)
        self.setTable(self.TFIs)
    
    def callDialogAN(self):
        Dialog.DialogAddNumber(self.QMW, self.TFIs, self.VFF)
        self.setTable(self.TFIs)

    def callDialogAS(self):
        Dialog.DialogAddString(self.QMW, self.TFIs, self.VFF)
        self.setTable(self.TFIs)

    def callDialogRS(self):
        Dialog.DialogReplaceString(self.QMW, self.TFIs, self.VFF)
        self.setTable(self.TFIs)

    def callDialogRAN(self):
        Dialog.DialogRemoveAllName(self.QMW, self.TFIs, self.VFF)
        self.setTable(self.TFIs)
    
    def callDialogSNN(self):
        if self.widget_table.currentRow() >-1:
            Dialog.DialogSetNewName(self.QMW, self.TFIs, self.VFF, self.widget_table.currentRow())
            self.setTable(self.TFIs)
