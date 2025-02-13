import discord
from discord import app_commands
from discord.ext import commands
import json
import sqlite3


intents = discord.Intents.default()
intents.guilds = True
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix=';', intents=intents)

ARQUIVO_APELIDOS = "apelidos.json"

apelidos = {}


xp_por_nivel = {
    1: 0,
    2: 300,
    3: 900,
    4: 2700,
    5: 6500,
    6: 14000,
    7: 23000,
    8: 34000,
    9: 48000,
    10: 64000,
    11: 85000,
    12: 100000,
    13: 120000,
    14: 140000,
    15: 165000,
    16: 195000,
    17: 225000,
    18: 265000,
    19: 305000,
    20: 355000
}

gif_triste = [
    "https://i.gifer.com/origin/2b/2bef5dcb100766198394e5bd1bcff395_w200.gif",
    "https://i.pinimg.com/originals/29/04/46/290446f550eb85cb9b414dfd1f660109.gif",
    "https://media4.giphy.com/media/v1.Y2lkPTc5MGI3NjExZTB6bWRpYng0NGZkMnBzcWV1MW1iNmRtenVvM3pyemtmN2lqbThiNiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/EALdarQtRPFnO/giphy.webp",
    "https://i.pinimg.com/originals/23/4e/fd/234efd2c48b8a2c734cf8d476b082377.gif",
    "https://media.tenor.com/ZRdwRINZSeUAAAAC/triste-sad.gif",
    "https://i.pinimg.com/originals/04/36/bf/0436bfc9861b4b57ffffda82d3adad6e.gif",
    "https://media.tenor.com/images/4b5e9867209d7b1712607958e01a80f1/tenor.gif",
    "https://aniyuki.com/wp-content/uploads/2022/01/aniyuki-anime-girl-crying-gifs-39.gif",
    "https://i.pinimg.com/originals/e6/0d/b6/e60db6e53d6071d10d08e93dbc6c48a1.gif",
    "https://aniyuki.com/wp-content/uploads/2022/01/aniyuki-anime-girl-crying-gifs-29.gif",
    "https://media.tenor.com/CIEu-0G58gcAAAAC/anime.gif",
    "https://media2.giphy.com/media/v1.Y2lkPTc5MGI3NjExZmdsY3B6cDNnZGg3cHNpdnQ3a2o3b3pxZ3pnejBnemowdTJtMWNsbyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/3fmRTfVIKMRiM/giphy.webp"
]

gif_feliz = [
    "https://media4.giphy.com/media/v1.Y2lkPTc5MGI3NjExc2Q5Z3hvYjhveGQ5cjA0aDVzaHNzNmRiZ3NkMDZkNzd2MDQzenIzcCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/13k4VSc3ngLPUY/giphy.webp",
    "https://i.giphy.com/13G7hmmFr9yuxG.webp",
    "https://c.tenor.com/V7iWZMQLPDMAAAAC/tenor.gif",
    "https://c.tenor.com/WU4iBeEeK88AAAAd/tenor.gif",
    "https://www.gifcen.com/wp-content/uploads/2022/05/anime-gif-7.gif",
    "https://i.gifer.com/origin/e3/e3ae369ad93835f8a30a503ae116e3fb.gif",
    "https://media.tenor.co/images/7f4d56cef853d7a1135bdc9dc53f46d3/raw",
    "https://c.tenor.com/lVXo9rYZECIAAAAC/anime-happy.gif",
    "https://c.tenor.com/v3mmhTRfBosAAAAC/tenor.gif",
    "https://c.tenor.com/nBWlYPbKxzwAAAAC/tenor.gif",
    "https://c.tenor.com/dbN19CnNn5QAAAAC/minions-dance.gif",
    "https://i.pinimg.com/originals/3f/a2/c7/3fa2c7e54f7e7b13742f2996e35a3d61.gif",
    "https://media.tenor.com/f_47e8MKBpAAAAAd/dance-anime.gif",
    "https://media.tenor.com/MinXQiaQUHsAAAAC/anime-happy-anime.gif",
    "https://usagif.com/wp-content/uploads/gify/46-anime-dance-madoka-magica-pmmm.gif"
]

gif_beijar = [
    "https://i.gifer.com/2uEt.gif",
    "https://i.gifer.com/B835.gif",
    "https://i.gifer.com/2lte.gif",
    "https://i.gifer.com/i0I.gif",
    "https://i.gifer.com/2QHD.gif",
    "https://i.gifer.com/C1et.gif",
    "https://i.gifer.com/AUhu.gif",
    "https://c.tenor.com/VMdN4bSBk7UAAAAC/nasuke-kiss.gif",
    "https://usagif.com/wp-content/uploads/gify/naruto-sudden-kiss-with-sasuke-usagifdotcom.gif",
    "https://i.gifer.com/8Uc1.gif",
    "https://i.gifer.com/XsqT.gif"
]


def verificar_nivel(xp):
    #ordem decressente
    for nivel in sorted(xp_por_nivel.keys(), reverse=True):
        if xp >= xp_por_nivel[nivel]:
            return nivel

def conectar_sqlite():
    try:
        return sqlite3.connect("bot_db")
    except mysql.connector.Error as err:
        print(f"Erro ao conectar ao no banco de dados: {err}")
        return None

def carregar_fichas():
    botDB = conectar_sqlite()
    botDB.row_factory = sqlite3.Row  # Permite acessar colunas por nome
    cursor = botDB.cursor()

    cursor.execute("SELECT * FROM fichas")
    
    # Converter as linhas para dicionários
    fichas = {str(row["fichas_id"]): dict(row) for row in cursor.fetchall()}

    cursor.close()
    botDB.close()
    
    return fichas

def salvar_fichas(fichas):
    botDB = conectar_sqlite()
    cursor = botDB.cursor()

    for ficha_id, ficha in fichas.items():
        query = """
        INSERT INTO fichas (fichas_id, fichas_nome, fichas_nivel, fichas_classe, fichas_raca, fichas_xp, 
                            forca, destreza, constituicao, inteligencia, sabedoria, carisma, fichas_imagem)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(fichas_id) DO UPDATE SET 
            fichas_nome = excluded.fichas_nome, 
            fichas_nivel = excluded.fichas_nivel, 
            fichas_classe = excluded.fichas_classe, 
            fichas_raca = excluded.fichas_raca, 
            fichas_xp = excluded.fichas_xp, 
            forca = excluded.forca, 
            destreza = excluded.destreza, 
            constituicao = excluded.constituicao, 
            inteligencia = excluded.inteligencia, 
            sabedoria = excluded.sabedoria, 
            carisma = excluded.carisma, 
            fichas_imagem = excluded.fichas_imagem
        """

        valores = (
            ficha_id,
            ficha['fichas_nome'],
            ficha['fichas_nivel'],
            ficha['fichas_classe'],
            ficha['fichas_raca'],
            ficha['fichas_xp'],
            ficha['forca'],
            ficha['destreza'],
            ficha['constituicao'],
            ficha['inteligencia'],
            ficha['sabedoria'],
            ficha['carisma'],
            ficha['fichas_imagem']
        )

        cursor.execute(query, valores)
    
    botDB.commit()
    cursor.close()
    botDB.close()

def carregar_apelidos():
    global apelidos
    try:
        with open(ARQUIVO_APELIDOS, "r") as arquivo:
            apelidos = json.load(arquivo)
    except FileNotFoundError:
        apelidos = {}

def salvar_apelidos():
    with open(ARQUIVO_APELIDOS, "w") as arquivo:
        json.dump(apelidos, arquivo, indent=4)

def carregar_armas():
    botDB = conectar_sqlite()
    botDB.row_factory = sqlite3.Row  
    cursor = botDB.cursor()

    cursor.execute("SELECT * FROM armas")
    
    armas = {str(row["armas_id"]): dict(row) for row in cursor.fetchall()}

    cursor.close()
    botDB.close()
    
    return armas

def salvar_armas(armas):
    botDB = conectar_sqlite()
    cursor = botDB.cursor()

    for arma_id, arma in armas.items():
        query = """
        INSERT INTO armas (armas_id, armas_nome, armas_dano, armas_preco, armas_peso, armas_categoria, armas_propriedades)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(armas_id) DO UPDATE SET
            armas_nome = excluded.armas_nome,
            armas_dano = excluded.armas_dano,
            armas_peso = excluded.armas_peso,
            armas_preco = excluded.armas_preco,
            armas_categoria = excluded.armas_categoria,
            armas_propriedades = excluded.armas_propriedades
        """
        valores = (
            arma_id,
            arma['nome'],     
            arma['dano'],
            arma['preco'],    
            arma['peso'],     
            arma['categoria'],
            arma['propriedades']
        )

        cursor.execute(query, valores)

    botDB.commit()
    cursor.close()
    botDB.close()

def carregar_armas_ficha(player_id):
    botDB = conectar_sqlite()
    botDB.row_factory = sqlite3.Row
    cursor = botDB.cursor()

    query = """
    SELECT armas.armas_nome, armas.armas_dano, armas.armas_propriedades, armas.armas_peso, armas.armas_categoria
    FROM fichas_armas
    INNER JOIN fichas ON fichas.fichas_id = fichas_armas.ficha_id
    INNER JOIN armas ON armas.armas_id = fichas_armas.arma_id
    WHERE fichas.fichas_id = ?;
    """
    
    cursor.execute(query, (player_id,))
    armas = cursor.fetchall()
    return armas


class ficha_modal(discord.ui.Modal):
    def __init__(self):
        super().__init__(title='Criar sua Ficha')

        self.nome = discord.ui.TextInput(label='Nome', placeholder='*Fulano', max_length=35, min_length=2)
        self.raca = discord.ui.TextInput(label='Raça', placeholder='*Humano', max_length=35)
        self.classe = discord.ui.TextInput(label='Classe', placeholder='*guerreiro')
        self.xp = discord.ui.TextInput(label='XP', placeholder='*1500')
        self.atributos = discord.ui.TextInput(label='Em ordem (for, des, cons, int, sab, car)', placeholder='15, 12, 13, 10, 8, 14', style=discord.TextStyle.paragraph)

        self.add_item(self.nome)
        self.add_item(self.raca)
        self.add_item(self.classe)
        self.add_item(self.xp)
        self.add_item(self.atributos)

    async def on_submit(self, interact:discord.Interaction):
        fichas = carregar_fichas()
        membro = str(interact.user.id)
        
        nivel = verificar_nivel(int(self.xp.value))

        atributos = self.atributos.value
        if ',' in atributos:
            atributos_lista = self.atributos.value.split(',')
        else:
            atributos_lista = self.atributos.value.split(' ')

        for atributo in atributos_lista:
            atributo = int(atributo.strip())

        fichas[membro] = {"fichas_nome": self.nome.value, 
            "fichas_nivel": nivel, 
            "fichas_classe": self.classe.value, 
            "fichas_raca": self.raca.value, 
            "fichas_xp": self.xp.value, 
            "forca": atributos_lista[0], 
            "destreza": atributos_lista[1], 
            "constituicao": atributos_lista[2], 
            "inteligencia": atributos_lista[3], 
            "sabedoria": atributos_lista[4], 
            "carisma":atributos_lista[5], 
            "fichas_imagem": None
        }

        salvar_fichas(fichas)
        await interact.response.send_message('Ficha Salva com Sucesso!', ephemeral=True)

class nova_arma_modal(discord.ui.Modal):
    def __init__(self):
        super().__init__(title='Nova Arma')

        self.nome = discord.ui.TextInput(
            label='Nome da Arma',
            placeholder='*Não coloque nomes repetidos. Antes, use ;?arma (nome)',
            max_length=35, min_length=2
        )

        self.dano = discord.ui.TextInput(
            label='Dano',
            placeholder='Exemplo: 1d4 perfurante',
            max_length=35
        )

        self.peso = discord.ui.TextInput(
            label='Peso(Kg)',
            placeholder='exemplo: 1.5',
            max_length=4, 
            required=False
        )

        self.propriedades = discord.ui.TextInput(
            label='Propriedades',
            placeholder='Exemplo: Acuidade, leve, arremesso (distância 6/18)'
        )

        self.categoria = discord.ui.TextInput(
            label='Categoria',
            placeholder='Exemplo: Arma Simples Corpo-a-Corpo'
        )


        self.add_item(self.nome)
        self.add_item(self.dano)
        self.add_item(self.peso)
        self.add_item(self.propriedades)
        self.add_item(self.categoria)
        

    async def on_submit(self, interaction: discord.Interaction):
        botDB = conectar_sqlite()
        cursor = botDB.cursor()

        # Verificar o maior ID existente
        cursor.execute("SELECT MAX(armas_id) FROM armas")
        max_id = cursor.fetchone()[0] or 0 
        novo_id = max_id + 1  

        cursor.execute("SELECT armas_nome FROM armas")
        nomes_armas = [row[0] for row in cursor.fetchall()]

        armas = carregar_armas()
        nome_arma = self.nome.value.lower().strip()
        if nome_arma in [nome.lower() for nome in nomes_armas]:
            await interaction.response.send_message(f'Arma {nome_arma} já existe, use outro nome!')
            return
        
        conteudo = {
            "nome": self.nome.value.capitalize(),
            "preco": None,
            "dano": self.dano.value,
            "peso": self.dano.value,
            "propriedades": self.propriedades.value,
            "categoria": self.categoria.value,
        }

        arma = {}
        arma[novo_id] = conteudo
        salvar_armas(arma)



        cursor.close()
        botDB.close()

        await interaction.response.send_message(f"Arma **{self.nome.value}** criada com sucesso!", ephemeral=True)

from discord.ui import Button
class ConfirmView(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.value = None

    @discord.ui.button(label='Sim', style=discord.ButtonStyle.green)
    async def confirm(self, interaction: discord.Interaction, button: Button):
        await interaction.response.send_modal(ficha_modal())
        self.value = True
        self.stop()

    @discord.ui.button(label='Não', style=discord.ButtonStyle.red)
    async def cancel(self, interaction: discord.Interaction, button: Button):
        await interaction.response.send_message('Operação cancelada.', ephemeral=True)
        self.value = False
        self.stop()


@bot.event
async def on_ready():
    carregar_apelidos()
    #await bot.tree.sync() -> ative apenas se quiser sincronizar os comandos slash toda vez que ligar o bot 
    #para sicronizar manualmente use ;sicronizar
    print(f"O bot {bot.user} está online!")


@bot.command(name='xp')
async def adicionar_xp(ctx:commands.Context, num:int = None):
    fichas = carregar_fichas()

    if str(ctx.author.id) in fichas:
        jogador = fichas[str(ctx.author.id)]
        nome = jogador['fichas_nome']
        if num is None:
            xp = jogador['fichas_xp']
            await ctx.send(f'{nome}, você tem {xp} de XP')
            return

        jogador['fichas_xp'] += num
        xp = jogador['fichas_xp']
        
        
        nivel_anterior = jogador['fichas_nivel']
        nivel = verificar_nivel(xp)

        if nivel == nivel_anterior:
            await ctx.send(f'{nome}, você recebeu {num} de XP! Agora tendo um total de {xp}')

        else:
            await ctx.send(f'**Parabens você subiu para o nivel {nivel}**\n agora vc tem um total de {xp} de XP')

        salvar_fichas(jogador)
    else:
        await ctx.send(f"{ctx.author.display_name}, você ainda não tem uma ficha!")


@bot.command(name="ficha")
async def ver_ficha(ctx: commands.Context, membro: discord.Member = None):

    if membro:  
        jogador_id = str(membro.id) 
        apelido = apelidos.get(str(membro.id), membro.display_name)
    else:    
        jogador_id = str(ctx.author.id)
        autor = ctx.author
        apelido = autor.display_name
    
    fichas = carregar_fichas()


    if jogador_id not in fichas:
        await ctx.send(f"{apelido}, ainda não tem uma ficha.")
        return
    
    ficha = fichas[jogador_id]

    atributos = [
        ficha['forca'],
        ficha['destreza'],
        ficha['constituicao'],
        ficha['inteligencia'],
        ficha['sabedoria'],
        ficha['carisma'] 
        ]
    
    mod = [(num - 10) // 2 for num in atributos] 


    mensagem =discord.Embed(title= f"Ficha de {apelido}",
    description=f"Nome: {ficha['fichas_nome']}\n" \
                f"Raça: {ficha['fichas_raca']}\n" \
                f"Classe: {ficha['fichas_classe']}\n" \
                f"Nível: {ficha['fichas_nivel']}"\

    )
    
    mensagem.add_field(name='Atributos', value=f"\nFor: {ficha['forca']}\nDes: {ficha['destreza']}\n" \
                f"Con: {ficha['constituicao']}\nInt: {ficha['inteligencia']}" \
                f"\nSab: {ficha['sabedoria']}\nCar: {ficha['carisma']}", inline=True
                )
    mensagem.add_field(name='Modificadores', value=f"\n{mod[0]}\n{mod[1]}\n" \
                                                    f"{mod[2]}\n{mod[3]}\n" \
                                                    f"{mod[4]}\n{mod[5]}", inline=True)

    if ficha['fichas_imagem']:
        mensagem.set_thumbnail(url=ficha['fichas_imagem'])
    

    await ctx.send(embed=mensagem)


@bot.tree.command(description='criar sua ficha')
async def criar_ficha(interaction: discord.Interaction):
    fichas = carregar_fichas()
    membro = str(interaction.user.id)

    if membro in fichas:
        view = ConfirmView()
        await interaction.response.send_message(
            'Você já tem uma ficha, deseja reescrever?',
            view=view,
            ephemeral=True
        )
    else:
        await interaction.response.send_modal(ficha_modal())


@bot.command(name='foto_ficha')
async def definir_imagem(ctx: commands.Context):
    autor = ctx.author
    apelido = apelidos.get(str(autor.id), autor.display_name) 
    jogador_id = str(ctx.author.id)
    fichas = carregar_fichas()
    autor = ctx.author
    apelido = apelidos.get(str(autor.id), autor.display_name)

    if jogador_id not in fichas:
        await ctx.send(f"{ctx.author.name}, você ainda não tem uma ficha.")
        return

    await ctx.send("Envie a imagem da sua ficha.")
    imagem_msg = await bot.wait_for('message', check=lambda message: message.author == ctx.author and message.attachments)

    if imagem_msg.attachments:
        imagem_url = imagem_msg.attachments[0].url
        fichas[jogador_id]['fichas_imagem'] = imagem_url
        salvar_fichas(fichas)
        await ctx.send(f"Imagem da ficha de {apelido} foi definida com sucesso!")
    else:
        await ctx.send("Você não enviou uma imagem. Tente novamente.")


@bot.command(name="upd_atributos")
async def atualizar_atributos(ctx: commands.Context, *,atributos:str):

    atributos = atributos.lower().strip()
    atributos = atributos.replace('ç', 'c')
    atributos = atributos.replace('ê', 'e')
    atributos = atributos.replace('ã', 'a')
    
    fichas = carregar_fichas()
    jogador_id = str(ctx.author.id)
    apelido = apelidos.get(jogador_id, ctx.author.display_name)
    ficha = fichas[jogador_id]

    
    if ',' in atributos:
        lista = atributos.split(',')
        lista[1] = lista[1].strip()
        ficha[str(lista[0])] += 1
        ficha[str(lista[1])] += 1

    else:
        lista = atributos.split(' ')
        if len(lista) == 2:
            lista[1] = lista[1].strip()
            lista[0] = lista[0].strip()
            ficha[str(lista[0])] += 1
            ficha[str(lista[1])] += 1

            #se colocar só um são 2 pontos
        else:
            atributos = lista[0].strip()
            ficha[str(atributos)] += 2
            
        fichas[jogador_id] = ficha
        salvar_fichas(fichas)

    await ctx.send(f'ficha de {apelido} atualizada, ')


@bot.command(name='armas')
async def armas(ctx: commands.Context, membro: discord.Member = None):
    if membro:
        ficha_id = str(membro.id)
        apelido = apelidos.get(str(membro.id), membro.display_name)

        fichas = carregar_fichas()  
        ficha = fichas[str(ficha_id)]
        
        if not ficha:
            await ctx.send(f"{membro.mention}, não possui ficha cadastrada")
            return

    else:
        apelido = apelidos.get(str(ctx.author.id), ctx.author.display_name)

        ficha_id = ctx.author.id
        fichas = carregar_fichas()  
        ficha = fichas[str(ficha_id)]

        if not ficha:
            await ctx.send(f"{apelido}, você não possui ficha cadastrada")
            return
    
    armas = carregar_ficha_armas(ficha_id)

    if not armas:
        await ctx.send(f" Nenhuma arma encontrada para a ficha '{ficha["fichas_nome"]}' de {apelido}.")
        return

    embed = discord.Embed(
    title=f"Armas da ficha **{ficha['fichas_nome']}** de {apelido}",
    color=discord.Color.blue()
    )

    for arma in armas:
        embed.add_field(
            name=f"**{arma['armas_nome']}**",
            value=(
                f"**Dano:** {arma['armas_dano']}\n"
                f"**Propriedades:** {arma['armas_propriedades']}\n"
                f"**Peso:** {arma['armas_peso']}Kg\n"
                f"**Categoria:** {arma['armas_categoria']}"
            ),inline=False)
    await ctx.send(embed=embed)


@bot.command(name='adicionar_arma')
async def adicionar_arma(ctx: commands.Context, *, nome_arma: str):
    botDB = conectar_sqlite()
    cursor = botDB.cursor()

    nome_arma = nome_arma.strip()
    nome_arma = nome_arma.lower()

    id = str(ctx.author.id)
    fichas = carregar_fichas()
    ficha = fichas.get(id, {})

    if not ficha:
        await ctx.send(f"{ctx.author.mention} não possui ficha cadastrada.", ephemeral=True)
        return

    query = """
        SELECT armas_id FROM armas 
        WHERE LOWER(armas_nome) = ?
    """
    cursor.execute(query, (nome_arma,))
    arma = cursor.fetchone()  

    if arma:
        
        query = """
        INSERT INTO fichas_armas (ficha_id, arma_id) VALUES (?, ?)
        """
        valores = (id, arma[0])  
        cursor.execute(query, valores)
        botDB.commit()  
        await ctx.send(f'Arma "{nome_arma}" adicionada à sua ficha.')

    else:
        await ctx.send(f'Arma "{nome_arma}" não encontrada.')
    
    cursor.close()  
    botDB.close()  


@bot.tree.command(description='Criar uma arma nova')
async def criar_arma(interaction: discord.Interaction):
    await interaction.response.send_modal(nova_arma_modal())


@bot.command(name='?arma')
async def pesquisar_arma(ctx: commands.Context, *,nome_arma: str):
    botDB = conectar_sqlite()
    botDB.row_factory = sqlite3.Row  # Permite acessar colunas por nome
    cursor = botDB.cursor()
    nome_arma = nome_arma.lower().strip()


    query = """
        SELECT * from armas 
        where lower(armas_nome) like ?
    """
    parametro = "%" + nome_arma + "%"
    cursor.execute(query, (parametro,))
    armas_arma = cursor.fetchall()

    resultados = 0
    mensagem = discord.Embed(title=' ')

    for arma in armas_arma:
        mensagem.add_field(
                name=f'**{arma["armas_nome"]}**\n',
                value=f'**Preço**: {arma["armas_preco"]}\n'
                f"**Dano**: {arma['armas_dano']}\n"
                f"**Peso**: {arma['armas_peso']}Kg\n"
                f"**Propriedades**: {arma['armas_propriedades']}\n"
                f"**Categoria**: {arma['armas_categoria']}\n", 
                inline= False
            )
        resultados += 1

        mensagem.description = f'{resultados} resultados para "{nome_arma}"'

    await ctx.send(embed=mensagem)


@bot.command(name="oi")
async def oi(ctx: commands.Context):
    autor = ctx.author
    apelido = apelidos.get(str(autor.id), autor.display_name) 
    await ctx.reply(f"Oi {apelido}")


@bot.command(name='nick')
async def nick(ctx: commands.Context, *, nick: str = None):
    if not nick:
        await ctx.send("Você deve colocar o nick após o comando. Exemplo: ;nick Macacopelado")
        return
    else:
        apelidos[str(ctx.author.id)] = nick
        salvar_apelidos() 
        await ctx.reply(f"Seu apelido foi definido como {nick}")


@bot.command(name="xingar")
async def xingar(ctx: commands.Context, membro: discord.Member = None):
    autor = ctx.author
    if membro:
        apelido = apelidos.get(str(membro.id), membro.display_name)

    else:
        apelido = apelidos.get(str(autor.id), autor.display_name)

    respostas = [
        f"Vai se fuder {apelido}",
        f"Você é um saco, {apelido}!",
        f"você é um bosta, {apelido}, aceita!"
    ]
    await ctx.send(random.choice(respostas))


@bot.command(name='beijar')
async def beijar(ctx: commands.Context, membro: discord.Member = None):
    
    if str(membro.id) == "1314269297475846157":
        await ctx.reply('Eca! Que nojo! Claro que não. 🤢')
        return
    autor = ctx.author
    apelido1 = apelidos.get(str(autor.id), autor.display_name)
    apelido2 = apelidos.get(str(membro.id), membro.display_name)

    msg_beijar = [
        f"{apelido2} não gostou",
        f"{apelido2} gostou",
        "foi um beijo gostoso",
        "foi beijo molhado e demorado",
        "foi um beijo apaixonado",
        "foi um beijo forçado",
        f"após o beijo {apelido2} deu um soco em {apelido1}",
        f"após o beijo {apelido1} e {apelido2} se apaixonaram e viveram felizes Juntos"
    ]

    msg = discord.Embed(title= f"{apelido1} Beijou💋 {apelido2}",
    description= random.choice(msg_beijar)
    )

    msg.set_image(url= random.choice(gif_beijar))
    await ctx.send(embed= msg)


@bot.command(name="calc")
async def somar(ctx: commands.Context, num1: float, op: str, num2: float):
    try:
        if op == '/':
            resultado = num1 / num2
            await ctx.send(f"A divisão de {num1} / {num2} é igual a {resultado}")
        if op == '*':
            resultado = num1 * num2
            await ctx.send(f"A multiplicção de {num1} * {num2} é igual a {resultado}")
        if op == '+':
            resultado = num1 + num2
            await ctx.send(f"A soma de {num1} + {num2} é igual a {resultado}")
        if op == '-':
            resultado = num1 - num2
            await ctx.send(f"A subtração de {num1} - {num2} é igual a {resultado}")
        if op == '**':
            resultado = num1 ** num2
            await ctx.send(f"A soma de {num1} ** {num2} é igual a {resultado}")
    except ValueError:
        await ctx.send(f'algo deu errado, use o modelo `;calc 25 / 5` operações(/, *, +, -, **)', ephemeral=True)


@bot.command(name= "falar")
async def falar(ctx: commands.Context, *, frase):
    frase = frase.strip()
    await ctx.send(frase)


@bot.command(name="enviar")
async def enviar(ctx, canal_id: int, *, mensagem: str):
    try:
        # Obter o objeto do canal pelo ID
        canal = bot.get_channel(canal_id)
        if not canal:
            await ctx.send("Canal não encontrado. Verifique se o ID está correto.")
            return
        
        # Enviar a mensagem
        await canal.send(mensagem)
        await ctx.send(f"Mensagem enviada para o canal {canal.mention} com sucesso!")
    except discord.Forbidden:
        await ctx.send("Não tenho permissão para enviar mensagens nesse canal.")
    except discord.HTTPException as e:
        await ctx.send(f"Erro ao tentar enviar a mensagem: {e}")


@bot.command(name="ajuda")
async def ajuda(ctx: commands.Context):
    comandos = [
        {"nome": ";rolar", "descricao": "Rola dados no formato XdY, onde X é a quantidade de dados e Y o número de lados."},
        {"nome": ";rolar_c", "descricao": "diferente do anterior on 2d4+1 = (1d4+1d4)+1, nesse = (1d4+1)+(1d4+1)"},
        {"nome": ";xp", "descricao": "Adiciona XP à sua ficha `;xp 300`. Ou caso você não coloque nenhum valor `;xp` ele mostra seu XP atual"},
        {"nome": ";foto_ficha", "descricao": "Adiciona uma imagem à sua ficha. mande o comando e depois que for respondido pelo bot mande o arquivo da imagem"},
        {"nome": ";ficha", "descricao": "Exibe a sua ficha, ou a ficha da pessoa que você marcou ex: `;ficha` ou `;ficha @fulano`"},
        {"nome": ";oi", "descricao": "Envia uma saudação personalizada."},
        {"nome": ";nick", "descricao": "Define um apelido para ser usado pelo bot quando se referir a você."},
        {"nome": ";xingar", "descricao": "Envia um xingamento aleatório direcionado a pessoa que você marcou."},
        {"nome": ";calc", "descricao": "calculadora simples `;calc 5 * 6`."},
        {"nome": ";upd_atributos", "descricao": "usado para adicionar pontos aos atributos da ficha. Atualize um atributo `;upd_atributos destreza` e ganhe +2 na base desse atributo ou dois atributos `;upd_atributos destreza inteligencia` +1 pra cada."},
        {"nome": ";falar", "descricao": "Repete a frase fornecida."},
        {"nome": ";beijar", "descricao": "Marque a pessoa que você quer beijar e veja o que acontece"},
        {"nome": ";?arma", "descricao": "pesquise pelo nome de uma arma ou parte do nome `;?arma bes` todas as armas que começam com 'bes' apareceram."},
        {"nome": ";adicionar_arma", "descricao": "adiciona uma arma a sua ficha `;adicionar_arma adaga`."},
        {"nome": ";armas", "descricao": "vê as armas vinculadas a sua ficha ou a de quem você marcou ex: `;armas` ou `;armas @fulano`."},
        {"nome": "/criar_ficha", "descricao": "Abre um formulario para a criação de uma nova Ficha de personagem."},
        {"nome": "/criar_arma", "descricao": "Abre um formulario para a criação de uma nova Arma de D&D."},
    ]

    descricao_comandos = "\n".join([f"**{comando['nome']}**: {comando['descricao']}" for comando in comandos])
    embed = discord.Embed(
        title="Lista de Comandos",
        description=descricao_comandos,
        color=discord.Color.yellow()
    )

    await ctx.send(embed=embed)


@bot.command()
async def sincronizar(ctx: commands.Context):
    sics = await bot.tree.sync()
    await ctx.send(f"{len(sincs)} comandos sincronizados", ephemeral= True)


@bot.event
async def on_member_join(membro:discord.Member):
    server = membro.guild
    canal = discord.utils.get(server.text_channels, name='bem-vindo')
    if canal:
        await canal.send(f'**BEM-VINDO** {f"<@{membro.id}>"} ao servidor {server.name}\n')


@bot.event
async def on_message(message):
    if message.content.startswith(bot.command_prefix):
        await bot.process_commands(message)
        return

    if message.author.bot:
        return

    # Responder se o bot for mencionado
    if bot.user.mentioned_in(message) and not message.mention_everyone:
        await message.channel.send("Me chamou? Use `;ajuda` para ver o que posso fazer!")
        return


    dado = message.content.replace(" ", "")
    if "#" in dado:
        dado = message.content.replace("#", "")
        rolagem_individual = True
    else:
        rolagem_individual = False

    try:
        #verifica o formato da mensagem (1d20, 1d4 etc...)
        if len(dado) > 2 and dado[1] in ['d', 'D']:
            try: 
                numero_dados, numero_lados = int(dado[0]), int(dado[2])
            except Exception as e:
                return

            if "+" in dado:
                base, mod = dado.split("+")
                mod = int(mod)
            elif "-" in dado:
                base, mod = dado.split("-")
                mod = -int(mod)
            else:
                base, mod = dado, 0

            quantidade, lados = base.lower().split("d")
            quantidade = int(quantidade)
            lados = int(lados)

            if quantidade <= 0:
                await message.channel.send("Você deve rolar pelo menos 1 dado!")
                return
            if lados <= 1:
                await message.channel.send("O dado precisa ter mais de 1 lado!")
                return
            if quantidade > 100:
                await message.channel.send("Você não pode rolar mais de 100 dados de uma vez!")
                return

            if rolagem_individual == False:
                resultados = [random.randint(1, lados) for _ in range(quantidade)]
                soma = sum(resultados) + mod
                resultados_str = "\n".join(map(str, resultados))
            elif quantidade > 1 or mod != 0:
                resultados = [random.randint(1, lados) + mod for _ in range(quantidade)]
                soma = sum(resultados)
                resultados_str = '\n'.join([f"({resultado - mod} + {mod}) = {resultado}" for resultado in resultados])

            def criar_embed():
                if mod != 0:
                    if rolagem_individual == False:
                        return discord.Embed(
                            title=f"Rolagem individual: {dado} 🎲",
                            description=(
                                f"**Natural:\n{resultados_str}**\n"
                                f"**Modificador: {mod}**\n"
                                f"**Total: {soma}**"
                            ),
                            color=discord.Color.blue()
                        )
                    else:
                        return discord.Embed(
                            title=f"Rolagem: {dado}🎲",
                            description=(
                                f"{resultados_str}\n"  
                                f"**Total: {soma}**"  
                            ),
                            color=discord.Color.blue()
                        )
                
                elif quantidade == 1:
                    cor = (
                        discord.Color.green() if lados == 20 and resultados[0] == 20 else
                        discord.Color.red() if lados == 20 and resultados[0] == 1 else
                        discord.Color.blue()
                    )
                    descricao = (
                        f"**Resultado: {resultados_str} (Acerto Crítico)**" if resultados[0] == 20 else
                        f"**Resultado: {resultados_str} (Falha Crítica)**" if resultados[0] == 1 else
                        f"**Resultado: {resultados_str}**"
                    )
                    embed = discord.Embed(
                        title=f"Rolagem: {dado} 🎲",
                        description=descricao,
                        color=cor
                    )

                    # Adiciona thumbnails para críticos ou falhas
                    if lados == 20 and resultados[0] == 20:
                        gif = random.choice(gif_feliz) 
                        embed.set_thumbnail(url=gif)
                    elif lados == 20 and resultados[0] == 1:
                        gif = random.choice(gif_triste) 
                        embed.set_thumbnail(url=gif)

                    return embed
                else:
                    return discord.Embed(
                        title=f"Rolagem: {dado} 🎲",
                        description=(
                            f"**\nResultados:\n {resultados_str}**\n"
                            f"**Total: {soma}**"
                        ),
                        color=discord.Color.blue()
                    )

             
            embed = criar_embed()
            await message.channel.send(embed=embed)
    except ValueError:
        await message.channel.send("Formato inválido! Use algo como 1d20 ou 1d20+5.")

    # Garante que outros comandos ainda funcionem
    await bot.process_commands(message)


# Rodando o bot
bot.run("coloque seu token aqui")