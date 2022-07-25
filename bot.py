import discord #versão dev, instalada pelo uso do link/clone do github e não pelo pip install discord diretamente
from discord import app_commands #(à data deste commit o "pip install discord" ainda não está atualizado para a ultima versão)
from discord.ui import Button,Select,View
from discord.ext import tasks
import os
import asyncio
import requests

TOKEN = os.getenv("DISCORD_TOKEN")
MY_GUILD = discord.Object(id=os.getenv("DEBUG_GUILD_ID")) #variáveis hardcoded
URL = "https://api.fogos.pt/v2/incidents/active"
#dicionario tipo key-distrito->value-concelhos
distritosConcelhosDic={"Aveiro": ["Águeda", "Albergaria-a-Velha", "Anadia", "Arouca", "Aveiro", "Castelo de Paiva", "Espinho", "Estarreja", "Ílhavo", "Mealhada", "Murtosa", "Oliveira de Azeméis", "Oliveira do Bairro", "Ovar", "Santa Maria da Feira", "São João da Madeira", "Sever do Vouga", "Vagos", "Vale de Cambra"],
"Beja": ["Aljustrel", "Almodôvar", "Alvito", "Barrancos", "Beja", "Castro Verde", "Cuba", "Ferreira do Alentejo", "Mértola", "Moura", "Odemira", "Ourique", "Serpa", "Vidigueira"],
"Braga":["Amares","Barcelos","Braga","Cabeceiras de Basto","Celorico de Basto","Esposende","Fafe","Guimarães","Póvoa de Lanhoso","Terras de Bouro","Vieira do Minho","Vila Nova de Famalicão","Vila Verde","Vizela"],
"Bragança": ["Alfândega da Fé", "Bragança", "Carrazeda de Ansiães", "Freixo de Espada à Cinta", "Macedo de Cavaleiros", "Miranda do Douro", "Mirandela", "Mogadouro", "Torre de Moncorvo", "Vila Flor", "Vimioso", "Vinhais"],
"Castelo Branco": ["Belmonte", "Castelo Branco", "Covilhã", "Fundão", "Idanha-a-Nova", "Oleiros", "Penamacor", "Proença-a-Nova", "Sertã", "Vila de Rei", "Vila Velha de Ródão"],
"Coimbra": ["Arganil", "Cantanhede", "Coimbra", "Condeixa-a-Nova", "Figueira da Foz", "Góis", "Lousã", "Mira", "Miranda do Corvo", "Montemor-o-Velho", "Oliveira do Hospital", "Pampilhosa da Serra","Penacova"],
"Évora": ["Alandroal", "Arraiolos", "Borba", "Estremoz", "Évora", "Montemor-o-Novo", "Mora", "Mourão", "Olivença", "Portel", "Redondo", "Reguengos de Monsaraz", "Vendas Novas", "Viana do Alentejo", "Vila Viçosa"],
"Faro": ["Albufeira", "Alcoutim", "Aljezur", "Castro Marim", "Faro", "Lagoa", "Lagos", "Loulé", "Monchique", "Olhão", "Portimão", "São Brás de Alportel", "Silves", "Tavira", "Vila do Bispo", "Vila Real de Santo António"],
"Guarda": ["Aguiar da Beira", "Almeida", "Celorico da Beira", "Figueira de Castelo Rodrigo", "Fornos de Algodres", "Gouveia", "Guarda", "Manteigas", "Mêda", "Pinhel", "Sabugal", "Seia", "Trancoso", "Vila Nova de Foz Côa"],
"Leiria": ["Alcobaça", "Alvaiázere", "Ansião", "Batalha", "Bombarral", "Caldas da Rainha", "Castanheira de Pera", "Figueiró dos Vinhos", "Leiria", "Marinha Grande", "Nazaré", "Óbidos", "Pedrógão Grande", "Peniche", "Pombal", "Porto de Mós"],
"Lisboa": ["Alenquer", "Amadora", "Arruda dos Vinhos", "Azambuja", "Cadaval", "Cascais", "Lisboa", "Loures", "Lourinhã", "Mafra", "Odivelas", "Oeiras", "Sintra", "Sobral de Monte Agraço", "Torres Vedras", "Vila Franca de Xira"],
"Portalegre": ["Alter do Chão", "Arronches", "Avis", "Campo Maior", "Castelo de Vide", "Crato", "Elvas", "Fronteira", "Gavião", "Marvão", "Monforte", "Nisa", "Ponte de Sor", "Portalegre", "Sousel"],
"Porto": ["Amarante", "Baião", "Felgueiras", "Gondomar", "Lousada", "Maia", "Marco de Canaveses", "Matosinhos", "Paços de Ferreira", "Paredes", "Penafiel", "Porto", "Póvoa de Varzim", "Santo Tirso", "Trofa", "Valongo", "Vila do Conde", "Vila Nova de Gaia"],
"Santarém": ["Abrantes", "Alcanena", "Almeirim", "Alpiarça", "Benavente", "Cartaxo", "Chamusca", "Constância", "Coruche", "Entroncamento", "Ferreira do Zêzere", "Golegã", "Mação", "Ourém", "Rio Maior", "Salvaterra de Magos", "Santarém", "Sardoal", "Tomar", "Torres Novas", "Vila Nova da Barquinha"],
"Setúbal": ["Alcácer do Sal", "Alcochete", "Almada", "Barreiro", "Grândola", "Moita", "Montijo", "Palmela", "Santiago do Cacém", "Seixal", "Sesimbra", "Setúbal", "Sines"],
"Viana do Castelo": ["Arcos de Valdevez", "Caminha", "Melgaço", "Monção", "Paredes de Coura", "Ponte da Barca", "Ponte de Lima", "Valença", "Viana do Castelo", "Vila Nova de Cerveira"],
"Vila Real": ["Alijó", "Boticas", "Chaves", "Mesão Frio", "Mondim de Basto", "Montalegre", "Murça", "Peso da Régua", "Ribeira de Pena", "Sabrosa", "Santa Marta de Penaguião", "Valpaços", "Vila Pouca de Aguiar", "Vila Real"],
"Viseu": ["Armamar", "Carregal do Sal", "Castro Daire", "Cinfães", "Lamego", "Mangualde", "Moimenta da Beira", "Mortágua", "Nelas", "Oliveira de Frades", "Penalva do Castelo", "Penedono", "Resende", "Santa Comba Dão", "São João da Pesqueira", "São Pedro do Sul", "Sátão", "Sernancelhe", "Tabuaço", "Tarouca", "Tondela", "Vila Nova de Paiva", "Viseu", "Vouzela"]}

class BOT(discord.Client): #incialização da tree dos comandos e sync dos mesmos
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        self.tree.copy_global_to(guild=MY_GUILD)
        await self.tree.sync(guild=MY_GUILD)

class BotaoOn(View): #Caso o comando /alerta seja chamado quando a vigiancia está ativa mostra este botão
    @discord.ui.button(label="Ligado", style=discord.ButtonStyle.success)
    async def button_callback(self,interaction,button):
        global AlertOnOff
        if not vigilancia.is_running():
            vigilancia.start()
        if AlertOnOff[interaction.guild.id]==1:
            button.label="Desligado"
            AlertOnOff[interaction.guild.id]=0
            button.style=discord.ButtonStyle.danger
        else:
            AlertOnOff[interaction.guild.id]=1
            global AlertLastRead
            AlertLastRead[interaction.guild.id]=0
            button.label=f"Ligado"
            button.style=discord.ButtonStyle.success
        await interaction.response.edit_message(view=self)

class BotaoOff(View): #caso esteja desativa mostra este, fazem exatamente o mesmo mas o estilo inicial com que aparecem é diferente
    @discord.ui.button(label="Desligado", style=discord.ButtonStyle.danger) #não consigo arranjar um work-around melhor, aceito sugestões :3
    async def button_callback(self,interaction,button):
        global AlertOnOff
        if not vigilancia.is_running():
            vigilancia.start()
        if AlertOnOff[interaction.guild.id]==1:
            AlertOnOff[interaction.guild.id]=0
            button.label="Desligado"
            button.style=discord.ButtonStyle.danger
        else:
            global AlertLastRead
            AlertOnOff[interaction.guild.id]=1
            AlertLastRead[interaction.guild.id]=0
            button.label=f"Ligado"
            button.style=discord.ButtonStyle.success
        await interaction.response.edit_message(view=self)

intents = discord.Intents.default()
client = BOT(intents=intents)
AlertConcelho={} #estes 4 primeiros dicionários devem ser guardados de alguma forma, para manter persistência de dados entre todos os servers do bot
AlertChannel={}
AlertOnOff={}
AlertDistrito={}
AlertLastRead={}
AlertnumIncendios={}
ConcelhoOpcoes={}
ConcelhoIncendios={}
DataMsg={}

@client.event
async def on_ready():
    print(f"\n\nLOGIN: {client.user} [ID: {client.user.id}]\n\n")
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"incêndios!",url="https://fogos.pt"))

@client.tree.command(description="Permite configuar o canal do discord onde envio os alertas e o concelho a vigiar!")
async def alerta(interaction):                 # comanndo /alerta
    await interaction.response.defer()
    if not interaction.user.guild_permissions.administrator:
        await interaction.followup.send("\n**Não te foi atruibuido nenhum cargo com permissão de administrador por isso não podes mudar as configurações do bot!**",ephemeral=True)
        return 1
    FollowupAlerta=await interaction.followup.send("**\n**:tools:")
    global AlertOnOff
    global ConcelhoOpcoes
    if interaction.guild.id not in AlertOnOff.keys():
        AlertOnOff[interaction.guild.id]=0
    ConcelhoOpcoes[interaction.guild.id]=" "
    view=BotaoOff() #botão adpativo referido no ínicio do código, adicionamos como off, se estiver em modo vigilancia será mudado à frente podemos
    text_channel_dic=[] #já adicionar à view pois é o primeiro elemento do menu, depois de o mostrarmos alteramos a variável
    for channel in interaction.guild.channels:
        if str(channel.type) == 'text':
            if interaction.guild.id in AlertChannel.keys():                 #cria a lista de canais para escolher, verifica
                if AlertChannel[interaction.guild.id]==channel:      #se já foi escolhido antes para mostrar esse como default
                    text_channel_dic.append(discord.SelectOption(label=str(channel.position)+" - "+channel.name,emoji="#️⃣",description="id: "+str(channel.id),default=True))
                else:
                    text_channel_dic.append(discord.SelectOption(label=str(channel.position)+" - "+channel.name,emoji="#️⃣",description="id: "+str(channel.id)))
            else:
                text_channel_dic.append(discord.SelectOption(label=str(channel.position)+" - "+channel.name,emoji="#️⃣",description="id: "+str(channel.id)))
    selecao_canal=Select(options=text_channel_dic,placeholder="Clique para selecionar o canal!")
    distritosEscolha=[]
    for distrito in distritosConcelhosDic.keys():
        if interaction.guild.id in AlertDistrito.keys():
            if AlertDistrito[interaction.guild.id]==distrito:
                distritosEscolha.append(discord.SelectOption(label=distrito,emoji="🌍",default=True))   #o mesmo para os distritos
            else:
                distritosEscolha.append(discord.SelectOption(label=distrito,emoji="🌍"))
        else:
            distritosEscolha.append(discord.SelectOption(label=distrito,emoji="🌍"))
    selecao_distrito=Select(options=distritosEscolha,placeholder="Clique para selecionar o distrito!")

    async def resposta_canal(interaction): #irá eventualmente receber a resposta do dropdown do canal
        await interaction.response.defer(thinking=False)
        global AlertChannel
        for channel in interaction.guild.channels:
            if str(channel.type) == 'text' and channel.name==selecao_canal.values[0].split(" - ")[1]:
                AlertChannel[interaction.guild.id]=channel #guarda associado ao id do server no dicionario
        await interaction.channel.send(f"**\nCanal atualizado com sucesso!**",delete_after=1)

    async def resposta_distrito(interaction): #irá eventualmente receber a resposta do dropdown do distrito
        await interaction.response.defer(thinking=False)
        global AlertDistrito
        AlertDistrito[interaction.guild.id]=selecao_distrito.values[0]
        global ConcelhoOpcoes
        if ConcelhoOpcoes[interaction.guild.id]!=" ":
            await ConcelhoOpcoes[interaction.guild.id].delete()   #codigo para questões de estética, apaga o dropdown antigo
            ConcelhoOpcoes[interaction.guild.id]=" "              # do concelho para mostrar o novo se for mudado o distrito
        concelhosEscolha=[]
        for distrito,concelhos in distritosConcelhosDic.items():    #tal como nos dois anteriores, cria a lista de concelhos para escolher
            if distrito==selecao_distrito.values[0]:                # mas aqui se já houver um concelho escolhido implica que também há um distrito
                for concelho in concelhos:                       # e por isso não pode ser mostrado pela ativação da escolha do distritor, existe
                        concelhosEscolha.append(discord.SelectOption(label=concelho,emoji="📍")) #um caso mais abaixo para este exato propósito
        selecao_concelho=Select(options=concelhosEscolha,placeholder="Clica para selecionar o concelho!")
        view.add_item(selecao_concelho)
        ConcelhoOpcoes[interaction.guild.id]= await interaction.channel.send("**\nSeleciona agora um concelho:**",view = view,delete_after=300)
        view.remove_item(selecao_concelho)

        async def resposta_concelho(interaction):                   #irá eventualmente receber a resposta do dropdown do concelho
            await interaction.response.defer(thinking=False)
            global AlertConcelho
            global AlertLastRead
            AlertLastRead[interaction.guild.id]=0
            AlertConcelho[interaction.guild.id]=selecao_concelho.values[0]
            await interaction.channel.send(f"**\nRegião atualizada com sucesso!**",delete_after=1)
        selecao_concelho.callback = resposta_concelho

    selecao_distrito.callback = resposta_distrito
    selecao_canal.callback = resposta_canal
    if AlertOnOff[interaction.guild.id]==1: #botão adpativo referido no ínicio do código e definido no ínicio desta função
        view=BotaoOn()
    await interaction.channel.send("**\nClique para mudar o estado:**",view = view,delete_after=300) #mostra o botão do estado
    view=View()
    view.add_item(selecao_canal)
    await interaction.channel.send("**\nEscolhe o canal para emitir os alertas:**",view = view,delete_after=300) #mostra o dropdown do canal
    view.remove_item(selecao_canal)
    view.add_item(selecao_distrito)
    await interaction.channel.send("**\nEscolhe o distrito para vigiar por incêndios:**",view = view,delete_after=300) #mostra o dropdown do distrito
    view.remove_item(selecao_distrito)
    if interaction.guild.id in AlertDistrito.keys(): # o caso referido antes, se já tiver escolhido um concelho salta logo a escolha do distrito
        concelhosEscolha=[]                           # e mostra a lista de concelhos com o concelho escolhido sem ser preciso mexer nos distritos
        for distrito,concelhos in distritosConcelhosDic.items():
            if distrito==AlertDistrito[interaction.guild.id]:
                for concelho in concelhos:
                    if interaction.guild.id in AlertConcelho.keys():
                        if AlertConcelho[interaction.guild.id]==concelho:
                            concelhosEscolha.append(discord.SelectOption(label=concelho,emoji="📍",default=True))
                        else:
                            concelhosEscolha.append(discord.SelectOption(label=concelho,emoji="📍"))
                    else:
                        concelhosEscolha.append(discord.SelectOption(label=concelho,emoji="📍"))
        selecao_concelho=Select(options=concelhosEscolha,placeholder="Clica para selecionar o concelho!")
        view.add_item(selecao_concelho) #mostra o dropdown dos concelhos com o escolhido anteriormente lá como default
        ConcelhoOpcoes[interaction.guild.id]= await interaction.channel.send("**\nSeleciona agora um concelho:**",view = view,delete_after=300)
        view.remove_item(selecao_concelho)

    async def resposta_concelho(interaction):  #esta é resposta para o botão que aparece automatico se ja estiver escolhido um concelho
            await interaction.response.defer(thinking=False) #, não confundir com a resposta anterior do botão que é chamado pela escolha do distrito
            global AlertConcelho
            global AlertLastRead
            AlertLastRead[interaction.guild.id]=0
            AlertConcelho[interaction.guild.id]=selecao_concelho.values[0]
            await interaction.channel.send(f"**\nRegião atualizada com sucesso!**",delete_after=1)

    if interaction.guild.id in AlertDistrito.keys():    #apenas podemos iniciar esta variável se o botão for criado
        selecao_concelho.callback = resposta_concelho   # ou seja, se já tiver sido escolhido um concelho antes
    await asyncio.sleep(298)
    await FollowupAlerta.delete()

@client.tree.command(description="Mostra todos os incêndios a nível nacional e permite pesquisar por região!")
async def incendios(interaction):
    await interaction.response.defer()
    FollowupIncendio=await interaction.followup.send("**\n**:fire:")
    global DataMsg
    global ConcelhoIncendios
    DataMsg[interaction.guild.id]=" "
    ConcelhoIncendios[interaction.guild.id]=" "                            #ligeiro código esparguete, não consegui arranjar melhor maneira de permitir
    view=View()                                                 #chamar a funcao do comando incendios ao clicar no "procura informacoes no bot"
    distritosEscolha=[]#                                         dentro do alerta sem ser copiando a para aqui dentro como parte do /alerta
    for distrito in distritosConcelhosDic.keys():
        distritosEscolha.append(discord.SelectOption(label=distrito,emoji="🌍"))            #cria o dropdown de distritos
    selecao_distrito=Select(options=distritosEscolha,placeholder="Clique para selecionar o distrito!")

    async def resposta_distrito(interaction):    #irá eventualmente buscar a resposta ao dropdown do distrito
        global ConcelhoIncendios
        global DataMsg
        if DataMsg[interaction.guild.id]!=" ":
            await DataMsg[interaction.guild.id].delete()
            DataMsg[interaction.guild.id]=" "
        if ConcelhoIncendios[interaction.guild.id]!=" ":
            await ConcelhoIncendios[interaction.guild.id].delete()
            ConcelhoIncendios[interaction.guild.id]=" "
        await interaction.response.defer(thinking=False)
        concelhosEscolha=[]
        for distrito,concelhos in distritosConcelhosDic.items():        #cria a lista de concelhos a partir do distrito e mostra-a
            if distrito==selecao_distrito.values[0]:
                for concelho in concelhos:
                    concelhosEscolha.append(discord.SelectOption(label=concelho,emoji="📍"))
        selecao_concelho=Select(options=concelhosEscolha,placeholder="Clique para selecionar o concelho!")
        view.remove_item(selecao_distrito)
        view.add_item(selecao_concelho)
        ConcelhoIncendios[interaction.guild.id]=await interaction.channel.send("**\nAgora escolhe um concelho:**",view = view,delete_after=300)
        view.remove_item(selecao_concelho)

        async def resposta_concelho(interaction): #irá eventualmente buscar a resposta ao dropdown do concelho
            global DataMsg
            if DataMsg[interaction.guild.id]!=" ":
                await DataMsg[interaction.guild.id].delete()
                DataMsg[interaction.guild.id]=" "
            await interaction.response.defer(thinking=False)
            dados=(requests.get(URL,{"concelho":selecao_concelho.values[0]})).json() #pede à API os dados apenas do concelho selecionado
            if dados['data'] != []: #formata os dados e mostra os casa haja >1 incendio nesse concelho, senao mostra a mensagem
                DataMsg[interaction.guild.id]=await interaction.channel.send(await formatedData(dados,selecao_concelho.values[0]),delete_after=300) #
            else:
                await interaction.channel.send(f"**\nNão existem incêndios em {selecao_concelho.values[0]}.**",delete_after=2)
        selecao_concelho.callback = resposta_concelho

    selecao_distrito.callback = resposta_distrito
    dados=(requests.get(URL)).json()     #busca o numero de incêndios em portugal e mostra-os
    if dados['data'] == []:
        await interaction.channel.send("**\nNão existem incêndios em Portugal neste momento.**",delete_after=300)
    else:
        numIncendios=len(dados['data']) #caso haja pelos menos 1 incêndio, mostra o dropdown dos distritos para procurar por incêndios
        if numIncendios>1:
            await interaction.channel.send(f"**\nExistem {numIncendios} incêndios em Portugal.**",delete_after=300)
        else:
            await interaction.channel.send("**\nExiste um incêndio em Portugal.**",delete_after=300)
        view.add_item(selecao_distrito)
        await interaction.channel.send("**\nEscolhe um distrito para procurar por incêndios:**",view = view,delete_after=300)
    await asyncio.sleep(298)
    await FollowupIncendio.delete()

@tasks.loop(seconds=840)
async def vigilancia(): #loop do alerta
    for guild in client.guilds:
        server_id=guild.id
        if server_id not in AlertOnOff.keys():
            AlertOnOff[server_id]=0
        if AlertOnOff[server_id]!=1: #não está ligado o alerta neste guild
            return -2
        if server_id not in AlertChannel.keys():
            if server_id not in AlertConcelho.keys():
                return 0
            else:
                return 1
        if server_id not in AlertConcelho.keys():
            return -1
        InfoButton=Button(label="Procurar mais informação no bot!",style=discord.ButtonStyle.success,emoji="🔎")
        WebsiteButton=Button(label="Saber mais em fogos.pt",url="https://fogos.pt")
        async def resposta_info(interaction):
            await interaction.response.defer(thinking=False)
            global DataMsg
            global ConcelhoIncendios
            DataMsg[interaction.guild.id]=" "
            ConcelhoIncendios[interaction.guild.id]=" "     #ligeiro código esparguete, não consegui arranjar melhor maneira de permitir
            view=View()                                    #chamar a funcao do comando incendios ao clicar no "procura informacoes no bot"
            distritosEscolha=[]                                  #dentro do alerta sem ser copiando a para aqui dentro como parte do /alerta
            for distrito in distritosConcelhosDic.keys():               #sendo assim, até à linha "InfoButton.callback=resposta_info"
                distritosEscolha.append(discord.SelectOption(label=distrito,emoji="🌍"))    #toda a informação pode ser consultado acima
            selecao_distrito=Select(options=distritosEscolha,placeholder="Clique para selecionar o distrito!") # nos comentarios da mesma função

            async def resposta_distrito(interaction):
                await interaction.response.defer(thinking=False)
                global ConcelhoIncendios
                global DataMsg
                if DataMsg[interaction.guild.id]!=" ":
                    await DataMsg[interaction.guild.id].delete()
                    DataMsg[interaction.guild.id]=" "
                if ConcelhoIncendios[interaction.guild.id]!=" ":
                    await ConcelhoIncendios[interaction.guild.id].delete()
                    ConcelhoIncendios[interaction.guild.id]=" "
                concelhosEscolha=[]
                for distrito,concelhos in distritosConcelhosDic.items():
                    if distrito==selecao_distrito.values[0]:
                        for concelho in concelhos:
                            concelhosEscolha.append(discord.SelectOption(label=concelho,emoji="📍"))
                selecao_concelho=Select(options=concelhosEscolha,placeholder="Clique para selecionar o concelho!")
                view.remove_item(selecao_distrito)
                view.add_item(selecao_concelho)
                ConcelhoIncendios[interaction.guild.id]=await interaction.channel.send("**\nAgora escolhe um concelho:**",view = view,delete_after=300)
                view.remove_item(selecao_concelho)

                async def resposta_concelho(interaction):
                    global DataMsg
                    if DataMsg[interaction.guild.id]!=" ":
                        await DataMsg[interaction.guild.id].delete()
                        DataMsg[interaction.guild.id]=" "
                    await interaction.response.defer(thinking=False)
                    dados=(requests.get(URL,{"concelho":selecao_concelho.values[0]})).json()
                    if dados['data'] != []:
                        DataMsg[interaction.guild.id]=await interaction.channel.send(await formatedData(dados,selecao_concelho.values[0]),delete_after=300) #
                    else:
                        await interaction.channel.send(f"**\nNão existem incêndios em {selecao_concelho.values[0]}.**",delete_after=2)
                selecao_concelho.callback = resposta_concelho

            selecao_distrito.callback = resposta_distrito
            dados=(requests.get(URL)).json()
            if dados['data'] == []:
                await interaction.channel.send("**\nNão existem incêndios em Portugal neste momento.**",delete_after=300)
            else:
                numIncendios=len(dados['data'])
                if numIncendios>1:
                    await interaction.channel.send(f"**\nExistem {numIncendios} incêndios em Portugal.**",delete_after=300)
                else:
                    await interaction.channel.send("**\nExiste um incêndio em Portugal.**",delete_after=300)
                view.add_item(selecao_distrito)
                await interaction.channel.send("**\nEscolhe um distrito para procurar por incêndios:**",view = view,delete_after=300)
        InfoButton.callback=resposta_info
        view=View()
        view.add_item(InfoButton)
        view.add_item(WebsiteButton)
        global AlertLastRead
        global AlertnumIncendios
        AlertnumIncendios[server_id]=0
        dados=(requests.get(URL,{"concelho":AlertConcelho[server_id]})).json()
        for incendio in dados['data']:
            if incendio["concelho"]==AlertConcelho[server_id] and (incendio["status"]=="Despacho" or incendio["status"]=="Início" or incendio["status"]=="Em Curso" or incendio["status"]=="Despacho de 1º Alerta" or incendio["status"]=="Chegada ao TO"):
                AlertnumIncendios[server_id]+=1
        try:
            if AlertnumIncendios[server_id]>AlertLastRead[server_id] and AlertLastRead[server_id]==0 and AlertnumIncendios[server_id]==1:
                await AlertChannel[server_id].send(f"""**\n❗ ALERTA ❗
                \nSURGIU 1 INCÊNDIO EM {AlertConcelho[server_id].upper()}
                \n@everyone\n\n**""",view=view,delete_after=838) # numero de incêndios subiu em relação ao último check
            elif AlertnumIncendios[server_id]>AlertLastRead[server_id] and AlertLastRead[server_id]==0 and AlertnumIncendios[server_id]>1:
                await AlertChannel[server_id].send(f"""**\n❗ ALERTA ❗
                \nSURGIRAM {AlertnumIncendios[server_id]} INCÊNDIOS EM {AlertConcelho[server_id].upper()}
                \n@everyone\n\n**""",view=view,delete_after=838)
            elif AlertnumIncendios[server_id]>AlertLastRead[server_id]:
                await AlertChannel[server_id].send(f"""**\n❗ ALERTA ❗
                \nAUMENTO DO NÚMERO DE INCÊNDIOS ATIVOS EM {AlertConcelho[server_id].upper()} DE {AlertLastRead[server_id]} PARA {AlertnumIncendios[server_id]}
                \n@everyone\n\n**""",view=view,delete_after=838)
            elif AlertnumIncendios[server_id]<AlertLastRead[server_id] and AlertnumIncendios[server_id]<=0: # numero de incêndios desceu em relação ao último check
                await AlertChannel[server_id].send(f"""**\n❕ NOVO DESENVOLVIMENTO ❕
                \nJÁ NÃO EXISTE NENHUM INCÊNDIO OFICIALMENTE ATIVO EM {AlertConcelho[server_id].upper()}
                \n@everyone**
                _\nNeste alerta apenas são considerados ativos os incêndios em curso.
                \nPara ver se o incêndio ainda está em resolução, conclusão ou vigilância use um dos botões abaixo.\n\n_""",delete_after=838)
            elif AlertnumIncendios[server_id]<AlertLastRead[server_id]:
                await AlertChannel[server_id].send(f"""**\n❕ NOVO DESENVOLVIMENTO ❕
                \nDIMINUIÇÃO DO NÚMERO DE INCÊNDIOS ATIVOS EM {AlertConcelho[server_id].upper()} DE {AlertLastRead[server_id]} PARA {AlertnumIncendios[server_id]}
                \n@everyone**
                _\nNeste alerta apenas são considerados ativos os incêndios em curso.
                \nPara ver se o incêndio ainda está em resolução, conclusão ou vigilância use um dos botões abaixo.\n\n_""",delete_after=838)
            else:
                if AlertnumIncendios[server_id]==1:
                    await AlertChannel[server_id].send(f"""**\n{AlertDistrito[server_id].upper()}, {AlertConcelho[server_id].upper()}**   :eyes:
                    \n*É recomendado que os utilizadores definam as configurações de notificação deste canal apenas para menções*   :inbox_tray:
                    \n**ATUALMENTE ESTÁ 1 INCÊNDIO ATIVO EM {AlertConcelho[server_id].upper()} :fire:**""",delete_after=839)
                elif AlertnumIncendios[server_id]>1:
                    await AlertChannel[server_id].send(f"""**\n{AlertDistrito[server_id].upper()}, {AlertConcelho[server_id].upper()}**   :eyes:
                    \n*É recomendado que os utilizadores definam as configurações de notificação deste canal apenas para menções*   :inbox_tray:
                    \n**ATUALMENTE ESTÃO {AlertnumIncendios[server_id]} INCÊNDIOS ATIVOS EM {AlertConcelho[server_id].upper()} :fire:**""",delete_after=839)
                else:
                    await AlertChannel[server_id].send(f"""**\n{AlertDistrito[server_id].upper()}, {AlertConcelho[server_id].upper()}**   :eyes:
                    \n*É recomendado que os utilizadores definam as configurações de notificação deste canal apenas para menções*   :inbox_tray:
                    \n**ATUALMENTE NÃO HÁ INCÊNDIOS ATIVOS EM {AlertConcelho[server_id].upper()}   :fire:**""",delete_after=839)
            view.remove_item(InfoButton)
            view.remove_item(WebsiteButton)
        except:
            AlertOnOff[server_id]=0
            return 2
        AlertLastRead[server_id]=AlertnumIncendios[server_id]

async def formatedData(dados,local): #recebe os dados da API e formata-os o /incendios, o param local é apenas para 2 mensagens estéticas
    final=""
    numIncendios=len(dados['data'])
    for i in range (numIncendios):
        if(numIncendios>1):
            if i==0:
                final+=f"**\nExistem {numIncendios} incêndios no concelho de {local}:\n**" #caso haja mais que um
                final+=f"\n\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t:one:" #mostra a emoji corresponde ao número incêndio
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
        else: #se apaenas existir um incêndio não mostra emoji e a mensage muda
            final+=f"**\nExiste um incêndio na zona no concelho de {local}:**" #dados formatados:
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
    return final #devolva os dados de todos os incêndios agrupados numa string com parágrafos

client.run(TOKEN)