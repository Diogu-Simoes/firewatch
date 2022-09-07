import discord #versão dev, instalada pelo uso do link/clone do github e não pelo pip install discord diretamente
from discord import app_commands #(à data deste commit o "pip install discord" ainda não está atualizado para a ultima versão)
from discord.ui import Button,Select,View
from discord.ext import tasks
import os
import asyncio
import requests
import MySQLdb

print("\n-------------------------------------------------------------------------------------------------------------------------------------------------")
print("\nVERSÃO 1.0.1")
print("\n-------------------------------------------------------------------------------------------------------------------------------------------------")
TOKEN = os.getenv("DISCORD_TOKEN")
MY_GUILD = discord.Object(id=os.getenv("DEBUG_GUILD_ID")) #variáveis hardcoded
DBHOST=os.getenv("DBHOST")
DBUSER=os.getenv("DBUSER")
DBPASS=os.getenv("DBPASS")
DBUSE=os.getenv("DBUSE")
MAINTENANCE=os.getenv("MAINTENANCE")
URL="https://api.fogos.pt/v2/incidents/active"
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
    print("\n-------------------------------------------------------------------------------------------------------------------------------------------------")
    print(f"\nConectei-me novamente ao Discord!")
    print("\n-------------------------------------------------------------------------------------------------------------------------------------------------")
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"incêndios!",url="https://fogos.pt"))
    print("\nCarregando dados para a memória local...")
    print("\n-------------------------------------------------------------------------------------------------------------------------------------------------")
    try:
        connection=MySQLdb.connect(
        host=DBHOST,
        user=DBUSER,
        password=DBPASS
        )
        c=connection.cursor()
        c.execute(f"USE {DBUSE}")
    except Exception as error_message:
        print(f"\nNão foi possível ligar à base dados para carregar os dados!")
        print(f"\nMensagem de erro: {error_message}")
        print(f"\nO bot não irá iniciar!")
        print("\n-------------------------------------------------------------------------------------------------------------------------------------------------")
        exit()
    try:
        for guild in client.guilds:
            server_id=guild.id
            c.execute(f"SELECT * FROM GUILDS WHERE ID = '{server_id}'")
            result=c.fetchall()
            if result==():
                pass
            else:
                for row in result:
                    AlertChannel[server_id]= client.get_channel(int(row[1]))
                    AlertDistrito[server_id]=row[2]
                    AlertConcelho[server_id]=row[3]
                    AlertLastRead[server_id]=int(row[4])
                    AlertOnOff[server_id]=int(row[5])
        connection.close()
    except Exception as error_message:
        print(f"\nNão foi possível carregar os dados da base de dados!")
        print(f"\nMensagem de erro: {error_message}")
        print(f"\nO bot não irá iniciar!")
        print("\n-------------------------------------------------------------------------------------------------------------------------------------------------")
        connection.close()
        exit()
    print("\nDados carregados com sucesso!")
    print("\n-------------------------------------------------------------------------------------------------------------------------------------------------")
    if not vigilancia.is_running():
        vigilancia.start()
    if not databaseUpdate.is_running():
        databaseUpdate.start()

@client.tree.command(description="Permite configuar o canal do discord onde envio os alertas e o concelho a vigiar!")
async def alerta(interaction):                 # comanndo /alerta
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message("\n**Não te foi atruibuido nenhum cargo com permissão de administrador por isso não podes mudar as configurações do bot!**",ephemeral=True)
        return 1
    await interaction.response.defer()
    FollowupAlerta=await interaction.followup.send("**\nALERTA**   :rotating_light:")
    global AlertOnOff
    global ConcelhoOpcoes
    ConcelhoOpcoes[interaction.guild.id]=" "
    view=BotaoOff() #botão adpativo referido no ínicio do código, adicionamos como off, se estiver em modo vigilancia será mudado à frente podemos
    text_channel_dic=[] #já adicionar à view pois é o primeiro elemento do menu, depois de o mostrarmos alteramos a variável
    for channel in interaction.guild.channels:
        if str(channel.type) == "text":
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
    if interaction.guild.id not in AlertOnOff.keys():
        AlertOnOff[interaction.guild.id]=0
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
    try:
        await FollowupAlerta.delete()
    except Exception as error_message:
        print(f"\nNão consegui apagar o menu de alerta que foi chamado na guild {client.get_guild(interaction.guild.id).name} (ID: {interaction.guild.id}).")
        print(f"\nMensagem de erro: {error_message}")
        print("\nSe este foi apagado manulamente isto é esperado.")
        print("\n-------------------------------------------------------------------------------------------------------------------------------------------------")

@tasks.loop(seconds=800)
async def vigilancia(): #loop do alerta
    print("\n\nEnviando novo alerta para todos os servidores com o alerta ligado...")
    print("\n-------------------------------------------------------------------------------------------------------------------------------------------------")
    for guild in client.guilds:
        server_id=guild.id
        if server_id not in AlertOnOff.keys():
            pass
        elif AlertOnOff[server_id]!=1: #não está ligado o alerta neste guild
            pass
        elif server_id not in AlertChannel.keys():
            pass    #mtalvez mostrar um alerta aos servidores aqui
        elif server_id not in AlertDistrito.keys():
            pass
        elif server_id not in AlertConcelho.keys():
            pass
        else:
            WebsiteButton=Button(label="Usa /incendios ou clica aqui para saber mais!",url="https://fogos.pt")
            view=View()
            view.add_item(WebsiteButton)
            global AlertLastRead
            global AlertnumIncendios
            AlertnumIncendios[server_id]=0
            dados=(requests.get(URL,{"concelho":AlertConcelho[server_id]})).json()
            for incendio in dados['data']:
                splitted=incendio["location"].split(",")
                location=splitted[0]+splitted[1]
                if (incendio["concelho"]==AlertConcelho[server_id] or location["location"]==(AlertDistrito[server_id]+", "+AlertConcelho[server_id])) and incendio["status"]!="Em Resolução" and incendio["status"]!="Vigilância" and incendio["status"]!="Conclusão":
                    AlertnumIncendios[server_id]+=1
            try:
                try:
                    last_message = await AlertChannel[server_id].fetch_message(AlertChannel[server_id].last_message_id)
                    if last_message.author.id==client.user.id:
                        await last_message.delete()
                except Exception as error_message:
                    print(f"\nNão consegui apagar o último alerta que enviei na guild {client.get_guild(server_id).name} (ID: {server_id})")
                    print(f"\nMensagem de erro: {error_message}")
                    print("\nSe alguém mandou uma mensagem no canal depois desse alerta ou foi apagado manualmente isto é esperado.")
                    print("\nIrei enviar o novo na mesma!")
                    print("\n-------------------------------------------------------------------------------------------------------------------------------------------------")
                if MAINTENANCE=="1":
                        await AlertChannel[server_id].send(f"**\nThis discord bot will be down for maintenance indefinitely while I sort out some hosting issues.\n**\n_Expect a couple of new features on my return!\n_\n**For further news and updates click on my profile picture and follow the link to GitHub in my description!**")
                else:
                    if AlertnumIncendios[server_id]>AlertLastRead[server_id] and AlertLastRead[server_id]==0 and AlertnumIncendios[server_id]==1:
                        await AlertChannel[server_id].send(f"""**\nALERTA!
                        \nSURGIU 1 INCÊNDIO ATIVO EM {AlertConcelho[server_id].upper()}   🔥
                        \n@everyone\n\n**""",view=view,delete_after=838) # numero de incêndios subiu em relação ao último check
                    elif AlertnumIncendios[server_id]>AlertLastRead[server_id] and AlertLastRead[server_id]==0 and AlertnumIncendios[server_id]>1:
                        await AlertChannel[server_id].send(f"""**\nALERTA!
                        \nSURGIRAM {AlertnumIncendios[server_id]} INCÊNDIOS EM {AlertConcelho[server_id].upper()}   🔥
                        \n@everyone\n\n**""",view=view,delete_after=838)
                    elif AlertnumIncendios[server_id]>AlertLastRead[server_id]:
                        await AlertChannel[server_id].send(f"""**\nALERTA!
                        \nAUMENTO DO NÚMERO DE INCÊNDIOS ATIVOS EM {AlertConcelho[server_id].upper()} DE {AlertLastRead[server_id]} PARA {AlertnumIncendios[server_id]}   🔥
                        \n@everyone\n\n**""",view=view,delete_after=838)
                    elif AlertnumIncendios[server_id]<AlertLastRead[server_id] and AlertnumIncendios[server_id]<=0: # numero de incêndios desceu em relação ao último check
                        await AlertChannel[server_id].send(f"""**\nNOVO DESENVOLVIMENTO!
                        \nJÁ NÃO EXISTE NENHUM INCÊNDIO OFICIALMENTE ATIVO EM {AlertConcelho[server_id].upper()}   💧
                        \n@everyone**
                        _\nNeste alerta apenas são considerados ativos os incêndios em curso._
                        \n**Para ver se algum incêndio ainda está em resolução, conclusão ou vigilância segue o botão abaixo.   :arrow_heading_down:\n\n**""",view=view,delete_after=838)
                    elif AlertnumIncendios[server_id]<AlertLastRead[server_id]:
                        await AlertChannel[server_id].send(f"""**\nNOVO DESENVOLVIMENTO!
                        \nDIMINUIÇÃO DO NÚMERO DE INCÊNDIOS ATIVOS EM {AlertConcelho[server_id].upper()} DE {AlertLastRead[server_id]} PARA {AlertnumIncendios[server_id]}   💧
                        \n@everyone**
                        _\nNeste alerta apenas são considerados ativos os incêndios em curso._
                        \n**Para ver se algum incêndio ainda está em resolução, conclusão ou vigilância segue o botão abaixo.   :arrow_heading_down:\n\n**""",view=view,delete_after=838)
                    else:
                        if AlertnumIncendios[server_id]==1:
                            await AlertChannel[server_id].send(f"""**\nZONA VIGIADA: {AlertDistrito[server_id].upper()}, {AlertConcelho[server_id].upper()}**   👀
                            \n*Deve definir as configurações de notificação deste canal apenas para menções pois será muito atualizado, provocando spam.*
                            \n**ATUALMENTE ESTÁ 1 INCÊNDIO ATIVO EM {AlertConcelho[server_id].upper()}**   🔥
                            _\nNeste alerta apenas são considerados ativos os incêndios em curso._
                            \n**Para ver se algum incêndio ainda está em resolução, conclusão ou vigilância segue o botão abaixo.   :arrow_heading_down:\n\n**""",view=view,delete_after=839)
                        elif AlertnumIncendios[server_id]>1:
                            await AlertChannel[server_id].send(f"""**\nZONA VIGIADA: {AlertDistrito[server_id].upper()}, {AlertConcelho[server_id].upper()}**   👀
                            \n*Deve definir as configurações de notificação deste canal apenas para menções pois será muito atualizado, provocando spam.*
                            \n**ATUALMENTE ESTÃO {AlertnumIncendios[server_id]} INCÊNDIOS ATIVOS EM {AlertConcelho[server_id].upper()}**   🔥
                            _\nNeste alerta apenas são considerados ativos os incêndios em curso._
                            \n**Para ver se algum incêndio ainda está em resolução, conclusão ou vigilância segue o botão abaixo.   :arrow_heading_down:\n\n**""",view=view,delete_after=839)
                        else:
                            await AlertChannel[server_id].send(f"""**\nZONA VIGIADA: {AlertDistrito[server_id].upper()}, {AlertConcelho[server_id].upper()}**   👀
                            \n*Deve definir as configurações de notificação deste canal apenas para menções pois será muito atualizado, provocando spam.*
                            \n**ATUALMENTE NÃO HÁ INCÊNDIOS ATIVOS EM {AlertConcelho[server_id].upper()}**   💧
                            _\nNeste alerta apenas são considerados ativos os incêndios em curso._
                            \n**Para ver se algum incêndio ainda está em resolução, conclusão ou vigilância segue o botão abaixo.   :arrow_heading_down:\n\n**""",view=view,delete_after=839)
                view.remove_item(WebsiteButton)
            except Exception as error_message:
                AlertOnOff[server_id]=0
                print(f"\n\nErro durante a vigilância na guild {client.get_guild(server_id).name} (ID: {server_id}")
                print(f"\nMensagem de erro: {error_message}")
                print("\nSe for sobre o canal não existir isto é esperado se o mesmo foi apagado e não se alterou no alerta.")
                print("\n-------------------------------------------------------------------------------------------------------------------------------------------------")
            AlertLastRead[server_id]=AlertnumIncendios[server_id]
    print("\nAlertas enviados com sucesso!")
    print("\n-------------------------------------------------------------------------------------------------------------------------------------------------")

@tasks.loop(seconds=1000)
async def databaseUpdate():
    print("\n\nAtualizando a base de dados...")
    print("\n-------------------------------------------------------------------------------------------------------------------------------------------------")
    try:
        connection=MySQLdb.connect(
        host=DBHOST,
        user=DBUSER,
        password=DBPASS
        )
        c=connection.cursor()
        c.execute(f"USE {DBUSE}")
    except Exception as error_message:
        print("\nNão foi possível ligar à base dados para atualizar os dados!")
        print(f"\nMensagem de erro: {error_message}")
        print("\nAs últimas alterações não serão guardadas!")
        print("\n-------------------------------------------------------------------------------------------------------------------------------------------------")

        return(-2)
    try:
        for guild in client.guilds:
            server_id=guild.id
            if server_id not in AlertOnOff.keys() or server_id not in AlertChannel.keys() or server_id not in AlertDistrito.keys() or server_id not in AlertConcelho.keys():
                pass
            else:
                if server_id not in AlertLastRead.keys():
                    AlertLastRead[server_id]=0
                c.execute(f"SELECT * from GUILDS WHERE ID = '{server_id}'")
                result=c.fetchall()
                if result==():
                    operation = f"INSERT INTO GUILDS(\
                    ID, CANAL, DISTRITO, CONCELHO, LASTREAD, STATUS) \
                    VALUES ('{server_id}', '{AlertChannel[server_id].id}', '{AlertDistrito[server_id]}', '{AlertConcelho[server_id]}', '{AlertLastRead[server_id]}', '{AlertOnOff[server_id]}' \
                    )"
                else:
                    operation=f"UPDATE GUILDS SET CANAL='{AlertChannel[server_id].id}' , DISTRITO = '{AlertDistrito[server_id]}' , CONCELHO = '{AlertConcelho[server_id]}', LASTREAD = '{AlertLastRead[server_id]}', STATUS = '{AlertOnOff[server_id]}' WHERE ID = '{server_id}'"
                c.execute(operation)
                connection.commit()
        print("\n\nBase de dados atualizada com sucesso!")
        print("\n-------------------------------------------------------------------------------------------------------------------------------------------------")
        connection.close()
    except Exception as error_message:
        print(f"\nNão foi possível atualizar os dados da guild {client.get_guild(server_id).name} (ID: {server_id}) na base de dados!")
        print(f"\nMensagem de erro: {error_message}")
        print("\nAs últimas alterações não serão guardadas!")
        print("\n-------------------------------------------------------------------------------------------------------------------------------------------------")
        connection.rollback()
        connection.close()

client.run(TOKEN)