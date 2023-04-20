import tkinter as tk
import pandas as pd
import os
import csv
from tkinter import filedialog, ttk
import subprocess

csv_file = "//Users/moshe/Documents/Progrmas/Python/geometryApp_git/Data/Gimatrea/gematria_values.csv"
gematria_methods_file = "/Users/moshe/Documents/Progrmas/Python/geometryApp_git/Data/Words/Dataword.csv"


# Load and save to CSV
def load_database(csv_path):
    if not os.path.exists(csv_path):
        with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=['word', 'Basic', 'Fill', 'Small', 'Values'])
            writer.writeheader()
    db = pd.read_csv(csv_path, encoding='utf-8', header=0)
    db.columns = ['word', 'Basic', 'Fill', 'Small', 'Values']
    print("Loaded database:", db)
    return db


def load_gematria_methods(csv_path):
    gematria_methods = {'normal': {}, 'fill': {}, 'small': {}, 'values': {}}
    with open(csv_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            gematria_methods['normal'][row['letter']] = int(row['normal_gematria'])
            gematria_methods['fill'][row['letter']] = int(row['fill_gematria'])
            gematria_methods['small'][row['letter']] = int(row['small_gematria'])
            gematria_methods['values'][row['letter']] = int(row['small_Values'])
    return gematria_methods

# Load the gematria methods from the file
gematria_methods = load_gematria_methods(gematria_methods_file)


def save_to_database(csv_path, row):
    os.makedirs(os.path.dirname(csv_path), exist_ok=True)
    with open(csv_path, 'a', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=['word', 'Basic', 'Fill', 'Small', 'Values'])
        writer.writerow(row)


# Calculate gematria
def calculate_gematria(word, gematria_values, method):
    return sum(gematria_values[method].get(c, 0) for c in word)


# GUI functions
def calculate_and_save():
    word = input_word.get()
    normal = calculate_gematria(word, gematria_methods, 'normal')
    fill = calculate_gematria(word, gematria_methods, 'fill')
    small = calculate_gematria(word, gematria_methods, 'small')
    values = calculate_gematria(word, gematria_methods, 'values')

    # Load the database
    db = load_database(csv_file)

    # Check if the word already exists in the database
    if not db[db['word'] == word].empty:
        print(f"Word '{word}' already exists in the database.")
    else:
        save_to_database(csv_file, {'word': word, 'Basic': normal, 'Fill': fill, 'Small': small, 'Values': values})

    result_normal.set(f"Normal: {normal}")
    result_fill.set(f"Fill: {fill}")
    result_small.set(f"Small: {small}")
    result_values.set(f"Values: {values}")

    find_similar_words(normal, fill, small, values)


def calculate_and_show():
    word = input_word.get()
    normal = calculate_gematria(word, gematria_methods, 'normal')
    fill = calculate_gematria(word, gematria_methods, 'fill')
    small = calculate_gematria(word, gematria_methods, 'small')
    values = calculate_gematria(word, gematria_methods, 'values')

    result_normal.set(f"Normal: {normal}")
    result_fill.set(f"Fill: {fill}")
    result_small.set(f"Small: {small}")
    result_values.set(f"Values: {values}")

    find_similar_words(normal, fill, small, values)


root = tk.Tk()
root.title("Gematria Calculator")

# Create the input_word StringVar object
input_word = tk.StringVar()

# Initialize the result StringVar objects after the root object
result_normal = tk.StringVar()
result_fill = tk.StringVar()
result_small = tk.StringVar()
result_values = tk.StringVar()

result_normal.set(f"Normal: {0}")
result_fill.set(f"Fill: {0}")
result_small.set(f"Small: {0}")
result_values.set(f"Values: {0}")

def find_similar_words(normal, fill, small, values):
    input_word_value = input_word.get()
    db = load_database(csv_file)

    similar_normal = db[db['Basic'] == normal]['word'].tolist()
    similar_fill = db[db['Fill'] == fill]['word'].tolist()
    similar_small = db[db['Small'] == small]['word'].tolist()
    similar_values = db[db['Values'] == values]['word'].tolist()

    listbox_normal.delete(0, tk.END)
    listbox_fill.delete(0, tk.END)
    listbox_small.delete(0, tk.END)
    listbox_values.delete(0, tk.END)

    for word in similar_normal:
        if word != input_word_value:
            listbox_normal.insert(tk.END, word)
    for word in similar_fill:
        if word != input_word_value:
            listbox_fill.insert(tk.END, word)
    for word in similar_small:
        if word != input_word_value:
            listbox_small.insert(tk.END, word)
    for word in similar_values:
        if word != input_word_value:
            listbox_values.insert(tk.END, word)

tk.Label(root, text="Enter Text:").grid(row=0, column=0)
tk.Entry(root, textvariable=input_word).grid(row=0, column=1)
tk.Button(root, text="calculate", command=calculate_and_save).grid(row=0, column=2)

tk.Label(root, textvariable=result_normal).grid(row=1, column=0)
tk.Label(root, textvariable=result_fill).grid(row=1, column=1)
tk.Label(root, textvariable=result_small).grid(row=1, column=2)
tk.Label(root, textvariable=result_values).grid(row=1, column=3)

listbox_normal = tk.Listbox(root, width=30, height=15)
listbox_fill = tk.Listbox(root, width=30, height=15)
listbox_small = tk.Listbox(root, width=30, height=15)
listbox_values = tk.Listbox(root, width=30, height=15)

listbox_normal.grid(row=2, column=0)
listbox_fill.grid(row=2, column=1)
listbox_small.grid(row=2, column=2)
listbox_values.grid(row=2, column=3)

tk.Button(root, text="Show Result", command=calculate_and_show).grid(row=5, column=0)

root.mainloop()





