def removeBetweenChar(TFIs, VFF):
    over = VFF.isOver
    under = VFF.isUnder
    charToFind1 = VFF.str_first
    charToFind2 = VFF.str_second
    spaceOrBlank = ''

    if VFF.isSpace:
        spaceOrBlank = ' '
    for infoIndex in TFIs.infosIndex:
        newName = TFIs.fileInfos[infoIndex].newName
        numToFind1 = newName.find(charToFind1) + over
        numToFind2 = newName.find(charToFind2,numToFind1) + 1 - under
        if (numToFind1 > -1) and (numToFind2 > 0):
            newName = newName[:numToFind1] + spaceOrBlank + newName[numToFind2:]
        else:
            pass
        TFIs.fileInfos[infoIndex].newName = newName
    VFF.init()



def removeFollowOrder(TFIs, VFF):
    over = VFF.isOver
    under = VFF.isUnder
    numToOrder1 = VFF.int_first + over
    numToOrder2 = VFF.int_second + 1 - under
    spaceOrBlank = ''

    if VFF.isSpace:
        spaceOrBlank = ' '
    for infoIndex in TFIs.infosIndex:
        newName = TFIs.fileInfos[infoIndex].newName
        if numToOrder1 < numToOrder2:
            newName = newName[:numToOrder1] + spaceOrBlank + newName[numToOrder2:]
        else:
            pass
        TFIs.fileInfos[infoIndex].newName = newName
    VFF.init()



def addNumber(TFIs, VFF):
    startNum = VFF.int_start
    digitNum = VFF.int_digit
    isFront = VFF.isFront
    digit_format = "%0" + str(digitNum) + "d"
    spaceOrBlank = ''

    if VFF.isSpace:
        spaceOrBlank = ' '

    if isFront == True:
        for infoIndex in TFIs.infosIndex:
            newName = TFIs.fileInfos[infoIndex].newName
            newName = digit_format % startNum + spaceOrBlank + newName
            startNum += 1
            TFIs.fileInfos[infoIndex].newName = newName
    else:
        for infoIndex in TFIs.infosIndex:
            newName = TFIs.fileInfos[infoIndex].newName
            newName = newName + spaceOrBlank + digit_format % startNum
            startNum += 1
            TFIs.fileInfos[infoIndex].newName = newName
    VFF.init()



def addString(TFIs, VFF):
    changedString = VFF.str_first
    isFront = VFF.isFront
    spaceOrBlank = ''

    if VFF.isSpace:
        spaceOrBlank = ' '

    if isFront == True:
        for infoIndex in TFIs.infosIndex:
            newName = TFIs.fileInfos[infoIndex].newName
            newName = changedString + spaceOrBlank + newName
            TFIs.fileInfos[infoIndex].newName = newName
    else:
        for infoIndex in TFIs.infosIndex:
            newName = TFIs.fileInfos[infoIndex].newName
            newName = newName + spaceOrBlank + changedString
            TFIs.fileInfos[infoIndex].newName = newName
    VFF.init()



def replaceString(TFIs, VFF):
    originalString = VFF.str_first
    changedString = VFF.str_second
    
    for infoIndex in TFIs.infosIndex:
        newName = TFIs.fileInfos[infoIndex].newName
        if newName.find(originalString) >= 0:
            newName = newName.replace(originalString, changedString)
        else:
            pass
        TFIs.fileInfos[infoIndex].newName = newName
    VFF.init()



def removeAllName(TFIs):    
    for infoIndex in TFIs.infosIndex:
        TFIs.fileInfos[infoIndex].newName = ""



def setNewName(TFIs, VFF):
    selectedIndex = VFF.int_start
    changedString = VFF.str_first
    TFIs.fileInfos[selectedIndex].newName = changedString
    VFF.init()


