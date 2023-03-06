import sys
import time
import re
import random
from PyQt5 import QtCore
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import *
import cgitb
from email.message import EmailMessage
import ssl
import smtplib
import mysql.connector as con

cgitb.enable(format = 'text')


class DBConnection(QDialog):
    def __init__(self):
        super(DBConnection, self).__init__()

        loadUi('connectdb.ui', self)
        self.show()
        self.push.clicked.connect(self.DBConnect)

    def DBConnect(self):
        try:
            db = con.connect(
                host='localhost',
                user='127.0.0.1',
                passwd='',
                db='ohioacademy'
            )

            QMessageBox.about(self, 'connection', 'Database successfully connected')

        except con.Error as e:
            QMessageBox.about(self, 'connect', 'failed to connect')
            sys.exit(1)










class RegisterWindow(QDialog):
    def __init__(self):
        super().__init__()
        loadUi('register.ui', self)
        self.show()
        self.otp = self.generateOTP()
        # self.button = self.findChild(QPushButton, 'regbtn_sub')
        self.regbtn_sub.clicked.connect(self.emailVerification)

    def emailVerification(self):
        fn = self.firstname_in.text()
        ln = self.lastname_in.text()
        mdn = self.middlename_in.text()
        sex_m = self.male_radio.text()
        sex_f = self.female_radio.text()
        em = self.email_in.text()
        dep = self.department_in.text()
        aca = self.schoolsession_in.text()
        lev = self.selection_combo.currentText()
        pw = self.password_in.text()
        cnpw = self.confirmpass_in.text()

        time.sleep(2)
        print(em)
        pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if re.fullmatch(pattern, em):
            QMessageBox.information(self, 'Registration Progress', 'A 5-digit OTP code has been sent to you, please verify your email')
            time.sleep(1)
            self.sendMail()
            time.sleep(1)
            self.verify_otp = OTPWindow(self.otp)
            self.verify_otp.show()
        else:
            QMessageBox.information(self, 'Invalid Email', 'Please type in a valid email address.')
            self.email_in.setText('')
            print('no match')

        time.sleep(0.5)

    def generateOTP(self):
        self.otp_num = ''
        for x in range(5):
            u = random.randint(1, 9)
            self.otp_num += str(u)
        return self.otp_num


    def sendMail(self):

    #email sender and receiver initializing

        email_sender = 'theolam6@gmail.com'
        email_password = 'sacriznaxcsixlzc'
        email_receiver =  self.email_in.text()

    #email formation

        Subject = 'Verify Your Login'
        Body = f"""Hello, your OTP code is {self.otp}.\n If you did 
                    not request it, please ignore this email."""

    #create an instance for the email body

        email = EmailMessage()
        email['From'] = email_sender
        email['To'] = email_receiver
        email['Subject'] = Subject
        email.set_content(Body)

    #create context using smtplib & ssl libraries

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context)as smtp:
                smtp.login(email_sender, email_password)
                smtp.sendmail(email_sender, email_receiver, email.as_string())


        time.sleep(2)


    def movetoDB(self):
        fn = self.firstname_in.text()
        ln = self.lastname_in.text()
        mdn = self.middlename_in.text()
        sex_m = self.male_radio.text()
        sex_f = self.female_radio.text()
        em = self.email_in.text()
        dep = self.department_in.text()
        aca = self.schoolsession_in.text()
        lev = self.selection_combo.currentText()
        pw = self.password_in.text()
        cnpw = self.confirmpass_in.text()




class OTPWindow(QDialog):
    def __init__(self, f):
        super(OTPWindow, self).__init__()
        self.f = f
        loadUi('otpbox.ui', self)
        self.show()
        self.regObj = RegisterWindow()
        self.otpbtn.clicked.connect(self.checkOTP)



    def checkOTP(self):
        otpline = self.otp_line.text()

        if otpline == self.f:
            print(otpline)
            QMessageBox.information(self, 'Registration Progress', 'Registration Successful!')
            time.sleep(1.5)
            self.regObj.movetoDB()

        else:
            QMessageBox.about(self, 'Invalid OTP', ' Check the code sent to your email and try Again')

















class LogInWindow(QDialog):
    def __init__(self):
        super(LogInWindow, self).__init__()
        loadUi('login.ui', self)
        self.show()


class Mainwindow(QDialog):
    def __init__(self):
        super(Mainwindow, self).__init__()

        loadUi('home.ui', self)
        self.show()
        self.setMaximumSize(QtCore.QSize(1200, 800))
        self.setMinimumSize(QtCore.QSize(1200, 800))

        self.button = self.findChild(QPushButton, 'home_regbtn')
        self.button.clicked.connect(self.on_register)

        self.button = self.findChild(QPushButton, 'home_regbtn_2')
        self.button.clicked.connect(self.on_login)

    def on_register(self):
        self.w = RegisterWindow()
        self.w.show()

    def on_login(self):
        self.x = LogInWindow()
        self.x.show()



app = QApplication(sys.argv)
widget = DBConnection()
app.exec_()

try:
    sys.exit(app.exec_())
except:
    print('Exiting')





