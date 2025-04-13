import sys
import mysql.connector
import pandas as pd
import os
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QMenu, QInputDialog, QMessageBox, QFileDialog
)
from PyQt6.QtGui import QFont, QAction
from PyQt6.QtGui import QPalette, QBrush, QPixmap


from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QMessageBox, QFrame
)
from PyQt6.QtGui import QFont, QPixmap
from PyQt6.QtCore import Qt, QSize
import sys

# MySQL Database Connection
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Radha@1474",
    database="menu_management"
)
cursor = conn.cursor()

# ✅ Credentials
CORRECT_USERNAME = "admin"
CORRECT_PASSWORD = "password123"

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Question paper generator")
        self.resize(1024, 768)
        

        # ✅ Main Layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        self.setLayout(main_layout)

        # ✅ Create Background First
        self.background_label = QLabel(self)
        self.background_label.setScaledContents(True)

        # ✅ Card-like Login Frame
        login_frame = QFrame(self)
        login_frame.setStyleSheet("""
            background-color: white;
            border-radius: 12px;
            padding: 30px;
            border: 1px solid #ccc;
        """)
        frame_layout = QVBoxLayout()
        frame_layout.setSpacing(15)
        login_frame.setLayout(frame_layout)

        # ✅ Shop Name
        shop_label = QLabel("        ADCET         ")
        shop_label.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        shop_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        shop_label.setStyleSheet("color: #222;")
        frame_layout.addWidget(shop_label)

        # ✅ Owner Name
        owner_label = QLabel("COE")
        owner_label.setFont(QFont("Arial", 12))
        owner_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        owner_label.setStyleSheet("color: #666;")
        frame_layout.addWidget(owner_label)

        # ✅ Username Input
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Enter Username")
        self.username_input.setFont(QFont("Arial", 12))
        self.username_input.setStyleSheet(self.input_style())
        frame_layout.addWidget(self.username_input)

        # ✅ Password Input
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter Password")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setFont(QFont("Arial", 12))
        self.password_input.setStyleSheet(self.input_style())
        frame_layout.addWidget(self.password_input)

        # ✅ Login Button
        self.login_button = QPushButton("Login")
        self.login_button.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        self.login_button.setStyleSheet(self.button_style())
        self.login_button.clicked.connect(self.validate_login)
        frame_layout.addWidget(self.login_button)

        # ✅ Add Login Frame to Main Layout
        main_layout.addWidget(login_frame, alignment=Qt.AlignmentFlag.AlignCenter)

        # ✅ Apply Background
        self.set_background()

    def set_background(self):
        """ Set a full-screen background image using QLabel. """
        background_image = QPixmap("exam.jpg")  # Load background image

        if not background_image.isNull():
            self.background_label.setPixmap(background_image.scaled(
                self.size(), Qt.AspectRatioMode.IgnoreAspectRatio, Qt.TransformationMode.SmoothTransformation
            ))
            self.background_label.setGeometry(0, 0, self.width(), self.height())  # Fill screen

        # ✅ Ensure UI elements stay in front of the background
        self.background_label.lower()

    def resizeEvent(self, event):
        """ Ensure background resizes dynamically when window is resized. """
        self.set_background()
        super().resizeEvent(event)

    def input_style(self):
        return """
            QLineEdit {
                border: 2px solid #007BFF;
                border-radius: 5px;
                padding: 8px;
                font-size: 14px;
                background-color: white;
            }
            QLineEdit:focus {
                border-color: #0056b3;
            }
        """

    def button_style(self):
        return """
            QPushButton {
                background-color: #007BFF; color: white;
                border-radius: 8px; padding: 10px;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
        """

    def validate_login(self):
        username = self.username_input.text()
        password = self.password_input.text()
        
        if username == CORRECT_USERNAME and password == CORRECT_PASSWORD:
            self.open_dashboard()
        else:
            QMessageBox.warning(self, "Error", "Invalid Username or Password!")

    def open_dashboard(self):
        self.dashboard = Dashboard()
        self.dashboard.show()
        self.close()

####################################################################################

class Dashboard(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Academic Dashboard")
        self.setGeometry(100, 100, 1000, 600)

        # ✅ Initialize background label
        self.background_label = QLabel(self)
        self.set_background()

        self.initUI()
    
    def initUI(self):
        self.menu_bar = self.menuBar()
        self.menu_bar.setFont(QFont("Arial", 12))
        
        # Admin Menu
        admin_menu = self.menu_bar.addMenu("Admin")
        add_dept_action = QAction("Add Department", self)
        add_dept_action.triggered.connect(self.add_department)
        admin_menu.addAction(add_dept_action)
        
        del_dept_action = QAction("Delete Department", self)
        del_dept_action.triggered.connect(self.delete_department)
        admin_menu.addAction(del_dept_action)
        
        self.load_departments()

    def set_background(self):
        """ Set a full-screen background image using QLabel. """
        background_image = QPixmap("3.jpg")  # ✅ Replace with your actual image path

        if not background_image.isNull():
            self.background_label.setPixmap(background_image.scaled(
                self.size(), Qt.AspectRatioMode.IgnoreAspectRatio, Qt.TransformationMode.SmoothTransformation
            ))
            self.background_label.setGeometry(0, 0, self.width(), self.height())  # Fill screen
            self.background_label.setScaledContents(True)  # ✅ Ensure image scales properly
        
        # ✅ Ensure UI elements stay in front of the background
        self.background_label.lower()
    
    def resizeEvent(self, event):
        """ Ensure the background image resizes dynamically with the window. """
        self.set_background()
        super().resizeEvent(event)

    def load_departments(self):
        cursor.execute("SELECT id, name FROM departments")
        departments = cursor.fetchall()
        for dept_id, dept_name in departments:
            dept_menu = self.menu_bar.addMenu(dept_name)
            self.load_years(dept_menu, dept_id)
            
            add_year_action = QAction("Add Year", self)
            add_year_action.triggered.connect(lambda _, d=dept_id: self.add_year(d))
            dept_menu.addAction(add_year_action)
            
            del_year_action = QAction("Delete Year", self)
            del_year_action.triggered.connect(lambda _, d=dept_id: self.delete_year(d))
            dept_menu.addAction(del_year_action)

    def add_department(self):
        """ Add a new department """
        dept_name, ok = QInputDialog.getText(self, "Add Department", "Enter Department Name:")
        if ok and dept_name:
            cursor.execute("INSERT INTO departments (name) VALUES (%s)", (dept_name,))
            conn.commit()
            QMessageBox.information(self, "Success", "Department added successfully!")
            self.menu_bar.clear()
            self.initUI()

    def delete_department(self):
        """ Delete a department """
        cursor.execute("SELECT id, name FROM departments")
        departments = cursor.fetchall()
        dept_names = [dept[1] for dept in departments]
        
        if not dept_names:
            QMessageBox.warning(self, "Warning", "No departments available to delete.")
            return

        dept_name, ok = QInputDialog.getItem(self, "Delete Department", "Select Department:", dept_names, 0, False)
        if ok and dept_name:
            dept_id = next(dept[0] for dept in departments if dept[1] == dept_name)
            cursor.execute("DELETE FROM departments WHERE id = %s", (dept_id,))
            conn.commit()
            QMessageBox.information(self, "Success", "Department deleted successfully!")
            self.menu_bar.clear()
            self.initUI()
    
    def load_years(self, dept_menu, dept_id):
        cursor.execute("SELECT id, year_name FROM years WHERE department_id = %s", (dept_id,))
        years = cursor.fetchall()
        for year_id, year_name in years:
            year_menu = QMenu(year_name, self)
            dept_menu.addMenu(year_menu)
            self.load_subjects(year_menu, year_id)
            
            add_subject_action = QAction("Add Subject", self)
            add_subject_action.triggered.connect(lambda _, y=year_id: self.add_subject(y))
            year_menu.addAction(add_subject_action)
            
            del_subject_action = QAction("Delete Subject", self)
            del_subject_action.triggered.connect(lambda _, y=year_id: self.delete_subject(y))
            year_menu.addAction(del_subject_action)
            
    def add_year(self, dept_id):
        """ Add a new academic year to a department """
        year_name, ok = QInputDialog.getText(self, "Add Year", "Enter Year Name:")
        if ok and year_name:
            cursor.execute("SELECT COUNT(*) FROM years WHERE department_id = %s AND year_name = %s", (dept_id, year_name))
            if cursor.fetchone()[0] > 0:
                QMessageBox.warning(self, "Error", "Year already exists in this department!")
            else:
                cursor.execute("INSERT INTO years (department_id, year_name) VALUES (%s, %s)", (dept_id, year_name))
                conn.commit()
                QMessageBox.information(self, "Success", "Year added successfully!")
                self.menu_bar.clear()
                self.initUI()
                
    def delete_year(self, dept_id):
        """ Delete a year from a department """
        cursor.execute("SELECT id, year_name FROM years WHERE department_id = %s", (dept_id,))
        years = cursor.fetchall()
        year_names = [year[1] for year in years]

        if not year_names:
            QMessageBox.warning(self, "Warning", "No years available to delete.")
            return

        year_name, ok = QInputDialog.getItem(self, "Delete Year", "Select Year:", year_names, 0, False)
        if ok and year_name:
            year_id = next(year[0] for year in years if year[1] == year_name)
            cursor.execute("DELETE FROM years WHERE id = %s", (year_id,))
            conn.commit()
            QMessageBox.information(self, "Success", "Year deleted successfully!")
            self.menu_bar.clear()
            self.initUI()       
    
    def load_subjects(self, year_menu, year_id):
        cursor.execute("SELECT id, subject_name FROM subjects WHERE year_id = %s", (year_id,))
        subjects = cursor.fetchall()
        for subj_id, subj_name in subjects:
            subject_menu = QMenu(subj_name, self)
            year_menu.addMenu(subject_menu)

            upload_qb_action = QAction("Upload Question Bank (Excel)", self)
            upload_qb_action.triggered.connect(lambda _, s=subj_id: self.upload_question_bank(s))
            subject_menu.addAction(upload_qb_action)

            self.load_uploaded_files(subject_menu, subj_id)
            
    def add_subject(self, year_id):
        """ Add a subject to a year """
        subject_name, ok = QInputDialog.getText(self, "Add Subject", "Enter Subject Name:")
        if ok and subject_name:
            cursor.execute("SELECT COUNT(*) FROM subjects WHERE year_id = %s AND subject_name = %s", (year_id, subject_name))
            if cursor.fetchone()[0] > 0:
                QMessageBox.warning(self, "Error", "Subject already exists for this year!")
            else:
                cursor.execute("INSERT INTO subjects (year_id, subject_name) VALUES (%s, %s)", (year_id, subject_name))
                conn.commit()
                QMessageBox.information(self, "Success", "Subject added successfully!")
                self.menu_bar.clear()
                self.initUI()
                
    def delete_subject(self, year_id):
        """ Delete a subject from a year """
        cursor.execute("SELECT id, subject_name FROM subjects WHERE year_id = %s", (year_id,))
        subjects = cursor.fetchall()
        subject_names = [sub[1] for sub in subjects]

        if not subject_names:
            QMessageBox.warning(self, "Warning", "No subjects available to delete.")
            return

        subject_name, ok = QInputDialog.getItem(self, "Delete Subject", "Select Subject:", subject_names, 0, False)
        if ok and subject_name:
            subject_id = next(sub[0] for sub in subjects if sub[1] == subject_name)
            cursor.execute("DELETE FROM subjects WHERE id = %s", (subject_id,))
            conn.commit()
            QMessageBox.information(self, "Success", "Subject deleted successfully!")
            self.menu_bar.clear()
            self.initUI()

    def load_uploaded_files(self, subject_menu, subject_id):
        cursor.execute("SELECT id, file_name FROM excel_files WHERE subject_id = %s", (subject_id,))
        files = cursor.fetchall()
        for file_id, file_name in files:
            file_menu = QMenu(file_name, self)
            subject_menu.addMenu(file_menu)

            open_file_action = QAction("Open File", self)
            open_file_action.triggered.connect(lambda _, f=file_id: self.open_uploaded_file(f))
            file_menu.addAction(open_file_action)

            del_file_action = QAction("Delete File", self)
            del_file_action.triggered.connect(lambda _, f=file_id: self.delete_uploaded_file(f))
            file_menu.addAction(del_file_action)
    
    def upload_question_bank(self, subject_id):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Open Question Bank", "", 
            "Excel Files (*.csv *.xls *.xlsx *.xlsb *.xlsm);;All Files (*)"  
        )
        if not file_path:
            return
        try:
            with open(file_path, "rb") as file:
                file_data = file.read()
            cursor.execute(
                "INSERT INTO excel_files (subject_id, file_name, file_data) VALUES (%s, %s, %s)",
                (subject_id, file_path.split("/")[-1], file_data)
            )
            conn.commit()
            QMessageBox.information(self, "Success", "Question bank uploaded successfully!")
            self.menu_bar.clear()
            self.initUI()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error uploading file: {str(e)}")
    
    def open_uploaded_file(self, file_id):
        cursor.execute("SELECT file_name, file_data FROM excel_files WHERE id = %s", (file_id,))
        file = cursor.fetchone()
        if not file:
            QMessageBox.warning(self, "Error", "File not found in database.")
            return
        
        file_name, file_data = file
        file_path = os.path.join(os.getcwd(), file_name)
        
        try:
            with open(file_path, "wb") as f:
                f.write(file_data)

            os.system(f'start excel "{file_path}"')  # Open in Excel
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Could not open file: {str(e)}")

    def delete_uploaded_file(self, file_id):
        cursor.execute("SELECT file_name FROM excel_files WHERE id = %s", (file_id,))
        file = cursor.fetchone()
        if not file:
            QMessageBox.warning(self, "Error", "File not found in database.")
            return
        reply = QMessageBox.question(self, "Delete File", f"Are you sure you want to delete '{file[0]}'?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            cursor.execute("DELETE FROM excel_files WHERE id = %s", (file_id,))
            conn.commit()
            QMessageBox.information(self, "Success", "File deleted successfully!")
            self.menu_bar.clear()
            self.initUI()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    login_window = LoginWindow()
    login_window.show()
    login_window.showMaximized()
    sys.exit(app.exec())

