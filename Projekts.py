import tkinter as tk
import json
from datetime import date

logs= tk.Tk()
logs.title("Dzimšanas datu bāze 2027")
logs.geometry("300x500")






logs.mainloop()



class Newborns_data:
    def __init__(self, name, lastname, sex, date2, person_code):
        self.name = name
        self.lastname = lastname
        self.sex = sex
        self.date2 = date2
        self.__person_code = str(person_code)

    def Get_personcode (self):
        return self.__person_code

    def Change_lastname (self):
        while new_lastname == True:
            new_lastname= str(input("Your new last name: ")).capitalize()

x= date(2090, 8, 13)
p1= ("Liene", "Miķele", "fem", x , 3004823453 )


print(x)
print(p1)

