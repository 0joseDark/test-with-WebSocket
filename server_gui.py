import asyncio
import websockets
import threading
import tkinter as tk
from tkinter import scrolledtext, messagebox
import logging

# Configuração do log
logging.basicConfig(filename="server_log.log", level=logging.INFO, format="%(asctime)s - %(message)s")

connected_clients = set()
server = None

class WebSocketServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.server = None

    async def handler(self, websocket, path):
        client_info = f"Novo cliente conectado: {websocket.remote_address}"
        logging.info(client_info)
        connected_clients.add(websocket)
        try:
            async for message in websocket:
                broadcast_message = f"Mensagem de {websocket.remote_address}: {message}"
                logging.info(broadcast_message)
                await asyncio.wait([client.send(message) for client in connected_clients])
        finally:
            disconnect_info = f"Cliente desconectado: {websocket.remote_address}"
            logging.info(disconnect_info)
            connected_clients.remove(websocket)

    async def start(self):
        self.server = await websockets.serve(self.handler, self.host, self.port)
        await self.server.wait_closed()

    def stop(self):
        if self.server:
            self.server.close()

# Função para iniciar o servidor em uma thread separada
def start_server(host, port, output_widget):
    server = WebSocketServer(host, port)

    def run_server():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(server.start())

    server_thread = threading.Thread(target=run_server, daemon=True)
    server_thread.start()

    output_widget.insert(tk.END, f"Servidor iniciado em {host}:{port}\n")
    logging.info(f"Servidor iniciado em {host}:{port}")

    return server

# Função para parar o servidor
def stop_server(server, output_widget):
    if server:
        server.stop()
        output_widget.insert(tk.END, "Servidor desligado.\n")
        logging.info("Servidor desligado.")
    else:
        output_widget.insert(tk.END, "Servidor não está em execução.\n")
        logging.info("Tentativa de desligar um servidor não iniciado.")

# Função para o botão de iniciar o servidor
def on_start_server(output_widget, host_entry, port_entry):
    host = host_entry.get()
    port = int(port_entry.get())
    global server
    server = start_server(host, port, output_widget)

# Função para o botão de parar o servidor
def on_stop_server(output_widget):
    global server
    stop_server(server, output_widget)

# Interface gráfica usando Tkinter
def create_gui():
    window = tk.Tk()
    window.title("Gerenciador de Servidor WebSocket")

    # Container de host e porta
    frame = tk.Frame(window)
    frame.pack(pady=10)

    tk.Label(frame, text="Host:").grid(row=0, column=0, padx=5)
    host_entry = tk.Entry(frame)
    host_entry.grid(row=0, column=1, padx=5)
    host_entry.insert(0, "0.0.0.0")

    tk.Label(frame, text="Porta:").grid(row=1, column=0, padx=5)
    port_entry = tk.Entry(frame)
    port_entry.grid(row=1, column=1, padx=5)
    port_entry.insert(0, "8765")

    # Botões de iniciar e parar o servidor
    button_frame = tk.Frame(window)
    button_frame.pack(pady=10)

    start_button = tk.Button(button_frame, text="Iniciar Servidor", command=lambda: on_start_server(output_text, host_entry, port_entry))
    start_button.grid(row=0, column=0, padx=10)

    stop_button = tk.Button(button_frame, text="Desligar Servidor", command=lambda: on_stop_server(output_text))
    stop_button.grid(row=0, column=1, padx=10)

    # Área de texto para mostrar a saída do servidor
    output_text = scrolledtext.ScrolledText(window, width=50, height=15)
    output_text.pack(pady=10)

    window.mainloop()

if __name__ == "__main__":
    create_gui()
