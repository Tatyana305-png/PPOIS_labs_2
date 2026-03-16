import sys
from PyQt5.QtWidgets import QApplication
from TeacherBase.Controllers.MainController import MainController

def main():
    app = QApplication(sys.argv)
    controller = MainController()
    controller.run()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
