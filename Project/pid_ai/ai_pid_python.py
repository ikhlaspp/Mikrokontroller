
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import time, threading, csv
import numpy as np
import imclab
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

class AIPIDApp:
    def __init__(self, root):
        self.root = root
        self.root.title("iMCLab AI PID Controller (XGBoost + Serial)")
        self.root.geometry("1450x900")

        # ===== PID PARAMETER (STABLE) =====
        self.kp = 0.005
        self.ki = 0.005
        self.kd = 0.002

        self.setpoint = 0.0
        self.running = False
        self.lab = None
        self.use_ai = tk.BooleanVar(value=True)

        self.integral = 0.0
        self.prev_rpm = 0.0
        self.rpm_filtered = 0.0

        self.time_data, self.sp_data, self.rpm_data = [], [], []
        self.window_size = 200
        self.start_time = 0

        self.build_ui()
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    # ================= UI =================
    def build_ui(self):
        main = tk.Frame(self.root)
        main.pack(fill="both", expand=True)

        left = ttk.LabelFrame(main, text="Control Panel")
        left.pack(side="left", fill="y", padx=10, pady=10)

        ttk.Label(left, text="Connection", font=("Segoe UI", 10, "bold")).pack(anchor="w")
        ttk.Button(left, text="Connect", command=self.connect_arduino).pack(fill="x")
        self.lbl_status = ttk.Label(left, text="Disconnected", foreground="red")
        self.lbl_status.pack(anchor="w", pady=(0,10))

        ttk.Label(left, text="Target RPM", font=("Segoe UI", 10, "bold")).pack(anchor="w")
        self.scale_sp = tk.Scale(left, from_=0, to=5000, orient=tk.HORIZONTAL)
        self.scale_sp.bind("<ButtonRelease-1>", self.on_setpoint_change)
        self.scale_sp.pack(fill="x")

        ttk.Checkbutton(left, text="Enable AI Auto Tuning",
                        variable=self.use_ai).pack(anchor="w", pady=5)

        self.btn_start = ttk.Button(left, text="Start PID", command=self.start_pid)
        self.btn_start.pack(fill="x", pady=5)

        self.btn_stop = ttk.Button(left, text="Stop PID", command=self.stop_pid, state="disabled")
        self.btn_stop.pack(fill="x", pady=5)

        ttk.Button(left, text="Export CSV", command=self.export_csv).pack(fill="x", pady=2)
        ttk.Button(left, text="Export Graph PNG", command=self.export_png).pack(fill="x", pady=2)

        self.lbl_rpm = ttk.Label(left, text="RPM: 0", font=("Segoe UI", 14, "bold"))
        self.lbl_rpm.pack(pady=10)

        # ===== RIGHT PANEL GRAPH =====
        right = tk.Frame(main)
        right.pack(side="right", fill="both", expand=True)

        header = tk.Frame(right, bg="#0078d4", height=45)
        header.pack(fill="x")
        tk.Label(header, text="Real-time Monitoring", bg="#0078d4",
                 fg="white", font=("Segoe UI", 12, "bold")).pack(pady=8)

        self.fig = Figure(figsize=(8,7), dpi=100)
        self.ax1 = self.fig.add_subplot(211)
        self.line_sp, = self.ax1.plot([], [], 'g--', label="Target")
        self.line_rpm, = self.ax1.plot([], [], 'r-', label="Actual")
        self.ax1.legend(); self.ax1.grid(alpha=0.3)

        self.ax2 = self.fig.add_subplot(212, sharex=self.ax1)
        self.line_err, = self.ax2.plot([], [], color="purple", label="Error (PV-SP)")
        self.ax2.axhline(0, color="black")
        self.ax2.legend(); self.ax2.grid(alpha=0.3)

        self.fig.tight_layout()
        self.canvas = FigureCanvasTkAgg(self.fig, master=right)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

    # ================= CONTROLS =================
    def connect_arduino(self):
        try:
            self.lab = imclab.iMCLab()
            self.lbl_status.config(text="Connected", foreground="green")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def on_setpoint_change(self, event):
        self.setpoint = float(self.scale_sp.get())

    def start_pid(self):
        if not self.lab:
            messagebox.showerror("Error", "Not connected")
            return
        self.running = True
        self.btn_start.config(state="disabled")
        self.btn_stop.config(state="normal")
        self.start_time = time.time()
        threading.Thread(target=self.pid_loop, daemon=True).start()
        self.animate_plot()

    def stop_pid(self):
        self.running = False
        self.btn_start.config(state="normal")
        self.btn_stop.config(state="disabled")
        if self.lab:
            self.lab.op(0)

    # ================= PID LOOP (UNCHANGED) =================
    def pid_loop(self):
        last_time = time.time()
        KICK_POWER = 83.0
        RPM_ALIVE = 500
        while self.running:
            now = time.time()
            if now - last_time >= 0.1:
                raw_rpm = getattr(self.lab, "RPM", 0)
                self.rpm_filtered = 0.7*self.rpm_filtered + 0.3*raw_rpm
                pv = self.rpm_filtered
                error = self.setpoint - pv

                P = self.kp * error
                self.integral += error * 0.1
                D = -self.kd * (pv - self.prev_rpm) / 0.1
                op = P + self.ki*self.integral + D

                if pv < RPM_ALIVE and op > 1:
                    op = max(op, KICK_POWER)
                else:
                    op = max(op, 55)

                op = max(0, min(100, op))
                self.lab.op(op)

                self.prev_rpm = pv
                last_time = now

                t = now - self.start_time
                self.time_data.append(t)
                self.sp_data.append(self.setpoint)
                self.rpm_data.append(pv)

                if len(self.time_data) > self.window_size:
                    self.time_data.pop(0); self.sp_data.pop(0); self.rpm_data.pop(0)

                self.root.after(0, self.lbl_rpm.config, {"text": f"RPM: {raw_rpm:.0f}"})
            time.sleep(0.01)

    # ================= GRAPH (FIXED) =================
    def animate_plot(self):
        self.line_sp.set_data(self.time_data, self.sp_data)
        self.line_rpm.set_data(self.time_data, self.rpm_data)

        err = np.array(self.rpm_data) - np.array(self.sp_data)
        self.line_err.set_data(self.time_data, err)

        if self.time_data:
            xmin, xmax = min(self.time_data), max(self.time_data) + 0.5
            self.ax1.set_xlim(xmin, xmax)
            self.ax1.set_ylim(0, max(self.sp_data + self.rpm_data) + 200)

            ymax = max(500, np.max(np.abs(err)) * 1.2)
            self.ax2.set_xlim(xmin, xmax)
            self.ax2.set_ylim(-ymax, ymax)

        self.canvas.draw()
        self.root.after(200, self.animate_plot)

    # ================= EXPORT =================
    def export_csv(self):
        file = filedialog.asksaveasfilename(defaultextension=".csv")
        if not file: return
        with open(file, "w", newline="") as f:
            w = csv.writer(f)
            w.writerow(["time","setpoint","rpm"])
            for i in range(len(self.time_data)):
                w.writerow([self.time_data[i], self.sp_data[i], self.rpm_data[i]])
        messagebox.showinfo("OK","CSV exported")

    def export_png(self):
        file = filedialog.asksaveasfilename(defaultextension=".png")
        if file:
            self.fig.savefig(file)
            messagebox.showinfo("OK","Graph exported")

    def on_close(self):
        self.running = False
        if self.lab:
            try:
                self.lab.op(0); self.lab.close()
            except: pass
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = AIPIDApp(root)
    root.mainloop()
