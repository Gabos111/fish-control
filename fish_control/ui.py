#!/usr/bin/env python3
import os
import yaml
import tkinter as tk
from tkinter import ttk, messagebox

# Path to cfg.yaml
CFG_PATH = os.path.abspath(os.path.join(
    os.path.dirname(__file__), "..", "cfg.yaml"
))

class FishControlGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Fish Control Center")
        self.resizable(False, False)
        self.load_cfg()
        self.create_widgets()

    def load_cfg(self):
        try:
            with open(CFG_PATH) as f:
                self.cfg = yaml.safe_load(f)
        except Exception:
            self.cfg = {
                "mode": "standby",
                "amplitude_tail": 20.0,
                "amplitude_fin": 20.0,
                "frequency": 0.3,
                "phase": 0.0,
                "phi_tail": 0.0,
                "phi_fin": 0.0,
                "logging": False
            }

    def save_cfg(self):
        # Build new config from widget values
        new_cfg = {
            "mode": self.mode_var.get(),
            "amplitude_tail": float(self.ampt_var.get()),
            "amplitude_fin": float(self.ampf_var.get()),
            "frequency": float(self.freq_var.get()),
            "phase": float(self.phase_var.get()),
            "phi_tail": float(self.phit_var.get()),
            "phi_fin": float(self.phif_var.get()),
            "logging": self.logging
        }
        try:
            with open(CFG_PATH, "w") as f:
                yaml.safe_dump(new_cfg, f)
            messagebox.showinfo("Success", "Configuration saved.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save: {e}")

    def toggle_logging(self):
        self.logging = not self.logging
        self.log_btn.config(text="Stop Logging" if self.logging else "Start Logging")

    def create_widgets(self):
        frame = ttk.Frame(self, padding=10)
        frame.grid()

        # Left column
        ttk.Label(frame, text="Mode:").grid(row=0, column=0, sticky="w")
        self.mode_var = tk.StringVar(value=self.cfg.get("mode"))
        ttk.Combobox(frame, textvariable=self.mode_var, values=["standby","test","symmetric_sin"], state="readonly")\
            .grid(row=0, column=1, sticky="ew")

        # Numeric parameters
        self.ampt_var = tk.DoubleVar(value=self.cfg.get("amplitude_tail"))
        ttk.Label(frame, text="Amplitude Tail:").grid(row=1, column=0, sticky="w")
        ttk.Entry(frame, textvariable=self.ampt_var).grid(row=1, column=1, sticky="ew")

        self.ampf_var = tk.DoubleVar(value=self.cfg.get("amplitude_fin"))
        ttk.Label(frame, text="Amplitude Fin:").grid(row=2, column=0, sticky="w")
        ttk.Entry(frame, textvariable=self.ampf_var).grid(row=2, column=1, sticky="ew")

        self.freq_var = tk.DoubleVar(value=self.cfg.get("frequency"))
        ttk.Label(frame, text="Frequency:").grid(row=3, column=0, sticky="w")
        ttk.Entry(frame, textvariable=self.freq_var).grid(row=3, column=1, sticky="ew")

        self.phase_var = tk.DoubleVar(value=self.cfg.get("phase"))
        ttk.Label(frame, text="Phase:").grid(row=4, column=0, sticky="w")
        ttk.Entry(frame, textvariable=self.phase_var).grid(row=4, column=1, sticky="ew")

        # Test angles
        self.phit_var = tk.DoubleVar(value=self.cfg.get("phi_tail"))
        ttk.Label(frame, text="Phi Tail (test):").grid(row=5, column=0, sticky="w")
        ttk.Entry(frame, textvariable=self.phit_var).grid(row=5, column=1, sticky="ew")

        self.phif_var = tk.DoubleVar(value=self.cfg.get("phi_fin"))
        ttk.Label(frame, text="Phi Fin (test):").grid(row=6, column=0, sticky="w")
        ttk.Entry(frame, textvariable=self.phif_var).grid(row=6, column=1, sticky="ew")

        # Logging
        self.logging = self.cfg.get("logging", False)
        self.log_btn = ttk.Button(frame, text=("Stop Logging" if self.logging else "Start Logging"),
                                  command=self.toggle_logging)
        self.log_btn.grid(row=7, column=0, columnspan=2, pady=(10, 0), sticky="ew")

        # Apply button
        ttk.Button(frame, text="Apply", command=self.save_cfg)\
            .grid(row=8, column=0, columnspan=2, pady=(5, 0), sticky="ew")

        # Expand columns
        frame.columnconfigure(0, weight=1)
        frame.columnconfigure(1, weight=3)

if __name__ == "__main__":
    app = FishControlGUI()
    app.mainloop()