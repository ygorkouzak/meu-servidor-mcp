from mcp.server.fastmcp import FastMCP

# Inicializa o servidor MCP
mcp = FastMCP("MeuServidorLocal")

@mcp.tool()
def ler_saudar_usuario(nome: str) -> str:
    """Uma ferramenta que saúda o usuário pelo nome."""
    return f"Olá {nome}! O servidor MCP local está funcionando com a OpenAI!"

if __name__ == "__main__":
    mcp.run()
