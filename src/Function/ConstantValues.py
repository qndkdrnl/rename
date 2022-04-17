import locale as LC

SIZE_MAXDIGIT = 1024
STR_BYTE = " bytes"
STR_KIB = " KiB"
STR_MIB = " MiB"
STR_GIB = " GiB"

SIZE_MAXPATHLENGTH = 255
SIZE_WIDTH_MAINFRAME = 800
SIZE_HEIGHT_MAINFRAME = 530 
SIZE_WIDTH_DIALOG = 350
SIZE_HEIGHT_DIALOG = 120
SIZE_WIDTH_DWIDGETS = 70
SIZE_HEIGHT_DWIDGETS = 30
SIZE_WIDTH_MFWIDGETS = SIZE_WIDTH_DWIDGETS + 30
SIZE_HEIGHT_MFWIDGETS = SIZE_HEIGHT_DWIDGETS + 10

if LC.getdefaultlocale()[0] == "ko_KR":
    #메인윈도우 문자
    STR_MAINWINDOW = "파일 이름 바꾸기"
    STR_CONFIRMNEWNAME = "변경된 이름\n적용하기"
    STR_UNDOCHANGED = "변경된 이름\n취소하기"
    STR_UP = "위로"
    STR_DOWN = "아래로"
    STR_RBC = "두 문자 사이\n이름 지우기"
    STR_RFO = "두 위치 사이\n이름 지우기"
    STR_AN = "숫자\n추가하기"
    STR_AS = "문자\n추가하기"
    STR_RS = "문자 대체하기"
    STR_RAN = "이름 모두 지우기" 
    STR_SNN = "새 이름 입력"
    STR_OLDNAME = "원래 이름"
    STR_NEWNAME = "새 이름"
    STR_PATH = "경로"
    STR_MODIFIEDDATE = "수정한 날짜"
    STR_SIZE = "파일 크기"
    STR_FILE = "파일(&F)"
    STR_OPENFILES = "파일 새로 열기"
    STR_ADDFILES = "파일 추가하기"
    STR_OPENFOLDER = "폴더 새로 열기"
    STR_ADDFOLDER = "폴더 추가하기"
    STR_CLEANFILE = "비우기"
    STR_QUIT = "종료"
    STR_ACTIONOPENFILES = STR_OPENFILES + "(&N)"
    STR_ACTIONADDFILES = STR_ADDFILES + "(&A)"
    STR_ACTIONOPENFOLDER = STR_OPENFOLDER + "(&O)"
    STR_ACTIONADDFOLDER = STR_ADDFOLDER + "(&F)"
    STR_ACTIONCLEANFILE = STR_CLEANFILE + "(&C)"
    STR_ACTIONQUIT = STR_QUIT + "(&Q)"
    #다이얼로그 문자
    STR_DIALOGCNN = STR_CONFIRMNEWNAME.replace("\n"," ")
    STR_DIALOGUC = STR_UNDOCHANGED.replace("\n"," ")
    STR_DIALOGRBC = STR_RBC.replace("\n"," ")
    STR_DIALOGRFO = STR_RFO.replace("\n"," ")
    STR_DIALOGAN = STR_AN.replace("\n"," ")
    STR_DIALOGAS = STR_AS.replace("\n"," ")
    STR_DIALOGRS = STR_RS
    STR_DIALOGRAN = STR_RAN
    STR_DIALOGSNN = STR_SNN
    STR_ISFRONT = "앞에 추가"
    STR_ISSPACE = "빈칸 추가"
    STR_FIRSTSTR = "시작 문자"
    STR_SECONDSTR = "마지막 문자"
    STR_FIRSTNUM = "시작 숫자"
    STR_SECONDNUM = "마지막 숫자"
    STR_TOADDSTR = "추가할 문자"
    STR_TOFINDSTR = "찾을 문자"
    STR_TOCHANGESTR = "바꿀 문자"
    STR_DIGITNUM = "자리수"
    STR_ISOVERNUM = "초과"
    STR_ISORMORENUM = "이상"
    STR_ISUNDERNUM = "미만"
    STR_ISORLESSNUM = "이하"
    STR_ISOVERCHAR = "이후부터"
    STR_ISORMORECHAR = "부터(포함)"
    STR_ISUNDERCHAR = "이전까지"
    STR_ISORLESSCHAR = "까지(포함)"
    STR_SELECTFOLDER = "폴더를 선택해주세요"
    STR_ISINCLUDESUB = "하위 폴더 포함"
    
    STR_HINT_CASESENSITIVE = "대소문자 구분"
    STR_HINT_ONLYNUM = "숫자만 입력"
    STR_HINT_INPUT = "입력하세요"
    
    #다이얼로그 입력 제한용 정규표현식
    SET_NOSPECIALCHAR = "[^\\\|*/?%:\"><.]*"
    SET_ONLYINTCHAR = "[0-9]*"
    
    SET_DATE = "%Y년 %m월 %d일 %H시 %M분 %S초"
    
    #메시지 다이얼로그 문자
    MSG_ASK_CONFRIMCHANGE = "파일 이름을 변경하시겠습니까?"
    MSG_ASK_UNDOCHANGE = "이름 변경을 취소하시겠습니까?"
    MSG_ASK_REMOVEALLNAME = "이름을 모두 지웁니다"
    
    
    MSG_WRN_WRNTITLE = "경 고"
    MSG_WRN_NOSPECIALCHAR = "파일 이름에 다음 특수 문자 사용 불가\n\\  |  *  /  ?  %  :  \"  >  <  ."
    MSG_WRN_ONLYNUM = "숫자만 입력하세요"
    MSG_WRN_SUBFOLDERS = "하위 폴더가 많을 경우 오래 걸리거나 프로그램이 멈출 수 있습니다"

    MSG_ERROR_ERRORTITLE = "오 류"
    MSG_ERROR_FIRSTSTRING = "첫번째 문자열 오류"
    MSG_ERROR_SECONDSTRING = "두번째 문자열 오류"
    MSG_ERROR_INTNUM = "자연수를 입력하세요"
    MSG_ERROR_SMALLNUM = "첫번째 숫자보다 큰 숫자를 입력하세요"
    MSG_ERROR_ZERONUM = "0보다 큰 자연수를 입력하세요"
    MSG_ERROR_DIGITNUM = "자리수는 " + MSG_ERROR_ZERONUM
    MSG_ERROR_NOTEXISTFILE = "파일이 존재하지 않습니다"
    MSG_ERROR_NOTEXISTPATH = "폴더가 존재하지 않습니다"
    MSG_ERROR_NOFILEINPATH = "폴더 내부에 " + MSG_ERROR_NOTEXISTFILE
    MSG_ERROR_EXISTSAMEFILE = "이름이 같은 파일이 이미 존재합니다"
    MSG_ERROR_DUPLICATEDNAME = "바꿀 이름 중 같은 것이 존재합니다"
    MSG_ERROR_TOOLARGENAMELENG = "파일명이 너무 깁니다. 경로를 포함하여 " + str(SIZE_MAXPATHLENGTH) + "자 이하로 줄여주세요"