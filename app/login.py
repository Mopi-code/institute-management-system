import sys
from PySide6.QtWidgets import QApplication, QMessageBox, QHBoxLayout, QVBoxLayout, QWidget, QMainWindow, QLabel, QLineEdit, QPushButton
from qt_material import apply_stylesheet
from PySide6.QtCore import Qt
from institute import Institute

import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()

myconnection=mysql.connector.connect(
    host=os.getenv('DB_HOST', 'localhost'),
    user=os.getenv('DB_USER', 'root'),
    password=os.getenv('DB_PASSWORD'),
    database=os.getenv('DB_NAME', 'institute')
)
mycursor=myconnection.cursor()


class Login(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle('Login Window')
        self.setGeometry(500,100,500,400)
        
        self.title=QLabel('Login')
        self.title.setObjectName('title')
        
        self.email=QLabel('Email :')
        self.email_entry=QLineEdit()
        
        self.password=QLabel('Password :')
        self.password_entry=QLineEdit()
        
        self.log_in=QPushButton('Log In')
        self.log_in.clicked.connect(self.login_member)
        
        self.back_to_register=QPushButton('Back to Register')
        self.back_to_register.clicked.connect(self.go_to_register)
        
        self.initUI()
        self.stylesheet()
        
    def initUI(self):
        central_widget=QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout=QVBoxLayout(central_widget)
        main_layout.setSpacing(10)
        main_layout.setContentsMargins(15,10,15,10)
        
        self.title.setFixedSize(470,70)
        self.title.setAlignment(Qt.AlignCenter)
        
        self.box_email=QHBoxLayout()
        self.box_email.setContentsMargins(0,10,0,0)
        
        self.email.setFixedSize(100,60)
        self.email_entry.setPlaceholderText('Your email')
        self.email_entry.setFixedSize(340,60)
        
        self.box_password=QHBoxLayout()
        self.box_password.setContentsMargins(0,0,0,20)
        
        self.password.setFixedSize(100,60)
        self.password_entry.setPlaceholderText('Your password')
        self.password_entry.setFixedSize(340,60)
        
        self.bottom_box=QVBoxLayout()
        
        self.log_in.setFixedSize(200,50)
        self.back_to_register.setFixedSize(300,50)
        
        self.box_email.addWidget(self.email)
        self.box_email.addWidget(self.email_entry)
        
        self.box_password.addWidget(self.password)
        self.box_password.addWidget(self.password_entry)
        
        self.bottom_box.addWidget(self.log_in,alignment=Qt.AlignCenter)
        self.bottom_box.addWidget(self.back_to_register,alignment=Qt.AlignCenter)
        
        main_layout.addWidget(self.title)
        
        main_layout.addLayout(self.box_email)
        main_layout.addLayout(self.box_password)
        main_layout.addLayout(self.bottom_box)
        
        main_layout.addStretch()
        
        central_widget.setLayout(main_layout)
        
    def login_member(self):
        email=self.email_entry.text()
        password=self.password_entry.text()

        if len(email)==0:
            QMessageBox.warning(
                self,
                'Email Error!',
                'Please enter your email.'
            )
            
        else :
            if len(password)==0:
                QMessageBox.warning(
                    self,
                    'Password Error!',
                    'Please enter your password.'
                )
                
            else :
                mycursor.execute("SELECT student_id,name FROM students WHERE email=%s AND password=%s",(email,password))
                existing=mycursor.fetchone()
                
                if existing :
                    student_id,name=existing
                    
                    self.institute=Institute(student_id,name)
                    self.institute.show()
                    self.close()
                else :
                    QMessageBox.warning(
                        self,
                        'Login Failed',
                        'Wrong email or password.'
                    )
  
    def go_to_register(self):
        from register import Register
        
        self.register_window=Register()
        self.register_window.show()
        
        self.close()
        
    def stylesheet(self) :
        self.setStyleSheet("""
            QLabel#title{
				font-size: 35px;
				font-family: Arial;
			} 
            QLabel{
				font-size: 20px;
				font-family: Arial;
			} 
            QLineEdit{
                font-size: 20px;
            }
            QPushButton{
                font-size: 15px;
                background-color: #4266f5;
                border-color: #4266f5;
                color: white;
            }
            QPushButton:hover{
                background-color: transparent;
                color: #4266f5;
            }
        """)


def main():
    app=QApplication(sys.argv)
    
    window=Login()
    window.show()
    
    apply_stylesheet(app,'dark_blue.xml')
    sys.exit(app.exec())
    
if __name__=='__main__':
    main()