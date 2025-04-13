import sys
import mysql.connector
import pandas as pd
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QMenu, QInputDialog, QMessageBox, QFileDialog
)
from PyQt6.QtGui import QFont, QAction

# MySQL Database Connection
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Radha@1474",
    database="menu_management"
)
cursor = conn.cursor()

class Dashboard(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Academic Dashboard")
        self.setGeometry(100, 100, 1000, 600)
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
    
    def load_departments(self):
        """ Load all departments into the menu """
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
    
    def load_years(self, dept_menu, dept_id):
        """ Load years under a department """
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
    
    def load_subjects(self, year_menu, year_id):
        """ Load subjects under a year """
        cursor.execute("SELECT id, subject_name FROM subjects WHERE year_id = %s", (year_id,))
        subjects = cursor.fetchall()
        for subj_id, subj_name in subjects:
            subject_menu = QMenu(subj_name, self)
            year_menu.addMenu(subject_menu)

            # Option to upload question bank
            upload_qb_action = QAction("Upload Question Bank (Excel)", self)
            upload_qb_action.triggered.connect(lambda _, s=subj_id: self.upload_question_bank(s))
            subject_menu.addAction(upload_qb_action)

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
        """ Delete an existing department """
        cursor.execute("SELECT id, name FROM departments")
        departments = cursor.fetchall()
        dept_names = [dept[1] for dept in departments]
        dept_name, ok = QInputDialog.getItem(self, "Delete Department", "Select Department:", dept_names, 0, False)
        if ok and dept_name:
            cursor.execute("DELETE FROM departments WHERE name = %s", (dept_name,))
            conn.commit()
            QMessageBox.information(self, "Success", "Department deleted successfully!")
            self.menu_bar.clear()
            self.initUI()
    
    def add_year(self, dept_id):
        """ Add a new academic year under a department """
        year_name, ok = QInputDialog.getText(self, "Add Year", "Enter Year Name:")
        if ok and year_name:
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
        year_name, ok = QInputDialog.getItem(self, "Delete Year", "Select Year:", year_names, 0, False)
        if ok and year_name:
            cursor.execute("DELETE FROM years WHERE year_name = %s AND department_id = %s", (year_name, dept_id))
            conn.commit()
            QMessageBox.information(self, "Success", "Year deleted successfully!")
            self.menu_bar.clear()
            self.initUI()
    
    def add_subject(self, year_id):
        """ Add a new subject under a year """
        subj_name, ok = QInputDialog.getText(self, "Add Subject", "Enter Subject Name:")
        if ok and subj_name:
            cursor.execute("INSERT INTO subjects (year_id, subject_name) VALUES (%s, %s)", (year_id, subj_name))
            conn.commit()
            QMessageBox.information(self, "Success", "Subject added successfully!")
            self.menu_bar.clear()
            self.initUI()
    
    def delete_subject(self, year_id):
        """ Delete a subject from a year """
        cursor.execute("SELECT id, subject_name FROM subjects WHERE year_id = %s", (year_id,))
        subjects = cursor.fetchall()
        subject_names = [subj[1] for subj in subjects]
        subj_name, ok = QInputDialog.getItem(self, "Delete Subject", "Select Subject:", subject_names, 0, False)
        if ok and subj_name:
            cursor.execute("DELETE FROM subjects WHERE subject_name = %s AND year_id = %s", (subj_name, year_id))
            conn.commit()
            QMessageBox.information(self, "Success", "Subject deleted successfully!")
            self.menu_bar.clear()
            self.initUI()

    def upload_question_bank(self, subject_id):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Open Question Bank", "", 
            "Excel Files (*.csv *.xls *.xlsx *.xlsb);;All Files (*)"
        )

        if not file_path:
            return  # If no file is selected, exit the function

        try:
            # Determine file type and read accordingly
            if file_path.endswith('.csv'):
                df = pd.read_csv(file_path)
            elif file_path.endswith('.xlsb'):
                df = pd.read_excel(file_path, engine='pyxlsb')
            else:  # Handles .xls and .xlsx
                df = pd.read_excel(file_path)

            # Remove leading/trailing spaces from column names
            df.columns = df.columns.str.strip()
            print("Columns in DataFrame:", df.columns.tolist())  # Debugging

            # Ensure required columns exist
            required_columns = {'Question', 'Answer'}
            if not required_columns.issubset(df.columns):
                print("Error: Required columns 'Question' or 'Answer' not found in the file.")
                return

            # Insert each question-answer pair into the database
            for _, row in df.iterrows():
                question = row['Question']
                answer = row['Answer']
                print(f"Uploading: {question} -> {answer}")  # Debugging
                # Insert into database (Replace with actual DB logic)
                # cursor.execute("INSERT INTO question_bank (subject_id, question, answer) VALUES (%s, %s, %s)",
                #                (subject_id, question, answer))
                # db.commit()

        except Exception as e:
            print("Error reading Excel file:", e)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    dashboard = Dashboard()
    dashboard.show()
    sys.exit(app.exec())
