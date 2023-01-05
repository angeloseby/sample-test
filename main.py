from PyQt5.QtWidgets import *
from PyQt5 import uic

import smtplib
from email import encoders
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart

class MailSenderGUI(QMainWindow):
    
    def __init__(self):
        super(MailSenderGUI,self).__init__()
        uic.loadUi("mailsender.ui",self)
        self.show()
        
        self.loginButton.clicked.connect(self.login)
        self.attachButton.clicked.connect(self.attach)
        self.sendButton.clicked.connect(self.send)
        self.helpButton.clicked.connect(self.help)
        
    def login(self):
        try:
            self.server = smtplib.SMTP(self.smtpserver.text(),self.port.text())
            self.server.ehlo()
            self.server.starttls()
            self.server.ehlo()
            print(self.email.text(),self.password.text())
            self.server.login(self.email.text(),self.password.text())
            
            self.email.setEnabled(False)
            self.password.setEnabled(False)
            self.smtpserver.setEnabled(False)
            self.port.setEnabled(False)
            self.loginButton.setEnabled(False)
            
            self.to.setEnabled(True)
            self.subject.setEnabled(True)
            self.body.setEnabled(True)
            self.attachButton.setEnabled(True)
            self.sendButton.setEnabled(True)
            
            self.msg = MIMEMultipart()
            
        except smtplib.SMTPAuthenticationError:
            message_box = QMessageBox()
            message_box.setText("Invalid Login Credentials")
            message_box.exec()
        except :
            message_box = QMessageBox()
            message_box.setText("Login Failed")
            message_box.exec()
            
            
        
    def attach(self):
        options = QFileDialog.Options()
        filenames,_ = QFileDialog.getOpenFileNames(self,"Open File","","All Files (*.*)",options=options)
        if filenames != filenames:
            for filename in filenames:
                attatchment = open(filename,'rb')
                
                filename = filename[filename.rfind("/")+1] 
                
                p = MIMEBase('application','octet-stream')
                p.set_payload(attatchment.read())
                encoders.encode_base64(p)
                p.add_header("Content-Disposition",f"attachment; filename={filename}")
                self.msg.attach(p)
                
                if not self.attatchments_label.text().endswith(":"):
                    self.attatchments_label.setText(self.attatchments_label.text()+",")
                self.attatchments_label.setText(self.attatchments_label.text()+filename)
                
        
    def send(self):
        dialog = QMessageBox()
        dialog.setText("Do you want to send this mail?")
        dialog.addButton(QPushButton("Yes"),QMessageBox.YesRole) #0
        dialog.addButton(QPushButton("No"),QMessageBox.NoRole) #1
        
        if dialog.exec_()==0:
            try:
                self.msg['From'] = self.email.text()
                self.msg['To'] = self.to.text()
                self.msg['Subject'] = self.subject.text()
                self.msg.attach(MIMEText(self.body.toPlainText(),'plain'))
                text = self.msg.as_string()
                self.server.sendmail(self.email.text(),self.to.text(),text)
                
                message_box = QMessageBox()
                message_box.setText("Email Send")
                message_box.exec()
            except:
                message_box = QMessageBox()
                message_box.setText("Mail not send")
                message_box.exec()
    
    def help(self):
        pass
        
        
        
app = QApplication([])
window = MailSenderGUI()
app.exec_()