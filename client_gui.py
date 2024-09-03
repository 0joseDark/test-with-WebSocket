import asyncio
import websockets
import threading
import tkinter as tk
from tkinter import scrolledtext, messagebox
import logging

# Configuração do log para registrar atividades do cliente
logging.basicConfig(filename="client_log.txt", level=logging.INFO, format="%(asctime)s - %(message)s")

# Classe que gerencia a conexão WebSocket
class WebSocketClient:
    def __init__(self, host, port):
        """
        Inicializa o cliente WebSocket com o host e a porta fornecidos.
        """
        self.host = host
        self.port = port
        self.websocket = None  # Inicialmente, não há conexão WebSocket
        self.connected = False  # Flag para verificar se o cliente está conectado

    async def connect(self):
        """
        Estabelece uma conexão com o servidor WebSocket.
        """
        try:
            self.websocket = await websockets.connect(f"ws://{self.host}:{self.port}")
            self.connected = True
            logging.info(f"Conectado ao servidor em {self.host}:{self.port}")
        except Exception as e:
            logging.error(f"Erro ao conectar: {e}")
            messagebox.showerror("Erro", f"Não foi possível conectar ao servidor: {e}")

    async def disconnect(self):
        """
        Desconecta do servidor WebSocket.
        """
        if self.websocket:
            await self.websocket.close()
            self.connected = False
            logging.info(f"Desconectado do servidor em {self.host}:{self.port}")

    async def send_message(self, message):
        """
        Envia uma mensagem ao servidor WebSocket.
        """
        if self.connected and self.websocket:
            await self.websocket.send(message)
            logging.info(f"Mensagem enviada: {message}")

# Função para iniciar a conexão com o servidor WebSocket
def start_connection(client, output_widget):
    """
    Inicia a conexão ao servidor WebSocket em uma thread separada.
    """
    def run_client():
        asyncio.run(client.connect())
        if client.connected:
            output_widget.insert(tk.END, f"Conectado ao servidor em {client.host}:{client.port}\n")

    threading.Thread(target=run_client, daemon=True).start()

# Função para encerrar a conexão com o servidor WebSocket
def stop_connection(client, output_widget):
    """
    Desconecta do servidor WebSocket em uma thread separada.
    """
    def run_client():
        asyncio.run(client.disconnect())
        if not client.connected:
            output_widget.insert(tk.END, "Desconectado do servidor.\n")

    threading.Thread(target=run_client, daemon=True).start()

# Função para enviar uma mensagem ao servidor WebSocket
def send_message(client, message_entry):
    """
    Envia uma mensagem para o servidor WebSocket.
    """
    message = message_entry.get()  # Obtém o texto inserido pelo usuário
    if client.connected:
        asyncio.run(client.send_message(message))
        message_entry.delete(0, tk.END)  # Limpa o campo de entrada de texto após o envio

# Função que cria a interface gráfica (GUI) usando Tkinter
def create_gui():
    """
    Cria a interface gráfica do cliente WebSocket.
    """
    window = tk.Tk()
    window.title("Cliente WebSocket")

    # Container para os campos de entrada de host e porta
    frame = tk.Frame(window)
    frame.pack(pady=10)

    # Campo de entrada para o host
    tk.Label(frame, text="Host:").grid(row=0, column=0, padx=5)
    host_entry = tk.Entry(frame)
    host_entry.grid(row=0, column=1, padx=5)
    host_entry.insert(0, "127.0.0.1")  # Host padrão (localhost)

    # Campo de entrada para a porta
    tk.Label(frame, text="Porta:").grid(row=1, column=0, padx=5)
    port_entry = tk.Entry(frame)
    port_entry.grid(row=1, column=1, padx=5)
    port_entry.insert(0, "8765")  # Porta padrão

    # Botões para conectar e desconectar do servidor WebSocket
    button_frame = tk.Frame(window)
    button_frame.pack(pady=10)

    # Instancia o cliente WebSocket
    client = WebSocketClient(host_entry.get(), int(port_entry.get()))

    # Botão para conectar
    connect_button = tk.Button(button_frame, text="Conectar", command=lambda: start_connection(client, output_text))
    connect_button.grid(row=0, column=0, padx=10)

    # Botão para desconectar
    disconnect_button = tk.Button(button_frame, text="Desconectar", command=lambda: stop_connection(client, output_text))
    disconnect_button.grid(row=0, column=1, padx=10)

    # Campo de entrada e botão para enviar mensagens
    message_frame = tk.Frame(window)
    message_frame.pack(pady=10)

    tk.Label(message_frame, text="Mensagem:").grid(row=0, column=0, padx=5)
    message_entry = tk.Entry(message_frame, width=40)
    message_entry.grid(row=0, column=1, padx=5)

    send_button = tk.Button(message_frame, text="Enviar", command=lambda: send_message(client, message_entry))
    send_button.grid(row=0, column=2, padx=10)

    # Área de texto para mostrar a saída (logs, mensagens)
    output_text = scrolledtext.ScrolledText(window, width=50, height=15)
    output_text.pack(pady=10)

    window.mainloop()  # Inicia o loop principal da interface gráfica

# Ponto de entrada do script
if __name__ == "__main__":
    create_gui()
