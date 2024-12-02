import customtkinter as ctk
from PIL import Image
# Configuración básica
ctk.set_appearance_mode("Dark")  # Modo oscuro
ctk.set_default_color_theme("blue")  # Tema azul

class App():
    def __init__(self, app):
        self.app = app
        self.app.title("CustomTkinter Menu")
        self.app.geometry("800x600")
        
        icon_home = Image.open("images/hogar2.png")  # Asegúrate de tener esta imagen en el directorio adecuado
        icon_home = self.icon_home.resize((30, 30), Image.Resampling.LANCZOS)
        icon_home = ctk.CTkImage(light_image=self.icon_home, size=(30, 30))

        # Frame principal
        self.main_frame = ctk.CTkFrame(self, corner_radius=0)
        self.main_frame.pack(fill="both", expand=True)

        # Frame del menú
        self.menu_frame = ctk.CTkFrame(self.main_frame, width=200, corner_radius=0)
        self.menu_frame.grid(row=0, column=0, sticky="ns")

        # Botón para ocultar/mostrar el menú
        self.toggle_menu_button = ctk.CTkButton(
            self, text="☰", width=30, command=self.toggle_menu
        )
        self.toggle_menu_button.place(x=10, y=10)

        # Botones del menú
        self.home_button = ctk.CTkButton(self.menu_frame, text="Home", command=self.show_home, image=self.icon_home)
        self.frame2_button = ctk.CTkButton(self.menu_frame, text="Ventas", command=self.show_frame2)
        self.frame3_button = ctk.CTkButton(self.menu_frame, text="Agregar Producto", command=self.show_frame3)

        #self.home_button.pack(pady=1)
        #self.frame2_button.pack(pady=1)
        #self.frame3_button.pack(pady=1)
        self.home_button.place(relx=0.1, rely=0.1)
        self.frame2_button.place(relx=0.1, rely=0.18)
        # Frame del contenido
        self.content_frame = ctk.CTkFrame(self.main_frame, corner_radius=10)
        self.content_frame.grid(row=0, column=1, sticky="nsew")

        # Configuración de layout
        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(1, weight=1)

        # Inicializar con la pantalla principal
        self.active_frame = None
        self.show_home()

        self.menu_visible = True  # Estado inicial del menú

    def toggle_menu(self):
        """Oculta o muestra el menú."""
        if self.menu_visible:
            self.menu_frame.grid_remove()  # Oculta el menú
        else:
            self.menu_frame.grid()  # Muestra el menú nuevamente
        self.menu_visible = not self.menu_visible

    def show_frame(self, frame_class):
        """Cambia el contenido del frame a la clase especificada."""
        if self.active_frame:
            self.active_frame.destroy()
        self.active_frame = frame_class(self.content_frame)
        self.active_frame.pack(fill="both", expand=True)

    def show_home(self):
        """Muestra la pantalla Home."""
        self.show_frame(HomeFrame)

    def show_frame2(self):
        """Muestra Frame 2."""
        self.show_frame(Frame2)

    def show_frame3(self):
        """Muestra Frame 3."""
        self.show_frame(Frame3)


class HomeFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        label = ctk.CTkLabel(self, text="Home Screen", font=("Arial", 24))
        label.pack(pady=20)
        btn = ctk.CTkButton(self, text="hola", command=self.insertar)
        btn.place(relx=0.1, rely=0.1)
        
        labeln = ctk.CTkLabel(self, text="nombre: ", font=("Arial", 24))
        labeln.pack(pady=40)
        self.textt = ctk.CTkEntry(self)
        self.textt.place(relx=0.1, rely=0.4)
        
    def insertar(self):
        testo = self.textt.get().strip()
        lab = ctk.CTkLabel(self, text=f'hola {testo}')
        lab.place(relx=0.1, rely=0.5)
class Frame2(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        label = ctk.CTkLabel(self, text="Frame 2 Content", font=("Arial", 24))
        label.pack(pady=20)


class Frame3(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        label = ctk.CTkLabel(self, text="Frame 3 Content", font=("Arial", 24))
        label.pack(pady=20)

'''
if __name__ == "__main__":
    app = App()
    app.mainloop()
    '''
