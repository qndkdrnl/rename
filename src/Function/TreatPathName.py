import pathlib as PL
import Function.ConstantValues as CVs
import time as TM
from PyQt5.QtCore import QDir

class TreatFileInfos:
    def __init__(self):
        self.infosIndex = []
        self.fileInfos = []
        #self.pathsIndex = []

    #파일 리스트를 받아서 세부 정보를 저장하는 메소드, 매개변수 : [파일 경로:str,pathlib.Path]:리스트
    def setFileInfos(self, tempList):
        addNum = len(self.infosIndex)
        removeIndex = self.isExistFile(tempList, False) 
        if len(removeIndex) > 0:
            self.deleteWrongList(tempList, removeIndex)
        if addNum != 0:
            removeIndex = self.isSameFile(tempList)
            if len(removeIndex) > 0:
                self.deleteWrongList(tempList, removeIndex)
        for index, tempInfo in enumerate(tempList):
            self.infosIndex.append(index + addNum)
            self.fileInfos.append(tempInfo)

    #폴더 리스트를 받아서 내부 파일 리스트를 넘기는 메소드, 매개변수 : list:[폴더 경로:str,pathlib.Path], bool:하위폴더 검색여부
    def setFileInfosFromFolder(self, tempList, loopForSubfolder):
        tempFilesList =[]
        tempFolderList = []
        removeIndex = self.isExistFile(tempList, False) 
        if len(removeIndex) > 0:
            self.deleteWrongList(tempList, removeIndex)

        for temp in tempList:
            for tempInfo in sorted(temp.oldPathName.iterdir()):
                if tempInfo.is_dir():
                    if loopForSubfolder:
                        tempFolderList.append(str(tempInfo))
                    else:
                        pass
                else:
                    tempFilesList.append(InfoForFile(tempInfo))
        if len(tempFilesList) != 0:
            self.setFileInfos(tempFilesList)
        if len(tempFolderList) != 0:
            valueForSubfolder = (tempFolderList, loopForSubfolder)
            self.differentiateFileFolder(valueForSubfolder)
    
    #파일 리스트를 받아서 폴더/파일 구분, 세부정보를 얻는 메소드에 넘기는 메소드, 매개변수 : tuple:([list:파일경로], bool:하위폴더검색여부)
    def differentiateFileFolder(self, pathsFromMainWindow):
        tempFilesList = []
        tempFoldersList = []
        for tempInfo in pathsFromMainWindow[0]:
            temp = PL.Path(tempInfo)
            if temp.exists():
                temp = InfoForFile(temp)
                if temp.oldPathName.is_dir():
                    tempFoldersList.append(temp)
                    print(QDir(str(temp.oldPathName)).count())
                else:
                    tempFilesList.append(temp)
            else:
                return CVs.MSG_ERROR_NOTEXISTPATH
        if pathsFromMainWindow[1] == True:
            loopForSubfolder = True
        else:
            loopForSubfolder = False
        
        if len(tempFilesList) != 0:
            self.setFileInfos(tempFilesList)
        
        if len(tempFoldersList) != 0:
            self.setFileInfosFromFolder(tempFoldersList, loopForSubfolder)
        return 0

    #파일이 실존하는지 확인하는 메소드, 매개변수 : list:파일 리스트, bool:원래이름/새이름 확인 
    def isExistFile(self, tempList, checkNewName):
        problemIndex = []
        if checkNewName:
            for index, tempInfo in enumerate(tempList):
                if not(tempInfo.newPathName.exists()):
                    problemIndex.append(index)
        else:
            for index, tempInfo in enumerate(tempList):
                if not(tempInfo.oldPathName.exists()):
                    problemIndex.append(index)
        return problemIndex

    #이름이 같은 파일이 존재하는지 확인하는 메소드, 매개변수 : list:파일 리스트
    def isSameFile(self, tempList):
        problemIndex = []
        for index, tempInfo in enumerate(tempList):
            for fileInfo in self.fileInfos:
                if tempInfo.oldPathName.samefile(fileInfo.oldPathName):
                    problemIndex.append(index)
                    break
        return problemIndex

    #존재하지 않거나, 중복된 파일 정보를 삭제하는 메소드, 매개변수 : list:[파일 리스트], list:[삭제할 파일 인덱스]
    def deleteWrongList(self, tempList, removeIndex):
        for index in reversed(removeIndex):
            del tempList[index]

    #기존 파일 관련정보 초기화
    def removeInfos(self):
        self.infosIndex.clear()
        self.fileInfos.clear()

    #파일 순서를 바꾸는 메소드, 인덱스 리스트에서만 변경, 매개변수 : bool:앞,뒤로 옮김 여부, list:[선택된 행]
    def moveFileInfo(self, isUp, currentRows):
        if isUp == True:
            upConstant = -1
            rowList = currentRows
        else:
            upConstant = 1
            rowList = reversed(currentRows)
        numberOfFiles = len(self.infosIndex)
        for currentRow in rowList:
            if (currentRow + upConstant < numberOfFiles) and (currentRow + upConstant > -1):
                tempInfo = self.infosIndex[currentRow]
                self.infosIndex[currentRow] = self.infosIndex[currentRow + upConstant]
                self.infosIndex[currentRow + upConstant] = tempInfo

    #파일을 불러온 처음 상태로 돌리는 메소드
    def undoChanged(self):
        for index in self.infosIndex:
            self.fileInfos[index].setNew()

    #바꾼 새 이름으로 파일을 바꾸는 메소드 
    def confirmNewName(self):
        #파일명 길이 체크
        for infoIndex in self.infosIndex:
            self.fileInfos[infoIndex].newPathName = self.fileInfos[infoIndex].path.joinpath(self.fileInfos[infoIndex].newName + self.fileInfos[infoIndex].suffix)
            if CVs.SIZE_MAXPATHLENGTH <= len(str(self.fileInfos[infoIndex].newPathName)):
                errorFileName = self.fileInfos[infoIndex].newPathName
                return (CVs.MSG_ERROR_TOOLARGENAMELENG, errorFileName)
        
        checkSameName = []
        for index, infoIndex in enumerate(self.infosIndex): #바꿀 이름끼리 같은지 확인
            isSameFile = False
            for compareIndex in self.infosIndex[index+1:]:
                if str(self.fileInfos[infoIndex].newPathName) == str(self.fileInfos[compareIndex].newPathName):
                    isSameFile = True
                    checkSameName.append(index)
                    break
            if isSameFile:
                errorFileName = self.fileInfos[infoIndex].newPathName
                return (CVs.MSG_ERROR_DUPLICATEDNAME, errorFileName)

        tempList = []
        for infoIndex in self.infosIndex:
            if self.fileInfos[infoIndex].oldPathName.exists(): #원본 파일이 현재 존재 확인
                if self.fileInfos[infoIndex].oldName == self.fileInfos[infoIndex].newName: #이름이 바뀌지 않을 경우 패스
                    tempList.append(str(self.fileInfos[infoIndex].newPathName))
                elif not(self.fileInfos[infoIndex].newPathName.exists()): #바꿀 이름의 파일이 이미 존재하는지 확인, not(False)가 정상
                    self.fileInfos[infoIndex].oldPathName.rename(self.fileInfos[infoIndex].newPathName)
                    tempList.append(str(self.fileInfos[infoIndex].newPathName))
                else:
                    errorFileName = self.fileInfos[infoIndex].newPathName
                    return (CVs.MSG_ERROR_EXISTSAMEFILE, errorFileName)
            else:
                errorFileName = self.fileInfos[infoIndex].newPathName
                return (CVs.MSG_ERROR_NOTEXISTFILE, errorFileName)
        self.removeInfos()
        self.differentiateFileFolder([tempList,False])
        return True


class InfoForFile:
    def __init__(self,pathAndName):
        if type(pathAndName) == str:
            self.oldPathName = PL.Path(pathAndName.strip())
        elif type(pathAndName) == type(PL.Path()):
            self.oldPathName = pathAndName

        self.path = self.oldPathName.parent
        
        self.oldName = self.oldPathName.stem
        
        self.suffix = self.oldPathName.suffixes
        # 복수확장자일경우 ex) .tar.xz
        if len(self.suffix) > 1 and self.suffix.count(".tar") > 0:
            self.suffix = (self.suffix[len(self.suffix)-2] + self.suffix[len(self.suffix)-1]).strip()
        else:
            self.suffix = self.oldPathName.suffix
        #self.accessedDate = TM.strftime(CVs.set_date, TM.localtime(self.oldPathName.stat().st_atime))
        self.modifiedDate = TM.strftime(CVs.SET_DATE, TM.localtime(self.oldPathName.stat().st_mtime))
        self.size = self.oldPathName.stat().st_size
        if self.size > CVs.SIZE_MAXDIGIT:
            self.size = "%0.2f" % (self.size/CVs.SIZE_MAXDIGIT) + CVs.STR_KIB
        else:
            self.size = str(self.size) + CVs.STR_BYTE
        self.setNew()

    def setNew(self):
        self.tempName = self.oldName
        self.newPathName = self.oldPathName
        self.newName = self.oldName




class ValueForFunction:
    def __init__(self):
        self.init()
        
    def init(self):
        self.str_first = ""
        self.str_second = ""
        self.int_first = 1
        self.int_second = 1
        self.int_start = 0
        self.int_digit = 0
        self.isFront = False
        self.isSpace = False
        self.isOver = 0   # ~부터(포함,이상) = 0, ~다음부터(미포함,초과) = 1
        self.isUnder = 0  # ~까지(포함,이하) = False, ~이전까지(미포함,미만) = True
    
    def notBlank(self, getStr):
        return len(getStr) > 0

    def setFisrtNum(self, getNum):
        if self.notBlank(getNum) and (int(getNum) > 0):
            self.int_first = int(getNum) - 1
            return True
        else:
            return False

    def setSecondNum(self, getNum):
        if self.notBlank(getNum) and (int(getNum) > 0):
            self.int_second = int(getNum) - 1
            return True
        else:
            return False

    def setStartNum(self, getNum):
        if self.notBlank(getNum) and (int(getNum) >= 0):
            self.int_start = int(getNum)
            return True
        else:
            return False

    def setDigitNum(self, getNum):
        if self.notBlank(getNum) and (int(getNum) > 0):
            self.int_digit = int(getNum)
            return True
        else:
            return False

    def setFisrtStr(self, getString):
        if self.notBlank(getString):
            self.str_first = getString
            return True
        else:
            return False

    def setSecondStr(self, getString):
        if self.notBlank(getString):
            self.str_second = getString
            return True
        else:
            return False

    def setValuesRBC(self, getValues):
        self.init()
        if self.setFisrtStr(getValues[0]):
            if self.setSecondStr(getValues[1]):
                self.isSpace = getValues[2]
                self.isOver = getValues[3]
                self.isUnder = getValues[4]
                return True
            else:
                return CVs.MSG_ERROR_SECONDSTRING
        else:
            return CVs.MSG_ERROR_FIRSTSTRING
    
    def setValuesRFO(self, getValues):
        self.init()
        if self.setFisrtNum(getValues[0]):
            if self.setSecondNum(getValues[1]):
                self.isSpace = getValues[2]
                self.isOver = getValues[3]
                self.isUnder = getValues[4]
                return True
            else:
                return CVs.MSG_ERROR_SMALLNUM
        else:
            return CVs.MSG_ERROR_ZERONUM
    
    def setValuesAN(self, getValues):
        self.init()
        if self.setStartNum(getValues[0]):
            if self.setDigitNum(getValues[1]):
                self.isSpace = getValues[2]
                self.isFront = getValues[3]
                return True
            else:
                return CVs.MSG_ERROR_DIGITNUM
        else:
            return CVs.MSG_ERROR_ZERONUM
    
    def setValuesAS(self, getValues):
        self.init()
        if self.setFisrtStr(getValues[0]):
            self.isSpace = getValues[1]
            self.isFront = getValues[2]
            return True
        else:
            return CVs.MSG_ERROR_FIRSTSTRING
    
    def setValuesRS(self, getValues):
        self.init()
        if self.setFisrtStr(getValues[0]):
            if self.setSecondStr(getValues[1]):
                return True
            else:
                return CVs.MSG_ERROR_SECONDSTRING
        else:
            return CVs.MSG_ERROR_FIRSTSTRING

    def setValuesSNN(self, getValues):
        self.init()
        self.setStartNum(getValues[0])
        if self.setFisrtStr(getValues[1]):
            return True
        else:
            return CVs.MSG_ERROR_FIRSTSTRING

