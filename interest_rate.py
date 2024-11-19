# Interest Rate Calculator App

# import modules
import sys
import os
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtWidgets import (QApplication, 
                            QWidget, QLabel, QLineEdit, 
                            QPushButton, QVBoxLayout, QTreeView,
                            QHBoxLayout, QComboBox, QMainWindow,  
                            QMessageBox, QFileDialog, QCheckBox)
from PyQt5.QtSql import QSqlDatabase, QSqlQuery
from PyQt5.QtGui import QStandardItem, QStandardItemModel

import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas


class InterestRateApp(QMainWindow):
    def __init__(self):
        super(InterestRateApp, self).__init__()
        
        # main windows objects and settings
        self.setWindowTitle("Interest Rate Calculator App")
        self.resize(750, 600)
        
        main_window = QWidget()
        
         # create objects for/on display screen
        self.rate_text = QLabel("Interest Rate")
        self.rate_input = QLineEdit()
        
        self.initial_text = QLabel("Initial Investment")
        self.initial_input = QLineEdit()
        
        self.years_text = QLabel("Years of Investment")
        self.years_input = QLineEdit()  
        
        
        
        # create tree view
        self.model = QStandardItemModel()
        self.tree_view = QTreeView()
        self.tree_view.setModel(self.model)

        self.calc_button = QPushButton("Calculate")
        self.clear_button = QPushButton("Clear")
        self.save_button = QPushButton("Save")
        #self.figure = QLabel("Loading chart")
        
        self.dark_mode = QCheckBox("Dark Mode")
        
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        
        # set app layout
        self.main_layout = QVBoxLayout()
        
        self.row1 = QHBoxLayout()
        self.row2 = QHBoxLayout()
        
        self.col1 = QVBoxLayout()
        self.col2 = QVBoxLayout()

        # add widgets
        self.row1.addWidget(self.rate_text)
        self.row1.addWidget(self.rate_input)
        self.row1.addWidget(self.initial_text)
        self.row1.addWidget(self.initial_input)
        self.row1.addWidget(self.years_text)
        self.row1.addWidget(self.years_input)
        self.row1.addWidget(self.dark_mode)

        self.col1.addWidget(self.tree_view)
        self.col1.addWidget(self.calc_button)
        self.col1.addWidget(self.clear_button)
        self.col1.addWidget(self.save_button)
        
        #self.col2.addWidget(self.figure)
        self.col2.addWidget(self.canvas)
        
        self.row2.addLayout(self.col1, 30)
        self.row2.addLayout(self.col2, 80)
        
        self.main_layout.addLayout(self.row1)
        self.main_layout.addLayout(self.row2)
        
        main_window.setLayout(self.main_layout)
        self.setCentralWidget(main_window)
        
        self.calc_button.clicked.connect(self.calc_interest)
        self.clear_button.clicked.connect(self.reset)
        self.save_button.clicked.connect(self.save_data)
        self.dark_mode.stateChanged.connect(self.toggle_mode)
        
        self.apply_styles()
     
    
# set dark mode
    def apply_styles(self):
        # set dark modes
            self.setStyleSheet(    
                """
                   FinanceApp {
                       background-color: #f0f0f0;
                   }            
                   QLabel, QLineEdit, QPushButton {
                       background-color: #f8f8f8;
                   }
                   QTreeView {
                       background-color: #ffffff;
                   }
                
                """
            )
            if self.dark_mode.isChecked():
                self.setStyleSheet(
                    """
                    FinanceApp {
                        background-color: #222222
                    }            
                    QLabel, QLineEdit, QPushButton {
                        background-color: #333333;
                        color: #eeeeee;
                    }
                    QTreeView {
                        background-color: #444444;
                        color: #eeeeee;
                    }
                    
                    """
                )
                
    def toggle_mode(self):
        self.apply_styles()
            
        
    def calc_interest(self):
        initial_investment = None
        # get input
        try: 
            interest_rate = float(self.rate_input.text())
            initial_investment = float(self.initial_input.text())
            num_years = int(self.years_input.text())
            
        except ValueError:
            QMessageBox.warning(self, "Error", "Invalid input, enter a number")

        self.model.clear()
        
        self.model.setHorizonalHeaderLabels(["Year", "Total"])

        # calculate interest
        total = initial_investment
        for year in range(1, num_years+1):
            total += total * (interest_rate/100)
            item_year = QStandardItem(str(year))
            item_total = QStandardItem("{:.2f}".format(total))
            self.model.appendRow([item_year, item_total])
            
        #update chat with input data 
        self.figure.clear()
        plt.style.use('seaborn')
        ax = self.figure.subplots()
        years = list(range(1, num_years+1))
        totals = [initial_investment * (1 + interest_rate/100)**year for year in years]
        
        ax.plot(years, totals)
        ax.set_title("Interest Chart")
        ax.set_xlabel("Year")
        ax.set_ylabel("Total")
        self.canvas.draw()
        
        
    # save data
    def save_data(self):
        # get current working direectory
        dir_path = QFileDialog.getExistingDirectory(self, "Select Directory")
        # create file and folder
        if dir_path:
            folder_path = os.path.join(dir_path, "Saved Folder")
            os.makedirs(folder_path, exist_ok=True)
            
            file_path = os.path.join(folder_path, "results.csv")
            with open(file_path, "w") as file:
                file.write("Year, Total\n")
                for row in range(self.model.rowCount()):
                    year = self.model.index(row, 0).data()
                    total = self.model.index(row, 1).data()
                    file.write("{},{}".format(year, total))
                    
            plt.savefig("chart.png")
            
            QMessageBox.information(self, "Save Results", "Results saved to the folder")
        else:
            QMessageBox.warning(self, "Save Results", "The directory selected")     
            
            
    def reset(self):
        self.rate_input.clear()
        self.initial_input.clear()
        self.years_input.clear()
        self.model.clear()
        
        self.figure.clear()
        self.canvas.draw()
        


# Run the app
if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = InterestRateApp()
    main_window.show()
    sys.exit(app.exec_())
        



        


