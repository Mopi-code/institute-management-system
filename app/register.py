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


class Register(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle('Register Window')
        self.setGeometry(500,100,500,470)
        
        self.title=QLabel('Create Account')
        self.title.setObjectName('title')
        
        self.name=QLabel('Name :')
        self.name_entry=QLineEdit()
        
        self.email=QLabel('Email :')
        self.email_entry=QLineEdit()
        
        self.password=QLabel('Password :')
        self.password_entry=QLineEdit()
        
        self.sign_up=QPushButton('Sign Up')
        self.sign_up.clicked.connect(self.sign_up_member)
        
        self.back_to_login=QPushButton('Back to Login')
        self.back_to_login.clicked.connect(self.go_to_login)
        
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
        
        self.box_name=QHBoxLayout()
        self.box_name.setContentsMargins(0,10,0,0)
        
        self.name.setFixedSize(100,60)
        self.name_entry.setPlaceholderText('Your name')
        self.name_entry.setFixedSize(340,60)
        
        self.box_email=QHBoxLayout()
        
        self.email.setFixedSize(100,60)
        self.email_entry.setPlaceholderText('Your email')
        self.email_entry.setFixedSize(340,60)
        
        self.box_password=QHBoxLayout()
        self.box_password.setContentsMargins(0,0,0,20)
        
        self.password.setFixedSize(100,60)
        self.password_entry.setPlaceholderText('Your password')
        self.password_entry.setFixedSize(340,60)
        
        self.bottom_box=QVBoxLayout()
        
        self.sign_up.setFixedSize(200,50)
        self.back_to_login.setFixedSize(300,50)
        
        self.box_name.addWidget(self.name)
        self.box_name.addWidget(self.name_entry)
        
        self.box_email.addWidget(self.email)
        self.box_email.addWidget(self.email_entry)
        
        self.box_password.addWidget(self.password)
        self.box_password.addWidget(self.password_entry)
        
        self.bottom_box.addWidget(self.sign_up,alignment=Qt.AlignCenter)
        self.bottom_box.addWidget(self.back_to_login,alignment=Qt.AlignCenter)
        
        main_layout.addWidget(self.title)
        
        main_layout.addLayout(self.box_name)
        main_layout.addLayout(self.box_email)
        main_layout.addLayout(self.box_password)
        main_layout.addLayout(self.bottom_box)
        
        main_layout.addStretch()
        
        central_widget.setLayout(main_layout)
        
    def sign_up_member(self):
        name=self.name_entry.text()
        email=self.email_entry.text()
        password=self.password_entry.text()

        if len(name)==0:
            QMessageBox.warning(
                self,
                'Name Error!',
                'Please enter your name.'
            )
            
        else : 
            if len(email)==0:
                QMessageBox.warning(
                    self,
                    'Email Error!',
                    'Please enter your email.'
                )
                
            else :
                mycursor.execute("SELECT * FROM students WHERE email=%s",(email,))
                existing=mycursor.fetchone()
                
                if existing :
                    QMessageBox.warning(
                        self,
                        'Email Repeated!',
                        'We already have a user with this email, enter another email.'
                    )
                else :
                    if len(password)<=7:
                        QMessageBox.warning(
                            self,
                            'Password error',
                            'Your password should be at least 8-digits'
                        )   
                    else :
                        mycursor.execute(
                            'INSERT INTO students(name,email,password) VALUES (%s,%s,%s)',
                            (name,email,password,))
                        myconnection.commit()
                        
                        new_student_id=mycursor.lastrowid
                        
                        self.institute=Institute(new_student_id,name)
                        self.institute.show()
                        self.close()
  
    def go_to_login(self):
        from login import Login   
              
        self.login_window=Login()
        self.login_window.show()
        
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
    
    window=Register()
    window.show()
    
    apply_stylesheet(app,'dark_blue.xml')
    sys.exit(app.exec())
    
if __name__=='__main__':
    main()