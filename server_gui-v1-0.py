import asyncio
import websockets
import tkinter as tk
from tkinter import simpledialog, messagebox
from threading import Thread

# Log de utilizadores
user_log = {}

# Função para salvar o log de utilizadores num arquivo
def save_user_log():
    with open("user_log.txt", "w") as f:
        for username, password in user_log.items():
            f.write(f"{username}:{password}\n")

# Função para carregar o log de utilizadores do arquivo
def load_user_log():
    global user_log
    try:
        with open("user_log.txt", "r") as f:
            for line in f:
                username, password = line.strip().split(":")
                user_log[username] = password
    except FileNotFoundError:
        pass

# Função para adicionar utilizadores
def add_user():
    username = simpledialog.askstring("Adicionar Utilizador", "Nome de Utilizador:")
    if username in user_log:
        messagebox.showerror("Erro", "Utilizador já existe!")
        return
    password = simpledialog.askstring("Adicionar Utilizador", "Palavra-passe:")
    user_log[username] = password
    save_user_log()
    messagebox.showinfo("Sucesso", "Utilizador adicionado!")

# Função do servidor WebSocket
async def websocket_handler(websocket, path):
    try:
        async for message in websocket:
            print(f"Recebido: {message}")
            await websocket.send(f"Echo: {message}")
    except websockets.exceptions.ConnectionClosedOK:
        print("Conexão fechada")

# Função para iniciar o servidor numa thread separada
def start_server_thread(host, port):
    async def start_server():
        server = await websockets.serve(websocket_handler, host, port)
        await server.wait_closed()

    asyncio.run(start_server())

# Função para ligar o servidor ao clicar no botão
def start_server():
    host = host_entry.get()
    port = int(port_entry.get())
    server_thread = Thread(target=start_server_thread, args=(host, port), daemon=True)
    server_thread.start()
    messagebox.showinfo("Servidor", "Servidor ligado.")

# Função para parar o servidor
def stop_server():
    # Ainda que a interrupção do servidor em execução seja complexa, a interface é simplificada.
    # Isto deve ser tratado no código real com um shutdown apropriado.
    messagebox.showinfo("Servidor", "Função de desligar o servidor não implementada neste exemplo.")

# Interface gráfica
def create_server_window():
    global host_entry, port_entry

    root = tk.Tk()
    root.title("Servidor WebSocket")

    tk.Label(root, text="Host:").grid(row=0, column=0)
    host_entry = tk.Entry(root)
    host_entry.grid(row=0, column=1)

    tk.Label(root, text="Porta:").grid(row=1, column=0)
    port_entry = tk.Entry(root)
    port_entry.grid(row=1, column=1)

    start_button = tk.Button(root, text="Ligar Servidor", command=start_server)
    start_button.grid(row=2, column=0)

    stop_button = tk.Button(root, text="Desligar Servidor", command=stop_server)
    stop_button.grid(row=2, column=1)

    add_user_button = tk.Button(root, text="Adicionar Utilizador", command=add_user)
    add_user_button.grid(row=3, column=0, columnspan=2)

    root.mainloop()

# Carregar utilizadores ao iniciar
load_user_log()

# Iniciar a janela do servidor
create_server_window()
