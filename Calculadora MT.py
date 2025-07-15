#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      AlbertoAlvarez
#
# Created:     10/07/2025
# Copyright:   (c) AlbertoAlvarez 2025
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import tkinter as tk
from tkinter import ttk, messagebox
import math

# Bibliotecas de cables: subterráneos y aéreos, aluminio y cobre
cable_data_sub_Al = {
    50: {"Ia": 130, "R": 0.8180, "X": 0.24},
    70: {"Ia": 160, "R": 0.5650, "X": 0.23},
    95: {"Ia": 190, "R": 0.4080, "X": 0.22},
    120:{"Ia": 215, "R": 0.3230, "X": 0.21},
    150:{"Ia": 245, "R": 0.2630, "X": 0.20},
    185:{"Ia": 280, "R": 0.2100, "X": 0.20},
    240:{"Ia": 320, "R": 0.1610, "X": 0.19},
    300:{"Ia": 365, "R": 0.1300, "X": 0.19},
    400:{"Ia": 415, "R": 0.1020, "X": 0.18},
    500:{"Ia": 480, "R": 0.0805, "X": 0.17},
    630:{"Ia": 545, "R": 0.0640, "X": 0.16},
}

cable_data_sub_Cu = {
    50: {"Ia": 225, "R": 0.3870, "X": 0.18},
    70: {"Ia": 260, "R": 0.2760, "X": 0.17},
    95: {"Ia": 305, "R": 0.2010, "X": 0.16},
    120:{"Ia": 345, "R": 0.1590, "X": 0.16},
    150:{"Ia": 395, "R": 0.1260, "X": 0.15},
    185:{"Ia": 445, "R": 0.1020, "X": 0.15},
    240:{"Ia": 510, "R": 0.0772, "X": 0.14},
    300:{"Ia": 575, "R": 0.0601, "X": 0.14},
    400:{"Ia": 665, "R": 0.0450, "X": 0.13},
}

overhead_data_Al = {
    50: {"Ia": 145, "R": 0.50,   "X": 0.35},
    70: {"Ia": 185, "R": 0.31,   "X": 0.35},
    95: {"Ia": 225, "R": 0.243,  "X": 0.35},
    120:{"Ia": 260, "R": 0.190,  "X": 0.35},
    150:{"Ia": 300, "R": 0.152,  "X": 0.35},
    185:{"Ia": 340, "R": 0.120,  "X": 0.35},
    240:{"Ia": 400, "R": 0.0917, "X": 0.35},
    300:{"Ia": 450, "R": 0.0745, "X": 0.35},
    400:{"Ia": 530, "R": 0.0562, "X": 0.35},
}

overhead_data_Cu = {
    50: {"Ia": 260, "R": 0.24,  "X": 0.28},
    70: {"Ia": 325, "R": 0.17,  "X": 0.27},
    95: {"Ia": 380, "R": 0.123, "X": 0.26},
    120:{"Ia": 440, "R": 0.097, "X": 0.26},
    150:{"Ia": 510, "R": 0.077, "X": 0.25},
    185:{"Ia": 585, "R": 0.058, "X": 0.25},
    240:{"Ia": 680, "R": 0.043, "X": 0.24},
    300:{"Ia": 780, "R": 0.034, "X": 0.23},
}

# Tablas de factores de corrección (referencia típica)
factores_tabla = {
    'Ca (Temp ambiente)': [
        ('15°C', 1.08), ('20°C', 1.04), ('25°C', 1.00),
        ('30°C', 0.94), ('35°C', 0.88), ('40°C', 0.82)
    ],
    'Cd (Agrupamiento)': [
        ('1 cable', 1.00), ('2 cables', 0.80), ('3 cables', 0.70), ('4 cables', 0.65)
    ],
    'Ci (Instal. interior)': [
        ('Conducto ventilado', 1.00), ('Conducto no ventilado', 0.90),
        ('Canaleta', 0.75), ('Empotrado', 0.50)
    ],
    'Cg (Suelo)': [
        ('50 Ω·m', 1.00), ('100 Ω·m', 0.92), ('150 Ω·m', 0.85), ('200 Ω·m', 0.80)
    ]
}

class MTApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Cálculo de Líneas MT")
        self.resultados = []

        # Entradas de parámetros
        params = ["cos φ:", "Sistema:", "Tensión (kV):", "ID Tramo:",
                  "Longitud (m):", "Potencia Pn (MW):", "Ca:", "Cd:", "Ci:", "Cg:"]
        for i, txt in enumerate(params):
            tk.Label(self, text=txt).grid(row=i, column=0, sticky="e", padx=5, pady=2)

        self.entry_cos = tk.Entry(self);      self.entry_cos.grid(row=0, column=1)
        self.tipo_var = tk.StringVar(value="trifasico")
        fr = tk.Frame(self); fr.grid(row=1, column=1, columnspan=2, sticky="w")
        tk.Radiobutton(fr, text="Monofásico", variable=self.tipo_var, value="monofasico").pack(side="left")
        tk.Radiobutton(fr, text="Trifásico", variable=self.tipo_var, value="trifasico").pack(side="left")
        self.entry_v   = tk.Entry(self);      self.entry_v.grid(row=2, column=1)
        self.entry_id  = tk.Entry(self);      self.entry_id.grid(row=3, column=1)
        self.entry_L   = tk.Entry(self);      self.entry_L.grid(row=4, column=1)
        self.entry_Pn  = tk.Entry(self);      self.entry_Pn.grid(row=5, column=1)

        self.corre_vars = {}
        for j, f in enumerate(["Ca","Cd","Ci","Cg"], start=6):
            ent = tk.Entry(self); ent.insert(0, "1.0")
            ent.grid(row=j, column=1)
            self.corre_vars[f] = ent

        # Instalación y material
        tk.Label(self, text="Instalación:").grid(row=10, column=0, sticky="e")
        self.inst_var = tk.StringVar(value="subterraneo")
        insf = tk.Frame(self); insf.grid(row=10, column=1, columnspan=2, sticky="w")
        tk.Radiobutton(insf, text="Subterráneo", variable=self.inst_var, value="subterraneo").pack(side="left")
        tk.Radiobutton(insf, text="Aéreo",      variable=self.inst_var, value="aereo").pack(side="left")

        tk.Label(self, text="Material:").grid(row=11, column=0, sticky="e")
        self.mat_var = tk.StringVar(value="Al")
        matf = tk.Frame(self); matf.grid(row=11, column=1, columnspan=2, sticky="w")
        tk.Radiobutton(matf, text="Aluminio", variable=self.mat_var, value="Al").pack(side="left")
        tk.Radiobutton(matf, text="Cobre",     variable=self.mat_var, value="Cu").pack(side="left")

        # Botones
        tk.Button(self, text="Tablas Factores", command=self.mostrar_tablas).grid(row=12, column=0)
        tk.Button(self, text="Siguiente: Sección", command=self.mostrar_seleccion).grid(row=12, column=1, columnspan=2)

    def mostrar_tablas(self):
        win = tk.Toplevel(self)
        win.title("Tablas de Factores de Corrección")
        text = tk.Text(win, width=50, height=20)
        for title, rows in factores_tabla.items():
            text.insert(tk.END, f"{title}\n")
            for k,v in rows:
                text.insert(tk.END, f"  {k:15} -> {v}\n")
            text.insert(tk.END, "\n")
        text.config(state=tk.DISABLED)
        text.pack(padx=10, pady=10)

    def mostrar_seleccion(self):
        try:
            cos_phi = float(self.entry_cos.get())
            tipo    = self.tipo_var.get()
            V_kV    = float(self.entry_v.get())
            ID      = self.entry_id.get().strip()
            L_km    = float(self.entry_L.get())/1000
            Pn_W    = float(self.entry_Pn.get())*1e6
        except ValueError:
            messagebox.showerror("Error","Revisa campos numéricos completos")
            return
        k_total = math.prod(float(e.get()) for e in self.corre_vars.values())
        In = Pn_W/(math.sqrt(3)*V_kV*1000*cos_phi) if tipo=="trifasico" else Pn_W/(V_kV*1000*cos_phi)
        # Selección dict
        if self.inst_var.get()=="aereo":
            data_dict = overhead_data_Al if self.mat_var.get()=="Al" else overhead_data_Cu
        else:
            data_dict = cable_data_sub_Al if self.mat_var.get()=="Al" else cable_data_sub_Cu
        rec = next((s for s,d in sorted(data_dict.items()) if d["Ia"]*k_total>=In), None)
        rec = rec or max(data_dict)
        sec_win = tk.Toplevel(self)
        sec_win.title("Selección de Sección")
        tk.Label(sec_win, text=f"In = {In:.1f} A").pack()
        tk.Label(sec_win, text=f"Sección mínima: {rec} mm²").pack()
        self.sec_var = tk.IntVar(value=rec)
        ttk.Combobox(sec_win, values=list(data_dict), textvariable=self.sec_var, state="readonly").pack(pady=5)
        tk.Button(sec_win,text="Confirmar", command=lambda: self.confirmar_seccion(sec_win,In,Pn_W,L_km,cos_phi,tipo,k_total,data_dict)).pack(pady=10)

    def confirmar_seccion(self,win,In,Pn_W,L_km,cos_phi,tipo,k_total,data_dict):
        sec = self.sec_var.get();win.destroy()
        # si aéreo se fuerza Cg=1
        if self.inst_var.get()=="aereo":
            self.corre_vars["Cg"].delete(0,tk.END);self.corre_vars["Cg"].insert(0,"1.0")
            k_total = math.prod(float(e.get()) for e in self.corre_vars.values())
        data = data_dict[sec]
        Iac = data["Ia"]*k_total
        if In>Iac: messagebox.showwarning("Sección insuficiente",f"In {In:.1f}A > Iac {Iac:.1f}A para {sec}mm²")
        sinφ=math.sqrt(1-cos_phi**2)
        Kd,Kl=(math.sqrt(3),3) if tipo=="trifasico" else (2,2)
        deltaU_pct = (Kd*In*(data["R"]*cos_phi+data["X"]*sinφ)*L_km)/(float(self.entry_v.get())*1000)*100
        P_perd_W = Kl*In**2*data["R"]*L_km;Ppn_kW=P_perd_W/1000
        if deltaU_pct>5: messagebox.showerror("Caída alta",f"ΔU {deltaU_pct:.2f}% >5%")
        elif deltaU_pct>3: messagebox.showwarning("Caída moderada",f"ΔU {deltaU_pct:.2f}% >3%")
        Pperd_pct=(P_perd_W/Pn_W*100) if Pn_W else 0
        self.resultados.append({"ID":self.entry_id.get(),"Ppn_kW":Ppn_kW,"P_perd_W":P_perd_W,"ΔU_%":deltaU_pct,"Pperd_%":Pperd_pct})
        if messagebox.askyesno("Tramo calculado","Añadir otro tramo? "):
            for e in [self.entry_id,self.entry_L,self.entry_Pn]+list(self.corre_vars.values()): e.delete(0,tk.END);
            for f in self.corre_vars.values(): f.insert(0,"1.0")
        else: self.mostrar_resultado_final()

    def mostrar_resultado_final(self):
        win=tk.Toplevel(self);win.title("Resumen")
        tree=ttk.Treeview(win,columns=("ID","Ppn_kW","Pérdida_W","ΔU_%","Pperd_%"),show="headings")
        for c in tree["columns"]: tree.heading(c,text=c);tree.column(c,anchor="center")
        for r in self.resultados: tree.insert("","end",values=(r["ID"],f"{r['Ppn_kW']:.2f}",f"{int(r['P_perd_W'])}",f"{r['ΔU_%']:.2f}",f"{r['Pperd_%']:.3f}"))
        tree.pack(expand=True,fill="both",padx=10,pady=10)
        total=sum(r['Ppn_kW'] for r in self.resultados)
        tk.Label(win,text=f"Pérdida total: {total:.2f} kW").pack(pady=5)

if __name__=="__main__":
    app=MTApp();app.mainloop()

