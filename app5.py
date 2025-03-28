#!/usr/bin/env python3
import sqlite3
import os
from datetime import datetime

DB_NAME = "personal_tracker.db"


def create_tables():
    """Create tables for Finance, Fitness, Faith, Friendship, and Family."""
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()

        # Finance table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS finance (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                amount REAL NOT NULL,
                category TEXT,
                notes TEXT
            )
        """)

        # Fitness table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS fitness (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                exercise_type TEXT NOT NULL,
                duration_minutes INTEGER,
                notes TEXT
            )
        """)

        # Faith table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS faith (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                reflection TEXT
            )
        """)

        # Friendship table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS friendship (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                last_contacted TEXT,
                notes TEXT
            )
        """)

        # Family table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS family (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                relationship TEXT,
                notes TEXT
            )
        """)

        conn.commit()


def add_finance_record():
    """Add a new Finance record."""
    date_str = input("Enter date (YYYY-MM-DD) [default: today]: ")
    if not date_str:
        date_str = datetime.now().strftime("%Y-%m-%d")

    amount = float(input("Enter amount (e.g., -200 for expense, 500 for income): "))
    category = input("Enter category (e.g., 'Food', 'Salary', 'Rent'): ")
    notes = input("Enter any notes (optional): ")

    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO finance (date, amount, category, notes)
            VALUES (?, ?, ?, ?)
        """, (date_str, amount, category, notes))
        conn.commit()

    print("Finance record added successfully.\n")


def view_finance_records():
    """View all Finance records."""
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, date, amount, category, notes FROM finance ORDER BY date DESC")
        rows = cursor.fetchall()

        if rows:
            print("ID | Date       | Amount    | Category   | Notes")
            print("---+------------+-----------+------------+-------------------")
            for row in rows:
                print(f"{row[0]:2} | {row[1]} | {row[2]:9.2f} | {row[3]:10} | {row[4]}")
        else:
            print("No Finance records found.")
    print()


def add_fitness_record():
    """Add a new Fitness record."""
    date_str = input("Enter date (YYYY-MM-DD) [default: today]: ")
    if not date_str:
        date_str = datetime.now().strftime("%Y-%m-%d")

    exercise_type = input("Enter exercise type (e.g., Running, Weightlifting): ")
    duration = input("Enter duration in minutes (optional): ")
    duration = int(duration) if duration else None
    notes = input("Enter notes (optional): ")

    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO fitness (date, exercise_type, duration_minutes, notes)
            VALUES (?, ?, ?, ?)
        """, (date_str, exercise_type, duration, notes))
        conn.commit()

    print("Fitness record added successfully.\n")


def view_fitness_records():
    """View all Fitness records."""
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, date, exercise_type, duration_minutes, notes FROM fitness ORDER BY date DESC")
        rows = cursor.fetchall()

        if rows:
            print("ID | Date       | Exercise Type    | Duration | Notes")
            print("---+------------+------------------+----------+-----------------")
            for row in rows:
                duration_str = str(row[3]) if row[3] is not None else "N/A"
                print(f"{row[0]:2} | {row[1]} | {row[2]:16} | {duration_str:8} | {row[4]}")
        else:
            print("No Fitness records found.")
    print()


def add_faith_record():
    """Add a new Faith record."""
    date_str = input("Enter date (YYYY-MM-DD) [default: today]: ")
    if not date_str:
        date_str = datetime.now().strftime("%Y-%m-%d")

    reflection = input("Write your reflection, prayer, or note: ")

    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO faith (date, reflection)
            VALUES (?, ?)
        """, (date_str, reflection))
        conn.commit()

    print("Faith record added successfully.\n")


def view_faith_records():
    """View all Faith records."""
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, date, reflection FROM faith ORDER BY date DESC")
        rows = cursor.fetchall()

        if rows:
            print("ID | Date       | Reflection/Note")
            print("---+------------+---------------------------")
            for row in rows:
                print(f"{row[0]:2} | {row[1]} | {row[2]}")
        else:
            print("No Faith records found.")
    print()


def add_friendship_record():
    """Add a new Friendship record."""
    name = input("Enter the friend’s name: ")
    last_contacted = input("Enter last contacted date (YYYY-MM-DD) [leave blank if unknown]: ")
    notes = input("Enter notes (optional): ")

    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO friendship (name, last_contacted, notes)
            VALUES (?, ?, ?)
        """, (name, last_contacted, notes))
        conn.commit()

    print("Friendship record added successfully.\n")


def view_friendship_records():
    """View all Friendship records."""
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, last_contacted, notes FROM friendship ORDER BY name ASC")
        rows = cursor.fetchall()

        if rows:
            print("ID | Name            | Last Contacted | Notes")
            print("---+-----------------+---------------+---------------------")
            for row in rows:
                last_contacted_str = row[2] if row[2] else "N/A"
                print(f"{row[0]:2} | {row[1]:15} | {last_contacted_str:13} | {row[3]}")
        else:
            print("No Friendship records found.")
    print()


def add_family_record():
    """Add a new Family record."""
    name = input("Enter family member’s name: ")
    relationship = input("Enter relationship (e.g., Father, Sister, Uncle): ")
    notes = input("Enter notes (optional): ")

    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO family (name, relationship, notes)
            VALUES (?, ?, ?)
        """, (name, relationship, notes))
        conn.commit()

    print("Family record added successfully.\n")


def view_family_records():
    """View all Family records."""
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, relationship, notes FROM family ORDER BY name ASC")
        rows = cursor.fetchall()

        if rows:
            print("ID | Name            | Relationship  | Notes")
            print("---+-----------------+---------------+--------------------")
            for row in rows:
                print(f"{row[0]:2} | {row[1]:15} | {row[2]:13} | {row[3]}")
        else:
            print("No Family records found.")
    print()


def finance_menu():
    """Menu for Finance operations."""
    while True:
        print("\n--- Finance Menu ---")
        print("[1] Add Finance Record")
        print("[2] View Finance Records")
        print("[0] Back to Main Menu")
        choice = input("Select an option: ")

        if choice == "1":
            add_finance_record()
        elif choice == "2":
            view_finance_records()
        elif choice == "0":
            break
        else:
            print("Invalid choice. Please try again.")


def fitness_menu():
    """Menu for Fitness operations."""
    while True:
        print("\n--- Fitness Menu ---")
        print("[1] Add Fitness Record")
        print("[2] View Fitness Records")
        print("[0] Back to Main Menu")
        choice = input("Select an option: ")

        if choice == "1":
            add_fitness_record()
        elif choice == "2":
            view_fitness_records()
        elif choice == "0":
            break
        else:
            print("Invalid choice. Please try again.")


def faith_menu():
    """Menu for Faith operations."""
    while True:
        print("\n--- Faith Menu ---")
        print("[1] Add Faith Record")
        print("[2] View Faith Records")
        print("[0] Back to Main Menu")
        choice = input("Select an option: ")

        if choice == "1":
            add_faith_record()
        elif choice == "2":
            view_faith_records()
        elif choice == "0":
            break
        else:
            print("Invalid choice. Please try again.")


def friendship_menu():
    """Menu for Friendship operations."""
    while True:
        print("\n--- Friendship Menu ---")
        print("[1] Add Friendship Record")
        print("[2] View Friendship Records")
        print("[0] Back to Main Menu")
        choice = input("Select an option: ")

        if choice == "1":
            add_friendship_record()
        elif choice == "2":
            view_friendship_records()
        elif choice == "0":
            break
        else:
            print("Invalid choice. Please try again.")


def family_menu():
    """Menu for Family operations."""
    while True:
        print("\n--- Family Menu ---")
        print("[1] Add Family Record")
        print("[2] View Family Records")
        print("[0] Back to Main Menu")
        choice = input("Select an option: ")

        if choice == "1":
            add_family_record()
        elif choice == "2":
            view_family_records()
        elif choice == "0":
            break
        else:
            print("Invalid choice. Please try again.")


def main():
    """Main function to run the personal tracker application."""
    # Create tables if they don't exist
    create_tables()

    while True:
        print("========== Personal Tracker ==========")
        print("[1] Finance")
        print("[2] Fitness")
        print("[3] Faith")
        print("[4] Friendship")
        print("[5] Family")
        print("[0] Exit")
        choice = input("Select a section: ")

        if choice == "1":
            finance_menu()
        elif choice == "2":
            fitness_menu()
        elif choice == "3":
            faith_menu()
        elif choice == "4":
            friendship_menu()
        elif choice == "5":
            family_menu()
        elif choice == "0":
            print("Exiting application. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.\n")


if __name__ == "__main__":
    main()
