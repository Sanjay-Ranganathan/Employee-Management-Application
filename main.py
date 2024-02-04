import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

class Employee:
    def __init__(self, full_name, age, date_of_birth, salary, department):
        self.full_name = full_name
        self.age = age
        self.date_of_birth = date_of_birth
        self.salary = salary
        self.department = department

class EmployeeManagementApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Employee Management System")
        
        #connect to sqlite database (create if not exists)
        self.conn = sqlite3.connect('employee_database.db')
        self.create_employee_table()
        
        # Variables
        self.username_var = tk.StringVar()
        self.password_var = tk.StringVar()

        # Employee list
        self.employees = []

        # Login Page
        self.login_frame = tk.Frame(root)
        self.login_frame.pack(padx=20, pady=20)
        self.create_login_page()
        
    def create_employee_table(self):
        # Create a table for employees if it doesn't exist
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS employees (
                id INTEGER PRIMARY KEY,
                full_name TEXT NOT NULL,
                age INTEGER NOT NULL,
                date_of_birth TEXT NOT NULL,
                salary REAL NOT NULL,
                department TEXT NOT NULL
            )
        ''')
        self.conn.commit()
    
    def save_employee_to_db(self, employee):
        # Save an employee to the database
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO employees (full_name, age, date_of_birth, salary, department)
            VALUES (?, ?, ?, ?, ?)
        ''', (employee.full_name, employee.age, employee.date_of_birth, employee.salary, employee.department))
        self.conn.commit()

    def load_employees_from_db(self):
        # Load employees from the database
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM employees')
        rows = cursor.fetchall()
        self.employees = [Employee(row[1], row[2], row[3], row[4], row[5]) for row in rows]


    def create_login_page(self):
        tk.Label(self.login_frame, text="Username:").grid(row=0, column=0, padx=5, pady=5)
        tk.Entry(self.login_frame, textvariable=self.username_var).grid(row=0, column=1, padx=5, pady=5)
        tk.Label(self.login_frame, text="Password:").grid(row=1, column=0, padx=5, pady=5)
        tk.Entry(self.login_frame, textvariable=self.password_var, show="*").grid(row=1, column=1, padx=5, pady=5)

        tk.Button(self.login_frame, text="Login", command=self.login).grid(row=2, column=0, columnspan=2, pady=10)

    def login(self):
        # Implement your authentication logic here
        # For simplicity, let's consider a simple username/password check
        if self.username_var.get() == "admin" and self.password_var.get() == "admin":
            self.show_employee_list_page()
        else:
            messagebox.showerror("Error", "Invalid username or password")

    def show_employee_list_page(self):
        self.login_frame.destroy()

        # Employee List Page
        self.employee_list_frame = tk.Frame(self.root)
        self.employee_list_frame.pack(padx=20, pady=20)

        # Treeview to display employees in a table
        columns = ("Serial No", "Name", "Age", "Department", "Salary")
        self.employee_tree = ttk.Treeview(self.employee_list_frame, columns=columns, show="headings", selectmode="browse")

        # Add column headings
        for col in columns:
            self.employee_tree.heading(col, text=col)
            self.employee_tree.column(col, width=100)  # Adjust width as needed

        self.employee_tree.grid(row=0, column=0, columnspan=5, padx=5, pady=5)

        # Update table with existing employees
        self.update_employee_table()

        tk.Button(self.employee_list_frame, text="Add Employee", command=self.add_employee).grid(row=1, column=0, padx=5, pady=5)
        tk.Button(self.employee_list_frame, text="Search Employee", command=self.search_employee).grid(row=1, column=1, padx=5, pady=5)
        tk.Button(self.employee_list_frame, text="Edit Employee", command=self.edit_employee).grid(row=1, column=2, padx=5, pady=5)
        tk.Button(self.employee_list_frame, text="Filter Employee", command=self.filter_employee).grid(row=1, column=3, padx=5, pady=5)
        tk.Button(self.employee_list_frame, text="Delete Employee", command=self.delete_employee).grid(row=1, column=4, padx=5, pady=5)
        
        # Load employees from the database
        self.load_employees_from_db()
        # Update table with existing employees
        self.update_employee_table()

    def update_employee_table(self):
        # Clear existing items
        for item in self.employee_tree.get_children():
            self.employee_tree.delete(item)

        # Add employees to table with serial numbers and tags
        for index, employee in enumerate(self.employees, start=1):
            item_id = self.employee_tree.insert("", "end", values=(index, employee.full_name, employee.age, employee.department, employee.salary))
            self.employee_tree.item(item_id, tags=(index,))  # Tag the item with the serial number
        
        #save existing employees to the database
        # cursor=self.conn.cursor()
        # cursor.execute('DELETE FROM employees')
        for employee in self.employees:
            self.save_employee_to_db(employee)

    def add_employee(self):
        # Create a new window for adding employee
        add_employee_window = tk.Toplevel(self.root)
        add_employee_window.title("Add Employee")

        # Variables for entry fields
        full_name_var = tk.StringVar()
        age_var = tk.IntVar()
        date_of_birth_var = tk.StringVar()
        salary_var = tk.DoubleVar()
        department_var = tk.StringVar()

        # Labels and Entry fields
        tk.Label(add_employee_window, text="Full Name:").grid(row=0, column=0, padx=5, pady=5)
        tk.Entry(add_employee_window, textvariable=full_name_var).grid(row=0, column=1, padx=5, pady=5)

        tk.Label(add_employee_window, text="Age:").grid(row=1, column=0, padx=5, pady=5)
        tk.Entry(add_employee_window, textvariable=age_var).grid(row=1, column=1, padx=5, pady=5)

        tk.Label(add_employee_window, text="Date of Birth:").grid(row=2, column=0, padx=5, pady=5)
        tk.Entry(add_employee_window, textvariable=date_of_birth_var).grid(row=2, column=1, padx=5, pady=5)

        tk.Label(add_employee_window, text="Salary:").grid(row=3, column=0, padx=5, pady=5)
        tk.Entry(add_employee_window, textvariable=salary_var).grid(row=3, column=1, padx=5, pady=5)

        tk.Label(add_employee_window, text="Department:").grid(row=4, column=0, padx=5, pady=5)
        tk.Entry(add_employee_window, textvariable=department_var).grid(row=4, column=1, padx=5, pady=5)

        # Button to add employee
        tk.Button(add_employee_window, text="Add Employee", command=lambda: self.save_employee(
            full_name_var.get(), age_var.get(), date_of_birth_var.get(), salary_var.get(), department_var.get(), add_employee_window)
        ).grid(row=5, column=0, columnspan=2, pady=10)

    def save_employee(self, full_name, age, date_of_birth, salary, department, window):
        # Validate the input
        if not full_name or not age or not date_of_birth or not salary or not department:
            messagebox.showerror("Error", "Please fill in all fields.")
            return

        # Create an Employee object and add it to the list
        new_employee = Employee(full_name, age, date_of_birth, salary, department)
        self.employees.append(new_employee)

        # Show a success message
        messagebox.showinfo("Success", f"Employee '{full_name}' added successfully.")

        # Update the employee table
        self.update_employee_table()

        # Close the add employee window
        window.destroy()
        #save the employees to the database
        new_employee = Employee(full_name, age, date_of_birth, salary, department)
        self.save_employee_to_db(new_employee)

    def search_employee(self):
        # Create a new window for searching employee
        search_employee_window = tk.Toplevel(self.root)
        search_employee_window.title("Search Employee")

        # Variables for search fields
        search_name_var = tk.StringVar()
        search_age_var = tk.IntVar()
        search_department_var = tk.StringVar()

        # Labels and Entry fields for search criteria
        tk.Label(search_employee_window, text="Search by Name:").grid(row=0, column=0, padx=5, pady=5)
        tk.Entry(search_employee_window, textvariable=search_name_var).grid(row=0, column=1, padx=5, pady=5)
        tk.Button(search_employee_window, text="Search by Name", command=lambda: self.perform_search(
            name=search_name_var.get(), age=None, department=None, window=search_employee_window)
        ).grid(row=0, column=2, padx=5, pady=5)

        tk.Label(search_employee_window, text="Search by Age:").grid(row=1, column=0, padx=5, pady=5)
        tk.Entry(search_employee_window, textvariable=search_age_var).grid(row=1, column=1, padx=5, pady=5)
        tk.Button(search_employee_window, text="Search by Age", command=lambda: self.perform_search(
            name=None, age=search_age_var.get(), department=None, window=search_employee_window)
        ).grid(row=1, column=2, padx=5, pady=5)

        tk.Label(search_employee_window, text="Search by Department:").grid(row=2, column=0, padx=5, pady=5)
        tk.Entry(search_employee_window, textvariable=search_department_var).grid(row=2, column=1, padx=5, pady=5)
        tk.Button(search_employee_window, text="Search by Department", command=lambda: self.perform_search(
            name=None, age=None, department=search_department_var.get(), window=search_employee_window)
        ).grid(row=2, column=2, padx=5, pady=5)

    def perform_search(self, name, age, department, window):
        # Filter employees based on search criteria
        search_results = []
        for employee in self.employees:
            if (not name or name.lower() in employee.full_name.lower()) and \
               (age is None or age == employee.age) and \
               (not department or department.lower() in employee.department.lower()):
                search_results.append(employee)

        # Display search results in a new window
        self.display_search_results(search_results)

        # Close the search window
        window.destroy()

    def display_search_results(self, search_results):
        # Create a new window for displaying search results
        search_results_window = tk.Toplevel(self.root)
        search_results_window.title("Search Results")

        # Treeview to display search results in a table
        columns = ("Name", "Age", "Department", "Salary")
        search_results_tree = ttk.Treeview(search_results_window, columns=columns, show="headings", selectmode="browse")

        # Add column headings
        for col in columns:
            search_results_tree.heading(col, text=col)
            search_results_tree.column(col, width=100)  # Adjust width as needed

        search_results_tree.grid(row=0, column=0, columnspan=5, padx=5, pady=5)

        # Add search results to table
        for result in search_results:
            search_results_tree.insert("", "end", values=(result.full_name, result.age, result.department, result.salary))


    def edit_employee(self):
     # Check if any employee is selected
        selected_item = self.employee_tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select an employee to edit.")
            return

        # Get the tags (serial number) associated with the selected item
        tags = self.employee_tree.item(selected_item)['tags']

        if not tags:
            messagebox.showerror("Error", "Selected employee does not have a serial number.")
            return

        # The first tag is assumed to be the serial number
        selected_serial_number = tags[0]

        # Convert the serial number to an integer
        selected_index = int(selected_serial_number)

        # Create a new window for editing employee
        edit_employee_window = tk.Toplevel(self.root)
        edit_employee_window.title("Edit Employee")

        # Variables for entry fields
        full_name_var = tk.StringVar(value=self.employees[selected_index - 1].full_name)
        age_var = tk.IntVar(value=self.employees[selected_index - 1].age)
        date_of_birth_var = tk.StringVar(value=self.employees[selected_index - 1].date_of_birth)
        salary_var = tk.DoubleVar(value=self.employees[selected_index - 1].salary)
        department_var = tk.StringVar(value=self.employees[selected_index - 1].department)

        # Labels and Entry fields
        tk.Label(edit_employee_window, text="Full Name:").grid(row=0, column=0, padx=5, pady=5)
        tk.Entry(edit_employee_window, textvariable=full_name_var).grid(row=0, column=1, padx=5, pady=5)

        tk.Label(edit_employee_window, text="Age:").grid(row=1, column=0, padx=5, pady=5)
        tk.Entry(edit_employee_window, textvariable=age_var).grid(row=1, column=1, padx=5, pady=5)

        tk.Label(edit_employee_window, text="Date of Birth:").grid(row=2, column=0, padx=5, pady=5)
        tk.Entry(edit_employee_window, textvariable=date_of_birth_var).grid(row=2, column=1, padx=5, pady=5)

        tk.Label(edit_employee_window, text="Salary:").grid(row=3, column=0, padx=5, pady=5)
        tk.Entry(edit_employee_window, textvariable=salary_var).grid(row=3, column=1, padx=5, pady=5)

        tk.Label(edit_employee_window, text="Department:").grid(row=4, column=0, padx=5, pady=5)
        tk.Entry(edit_employee_window, textvariable=department_var).grid(row=4, column=1, padx=5, pady=5)

        # Button to save edited employee details
        tk.Button(edit_employee_window, text="Save Changes", command=lambda: self.save_edited_employee(
            selected_index - 1, full_name_var.get(), age_var.get(), date_of_birth_var.get(), salary_var.get(), department_var.get(), edit_employee_window)
        ).grid(row=5, column=0, columnspan=2, pady=10)
    
    def save_edited_employee(self, index, full_name, age, date_of_birth, salary, department, window):
        # Validate the input
        if not full_name or not age or not date_of_birth or not salary or not department:
            messagebox.showerror("Error", "Please fill in all fields.")
            return

        # Update the selected employee's information
        edited_employee = Employee(full_name, age, date_of_birth, salary, department)
        self.employees[index] = edited_employee

        # Show a success message
        messagebox.showinfo("Success", f"Employee '{full_name}' edited successfully.")

        # Update the employee table
        self.update_employee_table()

        # Close the edit employee window
        window.destroy()
    def filter_employee(self):
        # Create a new window for filtering employees
        filter_employee_window = tk.Toplevel(self.root)
        filter_employee_window.title("Filter Employee")

        # Variables for filter fields
        filter_salary_var = tk.DoubleVar()
        filter_age_var = tk.IntVar()
        filter_department_var = tk.StringVar()

        # Labels and Entry fields for filter criteria
        tk.Label(filter_employee_window, text="Filter by Salary:").grid(row=0, column=0, padx=5, pady=5)
        tk.Entry(filter_employee_window, textvariable=filter_salary_var).grid(row=0, column=1, padx=5, pady=5)
        tk.Button(filter_employee_window, text="Filter", command=lambda: self.perform_filter(
            filter_salary=filter_salary_var.get(), filter_age=None, filter_department=None, window=filter_employee_window)
        ).grid(row=0, column=2, padx=5, pady=5)

        tk.Label(filter_employee_window, text="Filter by Age:").grid(row=1, column=0, padx=5, pady=5)
        tk.Entry(filter_employee_window, textvariable=filter_age_var).grid(row=1, column=1, padx=5, pady=5)
        tk.Button(filter_employee_window, text="Filter", command=lambda: self.perform_filter(
            filter_salary=None, filter_age=filter_age_var.get(), filter_department=None, window=filter_employee_window)
        ).grid(row=1, column=2, padx=5, pady=5)

        tk.Label(filter_employee_window, text="Filter by Department:").grid(row=2, column=0, padx=5, pady=5)
        tk.Entry(filter_employee_window, textvariable=filter_department_var).grid(row=2, column=1, padx=5, pady=5)
        tk.Button(filter_employee_window, text="Filter", command=lambda: self.perform_filter(
            filter_salary=None, filter_age=None, filter_department=filter_department_var.get(), window=filter_employee_window)
        ).grid(row=2, column=2, padx=5, pady=5)

    def perform_filter(self, filter_salary, filter_age, filter_department, window):
        # Filter employees based on filter criteria
        filtered_results = []
        for employee in self.employees:
            if (filter_salary is None or filter_salary == employee.salary) and \
               (filter_age is None or filter_age == employee.age) and \
               (filter_department is None or filter_department.lower() == employee.department.lower()):
                filtered_results.append(employee)

        # Display filtered results in a new window
        self.display_filter_results(filtered_results)

        # Close the filter window
        window.destroy()

    def display_filter_results(self, filtered_results):
        # Create a new window for displaying filtered results
        filter_results_window = tk.Toplevel(self.root)
        filter_results_window.title("Filter Results")

        # Treeview to display filtered results in a table
        columns = ("Name", "Age", "Department", "Salary")
        filter_results_tree = ttk.Treeview(filter_results_window, columns=columns, show="headings", selectmode="browse")

        # Add column headings
        for col in columns:
            filter_results_tree.heading(col, text=col)
            filter_results_tree.column(col, width=100)  # Adjust width as needed

        filter_results_tree.grid(row=0, column=0, columnspan=4, padx=5, pady=5)

        # Add filtered results to table
        for result in filtered_results:
            filter_results_tree.insert("", "end", values=(result.full_name, result.age, result.department, result.salary))
    def delete_employee(self):
        # Check if any employee is selected
        selected_item = self.employee_tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select an employee to delete.")
            return

        # Get the tags (serial number) associated with the selected item
        tags = self.employee_tree.item(selected_item)['tags']

        if not tags:
            messagebox.showerror("Error", "Selected employee does not have a serial number.")
            return

        # The first tag is assumed to be the serial number
        selected_serial_number = tags[0]

        # Convert the serial number to an integer
        selected_index = int(selected_serial_number)

        # Confirm deletion
        confirm = messagebox.askyesno("Confirm Deletion", "Are you sure you want to delete this employee?")
        if not confirm:
            return

        # Delete the selected employee from the list
        deleted_employee = self.employees.pop(selected_index - 1)

        # Show a success message
        messagebox.showinfo("Success", f"Employee '{deleted_employee.full_name}' deleted successfully.")

        # Update the employee table
        self.update_employee_table()
        cursor=self.conn.cursor()
        cursor.execute('DELETE FROM employees WHERE id=?',(selected_index))
        self.conn.commit()

# ... (remaining methods)
if __name__ == "__main__":
    root = tk.Tk()
    app = EmployeeManagementApp(root)
    root.mainloop()
