import os 
import sys
import pandas as pd
from PyQt5.QtWidgets import (
    QApplication,QMainWindow,QWidget,QVBoxLayout,QLabel,QHBoxLayout,QLineEdit,QPushButton,QTableWidget,QTableWidgetItem,QHeaderView,QMessageBox,QInputDialog,QFileDialog
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
import sqlite3



# import matplotlib.pyplot as plot
# Database Path
DATABASE_PATH = os.path.join("Database","inventory.db")

def Database():
    os.makedirs(os.path.dirname(DATABASE_PATH),exist_ok=True)
    conn = sqlite3.connect(DATABASE_PATH)
    cur = conn.cursor()

    # Inventory Table
    cur.execute('''CREATE TABLE IF NOT EXISTS inventory (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                category TEXT,
                quantity INTEGER NOT NULL,
                purchase_price REAL,
                selling_price REAL
                ) ''')
    
    # cur.execute('''CREATE TABLE IF NOT EXISTS sales (
    #             product_id INTEGER,
    #             quantity_sold INTEGER,
    #             Sale_price REAL,
    #             Sale_date TEXT,
    #             FOREIGN KEY (product_id) REFERENCES inventory (id)''')
    conn.commit()
    conn.close()

class InventoryApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initui()

    def initui(self):
        self.setWindowTitle("Inventory Admin Panel")
        self.setGeometry(100,100,1200,800)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        # This is our Title label 
        self.Inventory_Label = QLabel("Inventory Management System")
        self.Inventory_Label.setFont(QFont("Arial",28,QFont.Bold))
        self.Inventory_Label.setAlignment(Qt.AlignCenter)
        self.Inventory_Label.setStyleSheet("color:grey;margin-bottom:20px;")
        self.layout.addWidget(self.Inventory_Label)

        # Dashboard Layout:
        self.dashboard_layout = QHBoxLayout()
        
        self.total_items = QLabel("Total Items: 0")
        self.total_items.setFont(QFont("Arial",14))
        self.total_items.setStyleSheet("color:#a83260;")

        self.total_categories = QLabel("Total Categories: 0")
        self.total_categories.setFont(QFont("Arial",14))
        self.total_categories.setStyleSheet("color:#a83260;")

        self.profit = QLabel("Total Profit: ₹0.00")
        self.profit.setFont(QFont("Arial",14))
        self.profit.setStyleSheet("color:#a83260;")

        self.stock = QLabel("Total Stock: ₹0.00")
        self.stock.setFont(QFont("Arial",14))
        self.stock.setStyleSheet("color:#a83260;")

        self.dashboard_layout.addWidget(self.total_items)
        self.dashboard_layout.addWidget(self.total_categories)
        self.dashboard_layout.addWidget(self.profit)
        self.dashboard_layout.addWidget(self.stock)
        self.layout.addLayout(self.dashboard_layout)

        # Input Fields
        self.id_input = QLineEdit()
        self.id_input.setPlaceholderText("Product Id(Optional) : ")
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Product Name : ")
        self.category = QLineEdit()
        self.category.setPlaceholderText("Product Category : ")
        self.quantity = QLineEdit()
        self.quantity.setPlaceholderText("Product Quantity : ")
        self.purchase_price = QLineEdit()
        self.purchase_price.setPlaceholderText("Product Purchase Price : ")
        self.selling_price = QLineEdit()
        self.selling_price.setPlaceholderText("Product Selling Price : ")

        input_labels = [self.id_input,self.name_input,self.category,self.quantity,self.purchase_price,self.selling_price]

        for fields in input_labels:
            fields.setStyleSheet("""
                        QLineEdit {
                                 padding:8px;
                                 border:1px solid #ddd;
                                 border-radius:5px;
                                 background-color:#ecf0f1;
                                 }
                            """)
        # Buttons
        self.add_button = self.create_button("Add",self.add)
        self.delete_button = self.create_button("Delete",self.delete)
        self.update_button = self.create_button("Update",self.update)
        self.import_data_button = self.create_button("Import CSV/Excel",self.import_csv_excel)
        self.clear_all_button = self.create_button("Clear All",self.clear_all)
        self.refresh_button = self.create_button("Refresh",self.load_data)
        # self.plot_data = self.create_button("Plot Sales Data",self.plot_sales_data)
        # self.sales = self.create_button("Manage Sales",self.manage_sales)

        #  Table Widget
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(
            ["Product Id","Name","Category","Quantity","Purchase Price","Selling Price"]
        )
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.verticalHeader().setVisible(False)
        self.table.setStyleSheet("""
                    QTableWidget {
                                 background-color:#f9f9f9;
                                 border: 1px solid #ddd;
                                 gridline-color:#ccc;
                                 }
                    QHeaderView::section {
                                 background-color:#2c3e50;
                                 color:white;
                                 padding:8px;
                                 font-weight:bold;
                                 }
                    QTableWidget::item {
                                 padding:5px;
                                 }
                    """)
        # Layout Setup
        input_layout = QHBoxLayout()
        input_layout.addWidget(self.id_input)
        input_layout.addWidget(self.name_input)
        input_layout.addWidget(self.category)
        input_layout.addWidget(self.quantity)
        input_layout.addWidget(self.purchase_price)
        input_layout.addWidget(self.selling_price)
        input_layout.addWidget(self.add_button)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.update_button)
        button_layout.addWidget(self.delete_button)
        button_layout.addWidget(self.clear_all_button)
        button_layout.addWidget(self.refresh_button)
        button_layout.addWidget(self.import_data_button)
        # button_layout.addWidget(self.sales)
        # button_layout.addWidget(self.plot_data)

        self.layout.addLayout(input_layout)
        self.layout.addWidget(self.table)
        self.layout.addLayout(button_layout)

        # Load Initial Data
        self.load_data()
    def add(self):
        id_product = self.id_input.text()
        name = self.name_input.text()
        category = self.category.text()
        quantity = self.quantity.text()
        purchase_price = self.purchase_price.text()
        selling_price = self.selling_price.text()

        if not id_product or not name or not category or not quantity or not purchase_price or not selling_price:
            QMessageBox.warning(self,"Input Error","All Input Fields Are Required!")
            return
        
        try:
            id_product = int(id_product)
            quantity = int(quantity)
            purchase_price,selling_price = float(purchase_price),float(selling_price)
        except ValueError:
            QMessageBox.warning(self,"Field Error","Please Enter Valid Numeric Values for  Id, Quantity, purchase price, selling price")
            return
        
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        cursor.execute('''INSERT INTO inventory (id,name,category,quantity,purchase_price,selling_price) VALUES (?,?,?,?,?,?)''',(id_product,name,category,quantity,purchase_price,selling_price))

        conn.commit()
        conn.close()        

        QMessageBox.information(self,"Success","Item Added Successfully")
        
        self.load_data()

    def load_data(self):
        try:
            conn = sqlite3.connect(DATABASE_PATH)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM inventory")
            rows = cursor.fetchall()
            conn.close()

            self.table.setRowCount(0) # Clear Existing Rows

            for row in rows:
                row_position = self.table.rowCount()
                self.table.insertRow(row_position)

                for col,data in enumerate(row):
                    self.table.setItem(row_position,col,QTableWidgetItem(str(data)))
            
            total_items = len(rows)
            total_categories = {row[2] for row in rows}
            profit = sum([(row[3]*row[5]) for row in rows])
            stock = sum([(row[3] * row[4]) for row in rows])
            self.total_items.setText(f"Total Items: {total_items}")
            self.total_categories.setText(f"Total Categories: {len(total_categories)}")
            self.profit.setText(f"Total Profit: ₹{profit:.2f}")
            self.stock.setText(f"Total Stock: ₹{stock:.2f}")
        except Exception as e:
            QMessageBox.critical(self,"Error",f"An Error Occured: {e}")

    def delete(self):
        try:
            selected_row = self.table.currentRow()
            if selected_row == -1:
                QMessageBox.warning(self,"Selection Error","No Row Is Selected To Delete")
                return
            item_id = int(self.table.item(selected_row,0).text())
            conn = sqlite3.connect(DATABASE_PATH)
            cursor = conn.cursor()
            cursor.execute("DELETE FROM inventory WHERE id = ?",(item_id,))
            conn.commit()
            conn.close()

            QMessageBox.information(self,"Success","Item Deleted Successfully!")
            self.load_data()
        except Exception as e:
            QMessageBox.critical(self,"Error",f"An Error Occured: {e}")

    def update(self):
        item_id,ok = QInputDialog.getText(self,"Product Id","Enter Product Id")
        if not ok:
            return
        item_name,ok = QInputDialog.getText(self,"Product Name","Enter Product Name")
        if not ok:
            return
        item_category,ok = QInputDialog.getText(self,"Product Category","Enter Product Category")
        if not ok:
            return
        item_quantity,ok = QInputDialog.getText(self,"Product Quantity","Enter Product Quantity")
        if not ok:
            return
        item_purchase,ok = QInputDialog.getText(self,"Product Purchase Price","Enter Product Purchase Price")
        if not ok:
            return
        item_selling,ok = QInputDialog.getText(self,"Product Selling Price","Enter Product Selling Price")
        if not ok:
            return
        
        if not item_id or not item_name or not item_category or not item_quantity or not item_purchase or not item_selling:
            QMessageBox.warning(self,"Field Error","All Input Fields Are Required!")
            return
        
        try:
            item_id = int(item_id)
            item_quantity = int(item_quantity)
            item_purchase = float(item_purchase)
            item_selling = float(item_selling)
        except ValueError:
            QMessageBox.warning(self,"Data Error","Please Input Correct Numerical Values for The Fields Id, Quantity, Purchase Price, Selling Price")
            return
        
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        cursor.execute("UPDATE inventory SET name = ?,category = ?, quantity = ?, purchase_price = ?, selling_price = ? WHERE id = ?",(item_name,item_category,item_quantity,item_purchase,item_selling,item_id))
        conn.commit()
        conn.close()
        self.load_data()
        
    def import_csv_excel(self):
        file_path,_ = QFileDialog.getOpenFileName(self,"Open File","","CSV Files (*.csv);;Excel Files (*.xlsx)")
        if not file_path:
            return
        
        try:
            if file_path.endswith(".csv"):
                data = pd.read_csv(file_path)
            elif file_path.endswith(".xlsx"):
                data = pd.read_excel(file_path)
            else:
                raise ValueError("Unsupported File Format!")
            conn = sqlite3.connect(DATABASE_PATH)
            data.to_sql("inventory",conn, if_exists="append",index=False)
            conn.close()
            self.load_data()
            QMessageBox.information(self,"Success","Data Imported Successfully!")
        except Exception as e:
            QMessageBox.critical(self,"Error",f"An Error Occured: {e}")

    def clear_all(self):
        self.table.setRowCount(0)

        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        cursor.execute("""DELETE FROM inventory""")
        conn.commit()
        conn.close()

    def create_button(self,text,callback):
        button = QPushButton(text)
        button.clicked.connect(callback)
        button.setStyleSheet("""
                    QPushButton {
                             background-color:red;
                             color:white;
                             padding:10px;
                             border-radius:5px;
                             font-size:14px;
                             }
                    QPushButton:Hover {
                             background:#b33243;
                             }
                    """)
        return button

if __name__ == "__main__":
    Database()
    app = QApplication(sys.argv)
    app.setStyleSheet("""
                QWidget {
                      font-family:Arial;
                      font-size:19px;
                      }
        """)
    window = InventoryApp()
    window.show()
    sys.exit(app.exec_())    

