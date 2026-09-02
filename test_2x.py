import sys
import random
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget,
    QHBoxLayout, QLabel, QLineEdit
)
from martypy import Marty


class MartyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.my_marty = None

        self.initUI()

    
    def initUI(self):
        self.setWindowTitle("Interface Marty")

        self.lbl_etat = QLabel("Déconnecté")
        self.lbl_etat.setStyleSheet("color: red; font-weight: bold;")

        self.txt_ip = QLineEdit()
        self.txt_ip.setPlaceholderText("IP du robot")

        self.btn_connexion = QPushButton("Connecter")
        self.btn_connexion.clicked.connect(self.connecter_robot)

        layout_top = QHBoxLayout()
        layout_top.addWidget(self.lbl_etat)
        layout_top.addWidget(self.txt_ip)
        layout_top.addWidget(self.btn_connexion)

        

        layout_vertical = QVBoxLayout()
        
        layout_vertical.setSpacing(12)
        self.battery_label = QLabel("Batterie : Inconnue")
        layout_top.addWidget(self.battery_label)
        self.btn_battery = QPushButton("Vérifier")
        self.btn_battery.clicked.connect(self.check_battery)
        self.btn_battery.setEnabled(False)
        layout_top.addWidget(self.btn_battery)
        self.btn_get_name = QPushButton("Lire nom")
        self.btn_get_name.clicked.connect(self.get_robot_name)
        self.btn_get_name.setEnabled(False)
        layout_top.addWidget(self.btn_get_name)
        self.txt_new_name = QLineEdit()
        self.txt_new_name.setPlaceholderText("Nouveau nom")
        self.txt_new_name.setEnabled(False)
        layout_top.addWidget(self.txt_new_name)
        self.btn_set_name = QPushButton("Changer nom")
        self.btn_set_name.clicked.connect(self.set_robot_name)
        self.btn_set_name.setEnabled(False)
        layout_top.addWidget(self.btn_set_name)
        
        

        main_layout = QVBoxLayout()
        main_layout.addLayout(layout_top)
        main_layout.addLayout(layout_vertical)
        

        widget_central = QWidget()
        widget_central.setLayout(main_layout)
        self.setCentralWidget(widget_central)

    def get_robot_name(self):
        if self.my_marty is not None:
            try:
                name = self.my_marty.get_name()
                print("Nom du robot  :", name)
            except Exception as e:
                print("Erreur lecture nom :", e)
        else:
            print("Robot non connecté.")
        #Cette fonction utilise get_name() de Marty
    def set_robot_name(self):
        if self.my_marty is not None:
            new_name = self.txt_new_name.text().strip()
            if not new_name:
                print("Nom vide.")
                return
            try:
                self.my_marty.set_name(new_name)
                print("Nom changé :", new_name)
            except Exception as e:
                print("Erreur  changement nom :", e)
        else:
            print("Robot non connecté.")

    def connecter_robot(self):
        ip = self.txt_ip.text().strip()
        QApplication.processEvents()
        if not ip:
            print("Erreur : aucune IP saisie.")
            return

        try:
            self.my_marty = Marty("wifi", ip)
        except Exception as e:
            print("Erreur : connexion impossible :", e)
            return
        self.connected = True

        self.lbl_etat.setText("Connecté")
        self.lbl_etat.setStyleSheet("color: green; font-weight: bold;")
        self.btn_connexion.setText("Déconnexion")
        self.btn_connexion.clicked.disconnect()
        self.btn_connexion.clicked.connect(self.deconnecter_robot)
        self.btn_battery.setEnabled(True)
        self.btn_get_name.setEnabled(True)
        self.btn_set_name.setEnabled(True)
        self.txt_new_name.setEnabled(True)

    def deconnecter_robot(self):
        if self.my_marty:
            self.my_marty.close()

        self.my_marty = None
        self.controller = None

        self.lbl_etat.setText("Déconnecté")
        self.lbl_etat.setStyleSheet("color: red; font-weight: bold;")
        self.btn_connexion.setText("Connexion")
        self.btn_connexion.clicked.disconnect()
        self.btn_connexion.clicked.connect(self.connecter_robot)
        self.btn_battery.setEnabled(False)
        self.btn_get_name.setEnabled(False)
        self.btn_set_name.setEnabled(False)
        self.txt_new_name.setEnabled(False)

    def check_battery(self):
        if self.my_marty is not None:
            try:
                batt_percent = self.my_marty.get_battery_remaining()
                self.battery_label.setText(f"Batterie : {batt_percent}%")
            except Exception as e:
                self.battery_label.setText(f"Erreur batterie : {e}")
        else:
            self.battery_label.setText("Robot connecté.")

    def couleur_aleatoire():
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
        return (r, g, b)
    
    def set_eyes_random(marty):
        r, g, b = couleurs_aleatoire()
        marty.set_eye_color(r, g, b)

    def move_forward(marty):
        set_eyes_random(marty)
        marty.walk(5)

    def move_backward(marty):
        set_eyes_random(marty)
        marty.walk(-5)
    
    def move_left(marty):
        set_eyes_random(marty)
        marty.turn(-30) #tourne à gauche

    def move_right(marty):
        set_eyes_random(marty)
        marty.trun(30) # tourne à gauche

if __name__ == '__main__':
    app = QApplication(sys.argv)
    fenetre = MartyApp()
    fenetre.show()
    sys.exit(app.exec())