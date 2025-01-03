#!/usr/bin/env python3.11
# -*- coding: utf-8 -*-
"""
# Quanta is a variable quantum calculater for qubit states and gates. This program will help understand states while building programs or systems for QPU's or qpu like services.

I built this to understand the spin variables for sub-bit processing in qubit states.

"""
import sys
import os
import logging
import traceback
import threading
import multiprocessing
import queue
from typing import Optional, Dict
import numpy as np
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit.circuit import Parameter
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, ttk

# Configure Logging
logging.basicConfig(
    filename='quantum_verse_calculator.log',
    filemode='a',
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# --- Quantum Calculator Functionalities ---

class QuantumCalculator:
    def __init__(self):
        self.backend = AerSimulator(method='statevector')
        logging.info("QuantumCalculator initialized with AerSimulator (statevector).")

    def observe_qubits(self, num_qubits: int, shots: int = 1024) -> Dict[str, int]:
        try:
            circuit = QuantumCircuit(num_qubits, num_qubits)
            circuit.h(range(num_qubits))
            circuit.measure(range(num_qubits), range(num_qubits))
            circuit.save_statevector()
            job = self.backend.run(circuit, shots=shots)
            result = job.result()
            counts = result.get_counts(circuit)
            logging.info(f"Observed qubits: {counts}")
            return counts
        except Exception as e:
            logging.error(f"Error in observe_qubits: {e}")
            raise

    def calculate_error_rates(self, num_qubits: int, shots: int = 1024) -> float:
        try:
            counts = self.observe_qubits(num_qubits, shots)
            total = sum(counts.values())
            errors = 0
            for outcome, count in counts.items():
                if '1' in outcome:
                    errors += count
            error_rate = errors / total
            logging.info(f"Calculated error rate: {error_rate}")
            return error_rate
        except Exception as e:
            logging.error(f"Error in calculate_error_rates: {e}")
            raise

    def calculate_gate_variables(self, gate_type: str, angle: float = 0.0, qubit: int = 0) -> QuantumCircuit:
        try:
            circuit = QuantumCircuit(qubit + 1)
            if gate_type.upper() == 'RX':
                circuit.rx(angle, qubit)
            elif gate_type.upper() == 'RY':
                circuit.ry(angle, qubit)
            elif gate_type.upper() == 'RZ':
                circuit.rz(angle, qubit)
            elif gate_type.upper() == 'H':
                circuit.h(qubit)
            elif gate_type.upper() == 'X':
                circuit.x(qubit)
            else:
                raise ValueError("Unsupported gate type.")
            circuit.save_statevector()
            logging.info(f"Applied gate {gate_type} with angle {angle} on qubit {qubit}.")
            return circuit
        except Exception as e:
            logging.error(f"Error in calculate_gate_variables: {e}")
            raise

    def calculate_spin(self, qubit_state: Optional[str] = None) -> float:
        try:
            circuit = QuantumCircuit(1, 1)
            if qubit_state == '1':
                circuit.x(0)
            circuit.h(0)
            circuit.measure(0, 0)
            circuit.save_statevector()
            job = self.backend.run(circuit, shots=1024)
            result = job.result()
            counts = result.get_counts(circuit)
            ones = counts.get('1', 0)
            spin = ones / 1024
            logging.info(f"Calculated spin: {spin}")
            return spin
        except Exception as e:
            logging.error(f"Error in calculate_spin: {e}")
            raise

    def grovers_speed_between_qubits(self, target_state: str, num_qubits: int) -> float:
        try:
            from qiskit.algorithms import Grover
            from qiskit.circuit.library import ZGate

            if len(target_state) != num_qubits:
                raise ValueError("Target state length must match the number of qubits.")

            oracle = QuantumCircuit(num_qubits)
            for idx, bit in enumerate(target_state):
                if bit == '0':
                    oracle.x(idx)
            oracle.cz(num_qubits - 1, num_qubits - 2)  # Example two-qubit CZ gate as oracle
            for idx, bit in enumerate(target_state):
                if bit == '0':
                    oracle.x(idx)
            oracle.save_statevector()

            grover = Grover(oracle=oracle)
            result = grover.run(self.backend)
            iterations = result.optimal_num_iterations
            speed = iterations  # Placeholder for actual speed calculation
            logging.info(f"Grover's algorithm iterations: {iterations}")
            return speed
        except ImportError:
            logging.error("Grover's algorithm module not found. Please ensure you have the latest version of Qiskit installed.")
            raise ImportError("Grover's algorithm module not found. Please update Qiskit using 'pip install --upgrade qiskit'.")
        except Exception as e:
            logging.error(f"Error in grovers_speed_between_qubits: {e}")
            raise

# --- GUI Implementation ---

class QuantumVerseCalculatorGUI:
    def __init__(self, master):
        self.master = master
        master.title("QuantumVerse Calculator")
        master.geometry("900x700")  # Increased size for better layout
        master.resizable(False, False)
        self.calculator = QuantumCalculator()
        self.create_widgets()
        self.log_queue = queue.Queue()
        self.master.after(100, self.process_log_queue)

    def create_widgets(self):
        style = ttk.Style()
        # Use a more modern font
        default_font = ("Helvetica", 10)
        style.configure(".", font=default_font)

        # Configure styles with black text and existing background colors
        style.configure("TButton",
                        padding=6,
                        relief="flat",
                        background="#4A90E2",  # Existing blue background
                        foreground="black",     # Changed text color to black
                        font=("Helvetica", 10, "bold"))
        style.map("TButton",
                  background=[('active', '#357ABD')])  # Slightly darker on hover

        style.configure("TLabel",
                        background="#2C3E50",    # Existing dark background
                        foreground="black",      # Changed text color to black
                        font=("Helvetica", 10))
        style.configure("TFrame",
                        background="#2C3E50")    # Existing dark background
        style.configure("TEntry",
                        fieldbackground="#34495E",  # Existing entry background
                        foreground="black",          # Changed text color to black
                        font=("Helvetica", 10))
        style.configure("TCombobox",
                        fieldbackground="#34495E",  # Existing combobox background
                        foreground="black",          # Changed text color to black
                        font=("Helvetica", 10))
        style.configure("TNotebook", background="#2C3E50")
        style.configure("TNotebook.Tab", background="#4A90E2", foreground="black", font=("Helvetica", 10, "bold"))
        style.map("TNotebook.Tab",
                  background=[('selected', '#357ABD')],
                  foreground=[('selected', 'black')])

        container = ttk.Frame(self.master, padding=10)
        container.pack(fill='both', expand=True)

        # Tabs
        self.notebook = ttk.Notebook(container)
        self.notebook.pack(fill='both', expand=True)

        # Observe Qubits Tab
        self.tab_observe = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_observe, text='Observe Qubits')
        self.create_observe_tab()

        # Error Rates Tab
        self.tab_error = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_error, text='Error Rates')
        self.create_error_tab()

        # Gate Variables Tab
        self.tab_gates = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_gates, text='Gate Variables')
        self.create_gates_tab()

        # Spin Calculation Tab
        self.tab_spin = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_spin, text='Calculate Spin')
        self.create_spin_tab()

        # Grover's Algorithm Tab
        self.tab_grover = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_grover, text="Grover's Speed")
        self.create_grover_tab()

        # Settings Tab
        self.tab_settings = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_settings, text="Settings")
        self.create_settings_tab()

        # Log Frame
        self.log_frame = ttk.LabelFrame(container, text="Logs", padding=10)
        self.log_frame.pack(fill='both', expand=True, pady=10)
        self.log_text = scrolledtext.ScrolledText(self.log_frame, state='disabled', wrap='word', bg="#34495E", fg="black", font=("Helvetica", 10))
        self.log_text.pack(fill='both', expand=True, padx=5, pady=5)

    def create_observe_tab(self):
        frame = ttk.Frame(self.tab_observe, padding=20)
        frame.pack(fill='both', expand=True)

        ttk.Label(frame, text="Number of Qubits:").grid(row=0, column=0, padx=10, pady=10, sticky='e')
        self.observe_qubits_entry = ttk.Entry(frame, width=15)
        self.observe_qubits_entry.insert(0, "2")
        self.observe_qubits_entry.grid(row=0, column=1, padx=10, pady=10, sticky='w')

        ttk.Label(frame, text="Shots:").grid(row=1, column=0, padx=10, pady=10, sticky='e')
        self.observe_shots_entry = ttk.Entry(frame, width=15)
        self.observe_shots_entry.insert(0, "1024")
        self.observe_shots_entry.grid(row=1, column=1, padx=10, pady=10, sticky='w')

        observe_button = ttk.Button(frame, text="Observe", command=self.observe_qubits)
        observe_button.grid(row=2, column=0, columnspan=2, pady=20)

        self.observe_result = scrolledtext.ScrolledText(frame, height=10, state='disabled', bg="#34495E", fg="black", font=("Helvetica", 10))
        self.observe_result.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

    def create_error_tab(self):
        frame = ttk.Frame(self.tab_error, padding=20)
        frame.pack(fill='both', expand=True)

        ttk.Label(frame, text="Number of Qubits:").grid(row=0, column=0, padx=10, pady=10, sticky='e')
        self.error_qubits_entry = ttk.Entry(frame, width=15)
        self.error_qubits_entry.insert(0, "2")
        self.error_qubits_entry.grid(row=0, column=1, padx=10, pady=10, sticky='w')

        ttk.Label(frame, text="Shots:").grid(row=1, column=0, padx=10, pady=10, sticky='e')
        self.error_shots_entry = ttk.Entry(frame, width=15)
        self.error_shots_entry.insert(0, "1024")
        self.error_shots_entry.grid(row=1, column=1, padx=10, pady=10, sticky='w')

        error_button = ttk.Button(frame, text="Calculate Error Rate", command=self.calculate_error_rate)
        error_button.grid(row=2, column=0, columnspan=2, pady=20)

        self.error_result = ttk.Label(frame, text="Error Rate: N/A", font=("Helvetica", 12, "bold"))
        self.error_result.grid(row=3, column=0, columnspan=2, pady=10)

    def create_gates_tab(self):
        frame = ttk.Frame(self.tab_gates, padding=20)
        frame.pack(fill='both', expand=True)

        ttk.Label(frame, text="Gate Type:").grid(row=0, column=0, padx=10, pady=10, sticky='e')
        self.gate_type_var = tk.StringVar()
        self.gate_type_combo = ttk.Combobox(frame, textvariable=self.gate_type_var, state='readonly', width=17)
        self.gate_type_combo['values'] = ('RX', 'RY', 'RZ', 'H', 'X')
        self.gate_type_combo.current(0)
        self.gate_type_combo.grid(row=0, column=1, padx=10, pady=10, sticky='w')

        ttk.Label(frame, text="Angle (for RX, RY, RZ):").grid(row=1, column=0, padx=10, pady=10, sticky='e')
        self.gate_angle_entry = ttk.Entry(frame, width=15)
        self.gate_angle_entry.insert(0, "0.0")
        self.gate_angle_entry.grid(row=1, column=1, padx=10, pady=10, sticky='w')

        ttk.Label(frame, text="Qubit Index:").grid(row=2, column=0, padx=10, pady=10, sticky='e')
        self.gate_qubit_entry = ttk.Entry(frame, width=15)
        self.gate_qubit_entry.insert(0, "0")
        self.gate_qubit_entry.grid(row=2, column=1, padx=10, pady=10, sticky='w')

        gate_button = ttk.Button(frame, text="Apply Gate", command=self.apply_gate)
        gate_button.grid(row=3, column=0, columnspan=2, pady=20)

        self.gate_result = scrolledtext.ScrolledText(frame, height=10, state='disabled', bg="#34495E", fg="black", font=("Helvetica", 10))
        self.gate_result.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

    def create_spin_tab(self):
        frame = ttk.Frame(self.tab_spin, padding=20)
        frame.pack(fill='both', expand=True)

        ttk.Label(frame, text="Qubit State:").grid(row=0, column=0, padx=10, pady=10, sticky='e')
        self.spin_state_var = tk.StringVar()
        self.spin_state_combo = ttk.Combobox(frame, textvariable=self.spin_state_var, state='readonly', width=17)
        self.spin_state_combo['values'] = ('0', '1')
        self.spin_state_combo.current(0)
        self.spin_state_combo.grid(row=0, column=1, padx=10, pady=10, sticky='w')

        spin_button = ttk.Button(frame, text="Calculate Spin", command=self.calculate_spin)
        spin_button.grid(row=1, column=0, columnspan=2, pady=20)

        self.spin_result = ttk.Label(frame, text="Spin: N/A", font=("Helvetica", 12, "bold"))
        self.spin_result.grid(row=2, column=0, columnspan=2, pady=10)

    def create_grover_tab(self):
        frame = ttk.Frame(self.tab_grover, padding=20)
        frame.pack(fill='both', expand=True)

        ttk.Label(frame, text="Target State (binary):").grid(row=0, column=0, padx=10, pady=10, sticky='e')
        self.grover_target_entry = ttk.Entry(frame, width=20)
        self.grover_target_entry.insert(0, "11")
        self.grover_target_entry.grid(row=0, column=1, padx=10, pady=10, sticky='w')

        ttk.Label(frame, text="Number of Qubits:").grid(row=1, column=0, padx=10, pady=10, sticky='e')
        self.grover_qubits_entry = ttk.Entry(frame, width=20)
        self.grover_qubits_entry.insert(0, "2")
        self.grover_qubits_entry.grid(row=1, column=1, padx=10, pady=10, sticky='w')

        grover_button = ttk.Button(frame, text="Run Grover's Algorithm", command=self.run_grovers)
        grover_button.grid(row=2, column=0, columnspan=2, pady=20)

        self.grover_result = ttk.Label(frame, text="Grover's Speed: N/A", font=("Helvetica", 12, "bold"))
        self.grover_result.grid(row=3, column=0, columnspan=2, pady=10)

    def create_settings_tab(self):
        frame = ttk.Frame(self.tab_settings, padding=20)
        frame.pack(fill='both', expand=True)

        # Font Size Setting
        ttk.Label(frame, text="Font Size:").grid(row=0, column=0, padx=10, pady=10, sticky='e')
        self.font_size_var = tk.IntVar(value=10)
        self.font_size_spinbox = ttk.Spinbox(frame, from_=8, to=20, textvariable=self.font_size_var, width=5, command=self.update_font_size)
        self.font_size_spinbox.grid(row=0, column=1, padx=10, pady=10, sticky='w')

        # Theme Selection
        ttk.Label(frame, text="Theme:").grid(row=1, column=0, padx=10, pady=10, sticky='e')
        self.theme_var = tk.StringVar(value="Dark")
        self.theme_combo = ttk.Combobox(frame, textvariable=self.theme_var, state='readonly', width=17)
        self.theme_combo['values'] = ('Dark', 'Light')
        self.theme_combo.current(0)
        self.theme_combo.grid(row=1, column=1, padx=10, pady=10, sticky='w')
        self.theme_combo.bind("<<ComboboxSelected>>", self.change_theme)

        # Apply Button
        apply_button = ttk.Button(frame, text="Apply Settings", command=self.apply_settings)
        apply_button.grid(row=2, column=0, columnspan=2, pady=20)

    def update_font_size(self):
        new_size = self.font_size_var.get()
        default_font = ("Helvetica", new_size)
        for widget in self.master.winfo_children():
            try:
                widget.configure(font=default_font)
            except:
                pass

    def change_theme(self, event):
        theme = self.theme_var.get()
        if theme == "Light":
            self.master.configure(bg="#ECF0F1")  # Light background
            style = ttk.Style()
            style.configure("TButton",
                            background="#4A90E2",
                            foreground="black",
                            font=("Helvetica", 10, "bold"))
            style.map("TButton",
                      background=[('active', '#357ABD')])
            style.configure("TLabel",
                            background="#ECF0F1",
                            foreground="black",
                            font=("Helvetica", 10))
            style.configure("TFrame",
                            background="#ECF0F1")
            style.configure("TEntry",
                            fieldbackground="#ffffff",
                            foreground="black",
                            font=("Helvetica", 10))
            style.configure("TCombobox",
                            fieldbackground="#ffffff",
                            foreground="black",
                            font=("Helvetica", 10))
            style.configure("TNotebook", background="#ECF0F1")
            style.configure("TNotebook.Tab", background="#4A90E2", foreground="black", font=("Helvetica", 10, "bold"))
            style.map("TNotebook.Tab",
                      background=[('selected', '#357ABD')],
                      foreground=[('selected', 'black')])
            self.log_text.config(bg="#ffffff", fg="black")
        else:
            self.master.configure(bg="#2C3E50")  # Dark background
            style = ttk.Style()
            style.configure("TButton",
                            background="#4A90E2",
                            foreground="black",
                            font=("Helvetica", 10, "bold"))
            style.map("TButton",
                      background=[('active', '#357ABD')])
            style.configure("TLabel",
                            background="#2C3E50",
                            foreground="black",
                            font=("Helvetica", 10))
            style.configure("TFrame",
                            background="#2C3E50")
            style.configure("TEntry",
                            fieldbackground="#34495E",
                            foreground="black",
                            font=("Helvetica", 10))
            style.configure("TCombobox",
                            fieldbackground="#34495E",
                            foreground="black",
                            font=("Helvetica", 10))
            style.configure("TNotebook", background="#2C3E50")
            style.configure("TNotebook.Tab", background="#4A90E2", foreground="black", font=("Helvetica", 10, "bold"))
            style.map("TNotebook.Tab",
                      background=[('selected', '#357ABD')],
                      foreground=[('selected', 'black')])
            self.log_text.config(bg="#34495E", fg="black")

    def apply_settings(self):
        self.update_font_size()
        # Theme is already changed on selection
        self.log("Applied new settings.")

    def observe_qubits(self):
        try:
            num_qubits = int(self.observe_qubits_entry.get())
            shots = int(self.observe_shots_entry.get())
            if num_qubits <= 0 or shots <= 0:
                raise ValueError
            counts = self.calculator.observe_qubits(num_qubits, shots)
            self.observe_result.config(state='normal')
            self.observe_result.delete('1.0', tk.END)
            self.observe_result.insert(tk.END, f"Measurement Results:\n{counts}")
            self.observe_result.config(state='disabled')
            self.log(f"Observed {num_qubits} qubits with {shots} shots.")
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter positive integers for qubits and shots.")
        except ImportError as ie:
            messagebox.showerror("Import Error", str(ie))
            logging.error(str(ie))
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
            logging.error(f"Error in observe_qubits: {e}")

    def calculate_error_rate(self):
        try:
            num_qubits = int(self.error_qubits_entry.get())
            shots = int(self.error_shots_entry.get())
            if num_qubits <= 0 or shots <= 0:
                raise ValueError
            error_rate = self.calculator.calculate_error_rates(num_qubits, shots)
            self.error_result.config(text=f"Error Rate: {error_rate:.4f}")
            self.log(f"Calculated error rate for {num_qubits} qubits with {shots} shots: {error_rate:.4f}")
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter positive integers for qubits and shots.")
        except ImportError as ie:
            messagebox.showerror("Import Error", str(ie))
            logging.error(str(ie))
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
            logging.error(f"Error in calculate_error_rates: {e}")

    def apply_gate(self):
        try:
            gate_type = self.gate_type_var.get()
            angle = float(self.gate_angle_entry.get())
            qubit = int(self.gate_qubit_entry.get())
            if qubit < 0:
                raise ValueError
            circuit = self.calculator.calculate_gate_variables(gate_type, angle, qubit)
            job = self.calculator.backend.run(circuit, shots=1024)
            result = job.result()
            statevector = result.get_statevector(circuit)
            counts = result.get_counts(circuit)
            self.gate_result.config(state='normal')
            self.gate_result.delete('1.0', tk.END)
            self.gate_result.insert(tk.END, f"Gate Applied: {gate_type} on Qubit {qubit}\n")
            self.gate_result.insert(tk.END, f"Statevector:\n{statevector}\n")
            self.gate_result.insert(tk.END, f"Measurement Results:\n{counts}")
            self.gate_result.config(state='disabled')
            self.log(f"Applied gate {gate_type} with angle {angle} on qubit {qubit}.")
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid qubit index and angle.")
        except ImportError as ie:
            messagebox.showerror("Import Error", str(ie))
            logging.error(str(ie))
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
            logging.error(f"Error in apply_gate: {e}")

    def calculate_spin(self):
        try:
            qubit_state = self.spin_state_var.get()
            spin = self.calculator.calculate_spin(qubit_state)
            self.spin_result.config(text=f"Spin: {spin:.4f}")
            self.log(f"Calculated spin for qubit state '{qubit_state}': {spin:.4f}")
        except ImportError as ie:
            messagebox.showerror("Import Error", str(ie))
            logging.error(str(ie))
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
            logging.error(f"Error in calculate_spin: {e}")

    def run_grovers(self):
        try:
            target_state = self.grover_target_entry.get().strip()
            num_qubits = int(self.grover_qubits_entry.get())
            if num_qubits <= 0 or not all(bit in '01' for bit in target_state):
                raise ValueError
            speed = self.calculator.grovers_speed_between_qubits(target_state, num_qubits)
            self.grover_result.config(text=f"Grover's Speed: {speed}")
            self.log(f"Ran Grover's algorithm for target state '{target_state}' with {num_qubits} qubits.")
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid binary target state and positive number of qubits.")
        except ImportError as ie:
            messagebox.showerror("Import Error", str(ie))
            logging.error(str(ie))
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
            logging.error(f"Error in grovers_speed_between_qubits: {e}")

    def log(self, message: str):
        self.log_queue.put(message)

    def process_log_queue(self):
        try:
            while not self.log_queue.empty():
                message = self.log_queue.get_nowait()
                self.log_text.config(state='normal')
                self.log_text.insert(tk.END, f"{message}\n")
                self.log_text.see(tk.END)
                self.log_text.config(state='disabled')
        except Exception as e:
            logging.error(f"Error processing log queue: {e}")
        finally:
            self.master.after(100, self.process_log_queue)

# --- Main Execution ---

def main():
    try:
        root = tk.Tk()
        root.configure(bg="#2C3E50")  # Maintain existing dark background
        app = QuantumVerseCalculatorGUI(root)
        root.mainloop()
    except Exception as e:
        error_trace = traceback.format_exc()
        logging.critical(f"Unexpected error:\n{error_trace}")
        messagebox.showerror("Unexpected Error", f"An unexpected error occurred:\n{e}\n\nCheck the log file for more details.")
        sys.exit(1)

if __name__ == "__main__":
    main()
