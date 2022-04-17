import Gui.MainFrame as MF
from PyQt5.QtWidgets import QApplication
import sys


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui = MF.UiMainWindow()
    sys.exit(app.exec_())
'''
현재 문제 21.5.6
1. 드래그&드랍으로 파일 추가 후 메인창 비활성화 상태에서 테이블에 있는 아이템 하나를
    클릭, 드래그&드랍시 현재폴더(".")가 드래그&드랍 되는 버그
    - 해결책
        1) 하드코딩으로 파일을 읽을 때 "."을 읽지 않는다
        2) 파일을 읽을 때 상대경로를 모두 막는다
    - 해결됨
        - 원인 : 해당 버그에서 eventFilter가 쓰레기 값을 읽고, 공백('')을 값으로 보내면
                pathlib에서 공백을 현재 폴더로 읽어들여서 발생하는 오류
        - 해결 : eventFilter에서 문자열 길이 체크를 해서 0보다 클 경우만 list에 삽입

2. tablewidget의 columnheader 클릭시 정렬되는 기능 사용시
    item이 제대로 표시되지 않는 버그
2-1 파일 추가 전에 클릭 후 파일 추가시 원래 이름 열만 제대로 작동
    나머지 열은 비어있거나 다른 행의 값이 들어가있음
2-2 파일 추가 후 클릭 시에는 제대로 작동하는 것처럼 보이나
    이후 파일 추가하면 2-1과 같은 버그 발생
    - 해결책
        1) 주어진 기능을 사용하지 않고, 해당 열의 header와 관련된 fileinfo를 기준으로 정렬

3. verticalHeader().setSectionsMovable(True) 사용 하여 행을 이동 시
    보여지는 행은 움직이지만 행의 값은 변하지 않아서 기능 이용시 순서가 엇갈림
3-1 또한 여러행을 한꺼번에 이동 불가
    - 해결책
        1) 사용하지 않는다 - 마우스를 이용한 이동이 불가능함
        2) 행 이동 후 행 사이의 순서를 받아서 사용한다
            - 기존 fileInfo index위주의 기능을 모두 고쳐야함
            - 순서를 어떻게 받나?
    - 해결
        - 사용 안함
 4. QFileDialog.getExistingDirectory가 맘에 안듬
     - 해결책
         - TreeView 이용해서 Dialog를 하나 만듬
         - 복잡
    
'''