import discord
from discord.ext import commands
import os
from flask import Flask
from threading import Thread

# Configuração do bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# Configuração do servidor web (para manter Render acordado)
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot rodando com sucesso!"

def run_web():
    app.run(host='0.0.0.0', port=10000)  # Porta pode ser qualquer uma

# Inicia o servidor web em segundo plano
Thread(target=run_web).start()

# Evento de inicialização do bot
@bot.event
async def on_ready():
    print(f'Bot conectado como {bot.user}')

# Comando !claimed com 4 argumentos
@bot.command()
async def claimed(ctx, *, args):
    try:
        partes = [p.strip() for p in args.split(',')]
        if len(partes) != 4:
            await ctx.send("Formato inválido. Use: !claimed nome da hunt, horário, responsável, status")
            return

        nome_hunt, horario, responsavel, status = partes
        status = status.lower()

        if status == "claimar":
            mensagem = (
                f"✅ **Hunt Claimada!**\n"
                f"**Hunt Escolhida:** {nome_hunt}\n"
                f"**Horário Escolhido:** {horario}\n"
                f"**Responsável pela PT:** {responsavel}"
            )
        elif status == "liberar":
            mensagem = (
                f"❎ **Hunt Liberada!**\n"
                f"**Hunt:** {nome_hunt}\n"
                f"**Horário:** {horario}\n"
                f"**Liberada por:** {responsavel}"
            )
        else:
            await ctx.send("Status inválido. Use 'claimar' ou 'liberar'.")
            return

        await ctx.send(mensagem)
    except Exception as e:
        await ctx.send(f"Ocorreu um erro: {e}")

# Inicia o bot
bot.run(os.getenv('TOKEN'))
