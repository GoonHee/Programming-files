from tkinter import Tk, Canvas, Entry, Button, StringVar, filedialog, OptionMenu, Label, ttk, messagebox
from PIL import Image, ImageTk
import sqlite3

selected_car_id = None
image_path = None  # To store the uploaded image path

# Connect to the database and create the table
def connect_db():
    conn = sqlite3.connect('car_details.db')
    cursor = conn.cursor()
    cursor.execute(''' 
        CREATE TABLE IF NOT EXISTS cars (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            registration_number TEXT,
            make_and_model TEXT,
            seating_capacity TEXT,
            daily_rate REAL,
            fuel_type TEXT,
            manufacture_year TEXT,
            image_path TEXT
        )
    ''')
    conn.commit()
    return conn


# Function to save data to the database
def save_data():
    registration_number = entry_registration.get()
    make_and_model = make_and_model_var.get()
    seating_capacity = entry_seating.get()
    daily_rate = entry_rate.get()
    fuel_type = fuel_type_var.get()
    manufacture_year = entry_year.get()

    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(''' 
        INSERT INTO cars (registration_number, make_and_model, seating_capacity, daily_rate, fuel_type, manufacture_year, image_path)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (registration_number, make_and_model, seating_capacity, daily_rate, fuel_type, manufacture_year, image_path))
    conn.commit() #to make sure data save successfully in database.
    conn.close()
    messagebox.showinfo("Success", "Data saved successfully!")
    refresh_treeview()

def refresh_treeview():
    for row in treeview.get_children():
        treeview.delete(row)

    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT id, registration_number, make_and_model, seating_capacity, daily_rate, manufacture_year, fuel_type FROM cars')
    rows = cursor.fetchall()
    conn.close()

    for row in rows:
        treeview.insert("", "end", values=row)


# Function to upload an image
def browse_image():
    global image_path
    image_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
    if image_path:
        upload_image()

# Function to upload and display the image
def upload_image():
    img = Image.open(image_path)
    img = img.resize((150, 150), Image.LANCZOS)  # Resize the image to 150x150
    img = ImageTk.PhotoImage(img)
    image_display.config(image=img)
    image_display.image = img

# Function to delete a car from the database
def delete_data():
    global selected_car_id
    if selected_car_id is not None:
        confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this car?")
        if confirm:
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute('DELETE FROM cars WHERE id = ?', (selected_car_id,))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Car deleted successfully!")
            refresh_treeview()
            clear_selection()
    else:
        messagebox.showwarning("Warning", "Please select a car to delete.")


# Function to update a car's details
def update_data():
    global selected_car_id
    if selected_car_id is not None:
        registration_number = entry_registration.get()
        make_and_model = make_and_model_var.get()
        seating_capacity = entry_seating.get()
        daily_rate = entry_rate.get()
        manufacture_year=entry_year.get()
        fuel_type = fuel_type_var.get()

        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute(''' 
            UPDATE cars 
            SET registration_number = ?, make_and_model = ?, seating_capacity = ?, daily_rate = ?, manufacture_year = ?,fuel_type = ?, image_path = ?
            WHERE id = ?
        ''', (registration_number, make_and_model, seating_capacity, daily_rate, manufacture_year, fuel_type, image_path, selected_car_id))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Car updated successfully!")
        refresh_treeview()
        clear_selection()
    else:
        messagebox.showwarning("Warning", "Please select a car to update.")

def select_item(event):
    global selected_car_id, image_path
    selected_item = treeview.selection()
    if selected_item:
        item = treeview.item(selected_item)
        values = item['values']
        selected_car_id = values[0]  # Get the ID of the selected car

        # Fetch the selected car details from the database (including image path)
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM cars WHERE id = ?', (selected_car_id,))
        car_data = cursor.fetchone()
        conn.close()

        # retrieving the car details
        if car_data:   #if car data not empty
            entry_registration.delete(0, 'end')  #clear all the data
            entry_registration.insert(0, car_data[1])
            make_and_model_var.set(car_data[2])
            entry_seating.set(car_data[3])  # Set the seating capacity dropdown
            entry_rate.delete(0, 'end')
            entry_rate.insert(0, car_data[4])
            entry_year.delete(0,'end')
            entry_year.insert(0, car_data[5])
            fuel_type_var.set(car_data[6])

            # Load and display the image if the image path exists
            image_path = car_data[7]  # This is the image path stored in the database
            if image_path:
                upload_image()

def clear_selection():
    global selected_car_id
    selected_car_id = None
    entry_registration.delete(0, 'end')
    make_and_model_var.set("Select")
    entry_seating.set("Select")  # Reset dropdown
    entry_rate.delete(0, 'end')
    entry_year.delete(0,'end')
    fuel_type_var.set("Select")
    image_display.config(image="")  # Clear image


# Setting up the main window
window = Tk()
window.geometry("900x700")
window.configure(bg="#81BEEB")

# Canvas for layout
canvas = Canvas(
    window,
    bg="#81BEEB",
    height=600,
    width=800,
    bd=0,
    highlightthickness=0,
    relief="ridge"
)
canvas.place(x=0, y=0)

# Title
canvas.create_text(400, 28, anchor="center", text="MANAGE CAR DETAILS", fill="#000000",
                   font=("Times New Roman ExtraBold", 18))

# Input fields
canvas.create_text(37.0, 98.0, anchor="nw", text="Registration Number:", fill="#000000", font=("Inter Bold", 14 * -1))
entry_registration = Entry(bd=0, bg="#D9D9D9", fg="#000716", highlightthickness=0)
entry_registration.place(x=193.0, y=96.0, width=180.0, height=22.0)

canvas.create_text(37.0, 138.0, anchor="nw", text="Make & Model:", fill="#000000", font=("Inter Bold", 14 * -1))
make_and_model_var = StringVar(window)
make_and_model_var.set("Select")  # Default value
make_and_model_options = ["Toyota Camry", "Honda Civic", "BMW 3 Series", "Ford Focus", "Audi A4"]
make_and_model_dropdown = OptionMenu(window, make_and_model_var, *make_and_model_options)
make_and_model_dropdown.place(x=193.0, y=136.0, width=180.0)

canvas.create_text(37.0, 178.0, anchor="nw", text="Seating Capacity:", fill="#000000", font=("Inter Bold", 14 * -1))
entry_seating = StringVar(window)
entry_seating.set("Select")  # Default value
seating_options = ["2", "4", "5", "7", "8"]
seating_dropdown = OptionMenu(window, entry_seating, *seating_options)
seating_dropdown.place(x=193.0, y=176.0, width=180.0)

canvas.create_text(37.0, 218.0, anchor="nw", text="Daily Rate (RM):", fill="#000000", font=("Inter Bold", 14 * -1))
entry_rate = Entry(bd=0, bg="#D9D9D9", fg="#000716", highlightthickness=0)
entry_rate.place(x=193.0, y=216.0, width=180.0, height=22.0)

canvas.create_text(37.0, 258.0, anchor="nw", text="Manufacture Year:", fill="#000000", font=("Inter Bold", 14 * -1))
entry_year = Entry(bd=0, bg="#D9D9D9", fg="#000716", highlightthickness=0)
entry_year.place(x=193.0, y=256.0, width=180.0, height=22.0)

canvas.create_text(37.0, 298.0, anchor="nw", text="Fuel Type:", fill="#000000", font=("Inter Bold", 14 * -1))
fuel_type_var = StringVar(window)
fuel_type_var.set("Select")  # Default value
fuel_type_options = ["Petrol", "Diesel", "Electric", "Hybrid"]
fuel_type_dropdown = OptionMenu(window, fuel_type_var, *fuel_type_options)
fuel_type_dropdown.place(x=193.0, y=296.0, width=180.0)

# Browse image button
button_browse = Button(
    text="Browse Image",
    command=browse_image,
    bg="#64C4ED",  # Light blue background
    fg="black"
)
button_browse.place(x=193.0, y=346.0, width=100.0, height=30.0)

# Image display area
image_display = Label(window)
image_display.place(x=450, y=130, width=150, height=150)

treeview = ttk.Treeview(window, columns=("ID", "Registration Number", "Make & Model", "Seating Capacity", "Daily Rate", "Manufacture Year", "Fuel Type"), show="headings")

treeview.heading("ID", text="ID")
treeview.heading("Registration Number", text="Reg. No.")
treeview.heading("Make & Model", text="Make & Model")
treeview.heading("Seating Capacity", text="Seats")
treeview.heading("Daily Rate", text="Rate (RM)")
treeview.heading("Manufacture Year", text="Year")
treeview.heading("Fuel Type", text="Fuel Type")

treeview.column("ID", width=50, anchor="center")
treeview.column("Registration Number", width=100, anchor="center")
treeview.column("Make & Model", width=150, anchor="center")
treeview.column("Seating Capacity", width=100, anchor="center")
treeview.column("Daily Rate", width=100, anchor="center")
treeview.column("Manufacture Year", width=100, anchor = "center")
treeview.column("Fuel Type", width=100, anchor="center")

treeview.place(x=50, y=400, width=700, height=150)
treeview.bind("<<TreeviewSelect>>", select_item)

# Buttons for saving, updating, deleting, and clearing (below the image)
button_save = Button(
    text="Save",
    command=save_data,
    bg="green",  # Light blue background
    fg="#FFFFFF"
)
button_save.place(x=450, y=300, width=80, height=30)

button_update = Button(
    text="Update",
    command=update_data,
    bg="#FFA500",  # Orange background for update
    fg="#FFFFFF"
)
button_update.place(x=540, y=300, width=80, height=30)

button_delete = Button(
    text="Delete",
    command=delete_data,
    bg="#D9534F",  # Red background for delete
    fg="#FFFFFF"
)
button_delete.place(x=630, y=300, width=80, height=30)

button_clear = Button(
    text="Clear",
    command=clear_selection,
    bg="#DCDCDC",  # Light gray background for clear
    fg="#000000"
)
button_clear.place(x=720, y=300, width=80, height=30)

refresh_treeview()
window.mainloop()