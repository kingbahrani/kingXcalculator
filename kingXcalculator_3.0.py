import tkinter as tk
from tkinter import messagebox
import math

class KingXCalculator:
    def __init__(self, root_window):
        """
        Initialize the KingXCalculator.

        Args:
            root_window: The main Tkinter window.
        """
        self.root = root_window
        self.root.title("KingXCalculator")
        self.root.geometry("400x600") # Adjusted for a more vertical calculator layout
        self.root.resizable(False, False) # Make window not resizable
        self.root.configure(bg="#2C3E50") # Dark blue-grey background

        # Calculator state variables
        self.current_input = ""      # Stores the string of the number currently being entered
        self.first_operand = None    # Stores the first number in an operation
        self.operation = None        # Stores the pending operation (+, -, *, /, etc.)
        self.result_displayed = False # Flag to check if the display currently shows a result

        # --- Calculation Functions (kept from original, can be static or part of class) ---
        self.calc_functions = {
            "Addition": lambda x, y: x + y,
            "Subtraction": lambda x, y: x - y,
            "Multiplication": lambda x, y: x * y,
            "Division": self._divide,
            "Power": self._power,
            "Logarithm": self._logarithm,
        }

        self._create_widgets()

    # --- Helper Calculation Functions with Error Handling ---
    def _divide(self, x, y):
        if y == 0:
            return "Error: Div by Zero"
        return x / y

    def _power(self, x, y):
        try:
            return x ** y
        except OverflowError:
            return "Error: Overflow"


    def _logarithm(self, x, base):
        if x <= 0 or base <= 0 or base == 1:
            return "Error: Log Domain"
        try:
            return math.log(x, base)
        except ValueError: # Handles cases like math.log(-1, 10) if not caught by above
            return "Error: Log Input"
        except OverflowError:
            return "Error: Overflow"

    # --- GUI Creation ---
    def _create_widgets(self):
        """Creates and lays out the GUI widgets for the calculator."""

        # Display Screen
        display_font = ("Arial", 28, "bold")
        self.display_var = tk.StringVar()
        self.display_var.set("0") # Initial display
        display_entry = tk.Entry(
            self.root,
            textvariable=self.display_var,
            font=display_font,
            bd=10, # Border width
            relief=tk.RIDGE, # Sunken border
            justify="right", # Text alignment
            bg="#ABB7B7", # Light greyish display background
            fg="#000000"  # Black text
        )
        display_entry.pack(pady=20, padx=10, fill="x")

        # Button Frame
        button_frame = tk.Frame(self.root, bg="#2C3E50")
        button_frame.pack(expand=True, fill="both", padx=10, pady=10)

        # Button Definitions: (text, row, col, columnspan, rowspan, type, command_val)
        # Type can be 'number', 'operator', 'equals', 'clear', 'special_op'
        buttons = [
            ("C", 0, 0, 1, 1, "clear", "C"),  ("Log", 0, 1, 1, 1, "special_op", "Logarithm"), ("^", 0, 2, 1, 1, "operator", "Power"), ("/", 0, 3, 1, 1, "operator", "Division"),
            ("7", 1, 0, 1, 1, "number", "7"), ("8", 1, 1, 1, 1, "number", "8"), ("9", 1, 2, 1, 1, "number", "9"), ("*", 1, 3, 1, 1, "operator", "Multiplication"),
            ("4", 2, 0, 1, 1, "number", "4"), ("5", 2, 1, 1, 1, "number", "5"), ("6", 2, 2, 1, 1, "number", "6"), ("-", 2, 3, 1, 1, "operator", "Subtraction"),
            ("1", 3, 0, 1, 1, "number", "1"), ("2", 3, 1, 1, 1, "number", "2"), ("3", 3, 2, 1, 1, "number", "3"), ("+", 3, 3, 1, 1, "operator", "Addition"),
            ("0", 4, 0, 2, 1, "number", "0"), (".", 4, 2, 1, 1, "number", "."), ("=", 4, 3, 1, 1, "equals", "=")
        ]

        button_font = ("Arial", 16)
        button_bg_color = "#ECF0F1" # Light grey for numbers
        button_fg_color = "#2C3E50" # Dark text
        op_button_bg_color = "#E67E22" # Orange for operators
        op_button_fg_color = "#FFFFFF" # White text
        eq_button_bg_color = "#2ECC71" # Green for equals
        clear_button_bg_color = "#E74C3C" # Red for clear

        for i in range(5): # Rows for buttons
            button_frame.grid_rowconfigure(i, weight=1)
        for i in range(4): # Columns for buttons
            button_frame.grid_columnconfigure(i, weight=1)

        for btn_text, row, col, cspan, rspan, btn_type, cmd_val in buttons:
            action = lambda v=cmd_val, t=btn_type: self._on_button_click(v, t)
            
            bg_c = button_bg_color
            fg_c = button_fg_color
            if btn_type == "operator" or btn_type == "special_op":
                bg_c = op_button_bg_color
                fg_c = op_button_fg_color
            elif btn_type == "equals":
                bg_c = eq_button_bg_color
                fg_c = op_button_fg_color
            elif btn_type == "clear":
                bg_c = clear_button_bg_color
                fg_c = op_button_fg_color

            button = tk.Button(
                button_frame,
                text=btn_text,
                font=button_font,
                bg=bg_c,
                fg=fg_c,
                relief=tk.RAISED,
                bd=3,
                padx=20,
                pady=20,
                command=action
            )
            button.grid(row=row, column=col, columnspan=cspan, rowspan=rspan, sticky="nsew", padx=5, pady=5)


    # --- Event Handlers ---
    def _on_button_click(self, value, btn_type):
        """Handles clicks on any calculator button."""
        try:
            if btn_type == "number":
                self._handle_number(value)
            elif btn_type == "operator" or btn_type == "special_op":
                self._handle_operator(value) # 'value' here is the operation name
            elif btn_type == "equals":
                self._handle_equals()
            elif btn_type == "clear":
                self._handle_clear()
        except Exception as e:
            self._show_error(f"App Error: {e}")


    def _handle_number(self, digit):
        """Handles number and decimal point button clicks."""
        if self.result_displayed: # If a result was just shown, start new input
            self.current_input = ""
            self.result_displayed = False

        if digit == "." and "." in self.current_input:
            return # Allow only one decimal point

        if self.current_input == "0" and digit != ".": # Avoid leading zeros like "07"
             self.current_input = digit
        else:
            self.current_input += digit
        self.display_var.set(self.current_input if self.current_input else "0")

    def _handle_operator(self, op_name):
        """Handles operator button clicks (+, -, *, /, Power, Log)."""
        if self.current_input: # We have a number to operate on
            if self.first_operand is not None and self.operation is not None:
                # This means an operation is pending, like 5 + 3 then user presses *
                # We should calculate the pending operation first
                self._handle_equals(intermediate_calc=True)

            try:
                self.first_operand = float(self.current_input)
                self.operation = op_name # e.g., "Addition", "Power"
                self.current_input = ""
                self.result_displayed = False # Ready for next number
                # Optionally show the first operand and operator in display, or clear for next input
                # For now, we clear and wait for the second number
                self.display_var.set(f"{self.first_operand} {self._get_op_symbol(op_name)}")

            except ValueError:
                self._show_error("Invalid Input")
        elif self.first_operand is not None: # Allow changing operator if no new number entered
             self.operation = op_name
             self.display_var.set(f"{self.first_operand} {self._get_op_symbol(op_name)}")


    def _get_op_symbol(self, op_name):
        symbols = {
            "Addition": "+", "Subtraction": "-", "Multiplication": "*", "Division": "/",
            "Power": "^", "Logarithm": "log"
        }
        return symbols.get(op_name, "")


    def _handle_equals(self, intermediate_calc=False):
        """Handles the equals button click or intermediate calculation."""
        if self.operation and self.first_operand is not None and self.current_input:
            try:
                second_operand = float(self.current_input)
                if self.operation in self.calc_functions:
                    calculation_method = self.calc_functions[self.operation]
                    result = calculation_method(self.first_operand, second_operand)

                    if isinstance(result, str) and "Error" in result: # Error from calc func
                        self._show_error(result)
                        self._reset_state_after_error()
                    else:
                        # Format result nicely (e.g., remove .0 for integers)
                        if isinstance(result, float) and result.is_integer():
                            formatted_result = str(int(result))
                        else:
                            formatted_result = f"{result:.10g}" # Show up to 10 significant digits

                        self.display_var.set(formatted_result)
                        self.current_input = formatted_result # Result becomes current input for chaining
                        if not intermediate_calc:
                            self.result_displayed = True
                            self.first_operand = None # Clear first operand after direct equals
                            self.operation = None
                        else: # For intermediate calculations like 5 + 3 *
                            self.first_operand = float(formatted_result) # Result becomes new first_operand
                            # self.operation remains for the next part of the chain (set by new operator press)
                            self.current_input = "" # Ready for next number
                            self.result_displayed = False


                else:
                    self._show_error("Unknown Operation")
                    self._reset_state_after_error()

            except ValueError:
                self._show_error("Invalid Number")
                self._reset_state_after_error()
            except Exception as e:
                self._show_error(f"Calc Error: {e}")
                self._reset_state_after_error()
        # else: do nothing if not enough info for calculation


    def _handle_clear(self):
        """Handles the clear (C) button click."""
        self.current_input = ""
        self.first_operand = None
        self.operation = None
        self.result_displayed = False
        self.display_var.set("0")

    def _reset_state_after_error(self):
        """Resets calculator state after an error occurs during calculation."""
        self.current_input = ""
        self.first_operand = None
        self.operation = None
        self.result_displayed = True # So next number press clears the error message

    def _show_error(self, message):
        """Displays an error message on the calculator screen."""
        self.display_var.set(message)
        # Optionally use messagebox for more prominent errors:
        # messagebox.showerror("Calculator Error", message)


# --- Main Application Setup ---
if __name__ == "__main__":
    main_window = tk.Tk()
    calculator_app = KingXCalculator(main_window)
    main_window.mainloop()