import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

class BookTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Book Tracker")
        self.root.geometry("800x600")

        # Загрузка данных
        self.books = self.load_books()

        self.setup_ui()
        self.update_table()

    def setup_ui(self):
        # Фрейм добавления книги
        add_frame = ttk.LabelFrame(self.root, text="Добавить книгу", padding=10)
        add_frame.pack(fill=tk.X, padx=10, pady=5)

        # Название
        ttk.Label(add_frame, text="Название:").grid(row=0, column=0, sticky="w", pady=2)
        self.title_entry = ttk.Entry(add_frame, width=30)
        self.title_entry.grid(row=0, column=1, padx=5, pady=2, sticky="ew")

        # Автор
        ttk.Label(add_frame, text="Автор:").grid(row=1, column=0, sticky="w", pady=2)
        self.author_entry = ttk.Entry(add_frame, width=30)
        self.author_entry.grid(row=1, column=1, padx=5, pady=2, sticky="ew")

        # Жанр
        ttk.Label(add_frame, text="Жанр:").grid(row=2, column=0, sticky="w", pady=2)
        genres = ["Роман", "Фантастика", "Детектив", "Биографии", "Поэзия", "Научная литература", "Фэнтези", "Классика"]
        self.genre_var = tk.StringVar()
        self.genre_combobox = ttk.Combobox(add_frame, textvariable=self.genre_var, values=genres, state="readonly")
        self.genre_combobox.grid(row=2, column=1, padx=5, pady=2, sticky="ew")

        # Количество страниц
        ttk.Label(add_frame, text="Количество страниц:").grid(row=3, column=0, sticky="w", pady=2)
        self.pages_entry = ttk.Entry(add_frame, width=30)
        self.pages_entry.grid(row=3, column=1, padx=5, pady=2, sticky="ew")

        # Кнопка добавления
        add_btn = ttk.Button(add_frame, text="Добавить книгу", command=self.add_book)
        add_btn.grid(row=4, column=0, columnspan=2, pady=10)

        add_frame.columnconfigure(1, weight=1)

        # Фрейм фильтрации
        filter_frame = ttk.LabelFrame(self.root, text="Фильтрация", padding=10)
        filter_frame.pack(fill=tk.X, padx=10, pady=5)

        # Фильтр по жанру
        ttk.Label(filter_frame, text="Жанр:").grid(row=0, column=0, sticky="w")
        filter_genres = ["Все"] + genres
        self.filter_genre_var = tk.StringVar(value="Все")
        self.filter_genre_combobox = ttk.Combobox(filter_frame, textvariable=self.filter_genre_var,
                                                   values=filter_genres, state="readonly")
        self.filter_genre_combobox.grid(row=0, column=1, padx=5)

        # Фильтр по страницам
        ttk.Label(filter_frame, text="Страниц:").grid(row=0, column=2, sticky="w", padx=(20, 0))
        page_filters = ["Все", ">100", ">200", ">300", ">500"]
        self.filter_pages_var = tk.StringVar(value="Все")
        self.filter_pages_combobox = ttk.Combobox(filter_frame, textvariable=self.filter_pages_var,
                                     values=page_filters, state="readonly")
        self.filter_pages_combobox.grid(row=0, column=3, padx=5)

        # Кнопки фильтров
        filter_btn = ttk.Button(filter_frame, text="Применить фильтр", command=self.apply_filter)
        filter_btn.grid(row=0, column=4, padx=(10, 0))

        clear_filter_btn = ttk.Button(filter_frame, text="Сбросить фильтр", command=self.clear_filter)
        clear_filter_btn.grid(row=0, column=5, padx=5)

        filter_frame.columnconfigure(1, weight=1)

        # Таблица книг
        table_frame = ttk.Frame(self.root)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        columns = ("title", "author", "genre", "pages")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=15)
        self.tree.heading("title", text="Название")
        self.tree.heading("author", text="Автор")
        self.tree.heading("genre", text="Жанр")
        self.tree.heading("pages", text="Страниц")
        self.tree.column("title", width=200)
        self.tree.column("author", width=150)
        self.tree.column("genre", width=120)
        self.tree.column("pages", width=80)

        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)


    def validate_input(self, title, author, pages_str):
        """Проверка корректности ввода."""
        if not title or not author or not self.genre_var.get():
            messagebox.showerror("Ошибка", "Все поля должны быть заполнены!")
            return False

        try:
            pages = int(pages_str)
            if pages <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Ошибка", "Количество страниц должно быть положительным числом!")
            return False

        return True

    def add_book(self):
        """Добавление новой книги."""
        title = self.title_entry.get().strip()
        author = self.author_entry.get().strip()
        genre = self.genre_var.get()
        pages_str = self.pages_entry.get().strip()

        if not self.validate_input(title, author, pages_str):
            return

        book = {
            "title": title,
            "author": author,
            "genre": genre,
            "pages": int(pages_str)
        }

        self.books.append(book)
        self.save_books()
        self.update_table()
        self.clear_form()
        messagebox.showinfo("Успех", "Книга добавлена в коллекцию!")

    def clear_form(self):
        """Очистка формы ввода."""
        self.title_entry.delete(0, tk.END)
        self.author_entry.delete(0, tk.END)
        self.genre_var.set("")
        self.pages_entry.delete(0, tk.END)

    def load_books(self):
        """Загрузка книг из JSON-файла."""
        if os.path.exists("books_data.json"):
            try:
                with open("books_data.json", "r", encoding="utf-8") as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                messagebox.showwarning("Предупреждение", "Не удалось загрузить данные. Создан новый список.")
        return []

    def save_books(self):
        """Сохранение книг в JSON‑файл."""
        try:
            with open("books_data.json", "w", encoding="utf-8") as f:
                json.dump(self.books, f, ensure_ascii=False, indent=2)
        except IOError:
            messagebox.showerror("Ошибка", "Не удалось сохранить данные!")

    def update_table(self, filtered_books=None):
        """Обновление таблицы книг (с фильтрацией или без)."""
        # Очищаем таблицу
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Определяем, какие книги показывать
        books_to_show = filtered_books if filtered_books is not None else self.books

        # Заполняем таблицу
        for book in books_to_show:
            self.tree.insert("", tk.END, values=(
                book["title"],
                book["author"],
                book["genre"],
                book["pages"]
            ))

    def apply_filter(self):
        """Применение фильтров к списку книг."""
        selected_genre = self.filter_genre_var.get()
        selected_pages = self.filter_pages_var.get()

        filtered_books = []

        for book in self.books:
            # Проверка жанра
            genre_match = (selected_genre == "Все" or book["genre"] == selected_genre)

            # Проверка количества страниц
            pages_match = True
            if selected_pages != "Все":
                min_pages = int(selected_pages[1:])  # Убираем символ ">" и преобразуем в число
                if book["pages"] < min_pages:
                    pages_match = False

            if genre_match and pages_match:
                filtered_books.append(book)


        self.update_table(filtered_books)

    def clear_filter(self):
        """Сброс фильтров и отображение всех книг."""
        self.filter_genre_var.set("Все")
        self.filter_pages_var.set("Все")
        self.update_table()


# Запуск приложения
if __name__ == "__main__":
    root = tk.Tk()
    app = BookTracker(root)
    root.mainloop()
