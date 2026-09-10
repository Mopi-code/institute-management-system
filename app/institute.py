import sys
from PySide6.QtWidgets import (QApplication, QMessageBox, QHBoxLayout, QVBoxLayout, QWidget,
                                QMainWindow, QLabel, QPushButton, QTabWidget, QTableWidget,
                                QTableWidgetItem, QDialog)
from qt_material import apply_stylesheet
from PySide6.QtCore import Qt
from PySide6.QtGui import QAction

import time
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


class TeachersDialog(QDialog):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle('Teachers')
        self.setGeometry(600,200,500,400)
        
        self.table=QTableWidget()
        
        self.initUI()
        self.load_teachers()
        
    def initUI(self):
        layout=QVBoxLayout()
        layout.addWidget(self.table)
        self.setLayout(layout)
        
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(['Name','Subject','Email'])
        
    def load_teachers(self):
        mycursor.execute("SELECT name,subject,email FROM teachers")
        teachers=mycursor.fetchall()
        
        self.table.setRowCount(len(teachers))
        
        for row,(name,subject,email) in enumerate(teachers):
            self.table.setItem(row,0,QTableWidgetItem(name))
            self.table.setItem(row,1,QTableWidgetItem(subject))
            self.table.setItem(row,2,QTableWidgetItem(email))
        
        self.table.resizeColumnsToContents()


class Institute(QMainWindow):
    def __init__(self,student_id,name):
        super().__init__()
        
        self.student_id=student_id
        self.name=name
        
        self.setWindowTitle('Institute')
        self.setGeometry(500,100,700,500)
        
        self.welcome_label=QLabel(f'Welcome, {name}')
        self.welcome_label.setObjectName('title')
        
        self.logout_btn=QPushButton('Logout')
        self.logout_btn.clicked.connect(self.logout)
        
        self.tabs=QTabWidget()
        
        self.available_table=QTableWidget()
        self.enroll_btn=QPushButton('Enroll Selected')
        self.enroll_btn.clicked.connect(self.enroll_selected)
        self.refresh_available_btn=QPushButton('Refresh')
        self.refresh_available_btn.clicked.connect(self.load_available_classes)
        
        self.my_classes_table=QTableWidget()
        self.unenroll_btn=QPushButton('Unenroll Selected')
        self.unenroll_btn.clicked.connect(self.unenroll_selected)
        self.refresh_my_classes_btn=QPushButton('Refresh')
        self.refresh_my_classes_btn.clicked.connect(self.load_my_classes)
        
        self.available_class_ids=[]
        self.my_enroll_ids=[]
        
        self.initUI()
        self.create_menu_bar()
        self.stylesheet()
        
        self.load_available_classes()
        self.load_my_classes()
        
    def initUI(self):
        central_widget=QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout=QVBoxLayout(central_widget)
        
        header_box=QHBoxLayout()
        header_box.addWidget(self.welcome_label)
        header_box.addStretch()
        header_box.addWidget(self.logout_btn)
        
        self.available_table.setColumnCount(4)
        self.available_table.setHorizontalHeaderLabels(['Class Name','Teacher','Schedule','Capacity'])
        
        available_layout=QVBoxLayout()
        available_layout.addWidget(self.available_table)
        
        available_buttons=QHBoxLayout()
        available_buttons.addWidget(self.enroll_btn)
        available_buttons.addWidget(self.refresh_available_btn)
        available_layout.addLayout(available_buttons)
        
        available_widget=QWidget()
        available_widget.setLayout(available_layout)
        
        self.my_classes_table.setColumnCount(4)
        self.my_classes_table.setHorizontalHeaderLabels(['Class Name','Teacher','Schedule','Enrolled At'])
        
        my_classes_layout=QVBoxLayout()
        my_classes_layout.addWidget(self.my_classes_table)
        
        my_classes_buttons=QHBoxLayout()
        my_classes_buttons.addWidget(self.unenroll_btn)
        my_classes_buttons.addWidget(self.refresh_my_classes_btn)
        my_classes_layout.addLayout(my_classes_buttons)
        
        my_classes_widget=QWidget()
        my_classes_widget.setLayout(my_classes_layout)
        
        self.tabs.addTab(available_widget,'Available Classes')
        self.tabs.addTab(my_classes_widget,'My Classes')
        
        main_layout.addLayout(header_box)
        main_layout.addWidget(self.tabs)
        
        central_widget.setLayout(main_layout)
        
    def create_menu_bar(self):
        self.menu_bar=self.menuBar()
        self.file_menu=self.menu_bar.addMenu('File')
        
        self.view_teachers_action=QAction('View Teachers',self)
        self.view_teachers_action.triggered.connect(self.view_teachers)
        
        self.logout_action=QAction('Logout',self)
        self.logout_action.triggered.connect(self.logout)
        
        self.file_menu.addAction(self.view_teachers_action)
        self.file_menu.addAction(self.logout_action)
        
    def load_available_classes(self):
        mycursor.execute("""
            SELECT classes.class_id, classes.name, teachers.name, classes.schedule, classes.capacity,
            (SELECT COUNT(*) FROM enrollments WHERE enrollments.class_id=classes.class_id)
            FROM classes
            JOIN teachers ON classes.teacher_id=teachers.teacher_id
        """)
        classes=mycursor.fetchall()
        
        self.available_class_ids=[]
        self.available_table.setRowCount(len(classes))
        
        for row,(class_id,class_name,teacher_name,schedule,capacity,booked) in enumerate(classes):
            self.available_class_ids.append(class_id)
            
            self.available_table.setItem(row,0,QTableWidgetItem(class_name))
            self.available_table.setItem(row,1,QTableWidgetItem(teacher_name))
            self.available_table.setItem(row,2,QTableWidgetItem(schedule))
            self.available_table.setItem(row,3,QTableWidgetItem(f'{capacity} ({booked} booked)'))
        
        self.available_table.resizeColumnsToContents()

        
    def load_my_classes(self):
        mycursor.execute("""
            SELECT classes.name, teachers.name, classes.schedule, enrollments.enrolled_at, enrollments.enroll_id
            FROM enrollments
            JOIN classes ON enrollments.class_id=classes.class_id
            JOIN teachers ON classes.teacher_id=teachers.teacher_id
            WHERE enrollments.student_id=%s
        """,(self.student_id,))
        my_classes=mycursor.fetchall()
        
        self.my_enroll_ids=[]
        self.my_classes_table.setRowCount(len(my_classes))
        
        for row,(class_name,teacher_name,schedule,enrolled_at,enroll_id) in enumerate(my_classes):
            self.my_enroll_ids.append(enroll_id)
            
            self.my_classes_table.setItem(row,0,QTableWidgetItem(class_name))
            self.my_classes_table.setItem(row,1,QTableWidgetItem(teacher_name))
            self.my_classes_table.setItem(row,2,QTableWidgetItem(schedule))
            self.my_classes_table.setItem(row,3,QTableWidgetItem(str(enrolled_at)))
        
        self.my_classes_table.resizeColumnsToContents()
        
    def enroll_selected(self):
        row=self.available_table.currentRow()
        
        if row==-1:
            QMessageBox.warning(self,'No Selection','Please select a class first.')
            return
        
        class_id=self.available_class_ids[row]
        
        mycursor.execute(
            "SELECT * FROM enrollments WHERE student_id=%s AND class_id=%s",
            (self.student_id,class_id))
        existing=mycursor.fetchone()
        
        if existing:
            QMessageBox.warning(self,'Already Enrolled','You are already enrolled in this class.')
            return
        
        mycursor.execute("SELECT capacity FROM classes WHERE class_id=%s",(class_id,))
        capacity=mycursor.fetchone()[0]
        
        mycursor.execute("SELECT COUNT(*) FROM enrollments WHERE class_id=%s",(class_id,))
        booked=mycursor.fetchone()[0]
        
        if booked>=capacity:
            QMessageBox.warning(self,'Class Full','This class has reached its capacity.')
            return
        
        mycursor.execute(
            "INSERT INTO enrollments(student_id,class_id) VALUES (%s,%s)",
            (self.student_id,class_id))
        myconnection.commit()
        
        QMessageBox.information(self,'Success','You have been enrolled!')
        
        self.load_available_classes()
        self.load_my_classes()
        
    def unenroll_selected(self):
        row=self.my_classes_table.currentRow()
        
        if row==-1:
            QMessageBox.warning(self,'No Selection','Please select a class first.')
            return
        
        enroll_id=self.my_enroll_ids[row]
        
        reply=QMessageBox.question(
            self,
            'Confirm Unenroll',
            'Are you sure you want to unenroll from this class?',
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply==QMessageBox.Yes:
            mycursor.execute("DELETE FROM enrollments WHERE enroll_id=%s",(enroll_id,))
            myconnection.commit()
            
            self.load_available_classes()
            self.load_my_classes()
        
    def view_teachers(self):
        self.teachers_dialog=TeachersDialog()
        self.teachers_dialog.exec()
        
    def logout(self):
        from login import Login
        self.login_window=Login()
        self.login_window.show()
        self.close()
        
    def stylesheet(self):
        self.setStyleSheet("""
            QLabel#title{
				font-size: 35px;
				font-family: Arial;
			} 
            QLabel{
				font-size: 20px;
				font-family: Arial;
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
    from login import Login
    
    window=Login() 
    window.show()
    
    apply_stylesheet(app,'dark_blue.xml')
    sys.exit(app.exec())
    
if __name__=='__main__':
    main()