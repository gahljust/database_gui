import tkinter as tk
from tkinter import ttk
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import json

def get_all_tables():
    """Get all table names from the database."""
    conn = sqlite3.connect('MOLLER_ShowerMax.db')
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    conn.close()
    return [table[0] for table in tables]

def on_table_selected(event):
    """Callback for when a table is selected from the dropdown."""
    for widget in entry_frame.winfo_children():
        widget.destroy()

    table_name = table_var.get()
    conn = sqlite3.connect('MOLLER_ShowerMax.db')
    cursor = conn.cursor()
    cursor.execute(f"PRAGMA table_info({table_name})")
    columns = cursor.fetchall()
    conn.close()

    for column in columns:
        label = ttk.Label(entry_frame, text=column[1])
        label.pack(anchor='w')
        entry = ttk.Entry(entry_frame)
        entry.pack(fill='x', padx=10)
        # For simplicity, storing the entry widget in the label's data attribute (can be done differently)
        label._entry_widget = entry
    update_display_table(table_name)

def update_display_table(table_name):
    # Destroy any existing table window to avoid clutter
    try:
        table_window.destroy()
    except NameError:
        pass

    table_window = tk.Toplevel(root)
    table_window.title(f"{table_name} Data")

    table_tree = ttk.Treeview(table_window)
    table_tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    conn = sqlite3.connect('MOLLER_ShowerMax.db')
    df = pd.read_sql_query(f"SELECT * FROM {table_name}", conn)
    conn.close()

    table_tree['columns'] = list(df.columns)

    for col in df.columns:
        table_tree.heading(col, text=col)
        table_tree.column(col, width=100)

    for index, row in df.iterrows():
        table_tree.insert("", "end", values=tuple(row))

    # Add a scrollbar to the table
    scroll = ttk.Scrollbar(table_window, orient="vertical", command=table_tree.yview)
    scroll.pack(side=tk.RIGHT, fill=tk.Y)
    table_tree.configure(yscrollcommand=scroll.set)

def add_entry():
    conn = sqlite3.connect('MOLLER_ShowerMax.db')
    cursor = conn.cursor()

    table_name = table_var.get()
    columns = []
    values = []

    for label in entry_frame.winfo_children():
        if isinstance(label, ttk.Label):
            column_name = label.cget("text")
            entry_widget = label._entry_widget
            value = entry_widget.get()
            
            columns.append(column_name)
            values.append(value)

    placeholders = ', '.join(['?'] * len(columns))
    columns_str = ', '.join(columns)
    
    cursor.execute(f"INSERT INTO {table_name} ({columns_str}) VALUES ({placeholders})", values)
    conn.commit()
    conn.close()
        # Clear all entries
    for label in entry_frame.winfo_children():
        if isinstance(label, ttk.Label) and hasattr(label, "_entry_widget"):
            entry_widget = label._entry_widget
            entry_widget.delete(0, tk.END)

def plot_histogram():
    table_name = table_var.get()
    attribute_name = attribute_var.get()
    
    conn = sqlite3.connect('MOLLER_ShowerMax.db')
    
    if attribute_name in ['length', 'width', 'height']:
        df = pd.read_sql_query(f"SELECT dimensions FROM {table_name}", conn)
        index_map = {'length': 0, 'width': 1, 'height': 2}
        df[attribute_name] = df['dimensions'].apply(lambda x: json.loads(x)[index_map[attribute_name]])
    else:
        df = pd.read_sql_query(f"SELECT {attribute_name} FROM {table_name}", conn)
    
    conn.close()
    
    fig, ax = plt.subplots(figsize=(6, 4))
    df[attribute_name].hist(ax=ax)
    ax.set_title(f'{attribute_name} Histogram')
    ax.set_xlabel(attribute_name)
    ax.set_ylabel('Frequency')
    
    # Create a new top-level window for the histogram
    plot_window = tk.Toplevel(root)
    plot_window.title(f"{table_name} - {attribute_name} Histogram")

    canvas = FigureCanvasTkAgg(fig, master=plot_window)  # A tk.DrawingArea.
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
    canvas.draw()

# Create the main window
root = tk.Tk()
root.title("ShowerMax Data Manager")

# Main frame to hold canvas and scrollbar
frame_main = ttk.Frame(root, width=600, height=600)
frame_main.pack(fill=tk.BOTH, expand=1)
frame_main.pack_propagate(False)

# Create the canvas
canvas = tk.Canvas(frame_main)
canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

# Scrollbar for the canvas
scrollbar = ttk.Scrollbar(frame_main, orient="vertical", command=canvas.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
canvas.configure(yscrollcommand=scrollbar.set)

# Frame to hold all other GUI elements
frame_content = ttk.Frame(canvas)
canvas.create_window((0,0), window=frame_content, anchor="nw")

# Ensure that the canvas size adjusts if frame_content changes (due to widget additions, etc.)
frame_content.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

# Dropdown for table selection
label = ttk.Label(frame_content, text="Select Table")
label.pack(pady=20, padx=10)

table_var = tk.StringVar()
table_dropdown = ttk.Combobox(frame_content, textvariable=table_var, values=get_all_tables())
table_dropdown.bind("<<ComboboxSelected>>", on_table_selected)
table_dropdown.pack(pady=10, padx=10)

# Frame to hold dynamically generated entry fields
entry_frame = ttk.Frame(frame_content)
entry_frame.pack(pady=20, padx=10, fill='x', expand=True)

add_button = ttk.Button(frame_content, text="Add Entry", command=add_entry)
add_button.pack(pady=20, padx=10)

# Dropdown to choose an attribute/column to plot
attribute_label = ttk.Label(frame_content, text="Select Attribute to Plot")
attribute_label.pack(pady=20, padx=10)

# List the potential attributes.
attributes = ['weight', 'length', 'width', 'height']
attribute_var = tk.StringVar()
attribute_dropdown = ttk.Combobox(frame_content, textvariable=attribute_var, values=attributes)
attribute_dropdown.pack(pady=10, padx=10)

plot_button = ttk.Button(frame_content, text="Plot Histogram", command=plot_histogram)
plot_button.pack(pady=20, padx=10)

# Create a frame to hold the plot canvas
plot_frame = ttk.Frame(frame_content)
plot_frame.pack(pady=20, padx=10, fill='x', expand=True)

root.mainloop()

