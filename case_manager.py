import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

# إنشاء قاعدة البيانات
conn = sqlite3.connect('cases.db')
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS cases (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        case_number TEXT,
        case_type TEXT,
        case_count INTEGER,
        case_date TEXT,
        notes TEXT
    )
''')
conn.commit()

# دالة لإضافة قضية جديدة
def add_case():
    case_number = entry_case_number.get()
    case_type = combo_case_type.get()
    case_count = entry_case_count.get()
    case_date = entry_case_date.get()
    notes = entry_notes.get()

    if not case_number or not case_type or not case_count:
        messagebox.showerror("خطأ", "من فضلك أدخل جميع البيانات المطلوبة.")
        return

    cursor.execute('INSERT INTO cases (case_number, case_type, case_count, case_date, notes) VALUES (?, ?, ?, ?, ?)',
                   (case_number, case_type, case_count, case_date, notes))
    conn.commit()
    load_cases()
    clear_fields()

# دالة لحذف قضية
def delete_case():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showerror("خطأ", "من فضلك اختر قضية للحذف.")
        return
    case_id = tree.item(selected_item)['values'][0]
    cursor.execute('DELETE FROM cases WHERE id = ?', (case_id,))
    conn.commit()
    load_cases()

# دالة لتحميل القضايا إلى الجدول
def load_cases():
    for item in tree.get_children():
        tree.delete(item)
    cursor.execute('SELECT * FROM cases')
    for row in cursor.fetchall():
        tree.insert('', 'end', values=row)

# دالة لمسح الحقول بعد الإدخال
def clear_fields():
    entry_case_number.delete(0, tk.END)
    combo_case_type.set('')
    entry_case_count.delete(0, tk.END)
    entry_case_date.delete(0, tk.END)
    entry_notes.delete(0, tk.END)

# دالة لتحميل البيانات المحددة إلى الحقول لتعديلها
def load_selected_case():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showerror("خطأ", "من فضلك اختر قضية للتعديل.")
        return

    selected_case = tree.item(selected_item)['values']
    entry_case_number.delete(0, tk.END)
    entry_case_number.insert(0, selected_case[1])

    combo_case_type.set(selected_case[2])

    entry_case_count.delete(0, tk.END)
    entry_case_count.insert(0, selected_case[3])

    entry_case_date.delete(0, tk.END)
    entry_case_date.insert(0, selected_case[4])

    entry_notes.delete(0, tk.END)
    entry_notes.insert(0, selected_case[5])

# دالة لتحديث القضية المختارة
def update_case():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showerror("خطأ", "من فضلك اختر قضية للتحديث.")
        return

    case_id = tree.item(selected_item)['values'][0]
    case_number = entry_case_number.get()
    case_type = combo_case_type.get()
    case_count = entry_case_count.get()
    case_date = entry_case_date.get()
    notes = entry_notes.get()

    cursor.execute('''
        UPDATE cases
        SET case_number = ?, case_type = ?, case_count = ?, case_date = ?, notes = ?
        WHERE id = ?
    ''', (case_number, case_type, case_count, case_date, notes, case_id))
    conn.commit()
    load_cases()
    clear_fields()

# دالة للبحث عن القضايا
def search_case():
    search_term = entry_search.get()
    for item in tree.get_children():
        tree.delete(item)
    cursor.execute("SELECT * FROM cases WHERE case_number LIKE ? OR case_type LIKE ?", ('%' + search_term + '%', '%' + search_term + '%'))
    for row in cursor.fetchall():
        tree.insert('', 'end', values=row)

# إنشاء النافذة الرئيسية
root = tk.Tk()
root.title("برنامج إدارة وتنظيم القضايا")
root.geometry("950x600")

# نموذج إدخال البيانات
tk.Label(root, text="رقم القضية:").grid(row=0, column=0, padx=5, pady=5)
entry_case_number = tk.Entry(root)
entry_case_number.grid(row=0, column=1, padx=5, pady=5)

tk.Label(root, text="نوع القضية:").grid(row=1, column=0, padx=5, pady=5)
combo_case_type = ttk.Combobox(root, values=["جنائي", "مدني", "تجاري", "أخرى"])
combo_case_type.grid(row=1, column=1, padx=5, pady=5)

tk.Label(root, text="عدد الملفات:").grid(row=2, column=0, padx=5, pady=5)
entry_case_count = tk.Entry(root)
entry_case_count.grid(row=2, column=1, padx=5, pady=5)

tk.Label(root, text="تاريخ القضية:").grid(row=3, column=0, padx=5, pady=5)
entry_case_date = tk.Entry(root)
entry_case_date.grid(row=3, column=1, padx=5, pady=5)

tk.Label(root, text="ملاحظات:").grid(row=4, column=0, padx=5, pady=5)
entry_notes = tk.Entry(root)
entry_notes.grid(row=4, column=1, padx=5, pady=5)

btn_add = tk.Button(root, text="إضافة القضية", command=add_case)
btn_add.grid(row=5, column=0, pady=10)

btn_load = tk.Button(root, text="تحميل للتعديل", command=load_selected_case)
btn_load.grid(row=5, column=1, pady=10)

btn_update = tk.Button(root, text="تحديث القضية", command=update_case)
btn_update.grid(row=6, column=0, pady=10)

# البحث
tk.Label(root, text="بحث:").grid(row=7, column=0, padx=5, pady=5)
entry_search = tk.Entry(root)
entry_search.grid(row=7, column=1, padx=5, pady=5)
btn_search = tk.Button(root, text="بحث", command=search_case)
btn_search.grid(row=7, column=2, padx=5, pady=5)

# الجدول لعرض القضايا
columns = ("ID", "رقم القضية", "نوع القضية", "عدد الملفات", "تاريخ القضية", "ملاحظات")
tree = ttk.Treeview(root, columns=columns, show="headings")
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=150)
tree.grid(row=8, column=0, columnspan=3, pady=10)

btn_delete = tk.Button(root, text="حذف القضية", command=delete_case)
btn_delete.grid(row=9, column=0, columnspan=3, pady=5)

load_cases()
root.mainloop()

conn.close()