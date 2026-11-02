"""Jaundzimušo reģistrācijas sistēmas lietojumprogramma."""

from datetime import datetime
import json
import tkinter as tk
from tkinter import messagebox

DATA_FILE = "datu_faili.json"


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
        """Setter uzstāda personas kodu un pārbauda tā garumu."""
        to_get_line_between = str(new_code).replace("-", "").strip()
        if len(to_get_line_between) == 11 and to_get_line_between.isdigit():
            self.__person_code = str(new_code)
        else:
            raise ValueError("Personas kodam jāsastāv no 11 cipariem!")


class Newborns_data(Persona):
    """Apakšklase jaundzimušajiem, kas manto no Persona."""

    def __init__(self, name, lastname, sex, year, month, day, person_code, date2=None):
        super().__init__(name, lastname, person_code)
        self.sex = sex
        if date2:
            self.date2 = date2
        else:
            self.date2 = datetime(int(year), int(month), int(day)).strftime("%x")

    def Dinamisks_aprekins(self):
        """Dinamisks aprēķins, kas nosaka PK tipu."""
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
        """Pārvērš objektu vārdnīcā priekš JSON."""
        return {
            "name": self.name,
            "lastname": self.lastname,
            "sex": self.sex,
            "person_code": self.Get_personcode(),
            "date2": self.date2,}


def saglabat_datus_faila():
    """Saglabā datus JSON failā."""
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        dati_saglabasanai = [child.to_dict() for child in newborn_list]
        json.dump(dati_saglabasanai, f, ensure_ascii=False, indent=4)


def ieladet_datus_no_faila():
    """Ielādē datus no JSON faila un atgriež sarakstu."""
    pagaidu_saraksts = []
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            saturs = f.read()
            if saturs:
                dati = json.loads(saturs)
                for x in dati:
                    atjaunots_berns = Newborns_data(
                        name=x["name"],
                        lastname=x["lastname"],
                        sex=x["sex"],
                        year=0,
                        month=0,
                        day=0,
                        person_code=x["person_code"],
                        date2=x["date2"],
                    )
                    pagaidu_saraksts.append(atjaunots_berns)
    except FileNotFoundError:
        pass
    except Exception as e:
        print("Kļūda ielādējot failu:", e)
    return pagaidu_saraksts



newborn_list = ieladet_datus_no_faila()


def registret_bernu():
    """Reģistrē jaunu bērnu sistēmā."""
    try:
        vards = entry_name.get()
        uzvards = entry_lastname.get()
        dzimums = sex_variants.get()
        gads = entry_year.get()
        menesis = entry_month.get()
        diena = entry_day.get()
        p_kods = entry_code.get()

        if not (vards and uzvards and gads and menesis and diena and p_kods):
            messagebox.showwarning("Kļūda", "Lūdzu, aizpildiet visus laukus!")
            return

        jaunais_mazulis = Newborns_data(vards, uzvards, dzimums, gads, menesis, diena, p_kods, date2=None)
        jaunais_mazulis.Set_personcode(p_kods)

        newborn_list.append(jaunais_mazulis)
        saglabat_datus_faila()

        tips = jaunais_mazulis.Dinamisks_aprekins()
        messagebox.showinfo(
            "Success", 
            f"Reģistrēts: {jaunais_mazulis.name} {jaunais_mazulis.lastname} ({tips})\nDati saglabāti diskā!"
        )
        notirit_laukus()
    except ValueError as ve:
        messagebox.showerror("Kļūda ievadē", str(ve))
    except Exception:
        messagebox.showerror("Kļūda", "Gadam, mēnesim un dienai jābūt skaitļiem!")


def mekle_un_labo_bernadatus():
    """Meklē bērnu pēc personas koda un labo datus."""
    meklejamais_kods = entry_search_code.get()
    jaunais_vards = entry_new_name.get()
    jaunais_uzvards = entry_new_lastname.get()

    if not meklejamais_kods:
        messagebox.showwarning("Kļūda", "Ievadiet personas kodu meklēšanai!")
        return

    atrastais_berns = None
    for berns in newborn_list:
        if berns.Get_personcode() == meklejamais_kods:
            atrastais_berns = berns
            break

    if atrastais_berns:
        if jaunais_vards:
            atrastais_berns.Change_name(jaunais_vards)
        if jaunais_uzvards:
            atrastais_berns.Change_lastname(jaunais_uzvards)

        saglabat_datus_faila()

        messagebox.showinfo(
            "Atjaunināts",
            f"Dati mainīti un saglabāti failā! Tagad: {atrastais_berns.name} {atrastais_berns.lastname}",
        )

        entry_search_code.delete(0, tk.END)
        entry_new_name.delete(0, tk.END)
        entry_new_lastname.delete(0, tk.END)
    else:
        messagebox.showerror("Nav atrasts", "Bērns ar šādu personas kodu netika atrasts!")


def notirit_laukus():
    """Notīra visus reģistrācijas ievades laukus."""
    entry_name.delete(0, tk.END)
    entry_lastname.delete(0, tk.END)
    entry_year.delete(0, tk.END)
    entry_month.delete(0, tk.END)
    entry_day.delete(0, tk.END)
    entry_code.delete(0, tk.END)


logs = tk.Tk()
logs.title("Jaundzimušo Reģistrs")
logs.geometry("500x550")


tk.Label(logs, text="REĢISTRĀCIJA").grid(row=0, column=0, columnspan=2, pady=10)

tk.Label(logs, text="Vārds:").grid(row=1, column=0, sticky="w", padx=10)
entry_name = tk.Entry(logs)
entry_name.grid(row=1, column=1, pady=3)

tk.Label(logs, text="Uzvārds:").grid(row=2, column=0, sticky="w", padx=10)
entry_lastname = tk.Entry(logs)
entry_lastname.grid(row=2, column=1, pady=3)

tk.Label(logs, text="Dzimums:").grid(row=3, column=0, sticky="w", padx=10)
sex_variants = tk.StringVar(value="fem")
frame_sex = tk.Frame(logs)
frame_sex.grid(row=3, column=1, sticky="w", pady=3)
tk.Radiobutton(frame_sex, text="Sieviete (F)", variable=sex_variants, value="fem").pack(side="left")
tk.Radiobutton(frame_sex, text="Vīrietis (M)", variable=sex_variants, value="male").pack(side="left")

tk.Label(logs, text="Gads (YYYY):").grid(row=4, column=0, sticky="w", padx=10)
entry_year = tk.Entry(logs)
entry_year.grid(row=4, column=1, sticky="w", pady=3)

tk.Label(logs, text="Mēnesis (MM):").grid(row=5, column=0, sticky="w", padx=10)
entry_month = tk.Entry(logs)
entry_month.grid(row=5, column=1, sticky="w", pady=3)

tk.Label(logs, text="Diena (DD):").grid(row=6, column=0, sticky="w", padx=10)
entry_day = tk.Entry(logs)
entry_day.grid(row=6, column=1, sticky="w", pady=3)

tk.Label(logs, text="Personas kods (11 cipari):").grid(row=7, column=0, sticky="w", padx=10)
entry_code = tk.Entry(logs)
entry_code.grid(row=7, column=1, pady=3)

tk.Button(logs, text="Reģistrēt jaundzimušo", command=registret_bernu).grid(row=8, column=0, columnspan=2, pady=15)


tk.Label(logs, text="LABOT DATUS (pēc Personas koda)").grid(row=9, column=0, columnspan=2, pady=10)
         
tk.Label(logs, text="Meklēt Personas Kodu:").grid(row=10, column=0, sticky="w", padx=10)
entry_search_code = tk.Entry(logs)
entry_search_code.grid(row=10, column=1, pady=3)

tk.Label(logs, text="Jaunais Vārds:").grid(row=11, column=0, sticky="w", padx=10)
entry_new_name = tk.Entry(logs)
entry_new_name.grid(row=11, column=1, pady=3)

tk.Label(logs, text="Jaunais Uzvārds:").grid(row=12, column=0, sticky="w", padx=10)
entry_new_lastname = tk.Entry(logs)
entry_new_lastname.grid(row=12, column=1, pady=3)

tk.Button(logs, text="Meklēt un Saglabāt izmaiņas", command=mekle_un_labo_bernadatus).grid(row=13, column=0, columnspan=2, pady=15)

logs.mainloop()

