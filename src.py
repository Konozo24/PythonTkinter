import pandas as pd
import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
import os
import ttkbootstrap as tb
import time
import json


class mainWindow:
    def __init__(self, title):
        
        #Initialise main window
        self.root = tb.Window(themename='journal')
        self.root.style.theme_use('journal')
        self.root.title(title)
        self.current_frame = None
        self.screenWidth = self.root.winfo_screenwidth()
        self.screenHeight = self.root.winfo_screenheight()
        x = (self.screenWidth - 1000) // 2
        y = (self.screenHeight - 750) // 2 
        self.window_size = f'{1000}x{750}+{x}+{y}'
        self.root.geometry(self.window_size)
        
        self.style = tb.Style()
        self.style.configure('Custom.TButton', font=("Helvetica", 20), background='#4C9A8C', foreground='#FFFFFF')  
        self.style.configure('Custom2.TButton', font=("Helvetica", 20), background='#f5bf42', foreground='#FFFFFF')
        
        
    def clear_frame(self):
        """
        Clear all widgets from the current frame and main window.

        - Destroys all widgets in the `current_frame`, if it exists.
        - Ensures no remaining widgets remain in the main window.
        """
        
        if hasattr(self, 'current_frame') and self.current_frame is not None:
            for widget in self.current_frame.winfo_children():
                print(widget)
                widget.destroy()
                
            self.current_frame.destroy()
        self.current_frame = None
    
        #Remove remaining widgets 
        for widget in self.root.winfo_children():
            print(widget)
            widget.destroy()
        
    # Start the main application loop
    def run(self):
        self.root.mainloop()


class mainApp(mainWindow):

    def __init__(self, title):
        super().__init__(title)
        self.menuGUI()

    def menuGUI(self):
        """
        Set up and display the main menu.

        - Adds navigation buttons to access different modules of the application.
        - Ensures buttons are styled and spaced consistently.
        """
        self.current_frame = ttk.Labelframe(self.root, text="Main Menu", padding=(100, 100))
        self.current_frame.pack(pady=10, padx=10, fill='both', expand=True)
        
        titleLabel = ttk.Label(self.current_frame, text="Quaktask", bootstyle='primary',font=("Arial", 40, "bold"))
        titleLabel.pack(padx=10, pady=10)
        
        
        #Button for Main Menu
        self.buttons = [
            ttk.Button(self.current_frame, text='Expense Tracker', style='Custom.TButton',
                       command=self.open_expense_tracker).pack(ipadx=100, ipady=10, pady=20, fill=None, expand=True),
            ttk.Button(self.current_frame, text='Flashcard Quizzer', style='Custom.TButton',
                       command=self.open_flashcard).pack(ipadx=91, ipady=10, pady=20, fill=None, expand=True),
            ttk.Button(self.current_frame, text='To-Do List', style='Custom.TButton',
                       command=self.open_ToDoList).pack(ipadx=147, ipady=10, pady=20, fill=None, expand=True),
            ttk.Button(self.current_frame, text='Pomodoro Timer', style='Custom.TButton',
                       command=self.open_PomodoroTimer).pack(ipadx=103, ipady=10, pady=20, fill=None, expand=True),
            ttk.Button(self.current_frame, text='Exit', style='Custom2.TButton',
                       command=self.root.quit).pack(ipadx=100, ipady=10, pady=20, fill=None, expand=True)
        ]

    
    # Open the Expense Tracker in a new window
    def open_expense_tracker(self):

        self.clear_frame()
        Expense = ExpenseTracker("Expense Tracker", self.root, self)
        self.current_frame = Expense.current_frame


    # Open the Expense Tracker in a new window
    def open_flashcard(self):
        
        self.clear_frame()
        Flashcard = FlashcardApp("Flashcard", self.root, self)
        self.current_frame = Flashcard.current_frame


    # Open the To-Do List in a new window
    def open_ToDoList(self):
        
        self.clear_frame()
        ToDoList = ToDoApp("Flashcard", self.root, self)
        self.current_frame = ToDoList.current_frame


    # Open the Expense Tracker in a new window
    def open_PomodoroTimer(self):
        
        self.clear_frame()
        PomodoroTimer = Pomodorotimer("Pomodoro Timer", self.root, self)
        self.current_frame = PomodoroTimer.current_frame
        

class ExpenseTracker(mainWindow):
    """
    ExpenseTracker is a module that enables users to track and manage expenses via a GUI

    Responsibilities:
    - Allows users to add, visualize, save, and load expenses.
    - Implements a structured GUI for input and visualization.
    - Ensures proper file handling and data validation.
    """
    def __init__(self, title, root_window, mainApp):

        self.root = root_window
        self.mainApp = mainApp
        self.root.title(title)
        self.current_frame = ttk.Frame(self.root)
        self.current_frame.pack(fill='both')
        self.style = tb.Style()
        self.style.configure('.', font=("Helvetica", 12))
        # Initialise expense data and categories
        self.expense_df = pd.DataFrame(columns=['Date', 'Amount', 'Category', 'Description'])
        self.categories = ["Food", "Transportation", "Utilities", "Entertainment", "Others"]

        self.setupUi()
        self.createDirectories()
        

    # Create directory for new expense file if it doesn't exist
    def createDirectories(self):
        if not os.path.exists("expense_data"):
            os.makedirs("expense_data")


    # Set up GUI components
    def setupUi(self):
        
        # Frame for input widgets
        inputFrame = ttk.LabelFrame(self.root, text= 'Add Expense', bootstyle='info', padding=(10,10))
        inputFrame.pack(padx=10, pady=10, fill='x')

        # Input fields for expense details
        self.amountLabel = ttk.Label(inputFrame, text= 'Amount: ').grid(row=0, column=0, sticky= 'w',padx=5, pady=5)
        self.amountEntry = ttk.Entry(inputFrame, width=20, style="info.TEntry")
        self.amountEntry.grid(row=0, column=1, padx=5, pady=5)

        
        self.categoryLabel = ttk.Label(inputFrame, text= 'Category: ').grid(row=0, column=2, sticky= 'w',padx=5, pady=5)
        self.categoryVar = tk.StringVar()
        self.categoryCombo = ttk.Combobox(inputFrame, bootstyle='info', textvariable=self.categoryVar, values=self.categories)
        self.categoryCombo.grid(row=0, column=3, padx=5, pady=5)
        self.categoryCombo.set("Select Category")

        
        self.dateFrame = ttk.Label(inputFrame, text= 'Date: ').grid(row=1, column=0, sticky='w',padx=5, pady=5)
        self.dateEntry = tb.DateEntry(inputFrame, bootstyle='info', firstweekday=0)
        self.dateEntry.grid(row=1, column=1, padx=5, pady=5)

        
        self.descriptionLabel = ttk.Label(inputFrame, text= 'Description: ').grid(row=2, column=0, sticky= 'w', padx=5, pady=5)
        self.descriptionEntry = ttk.Entry(inputFrame, width=40, bootstyle='info')
        self.descriptionEntry.grid(row=2, column=1, columnspan=1, padx=5, pady=5)
        

        ttk.Label(inputFrame, text="Filter by Category:").grid(row=1, column=2, padx=5, pady=5)
        self.filterVar = tk.StringVar()
        self.filter_categories = ['All'] + self.categories
        self.filterCombo = ttk.Combobox(inputFrame, bootstyle='info', textvariable=self.filterVar, values=self.filter_categories)
        self.filterCombo.grid(row=1, column=3, padx=5, pady=5)
        self.filterCombo.set('All')

        self.cancel_filter_button = ttk.Button(inputFrame, text='Cancel Filter', bootstyle='info', command= lambda: self.filterCombo.set('All'))
        self.cancel_filter_button.grid(row=1, column=4, padx=5, pady=5) 

        # Button to add an expense entry
        add_Button = ttk.Button(inputFrame, text='Add Expense', bootstyle='success', command = self.add_Expenses)
        add_Button.grid(row=3, column=1, columnspan=2, pady=10)

        # Call filter_Expenses function when filterVar is updated
        self.filterVar.trace_add('write', self.filter_Expenses)

        # Treeview for displaying expense entries
        self.tree = ttk.Treeview(self.root, columns=("Date", "Amount", "Category", "Description"), bootstyle='info', show="headings")
        self.tree.heading("Date", text="Date")
        self.tree.heading("Amount", text="Amount")
        self.tree.heading("Category", text="Category")
        self.tree.heading("Description", text="Description")

        self.tree.column("Date", anchor="center", width=120)
        self.tree.column("Amount", anchor="center", width=120)
        self.tree.column("Category", anchor="center", width=120)
        self.tree.column("Description", anchor="center", width=200)

        self.tree.pack(padx=10, pady=10, expand=True, fill='both')

        # Button frame for control buttons
        buttonFrame = ttk.Frame(self.root)
        buttonFrame.pack(padx=10, pady=10)

        visualiseButton = ttk.Button(buttonFrame, text='Visualise Expenses', bootstyle='info', command=self.visualise_Expenses)
        visualiseButton.pack(side=tk.LEFT, padx=10)
        saveButton = ttk.Button(buttonFrame, text='Save Expenses', bootstyle='success', command=self.save_Expenses) 
        saveButton.pack(side=tk.LEFT, padx=10)
        loadButton = ttk.Button(buttonFrame, text='Load Expenses', bootstyle='info', command=self.load_Expenses)
        loadButton.pack(side=tk.LEFT, padx=10)
        deleteButton = ttk.Button(buttonFrame, text='Delete Expenses', bootstyle='danger', command=self.delete_Expenses)
        deleteButton.pack(side=tk.LEFT, padx=10)
        closeButton = ttk.Button(buttonFrame, text="Close", command=self.return_to_main_menu)  
        closeButton.pack(side=tk.LEFT, padx=10)

    # Return to Main Menu
    def return_to_main_menu(self):
        
        self.mainApp.clear_frame()
        self.mainApp.menuGUI()
    
    # Private method to add expense
    def _add_expense_internal(self, amount, category, description, date):
        new_Expense = pd.DataFrame({
                "Date": [date],
                "Amount": [amount],
                "Category": [category],
                "Description": [description]
            })
        
        #Add new expense to current expense dataframe
        self.expense_df = pd.concat([self.expense_df, new_Expense], ignore_index=True)
        self.expense_df = self.expense_df.sort_values('Date')

    def add_Expenses(self):
        """
        Add a new expense entry to the tracker.

        - Retrieve input values for amount, category, description, and date.
        - Validates the inputs to ensure correctness.
        - Appends the new entry to the DataFrame and updates the GUI.
        - Raises a ValueError for invalid inputs.
        """
        try:    
            # Retrieve input values
            amount = self.amountEntry.get()
            category = self.categoryVar.get()
            description = self.descriptionEntry.get()
            date = self.dateEntry.entry.get()

            # Input validation
            if category == "Select Category":
                raise ValueError("Please select a category")
            
            if amount is None or amount.strip() == '':
                raise ValueError("Please input an amount")
            
            # Convert amount to float and add inputs to Dataframe 
            amount = float(amount)
            display_date = pd.to_datetime(date, dayfirst=True)
            self._add_expense_internal(amount, category, description, display_date)
            
            #Clear the treeview
            for record in self.tree.get_children():
                self.tree.delete(record)

            #insert data into Treeview
            for index,row in self.expense_df.iterrows():
                self.tree.insert(parent='', index='end', values=(row['Date'].strftime('%Y-%m-%d'), 
                                                                 f"${row['Amount']}", 
                                                                 row['Category'], 
                                                                 row['Description']))
            
            #Reset input fields
            self.amountEntry.delete(0, tk.END)
            self.categoryCombo.set("Select Category")
            self.descriptionEntry.delete(0, tk.END)

        except ValueError as e:
            messagebox.showerror(title='Input Error', message=f'{str(e)}')

    def filter_Expenses(self, *args):
        selected_category = self.filterVar.get()

        for record in self.tree.get_children():
            self.tree.delete(record)

        if selected_category == 'All':
            filter_df = self.expense_df
        else:
            filter_df = self.expense_df[self.expense_df['Category'] == selected_category]

        for index,row in filter_df.iterrows():
            self.tree.insert(parent='', index='end', values=(row['Date'].strftime('%Y-%m-%d'), 
                                                                 f"${row['Amount']}", 
                                                                 row['Category'], 
                                                                 row['Description'])
                                                                 )


    def delete_Expenses(self):
        selected = self.tree.selection()
        if selected:
            confirm = messagebox.askyesno(title="Delete Confirmation", message="Are you sure you want to delete the selected Expense(s)?")
            if confirm:
                for item in selected:
                    # Get the values from the treeview
                    values = self.tree.item(item)['values']  
                    # Convert values to match DataFrame format for comparison
                    date = pd.to_datetime(values[0])
                    amount = float(values[1].replace('$', ''))
                    category = values[2]
                    description = values[3]

                    # Find and remove matching row from DataFrame
                    mask = ((self.expense_df['Date'] == date) & \
                            (self.expense_df['Amount'] == amount) & \
                            (self.expense_df['Category'] == category) & \
                            (self.expense_df['Description'] == description))
                    self.expense_df = self.expense_df[~mask]

                    # Remove selected item from treeview
                    self.tree.delete(item)

                self.expense_df.reset_index(drop=True, inplace=True)  # Reset the DataFrame index
                messagebox.showinfo("Success", "Selected Expense(s) deleted successfully!")
        else:
            messagebox.showwarning("Selection Error", "Please select a expense to delete.")

    def visualise_Expenses(self):
        """
        Visualize expenses using a pie chart.

        - Groups expenses by category and calculates the total amount for each category.
        - Uses matplotlib to display a pie chart with percentages and a title.
        """
        
        #Check existence of any category
        if self.expense_df.empty:
            messagebox.showerror(title='Visualisation Error', message=f'Unable to visualise expenses.')
            return
        
        #Set visual style 
        plt.style.use("fivethirtyeight")

        #Group expenses by category and calculate the total amount
        totalCategory = self.expense_df.groupby('Category')['Amount'].sum()
        
        #Create piechart with category totals
        plt.pie(totalCategory.values, labels=totalCategory.index, 
                autopct='%1.1f%%', shadow=True, 
                wedgeprops={'edgecolor': 'black'})
        
        #Set piechart title
        plt.title('Expenses by Category')

        #Ensure piechart has equal aspect ratio
        plt.axis()
        
        #Adjust layout and display chart
        plt.tight_layout()
        plt.legend(title='Category:')
        plt.show()

    #Save expenses to csv file
    def save_Expenses(self):    
        try:
            file_name = f"expense_data/expenses.csv"
            answer = messagebox.askokcancel(title='Save Confirmation', message='Confirm to save?')

            if answer == True:
                self.expense_df.to_csv(file_name, index=False)
                messagebox.showinfo(title='File saved', message='File saved successfully.')

            else:
                return
        except Exception as e:
            messagebox.showerror(title='Save Error', message=f'Unable to save the file: {str(e)}')

    #Load expenses from CSV file
    def load_Expenses(self):
        """
        Load expenses from an external CSV file into the tracker.

        - Prompts the user for a file name using a dialog box.
        - Reads the specified CSV file and parses its contents into a DataFrame.
        - Updates the treeview widget with the loaded expense entries.
        - Validates that the file exists and handles errors gracefully.
        - Raises a Load Error for invalid file name.
        """
        
        try:

            answer = messagebox.askokcancel(title='Load Confirmation', message='Confirm to load?')
            if answer == True:
                #the file name of the CSV file
                file_path = f"expense_data/expenses.csv" 

            
                # Load the file into a DataFrame, ensuring the 'Date' column is parsed correctly
                loaded_file = pd.read_csv(file_path, parse_dates= ['Date'])
                
            
                #Update expenses Dataframe
                self.expense_df = loaded_file

                
                #Delete old records
                for record in self.tree.get_children():
                    self.tree.delete(record)

                #Update Treeview from expenses Dataframe
                for index, row in self.expense_df.iterrows():
                    dollar_amount = f"${row['Amount']}"
                    self.tree.insert(parent='', index='end', values=(row['Date'].strftime('%Y-%m-%d'), 
                                                                    dollar_amount, 
                                                                    row['Category'],
                                                                    row['Description']))
                    
                messagebox.showinfo(title='Expenses loaded', message=f'Expenses from {file_path} loaded successfully.')
            else:
                return
        except Exception as e:
            messagebox.showerror(title='Load Error', message=f'Unable to load the file: {str(e)}')


class FlashcardBase(mainWindow):
    """Base class to manage flashcards."""
    def __init__(self):
        
        self.flashcards = {}
        

    def add_flashcard(self, question, answer):
        """Add a flashcard to the collection."""
        if question in self.flashcards:
            return False  # Indicates a duplicate
        self.flashcards[question] = answer
        return True


    def reset_flashcards(self):
        """Clear all flashcards."""
        self.flashcards.clear()


class FlashcardApp(FlashcardBase):
    """
    GUI-based flashcard application.
    Responsibilities:
    - Allows users to create, view ,save, and load flashcards.
    - Implements a structured GUI for input and visualization.
    - Ensures proper file handling and data validation.
    """
    FLASHCARD_FILE = "flashcards.json"
    def __init__(self, title, root_window, mainApp):
        super().__init__()
        self.root = root_window
        self.mainApp = mainApp
        self.root.title(title)
        self.current_frame = ttk.Frame(self.root)
        self.current_frame.pack(fill='both')
        self.flashcards = self.load_flashcard()
        
        self.correct_answers = 0  # Tracks correct answers during quizzes
        
        self.GUI_menu()


    def return_to_main_menu(self):
        self.clear_frame()
        self.mainApp.menuGUI()


    def GUI_menu(self):
        """Display the main menu."""
        self.clear_frame()
        tk.Label(self.root, text="Flashcard App", font=("Arial", 50)).pack(pady=50)
        tk.Button(self.root, text="Create Flashcards", font=("Arial", 18), command=self.create_flashcards, padx=9, pady=10).pack(pady=5)
        tk.Button(self.root, text="View Flashcards", font=("Arial", 18), command=self.view_flashcards, padx=23, pady=10).pack(pady=5)
        tk.Button(self.root, text="Quiz Yourself", font=("Arial", 18), command=self.quiz_flashcards, padx=49, pady=10).pack(pady=5)
        tk.Button(self.root, text="Reset Flashcards", font=("Arial", 18), command=self.reset_all_flashcards, padx=17, pady=10).pack(pady=5)
        tk.Button(self.root, text="Exit", font=("Arial", 16), command=self.return_to_main_menu, padx=25, pady=10).pack(pady=5)


    def create_flashcards(self):
        """Allows the user to create flashcards."""
        self.clear_frame()
        tk.Label(self.root, text="Create a Flashcard", font=("Arial", 18), padx=20, pady=10).pack(pady=10)

        tk.Label(self.root, text="Question:", font=("Arial", 16)).pack()
        self.question_entry = tk.Entry(self.root, width=50)
        self.question_entry.pack(pady=5)

        tk.Label(self.root, text="Answer:", font=("Arial", 16)).pack()
        self.answer_entry = tk.Entry(self.root, width=50) 
        self.answer_entry.pack(pady=5)

        tk.Button(self.root, text="Add Flashcard", font=("Arial", 15), command=self.process_add_flashcard).pack(pady=5)
        tk.Button(self.root, text="Back to Menu", font=("Arial", 15), command=self.GUI_menu).pack(pady=5)

    def reset_all_flashcards(self):
        if messagebox.askyesno("Confirm Deletion", "Are you sure you want to delete all flashcards?"):
        # Reset the flashcards in memory and in the file
            self.flashcards = {}
            self.save_flashcards()  # Save the empty dictionary to the file
            messagebox.showinfo("Deleted", "All flashcards have been deleted.")
            self.GUI_menu()

    def load_flashcard(self):
        """Load flashcards from the file."""
        try:
            with open(self.FLASHCARD_FILE, "r") as file:
                return json.load(file)
        except FileNotFoundError:
                return {}  # If the file doesn't exist, return an empty dictionary
        except json.JSONDecodeError:
                return {}

    def save_flashcards(self):
        """Save the current flashcards to a file."""
        with open(self.FLASHCARD_FILE, "w") as file:
            json.dump(self.flashcards, file)

    def process_add_flashcard(self):
        """Handle adding a flashcard."""
        question = self.question_entry.get().strip()
        answer = self.answer_entry.get().strip()
        if question and answer:
            if question not in self.flashcards:
                self.flashcards[question] = answer
                self.save_flashcards()
                messagebox.showinfo("Success", "Flashcard added!")
                self.question_entry.delete(0, tk.END)
                self.answer_entry.delete(0, tk.END)
            else:
                messagebox.showerror("Error", "This question already exists.")
        else:
            messagebox.showerror("Error", "Please fill in both fields.")


    def view_flashcards(self):
        """Display all flashcards."""
        self.clear_frame()
        tk.Label(self.root, text="Your Flashcards", font=("Arial", 20)).pack(pady=10)
        if not self.flashcards:
            tk.Label(self.root, text="No flashcards created yet.", font=("Arial", 16)).pack(pady=5)
        else:
            for question, answer in self.flashcards.items():
                tk.Label(self.root, text=f"Q: {question}", font=("Arial", 16)).pack(pady=2)
                tk.Label(self.root, text=f"A: {answer}", font=("Arial", 16), fg="gray").pack(pady=2)
        tk.Button(self.root, text="Back to Menu", font=("Arial", 16), command=self.GUI_menu).pack(pady=10)


    def quiz_flashcards(self):
        """Quiz the user."""
        if not self.flashcards:
            messagebox.showerror("Error", "No flashcards available for quizzing.")
            return
        self.clear_frame()
        self.questions = list(self.flashcards.keys())
        self.current_index = 0
        self.correct_answers = 0
        tk.Label(self.root, text="Quiz Yourself", font=("Arial", 20)).pack(pady=10)
        self.question_label = tk.Label(self.root, text=self.questions[self.current_index], font=("Arial", 16))
        self.question_label.pack(pady=10)
        self.answer_entry = tk.Entry(self.root, width=50)
        self.answer_entry.pack(pady=5)
        tk.Button(self.root, text="Submit Answer", font=("Arial", 16), command=self.check_answer).pack(pady=5)
        tk.Button(self.root, text="Back to Menu", font=("Arial", 16), command=self.GUI_menu).pack(pady=5)


    def check_answer(self):
        """Check the user's answer."""
        user_answer = self.answer_entry.get().strip()
        correct_answer = self.flashcards[self.questions[self.current_index]]
        if user_answer.lower() == correct_answer.lower():
            self.correct_answers += 1
            messagebox.showinfo("Correct!", "Good job! That's correct.")
        else:
            messagebox.showerror("Incorrect", f"The correct answer was: {correct_answer}")
        self.answer_entry.delete(0, tk.END)
        self.current_index += 1
        if self.current_index < len(self.questions):
            self.question_label.config(text=self.questions[self.current_index])
        else:
            self.show_score()


    def show_score(self):
        """Display quiz score."""
        messagebox.showinfo("Quiz Complete", f"You scored {self.correct_answers}/{len(self.questions)}!")
        self.GUI_menu()


    def clear_frame(self):
        """Clear the current screen."""
        for widget in self.root.winfo_children():
            widget.destroy()
    

class ToDoApp(mainWindow):
    """
    GUI-based To-Do List application.
    Responsibilities:
    - Allows users to add, delete ,save, and load To-Do list.
    - Implements a structured GUI for input and visualization.
    - Ensures proper file handling and data validation.
    """
    # Constructor initializes the ToDoApp class
    def __init__(self, title, root_window, mainApp):
        self.root = root_window  # Root window for the application
        self.mainApp = mainApp  # Main app instance
        self.tasks = pd.DataFrame(columns=["ID", "Task", "Important", "Done"])  # DataFrame to store tasks
        self.style = tb.Style()
        self.style.configure('.', font=("Helvetica", 12))

        self.setup_ui()  # Set up the user interface

    # Method to set up the UI components
    def setup_ui(self):
        self.current_frame = ttk.Frame(self.root)  # Frame to hold UI elements
        self.current_frame.pack(fill='both', expand=True)

        # Label for task input field
        ttk.Label(self.current_frame, text="Enter a New Task:", font=('Arial', 30, 'bold'), bootstyle='primary').pack(padx=10, pady=10, anchor="w")
        
        # Entry widget for entering a task
        self.task_entry = ttk.Entry(self.current_frame, width=50, bootstyle='primary')
        self.task_entry.pack(ipady=10, padx=10, fill="x")

        # Button frame containing action buttons
        button_frame = ttk.Frame(self.current_frame)
        button_frame.pack(padx=10, fill="both", expand=True)

        # Action buttons for task operations
        ttk.Button(button_frame, text="Add Task", command=self.add_task, bootstyle='success').pack(side="left", padx=5)
        ttk.Button(button_frame, text="Edit Task", command=self.edit_task, bootstyle='info').pack(side="left", padx=5)
        ttk.Button(button_frame, text="Mark as Done", command=self.mark_as_done, bootstyle='info').pack(side="left", padx=5)
        ttk.Button(button_frame, text="Mark as Important", command=self.mark_as_important, bootstyle='info').pack(side="left", padx=5)
        ttk.Button(button_frame, text="Cancel Mark as Done", command=self.cancel_mark_as_done, bootstyle='info').pack(side="left", padx=5)
        ttk.Button(button_frame, text="Cancel Important", command=self.cancel_mark_as_important, bootstyle='info').pack(side="left", padx=5)

        # Treeview to display tasks
        self.task_treeview = ttk.Treeview(self.current_frame, columns=("ID", "Task", "Important", "Done"), show="headings", bootstyle='primary')
        self.task_treeview.heading("ID", text="ID", anchor='w')
        self.task_treeview.heading("Task", text="Task", anchor='w')
        self.task_treeview.heading("Important", text="Important", anchor='w')
        self.task_treeview.heading("Done", text="Done", anchor='w')
        self.task_treeview.column("ID", width=50)
        self.task_treeview.column("Task", width=300)
        self.task_treeview.column("Important", width=100)
        self.task_treeview.column("Done", width=100)
        self.task_treeview.pack(padx=10, pady=10, fill="both", expand=True)

        # Control frame with buttons for saving, loading, deleting tasks
        control_frame = ttk.Frame(self.current_frame)
        control_frame.pack(pady=10)

        # Save, load, delete, and back buttons
        ttk.Button(control_frame, text="Save Tasks", command=self.save_tasks).pack(side="left", padx=10)
        ttk.Button(control_frame, text="Load Tasks", command=self.load_tasks).pack(side="left", padx=10)
        ttk.Button(control_frame, text="Delete Task", command=self.delete_task).pack(side="left", padx=10)
        ttk.Button(control_frame, text="Back to Menu", command=self.return_to_main_menu).pack(side="left", padx=10)

    # Method to cancel the "Done" mark on a task
    def cancel_mark_as_done(self):
        selected = self.task_treeview.selection()
        if selected:
            for item in selected:
                task_id = int(self.task_treeview.item(item, "values")[0])
                self.tasks.loc[self.tasks["ID"] == task_id, "Done"] = "❌"
            self.update_task_treeview()
        else:
            messagebox.showwarning("Selection Error", "Please select a task to cancel mark as done!")

    # Method to cancel the "Important" mark on a task
    def cancel_mark_as_important(self):
        selected = self.task_treeview.selection()
        if selected:
            for item in selected:
                task_id = int(self.task_treeview.item(item, "values")[0])
                self.tasks.loc[self.tasks["ID"] == task_id, "Important"] = "❌" 
            self.update_task_treeview()
        else:
            messagebox.showwarning("Selection Error", "Please select a task to cancel mark as important!")

    # Method to add a new task
    def add_task(self):
        task_text = self.task_entry.get().strip() 
        if task_text:
            new_task = {
                "ID": len(self.tasks) + 1,
                "Task": task_text,
                "Important": "❌",
                "Done": "❌" 
            }
            self.tasks = pd.concat([self.tasks, pd.DataFrame([new_task])], ignore_index=True)  # Add the task to the DataFrame
            self.update_task_treeview() 
            self.task_entry.delete(0, tk.END) 
        else:
            messagebox.showwarning("Input Error", "Task cannot be empty!") 

    # Method to delete a task
    def delete_task(self):
        
        selected = self.task_treeview.selection()
        if selected:
            confirm = messagebox.askyesno("Delete Confirmation", "Are you sure you want to delete the selected task(s)?")
            if confirm:
                for item in selected:
                    task_id = int(self.task_treeview.item(item, "values")[0])
                    self.tasks = self.tasks[self.tasks["ID"] != task_id]  # Remove the task from the DataFrame
                    self.update_task_treeview()
        else:
            messagebox.showwarning("Selection Error", "Please select a task to delete!")

    # Method to edit a selected task
    def edit_task(self):
        selected = self.task_treeview.selection()
        if selected:
            task_id = int(self.task_treeview.item(selected[0], "values")[0])  # Get the task ID
            old_task = self.tasks.loc[self.tasks["ID"] == task_id, "Task"].values[0]
            new_task = self.task_entry.get().strip()  # Get the new task text from the entry field
            if new_task:
                confirm = messagebox.askyesno("Edit Confirmation", f"Are you sure you want to change the task from '{old_task}' to '{new_task}'?")
                if confirm:
                    self.tasks.loc[self.tasks["ID"] == task_id, "Task"] = new_task  # Update the task in the DataFrame
                    self.update_task_treeview() 
                    self.task_entry.delete(0, tk.END)  
            else:
                messagebox.showwarning("Input Error", "Task cannot be empty!")  
        else:
            messagebox.showwarning("Selection Error", "Please select a task to edit!")

    # Method to mark a task as done
    def mark_as_done(self):
        selected = self.task_treeview.selection()  
        if selected:
            for item in selected:
                task_id = int(self.task_treeview.item(item, "values")[0])
                self.tasks.loc[self.tasks["ID"] == task_id, "Done"] = "✅" 
                self.update_task_treeview()
        else:
            messagebox.showwarning("Selection Error", "Please select a task to mark as done!")

    # Method to mark a task as important
    def mark_as_important(self):
        selected = self.task_treeview.selection() 
        if selected:
            for item in selected:
                task_id = int(self.task_treeview.item(item, "values")[0])
                self.tasks.loc[self.tasks["ID"] == task_id, "Important"] = "✅" 
            self.update_task_treeview()
        else:
            messagebox.showwarning("Selection Error", "Please select a task to mark as important!")

    # Method to save tasks to a CSV file
    def save_tasks(self):
        try:
            self.tasks.to_csv("tasks.csv", index=False)  # Save tasks to CSV file
            messagebox.showinfo("Success", "Tasks saved successfully to tasks.csv!")
        except Exception as e:
            messagebox.showerror("Error", f"Could not save tasks: {e}") 

    # Method to load tasks from a CSV file
    def load_tasks(self):
        try:
            self.tasks = pd.read_csv("tasks.csv") 
            self.update_task_treeview()
            messagebox.showinfo("Success", "Tasks loaded successfully from tasks.csv!")  
        except Exception as e:
            messagebox.showerror("Error", f"Could not load tasks: {e}") 

    # Method to update the task treeview with current tasks
    def update_task_treeview(self):
        for item in self.task_treeview.get_children():
            self.task_treeview.delete(item)  # Remove all existing rows
        for _, task in self.tasks.iterrows(): # Add each task to the treeview
            self.task_treeview.insert(
                "", "end",
                values=(task["ID"], task["Task"], task["Important"], task["Done"]),
            )

    # Method to return to the main menu
    def return_to_main_menu(self):
        self.mainApp.clear_frame()
        self.mainApp.menuGUI() 


class Timer(mainWindow):
    def __init__(self):
        # 'running' tracks whether the timer is active
        # 'remaining_time' holds the time left in seconds
        self.running = False
        self.remaining_time = 0


    def countdown(self, root, label):
        """
        Handles the countdown logic for the timer.
        Updates the UI label with remaining time and decrements time every second.
        Handles potential exceptions during runtime.
        """
        try:
            while self.remaining_time > 0 and self.running:
                minutes_left, seconds_left = divmod(self.remaining_time, 60)
                label.config(text=f"{minutes_left:02} : {seconds_left:02}")
                root.update()
                time.sleep(1)  # Pause for a second
                self.remaining_time -= 1

            # When the countdown finishes, go to the next cycle
            if self.remaining_time == 0 and self.running:
                self.next_cycle()

        except Exception as e:
            label.config(text="Error")
            print(f"An error occurred: {e}")


class Pomodorotimer(Timer):
    """
    GUI-based Pomodoro Timer application.
    Responsibilities:
    - Allows users to set working and resting duration.
    - Implements a strcutured GUI for time visualization.
    - Ensures proper file handling and data validation.
    """
    def __init__(self, title, root_window, mainApp):
        super().__init__()
        self.root = root_window
        self.mainApp = mainApp
        self.root.title(title)
        self.current_frame = ttk.Frame(self.root)
        self.current_frame.pack(fill='both',expand=True)
        self.style = tb.Style()
        self.style.configure('.', font=("Helvetica", 25))
    
        # Timer configuration
        self.cycles = 4
        self.current_cycle = 1
        self.pomodoro_count = 0
    
        self.setupGUI()

    # GUI setup
    def setupGUI(self):     
        
        #Main container for Timer
        main_container = ttk.Frame(self.current_frame)
        main_container.pack(fill='both', expand=True)

        #Timer Display
        self.label = tb.Label(main_container, text="00 : 00", font=("Helvetica", 40, "bold"), bootstyle='primary')
        self.label.pack(pady=20)

        #Input Section
        input_container = tb.Frame(main_container, bootstyle='light')
        input_container.pack(fill='x', padx=50, pady=10)


        #Work Duration Input
        time_frame = tb.Frame(input_container, bootstyle='light')
        time_frame.pack(side='left', expand=True, padx=5)

        self.input_duration = ttk.Entry(time_frame, justify="center")
        self.input_duration.pack()
        
        self.work_duration_label = tb.Label(time_frame, text='Work Duration (min)', font=("Helvetica", 20, "bold"), bootstyle='primary')
        self.work_duration_label.pack()

        self.input_shortbreak = tb.Entry(time_frame, justify="center")
        self.input_shortbreak.pack()
        
        self.short_break_label = tb.Label(time_frame, text="Short Break (min)", font=("Helvetica", 20, "bold"), bootstyle='primary')
        self.short_break_label.pack()

        self.input_longbreak = tb.Entry(time_frame, justify="center")
        self.input_longbreak.pack()
        
        self.long_break_label = tb.Label(time_frame, text="Long Break (min)", font=("Helvetica", 20, "bold"), bootstyle='primary')
        self.long_break_label.pack()

        self.button_frame = tb.Frame(main_container)
        self.button_frame.pack(pady=20)

        self.skip = tb.Button(self.button_frame, text="Skip", command=self.timer_skip, bootstyle="danger-outline")
        self.skip.pack(side='left', padx=10)

        self.start = tb.Button(self.button_frame, text="Start", command=self.timer_start, bootstyle="success-outline")
        self.start.pack(side='left', padx=10)

        self.reset = tb.Button(self.button_frame, text="Reset", command=self.timer_reset, bootstyle="warning-outline")
        self.reset.pack(side='left', padx=10)

        self.quit_button = tb.Button(self.button_frame, text="Exit", command=self.return_to_main_menu, bootstyle="primary-outline")
        self.quit_button.pack(side='left', padx=10)

        self.session_type_label = tb.Label(main_container, font=("Helvetica", 15, "bold"), text="Current Session: None", bootstyle='danger')
        self.session_type_label.pack(pady=10)

        self.pomodoro_count_label = tb.Label(main_container, font=("Helvetica", 15, "bold"), text="Pomodoros Completed: 0", bootstyle='danger')
        self.pomodoro_count_label.pack(pady=10)

        self.history = tb.Button(self.button_frame, text="Check History", command=self.show_history, bootstyle="primary-outline")
        self.history.pack(side='left', padx=10)

    
    def return_to_main_menu(self):

        self.clear_frame()
        self.mainApp.menuGUI()    

    # Starts the timer and toggles between 'Start' and 'Stop' button based on the current state
    def timer_start(self):
        if not self.running:
            # Validate input values (duration, breaks)
            if self.update():
                self.running = True
                self.start.config(text="Stop", command=self.timer_pause)
                self.run()
            else:
                print("Invalid Input")
        else:
            self.running = False
            self.start.config(text="Resume", command=self.timer_resume)


    def timer_pause(self):
        self.running = False
        self.start.config(text="Resume", command=self.timer_resume)

    # Resumes the timer countdown from the remaining time
    def timer_resume(self):
        self.running = True
        self.start.config(text="Stop", command=self.timer_pause)

        # Resume countdown from the remaining time
        self.countdown(self.root, self.label)


    def timer_reset(self):
        self.running = False
        self.current_cycle = 0
        self.remaining_time = 0  # Reset remaining time
        self.label.config(text="00 : 00")

        #Reset UI Button to default color setting
        for button, style in [
            (self.start, "success-outline"),
            (self.skip, "danger-outline"),
            (self.reset, "warning-outline"),
            (self.quit_button, "primary-outline")
        ]:
            button.config(bootstyle=style)

        self.start.config(text="Start", command=self.timer_start)

        self.pomodoro_count = 0
        self.pomodoro_count_label.config(text=f"Pomodoros Completed: {self.pomodoro_count}")
        self.session_type_label.config(text='Current Session: None', bootstyle='danger')

    
        # Ensure labels are reset visually (if needed)
        self.work_duration_label.config(text="Work Duration (min)")
        self.short_break_label.config(text="Short Break")
        self.long_break_label.config(text="Long Break")
        self.input_duration.delete(0, tk.END)
        self.input_shortbreak.delete(0, tk.END)
        self.input_longbreak.delete(0, tk.END)
    

    def timer_skip(self):

        # Prevent skipping at the end of cycle
        if (self.current_cycle == 1) and (not self.session_type == 'Long Break' or not self.session_type == 'Work Duration' \
                                          or not self.session_type == 'Short Break'):
            messagebox.showwarning(title='Skip Error', message='Press Start or Reset to continue the cycle!')
            return

        if self.running:
            self.running = False
            self.start.config(text="Start", command=self.timer_resume)
            self.work_duration_label.config(bootstyle='primary')
            self.short_break_label.config(bootstyle='primary')
            self.long_break_label.config(bootstyle='primary')
        self.next_cycle()

    # Manages the transitions between different session types (work, short break, long break)
    def next_cycle(self):
        if self.current_cycle == 5:  # After 4 cycles (work, break, work, long break)
            self.current_cycle = 1 # Reset the cycle counter for the next Pomodoro session
            self.label.config(text="End! Reset or Start", bootstyle='danger')
            self.start.config(text="Start", command=self.timer_start)
            
            # Change all elements to danger style after completing a full cycle
            danger_style_elements = [
                self.current_frame, self.label, 
                self.work_duration_label, self.short_break_label, self.long_break_label,
                self.start, self.skip, self.reset, self.quit_button, self.session_type_label
            ]
            
            for element in danger_style_elements:
                element.config(bootstyle='danger')

            # Increment Pomodoro Counter after a full cycle
            self.pomodoro_count += 1
            self.pomodoro_count_label.config(text=f"Pomodoros Completed: {self.pomodoro_count}")

            # Update Session Type & Reset time to default
            self.session_type_label.config(text=f"Current Session: None")
            self.remaining_time = 0

            # Log the completed cycle            
            return

        # Continue to the next session within the cycle
        if self.current_cycle == 1:
            # First work session
            self.session_type = "Work Duration"
            self.label.config(bootstyle='primary', text=f"{self.duration:02} : 00")

            primary_style_elements = [self.current_frame, self.label, 
                self.work_duration_label, self.short_break_label, self.long_break_label,
                self.start, self.skip, self.reset, self.quit_button, self.session_type_label
                ]

            for element in primary_style_elements:
                element.config(bootstyle='primary')

            # Update session type label and other UI elements
            self.session_type_label.config(text=f"Current Session: {self.session_type}")
            self.remaining_time = self.duration * 60

            self.log_session(self.session_type)

        elif self.current_cycle == 2:
            # Short break
            self.session_type = "Short Break"
            self.label.config(bootstyle='info', text=f"{self.shortbreak:02} : 00")

            info_style_elements = [self.current_frame, self.label, 
                self.work_duration_label, self.short_break_label, self.long_break_label,
                self.start, self.skip, self.reset, self.quit_button, self.session_type_label
                ]
            
            for element in info_style_elements:
                element.config(bootstyle='info')

            # Update session type label and other UI elements
            self.session_type_label.config(text=f"Current Session: {self.session_type}")
            self.remaining_time = self.shortbreak * 60

            self.log_session(self.session_type)

        elif self.current_cycle == 3:
            # Second work session
            self.session_type = "Work Duration"
            self.label.config(bootstyle='primary', text=f"{self.duration:02} : 00")

            primary_style_elements = [self.current_frame, self.label, 
                self.work_duration_label, self.short_break_label, self.long_break_label,
                self.start, self.skip, self.reset, self.quit_button, self.session_type_label
                ]  
            
            for element in primary_style_elements:
                element.config(bootstyle='primary')

            # Update session type label and other UI elements
            self.session_type_label.config(text=f"Current Session: {self.session_type}")
            self.remaining_time = self.duration * 60

            self.log_session(self.session_type)

        elif self.current_cycle == 4:
            # Long break
            self.session_type = "Long Break"
            self.label.config(bootstyle='success', text=f"{self.longbreak:02} : 00")

            success_style_elements = [self.current_frame, self.label, 
                self.work_duration_label, self.short_break_label, self.long_break_label,
                self.start, self.skip, self.reset, self.quit_button, self.session_type_label
                ]  
            
            for element in success_style_elements:
                element.config(bootstyle='success')

            # Update session type label and other UI elements
            self.session_type_label.config(text=f"Current Session: {self.session_type}")
            self.remaining_time = self.longbreak * 60

            self.log_session(self.session_type)

        self.current_cycle += 1  # Increment cycle for the next session

        # Start the countdown for the next session
        self.countdown(self.root, self.label)

    def run(self):
        if self.running:
            self.next_cycle()  # Start or continue the cycle


    def update(self):
        try:
            self.duration = int(self.input_duration.get())
            self.shortbreak = int(self.input_shortbreak.get())
            self.longbreak = int(self.input_longbreak.get())

            if self.duration <= 0 or self.shortbreak <= 0 or self.longbreak <= 0:
                raise Exception("Duration must be a positive integer")
            
            return True  # Validation passed
        
        except Exception as e:
            ui_elements = [
            self.current_frame, self.label, 
            self.work_duration_label, self.short_break_label, self.long_break_label,
            self.start, self.skip, self.reset, self.quit_button
        ]   
            for element in ui_elements:
                element.config(bootstyle='primary')

            self.label.config(text="Invalid Input")
            print(f"Error: {e}")
            return False  # Validation failed

    # Log each session cycle into a text file for tracking
    def log_session(self, session_type):
        try:
            # Log each cycle number and session type
            with open("pomodoro_log.txt", "a") as file:
                file.write(f"Cycle {self.current_cycle}: {session_type}\n")
        except Exception as e:
            print(f"Failed to log session: {e}")

    # Displays the Pomodoro session history from the log file
    def show_history(self):
        try:
            with open("pomodoro_log.txt", "r") as file:
                history = file.read()
    
            history_window = tk.Toplevel(self.root)  # Create a new window to display history
            history_window.title("Pomodoro History")
    
            history_label = tb.Label(
                history_window,
                text="Pomodoro Cycle History",
                font=("Arial", 18),
                bootstyle="info"
            )
            history_label.pack(pady=10)
    
            history_text = tk.Text(history_window, wrap="word", font=("Arial", 12))  # Create a text widget for the history
            history_text.insert("end", history)  # Insert the history into the widget
            history_text.config(state="disabled")  # Disable editing of the history
            history_text.pack(pady=10)
    
        except FileNotFoundError:
            # Handle the case when the history file doesn't exist
            history_window = tk.Toplevel(self.root)
            history_window.title("Pomodoro History")
            history_window.geometry("300x200")
            history_label = tb.Label(
                history_window,
                text="No history found!",
                font=("Arial", 18),
                bootstyle="danger"
            )
            history_label.pack(pady=10)


if __name__ == "__main__":
    app = mainApp(title='QuakTask')
    app.run()
