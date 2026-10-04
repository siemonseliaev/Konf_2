import argparse
import os
import shlex
import tkinter as tk


class Emulator(tk.Tk):

    def __init__(self, vfs_path: str, script_path: str = None):
        super().__init__()

        self.vfs_path = vfs_path
        self.script_path = script_path

        self.vfs_name = (
            os.path.basename(vfs_path) if vfs_path else "default_vfs.tar"
        )
        self.prompt = f"[{self.vfs_name}]$ "

        self.title(f"Эмулятор VFS — {self.vfs_name}")

        self.output = tk.Text(self, height=20, width=80, bg="black", fg="white")
        self.output.pack(fill=tk.BOTH, expand=True)

        # Строка ввода
        self.entry = tk.Entry(
            self, bg="white", fg="black", insertbackground="black"
        )
        self.entry.pack(fill=tk.X)
        self.entry.bind("<Return>", self.on_enter)
        self.print_debug_info()
        if self.script_path:
            self.run_startup_script(self.script_path)

        self.show_prompt()

    def print_debug_info(self):
        self.output.insert(tk.END, f"Путь к VFS: {self.vfs_path}\n")
        self.output.insert(
            tk.END, f"Путь к стартовому скрипту: {self.script_path}\n"
        )
        self.output.insert(tk.END, "\n")

    def show_prompt(self):
        self.output.insert(tk.END, self.prompt)
        self.output.see(tk.END)

    def execute_command(self, user_input: str):

        self.output.insert(tk.END, user_input + "\n")
        try:
            args = shlex.split(user_input)
        except Exception as e:

            self.output.insert(
                tk.END, f"Ошибка синтаксиса: {e}\n"
            )
            return

        if not args:
            return

        command = args[0]
        command_args = args[1:]

        self.parser(command, command_args)

    def run_startup_script(self, script_path: str):
        self.output.insert(
            tk.END, f"--- Запуск стартового скрипта: {script_path} ---\n"
        )
        if not os.path.exists(script_path):
            self.output.insert(
                tk.END,
                f"Ошибка: скрипт '{script_path}' не найден\n\n",
            )
            return

        try:
            with open(script_path, "r", encoding="utf-8") as f:
                lines = f.readlines()

            for line in lines:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue

                self.output.insert(tk.END, self.prompt)
                self.execute_command(line)

            self.output.insert(
                tk.END, "Завершение стартового скрипта\n\n"
            )

        except Exception as e:
            self.output.insert(
                tk.END, f"Ошибка при чтении скрипта: {e}\n\n"
            )

    def on_enter(self, event=None):
        user_input = self.entry.get()
        self.entry.delete(0, tk.END)

        self.execute_command(user_input)
        self.show_prompt()

    def parser(self, command, args):
        if command == "help":
            self.output.insert(
                tk.END,
                "Доступные команды:\n"
                "ls - вывести список файлов (заглушка)\n"
                "cd   - сменить директорию (заглушка)\n"
                "help        - показать справку\n"
                "exit        - завершить работу\n",
            )

        elif command == "cd":
            if len(args) != 1:
                self.output.insert(
                    tk.END, "Ошибка: cd требует ровно 1 аргумент\n"
                )
            else:
                self.output.insert(tk.END, f"cd: {args}\n")

        elif command == "ls":
            self.output.insert(tk.END, f"ls: {args}\n")

        elif command == "exit":
            if len(args) > 0:
                self.output.insert(
                    tk.END, "Ошибка: команда exit не принимает аргументов\n"
                )
                return
            self.destroy()

        else:
            self.output.insert(
                tk.END, f"Ошибка: неизвестная команда '{command}'\n"
            )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Эмулятор VFS")
    parser.add_argument(
        "--vfs",
        type=str,
        default="my_vfs.tar",
        help="Путь к физическому расположению VFS",
    )
    parser.add_argument(
        "--script",
        type=str,
        default=None,
        help="Путь к стартовому скрипту с командами",
    )

    parsed_args = parser.parse_args()

    app = Emulator(vfs_path=parsed_args.vfs, script_path=parsed_args.script)
    app.mainloop()