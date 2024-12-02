import customtkinter as ctk
from tkinter import messagebox
import cv2
from PIL import Image
from fun_sql.funciones import registrar_usuario

class RegisterApp:
    def __init__(self, register):
        self.register = register
        self.register.geometry("800x700")
        self.register.title("Registrar Usuario")
        
        back_icon = Image.open("images/back.png")  # Asegúrate de tener esta imagen en el directorio adecuado
        back_icon = back_icon.resize((30, 30), Image.Resampling.LANCZOS)
        back_icon = ctk.CTkImage(light_image=back_icon, size=(30, 30))
        
        # Botón para registrar
        back = ctk.CTkButton(master=self.register, text="Regresar",image=back_icon , fg_color="red", text_color="white" ,command=self.back_to_main)
        back.place(relx=0.1, rely=0.1)
        
        # Crear el marco principal
        self.card = ctk.CTkFrame(master=self.register, corner_radius=15, width=350, height=500)
        self.card.place(relx=0.5, rely=0.5, anchor="center")

        # Etiqueta de título
        title_label = ctk.CTkLabel(master=self.card, text="Registro de Usuario", font=("Arial", 16, "bold"))
        title_label.pack(pady=10)

        # Campo de nombre
        self.nombre = ctk.CTkEntry(master=self.card, placeholder_text="Nombre", width=250)
        self.nombre.pack(pady=10, padx=20)

        # Campo de apellido paterno
        self.apellido_p = ctk.CTkEntry(master=self.card, placeholder_text="Apellido Paterno", width=250)
        self.apellido_p.pack(pady=10, padx=20)

        # Campo de apellido materno
        self.apellido_m = ctk.CTkEntry(master=self.card, placeholder_text="Apellido Materno", width=250)
        self.apellido_m.pack(pady=10, padx=20)
        
        # Campo de apellido correo
        self.correo = ctk.CTkEntry(master=self.card, placeholder_text="Correo", width=250)
        self.correo.pack(pady=10, padx=20)

        # Campo de usuario
        self.username_entry = ctk.CTkEntry(master=self.card, placeholder_text="Usuario", width=250)
        self.username_entry.pack(pady=10, padx=20)

        # Campo de contraseña
        self.password_entry = ctk.CTkEntry(master=self.card, placeholder_text="Contraseña", show="*", width=250)
        self.password_entry.pack(pady=10, padx=20)

        # Botón para capturar foto
        photo_button = ctk.CTkButton(master=self.card, text="Capturar Foto", command=self.capture_photo)
        photo_button.pack(pady=10)

        # Botón para registrar
        register_button = ctk.CTkButton(master=self.card, text="Registrar", command=self.handle_register)
        register_button.pack(pady=10)

        # Contenedor para la imagen capturada
        self.photo_label = ctk.CTkLabel(master=self.card, text="No hay foto capturada", width=250, height=150)
        self.photo_label.pack(pady=10)

        self.photo_path = None  # Para almacenar la ruta de la foto capturada
        
    def back_to_main(self):
        # Limpia la pantalla actual
        for widget in self.register.winfo_children():
            widget.destroy()
        
        # Regresa a la pantalla principal
        from main import Main
        Main(self.register)

    def capture_photo(self):
        username = self.username_entry.get().strip()

        if not username:
            messagebox.showerror("Error", "Por favor, ingrese un nombre de usuario antes de capturar la foto.")
            return

        cap = cv2.VideoCapture(0)  # Inicia la cámara (0 para la cámara predeterminada)
        if not cap.isOpened():
            messagebox.showerror("Error", "No se pudo acceder a la cámara.")
            return

        # Mostrar la cámara en tiempo real
        while True:
            ret, frame = cap.read()
            if not ret:
                messagebox.showerror("Error", "Error al capturar la imagen.")
                break

            cv2.imshow("Presione 'Espacio' para capturar la foto, 'Esc' para cancelar", frame)
            key = cv2.waitKey(1)
            if key == 32:  # Espacio para capturar la foto
                # Usar el nombre del usuario para el archivo
                self.photo_path = f"fotos/{username}.png"
                cv2.imwrite(self.photo_path, frame)  # Guardar la foto
                messagebox.showinfo("Foto Capturada", f"Foto guardada como {self.photo_path}.")
                break
            elif key == 27:  # Esc para salir
                break

        cap.release()
        cv2.destroyAllWindows()

        if self.photo_path:
            # Mostrar la foto en la interfaz
            self.display_photo()

    def display_photo(self):
        # Cargar la imagen capturada
        img = Image.open(self.photo_path)
        img = img.resize((250, 150), Image.Resampling.LANCZOS)  # Redimensionar para ajustarse al contenedor
        ctk_img = ctk.CTkImage(light_image=img, size=(250, 150))  # Convertir a CTkImage
        self.photo_label.configure(image=ctk_img, text="")  # Elimina el texto
        self.photo_label.image = ctk_img  # Referencia para evitar el recolector de basura
        

    def handle_register(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        correo = self.correo.get().strip()
        nombre = self.nombre.get().strip()
        apellido_p = self.apellido_p.get().strip()
        apellido_m = self.apellido_m.get().strip()
        path_foto = self.photo_path
        #print(self.photo_path)
        if not nombre or not apellido_p or not apellido_m or not username or not password or not correo:
            messagebox.showerror("Error", "Por favor, complete todos los campos.")
        elif not self.photo_path:
            messagebox.showerror("Error", "Por favor, capture una foto antes de registrar.")
        else:
            registrar_usuario(nombre, apellido_p, apellido_m, correo, username, password, path_foto)
            #print(f"Usuario Registrado: {username}")
            #print(f"Foto Guardada en: {self.photo_path}")



