from PyQt5 import QtCore, QtGui, QtWidgets
# from PyQt5.QtGui import QPixmap, QPalette, QBrush,QLinearGradient,QColor
from PyQt5.QtWidgets import QGraphicsDropShadowEffect,QInputDialog,QMessageBox
from database import authenticate_user
import sqlite3
from Inventory import InventoryApp


class Ui_MainWindow_Login(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(646, 548)
        MainWindow.setMinimumSize(600, 500)  # Prevents resizing below this size

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.Backgroundwidget = QtWidgets.QWidget(self.centralwidget)
        self.Backgroundwidget.setGeometry(QtCore.QRect(0, 0, 711, 561))
        self.Backgroundwidget.setObjectName("Backgroundwidget")
        self.Backgroundwidget.setStyleSheet("""
                        QWidget {
                                background: rgb(182, 204, 240);
                                            }
        """)
        
        # Login Page Card
        self.LoginPage = QtWidgets.QWidget(self.centralwidget)
        self.LoginPage.setGeometry(QtCore.QRect(180, 100, 291, 341))
        self.LoginPage.setAutoFillBackground(True)
        self.LoginPage.setStyleSheet("""
            QWidget {
                background-color: white;
                border-radius: 15px; /* Rounded Corners */
            }
        """)
        self.LoginPage.setObjectName("LoginPage")
        
        # Add Shadow Effect to Login Page Card
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setXOffset(5)
        shadow.setYOffset(5)
        shadow.setColor(QtGui.QColor(0, 0, 0, 180))  # Black semi-transparent shadow
        self.LoginPage.setGraphicsEffect(shadow)

        self.UserLoginLabel = QtWidgets.QLabel(self.LoginPage)
        self.UserLoginLabel.setGeometry(QtCore.QRect(90, 78, 150, 40))
        # self.UserLoginLabel.setStyleSheet("""
        #                 QLabel {
        #                         padding:5px;
        #                         }
        #                     """)
        font = QtGui.QFont()
        font.setFamily("Cascadia Mono SemiBold")
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.UserLoginLabel.setFont(font)
        self.UserLoginLabel.setObjectName("UserLoginLabel")
        
        # Username Input Field with Rounded Borders
        self.UsernameInput = QtWidgets.QLineEdit(self.LoginPage)
        self.UsernameInput.setGeometry(QtCore.QRect(60, 160, 181, 30))
        self.UsernameInput.setStyleSheet("""
            QLineEdit {
                border: 2px solid gray;
                border-radius: 10px;
                padding: 5px;
            }
        """)
        self.UsernameInput.setObjectName("UsernameInput")
        
        # Password Input Field with Rounded Borders
        self.PasswordInput = QtWidgets.QLineEdit(self.LoginPage)
        self.PasswordInput.setGeometry(QtCore.QRect(60, 200, 181, 30))
        self.PasswordInput.setEchoMode(QtWidgets.QLineEdit.Password)
        self.PasswordInput.setClearButtonEnabled(False)
        self.PasswordInput.setStyleSheet("""
            QLineEdit {
                border: 2px solid gray;
                border-radius: 10px;
                padding: 5px;
            }
        """)
        self.PasswordInput.setObjectName("PasswordInput")
        
        self.WelcomeLabel = QtWidgets.QLabel(self.LoginPage)
        self.WelcomeLabel.setGeometry(QtCore.QRect(60, 120, 191, 20))
        self.WelcomeLabel.setObjectName("WelcomeLabel")
        
        self.RememberCheckBox = QtWidgets.QCheckBox(self.LoginPage)
        self.RememberCheckBox.setGeometry(QtCore.QRect(60, 240, 70, 17))
        self.RememberCheckBox.setObjectName("RememberCheckBox")
        
        self.ForgotButton = QtWidgets.QPushButton(self.LoginPage)
        self.ForgotButton.setGeometry(QtCore.QRect(160, 240, 91, 16))
        self.ForgotButton.setObjectName("ForgotButton")
        self.ForgotButton.setStyleSheet("""
                            QPushButton {
                                        color:#f7443e;
                                        }
        """)
        self.ForgotButton.clicked.connect(self.UpdatePass)
        
        # Login Button Styling
        self.LoginButton = QtWidgets.QPushButton(self.LoginPage)
        self.LoginButton.setGeometry(QtCore.QRect(110, 270, 75, 30))
        self.LoginButton.setStyleSheet("""
            QPushButton {
                background-color: #73a4f5;
                color: white;
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color: darkblue;
            }
        """)
        self.LoginButton.setObjectName("LoginButton")
        self.LoginButton.clicked.connect(self.login)
        
        self.CreateAccBtn = QtWidgets.QPushButton(self.LoginPage)
        self.CreateAccBtn.setGeometry(QtCore.QRect(102, 310, 91, 16))
        self.CreateAccBtn.setObjectName("CreateAccBtn")
        self.CreateAccBtn.setStyleSheet("""
                QPushButton {
                            color:black;
                            font-weight:bold;
                            }
        """)
        self.CreateAccBtn.clicked.connect(self.signup)
        
        
        MainWindow.setCentralWidget(self.centralwidget)
        
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.center_login_card()  # Centers it when the app starts
        MainWindow.resizeEvent = self.resizeEvent  # Attach resize event

    def login(self):
        username = self.UsernameInput.text()
        password = self.PasswordInput.text()

        if authenticate_user(username, password):
            self.open_inventory()
        else:
            QtWidgets.QMessageBox.warning(None, "Login Failed", "Invalid credentials!")
    def open_inventory(self):
        """Open Inventory System After Successful Login"""
        self.inventory_window = QtWidgets.QMainWindow()
        self.ui = InventoryApp()
        self.ui.show()
        # self.inventory_window.show()
    
    def signup(self):
        """Switch to Signup Window"""
        from SignUp import Ui_MainWindow_SignUp
        self.signup_window = QtWidgets.QMainWindow()
        self.ui = Ui_MainWindow_SignUp()
        self.ui.setupUi(self.signup_window)
        self.signup_window.show()
         

    def center_login_card(self):
            """ Dynamically centers the login card when the window resizes """
            window_width = self.centralwidget.width()
            window_height = self.centralwidget.height()

            card_width = self.LoginPage.width()
            card_height = self.LoginPage.height()

            # Calculate the new position to keep it centered
            new_x = (window_width - card_width) // 2
            new_y = (window_height - card_height) // 2

            self.LoginPage.setGeometry(new_x, new_y, card_width, card_height)

    def resizeEvent(self, event):
            """ Calls the center_login_card() whenever the window resizes """
            self.center_login_card()
            event.accept()

    def ForgotPass(self):
        self.username,ok = QInputDialog.getText(self.centralwidget,"Forgot Password","Enter Username")
        if not ok:
             return
    
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ?",(self.username,))
        exist = cursor.fetchone()
        conn.close()
        return exist is not None
    
    def UpdatePass(self):
        if self.ForgotPass():
            NewPass,ok = QInputDialog.getText(self.centralwidget,"New Password","Enter New Password")
            if not ok:
                return
            if not NewPass:
                QMessageBox.warning(self.centralwidget,"Error","Please Enter The New Password")
                return
            conn = sqlite3.connect("users.db")
            cursor = conn.cursor()
            cursor.execute("UPDATE users SET password = ? WHERE username = ?",(NewPass,self.username))
            conn.commit()
            conn.close()
            QMessageBox.information(self.centralwidget,"Success",f"Password for {self.username} has been changed Successfully!")
        else:
             QMessageBox.critical(self.centralwidget,"Error",f"No User Found By Username : {self.username}")
 
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.UserLoginLabel.setText(_translate("MainWindow", "User Login"))
        self.UsernameInput.setPlaceholderText(_translate("MainWindow", "Username"))
        self.PasswordInput.setPlaceholderText(_translate("MainWindow", "Password"))
        self.WelcomeLabel.setText(_translate("MainWindow", "Welcome to Whatsapp Automation Bot"))
        self.RememberCheckBox.setText(_translate("MainWindow", "Remember Me"))
        self.ForgotButton.setText(_translate("MainWindow", "Forgot Password?"))
        self.LoginButton.setText(_translate("MainWindow", "Login"))
        self.CreateAccBtn.setText(_translate("MainWindow", "Create Account"))

    


def Main_Login():
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow_Login()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())   
if __name__ == "__main__":
    Main_Login()
    
