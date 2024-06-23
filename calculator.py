import sys
import json
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QInputDialog

class BadCalculator(QWidget):
    def __init__(self):
        super().__init__()
        self.results_file = 'results.json'
        self.results = self.load_results()
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle('Bad Calculator')
        self.setGeometry(100, 100, 300, 200)

        self.layout = QVBoxLayout()

        self.display = QLineEdit(self)
        self.layout.addWidget(self.display)

        self.buttons = [
            '7', '8', '9', '/',
            '4', '5', '6', '*',
            '1', '2', '3', '-',
            '0', '.', '=', '+'
        ]

        self.button_layout = QVBoxLayout()
        self.create_buttons()
        self.layout.addLayout(self.button_layout)
        
        self.setLayout(self.layout)
    
    def create_buttons(self):
        for i in range(0, len(self.buttons), 4):
            row = QHBoxLayout()
            for j in range(4):
                button = QPushButton(self.buttons[i+j])
                button.clicked.connect(self.on_button_click)
                row.addWidget(button)
            self.button_layout.addLayout(row)
    
    def on_button_click(self):
        sender = self.sender().text()
        if sender == '=':
            self.calculate()
        else:
            self.display.setText(self.display.text() + sender)
    
    def calculate(self):
        expression = self.display.text()
        result = self.evaluate_expression(expression)
        self.display.setText(result)
    
    def evaluate_expression(self, expression):
        if expression in self.results:
            return self.results[expression]
        elif expression == "2+2":
            return "4"
        else:
            return self.ask_user_for_result(expression)
    
    def ask_user_for_result(self, expression):
        result, ok = QInputDialog.getText(self, 'Unknown Calculation', f'I don\'t know how to calculate {expression}. Please provide the result:')
        if ok:
            self.results[expression] = result
            self.save_results()
            return result
        else:
            return ""

    def load_results(self):
        try:
            with open(self.results_file, 'r') as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def save_results(self):
        with open(self.results_file, 'w') as file:
            json.dump(self.results, file, indent=4)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    calculator = BadCalculator()
    calculator.show()
    sys.exit(app.exec_())
