import customtkinter as ctk
from tkinter import messagebox, ttk
import mysql.connector

# CustomTkinter settings
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")


# MySQL Database Connection
def connect_to_database():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",  # Replace with your MySQL username
            password="root",  # Replace with your MySQL password
            database="genz_hypermart"
        )
        return connection
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")
        return None


# App to Show After Successful Login
def show_app():
    login_window.withdraw()  # Ensure login window is destroyed first
    root = ctk.CTk()
    root.geometry("1000x600")
    root.title("GEN-Z HYPERMART")

    # Header
    header_frame = ctk.CTkFrame(root, fg_color="lightblue")
    header_frame.pack(side="top", fill="x")

    header_label = ctk.CTkLabel(
        header_frame,
        text="GEN-Z HYPERMART",
        font=("Times New Roman", 20, "bold", "italic"),
        text_color="darkblue",
    )
    header_label.pack(side="left", padx=10, pady=10)

    # Main content frame
    frame = ctk.CTkFrame(root, fg_color="white")
    frame.pack(side="top", anchor="nw", padx=20, pady=10, fill="x")

    # Input fields
    def setup_input_fields():
        name_label = ctk.CTkLabel(frame, text="Name", font=("Times New Roman", 12, "bold"))
        name_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        name_entry = ctk.CTkEntry(frame)
        name_entry.grid(row=0, column=1, padx=10, pady=10)

        phone_label = ctk.CTkLabel(frame, text="Phone", font=("Times New Roman", 12, "bold"))
        phone_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")
        phone_entry = ctk.CTkEntry(frame)
        phone_entry.grid(row=1, column=1, padx=10, pady=10)

        address_label = ctk.CTkLabel(frame, text="Address", font=("Times New Roman", 12, "bold"))
        address_label.grid(row=2, column=0, padx=10, pady=10, sticky="w")
        address_entry = ctk.CTkEntry(frame)
        address_entry.grid(row=2, column=1, padx=10, pady=10)

        product_label = ctk.CTkLabel(frame, text="Product Name", font=("Times New Roman", 12, "bold"))
        product_label.grid(row=3, column=0, padx=10, pady=10, sticky="w")
        product_entry = ctk.CTkEntry(frame)
        product_entry.grid(row=3, column=1, padx=10, pady=10)

        quantity_label = ctk.CTkLabel(frame, text="Quantity", font=("Times New Roman", 12, "bold"))
        quantity_label.grid(row=3, column=2, padx=10, pady=10, sticky="w")
        quantity_entry = ctk.CTkEntry(frame)
        quantity_entry.grid(row=3, column=3, padx=10, pady=10)

        price_label = ctk.CTkLabel(frame, text="Price", font=("Times New Roman", 12, "bold"))
        price_label.grid(row=3, column=4, padx=10, pady=10, sticky="w")
        price_entry = ctk.CTkEntry(frame)
        price_entry.grid(row=3, column=5, padx=10, pady=10)

        total_label = ctk.CTkLabel(frame, text="Total", font=("Times New Roman", 12, "bold"))
        total_label.grid(row=3, column=6, padx=10, pady=10, sticky="w")
        total_entry = ctk.CTkEntry(frame)
        total_entry.grid(row=3, column=7, padx=10, pady=10)

        return name_entry, phone_entry, address_entry, product_entry, quantity_entry, price_entry, total_entry

    name_entry, phone_entry, address_entry, product_entry, quantity_entry, price_entry, total_entry = setup_input_fields()

    # Calculate Total
    def calculate_total(event):
        try:
            quantity = float(quantity_entry.get())
            price = float(price_entry.get())
            total = quantity * price
            total_entry.delete(0, ctk.END)
            total_entry.insert(0, f"{total:.2f}")
        except ValueError:
            total_entry.delete(0, ctk.END)
            total_entry.insert(0, "0")

    # Bind real-time calculation to the entry fields
    quantity_entry.bind("<KeyRelease>", calculate_total)
    price_entry.bind("<KeyRelease>", calculate_total)

    # Table Frame
    table_frame = ctk.CTkFrame(root, fg_color="white")
    table_frame.pack(fill="x", padx=20, pady=10)

    columns = ("serial", "product", "quantity", "price", "total")
    table = ttk.Treeview(table_frame, columns=columns, show="headings", height=8)
    table.heading("serial", text="S.No")
    table.heading("product", text="Product")
    table.heading("quantity", text="Quantity")
    table.heading("price", text="Price")
    table.heading("total", text="Total")
    table.column("serial", anchor="center")
    table.column("product", anchor="center")
    table.column("quantity", anchor="center")
    table.column("price", anchor="center")
    table.column("total", anchor="center")
    table.pack(fill="both", expand=True)

    serial_no = 0

    def add_to_table():
        nonlocal serial_no
        product = product_entry.get()
        quantity = quantity_entry.get()
        price = price_entry.get()
        total = total_entry.get()

        if not product or not quantity or not price or not total:
            messagebox.showinfo("Input Error", "All fields must be filled out!")
            return

        serial_no += 1
        table.insert("", "end", values=(serial_no, product, quantity, price, total))

        product_entry.delete(0, ctk.END)
        quantity_entry.delete(0, ctk.END)
        price_entry.delete(0, ctk.END)
        total_entry.delete(0, ctk.END)

    def clear_table():
        for item in table.get_children():
            table.delete(item)

    def save_table_to_database():
        connection = connect_to_database()
        if connection is None:
            return

        try:
            cursor = connection.cursor()
            query = """
                INSERT INTO billing_records (product_name, quantity, price, total, customer_name, phone, address)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            customer_name = name_entry.get()
            phone = phone_entry.get()
            address = address_entry.get()

            if not customer_name or not phone or not address:
                messagebox.showerror("Input Error", "Customer details (Name, Phone, Address) must be filled out!")
                return

            for row_id in table.get_children():
                row = table.item(row_id, 'values')
                product_name, quantity, price, total = row[1], row[2], row[3], row[4]
                cursor.execute(query, (product_name, quantity, price, total, customer_name, phone, address))

            connection.commit()
            messagebox.showinfo("Success", "All records saved successfully!")

            # Clear all fields and the table after submission
            name_entry.delete(0, ctk.END)
            phone_entry.delete(0, ctk.END)
            address_entry.delete(0, ctk.END)
            product_entry.delete(0, ctk.END)
            quantity_entry.delete(0, ctk.END)
            price_entry.delete(0, ctk.END)
            total_entry.delete(0, ctk.END)
            nonlocal serial_no
            serial_no = 0
            clear_table()

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")
        finally:
            connection.close()

    add_btn = ctk.CTkButton(frame, text="Add", command=add_to_table)
    add_btn.grid(row=3, column=8, padx=10, pady=10)

    clr_btn = ctk.CTkButton(frame, text="Clear", font=("Times New Roman", 10, "bold"), command=clear_table)
    clr_btn.grid(row=3, column=9, padx=10, pady=10)

    submit_button = ctk.CTkButton(
        frame, text="Submit", font=("Times New Roman", 12, "bold"),
        fg_color="blue", text_color="white", command=save_table_to_database
    )
    submit_button.grid(row=5, column=0, columnspan=8, pady=10)

    root.mainloop()


def validate_login():
    username = username_entry.get()
    password = password_entry.get()

    if username == "admin" and password == "admin":
        show_app()
    else:
        messagebox.showerror("Login Failed", "Invalid Login Credentials! Please Try Again")


# Login Window with grid layout inside a frame
login_window = ctk.CTk()
login_window.geometry("400x300")
login_window.title("Login")

# Frame for the login form
frame = ctk.CTkFrame(login_window)
frame.place(relx=0.5, rely=0.5, anchor="center")

# Username and Password Entry inside the frame using grid
username_label = ctk.CTkLabel(frame, text="Username", font=("Arial", 14))
username_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

username_entry = ctk.CTkEntry(frame)
username_entry.grid(row=0, column=1, padx=10, pady=10)

password_label = ctk.CTkLabel(frame, text="Password", font=("Arial", 14))
password_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")

password_entry = ctk.CTkEntry(frame, show="*")
password_entry.grid(row=1, column=1, padx=10, pady=10)

# Login Button inside the frame
login_button = ctk.CTkButton(frame, text="Login", command=validate_login)
login_button.grid(row=2, column=0, columnspan=2, pady=20)

login_window.mainloop()

