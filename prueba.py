from tkinter import *
from PIL import Image, ImageTk
from json import load, dump, JSONDecodeError
from random import choice
from tkinter import messagebox

# Clase para manejar usuarios
class UserManager:
    def __init__(self, file_name="users.txt"):
        self.file_name = file_name
        self.users = self.load_users()

    def load_users(self):
        try:
            with open(self.file_name, "r") as file:
                return load(file)
        except (FileNotFoundError, JSONDecodeError):
            return []

    def save_users(self):
        with open(self.file_name, "w") as file:
            dump(self.users, file, indent=4)

    def register_user(self, name, password):
        if any(user["name"] == name for user in self.users):
            return False
        new_user = {"name": name, "password": password, "active": 0, "score": 0}
        self.users.append(new_user)
        self.save_users()
        return True

    def login_user(self, name, password):
        for user in self.users:
            if user["name"] == name and user["password"] == password:
                user["active"] = 1
                self.save_users()
                return user
        return None

    def update_user(self, user):
        for idx, u in enumerate(self.users):
            if u["name"] == user["name"]:
                self.users[idx] = user
                self.save_users()
                break

# Clase para manejar las preguntas
class QuestionManager:
    def __init__(self, file_name="questions.txt"):
        self.file_name = file_name
        self.questions = self.load_questions()

    def load_questions(self):
        try:
            with open(self.file_name, "r", encoding="utf-8") as file:
                data = load(file)
                all_questions = []

                for category, questions in data.items():
                    for question in questions:
                        question["categoria"] = category
                        all_questions.append(question)

                choice(all_questions)
                return all_questions[:10]

        except (FileNotFoundError, JSONDecodeError):
            return []

# Clase principal del juego
class TriviaApp(Tk):
    def __init__(self):
        super().__init__()
        self.title("Trivia App")
        self.state("zoomed")  # Maximiza la ventana automáticamente

        self.user_manager = UserManager()
        self.question_manager = QuestionManager()

        self.current_user = None
        self.current_question_index = 0
        self.puntuacion = 0

        self.original_image = Image.open("1.png")
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        self.bg_image = ImageTk.PhotoImage(self.original_image.resize((screen_width, screen_height)))
        self.bg_label = Label(self, image=self.bg_image)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        Button(self, text="Comenzar", font=("Arial", 20), command=self.start).place(relx=0.5, rely=0.636, anchor="center")
    
    def clear_window(self):
        #Limpia todos los widgets de la ventana.
        for widget in self.winfo_children():
            widget.destroy()

    def start(self):
        self.clear_window()  # Limpiar la ventana
        self.main_menu()

    def main_menu(self):
        self.load_background("3.png")

        Label(self, text="Bienvenido a Trivia Game", font=("Arial", 24), bg="darkorange").pack(pady=130)

        Button(self, text="Registrar Usuario", font=("Arial", 19), command=self.register_user).place(relx=0.5, rely=0.717, anchor="center")
        Button(self, text="Iniciar Sesión", font=("Arial", 19), command=self.open_session).place(relx=0.5, rely=0.81, anchor="center")

    def register_user(self):
        #Ventana para registrar
        self.clear_window()
        self.load_background("2.png")

        Label(self, text="Nombre:", font=("Arial", 19), bg="gray1", fg="white").place(relx=0.5, rely=0.56, anchor="center")
        entry_name = Entry(self, font=("Arial", 12), bg="gray1", fg="white")
        entry_name.place(relx=0.5, rely=0.62, anchor="center")

        Label(self, text="Contraseña:", font=("Arial", 19), bg="gray1", fg="white").place(relx=0.5, rely=0.7, anchor="center")
        entry_password = Entry(self, show="*", font=("Arial", 12), bg="gray1", fg="white")
        entry_password.place(relx=0.5, rely=0.76, anchor="center")

        def save_user():
            name = entry_name.get()
            password = entry_password.get()
            if self.user_manager.register_user(name, password):
                messagebox.showinfo("Éxito", "Usuario registrado exitosamente.")
                self.main_menu()  # Regresa al menú principal
            else:
                messagebox.showerror("Error", "Usuario ya registrado.")
                self.main_menu()

        Button(self, text="Registrar", font=("Arial", 19) , bg="SlateBlue1", fg="white", command=save_user).place(relx=0.5, rely=0.86, anchor="center")

    def open_session(self):
        #Ventana para iniciar sesión
        self.clear_window()
        self.load_background("2.png")

        Label(self, text="Nombre:", font=("Arial", 19), bg="gray1", fg="white").place(relx=0.5, rely=0.56, anchor="center")
        entry_name = Entry(self, font=("Arial", 12), bg="gray1", fg="white")
        entry_name.place(relx=0.5, rely=0.62, anchor="center")

        Label(self, text="Contraseña:", font=("Arial", 19), bg="gray1", fg="white").place(relx=0.5, rely=0.7, anchor="center")
        entry_password = Entry(self, show="*", font=("Arial", 12), bg="gray1", fg="white")
        entry_password.place(relx=0.5, rely=0.76, anchor="center")

        def login_user():
            name = entry_name.get()
            password = entry_password.get()
            user = self.user_manager.login_user(name, password)

            if user:
                self.current_user = user
                messagebox.showinfo("Éxito", f"Sesión iniciada como {name}.")
                self.user_menu()
              
            else:
                messagebox.showerror("Error", "Credenciales incorrectas.")

        Button(self, text="Iniciar Sesión", font=("Arial", 19) , bg ="SlateBlue1", fg="white", command=login_user).place(relx=0.5, rely=0.86, anchor="center")

    def load_background(self, image_path):
        self.original_image = Image.open(image_path)
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        self.bg_image = ImageTk.PhotoImage(self.original_image.resize((screen_width, screen_height)))
        self.bg_label = Label(self, image=self.bg_image)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    def user_menu(self):
        self.clear_window()
        self.load_background("4.png")

        Label(self, text=f"Bienvenido, {self.current_user['name']}", font=("Arial", 24), bg="pale violet red").place(relx=0.5, rely=0.27, anchor="center")

        users_frame = Frame(self, bg="lightgreen", width=300, height=400)
        users_frame.place(relx=0.18, rely=0.24, anchor="nw")

        Label(users_frame, text="Usuarios Conectados:", font=("Arial", 14), bg="lightgreen", fg="black").pack(pady=10)

    # Mostrar los usuarios conectados y sus puntajes
        for user in self.user_manager.users:
            if user["active"]:
                user_info = f"Nombre: {user['name']} | Puntaje: {user['score']}"
                Label(users_frame, text=user_info, font=("Arial", 12), bg="lightgreen", fg="black").pack(pady=5)

        Button(self, text="Ver Puntaje", command=self.view_score, font=("Arial", 14), width=20).place(relx=0.5, rely=0.4, anchor="center")
        Button(self, text="Iniciar Preguntas", command=self.start_quiz, font=("Arial", 14), width=20).place(relx=0.5, rely=0.54, anchor="center")
        Button(self, text="Cerrar Sesión", command=self.logout, font=("Arial", 14), width=20).place(relx=0.5, rely=0.68, anchor="center")

    def view_score(self):
        if self.current_user:
            messagebox.showinfo("Puntaje", f"Tu puntaje es: {self.current_user['score']}")

    def start_quiz(self):
        self.puntuacion_ronda = 0  
        self.current_question_index = 0

        if not self.question_manager.questions:
            messagebox.showerror("Error", "No hay preguntas disponibles.")
            return

        self.show_question()

    def show_question(self):
        #Mostrar preguntas
        if self.current_question_index >= len(self.question_manager.questions):
            self.show_results()
            return

        self.clear_window()
        self.load_background("6.png") 

        pregunta = self.question_manager.questions[self.current_question_index]
        Label(self, text=f"Categoría: {pregunta['categoria']}", font=("Arial", 18), bg="coral").pack(pady=20)
        Label(self, text=pregunta["pregunta"], font=("Arial", 16), fg="white", wraplength=700, justify="center", bg="gray1").pack(pady=20)

        self.score_label = Label(self, text=f"Puntaje actual: {self.puntuacion_ronda}", font=("Arial", 16), bg="gray1", fg="white")
        self.score_label.pack(pady=40)

        opciones_frame = Frame(self, bg="gray1")
        opciones_frame.pack(pady=10)

        for opcion, texto in pregunta["opciones"].items():
            Button(opciones_frame, text=f"{opcion}: {texto}", width=35, command=lambda opcion=opcion: self.check_answer(opcion)).pack(pady=20)

        Button(self, text="Salir", font=("Arial", 14), bg="coral", fg="white", command=self.user_menu).pack(pady=20)
    def check_answer(self, respuesta_usuario):
        pregunta = self.question_manager.questions[self.current_question_index]
    
        if respuesta_usuario == pregunta["respuesta correcta"]:
            self.puntuacion_ronda += 2
        else:
            self.puntuacion_ronda -= 1

        self.current_question_index += 1
        self.show_question()

    def show_results(self):
        self.clear_window()
        self.load_background("7.png")

        # Actualizar el puntaje acumulado
        if self.current_user:
            self.current_user["score"] += self.puntuacion_ronda
            self.user_manager.update_user(self.current_user)

        Label(self, text=f"{self.puntuacion_ronda}", font=("Arial", 20), bg="coral", fg="white").place(relx=0.5, rely=0.5, anchor="center")
        Button(self, text="Volver al Menú", command=self.user_menu, width=20, font=("Arial", 20), bg="gray1", fg="white").place(relx=0.5, rely=0.6, anchor="center")

    def logout(self):
        self.current_user = None
        self.main_menu()

app = TriviaApp()
app.mainloop()