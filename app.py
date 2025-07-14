from api.server import Server
from dotenv import load_dotenv
load_dotenv()

if __name__ == "__main__":
    api_server = Server()
    api_server.run()
