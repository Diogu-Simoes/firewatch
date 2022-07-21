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
        if vigilancia.is_running():
            vigilancia.cancel()
            await asyncio.sleep(1)
            if vigilancia.is_running():
                await interaction.channel.send(f"**\nOcorreu um erro ao desativar o modo alerta!**",delete_after=2)
            else:
                button.label="Desligado"
                button.style=discord.ButtonStyle.danger
        else:
            vigilancia.start(interaction.guild.id)
            global AlertLastnumIncendio
            AlertLastRead[interaction.guild.id]=0
            await asyncio.sleep(1)
            if vigilancia.is_running():
                button.label="Ligado"
                button.style=discord.ButtonStyle.success
            else:
                await interaction.channel.send(f"**\nOcorreu um erro ao ativar o modo alerta!**",delete_after=2)
        await interaction.response.edit_message(view=self)

class BotaoOff(View): #caso esteja desativa mostra este, fazem exatamente o mesmo mas o estilo inicial com que aparecem é diferente
    @discord.ui.button(label="Desligado", style=discord.ButtonStyle.danger) #não consigo arranjar um work-around melhor, aceito sugestões :3
    async def button_callback(self,interaction,button):
        if vigilancia.is_running():
            vigilancia.cancel()
            await asyncio.sleep(1)
            if vigilancia.is_running():
                await interaction.channel.send(f"**\nOcorreu um erro ao desativar o modo alerta!**",delete_after=2)
            else:
                button.label="Desligado"
                button.style=discord.ButtonStyle.danger
        else:
            vigilancia.start(interaction.guild.id)
            global AlertLastnumIncendio
            AlertLastRead[interaction.guild.id]=0
            await asyncio.sleep(1)
            if vigilancia.is_running():
                button.label="Ligado"
                button.style=discord.ButtonStyle.success
            else:
                await interaction.channel.send(f"**\nOcorreu um erro ao ativar o modo alerta!**",delete_after=2)
        await interaction.response.edit_message(view=self)

intents = discord.Intents.default()
client = BOT(intents=intents)
AlertConcelho={} #estes 4 primeiros dicionários devem ser guardados de alguma forma, para manter persistência de dados entre todos os servers do bot
AlertChannel={}
AlertLastRead={}
AlertnumIncendios={}
AlertOnOff={}
AlertDistrito={}
ConcelhoOpcoes=" "
ConcelhoIncendios=" "
DataMsg=" "

@client.event
async def on_ready():
    print(f"\n\nLogado como {client.user} [ID: {client.user.id}]\n\n")
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"incêndios!",url="https://fogos.pt"))

@client.tree.command(description="Permite configuar o canal do discord onde envio os alertas e o concelho a vigiar!")
async def alerta(interaction: discord.Interaction):                 # comanndo /alerta
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message("**Não tens nenhum cargo com permissão de administrador por isso não podes mudar as configurações do bot!**",ephemeral=True)
        return 1
    global ConcelhoOpcoes
    view=BotaoOff() #botão adpativo referido no ínicio do código, adicionamos como off, se estiver em modo vigilancia será mudado à frente podemos
    await interaction.response.defer() #já adicionar à view pois é o primeiro elemento do menu, depois de o mostrarmos alteramos a variável
    text_channel_dic=[]
    count=1 # Nº do canal antes do nome para evitar exception de terem o mesmo nome
    for channel in interaction.guild.channels:
        if str(channel.type) == 'text':
            if interaction.guild.id in AlertChannel.keys():                 #cria a lista de canais para escolher, verifica
                if AlertChannel[interaction.guild.id]==channel:      #se já foi escolhido antes para mostrar esse como default
                    text_channel_dic.append(discord.SelectOption(label=str(count)+": "+channel.name,emoji="#️⃣",description="id: "+str(channel.id),default=True))
            text_channel_dic.append(discord.SelectOption(label=str(count)+": "+channel.name,emoji="#️⃣",description="id: "+str(channel.id)))
            count+=1
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
            if str(channel.type) == 'text' and channel.name==selecao_canal.values[0].split(": ")[1]:
                AlertChannel[interaction.guild.id]=channel #guarda associado ao id do server no dicionario
        await interaction.channel.send(f"**\nCanal atualizado com sucesso!**",delete_after=1)

    async def resposta_distrito(interaction): #irá eventualmente receber a resposta do dropdown do distrito
        await interaction.response.defer(thinking=False)
        global AlertDistrito
        AlertDistrito[interaction.guild.id]=selecao_distrito.values[0]
        global ConcelhoOpcoes
        if ConcelhoOpcoes!=" ":
            await ConcelhoOpcoes.delete()   #codigo para questões de estética, apaga o dropdown antigo
            ConcelhoOpcoes=" "              # do concelho para mostrar o novo se for mudado o distrito
        concelhosEscolha=[]
        for distrito,concelhos in distritosConcelhosDic.items():    #tal como nos dois anteriores, cria a lista de concelhos para escolher
            if distrito==selecao_distrito.values[0]:                # mas aqui se já houver um concelho escolhido implica que também há um distrito
                for concelho in concelhos:                       # e por isso não pode ser mostrado pela ativação da escolha do distritor, existe
                        concelhosEscolha.append(discord.SelectOption(label=concelho,emoji="📍")) #um caso mais abaixo para este exato propósito
        selecao_concelho=Select(options=concelhosEscolha,placeholder="Clica para selecionar o concelho!")
        view.add_item(selecao_concelho)
        ConcelhoOpcoes= await interaction.channel.send("**\nSeleciona agora um concelho:**",view = view,delete_after=300)
        view.remove_item(selecao_concelho)

        async def resposta_concelho(interaction):                   #irá eventualmente receber a resposta do dropdown do concelho
            await interaction.response.defer(thinking=False)
            global AlertConcelho
            AlertConcelho[interaction.guild.id]=selecao_concelho.values[0]
            await interaction.channel.send(f"**\nRegião atualizada com sucesso!**",delete_after=1)
        selecao_concelho.callback = resposta_concelho

    selecao_distrito.callback = resposta_distrito
    selecao_canal.callback = resposta_canal
    if vigilancia.is_running(): #botão adpativo referido no ínicio do código e definido no ínicio desta função
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
        ConcelhoOpcoes= await interaction.channel.send("**\nSeleciona agora um concelho:**",view = view,delete_after=300)
        view.remove_item(selecao_concelho)

    async def resposta_concelho(interaction):  #esta é resposta para o botão que aparece automatico se ja estiver escolhido um concelho
            await interaction.response.defer(thinking=False) #, não confundir com a resposta anterior do botão que é chamado pela escolha do distrito
            global AlertConcelho
            AlertConcelho[interaction.guild.id]=selecao_concelho.values[0]
            await interaction.channel.send(f"**\nRegião atualizada com sucesso!**",delete_after=1)

    if interaction.guild.id in AlertDistrito.keys():    #apenas podemos iniciar esta variável se o botão for criado
        selecao_concelho.callback = resposta_concelho   # ou seja, se já tiver sido escolhido um concelho antes
    msg=await interaction.followup.send("**⠀**")
    await msg.delete() #o defer obriga a enviar uma mensagem de followup mas esta é logo apagada

async def incendios(interaction: discord.Interaction):          # ligeiro código esparguete, não consegui arranjar melhor maneira de permitir
    await interaction.response.defer()                        #chamar a funcao do comando incendios ao clicar no "procura informacoes no bot"
    view=View()                                                     #dentro do alerta sem ser copiando a para aqui dentro como parte do /alerta
    distritosEscolha=[]
    for distrito in distritosConcelhosDic.keys():                                       #cria o dropdown de distritos
        distritosEscolha.append(discord.SelectOption(label=distrito,emoji="🌍"))
    selecao_distrito=Select(options=distritosEscolha,placeholder="Clique para selecionar o distrito!")

    async def resposta_distrito(interaction):    #irá eventualmente buscar a resposta ao dropdown do distrito
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
        for distrito,concelhos in distritosConcelhosDic.items():        #cria a lista de concelhos a partir do distrito e mostra-a
            if distrito==selecao_distrito.values[0]:
                for concelho in concelhos:
                    concelhosEscolha.append(discord.SelectOption(label=concelho,emoji="📍"))
        selecao_concelho=Select(options=concelhosEscolha,placeholder="Clique para selecionar o concelho!")
        view.remove_item(selecao_distrito)
        view.add_item(selecao_concelho)
        ConcelhoIncendios=await interaction.channel.send("**\nAgora escolhe um concelho:**",view = view,delete_after=300)
        view.remove_item(selecao_concelho)

        async def resposta_concelho(interaction): #irá eventualmente buscar a resposta ao dropdown do concelho
            global DataMsg
            if DataMsg!=" ":
                await DataMsg.delete()
                DataMsg=" "
            await interaction.response.defer(thinking=False)
            dados=(requests.get(URL,{"concelho":selecao_concelho.values[0]})).json() #pede à API os dados apenas do concelho selecionado
            if dados['data'] != []: #formata os dados e mostra os casa haja >1 incendio nesse concelho, senao mostra a mensagem
                DataMsg=await interaction.channel.send(await formatedData(dados,selecao_concelho.values[0]),delete_after=300) #
            else:
                await interaction.channel.send(f"**\nNão existem incêndios ativos em {selecao_concelho.values[0]}.**",delete_after=2)
        selecao_concelho.callback = resposta_concelho

    selecao_distrito.callback = resposta_distrito
    dados=(requests.get(URL,)).json()     #busca o numero de incêndios em portugal e mostra-os
    if dados['data'] == []:
        await interaction.channel.send("**\nNão existem incêndios ativos em Portugal neste momento.**",delete_after=300)
    else:
        numIncendios=len(dados['data']) #caso haja pelos menos 1 incêndio, mostra o dropdown dos distritos para procurar por incêndios
        if numIncendios>1:
            await interaction.channel.send(f"**\nExistem {numIncendios} incêndios ativos em Portugal.**",delete_after=300)
        else:
            await interaction.channel.send("**\nExiste um incêndio ativo em Portugal.**",delete_after=300)
        view.add_item(selecao_distrito)
        await interaction.channel.send("**\nEscolhe um distrito para procurar por incêndios:**",view = view,delete_after=300)
    msg=await interaction.followup.send("**⠀**")
    await msg.delete()

@tasks.loop(seconds=5)
async def vigilancia(server_id): #loop do alerta
    if server_id not in AlertChannel.keys():
        if server_id not in AlertConcelho.keys():
            print("\n\nCanal e concelho para os alertas ainda por definir.")
            return 0
        else:
            print("\n\nCanal para os alertas ainda por definir.")
            return 1
    if server_id not in AlertConcelho.keys():
        print("\n\nConcelho para os alertas ainda por definir.")
        return -1
    InfoButton=Button(label="Procurar mais informação no bot!",style=discord.ButtonStyle.success,emoji="🔎")
    WebsiteButton=Button(label="Saber mais em fogos.pt",url="https://fogos.pt")
    async def resposta_info(interaction):
        await incendios(interaction)
    InfoButton.callback=resposta_info
    view=View()
    view.add_item(InfoButton)
    view.add_item(WebsiteButton)
    global AlertLastRead
    global AlertnumIncendios
    dados=(requests.get(URL,{"concelho":AlertConcelho[server_id]})).json()
    AlertnumIncendios[server_id]=len(dados['data'])
    if AlertnumIncendios[server_id]>AlertLastRead[server_id] and AlertnumIncendios[server_id]==1:
        await AlertChannel[server_id].send(f"""**\n\t\t\t\t\t\t\t\t\t\t\t❗ ALERTA ❗
        \n\t\t\t\t\tSURGIU UM INCÊNDIO EM {AlertConcelho[server_id].upper()}!
        \n\t\t\t\t\t\t\t\t\t\t\t  @everyone\n\n**""",view=view,delete_after=3600)
    if AlertnumIncendios[server_id]>AlertLastRead[server_id]:     # numero de incêndios subiu em relação ao último check
        await AlertChannel[server_id].send(f"""**\n\t\t\t\t\t\t\t\t\t\t\t❗ ALERTA ❗
        \nAUMENTO DO NÚMERO DE INCÊNDIOS ATIVOS EM {AlertConcelho[server_id].upper()}
        \n\t\t\t\t\t\t\t\t\t\t\t  @everyone\n\n**""",view=view,delete_after=3600)
    elif AlertnumIncendios[server_id]<AlertLastRead[server_id]: # numero de incêndios desceu em relação ao último check
        await AlertChannel[server_id].send(f"**\n\t\t\t\t\t\t\t\t❕ NOVO DESENVOLVIMENTO ❕**",delete_after=3600)
        if AlertnumIncendios[server_id]==0:
            await AlertChannel[server_id].send(f"**\n\nJÁ NÃO EXISTE NENHUM INCÊNDIO OFICIALMENTE ATIVO!**",delete_after=3600) #delete_after=3600
        else:
            await AlertChannel[server_id].send(f"**\n\nDIMINUIÇÃO DO NÚMERO DE INCÊNDIOS ATIVOS EM {AlertConcelho[server_id].upper()})\n\n**",view=view,delete_after=3600)
    else:
        print("\n\nNão houve desenvolvimentos.")
    view.remove_item(InfoButton)
    view.remove_item(WebsiteButton)
    AlertLastRead[server_id]=AlertnumIncendios[server_id]


async def formatedData(dados,local): #recebe os dados da API e formata-os o /incendios, o param local é apenas para 2 mensagens estéticas
    final=""
    numIncendios=len(dados['data'])
    for i in range (numIncendios):
        if(numIncendios>1):
            print(final)
            if i==0:
                final+=f"**\nExistem agora {numIncendios} incêndios ativos na zona do concelho de {local}:\n**" #caso haja mais que um
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
            final+=f"**\nExiste agora um incêndio ativo na zona do concelho de {local}:**" #dados formatados:
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