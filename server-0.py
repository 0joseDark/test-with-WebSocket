import asyncio
import websockets
import logging

# Configuração do log para registrar atividades do servidor
logging.basicConfig(filename="server_log.txt", level=logging.INFO, format="%(asctime)s - %(message)s")

# Dicionário de usuários para autenticação (username: password)
USERS = {
    "user1": "password1",
    "user2": "password2",
}

async def authenticate(websocket):
    """
    Função de autenticação do usuário. Solicita username e password do cliente.
    """
    await websocket.send("Digite o seu username:")
    username = await websocket.recv()

    await websocket.send("Digite a sua password:")
    password = await websocket.recv()

    # Verifica se as credenciais são válidas
    if USERS.get(username) == password:
        await websocket.send("Autenticação bem-sucedida.")
        logging.info(f"Usuário {username} autenticado com sucesso.")
        return username
    else:
        await websocket.send("Autenticação falhou.")
        logging.warning(f"Falha na autenticação para o usuário {username}.")
        return None

async def handle_client(websocket, path):
    """
    Gerencia a conexão de um cliente após a autenticação.
    """
    username = await authenticate(websocket)
    if username:
        try:
            async for message in websocket:
                logging.info(f"Mensagem recebida de {username}: {message}")
                await websocket.send(f"Servidor recebeu a mensagem: {message}")
        except websockets.ConnectionClosed as e:
            logging.info(f"Conexão encerrada para o usuário {username}: {e}")
    else:
        await websocket.close()

# Função principal que inicia o servidor WebSocket
async def main():
    """
    Configura e inicia o servidor WebSocket.
    """
    server = await websockets.serve(handle_client, "localhost", 8765)
    logging.info("Servidor WebSocket iniciado em ws://localhost:8765")
    await server.wait_closed()

# Ponto de entrada do script
if __name__ == "__main__":
    asyncio.run(main())
