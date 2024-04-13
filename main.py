# This is a sample Python script.
import random
import string
import sys

from PyQt6.QtWidgets import QDialog, QApplication

from layout import Ui_Dialog





class MyForm(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.ui.generate.clicked.connect(self.generate)
        self.ui.easter.clicked.connect(self.easterClicked)
        self.ui.password.textChanged.connect(self.strenghtOfPassword)

        #Zasobnik nakow
        self.smallChars = [l for l in string.ascii_lowercase]
        self.capitalChars = [l for l in string.ascii_uppercase]
        self.numbers = [str(i) for i in range(0, 10)]
        self.specialChars = [l for l in string.punctuation]

    def generate(self):
        lenght = self.ui.lenght.text()
        type = self.ui.passwordType.currentText()
        password = ""
        if type == "Pin":
            for i in range(int(lenght)):
                password += str(random.randint(0, 9))
        elif self.ui.word.isChecked():
            words = self.readDict('odm.txt')
            while len(password) < int(lenght):
                password += random.choice(words)
        else:
            elements = [self.smallChars]
            if self.ui.capitalLater.isChecked():
                elements.append(self.capitalChars)
            if self.ui.numbers.isChecked():
                elements.append(self.numbers)
            if self.ui.specialChar.isChecked():
                elements.append(self.specialChars)
            for i in range(int(lenght)):
                type = random.randint(0, len(elements) - 1)
                password += elements[type][random.randint(0, len(elements[type]) - 1)]
            if self.ui.easter.isChecked() and len(password) >= 5:
                max_index = len(password) - 6
                start_index = random.randint(0, max_index)
                new_password = ''
                easter = "Zając"
                for i in range(len(password)):
                    if start_index <= i < start_index+5:
                        new_password += easter[i - start_index]
                    else:
                        new_password += password[i]
                password = new_password
            if self.checkPasswordIsValid(password) == False:
                self.generate()
            else:
                self.ui.generatedPassword.setText(password)
        self.ui.generatedPassword.setText(password)

    def readDict(self, path):
        words = []
        with open(path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            for line in lines:
                line = line.split(',')[0]
                line = line.replace('\n', '')
                if(len(line) > 2) and line.find(' ') == -1:
                    words.append(line)
        return words

    def easterClicked(self):
        if self.ui.easter.isChecked():
            self.ui.numbers.setChecked(False)
            self.ui.specialChar.setChecked(False)
            self.ui.capitalLater.setChecked(False)
            self.ui.word.setChecked(False)
            self.ui.numbers.setDisabled(True)
            self.ui.specialChar.setDisabled(True)
            self.ui.capitalLater.setDisabled(True)
            self.ui.word.setDisabled(True)
        else:
            self.ui.numbers.setDisabled(False)
            self.ui.specialChar.setDisabled(False)
            self.ui.capitalLater.setDisabled(False)
            self.ui.word.setDisabled(False)

    def checkPasswordIsValid(self, password):
        who_is_valid = [False, False, False, False]
        all_options = [self.smallChars, self.capitalChars, self.numbers, self.specialChars]
        who_is_checked = [True, self.ui.capitalLater.isChecked(), self.ui.numbers.isChecked(), self.ui.specialChar.isChecked()]
        for char in password:
            for which in range(len(all_options)):
                if who_is_checked[which]:
                    if char in all_options[which]:
                        who_is_valid[which] = True
        if who_is_valid[0] == who_is_checked[0] and who_is_valid[1] == who_is_checked[1] and who_is_valid[2] == who_is_checked[2] and who_is_valid[3] == who_is_checked[3]:
            return True
        else:
            return False

    def strenghtOfPassword(self):
        password = self.ui.password.text()
        powerBar = self.ui.powerbar
        powerBar.setMaximum(100)
        powerBar.setValue(0)
        points = 0
        has_any_char = [False, False, False, False]
        all_options = [self.smallChars, self.capitalChars, self.numbers, self.specialChars]
        for char in password:
            for tabChars in range(len(all_options)):
                if char in all_options[tabChars]:
                    has_any_char[tabChars] = True
        for has_in_pass in has_any_char:
            if has_in_pass:
                points += 20
        if 0 < len(password) <= 3:
            points += 5
        elif 4 <= len(password) <= 6:
            points += 10
        elif 7 <= len(password) <= 8:
            points += 15
        elif len(password) > 8:
            points += 20

        powerBar.setValue(points)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = MyForm()
    form.show()
    sys.exit(app.exec())


