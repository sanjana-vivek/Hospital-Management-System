import re
import tkinter as tk
from tkinter import ttk


def display_report(ReportTitle, column_names, column_2darray):

    # Prepare clean column names
    column_headings = [re.sub("\W+", "", i) for i in column_names]
    # Create the main window
    report_window = tk.Tk()
    report_window.title(ReportTitle)

    # Add a label to display the report title
    report_title = tk.Label(
        report_window, text=ReportTitle, font=("Helvetica", 14, "bold")
    )
    report_title.pack(padx=10, pady=10)

    # Create a Treeview widget for the table
    table_tree = ttk.Treeview(report_window)
    table_tree["columns"] = column_headings
    table_tree.heading("#0", text="S.No.")  # Index column
    for i, heading in enumerate(column_headings):
        table_tree.heading(heading, text=column_names[i])
        table_tree.pack(padx=10, pady=10)

    # Add sample data to the table (replace this with your SELECT statement)
    for i, row in enumerate(column_2darray):
        table_tree.insert("", "end", text=f"{i}.", values=row)

    # Add a button to close the report window
    close_button = tk.Button(report_window, text="Close", command=report_window.destroy)
    close_button.pack(padx=10, pady=10, side=tk.BOTTOM)

    # Start the Tkinter event loop
    report_window.mainloop()
