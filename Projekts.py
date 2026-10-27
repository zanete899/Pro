import tkinter as tk
import json

logs= tk.Tk()
logs.title("Dzimšanas datu bāze 2027")
logs.geometry("300x500")






logs.mainloop()



class Newborns_data:
    def __init__(self, name, lastname, sex, date, person_code):
        self.name = name
        self.lastname = lastname
        self.sex = sex
        self.date = date
        self.__person_code = person_code

    def Get_personcode (self):
        return self.__person_code

    def Change_lastname (self):
        new_lastname= input("Your new last name: ")
        if new_lastname



