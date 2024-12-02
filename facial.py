import cv2
import os
import face_recognition
import mediapipe as mp
from tkinter import Tk, Label, Button, messagebox
from PIL import Image, ImageTk

# Inicializar los módulos de MediaPipe
mp_face_mesh = mp.solutions.face_mesh
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

# Función para cargar y actualizar las imágenes conocidas
def load_known_faces():
    known_face_encodings = []
    known_face_names = []
    images_directory = "fotos"
    
    for filename in os.listdir(images_directory):
        if filename.endswith(".jpg") or filename.endswith(".png"):
            try:
                image_path = os.path.join(images_directory, filename)
                name = os.path.splitext(filename)[0]
                image = cv2.imread(image_path)
                image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                face_locations = face_recognition.face_locations(image_rgb)
                if face_locations:
                    face_encodings = face_recognition.face_encodings(image_rgb, known_face_locations=face_locations)[0]
                    known_face_encodings.append(face_encodings)
                    known_face_names.append(name)
            except Exception as e:
                print(f"Error al procesar la imagen {filename}: {e}")
    
    return known_face_encodings, known_face_names

# Cargar imágenes iniciales
known_face_encodings, known_face_names = load_known_faces()

class FaceRecognitionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Reconocimiento Facial")
        
        self.video_label = Label(root)
        self.video_label.pack()

        self.recognize_button = Button(root, text="Capturar y Reconocer", command=self.capture_image_and_recognize)
        self.recognize_button.pack()

        self.close_button = Button(root, text="Cerrar", command=self.cerrar)
        self.close_button.pack()

        self.cap = cv2.VideoCapture(0)
        self.stream_video()

    def cerrar(self):
        self.cap.release()  # Liberar la cámara antes de cerrar
        self.root.destroy() 

    def stream_video(self):
        ret, frame = self.cap.read()
        if ret:
            frame = cv2.flip(frame, 1)
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Procesar el frame para la malla facial
            with mp_face_mesh.FaceMesh(
                static_image_mode=False,
                max_num_faces=1,
                min_detection_confidence=0.5,
                min_tracking_confidence=0.5) as face_mesh:
                
                results = face_mesh.process(frame_rgb)
                if results.multi_face_landmarks:
                    for face_landmarks in results.multi_face_landmarks:
                        mp_drawing.draw_landmarks(
                            image=frame,
                            landmark_list=face_landmarks,
                            connections=mp_face_mesh.FACEMESH_TESSELATION,
                            landmark_drawing_spec=None,
                            connection_drawing_spec=mp_drawing_styles.get_default_face_mesh_tesselation_style())
                        mp_drawing.draw_landmarks(
                            image=frame,
                            landmark_list=face_landmarks,
                            connections=mp_face_mesh.FACEMESH_CONTOURS,
                            landmark_drawing_spec=None,
                            connection_drawing_spec=mp_drawing_styles.get_default_face_mesh_contours_style())
            
            # Convertir el frame a un formato compatible con Tkinter
            img = Image.fromarray(frame_rgb)
            imgtk = ImageTk.PhotoImage(image=img)
            self.video_label.imgtk = imgtk
            self.video_label.configure(image=imgtk)

        self.root.after(10, self.stream_video)

    def capture_image_and_recognize(self):
        # Recargar las imágenes cada vez que se capture una imagen para reconocimiento
        global known_face_encodings, known_face_names
        known_face_encodings, known_face_names = load_known_faces()

        ret, frame = self.cap.read()
        if not ret:
            messagebox.showerror("Error", "No se pudo capturar la imagen")
            return

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(frame_rgb)
        face_encodings = face_recognition.face_encodings(frame_rgb, known_face_locations=face_locations)

        recognized_name = "Desconocido"
        for face_encoding in face_encodings:
            results = face_recognition.compare_faces(known_face_encodings, face_encoding)
            if True in results:
                match_index = results.index(True)
                recognized_name = known_face_names[match_index]
                break

        if recognized_name != "Desconocido":
            messagebox.showinfo("Reconocido", f"Usuario reconocido: {recognized_name}")
            self.cap.release()  # Liberar la cámara antes de cerrar
            self.root.destroy() 
        else:
            messagebox.showwarning("No Reconocido", "Usuario no encontrado o desconocido")

if __name__ == "__main__":
    root = Tk()
    app = FaceRecognitionApp(root)
    root.mainloop()
