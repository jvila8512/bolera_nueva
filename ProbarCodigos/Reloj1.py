import sys
from PyQt6.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget,QLCDNumber
from PyQt6.QtCore import QTimer, QTime

class ClockApp(QLCDNumber): 

      def __init__(self, parent=None):
        super().__init__(parent)
        self.setSegmentStyle(QLCDNumber.SegmentStyle.Filled)
        self.setDigitCount(8)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.show_time)
        self.timer.start(1000)

        self.show_time()

        self.setWindowTitle("Digital Clock")
        self.resize(250, 60)

   
      def show_time(self):
        time = QTime.currentTime()
        text = time.toString("hh:mm:ss")

        # Blinking effect
        if (time.second() % 2) == 0:
            text = text.replace(":", " ")

        self.display(text)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    clock = ClockApp()
    clock.show()
    
    sys.exit(app.exec())