import asyncio
import websockets
import tkinter as tk
from tkinter import messagebox, simpledialog

# Variável global para armazenar a conexão
websocket_connection = None

# Função para conectar ao servidor
async def connect_to_server():
    global websocket_connection
    host = host_entry.get()
    port = port_entry.get()
    uri = f"ws://{host}:{port}"
    
    try:
        websocket_connection = await websockets.connect(uri)
        messagebox.showinfo("Conectado", "Ligado ao servidor com sucesso!")
        toggle_connection_buttons(connected=True)
    except Exception as e:
        print(f"Erro: {e}")
        messagebox.showerror("Erro", "Não foi possível conectar ao servidor.")

# Função para enviar mensagem
async def send_message(message_text):
    global websocket_connection
    try:
        if websocket_connection:
            await websocket_connection.send(message_text)
            response = await websocket_connection.recv()
            print(f"Recebido: {response}")
            messagebox.showinfo("Resposta", response)
        else:
            messagebox.showwarning("Aviso", "Não está conectado ao servidor.")
    except Exception as e:
        print(f"Erro: {e}")
        messagebox.showerror("Erro", "Erro ao enviar a mensagem.")

# Função para desligar do servidor
async def disconnect_from_server():
    global websocket_connection
    if websocket_connection:
        await websocket_connection.close()
        websocket_connection = None
        messagebox.showinfo("Desconectado", "Desligado do servidor com sucesso.")
        toggle_connection_buttons(connected=False)
    else:
        messagebox.showwarning("Aviso", "Não está conectado ao servidor.")

# Função para realizar o login
async def login():
    username = user_entry.get()
    password = pass_entry.get()
    if websocket_connection:
        login_message = f"LOGIN:{username}:{password}"
        await send_message(login_message)
    else:
        messagebox.showwarning("Aviso", "Não está conectado ao servidor.")

# Função para sair da aplicação
def exit_application():
    if websocket_connection:
        asyncio.get_event_loop().run_until_complete(disconnect_from_server())
    root.quit()

# Função para alternar entre os botões de conexão e desconexão
def toggle_connection_buttons(connected):
    if connected:
        connect_button.config(state=tk.DISABLED)
        disconnect_button.config(state=tk.NORMAL)
        send_button.config(state=tk.NORMAL)
    else:
        connect_button.config(state=tk.NORMAL)
        disconnect_button.config(state=tk.DISABLED)
        send_button.config(state=tk.DISABLED)

# Interface gráfica
def create_client_window():
    global host_entry, port_entry, message_entry, connect_button, disconnect_button, send_button, user_entry, pass_entry, root

    root = tk.Tk()
    root.title("Cliente WebSocket")

    tk.Label(root, text="Host:").grid(row=0, column=0)
    host_entry = tk.Entry(root)
    host_entry.grid(row=0, column=1)

    tk.Label(root, text="Porta:").grid(row=1, column=0)
    port_entry = tk.Entry(root)
    port_entry.grid(row=1, column=1)

    tk.Label(root, text="Utilizador:").grid(row=2, column=0)
    user_entry = tk.Entry(root)
    user_entry.grid(row=2, column=1)

    tk.Label(root, text="Palavra-passe:").grid(row=3, column=0)
    pass_entry = tk.Entry(root, show="*")
    pass_entry.grid(row=3, column=1)

    connect_button = tk.Button(root, text="Ligar ao Servidor", command=lambda: asyncio.get_event_loop().run_until_complete(connect_to_server()))
    connect_button.grid(row=4, column=0)

    disconnect_button = tk.Button(root, text="Desligar do Servidor", state=tk.DISABLED, command=lambda: asyncio.get_event_loop().run_until_complete(disconnect_from_server()))
    disconnect_button.grid(row=4, column=1)

    send_button = tk.Button(root, text="Login", state=tk.DISABLED, command=lambda: asyncio.get_event_loop().run_until_complete(login()))
    send_button.grid(row=5, column=0, columnspan=2)

    exit_button = tk.Button(root, text="Sair", command=exit_application)
    exit_button.grid(row=6, column=0, columnspan=2)

    root.mainloop()

# Iniciar a janela do cliente
create_client_window()
