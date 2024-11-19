# Expense Tracker App

# import modules
import sys

from PyQt5.QtCore import Qt, QDate
from PyQt5.QtWidgets import (QApplication, 
                            QWidget, QLabel, QLineEdit, 
                            QPushButton, QVBoxLayout, 
                            QHBoxLayout, QComboBox, 
                            QDateEdit, QTableWidget, 
                            QMessageBox, QTableWidgetItem, QHeaderView)
from PyQt5.QtSql import QSqlDatabase, QSqlQuery
#from PyQt5.QtCore import QDate


class ExpenseApp(QWidget):
    def __init__(self):
        super().__init__()
        
        # main windows objects and settings
        self.setWindowTitle("Expense Tracker App")
        self.resize(550, 500)
        
        # create objects for/on display screen
        self.date_box = QDateEdit()
        self.date_box.setDate(QDate.currentDate())
        self.dropdown = QComboBox()
        self.amount = QLineEdit()
        self.description = QLineEdit()  
        
        self.add_button = QPushButton("Add Expense")
        self.delete_button = QPushButton("Delete Expense")
        self.add_button.clicked.connect(self.add_expense)
        self.delete_button.clicked.connect(self.delete_expense)
        
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        header_names = ["id", "Date", "Category", "Amount", "Description"]
        self.table.setHorizontalHeaderLabels(header_names)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        
        self.table.sortByColumn(1, Qt.DescendingOrder)   # sort table in descending order
        
        # design and styling
        self.setStyleSheet("""
                          QWidget {background-color: #b8c9e1}
                          
                          QLabel{
                              color: #333;
                              font-size: 14px;
                          }
                          
                          QLineEdit, QComboBox, QDateEdit{
                              background-color: #b8c9e1;
                              color: #333;
                              border: 1px solid #444;
                              padding: 5px;
                          }
                          
                          QTableWidget{
                              background-color: #b8c9e1;
                              color: #333;
                              border: 1px solid #444;
                              selection-background-color: #ddd;
                          }
                          
                          QPushButton{
                              background-color: #4caf5a;
                              color: #fff;
                              border: none;
                              padding: 8px 16px;
                              font-size: 14px
                          }
                          
                          QPushButton:hover{
                              background-color: #45e049
                          }
                          
                          """)
        
        # create app layout
        self.dropdown.addItems(["Walmart", "House Rent", "Bills", "Insurance", "Medicals", "Housing", "Morgage"])
        
        self.main_layout = QVBoxLayout()
        self.row1 = QHBoxLayout()
        self.row2 = QHBoxLayout()
        self.row3 = QHBoxLayout()
        
        self.row1.addWidget(QLabel("Date:"))
        self.row1.addWidget(self.date_box)
        self.row1.addWidget(QLabel("Category:"))
        self.row1.addWidget(self.dropdown) 
        
        self.row2.addWidget(QLabel("Amount:"))
        self.row2.addWidget(self.amount)
        self.row2.addWidget(QLabel("Description:"))
        self.row2.addWidget(self.description) 
        
        self.row3.addWidget(self.add_button)
        self.row3.addWidget(self.delete_button) 
        
        self.main_layout.addLayout(self.row1)
        self.main_layout.addLayout(self.row2)
        self.main_layout.addLayout(self.row3)
        
        self.main_layout.addWidget(self.table)
        
        
        self.setLayout(self.main_layout)
        
        self.load_table()
        
        
    def load_table(self):
        self.table.setRowCount(0)
        
        query = QSqlQuery("SELECT * FROM expenses")
        row = 0
        while query.next():
            expense_id = query.value(0)
            date = query.value(1)
            category = query.value(2)
            amount = query.value(3)
            description = query.value(4)
            
            # add values to table
            self.table.insertRow(row)
            
            self.table.setItem(row, 0, QTableWidgetItem(str(expense_id)))
            self.table.setItem(row, 1, QTableWidgetItem(date))
            self.table.setItem(row, 2, QTableWidgetItem(category))
            self.table.setItem(row, 3, QTableWidgetItem(str(amount)))
            self.table.setItem(row, 4, QTableWidgetItem(description))
        
            row += 1
            
    
    def add_expense(self):
        # get current value from input_data
        date = self.date_box.date().toString("yyyy-MM-dd")
        category = self.dropdown.currentText()
        amount = self.amount.text()
        description = self.description.text()
        
        # create a new query to load to database
        query = QSqlQuery()
        query.prepare("""
                        INSERT INTO expenses (date, category, amount, description)
                        VALUES (?, ?, ?, ?)     
                      """)
        # load to database
        query.addBindValue(date)
        query.addBindValue(category)
        query.addBindValue(amount)
        query.addBindValue(description)
        query.exec_()
        
        # reset the input to default
        self.date_box.setDate(QDate.currentDate()) 
        self.dropdown.setCurrentIndex(0)
        self.amount.clear()
        self.description.clear()
        
        # load the new database
        self.load_table()
        
    
    def delete_expense(self):
        selected_row = self.table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "No Expense Chosen", "Please choose an expense to delete")
            return     
        
        # get column id
        expense_id = int(self.table.item(selected_row, 0).text()) 
        confirm_delete = QMessageBox.question(self, "Are yoou sure?","Delete Expense?", QMessageBox.Yes | QMessageBox.No)     
            
        if confirm_delete == QMessageBox.No:
            return
        
        query = QSqlQuery()
        query.prepare("DELETE FROM expenses WHERE id = ?")
        query.addBindValue(expense_id)
        query.exec_()
        
        self. load_table()
        

# create database
database = QSqlDatabase.addDatabase("QSQLITE")
database.setDatabaseName("expense.db")
if not database.open():
    QMessageBox.critical(None, "Error", "Could not open your Database")
    sys.exit(1)
    
    #set up the database
query = QSqlQuery()
query.exec_("""
                CREATE TABLE IF NOT EXISTS expenses (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        date TEXT,
                        category TEXT,
                        amount REAL,
                        description TEXT
                    )
            """)


# Run the app
if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = ExpenseApp()
    main_window.show()
    sys.exit(app.exec_())
        

        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        