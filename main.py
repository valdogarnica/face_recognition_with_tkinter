import customtkinter as ctk
from tkinter import messagebox 
from registro import RegisterApp
from inicio import App
from facial import FaceRecognitionApp
from fun_sql.funciones import *
from PIL import Image, ImageTk

class Main:
    def __init__(self, root):
        self.root = root
        #self.root.geometry("500x400")
        # Dimensiones de la ventana
        window_width = 1000
        window_height = 500

        # Obtener las dimensiones de la pantalla
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # Calcular las coordenadas para centrar la ventana
        x_cord = (screen_width // 2) - (window_width // 2)
        y_cord = (screen_height // 2) - (window_height // 2)

        # Configurar la geometría de la ventana centrada
        self.root.geometry(f"{window_width}x{window_height}+{x_cord}+{y_cord}")
        
        self.root.resizable(False, False)
        self.root.title("Login")
        ctk.set_appearance_mode("System")  # Modos: "Light", "Dark", "System"
        ctk.set_default_color_theme("blue")  # Temas: "blue", "green", "dark-blue"

        # BOTON BACK, REGRESA A LA PANTALLA PRINCIPAL
        self.card = ctk.CTkFrame(master=self.root, corner_radius=15, width=350, height=400)
        self.card.place(relx=0.5, rely=0.5, anchor="center")

        # Configurar los widgets
        self.create_widgets()

    def create_widgets(self):
       # Cargar las imágenes para los iconos
        login_icon = Image.open("images/acceso.png")  # Asegúrate de tener esta imagen en el directorio adecuado
        login_icon = login_icon.resize((30, 30), Image.Resampling.LANCZOS)
        login_icon = ctk.CTkImage(light_image=login_icon, size=(30, 30))

        face_icon = Image.open("images/face2.png")  # Asegúrate de tener esta imagen en el directorio adecuado
        face_icon = face_icon.resize((30, 30), Image.Resampling.LANCZOS)
        face_icon = ctk.CTkImage(light_image=face_icon, size=(30, 30))

        register_icon = Image.open("images/usuario-plus.png")  # Asegúrate de tener esta imagen en el directorio adecuado
        register_icon = register_icon.resize((30, 30), Image.Resampling.LANCZOS)
        register_icon = ctk.CTkImage(light_image=register_icon, size=(30, 30))
        
        # Etiqueta de título
        title_label = ctk.CTkLabel(master=self.card, text="Iniciar Sesión", font=("Arial", 18, "bold"))
        title_label.pack(pady=10)

        # Campo de usuario
        self.username_entry = ctk.CTkEntry(master=self.card, placeholder_text="Usuario", width=250)
        self.username_entry.pack(pady=10, padx=20)

        # Campo de contraseña
        self.password_entry = ctk.CTkEntry(master=self.card, placeholder_text="Contraseña", show="*", width=250)
        self.password_entry.pack(pady=10, padx=20)

        # Botón de inicio de sesión
        login_button = ctk.CTkButton(master=self.card, text="Iniciar Sesión", command=self.handle_login, image=login_icon, fg_color='green', text_color='white')
        login_button.pack(pady=10)
        
        # Botón de inicio de sesión facial
        face_buton = ctk.CTkButton(master=self.card, text="Facial", command=self.login_facial, image=face_icon, fg_color='blue', text_color='white')
        face_buton.pack(pady=10)
        
        # Botón de registrar usuario
        register = ctk.CTkButton(master=self.card, text="Registrar Usuario", image=register_icon, width=200 ,command=self.register)
        register.pack(pady=10)
        
    def login_facial(self):
        #FaceRecognitionApp(self.root)
        # Crear la ventana secundaria de FaceRecognitionApp
        self.face_app_window = ctk.CTkToplevel(self.root)  # Ventana secundaria para el reconocimiento facial
        self.face_app = FaceRecognitionApp(self.face_app_window)
    
    def register(self):
        # Abre una nueva ventana desde el archivo externo
        #register_window = ctk.CTk()  # Crear una nueva instancia de ventana
        #RegisterApp(register_window)  # Inicializa la clase del otro archivo
        #register_window.mainloop()
        #SOLOCION 1
        self.card.destroy()  # Elimina el contenido actual
        RegisterApp(self.root) 
        #SOLUCION 2
        #register_window = ctk.CTkToplevel(self.root)  # Crear una ventana secundaria
        #RegisterApp(register_window) 

    def handle_login(self):
        # Obtén los valores ingresados
        username = self.username_entry.get()
        password = self.password_entry.get()
        # Verifica si los campos están vacíos
        if not username or not password:
            messagebox.showerror("Error", "Por favor, complete todos los campos.")
        else:
            # Lógica de inicio de sesión (actualmente, solo imprime los valores)
            #print(f"Usuario: {username}, Contraseña: {password}")
            # Lógica de inicio de sesión (actualmente, solo imprime los valores)
            if (login(username, password)):
                messagebox.showinfo(title="EXITO!", message="INICIO DE SESION EXITOSO!")
                self.card.destroy()  # Elimina el contenido actual
                App(self.root)
            else:
                messagebox.showerror(title="ERROR!", message="UYY!!!, CREDENCIALES INCORRECTAS")
        


# Ejecutar la aplicación
if __name__ == "__main__":
    root = ctk.CTk()
    app = Main(root)
    root.mainloop()
