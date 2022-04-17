from PyQt5.Qt import QRegExpValidator, QRegExp, QModelIndex
from PyQt5.QtCore import QSize, Qt, QDir
from PyQt5.QtWidgets import QDialogButtonBox, QCheckBox, QLineEdit, QLabel, \
    QGridLayout, QVBoxLayout, QComboBox, QDialog, QFileSystemModel, QTreeView, \
    QMessageBox, QHBoxLayout

import pathlib as PL
import Function.ChangeFunctions as CF
import Function.ConstantValues as CVs


class UiDialog:
    def __init__(self, MainWindow, TFIs = None, VFF = None, *args):
        self.QMW = MainWindow
        self.TFIs = TFIs
        self.VFF = VFF
        self.args = args
        self.QD = QDialog(self.QMW)
        #self.QD = QDialog()
        
        self.setDialog()
        self.setWidgets()
        self.rt = self.QD.exec()
    
    def setDialog(self): pass
    def setWidgets(self): pass
    def setValue(self): pass
    def closeDialog(self):
        self.QD.close()
    '''
    특정 값 입력시 에러창 출력과 텍스트 지우는 함수
    self.lineEdit_start.textChanged.connect(self.abc)
    def abc(self):
        qrex1=QRegExp(".*\d.*") #숫자 존재 확인
        qrex2=QRegExp(".*\D.*") #문자 존재 확인
        if qrex1.exactMatch(self.lineEdit_start.text()) and not qrex2.exactMatch(self.lineEdit_start.text()):
            print(True)
        else:
            print(False)
            self.lineEdit_start.clear()
    '''

class GetOpenFolder(UiDialog):
    def setDialog(self):
        size_dialog = QSize(500, 400)
        self.QD.setMinimumSize(size_dialog)
        #self.QD.setMaximumSize(size_dialog)
        self.QD.setWindowTitle(self.args[0])
        
    def setWidgets(self):
        size_fixedWidget = QSize(CVs.SIZE_WIDTH_DWIDGETS,CVs.SIZE_HEIGHT_DWIDGETS)
        layout_base = QVBoxLayout(self.QD)
        layout_firstFloorFst = QHBoxLayout()
        layout_firstFloorSnd = QHBoxLayout()

        self.label_view = QLabel(CVs.STR_SELECTFOLDER, self.QD)
        #self.label_view.setAlignment(Qt.AlignCenter)

        self.checkBox_isIncludSub = QCheckBox(CVs.STR_ISINCLUDESUB, self.QD)
        self.checkBox_isIncludSub.setMinimumSize(size_fixedWidget)
        self.checkBox_isIncludSub.setMaximumHeight(size_fixedWidget.height())
        self.checkBox_isIncludSub.setMaximumWidth(size_fixedWidget.width() + size_fixedWidget.height())
        self.checkBox_isIncludSub.setLayoutDirection(Qt.RightToLeft)
        self.checkBox_isIncludSub.clicked.connect(self.showWarningSubFolder)

        systemModel = QFileSystemModel()
        systemModel.setRootPath("")
        systemModel.setFilter(QDir.Dirs | QDir.NoDotAndDotDot)
        self.treeView_Folder = QTreeView(self.QD)
        self.treeView_Folder.setModel(systemModel)
        self.treeView_Folder.setColumnHidden(1, True)
        self.treeView_Folder.setColumnHidden(2, True)
        self.treeView_Folder.setColumnWidth(0, 300)
        self.treeView_Folder.setExpanded(systemModel.index('/'), True)
        self.treeView_Folder.clicked.connect(self.getSelectedPath)
        
        self.label_path = QLabel(CVs.STR_PATH, self.QD)
        self.label_path.setAlignment(Qt.AlignCenter)
        
        self.lineEdit_path = QLineEdit(self.QD)
        self.lineEdit_path.setMinimumSize(size_fixedWidget)
        self.lineEdit_path.setMaximumHeight(size_fixedWidget.height())


        self.buttonBox = QDialogButtonBox(self.QD)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
        self.buttonBox.setCenterButtons(True)
        self.buttonBox.rejected.connect(self.QD.reject)
        self.buttonBox.accepted.connect(self.QD.accept)
        
        layout_firstFloorFst.addWidget(self.label_view)
        layout_firstFloorFst.addWidget(self.checkBox_isIncludSub)
        
        layout_firstFloorSnd.addWidget(self.label_path)
        layout_firstFloorSnd.addWidget(self.lineEdit_path)
        
        layout_base.addLayout(layout_firstFloorFst)
        layout_base.addWidget(self.treeView_Folder)
        layout_base.addLayout(layout_firstFloorSnd)
        layout_base.addWidget(self.buttonBox)

    def setValue(self):
        if self.rt == QDialog.Accepted:
            result = ([self.lineEdit_path.text()], self.checkBox_isIncludSub.isChecked())
            return result
        else:
            return ""
    
    def getSelectedPath(self):
        parentsPaths = []
        selectedItem = QModelIndex.sibling(self.treeView_Folder.currentIndex(), self.treeView_Folder.currentIndex().row(),0)

        def getParentsPath(currentPath, parentsPaths):
            if currentPath.data() is None: #현재경로가 없으면 그냥 종료
                return parentsPaths
            else:
                getParentsPath(currentPath.parent(), parentsPaths) #부모경로 얻고
                parentsPaths.append(currentPath.data()) #자신경로 추가
                return parentsPaths

        getParentsPath(selectedItem, parentsPaths)
        if len(parentsPaths) > 0 :
            if 0 < parentsPaths[0].count(":"):
                parentsPath = PL.Path(parentsPaths[0] + '/')
            else:
                parentsPath = PL.Path(parentsPaths[0])
            if len(parentsPaths) > 1:
                for parent in parentsPaths[1:]:
                    parentsPath = parentsPath.joinpath(parent)
            self.lineEdit_path.setText(str(parentsPath))
        else:
            self.lineEdit_path.setText(str(selectedItem.data()))

    def showWarningSubFolder(self):
        if self.checkBox_isIncludSub.isChecked():
            DialogMessage(self.QD, CVs.MSG_WRN_WRNTITLE, CVs.MSG_WRN_SUBFOLDERS)


class DialogMessage:
    def __init__(self, MainWindow, title, message, wrnOrErr=False):
        self.QMW = MainWindow
        if wrnOrErr:
            QMessageBox.critical(self.QMW, title, message)
        else:
            QMessageBox.warning(self.QMW, title, message)


class DialogConfirmNewName(UiDialog):
    def setDialog(self):
        size_dialog = QSize(CVs.SIZE_WIDTH_DIALOG, CVs.SIZE_HEIGHT_DIALOG)
        self.QD.setMinimumSize(size_dialog)
        self.QD.setMaximumSize(size_dialog)
        self.QD.setWindowTitle(CVs.STR_DIALOGCNN)
        
    def setWidgets(self):
        layout_base = QVBoxLayout(self.QD)

        self.label_start = QLabel(CVs.MSG_ASK_CONFRIMCHANGE, self.QD)
        self.label_start.setAlignment(Qt.AlignCenter)

        self.buttonBox = QDialogButtonBox(self.QD)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
        self.buttonBox.setCenterButtons(True)
        self.buttonBox.rejected.connect(self.closeDialog)
        self.buttonBox.accepted.connect(self.setValue)
        
        layout_base.addWidget(self.label_start)
        layout_base.addWidget(self.buttonBox)

    def setValue(self):
        setResult = self.TFIs.confirmNewName()
        if setResult == True:
            pass
        else:
            errorMessage = setResult[0] + "\n\n" + str(setResult[1])
            DialogMessage(self.QMW, CVs.MSG_ERROR_ERRORTITLE, errorMessage, True)
        self.closeDialog()


class DialogUndoChanged(UiDialog):
    def setDialog(self):
        size_dialog = QSize(CVs.SIZE_WIDTH_DIALOG, CVs.SIZE_HEIGHT_DIALOG)
        self.QD.setMinimumSize(size_dialog)
        self.QD.setMaximumSize(size_dialog)
        self.QD.setWindowTitle(CVs.STR_DIALOGUC)
        
    def setWidgets(self):
        layout_base = QVBoxLayout(self.QD)

        self.label_start = QLabel(CVs.MSG_ASK_UNDOCHANGE, self.QD)
        self.label_start.setAlignment(Qt.AlignCenter)
        
        self.buttonBox = QDialogButtonBox(self.QD)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
        self.buttonBox.setCenterButtons(True)
        self.buttonBox.rejected.connect(self.closeDialog)
        self.buttonBox.accepted.connect(self.setValue)

        layout_base.addWidget(self.label_start)
        layout_base.addWidget(self.buttonBox)

    def setValue(self):
        self.TFIs.undoChanged()
        self.closeDialog()


class DialogRemoveBetweenChar(UiDialog):
    def setDialog(self):
        size_dialog = QSize(CVs.SIZE_WIDTH_DIALOG, CVs.SIZE_HEIGHT_DIALOG)
        self.QD.setMinimumSize(size_dialog)
        self.QD.setMaximumSize(size_dialog)
        self.QD.setWindowTitle(CVs.STR_DIALOGRBC)
        
    def setWidgets(self):
        size_fixedWidget = QSize(CVs.SIZE_WIDTH_DWIDGETS,CVs.SIZE_HEIGHT_DWIDGETS)
        layout_base = QVBoxLayout(self.QD)
        layout_firstFloor = QGridLayout()
        inputValidator = QRegExpValidator(QRegExp(CVs.SET_NOSPECIALCHAR))#일부 특수문자 제외

        self.label_start = QLabel(CVs.STR_FIRSTSTR, self.QD)
        self.label_start.setMinimumSize(size_fixedWidget)
        self.label_start.setMaximumSize(size_fixedWidget)
        self.label_start.setAlignment(Qt.AlignCenter)
        
        self.lineEdit_start = QLineEdit(self.QD)
        self.lineEdit_start.setMinimumSize(size_fixedWidget)
        self.lineEdit_start.setMaximumHeight(size_fixedWidget.height())
        self.lineEdit_start.setValidator(inputValidator)
        self.lineEdit_start.setPlaceholderText(CVs.STR_HINT_CASESENSITIVE)
        self.lineEdit_start.setToolTip(CVs.MSG_WRN_NOSPECIALCHAR)
        
        self.comboBox_overOrMore = QComboBox(self.QD)
        self.comboBox_overOrMore.addItem(CVs.STR_ISORMORECHAR,0)
        self.comboBox_overOrMore.addItem(CVs.STR_ISOVERCHAR,1)
        
        
        self.label_end = QLabel(CVs.STR_SECONDSTR, self.QD)
        self.label_end.setMinimumSize(size_fixedWidget)
        self.label_end.setMaximumSize(size_fixedWidget)
        self.label_end.setAlignment(Qt.AlignCenter)
        
        self.lineEdit_end = QLineEdit(self.QD)
        self.lineEdit_end.setMinimumSize(size_fixedWidget)
        self.lineEdit_end.setMaximumHeight(size_fixedWidget.height())
        self.lineEdit_end.setValidator(inputValidator)
        self.lineEdit_end.setPlaceholderText(CVs.STR_HINT_CASESENSITIVE)
        self.lineEdit_end.setToolTip(CVs.MSG_WRN_NOSPECIALCHAR)
        
        self.comboBox_underOrLess = QComboBox(self.QD)
        self.comboBox_underOrLess.addItem(CVs.STR_ISORLESSCHAR,0)
        self.comboBox_underOrLess.addItem(CVs.STR_ISUNDERCHAR,1)
        
        self.checkBox_isSpace = QCheckBox(CVs.STR_ISSPACE, self.QD)
        self.checkBox_isSpace.setMinimumSize(size_fixedWidget)
        self.checkBox_isSpace.setMaximumSize(size_fixedWidget)
        
        
        self.buttonBox = QDialogButtonBox(self.QD)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
        self.buttonBox.setCenterButtons(True)
        self.buttonBox.rejected.connect(self.closeDialog)
        self.buttonBox.accepted.connect(self.setValue)
        
        
        layout_firstFloor.addWidget(self.label_start, 0, 0, 1, 1)
        layout_firstFloor.addWidget(self.lineEdit_start, 0, 1, 1, 1)
        layout_firstFloor.addWidget(self.comboBox_overOrMore, 0, 2, 1, 1)
        
        layout_firstFloor.addWidget(self.label_end, 1, 0, 1, 1)
        layout_firstFloor.addWidget(self.lineEdit_end, 1, 1, 1, 1)
        layout_firstFloor.addWidget(self.comboBox_underOrLess, 1, 2, 1, 1)
        layout_firstFloor.addWidget(self.checkBox_isSpace, 1, 3, 1, 1)

        layout_base.addLayout(layout_firstFloor)
        layout_base.addWidget(self.buttonBox)

    def setValue(self):
        getValues = []
        getValues.append(self.lineEdit_start.text())
        getValues.append(self.lineEdit_end.text())
        getValues.append(self.checkBox_isSpace.isChecked())
        getValues.append(self.comboBox_overOrMore.currentData())
        getValues.append(self.comboBox_underOrLess.currentData())
        setResult = self.VFF.setValuesRBC(getValues)
        if setResult == True:
            CF.removeBetweenChar(self.TFIs, self.VFF)
            self.closeDialog()
        else:
            DialogMessage(self.QMW, CVs.MSG_ERROR_ERRORTITLE, setResult, False)


class DialogRemoveFollowOrder(UiDialog):
    def setDialog(self):
        size_dialog = QSize(CVs.SIZE_WIDTH_DIALOG, CVs.SIZE_HEIGHT_DIALOG)
        self.QD.setMinimumSize(size_dialog)
        self.QD.setMaximumSize(size_dialog)
        self.QD.setWindowTitle(CVs.STR_DIALOGRFO)
        
    def setWidgets(self):
        size_fixedWidget = QSize(CVs.SIZE_WIDTH_DWIDGETS,CVs.SIZE_HEIGHT_DWIDGETS)
        layout_base = QVBoxLayout(self.QD)
        layout_firstFloor = QGridLayout()
        inputValidator = QRegExpValidator(QRegExp(CVs.SET_ONLYINTCHAR)) #숫자만 입력

        self.label_start = QLabel(CVs.STR_FIRSTNUM, self.QD)
        self.label_start.setMinimumSize(size_fixedWidget)
        self.label_start.setMaximumSize(size_fixedWidget)
        self.label_start.setAlignment(Qt.AlignCenter)
        
        self.lineEdit_start = QLineEdit(self.QD)
        self.lineEdit_start.setMinimumSize(size_fixedWidget)
        self.lineEdit_start.setMaximumHeight(size_fixedWidget.height())
        self.lineEdit_start.setValidator(inputValidator)
        self.lineEdit_start.setPlaceholderText(CVs.STR_HINT_ONLYNUM)
        self.lineEdit_start.setToolTip(CVs.MSG_WRN_ONLYNUM)
        
        self.comboBox_overOrMore = QComboBox(self.QD)
        self.comboBox_overOrMore.addItem(CVs.STR_ISORMORENUM,0)
        self.comboBox_overOrMore.addItem(CVs.STR_ISOVERNUM,1)
        
        
        self.label_end = QLabel(CVs.STR_SECONDNUM, self.QD)
        self.label_end.setMinimumSize(size_fixedWidget)
        self.label_end.setMaximumSize(size_fixedWidget)
        self.label_end.setAlignment(Qt.AlignCenter)
        
        self.lineEdit_end = QLineEdit(self.QD)
        self.lineEdit_end.setMinimumSize(size_fixedWidget)
        self.lineEdit_end.setMaximumHeight(size_fixedWidget.height())
        self.lineEdit_end.setValidator(inputValidator)
        self.lineEdit_end.setPlaceholderText(CVs.STR_HINT_ONLYNUM)
        self.lineEdit_end.setToolTip(CVs.MSG_WRN_ONLYNUM)
        
        self.comboBox_underOrLess = QComboBox(self.QD)
        self.comboBox_underOrLess.addItem(CVs.STR_ISORLESSNUM,0)
        self.comboBox_underOrLess.addItem(CVs.STR_ISUNDERNUM,1)
        
        self.checkBox_isSpace = QCheckBox(CVs.STR_ISSPACE, self.QD)
        self.checkBox_isSpace.setMinimumSize(size_fixedWidget)
        self.checkBox_isSpace.setMaximumSize(size_fixedWidget)
        
        
        self.buttonBox = QDialogButtonBox(self.QD)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
        self.buttonBox.setCenterButtons(True)
        self.buttonBox.rejected.connect(self.closeDialog)
        self.buttonBox.accepted.connect(self.setValue)
        
        
        layout_firstFloor.addWidget(self.label_start, 0, 0, 1, 1)
        layout_firstFloor.addWidget(self.lineEdit_start, 0, 1, 1, 1)
        layout_firstFloor.addWidget(self.comboBox_overOrMore, 0, 2, 1, 1)
        
        layout_firstFloor.addWidget(self.label_end, 1, 0, 1, 1)
        layout_firstFloor.addWidget(self.lineEdit_end, 1, 1, 1, 1)
        layout_firstFloor.addWidget(self.comboBox_underOrLess, 1, 2, 1, 1)
        layout_firstFloor.addWidget(self.checkBox_isSpace, 1, 3, 1, 1)

        layout_base.addLayout(layout_firstFloor)
        layout_base.addWidget(self.buttonBox)

    def setValue(self):
        getValues = []
        getValues.append(self.lineEdit_start.text())
        getValues.append(self.lineEdit_end.text())
        getValues.append(self.checkBox_isSpace.isChecked())
        getValues.append(self.comboBox_overOrMore.currentData())
        getValues.append(self.comboBox_underOrLess.currentData())
        setResult = self.VFF.setValuesRFO(getValues)
        if setResult == True:
            CF.removeFollowOrder(self.TFIs, self.VFF)
            self.closeDialog()
        else:
            DialogMessage(self.QMW, CVs.MSG_ERROR_ERRORTITLE, setResult, False)


class DialogAddNumber(UiDialog):
    def setDialog(self):
        size_dialog = QSize(CVs.SIZE_WIDTH_DIALOG, CVs.SIZE_HEIGHT_DIALOG)
        self.QD.setMinimumSize(size_dialog)
        self.QD.setMaximumSize(size_dialog)
        self.QD.setWindowTitle(CVs.STR_DIALOGAN)
        
    def setWidgets(self):
        size_fixedWidget = QSize(CVs.SIZE_WIDTH_DWIDGETS,CVs.SIZE_HEIGHT_DWIDGETS)
        layout_base = QVBoxLayout(self.QD)
        layout_firstFloor = QGridLayout()
        inputValidator = QRegExpValidator(QRegExp(CVs.SET_ONLYINTCHAR)) #숫자만 입력

        self.label_start = QLabel(CVs.STR_FIRSTNUM, self.QD)
        self.label_start.setMinimumSize(size_fixedWidget)
        self.label_start.setMaximumSize(size_fixedWidget)
        self.label_start.setAlignment(Qt.AlignCenter)
        
        self.lineEdit_start = QLineEdit(self.QD)
        self.lineEdit_start.setMinimumSize(size_fixedWidget)
        self.lineEdit_start.setMaximumHeight(size_fixedWidget.height())
        self.lineEdit_start.setValidator(inputValidator)
        self.lineEdit_start.setPlaceholderText(CVs.STR_HINT_ONLYNUM)
        self.lineEdit_start.setToolTip(CVs.MSG_WRN_ONLYNUM)
        
        self.checkBox_isFront = QCheckBox(CVs.STR_ISFRONT,self.QD)
        self.checkBox_isFront.setMinimumSize(size_fixedWidget)
        self.checkBox_isFront.setMaximumSize(size_fixedWidget)
        
        
        self.label_end = QLabel(CVs.STR_DIGITNUM, self.QD)
        self.label_end.setMinimumSize(size_fixedWidget)
        self.label_end.setMaximumSize(size_fixedWidget)
        self.label_end.setAlignment(Qt.AlignCenter)
        
        self.lineEdit_end = QLineEdit(self.QD)
        self.lineEdit_end.setMinimumSize(size_fixedWidget)
        self.lineEdit_end.setMaximumHeight(size_fixedWidget.height())
        self.lineEdit_end.setValidator(inputValidator)
        self.lineEdit_end.setPlaceholderText(CVs.STR_HINT_ONLYNUM)
        self.lineEdit_end.setToolTip(CVs.MSG_WRN_ONLYNUM)
        
        self.checkBox_isSpace = QCheckBox(CVs.STR_ISSPACE, self.QD)
        self.checkBox_isSpace.setMinimumSize(size_fixedWidget)
        self.checkBox_isSpace.setMaximumSize(size_fixedWidget)
        
        
        self.buttonBox = QDialogButtonBox(self.QD)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
        self.buttonBox.setCenterButtons(True)
        self.buttonBox.rejected.connect(self.closeDialog)
        self.buttonBox.accepted.connect(self.setValue)
        
        
        layout_firstFloor.addWidget(self.label_start, 0, 0, 1, 1)
        layout_firstFloor.addWidget(self.lineEdit_start, 0, 1, 1, 2)
        layout_firstFloor.addWidget(self.checkBox_isFront, 0, 3, 1, 1)
        
        layout_firstFloor.addWidget(self.label_end, 1, 0, 1, 1)
        layout_firstFloor.addWidget(self.lineEdit_end, 1, 1, 1, 2)
        layout_firstFloor.addWidget(self.checkBox_isSpace, 1, 3, 1, 1)

        layout_base.addLayout(layout_firstFloor)
        layout_base.addWidget(self.buttonBox)

    def setValue(self):
        getValues = []
        getValues.append(self.lineEdit_start.text())
        getValues.append(self.lineEdit_end.text())
        getValues.append(self.checkBox_isSpace.isChecked())
        getValues.append(self.checkBox_isFront.isChecked())
        setResult = self.VFF.setValuesAN(getValues)
        if setResult == True:
            CF.addNumber(self.TFIs, self.VFF)
            self.closeDialog()
        else:
            DialogMessage(self.QMW, CVs.MSG_ERROR_ERRORTITLE, setResult, False)


class DialogAddString(UiDialog):
    def setDialog(self):
        size_dialog = QSize(CVs.SIZE_WIDTH_DIALOG, CVs.SIZE_HEIGHT_DIALOG)
        self.QD.setMinimumSize(size_dialog)
        self.QD.setMaximumSize(size_dialog)
        self.QD.setWindowTitle(CVs.STR_DIALOGAS)
        
    def setWidgets(self):
        size_fixedWidget = QSize(CVs.SIZE_WIDTH_DWIDGETS,CVs.SIZE_HEIGHT_DWIDGETS)
        layout_base = QVBoxLayout(self.QD)
        layout_firstFloor = QGridLayout()
        inputValidator = QRegExpValidator(QRegExp(CVs.SET_NOSPECIALCHAR))

        self.label_start = QLabel(CVs.STR_TOADDSTR, self.QD)
        self.label_start.setMinimumSize(size_fixedWidget)
        self.label_start.setMaximumSize(size_fixedWidget)
        self.label_start.setAlignment(Qt.AlignCenter)
        
        self.lineEdit_start = QLineEdit(self.QD)
        self.lineEdit_start.setMinimumSize(size_fixedWidget)
        self.lineEdit_start.setMaximumHeight(size_fixedWidget.height())
        self.lineEdit_start.setValidator(inputValidator)
        self.lineEdit_start.setPlaceholderText(CVs.STR_HINT_INPUT)
        self.lineEdit_start.setToolTip(CVs.MSG_WRN_NOSPECIALCHAR)
        
        self.checkBox_isFront = QCheckBox(CVs.STR_ISFRONT,self.QD)
        self.checkBox_isFront.setMinimumSize(size_fixedWidget)
        self.checkBox_isFront.setMaximumSize(size_fixedWidget)
        
        self.checkBox_isSpace = QCheckBox(CVs.STR_ISSPACE, self.QD)
        self.checkBox_isSpace.setMinimumSize(size_fixedWidget)
        self.checkBox_isSpace.setMaximumSize(size_fixedWidget)
        
        
        self.buttonBox = QDialogButtonBox(self.QD)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
        self.buttonBox.setCenterButtons(True)
        self.buttonBox.rejected.connect(self.closeDialog)
        self.buttonBox.accepted.connect(self.setValue)
        
        
        layout_firstFloor.addWidget(self.label_start, 0, 0, 1, 1)
        layout_firstFloor.addWidget(self.lineEdit_start, 0, 1, 1, 2)
        layout_firstFloor.addWidget(self.checkBox_isFront, 0, 3, 1, 1)
        layout_firstFloor.addWidget(self.checkBox_isSpace, 1, 3, 1, 1)

        layout_base.addLayout(layout_firstFloor)
        layout_base.addWidget(self.buttonBox)

    def setValue(self):
        getValues = []
        getValues.append(self.lineEdit_start.text())
        getValues.append(self.checkBox_isSpace.isChecked())
        getValues.append(self.checkBox_isFront.isChecked())
        setResult = self.VFF.setValuesAS(getValues)
        if setResult == True:
            CF.addString(self.TFIs, self.VFF)
            self.closeDialog()
        else:
            DialogMessage(self.QMW, CVs.MSG_ERROR_ERRORTITLE, setResult, False)


class DialogReplaceString(UiDialog):
    def setDialog(self):
        size_dialog = QSize(CVs.SIZE_WIDTH_DIALOG, CVs.SIZE_HEIGHT_DIALOG)
        self.QD.setMinimumSize(size_dialog)
        self.QD.setMaximumSize(size_dialog)
        self.QD.setWindowTitle(CVs.STR_DIALOGRS)
        
    def setWidgets(self):
        size_fixedWidget = QSize(CVs.SIZE_WIDTH_DWIDGETS,CVs.SIZE_HEIGHT_DWIDGETS)
        layout_base = QVBoxLayout(self.QD)
        layout_firstFloor = QGridLayout()
        inputValidator = QRegExpValidator(QRegExp(CVs.SET_NOSPECIALCHAR))

        self.label_start = QLabel(CVs.STR_TOFINDSTR, self.QD)
        self.label_start.setMinimumSize(size_fixedWidget)
        self.label_start.setMaximumSize(size_fixedWidget)
        self.label_start.setAlignment(Qt.AlignCenter)
        
        self.lineEdit_start = QLineEdit(self.QD)
        self.lineEdit_start.setMinimumSize(size_fixedWidget)
        self.lineEdit_start.setMaximumHeight(size_fixedWidget.height())
        self.lineEdit_start.setValidator(inputValidator)
        self.lineEdit_start.setPlaceholderText(CVs.STR_HINT_CASESENSITIVE)
        self.lineEdit_start.setToolTip(CVs.MSG_WRN_NOSPECIALCHAR)


        self.label_end = QLabel(CVs.STR_TOCHANGESTR, self.QD)
        self.label_end.setMinimumSize(size_fixedWidget)
        self.label_end.setMaximumSize(size_fixedWidget)
        self.label_end.setAlignment(Qt.AlignCenter)
        
        self.lineEdit_end = QLineEdit(self.QD)
        self.lineEdit_end.setMinimumSize(size_fixedWidget)
        self.lineEdit_end.setMaximumHeight(size_fixedWidget.height())
        self.lineEdit_end.setValidator(inputValidator)
        self.lineEdit_end.setPlaceholderText(CVs.STR_HINT_CASESENSITIVE)
        self.lineEdit_end.setToolTip(CVs.MSG_WRN_NOSPECIALCHAR)
        
        
        self.buttonBox = QDialogButtonBox(self.QD)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
        self.buttonBox.setCenterButtons(True)
        self.buttonBox.rejected.connect(self.closeDialog)
        self.buttonBox.accepted.connect(self.setValue)
        
        
        layout_firstFloor.addWidget(self.label_start, 0, 0, 1, 1)
        layout_firstFloor.addWidget(self.lineEdit_start, 0, 1, 1, 2)
        
        layout_firstFloor.addWidget(self.label_end, 1, 0, 1, 1)
        layout_firstFloor.addWidget(self.lineEdit_end, 1, 1, 1, 2)

        layout_base.addLayout(layout_firstFloor)
        layout_base.addWidget(self.buttonBox)

    def setValue(self):
        getValues = []
        getValues.append(self.lineEdit_start.text())
        getValues.append(self.lineEdit_end.text())
        setResult = self.VFF.setValuesRS(getValues)
        if setResult == True:
            CF.replaceString(self.TFIs, self.VFF)
            self.closeDialog()
        else:
            DialogMessage(self.QMW, CVs.MSG_ERROR_ERRORTITLE, setResult, False)
            

class DialogRemoveAllName(UiDialog):
    def setDialog(self):
        size_dialog = QSize(CVs.SIZE_WIDTH_DIALOG, CVs.SIZE_HEIGHT_DIALOG)
        self.QD.setMinimumSize(size_dialog)
        self.QD.setMaximumSize(size_dialog)
        self.QD.setWindowTitle(CVs.STR_DIALOGRAN)
        
    def setWidgets(self):
        layout_base = QVBoxLayout(self.QD)

        self.label_start = QLabel(CVs.MSG_ASK_REMOVEALLNAME, self.QD)
        self.label_start.setAlignment(Qt.AlignCenter)
        
        self.buttonBox = QDialogButtonBox(self.QD)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
        self.buttonBox.setCenterButtons(True)
        self.buttonBox.rejected.connect(self.closeDialog)
        self.buttonBox.accepted.connect(self.setValue)

        layout_base.addWidget(self.label_start)
        layout_base.addWidget(self.buttonBox)

    def setValue(self):
        CF.removeAllName(self.TFIs)
        self.closeDialog()


class DialogSetNewName(UiDialog):
    def __init__(self, MainWindow, TFIs, VFF, selectedIndex):
        self.selectedIndex = selectedIndex
        super().__init__(MainWindow, TFIs, VFF)

    def setDialog(self):
        size_dialog = QSize(CVs.SIZE_WIDTH_DIALOG, CVs.SIZE_HEIGHT_DIALOG)
        self.QD.setMinimumSize(size_dialog)
        self.QD.setMaximumSize(size_dialog)
        self.QD.setWindowTitle(CVs.STR_DIALOGSNN)
        
    def setWidgets(self):
        size_fixedWidget = QSize(CVs.SIZE_WIDTH_DWIDGETS,CVs.SIZE_HEIGHT_DWIDGETS)
        layout_base = QVBoxLayout(self.QD)
        layout_firstFloor = QGridLayout()
        inputValidator = QRegExpValidator(QRegExp(CVs.SET_NOSPECIALCHAR))

        self.label_start = QLabel(CVs.STR_SNN, self.QD)
        self.label_start.setMinimumSize(size_fixedWidget)
        self.label_start.setMaximumSize(size_fixedWidget)
        self.label_start.setAlignment(Qt.AlignCenter)
        
        self.lineEdit_start = QLineEdit(self.QD)
        self.lineEdit_start.setMinimumSize(size_fixedWidget)
        self.lineEdit_start.setMaximumHeight(size_fixedWidget.height())
        self.lineEdit_start.setValidator(inputValidator)
        self.lineEdit_start.setPlaceholderText(CVs.STR_HINT_INPUT)
        self.lineEdit_start.setToolTip(CVs.MSG_WRN_NOSPECIALCHAR)
        self.lineEdit_start.setText(self.TFIs.fileInfos[self.selectedIndex].newName)
        
        
        self.buttonBox = QDialogButtonBox(self.QD)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
        self.buttonBox.setCenterButtons(True)
        self.buttonBox.rejected.connect(self.closeDialog)
        self.buttonBox.accepted.connect(self.setValue)
        
        
        layout_firstFloor.addWidget(self.label_start, 0, 0, 1, 1)
        layout_firstFloor.addWidget(self.lineEdit_start, 0, 1, 1, 3)

        layout_base.addLayout(layout_firstFloor)
        layout_base.addWidget(self.buttonBox)

    def setValue(self):
        getValues = []
        getValues.append(str(self.selectedIndex))
        getValues.append(self.lineEdit_start.text())
        setResult = self.VFF.setValuesSNN(getValues)
        if setResult == True:
            CF.setNewName(self.TFIs, self.VFF)
            self.closeDialog()
        else:
            DialogMessage(self.QMW, CVs.MSG_ERROR_ERRORTITLE, setResult, False)


