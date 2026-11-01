"""Jaundzimušo reģistrācijas sistēmas lietojumprogramma."""

from datetime import datetime
import json
import tkinter as tk
from tkinter import messagebox

DATA_FILE = "datu_faili.json"
newborn_list = []


class Persona:
    """Bāzes klase personai ar privātu mainīgo."""

    def __init__(self, name, lastname, person_code):
        self.name = str(name).capitalize()
        self.lastname = str(lastname).capitalize()
        self.__person_code = str(person_code)

    def Get_personcode(self):
        """Getter metode vērtības nolasīšanai."""
        return self.__person_code

    def Set_personcode(self, new_code):
        """Setter metode jauna koda maiņai ar pārbaudi (skolotājas prasība)."""
        clean_code = str(new_code).replace("-", "").strip()
        if len(clean_code) == 11 and clean_code.isdigit():
            self.__person_code = str(new_code)
        else:
            raise ValueError("Personas kodam jāsastāv no 11 cipariem!")


class Newborns_data(Persona):
    """Apakšklase jaundzimušajiem, kas manto no Persona."""

    def __init__(self, name, lastname, sex, year, month, day, person_code, date2=None,):
        super().__init__(name, lastname, person_code)
        self.sex = sex
        if date2:
            self.date2 = date2
        else:
            self.date2 = datetime(int(year), int(month), int(day)).strftime("%x")

    def Dinamisks_aprekins(self):
        """Dinamisks aprēķins, kas piekļūst datiem caur getter metodi."""
        kods = self.Get_personcode()
        if kods.startswith("3"):
            return "Jaunā tipa PK"
        return "Vecā tipa PK"

    def Change_lastname(self, new_lastname):
        """Maina uzvārdu."""
        self.lastname = str(new_lastname).capitalize()

    def Change_name(self, new_name):
        """Maina vārdu."""
        self.name = str(new_name).capitalize()

    def to_dict(self):
        """Pārvērš vārdnīcā."""
        return {
            "name": self.name,
            "lastname": self.lastname,
            "sex": self.sex,
            "person_code": self.Get_personcode(),
            "date2": self.date2,
        }


def saglabat_datus_faila():
    """Saglabā datus JSON failā."""
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        dati_saglabasanai = [child.to_dict() for child in newborn_list]
        json.dump(dati_saglabasanai, f, ensure_ascii=False, indent=4)


def ieladet_datus_no_faila():
    """Ielādē datus no JSON failā."""
    global newborn_list
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            saturs = f.read()
            if saturs:
                dati = json.loads(saturs)
                newborn_list = []
                for b in dati:
                    atjaunots_berns = Newborns_data(
                        name=b["name"],
                        lastname=b["lastname"],
                        sex=b["sex"],
                        year=0,
                        month=0,
                        day=0,
                        person_code=b["person_code"],
                        date2=b["date2"],
                    )
                    newborn_list.append(atjaunots_berns)
    except FileNotFoundError:
        newborn_list = []
    except Exception as e:
        print("Kļūda ielādējot failu:", e)


ieladet_datus_no_faila()
