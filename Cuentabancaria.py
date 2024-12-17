import tkinter as tk
from tkinter import messagebox, simpledialog, ttk

class CuentaBancaria:
    cuentas = []  # Lista global para todas las cuentas
    transacciones = []  # Registro de transacciones

    def __init__(self, numero_cuenta, titular, tipo_cuenta, saldo=0.0):
        self.numero_cuenta = numero_cuenta
        self.titular = titular
        self.tipo_cuenta = tipo_cuenta
        self.saldo = saldo
        self.contactos = []  # Lista de contactos guardados
        CuentaBancaria.cuentas.append(self)

    def depositar(self, monto):
        if monto > 0:
            self.saldo += monto
            CuentaBancaria.transacciones.append(f"Depósito: +${monto:.2f} a {self.titular}")
            return f"Depósito exitoso. Nuevo saldo: ${self.saldo:.2f}"
        return "Error: El monto debe ser positivo."

    def transferir(self, monto, contacto):
        if monto <= 0:
            return "Error: El monto debe ser positivo."
        if monto > self.saldo:
            return "Error: Fondos insuficientes."
        self.saldo -= monto
        CuentaBancaria.transacciones.append(f"Transferencia: -${monto:.2f} a {contacto}")
        return f"Transferencia exitosa. Nuevo saldo: ${self.saldo:.2f}"

class BancoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Banco Móvil - Simulación")
        self.root.geometry("400x500")
        self.cuenta_actual = None

        # Inicializar el frame aquí antes de usarlo
        self.frame = tk.Frame(self.root, bg="yellow")
        self.frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.frame_inicio()

    def frame_inicio(self):
        self.limpiar_pantalla()  # Ahora esto está bien, ya que self.frame está inicializado
        tk.Label(self.frame, text="Registro de Usuario", bg="yellow", font=("Arial", 16)).pack(pady=10)
        tk.Label(self.frame, text="Usuario:", bg="yellow").pack()
        self.entry_usuario = tk.Entry(self.frame)
        self.entry_usuario.pack(pady=5)

        tk.Label(self.frame, text="Contraseña:", bg="yellow").pack()
        self.entry_contra = tk.Entry(self.frame, show="*")
        self.entry_contra.pack(pady=5)

        tk.Button(self.frame, text="Siguiente", command=self.crear_cuenta).pack(pady=10)

    def crear_cuenta(self):
        self.limpiar_pantalla()

        tk.Label(self.frame, text="Crear Cuenta", bg="yellow", font=("Arial", 16)).pack(pady=10)
        tk.Label(self.frame, text="Nombre del Titular:", bg="yellow").pack()
        self.entry_nombre = tk.Entry(self.frame)
        self.entry_nombre.pack(pady=5)

        tk.Label(self.frame, text="Número de Cuenta:", bg="yellow").pack()
        self.entry_numero = tk.Entry(self.frame)
        self.entry_numero.pack(pady=5)

        tk.Label(self.frame, text="Tipo (ahorro/corriente):", bg="yellow").pack()
        self.entry_tipo = tk.Entry(self.frame)
        self.entry_tipo.pack(pady=5)

        tk.Button(self.frame, text="Guardar", command=self.guardar_cuenta).pack(pady=10)

    def guardar_cuenta(self):
        nombre = self.entry_nombre.get().strip()
        numero = self.entry_numero.get().strip()
        tipo = self.entry_tipo.get().lower()

        if not nombre or not numero.isdigit() or tipo not in ["ahorro", "corriente"]:
            messagebox.showerror("Error", "Datos inválidos. Inténtelo de nuevo.")
            return

        self.cuenta_actual = CuentaBancaria(numero, nombre, tipo, saldo=0.0)
        messagebox.showinfo("Éxito", "Cuenta creada correctamente.")
        self.agregar_contactos()

    def agregar_contactos(self):
        self.limpiar_pantalla()
        tk.Label(self.frame, text="Agregar Contactos", bg="yellow", font=("Arial", 16)).pack(pady=10)
        tk.Label(self.frame, text="Nombre del Contacto:", bg="yellow").pack()
        self.entry_contacto_nombre = tk.Entry(self.frame)
        self.entry_contacto_nombre.pack(pady=5)

        tk.Label(self.frame, text="Número de Cuenta:", bg="yellow").pack()
        self.entry_contacto_cuenta = tk.Entry(self.frame)
        self.entry_contacto_cuenta.pack(pady=5)

        tk.Button(self.frame, text="Guardar Contacto", command=self.guardar_contacto).pack(pady=5)
        tk.Button(self.frame, text="Siguiente", command=self.mostrar_operaciones).pack(pady=5)

    def guardar_contacto(self):
        nombre = self.entry_contacto_nombre.get().strip()
        cuenta = self.entry_contacto_cuenta.get().strip()
        if nombre and cuenta.isdigit():
            self.cuenta_actual.contactos.append((nombre, cuenta))
            messagebox.showinfo("Éxito", "Contacto guardado.")
            self.entry_contacto_nombre.delete(0, tk.END)
            self.entry_contacto_cuenta.delete(0, tk.END)
        else:
            messagebox.showerror("Error", "Datos inválidos.")

    def mostrar_operaciones(self):
        self.limpiar_pantalla()
        tk.Label(self.frame, text="Saldo Disponible:", font=("Arial", 14), bg="yellow").pack(pady=5)
        self.saldo_label = tk.Label(self.frame, text=f"${self.cuenta_actual.saldo:.2f}", 
                                    font=("Arial", 18), bg="white", width=20)
        self.saldo_label.pack(pady=5)

        operaciones_frame = tk.Frame(self.frame, bg="yellow")
        operaciones_frame.pack(pady=20)

        tk.Button(operaciones_frame, text="Consultar Saldo", width=15, command=self.consultar_saldo).grid(row=0, column=0, padx=5, pady=5)
        tk.Button(operaciones_frame, text="Depositar", width=15, command=self.depositar).grid(row=0, column=1, padx=5, pady=5)
        tk.Button(operaciones_frame, text="Transferir", width=15, command=self.transferir).grid(row=1, column=0, padx=5, pady=5)
        tk.Button(operaciones_frame, text="Ver Transacciones", width=15, command=self.ver_transacciones).grid(row=1, column=1, padx=5, pady=5)

        # Botón Cerrar sesión en la parte inferior derecha
        cerrar_sesion_btn = tk.Button(self.frame, text="Cerrar sesión", command=self.cerrar_sesion)
        cerrar_sesion_btn.pack(side="bottom", anchor="e", padx=20, pady=10)

    def consultar_saldo(self):
        messagebox.showinfo("Saldo", f"Saldo disponible: ${self.cuenta_actual.saldo:.2f}")

    def depositar(self):
        monto = simpledialog.askfloat("Depositar", "Ingrese monto a depositar:")
        if monto:
            resultado = self.cuenta_actual.depositar(monto)
            self.actualizar_saldo()
            messagebox.showinfo("Resultado", resultado)

    def transferir(self):
        contactos = self.cuenta_actual.contactos
        if not contactos:
            messagebox.showinfo("Error", "No hay contactos guardados.")
            return

        ventana_transferencia = tk.Toplevel(self.root)
        ventana_transferencia.title("Transferir Dinero")
        ventana_transferencia.geometry("300x200")

        tk.Label(ventana_transferencia, text="Seleccione el contacto:").pack(pady=10)

        self.contacto_var = tk.StringVar()
        contactos_nombres = [f"{nombre} - {numero}" for nombre, numero in contactos]
        menu_contactos = ttk.Combobox(ventana_transferencia, textvariable=self.contacto_var, values=contactos_nombres)
        menu_contactos.pack(pady=10)

        tk.Button(ventana_transferencia, text="Transferir", command=lambda: self.realizar_transferencia(menu_contactos.get(), ventana_transferencia)).pack()

    def realizar_transferencia(self, contacto_seleccionado, ventana):
        if not contacto_seleccionado:
            messagebox.showerror("Error", "Debe seleccionar un contacto.")
            return
        monto = simpledialog.askfloat("Monto", "Ingrese monto a transferir:")
        if monto:
            resultado = self.cuenta_actual.transferir(monto, contacto_seleccionado)
            self.actualizar_saldo()
            messagebox.showinfo("Resultado", resultado)
            ventana.destroy()

    def ver_transacciones(self):
        transacciones = "\n".join(CuentaBancaria.transacciones) or "No hay transacciones aún."
        messagebox.showinfo("Transacciones", transacciones)

    def actualizar_saldo(self):
        self.saldo_label.config(text=f"${self.cuenta_actual.saldo:.2f}")

    def limpiar_pantalla(self):
        for widget in self.frame.winfo_children():
            widget.destroy()

    def cerrar_sesion(self):
        self.limpiar_pantalla()
        self.frame_inicio()

if __name__ == "__main__":
    root = tk.Tk()
    app = BancoApp(root)
    root.mainloop()
