import asyncio
import websockets
import tkinter as tk
from tkinter import messagebox

# Função para conectar ao servidor
async def connect_to_server(uri, message_text):
    try:
        async with websockets.connect(uri) as websocket:
            await websocket.send(message_text)
            response = await websocket.recv()
            print(f"Recebido: {response}")
            messagebox.showinfo("Resposta", response)
    except Exception as e:
        print(f"Erro: {e}")
        messagebox.showerror("Erro", "Não foi possível conectar ao servidor.")

# Função de envio de mensagem
def send_message():
    host = host_entry.get()
    port = port_entry.get()
    message_text = message_entry.get()
    uri = f"ws://{host}:{port}"
    
    asyncio.get_event_loop().run_until_complete(connect_to_server(uri, message_text))

# Interface gráfica
def create_client_window():
    global host_entry, port_entry, message_entry

    root = tk.Tk()
    root.title("Cliente WebSocket")

    tk.Label(root, text="Host:").grid(row=0, column=0)
    host_entry = tk.Entry(root)
    host_entry.grid(row=0, column=1)

    tk.Label(root, text="Porta:").grid(row=1, column=0)
    port_entry = tk.Entry(root)
    port_entry.grid(row=1, column=1)

    tk.Label(root, text="Mensagem:").grid(row=2, column=0)
    message_entry = tk.Entry(root)
    message_entry.grid(row=2, column=1)

    send_button = tk.Button(root, text="Enviar Mensagem", command=send_message)
    send_button.grid(row=3, column=0, columnspan=2)

    root.mainloop()

# Iniciar a janela do cliente
create_client_window()
