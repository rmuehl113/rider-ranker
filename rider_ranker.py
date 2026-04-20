# Supermotocross Rider Ranker
# Author: Robert Muehleisen
# Date: 04/19/2026
# Description: A CLI-based supercross and motocross rider database and ranker. 
# Enter rider stats, view individual profiles, and rank riders across multiple categories
# Saves user entries to CSV file. Loads previous CSV file to keep an updated list of riders.

import csv
import os

def int_check(prompt):
    """
    Helper function to provide error handling for integer input
    Prints error message if user enters non-integer
    Loop until valid integer is entered
    """
    while True:
        try:
            user_input = input(prompt)
            user_int = int(user_input)
            break
        except ValueError:
            print("\nInvalid input. Please enter a valid number.")
    return user_int

class Rider:
    """
    Sets up base rider class
    Parameters: Name, Number, Nationality and Years pro
    Prints info with header
    """
    def __init__(self, name, number, nation, years_pro):
        self.name = name
        self.number = number
        self.nation = nation
        self.years_pro = years_pro

    def print_info(self):
        print("\n======================")
        print(f"{self.name}".center(22))
        print("======================")
        print(f"Number: {self.number}\nNationality: {self.nation}\nYears Pro: {self.years_pro}")
        print("======================")

class SXRider(Rider):
    """
    Sets up Supercross rider with Rider inheritied
    Parameters: Name, Number, Nationality, Years pro, SX titles and SX wins
    Returns: Total titles and wins
    Prints info with header
    """
    def __init__(self, name, number, nation, years_pro, sx_titles, sx_wins):
        Rider.__init__(self, name, number, nation, years_pro)  # inherits attributes from Rider class
        self.sx_titles = sx_titles
        self.sx_wins = sx_wins

    def total_titles(self):
        return self.sx_titles
    
    def total_wins(self):
        return self.sx_wins

    def print_info(self):
        super().print_info()  # inherits print method from Rider class
        print(f"Supercross Titles: {self.sx_titles}")
        print(f"Supercross Wins: {self.sx_wins}")
        print("======================")

class MXRider(Rider):
    """
    Sets up Motocross rider with Rider inherited
    Parameters: Name, Number, Nationality, Years pro, MX titles and MX wins
    Returns: Total titles and wins
    Prints info with header
    """
    def __init__(self, name, number, nation, years_pro, mx_titles, mx_wins):
        Rider.__init__(self, name, number, nation, years_pro)  # inherits attributes from Rider class
        self.mx_titles = mx_titles
        self.mx_wins = mx_wins

    def total_titles(self):
        return self.mx_titles
    
    def total_wins(self):
        return self.mx_wins

    def print_info(self):
        super().print_info()  # inherits print method from Rider class
        print(f"Motocross Titles: {self.mx_titles}")
        print(f"Motocross Wins: {self.mx_wins}")
        print("======================")

class SMXRider(SXRider, MXRider):
    """
    Sets up SMX rider with SX rider and MX rider inheritied
    Parameters: Name, Number, Nationality, Years pro, SX titles, SX wins, MX titles and MX wins
    Returns: Total titles and wins 
    Prints info with header
    """
    def __init__(self, name, number, nation, years_pro, sx_titles, sx_wins, mx_titles, mx_wins):
        SXRider.__init__(self, name, number, nation, years_pro, sx_titles, sx_wins)  # inherits attributes from SXRider class
        MXRider.__init__(self, name, number, nation, years_pro, mx_titles, mx_wins)  # inherits attributes from MXRider class
    
    def total_titles(self):
        return self.sx_titles + self.mx_titles
    
    def total_wins(self):
        return self.sx_wins + self.mx_wins
    
    def print_info(self):
        super().print_info()  # inherits print method from both MX and SX classes
        print(f"Total Titles: {self.total_titles()}")
        print(f"Total Wins: {self.total_wins()}")
        print("======================")

def load_riders():
    """
    Loads Rider data from riders.csv into a list
    Returns an empty list if the file does not exist
    """
    riders = []
    if os.path.exists("riders.csv"):
        with open("riders.csv") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row["type"] == "SX":
                    riders.append(SXRider(row["name"], row["number"], row["nation"], int(row["years_pro"]), int(row["sx_titles"]), int(row["sx_wins"])))
                elif row["type"] == "MX":
                    riders.append(MXRider(row["name"], row["number"], row["nation"], int(row["years_pro"]), int(row["mx_titles"]), int(row["mx_wins"])))
                elif row["type"] == "SMX":
                    riders.append(SMXRider(row["name"], row["number"], row["nation"], int(row["years_pro"]), int(row["sx_titles"]), int(row["sx_wins"]), 
                                           int(row["mx_titles"]), int(row["mx_wins"])))
        print("File loaded succesfully")
    else:
        print("No file found. Starting fresh.")
    return riders

def save_riders(riders):
    """
    Saves current rider data to riders.csv
    Parameters: riders list
    """
    with open("riders.csv", "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=["type", "name", "number", "nation", "years_pro", "sx_titles", "sx_wins", "mx_titles", "mx_wins"])
        writer.writeheader()
        for row in riders:
            if isinstance(row, SMXRider):
                writer.writerow({"type": "SMX", "name": row.name, "number": row.number, "nation": row.nation, "years_pro": row.years_pro, "sx_titles": row.sx_titles, 
                                 "sx_wins": row.sx_wins, "mx_titles": row.mx_titles, "mx_wins": row.mx_wins})
            elif isinstance(row, SXRider):
                writer.writerow({"type": "SX", "name": row.name, "number": row.number, "nation": row.nation, "years_pro": row.years_pro, "sx_titles": row.sx_titles, 
                                 "sx_wins": row.sx_wins, "mx_titles": 0, "mx_wins": 0})
            elif isinstance(row, MXRider):
                writer.writerow({"type": "MX", "name": row.name, "number": row.number, "nation": row.nation, "years_pro": row.years_pro, "sx_titles": 0, 
                                 "sx_wins": 0, "mx_titles": row.mx_titles, "mx_wins": row.mx_wins})

def display_menu(riders):
    """
    Displays rider count and menu options to user
    Allows user to chose which action to perform
    Parameters: riders list
    """
    print(f"\nRiders in database: {len(riders)}")
    print("Menu Options:\n1. View Rider Stats\n2. Rank Riders\n3. Add Rider\n4. Edit Rider\n5. Remove Rider\n6. Quit")
                
def view_riders(riders):
    """
    Prints all rider data
    Parameters: riders list
    """
    if not riders:
        print("No Rider Data!")
        return
    
    print("\n0. Back")
    for num, rider in enumerate(riders, 1):
        print(f"{num}. {rider.name}")
    while True:
        user_input = int_check("\nChoose a Rider: ")
        if user_input == 0:
            return
        if user_input > len(riders):
            print("\nInvalid input. Please enter a valid number.")
            continue
        riders[user_input - 1].print_info()
        break

def rank_riders(riders):
    """
    Ranking Riders by user-picked category
    Parameters: riders list
    Prints result of comparison
    """
    if not riders:
        print("No Rider Data!")
        return
    
    while True:
        print("\nRank Options: \n1. Total Titles\n2. Total Wins\n3. SX Titles\n4. SX Wins\n5. MX Titles\n6. MX Wins")
        user_input = input("Rank by: ")
    
        if user_input == "1":
            sorted_riders = sorted(riders, key=lambda r: r.total_titles(), reverse=True)  # sorted() with a lambda sorts the list by each rider's total_titles() method, reverse=True (highest first)
            break
        elif user_input == "2":
            sorted_riders = sorted(riders, key=lambda r: r.total_wins(), reverse=True)  # sorted() with a lambda sorts the list by each rider's total_wins() method, reverse=True (highest first)
            break
        elif user_input == "3":
            sorted_riders = sorted(riders, key=lambda r: r.sx_titles if hasattr(r, 'sx_titles') else 0, reverse=True)  # sorted() with a lambda sorts the list by each rider's sx_titles, 0 if none, reverse=True (highest first)
            break
        elif user_input == "4":
            sorted_riders = sorted(riders, key=lambda r: r.sx_wins if hasattr(r, 'sx_wins') else 0, reverse=True)  # sorted() with a lambda sorts the list by each rider's sx_wins, 0 if none, reverse=True (highest first)
            break
        elif user_input == "5":
            sorted_riders = sorted(riders, key=lambda r: r.mx_titles if hasattr(r, 'mx_titles') else 0, reverse=True)  # sorted() with a lambda sorts the list by each rider's mx_titles, 0 if none, reverse=True (highest first)
            break
        elif user_input == "6":
            sorted_riders = sorted(riders, key=lambda r: r.mx_wins if hasattr(r, 'mx_wins') else 0, reverse=True)  # sorted() with a lambda sorts the list by each rider's mx_wins, 0 if none, reverse=True (highest first)
            break
        else:
            print("\nInvalid input. Please select 1-6.")

    for rank, rider in enumerate(sorted_riders, 1):
        print()
        print(f"RANK #{rank}".center(20))
        print("====================")
        print(f"{rider.name}")
        if user_input == "1":
            print(f"Total Titles: {rider.total_titles()}")
        elif user_input == "2":
            print(f"Total Wins: {rider.total_wins()}")
        elif user_input == "3":
            print(f"Supercross Titles: {rider.sx_titles if hasattr(rider, 'sx_titles') else 0}")
        elif user_input == "4":
            print(f"Supercross Wins: {rider.sx_wins if hasattr(rider, 'sx_wins') else 0}")
        elif user_input == "5":
            print(f"Motocross Titles: {rider.mx_titles if hasattr(rider, 'mx_titles') else 0}")
        elif user_input == "6":
            print(f"Motocross Wins: {rider.mx_wins if hasattr(rider, 'mx_wins') else 0}")

def add_rider(riders):
    """
    Allows user to add rider into program
    Parameters: riders list
    Saves Rider to CSV after adding
    """
    while True:
        print("\nRider Types:\n1. SMX\n2. SX\n3. MX")
        user_input = input("\nSelect Rider Type: ")

        if user_input == "1":
            name = input("Enter Rider Name: ")
            number = input("Enter Rider Number: ")
            nation = input("Enter Rider Nation: ")
            years_pro = int_check("Enter Number of Years Pro: ")
            sx_titles = int_check("Enter Number of Supercross Titles: ")
            sx_wins = int_check("Enter Number of Supercross Wins: ")
            mx_titles = int_check("Enter Number of Motocross Titles: ")
            mx_wins = int_check("Enter Number of Motocross Wins: ")
                
            riders.append(SMXRider(name, number, nation, years_pro, sx_titles, sx_wins, mx_titles, mx_wins))  # add all user inputs to SMXRider
            save_riders(riders)
            print(f"\n{name} info saved succesfully!")
            break

        elif user_input == "2":
            name = input("Enter Rider Name: ")
            number = input("Enter Rider Number: ")
            nation = input("Enter Rider Nation: ")
            years_pro = int_check("Enter Number of Years Pro: ")
            sx_titles = int_check("Enter Number of Supercross Titles: ")
            sx_wins = int_check("Enter Number of Supercross Wins: ")

            riders.append(SXRider(name, number, nation, years_pro, sx_titles, sx_wins))  # add all user inputs to SXRider
            save_riders(riders)
            print(f"\n{name} info saved succesfully!")
            break

        elif user_input == "3":
            name = input("Enter Rider Name: ")
            number = input("Enter Rider Number: ")
            nation = input("Enter Rider Nation: ")
            years_pro = int_check("Enter Number of Years Pro: ")
            mx_titles = int_check("Enter Number of Motocross Titles: ")
            mx_wins = int_check("Enter Number of Motocross Wins: ")

            riders.append(MXRider(name, number, nation, years_pro, mx_titles, mx_wins))  # add all user inputs to MXRider
            save_riders(riders)
            print(f"\n{name} info saved succesfully!")
            break

        else:
            print("\nInvalid input. Please select 1-3.")

def edit_rider(riders):
    """
    Allows user to edit stats of a saved rider
    Parameters: riders list
    """
    if not riders:
        print("No Rider Data!")
        return
    
    print("\n0. Back")
    for num, rider in enumerate(riders, 1):
        print(f"{num}. {rider.name}")
    while True:
        user_input = int_check("\nChoose Rider to Edit: ")
        if user_input == 0:
            return
        if user_input > len(riders):
            print("\nInvalid input. Please enter a valid number.")
            continue
        rider_choice = riders[user_input - 1]
        break

    if isinstance(rider_choice, SMXRider):
        print(f"\n{rider_choice.name}")
        print("1. Years Pro\n2. Supercross Titles\n3. Supercross Wins\n4. Motocross Titles\n5. Motocross Wins")
        while True:
            stat_choice = input("\nChoose Stat to Edit:")
            if stat_choice == "1":
                rider_choice.years_pro = int_check("\nYears Pro: ")      
                break
            elif stat_choice == "2":
                rider_choice.sx_titles = int_check("\nSupercross Titles: ")
                break
            elif stat_choice == "3":
                rider_choice.sx_wins = int_check("\nSupercross Wins: ")
                break
            elif stat_choice == "4":
                rider_choice.mx_titles = int_check("\nMotocross Titles: ")
                break
            elif stat_choice == "5":
                rider_choice.mx_wins = int_check("\nMotocross Wins: ")
                break
            else:
                print("\nInvalid input. Please select 1-5.")
        save_riders(riders)
        print("\nStat Updated!")

    elif isinstance(rider_choice, SXRider):
        print(f"\n{rider_choice.name}")
        print("1. Years Pro\n2. Supercross Titles\n3. Supercross Wins")
        while True:
            stat_choice = input("\nChoose Stat to Edit:")
            if stat_choice == "1":
                rider_choice.years_pro = int_check("\nYears Pro: ")      
                break
            elif stat_choice == "2":
                rider_choice.sx_titles = int_check("\nSupercross Titles: ")
                break
            elif stat_choice == "3":
                rider_choice.sx_wins = int_check("\nSupercross Wins: ")
                break
            else:
                print("\nInvalid input. Please select 1-3")
        save_riders(riders)
        print("\nStat Updated!")

    elif isinstance(rider_choice, MXRider):
        print(f"\n{rider_choice.name}")
        print("1. Years Pro\n2. Motocross Titles\n3. Motocross Wins")
        while True:
            stat_choice = input("\nChoose Stat to Edit:")
            if stat_choice == "1":
                rider_choice.years_pro = int_check("\nYears Pro: ")      
                break
            elif stat_choice == "2":
                rider_choice.mx_titles = int_check("\nMotocross Titles: ")
                break
            elif stat_choice == "3":
                rider_choice.mx_wins = int_check("\nMotocross Wins: ")
                break
            else:
                print("\nInvalid input. Please select 1-3.")
        save_riders(riders)
        print("\nStat Updated!")

def remove_rider(riders):
    """
    Allows user to delete entire Rider from program
    Deletes entry from CSV and saves
    Parameters: riders list
    """
    if not riders:
        print("No Rider Data!")
        return
    
    print("\n0. Back")
    for num, rider in enumerate(riders, 1):
        print(f"{num}. {rider.name}")
    while True:
        user_input = int_check("\nChoose Rider to Delete: ")
        if user_input == 0:
            return
        if user_input > len(riders):
            print("\nInvalid input. Please enter a valid number.")
            continue
        riders.pop(user_input - 1)
        break
    save_riders(riders)
    print("Rider deleted. File updated.")

def main():
    """
    Main loop
    Initialized Rider data, shows menu to user, processes user input
    Calls appropriate function based on user input
    """
    print("\nWelcome to Rider Ranker!")
    riders = load_riders()

    while True:
        display_menu(riders)
        user_input = input("\nSelect an option (1-6): ")

        if user_input == "1":
            view_riders(riders)
        elif user_input == "2":
            rank_riders(riders)
        elif user_input == "3":
            add_rider(riders)
        elif user_input == "4":
            edit_rider(riders)
        elif user_input == "5":
            remove_rider(riders)
        elif user_input == "6":
            print("\nExiting program. Data saved.")
            break
        else:
            print("\nInvalid option. Please select 1-6.")

if __name__ == "__main__":
    main()