import discord
from discord import app_commands
from discord.ui import Select,View
from discord.ext import tasks
import asyncio
import os
import requests

TOKEN = os.getenv("DISCORD_TOKEN")
URL = "https://api.fogos.pt/v2/incidents/active"
MY_GUILD = discord.Object(id=os.getenv("DEBUG_GUILD_ID"))
distritosConcelhosDic={"Aveiro": ["Águeda", "Albergaria-a-Velha", "Anadia", "Arouca", "Aveiro", "Castelo de Paiva", "Espinho", "Estarreja", "Ílhavo", "Mealhada", "Murtosa", "Oliveira de Azeméis", "Oliveira do Bairro", "Ovar", "Santa Maria da Feira", "São João da Madeira", "Sever do Vouga", "Vagos", "Vale de Cambra",],
"Beja": ["Aljustrel", "Almodôvar", "Alvito", "Barrancos", "Beja", "Castro Verde", "Cuba", "Ferreira do Alentejo", "Mértola", "Moura", "Odemira", "Ourique", "Serpa", "Vidigueira",],
"Bragança": ["Alfândega da Fé", "Bragança", "Carrazeda de Ansiães", "Freixo de Espada à Cinta", "Macedo de Cavaleiros", "Miranda do Douro", "Mirandela", "Mogadouro", "Torre de Moncorvo", "Vila Flor", "Vimioso", "Vinhais",],
"Castelo Branco": ["Belmonte", "Castelo Branco", "Covilhã", "Fundão", "Idanha-a-Nova", "Oleiros", "Penamacor", "Proença-a-Nova", "Sertã", "Vila de Rei", "Vila Velha de Ródão",],
"Coimbra": ["Arganil", "Cantanhede", "Coimbra", "Condeixa-a-Nova", "Figueira da Foz", "Góis", "Lousã", "Mira", "Miranda do Corvo", "Montemor-o-Velho", "Oliveira do Hospital", "Pampilhosa da Serra",],
"Évora": ["Alandroal", "Arraiolos", "Borba", "Estremoz", "Évora", "Montemor-o-Novo", "Mora", "Mourão", "Olivença", "Portel", "Redondo", "Reguengos de Monsaraz", "Vendas Novas", "Viana do Alentejo", "Vila Viçosa",],
"Faro": ["Albufeira", "Alcoutim", "Aljezur", "Castro Marim", "Faro", "Lagoa", "Lagos", "Loulé", "Monchique", "Olhão", "Portimão", "São Brás de Alportel", "Silves", "Tavira", "Vila do Bispo", "Vila Real de Santo António",],
"Guarda": ["Aguiar da Beira", "Almeida", "Celorico da Beira", "Figueira de Castelo Rodrigo", "Fornos de Algodres", "Gouveia", "Guarda", "Manteigas", "Mêda", "Pinhel", "Sabugal", "Seia", "Trancoso", "Vila Nova de Foz Côa",],
"Leiria": ["Alcobaça", "Alvaiázere", "Ansião", "Batalha", "Bombarral", "Caldas da Rainha", "Castanheira de Pera", "Figueiró dos Vinhos", "Leiria", "Marinha Grande", "Nazaré", "Óbidos", "Pedrógão Grande", "Peniche", "Pombal", "Porto de Mós",],
"Lisboa": ["Alenquer", "Amadora", "Arruda dos Vinhos", "Azambuja", "Cadaval", "Cascais", "Lisboa", "Loures", "Lourinhã", "Mafra", "Odivelas", "Oeiras", "Sintra", "Sobral de Monte Agraço", "Torres Vedras", "Vila Franca de Xira",],
"Portalegre": ["Alter do Chão", "Arronches", "Avis", "Campo Maior", "Castelo de Vide", "Crato", "Elvas", "Fronteira", "Gavião", "Marvão", "Monforte", "Nisa", "Ponte de Sor", "Portalegre", "Sousel",],
"Porto": ["Amarante", "Baião", "Felgueiras", "Gondomar", "Lousada", "Maia", "Marco de Canaveses", "Matosinhos", "Paços de Ferreira", "Paredes", "Penafiel", "Porto", "Póvoa de Varzim", "Santo Tirso", "Trofa", "Valongo", "Vila do Conde", "Vila Nova de Gaia",],
"Santarém": ["Abrantes", "Alcanena", "Almeirim", "Alpiarça", "Benavente", "Cartaxo", "Chamusca", "Constância", "Coruche", "Entroncamento", "Ferreira do Zêzere", "Golegã", "Mação", "Ourém", "Rio Maior", "Salvaterra de Magos", "Santarém", "Sardoal", "Tomar", "Torres Novas", "Vila Nova da Barquinha",],
"Setúbal": ["Alcácer do Sal", "Alcochete", "Almada", "Barreiro", "Grândola", "Moita", "Montijo", "Palmela", "Santiago do Cacém", "Seixal", "Sesimbra", "Setúbal", "Sines",],
"Viana do Castelo": ["Arcos de Valdevez", "Caminha", "Melgaço", "Monção", "Paredes de Coura", "Ponte da Barca", "Ponte de Lima", "Valença", "Viana do Castelo", "Vila Nova de Cerveira",],
"Vila Real": ["Alijó", "Boticas", "Chaves", "Mesão Frio", "Mondim de Basto", "Montalegre", "Murça", "Peso da Régua", "Ribeira de Pena", "Sabrosa", "Santa Marta de Penaguião", "Valpaços", "Vila Pouca de Aguiar", "Vila Real",],
"Viseu": ["Armamar", "Carregal do Sal", "Castro Daire", "Cinfães", "Lamego", "Mangualde", "Moimenta da Beira", "Mortágua", "Nelas", "Oliveira de Frades", "Penalva do Castelo", "Penedono", "Resende", "Santa Comba Dão", "São João da Pesqueira", "São Pedro do Sul", "Sátão", "Sernancelhe", "Tabuaço", "Tarouca", "Tondela", "Vila Nova de Paiva", "Viseu", "Vouzela",]}
distritosEscolha=[]
for distrito in distritosConcelhosDic.keys():
    distritosEscolha.append(discord.SelectOption(label=distrito,emoji="🌍"))

class MyClient(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        await self.tree.sync(guild=MY_GUILD)

intents = discord.Intents.default()
client = MyClient(intents=intents)
AlertConcelho={}
AlertChannel={}
AlertOnOff={}
ConcelhoOpcoes=" "
ConcelhoIncendios=" "
DataMsg=" "

@client.event
async def on_ready():
    print(f"\n\nLogado com o nome {client.user} [ID: {client.user.id}]\n\n")
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"incêndios!",url="https://fogos.pt"))
    vigilancia.start()

@client.tree.command()
async def opcoes(interaction: discord.Interaction):
    await interaction.response.defer()
    text_channel_dic=[]
    for channel in interaction.guild.channels:
        if str(channel.type) == 'text':
            text_channel_dic.append(discord.SelectOption(label=channel.name,emoji="#️⃣",description="id: "+str(channel.id)))
    selecao_canal=Select(options=text_channel_dic,placeholder="Clique para selecionar o canal!")
    selecao_distrito=Select(options=distritosEscolha,placeholder="Clique para selecionar o distrito!")
    async def resposta_canal(interaction):
        await interaction.response.defer(thinking=False)
        global AlertChannel
        for channel in interaction.guild.channels:
            if str(channel.type) == 'text' and channel.name==selecao_canal.values[0]:
                AlertChannel[interaction.guild.id]=channel.id
        await interaction.channel.send(f"**\nCanal atualizado com sucesso!**",delete_after=1)
    async def resposta_distrito(interaction):
        await interaction.response.defer(thinking=False)
        global ConcelhoOpcoes
        if ConcelhoOpcoes!=" ":
            await ConcelhoOpcoes.delete()
            ConcelhoOpcoes=" "
        concelhosEscolha=[]
        for distrito,concelhos in distritosConcelhosDic.items():
            if distrito==selecao_distrito.values[0]:
                for concelho in concelhos:
                    concelhosEscolha.append(discord.SelectOption(label=concelho,emoji="📍"))
        selecao_concelho=Select(options=concelhosEscolha,placeholder="Clica para selecionar o concelho!")
        view.remove_item(selecao_distrito)
        view.add_item(selecao_concelho)
        ConcelhoOpcoes= await interaction.channel.send("**\nNão serão emitidos alertas sem um concelho definido!\nSeleciona agora um concelho:**",view = view,delete_after=300)
        view.remove_item(selecao_concelho)
        async def resposta_concelho(interaction):
            await interaction.response.defer(thinking=False)
            global AlertConcelho
            AlertConcelho[interaction.guild.id]=selecao_concelho.values[0]
            await interaction.channel.send(f"**\nRegião atualizada com sucesso!**",delete_after=1)
        selecao_concelho.callback = resposta_concelho
    selecao_distrito.callback = resposta_distrito
    selecao_canal.callback = resposta_canal
    view= View()
    view.add_item(selecao_canal)
    await interaction.channel.send("**\nEscolhe o canal para emitir os alertas:**",view = view,delete_after=300)
    view.remove_item(selecao_canal)
    view.add_item(selecao_distrito)
    await interaction.channel.send("**\nEscolhe o distrito para vigiar por incêndios:**",view = view,delete_after=300)
    msg=await interaction.followup.send("**\n\t\t\t\t\t\t\t\t\t\t\t\t\t**:tools:")
    await asyncio.sleep(300)
    await msg.delete()

@client.tree.command()
async def incendios(interaction: discord.Interaction):
    await interaction.response.defer()
    selecao_distrito=Select(options=distritosEscolha,placeholder="Clique para selecionar o distrito!")
    async def resposta_distrito(interaction):
        global ConcelhoIncendios
        global DataMsg
        if DataMsg!=" ":
            await DataMsg.delete()
            DataMsg=" "
        if ConcelhoIncendios!=" ":
            await ConcelhoIncendios.delete()
            ConcelhoIncendios=" "
        await interaction.response.defer(thinking=False)
        concelhosEscolha=[]
        for distrito,concelhos in distritosConcelhosDic.items():
            if distrito==selecao_distrito.values[0]:
                for concelho in concelhos:
                    concelhosEscolha.append(discord.SelectOption(label=concelho,emoji="📍"))
        selecao_concelho=Select(options=concelhosEscolha,placeholder="Clique para selecionar o concelho!")
        view.remove_item(selecao_distrito)
        view.add_item(selecao_concelho)
        ConcelhoIncendios=await interaction.channel.send("**\nAgora escolhe um concelho:**",view = view,delete_after=300)
        view.remove_item(selecao_concelho)
        async def resposta_concelho(interaction):
            global DataMsg
            if DataMsg!=" ":
                await DataMsg.delete()
                DataMsg=" "
            await interaction.response.defer(thinking=False)
            dados=(requests.get(URL,{"concelho":selecao_concelho.values[0]})).json()
            if dados['data'] != []:
                DataMsg=await interaction.channel.send(await formatedData(dados,selecao_concelho.values[0]),delete_after=300)
            else:
                await interaction.channel.send(f"**\nNão existem incêndios ativos em {selecao_concelho.values[0]}.**",delete_after=2)
        selecao_concelho.callback = resposta_concelho
    selecao_distrito.callback = resposta_distrito
    view=View()
    dados=(requests.get(URL,)).json()
    if dados['data'] == []:
        await interaction.channel.send("**\nNão existem incêndios ativos em Portugal neste momento.**",delete_after=300)
    else:
        numIncendios=len(dados['data'])
        if numIncendios>1:
            await interaction.channel.send(f"**\nExistem {numIncendios} incêndios ativos em Portugal.**",delete_after=300)
        else:
            await interaction.channel.send("**\nExistem um incêndio ativo em Portugal.**",delete_after=300)
        view.add_item(selecao_distrito)
        await interaction.channel.send("**\nEscolhe um distrito para procurar por incêndios:**",view = view,delete_after=300)
    msg=await interaction.followup.send("**\n\t\t\t\t\t\t\t\t\t\t\t\t\t**:fire:")
    await asyncio.sleep(300)
    await msg.delete()

@tasks.loop(seconds=180)
async def vigilancia():
    print(AlertChannel)
    print(AlertConcelho)

async def formatedData(dados,local):
    final=""
    numIncendios=len(dados['data'])
    for i in range (numIncendios):
        if(numIncendios>1):
            print(final)
            if i==0:
                final+=f"**\nExistem {numIncendios} incêndios ativos na zona do concelho de {local}:\n**"
                final+=f"\n\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t:one:"
            elif i==1:
                final+=f"\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t:two:"
            elif i==2:
                final+=f"\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t:three:"
            elif i==3:
                final+=f"\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t:four:"
            elif i==4:
                final+=f"\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t:five:"
            elif i==5:
                final+=f"\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t:six:"
            elif i==6:
                final+=f"\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t:seven:"
            elif i==7:
                final+=f"\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t:eight:"
            elif i==8:
                final+=f"\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t:nine:"
            else:
                final+=f"\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t{i}"
        else:
            final+=f"**\nExiste um incêndio ativo na zona do concelho de {local}:**"
        final+=f"""\n\n```
Localização: {dados['data'][i]['freguesia']}, {dados['data'][i]['localidade']}, {dados['data'][i]['detailLocation']}
Início: {dados['data'][i]['date']} às {dados['data'][i]['hour']}h
Estado: {dados['data'][i]['status']}
Origem: {dados['data'][i]['natureza']}
Fonte do alerta: {dados['data'][i]['icnf']['fontealerta']}
Operacionais no terreno: {dados['data'][i]['man']}
Meios terrestres: {dados['data'][i]['terrain']}
Meios aéreos: {dados['data'][i]['aerial']}
```**\n**"""
    return final

client.run(TOKEN)