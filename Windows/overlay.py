import multiprocessing
from PySide6.QtCore import Qt, QTimer, QUrl
from PySide6.QtWidgets import QApplication, QLabel
from PySide6.QtMultimedia import QSoundEffect
from os import getcwd

def start_OL(qcm: multiprocessing.Queue):
    app = QApplication([])
    overlay = QLabel('30/30 пулек')
    isCanShot = True
    def resize():
        if isCanShot:
            overlay.resize(500, 500)
        else:
            overlay.resize(1000, 1000)
        scr = app.primaryScreen().availableGeometry()

        overlay.move(scr.x() + (scr.width() - overlay.width()) // 2, 
                     (scr.y() + scr.height() - overlay.height()) // 2 + 490)

    resize()

    #Nastroyka
    overlay.setWindowFlags(
        Qt.WindowType.FramelessWindowHint |
        Qt.WindowType.WindowStaysOnTopHint |
        Qt.WindowType.Tool
    )
    overlay.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
    overlay.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
    overlay.setAlignment(Qt.AlignmentFlag.AlignCenter)
    overlay.setStyleSheet('''
    QLabel {
        font-size: 25px;
        font-weight: bold;
    }
    ''')

    Patron = 30
    ShotSound = QSoundEffect()
    ShotSound.setSource(QUrl.fromLocalFile(getcwd() + '\\shot.wav'))
    ShotSound.setVolume(0.3)

    reloadSount = QSoundEffect()
    reloadSount.setSource(QUrl.fromLocalFile(getcwd() + '\\reload.wav'))
    reloadSount.setVolume(0.4)

    mili = 0

    def reload():
        nonlocal mili
        nonlocal isCanShot
        nonlocal Patron

        Patron = 30
        isCanShot = True

        overlay.setText(f'{Patron}/30 пулек')
        resize()

    r_timer = QTimer()
    r_timer.setSingleShot(True)
    r_timer.timeout.connect(reload)

    def chech_comm():
        nonlocal Patron
        nonlocal isCanShot

        while not qcm.empty():
            cmd = qcm.get()

            if cmd[0] == 'Пойти нахуй':
                overlay.setText('Да я иду нахуй')
                overlay.adjustSize()
                resize()
            elif cmd[0] == 'shooot':
                if not isCanShot:
                    continue

                if Patron <= 1:
                    isCanShot = False
                    overlay.setText('Где боеприпассы, Шайгу, Герасимов(Перезарядка...)')
                    overlay.adjustSize()
                    resize()
                    reloadSount.play()
                    r_timer.start(1500)
                    continue

                Patron -= 1
                overlay.setText(f'{Patron}/30 пулек')
                overlay.adjustSize()
                resize()
                ShotSound.play()

    timer = QTimer()
    timer.timeout.connect(chech_comm)
    timer.start(50)

    overlay.show()
    app.exec()