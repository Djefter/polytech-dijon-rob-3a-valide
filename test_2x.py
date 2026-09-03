import sys
import random
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget,
    QHBoxLayout, QLabel, QLineEdit, QGridLayout
)
from martypy import Marty


class MartyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.my_marty = None
        self.initUI()

    
    def initUI(self):
        self.setWindowTitle("Interface Marty")

        # --- Connexion / IP / État ---
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

        # --- Batterie / Nom ---
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

        # --- Layout principal ---
        main_layout = QVBoxLayout()
        main_layout.addLayout(layout_top)

        # --- Boutons directionnels ---
        direction_layout = QGridLayout()

        btn_up = QPushButton("HAUT")
        btn_down = QPushButton("BAS")
        btn_left = QPushButton("GAUCHE")
        btn_right = QPushButton("DROITE")
        btn_stop = QPushButton("STOP")

        btn_up.clicked.connect(lambda: self.move_forward())
        btn_down.clicked.connect(lambda: self.move_backward())
        btn_left.clicked.connect(lambda: self.move_left())
        btn_right.clicked.connect(lambda: self.move_right())
        btn_stop.clicked.connect(lambda: self.stop_robot())

        direction_layout.addWidget(btn_up, 0, 1)
        direction_layout.addWidget(btn_left, 1, 0)
        direction_layout.addWidget(btn_stop, 1, 1)
        direction_layout.addWidget(btn_right, 1, 2)
        direction_layout.addWidget(btn_down, 2, 1)

        main_layout.addLayout(direction_layout)

        # --- Widget central ---
        widget_central = QWidget()
        widget_central.setLayout(main_layout)
        self.setCentralWidget(widget_central)

    # --- Fonctions Marty ---
    def get_robot_name(self):
        if self.my_marty:
            try:
                name = self.my_marty.get_name()
                print("Nom du robot :", name)
            except Exception as e:
                print("Erreur lecture nom :", e)
        else:
            print("Robot non connecté.")

    def set_robot_name(self):
        if self.my_marty:
            new_name = self.txt_new_name.text().strip()
            if not new_name:
                print("Nom vide.")
                return
            try:
                self.my_marty.set_name(new_name)
                print("Nom changé :", new_name)
            except Exception as e:
                print("Erreur changement nom :", e)
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
        if self.my_marty:
            try:
                batt_percent = self.my_marty.get_battery_remaining()
                self.battery_label.setText(f"Batterie : {batt_percent}%")
            except Exception as e:
                self.battery_label.setText(f"Erreur batterie : {e}")
        else:
            self.battery_label.setText("Robot non connecté.")

    # --- Fonctions de mouvement ---
    def couleur_aleatoire(self):
        return (
            random.randint(0, 255),
            random.randint(0, 255),
            random.randint(0, 255)
        )

    def set_eyes_random(self):
        if self.my_marty:
            r, g, b = self.couleur_aleatoire()
            self.my_marty.set_eye_color(r, g, b)

    def move_forward(self):
        if self.my_marty:
            self.set_eyes_random()
            self.my_marty.walk(5)

    def move_backward(self):
        if self.my_marty:
            self.set_eyes_random()
            self.my_marty.walk(-5)

    def move_left(self):
        if self.my_marty:
            self.set_eyes_random()
            self.my_marty.turn(-30)

    def move_right(self):
        if self.my_marty:
            self.set_eyes_random()
            self.my_marty.turn(30)

    def stop_robot(self):
        if self.my_marty:
            self.my_marty.stop()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    fenetre = MartyApp()
    fenetre.show()
    sys.exit(app.exec())
