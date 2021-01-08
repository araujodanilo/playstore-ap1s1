import os

dataSet = "src/encoded-googleplaystore.csv"
listaApps = []

class App():
    def __init__(self):
        self.nome = ""
        self.categoria = ""
        self.avaliacao = 0.0
        self.reviews = 0
        self.tamanho = 0
        self.tamanhoTipo = ""
        self.downloads = 0
        self.tipo = ""
        self.preco = 0.0
        self.idadeMinima = ""
        self.genero = ""
        self.ultimaAtualizacao = ""
        self.versao = ""
        self.android = ""

def CarregarDataSet(dataSet, lista):
    Arquivo = open(dataSet, "r")
    Arquivo.readline()
    teste = []
    for line in Arquivo:
        linha = line.split(";")
        a = App()
        a.nome = linha[0]
        a.categoria = linha[1]
        if linha[2].isdigit():
            a.avaliacao = float(linha[2])/10
        a.reviews = int(linha[3])
        if linha[4][-1].upper() == "M":
            a.tamanhoTipo = "MB"
            a.tamanho = int(float(linha[4][:-1])) # Repeti duas vezes pois o se colocar fora dara conflito por conta das strings
        elif linha[4][-1].lower() == "k":
            a.tamanhoTipo = "KB"
            a.tamanho = int(float(linha[4][:-1]))
        else:
            a.tamanhoTipo = "KB"
            a.tamanho = 0
        a.downloads = int(linha[5].replace("+","").replace(".","").replace(",",""))
        if linha[6].lower()=="free":
            a.tipo = "gratis"
        elif linha[6].lower()=="paid":
            a.tipo = "pago"
        a.preco = float(linha[7].replace("$",""))
        if linha[8].lower() == "everyone":
            a.idadeMinima = "Livre"
        elif linha[8].lower() == "teen":
            a.idadeMinima = "+14"
        elif linha[8].lower() == "everyone 10+":
            a.idadeMinima = "+10"
        elif linha[8].lower() == "mature 17+":
            a.idadeMinima = "+17"
        elif linha[8].lower() == "adults only 18+":
            a.idadeMinima = "+18"
        else:
            a.idadeMinima = "Não classificado"
        a.genero = linha[9]
        data = CarregarDadosData(linha[10])
        a.ultimaAtualizacao = data
        a.versao = linha[11]
        a.android = linha[12].replace("\n","")
        lista.append(a)
    Arquivo.close()
    for item in teste:
        print(item)

def VerificarDia(data, mes):
    remAno = data[:-6]
    remMes = remAno[mes+1:]
    if len(remMes) == 1:
        dia = str(0)+str(remMes)
        return dia
    return remMes

def VerificarMes(data):
    if "January" == data[0:7]:
        return "01", 7
    elif "February" == data[0:8]:
        return "02", 8
    elif "March" == data[0:5]:
        return "03", 5
    elif "April" == data[0:5]:
        return "04", 5
    elif "May" == data[0:3]:
        return "05", 3
    elif "June" == data[0:4]:
        return "06", 4
    elif "July" == data[0:4]:
        return "07", 4
    elif "August" == data[0:6]:
        return "08", 6
    elif "September" == data[0:9]:
        return "09", 9
    elif "October" == data[0:7]:
        return "10", 7
    elif "November" == data[0:8]:
        return "11", 8
    elif "December" == data[0:8]:
        return "12", 8

def CarregarDadosData(data):
    ano = data[-4:]
    mes, lenNumMes = VerificarMes(data)
    dia = VerificarDia(data, lenNumMes)
    newData = str(dia)+"/"+str(mes)+"/"+str(ano)
    return newData

def ListarDados(lista):
    loop = 0
    for app in lista:
        loop += 1
        print("#"+str(loop))
        print("Nome: " + app.nome +
              "\t- Categoria: " + app.categoria +
              "\t- Avaliação: "+ str(app.avaliacao) +
              "\nReview: " + str(app.reviews) +
              "\t- Tamanho: " + str(app.tamanho) + app.tamanhoTipo +
              "\t- Downloads: " + "+" + str(app.downloads) +
              "\t- Tipo: " + (app.tipo).capitalize() +
              "\t- Preço: " + str(app.preco) +
              "\nIdade minima: " + app.idadeMinima +
              "\t- Genero: " + app.genero +
              "\t- Ultima Atualizacao: " + app.ultimaAtualizacao+
              "\nVersão: " + app.versao +
              "\t- Android: " + app.android)

def CalcularMediaCat(lista): # Calcular media categorias
    dic = {}
    for app in lista:
        if app.categoria in dic:
            media = (dic[app.categoria]+app.avaliacao)/2
            dic[app.categoria] = media
        else:
            dic[app.categoria] = app.avaliacao
    melhorAvaliacao = 0.0
    melhorCategoria = []
    for item in dic.keys():
        if melhorAvaliacao < dic[item]:
            melhorCategoria = [item]
            melhorAvaliacao = dic[item]
        elif melhorAvaliacao == dic[item]:
            melhorCategoria.append(item)
    for categoria in melhorCategoria:
        print(categoria)
    print(melhorAvaliacao)


def InformarInstallCatPago(lista):
    dic = {}
    for d in lista:
        if d.tipo.lower() == "pago":
            if d.categoria in dic:
                dic[d.categoria] = dic[d.categoria] + 1
            else:
                dic[d.categoria] = 1
    for item in dic.keys():
        soma = soma + dic[item]
        print(item +": " + str(dic[item]) + " Instalações")

def AppPagoMenosReviws(lista):
    dic = {}
    for app in lista:
        if app.tipo.lower() == "pago":
            dic[app.nome] = app.reviews
    menorReviews = 99999999999999999
    menorReviewsNome = []
    for item in dic.keys():
        if menorReviews > dic[item]:
            menorReviews = dic[item]
            menorReviewsNome = [item]
        elif menorReviews == dic[item]:
            menorReviewsNome.append(item)
    for dado in menorReviewsNome:
        print("Nome: " + dado)
    print("Com " + str(menorReviews) + " Reviews")

def ExibirAppsLancadosAno(lista):
    dic = {}
    for app in lista:
        if app.ultimaAtualizacao[-4:] in dic:
            dic[app.ultimaAtualizacao[-4:]] = dic[app.ultimaAtualizacao[-4:]] + 1
        else:
            dic[app.ultimaAtualizacao[-4:]] = 1
    for item in dic.keys():
        print("Ano: " + str(item) + "\tApps: " + str(dic[item]))

def InformarTamMedioGenero(lista):
    dic = {}
    for app in lista:
        genero = (app.genero.replace(" & ", " ")).split(" ")
        for g in genero:
            if g in dic:
                dic[g] = dic[g] + app.tamanho / 2
            else:
                dic[g] = app.tamanho
    for item in dic.keys():
        print("Gênero: " + item + "\tTamnho médio: " + str(dic[item]))


def ExibirAndroidMaisUtil(lista):
    dic = {}
    for app in lista:
        if app.android != "Varies with device":
            app.android = (app.android).replace(" and up", "")
            if app.android in dic:
                dic[app.android] = dic[app.android] + 1
            else:
                dic[app.android] = 1
    listaAndroids = []
    for numero in range(1,5):
        qtddAndroid = 0
        nomeAndroid = ""
        for item in dic.keys():
            if not item in listaAndroids:
                if dic[item] > qtddAndroid:
                    nomeAndroid = item
                    qtddAndroid = dic[item]
        listaAndroids.append(nomeAndroid)
        print("#"+ str(numero) + " - " + nomeAndroid + "\t" + str(qtddAndroid))

def ClassificarAppsENP(lista):
    appsBons = []
    appsNormais = []
    appsRuins = []
    for app in lista:
        if int(app.ultimaAtualizacao[-4:]) == 2018:
            if app.downloads > 100000 and app.avaliacao >= 4: # Maior que 1000 e 4 estrla
                appsBons.append(app.nome)
            elif app.avaliacao <= 3.5:
                appsRuins.append(app.nome)
            else:
                appsNormais.append(app.nome)
    PrintarCalcularENP(appsBons, "Exelente")
    print("")
    PrintarCalcularENP(appsNormais, "Normais")
    print("")
    PrintarCalcularENP(appsRuins, "Ruins")

def PrintarCalcularENP(l, string):
    print("Apps " + str(string) + ":")
    loop = 0
    for app in l:
        loop += 1
        print("#"+str(loop) + "\n" + app)

def CalcularTamanhoApps(lista):
    soma = 0
    qtdd = 0
    for app in lista:
        if int(app.tamanho) > 0:
            if app.tamanhoTipo == "MB":
                soma += app.tamanho*1024
            elif app.tamanhoTipo == "KB":
                soma += app.tamanho
            elif app.tamanhoTipo == "GB":
                soma = app.tamanho*10240
            qtdd += 1
    if soma != 0 != qtdd:
        print("Tamanho médio dos apps: " + str(float(soma/qtdd)/1024)[0:5] + "MB")

def ExibirMesComMaisAtua(lista):
    dic = {}
    for app in lista:
        data = int(app.ultimaAtualizacao[3:5])
        if data in dic:
            dic[data] = dic[data] + 1
        else:
            dic[data] = 1
    maiorAtu = 0
    nmrMes = 0
    for item in range(1, 12):
        if maiorAtu < dic[item]:
            maiorAtu = dic[item]
            nmrMes = item
    print("Mes: " + str(nmrMes) + "\tQuantidade: " + str(maiorAtu) + " Atualizações")

def ExbirLollipopUper(lista):
    totalDeApps = 0
    androidSuport = 0
    for app in lista:
        totalDeApps += 1
        if app.android != "NaN" and app.android != "Varies with device":
            android = (app.android[0:4].replace("W",""))
            if android[-1] == ".":
                android = android[:-1]
            if float(android) >= 5.0 or (float(android) > 5.0 and "and up" in app.android):
                androidSuport += 1
    if totalDeApps != 0 != androidSuport:
        print("Percentual de apps que funcionam com android 5.0 para cima:")
        print(str((androidSuport*100)/totalDeApps))
        print(str(androidSuport))
        print(str(totalDeApps))


def CriarMenu():
    print("1 - Carregar banco de dados"
          "\n2 - Listar todos os dados"
          "\n3 - Categoria com maior media de avaliações"
          "\n4 - Listar instalações pago da categoria"
          "\n5 - App pago com menos reviews"
          "\n6 - App atualizado/lançado por ano"
          "\n7 - Tamanho medio de apps do mesmo genero"
          "\n8 - 5 Sistemas android mais utilizados"
          "\n9 - Apps de 2018"
          "\n10 - Tamanho médio dos aplicativos"
          "\n11 - Mês com mais atualização"
          "\n12 - Apps que funcionam com android 5 ou superior"
          "\n13 - Criar outro arquivo")
    try:
        opcao = int(input("Digite a opção: "))
    except ValueError:
        print("Opção inválida")
        opcao = -1
    return opcao

CarregarDataSet(dataSet, listaApps)

opcao = -1
while opcao != 0:
    opcao = CriarMenu()
    if opcao == 1:
        if not os.path.exists(dataSet):
            print("Arquivo não existe")
        else:
            CarregarDataSet(dataSet, listaApps)
    elif opcao == 2:
        ListarDados(listaApps)
    elif opcao == 3:
        CalcularMediaCat(listaApps)
    elif opcao == 4:
        InformarInstallCatPago(listaApps)
    elif opcao == 5:
        AppPagoMenosReviws(listaApps)
    elif opcao == 6:
        ExibirAppsLancadosAno(listaApps)
    elif opcao == 7:
        InformarTamMedioGenero(listaApps)
    elif opcao == 8:
        ExibirAndroidMaisUtil(listaApps)
    elif opcao == 9:
        ClassificarAppsENP(listaApps)
    elif opcao == 10:
        CalcularTamanhoApps(listaApps)
    elif opcao == 11:
        ExibirMesComMaisAtua(listaApps)
    elif opcao == 12:
        ExbirLollipopUper(listaApps)
    elif opcao == 13:
        print("")




