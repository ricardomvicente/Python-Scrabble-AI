"""
Jogo do Scrabble_2

Autor: Ricardo Vicente

Data: 26/10/2025
"""

LETRAS = (
    "A", "B", "C", "Ç", "D", "E", "F", "G", "H", "I", "J", "L",
    "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "X", "Z"
)

NIVEL_DO_AGENTE = ("FACIL", "MEDIO", "DIFICIL")

PONTUACAO_DAS_LETRAS = {
    "A": 1, "B": 3, "C": 2, "Ç": 3, "D": 2, "E": 1, "F": 4, "G": 4, "H": 4, "I": 1, "J": 5, "L": 2,
    "M": 1, "N": 3, "O": 1, "P": 2, "Q": 6, "R": 1, "S": 1, "T": 1, "U": 1, "V": 4, "X": 8, "Z": 8
}
NUM_MAX_LINHAS = 15
NUM_MIN_LINHAS = 1
NUM_MAX_COLUNAS = 15
NUM_MIN_COLUNAS = 1

PONTOS_INICIAIS = 0

TAM_MIN_PALAVRA = 2
TAM_MAX_PALAVRA = 15

OCORRENCIAS_LETRAS = (
    14, 3, 4, 2, 5, 11, 2, 2, 2, 10, 2, 5,
    6, 4, 10, 4, 1, 6, 8, 5, 7, 2, 1, 1
)
CASA_CENTRAL = (8, 8)

NUM_MAX_JOG_LETRAS = 7

NUM_MAX_DE_JOGADORES = 4
NUM_MIN_DE_JOGADORES = 2

LET_2_INDEX = dict(zip(LETRAS, range(len(LETRAS))))



def ordena_letras(seq):
    """
    Ordena uma sequência de letras segundo a ordem definida por LET_2_INDEX.

    Argumentos:
     -> seq: sequência de letras a ordenar - (iterável de str)

    Return:
     -> Lista de letras ordenadas - (list)
    """
    return sorted(seq, key = lambda x: LET_2_INDEX[x])

def dict_para_str_ordenado(d):
    """
    Converte um dicionário de letras em cadeia de caracteres ordenada, considerando a quantidade de cada letra.

    Argumentos:
     -> d: dicionário onde cada key é uma letra a seu quantidade o value- (dict)

    Return:
     -> Cadeia de caracteres com todas as letras do dicionário, repetidas conforme a quantidade e ordenadas - (str)
    """
    lista = []
    for l in d:
        for _ in range(d[l]):
            lista.append(l)
    lista = ordena_letras(lista)
    
    s = ""
    for l in lista:
        s += l

    return s


# -----------------------------------------------------------------------------
# TAD casa
# Construtor
def cria_casa(lin, col):
    """
    Cria uma casa a partir de uma linha e coluna.
    
    Argumentos:
     -> lin: inteiro positivo, representa a linha da casa - (int)
     -> col: inteiro positivo, representa a coluna da casa - (int)

    Return:
     -> Tuplo (linha, coluna) representando a casa

    Se algum dos argumentos for inválido, gera o erro:
     -> ValueError: cria_casa: argumentos inválidos
    """
    if type(lin) != int or not NUM_MIN_LINHAS <= lin <= NUM_MAX_LINHAS or \
       type(col) != int or not NUM_MIN_COLUNAS <= col <= NUM_MAX_COLUNAS:  
        raise ValueError ("cria_casa: argumentos inválidos")
    return (lin, col)

# Seletores
def obtem_col(c):
    """
    Obtém a coluna de uma casa.

    Argumentos:
     -> c: tuplo representando a casa (linha, coluna) - (tuple)

    Return:
     -> Inteiro correspondente à coluna da casa - (int)
    """
    return c[1]

def obtem_lin(c):
    """
    Obtém a linha de uma casa.

    Argumentos:
     -> c: tuplo representando a casa (linha, coluna) - (tuple)

    Return:
     -> Inteiro correspondente à linha da casa - (int)
    """
    return c[0]

# Reconhecedor
def eh_casa(arg):
    """
    Verifica se o argumento é uma casa válida.

    Argumentos:
     -> arg: valor qualquer a verificar - (qualquer tipo)

    Return:
     -> True se o argumento for uma casa válida, False caso contrário - (bool)
    """
    if type(arg) == tuple and len(arg) == 2 and \
       type(arg[0]) == int and NUM_MIN_LINHAS <= arg[0] <= NUM_MAX_LINHAS and\
       type(arg[1]) == int and NUM_MIN_COLUNAS <= arg[1] <= NUM_MAX_COLUNAS:
        return True
    return False

# Teste
def casas_iguais(c1, c2):
    """
    Verifica se duas casas são iguais.

    Argumentos:
     -> c1: primeira casa a comparar - (qualquer tipo)
     -> c2: segunda casa a comparar - (qualquer tipo)

    Return:
     -> True se ambos os argumentos forem casas e forem iguais, False caso contrário - (bool)
    """
    if eh_casa(c1) and eh_casa(c2):
        return c1 == c2
    return False

# Transformador
def casa_para_str(c):
    """
    Converte uma casa numa cadeia de caracteres.

    Argumentos:
     -> c: tuplo representando a casa (linha, coluna) - (tuple)

    Return:
     -> String no formato "(linha,coluna)" que representa a casa - (str)
    """
    return f"({obtem_lin(c)},{obtem_col(c)})"

def str_para_casa(s):
    """
    Converte uma cadeia de caracteres numa casa.

    Argumentos:
     -> s: string no formato "(linha,coluna)" - (str)

    Return:
     -> Tuplo (linha, coluna) representando a casa - (tuple)
    """
    casa = s[1:len(s)-1].strip().split(",")
    lin = int(casa[0])
    col = int(casa[1])
    return cria_casa(lin, col)

# Funções de Alto Nível
def incrementa_casa(c, d, s):
    """
    Calcula a casa a seguir a uma dada casa numa direção e distância.

    Argumentos:
     -> c: tuplo representando a casa inicial (linha, coluna) - (tuple)
     -> d: direção, "H" para horizontal ou "V" valor para vertical - (str)
     -> s: distância positiva a avançar - (int)

    Return:
     -> Tuplo (linha, coluna) representando a nova casa, ou a casa original se não existir - (tuple)
    """
    linha = obtem_lin(c)
    coluna = obtem_col(c)

    if d == "H":
        return cria_casa(linha, coluna + s) if coluna + s <= NUM_MAX_COLUNAS else c
    else:
        return cria_casa(linha + s, coluna) if linha + s <= NUM_MAX_LINHAS else c


# TAD jogador -----------------------------------------------------------------
# Construtor
def cria_humano(nome):
    """
    Cria um jogador Humano de Scrabble.

    Argumentos:
     -> nome: cadeia de caracteres que representa o nome do jogador - (str)

    Return:
     -> Dicionário que representa o jogador Humano - (dict)

    Se o argumento for inválido, gera o erro:
     -> ValueError: cria_humano: argumento inválido
     """
    if type(nome) != str or not nome:
        raise ValueError ("cria_humano: argumento inválido")
    return {"id": nome, "bot": False,"pontos": PONTOS_INICIAIS, "letras": {}}

def cria_agente(nivel):
    """
    Cria um jogador Agente de Scrabble.

    Argumentos:
     -> nivel: cadeia de caracteresque representa o nível do agente ('FACIL', 'MEDIO' ou 'DIFICIL') - (str)

    Return:
     -> Dicionário que representa o o jogador Agente - (dict)

    Se o argumento for inválido, gera o erro:
     -> ValueError: cria_agente: argumento inválido
    """
    if nivel not in NIVEL_DO_AGENTE:
        raise ValueError ("cria_agente: argumento inválido")
    return {"id": nivel, "bot": True, "pontos": PONTOS_INICIAIS, "letras": {}}

# Seletores
def jogador_identidade(j):
    """
    Devolve a identidade do jogador.

    Argumentos:
     -> j: dicionário que representa o jogador - (dict)

    Return:
     -> Nome do jogador se for Humano, ou nível se for Agente - (str)
    """
    return j["id"]

def jogador_pontos(j):
    """
    Devolve os pontos do jogador.

    Argumentos:
     -> j: dicionário que representa o jogador - (dict)

    Return:
     -> Pontos do jogador - (int)
    """
    return j["pontos"]

def jogador_letras(j):
    """
    Devolve todas as letras do jogador, ordenadas.

    Argumentos:
     -> j: dicionário que representa o jogador - (dict)

    Return:
     -> String com todas as letras do jogador, ordenadas - (str)
    """
    return dict_para_str_ordenado(j["letras"])

# Modificadores
def recebe_letra(j, l):
    """
    Acrescenta uma letra ao jogador.

    Argumentos:
     -> j: dicionário que representa o jogador - (dict)
     -> l: letra a adicionar - (str)

    Return:
     -> Próprio jogador com a letra acrescentada - (dict)
    """
    if l not in j["letras"]:
        j["letras"][l] = 1
    else:
        j["letras"][l] += 1
    return j

def usa_letra(j, l):
    """
    Remove uma letra do jogador, se existir.

    Argumentos:
     -> j: dicionário que representa o jogador - (dict)
     -> l: letra a remover - (str)

    Return:
     -> Próprio jogador com a letra removida - (dict)
    """
    if l not in j["letras"] or j["letras"][l] < 1:
        return j
    if j["letras"][l] == 1:
        del j["letras"][l]
    else:
        j["letras"][l] -= 1
    return j

def soma_pontos(j, p):
    """
    Adiciona pontos à pontuação do jogador.

    Argumentos:
     -> j: dicionário que representa o jogador - (dict)
     -> p: pontos a somar - (int)

    Return:
     -> Próprio jogador com a pontuação atualizada - (dict)
    """
    j["pontos"] += p
    return j

# Reconhecedor
def eh_jogador(arg):
    """
    Verifica se o argumento é um jogador válido.

    Argumentos:
     -> arg: valor qualquer a verificar - (qualquer tipo)

    Return:
     -> True se o argumento for um jogador, False caso contrário - (bool)
    """
    if type(arg) == dict and len(arg) == 4 and \
       "id" in arg and type(arg["id"]) == str and \
       "bot" in arg and type(arg["bot"]) == bool and \
       "pontos" in arg and type(arg["pontos"]) == int and \
       "letras" in arg and type(arg["letras"]) == dict:
        return True
    return False

def eh_humano(arg):
    """
    Verifica se o argumento é um jogador humano.

    Argumentos:
     -> arg: valor qualquer a verificar - (qualquer tipo)

    Return:
     -> True se for um jogador humano, False caso contrário - (bool)
    """
    return eh_jogador(arg) and not arg["bot"]

def eh_agente(arg):
    """
    Verifica se o argumento é um jogador agente.

    Argumentos:
     -> arg: valor qualquer a verificar - (qualquer tipo)

    Return:
     -> True se for um jogador agente, False caso contrário - (bool)
    """
    return eh_jogador(arg) and arg["bot"]

# Teste
def jogadores_iguais(j1, j2):
    """
    Verifica se dois jogadores são iguais.

    Argumentos:
     -> j1: primeiro jogador a comparar - (qualquer tipo)
     -> j2: segundo jogador a comparar - (qualquer tipo)

    Return:
     -> True se ambos forem jogadores e forem iguais, False caso contrário - (bool)
    """
    if eh_jogador(j1) and eh_jogador(j2):
        return j1 == j2
    return False

# Transformador
def jogador_para_str(t):
    """
    Converte um jogador numa cadeia de caracteres.

    Argumentos:
     -> t: dicionário que representa o jogador - (dict)

    Return:
     -> String que representa o jogador, mostrando identidade, pontos e letras - (str)
    """
    letras = ""
    if jogador_letras(t):
        letras = " "+" ".join(jogador_letras(t))
    else:
        letras = ""

    if eh_humano(t):
        return f"{jogador_identidade(t)} ({jogador_pontos(t):3d}):{letras}"
    elif eh_agente(t):
        return f"BOT({jogador_identidade(t)}) ({jogador_pontos(t):3d}):{letras}"

# Funções de Alto Nível
def distribui_letras(jog, saco, num):
    """
    Distribui letras do saco para o jogador.
    Modifica destrutivamente a lista de letras e o jogador passados como argumento

    Argumentos:
     -> jog: dicionário representando o jogador - (dict)
     -> saco: lista de letras disponíveis - (list)
     -> num: número máximo de letras a retirar do saco - (int)

    Return:
     -> Próprio jogador com as letras acrescentadas - (dict)
    """
    for _ in range(num):
        if not saco:
            break
        recebe_letra(jog, saco[-1])
        saco.pop(-1)
    return jog


# -----------------------------------------------------------------------------

def valor_letra(letra):
    """
    Retorna o índice associado a uma letra segundo a ordem definida em LET_2_INDEX.

    Argumentos:
     -> letra: letra a avaliar - (str)

    Return:
     -> Índice correspondente à letra - (int)
    """
    return LET_2_INDEX[letra]
    
def valor_palavra(palavra):
    """
    Retorna uma lista com os índices de cada letra de uma palavra, segundo a ordem definida em LET_2_INDEX.

    Argumentos:
     -> palavra: palavra a avaliar - (str)

    Return:
     -> Lista de inteiros representando os índices das letras da palavra - (list)
    """
    return [valor_letra(c) for c in palavra]


# TAD vocabulario -------------------------------------------------------------
# Construtor
def cria_vocabulario(v):
    """
    Cria um vocabulário a partir de um tuplo de palavras.

    Argumentos:
     -> v: tuplo de palavras únicas em maiúsculas - (tuple)

    Return:
     -> Dicionário que organiza as palavras por tamanho e letra inicial - (dict)

    Se o argumento for inválido, gera o erro:
     -> ValueError: cria_vocabulario: argumento inválido
    """
    if not isinstance(v, tuple) or len(v) < 1 or len(v) != len(set(v)):
        raise ValueError ("cria_vocabulario: argumento inválido")
    
    palavras = []
    for palavra in v:
        if not isinstance(palavra, str) or not TAM_MIN_PALAVRA <= len(palavra) <= TAM_MAX_PALAVRA or not palavra.isupper():
            raise ValueError ("cria_vocabulario: argumento inválido")
        for letra in palavra:
            if letra not in LETRAS:
                raise ValueError ("cria_vocabulario: argumento inválido")

        palavras.append(palavra)

    palavras = sorted(palavras, key = len)
    dic = {i : {} for i in range(TAM_MIN_PALAVRA, TAM_MAX_PALAVRA + 1)}

    for pal in palavras:
        tam = len(pal)
        letra = pal[0]
        if letra not in dic[tam]:
            dic[tam][letra] = []
        dic[tam][letra].append(pal)

    for tam in dic:
        for letra in dic[tam]:
            dic[tam][letra] = sorted(dic[tam][letra], key = valor_palavra)

    return dic

# Seletores
def obtem_pontos(vocabulario, palavra):
    """
    Devolve os pontos de uma palavra no vocabulário.

    Argumentos:
     -> vocabulario: dicionário que representa o vocabulário - (dict)
     -> palavra: cadeia de caracteres - (str)

    Return:
     -> Pontos da palavra se existir no vocabulário, ou 0 caso contrário - (int)
    """
    if palavra[0] not in vocabulario[len(palavra)]:
        return 0
    if palavra not in vocabulario[len(palavra)][palavra[0]]:
        return 0
    
    pontos = 0
    for letra in palavra:
        if letra not in PONTUACAO_DAS_LETRAS:
            return 0
        pontos += PONTUACAO_DAS_LETRAS[letra]
    return pontos

def obtem_palavras(vocabulario, comp, letra):
    """
    Devolve todas as palavras de determinado comprimento e letra inicial, com pontuação.

    Argumentos:
     -> vocabulario: dicionário que representa o vocabulário - (dict)
     -> comp: comprimento das palavras a procurar - (int)
     -> letra: primeira letra das palavras a procurar - (str)

    Return:
     -> Tuplo de pares (palavra, pontos), ordenados por pontuação decrescente e lexicograficamente em caso de empate. Ou tuplo vazio se não existirem palavras com o comprimento e letra indicados - (tuple)
    """
    if comp not in vocabulario or letra not in vocabulario[comp]:
        return ()
    
    lista_pares = []
    for palavra in vocabulario[comp][letra]:
        lista_pares += ((palavra, obtem_pontos(vocabulario, palavra)), )

    lista_pares.sort(key=lambda x: (-x[1], valor_palavra(x[0])))

    return tuple(lista_pares)

# Teste
def testa_palavra_padrao(vocabulario, palavra, padrao, letras):
    """
    Verifica se é possível formar a palavra a partir de um padrão e letras disponíveis.

    Argumentos:
     -> vocabulario: dicionário que representa o vocabulário - (dict)
     -> palavra: palavra a testar - (str)
     -> padrao: padrão com '.' indicando espaços livres - (str)
     -> letras: cadeia de letras disponíveis para completar o padrão - (str)

    Return:
     -> True se a palavra existir no vocabulário e puder ser formada com o padrão e letras, False caso contrário - (bool)
    """
    if len(palavra) != len(padrao) or len(palavra) not in vocabulario or palavra[0] not in vocabulario[len(palavra)]:
        return False
    
    dict_letras = {}

    for l in letras:
        if l not in dict_letras:
            dict_letras[l] = 1
        else:
            dict_letras[l] += 1

    if palavra in vocabulario[len(palavra)][palavra[0]]:
        for i in range(len(palavra)):
            letra_palavra = palavra[i]
            letra_padrao = padrao[i]

            if letra_padrao == ".":
                if letra_palavra not in dict_letras or dict_letras[letra_palavra] == 0:
                    return False
                else: 
                    if dict_letras[letra_palavra] == 1:
                        del dict_letras[letra_palavra]
                    else:
                        dict_letras[letra_palavra] -= 1
            else:
                if letra_palavra != letra_padrao:
                    return False

        return True
    
    else:
        return False

# -----------------------------------------------------------------------------

def eh_palavra_valida(p):
    """
    Verifica se uma palavra é válida segundo as regras do vocabulário.

    Argumentos:
     -> p: palavra a verificar - (str)

    Return:
     -> True se a palavra for válida, False caso contrário - (bool)
    """
    if TAM_MIN_PALAVRA <= len(p) <= TAM_MAX_PALAVRA and isinstance(p, str) and p.isupper():
        for l in p:
            if l not in LETRAS:
                return False
        return True
    return False

# -----------------------------------------------------------------------------

# Transformador
def ficheiro_para_vocabulario(nome_fich):
    """
    Cria um vocabulário a partir de um ficheiro de palavras.

    Argumentos:
     -> nome_fich: caminho para o ficheiro de palavras - (str)

    Return:
     -> Vocabulário criado a partir das palavras válidas do ficheiro - (dict)
    """
    palavras = []
    with open(nome_fich, "r", encoding = "utf-8") as file:
        linhas = file.readlines()
        for palavra in linhas:
            palavra = palavra.strip().upper()
            if eh_palavra_valida(palavra):
                palavras.append(palavra)
    
    palavras = set(palavras)

    return cria_vocabulario(tuple(palavras))

def vocabulario_para_str(vocabulario):
    """
    Converte todo o vocabulário numa cadeia de caracteres.

    Argumentos:
     -> vocabulario: dicionário que representa o vocabulário - (dict)

    Return:
     -> String com todas as palavras do vocabulário (Uma palavra por linha), ordenadas por comprimento crescente, letra inicial e ordem definida pelo seletor obtem_palavras - (str)
    """
    palavras = []
    palavras_str = ""
    for tam in sorted(vocabulario.keys()):
        for let in LETRAS:
            if let in vocabulario[tam]:
                palavras.extend(obtem_palavras(vocabulario, tam, let))
    
    for i in range(len(palavras)):
        if i == len(palavras) - 1:
            palavras_str += f"{palavras[i][0]}"
        else:
            palavras_str += f"{palavras[i][0]}\n"

    return palavras_str

# Funções de Alto Nível
def procura_palavra_padrao(vocabulario, padrao, letras, min_pontos):
    """
    Procura a palavra de maior pontuação que se pode formar com um padrão e letras disponíveis.

    Argumentos:
     -> vocabulario: dicionário que representa o vocabulário - (dict)
     -> padrao: padrão com '.' indicando espaços livres - (str)
     -> letras: cadeia de letras disponíveis para completar o padrão - (str)
     -> min_pontos: pontuação mínima exigida - (int)

    Return:
     -> Tuplo (palavra, pontuação) com a palavra de maior pontuação possível, ou ('', 0) se não existir nenhuma palavra válida
    """
    melhor_palavra = ""
    melhor_pontuacao = 0
    tam = len(padrao)

    if padrao[0] != "." and padrao[0] in LETRAS:
        if tam in vocabulario and padrao[0] in vocabulario[tam]:
            for palavra in vocabulario[tam][padrao[0]]:
                if testa_palavra_padrao(vocabulario, palavra, padrao, letras):
                    pontos = obtem_pontos(vocabulario, palavra)
                    if pontos >= min_pontos and \
                       (pontos > melhor_pontuacao or (pontos == melhor_pontuacao and valor_palavra(palavra) < valor_palavra(melhor_palavra))):
                        melhor_palavra = palavra
                        melhor_pontuacao = pontos
    else:
        for iniciais in vocabulario[tam]:
            for palavra in vocabulario[tam][iniciais]:
                if testa_palavra_padrao(vocabulario, palavra, padrao, letras):
                    pontos = obtem_pontos(vocabulario, palavra)
                    if pontos >= min_pontos and \
                       (pontos > melhor_pontuacao or (pontos == melhor_pontuacao and valor_palavra(palavra) < valor_palavra(melhor_palavra))):
                        melhor_palavra = palavra
                        melhor_pontuacao = pontos

    if not melhor_palavra:
        return ("", 0)

    return (melhor_palavra, melhor_pontuacao)


# TAD Tabuleiro ---------------------------------------------------------------
# Construtor
def cria_tabuleiro():
    """
    Cria um tabuleiro de Scrabble vazio.

    Return:
     -> Lista de listas representando o tabuleiro, com '.' em todas as casas - (list)
    """
    tabuleiro = []
    for i in range(NUM_MAX_LINHAS):
        tabuleiro.append([])
        for _ in range(NUM_MAX_COLUNAS):
            tabuleiro[i].append(".")

    return tabuleiro


# -----------------------------------------------------------------------------

def ajustar_casa(casa):
    """
    Ajusta as coordenadas de uma casa para os índices do tabuleiro

    No tabuleiro, as posições são guardadas com índices de 0 a 14, mas as coordenadas fornecidas pelos jogadores vão de 1 a 15. Então, é necessário subtrair 1 a cada valor para converter as coordenadas para o formato usado internamente.
    
    Argumentos:
     ->  Recebe uma casa - (tuple)

    Return:
     ->  Tuplo com as coordenadas ajustadas ao tabuleiro
    """
    lin = obtem_lin(casa)
    col = obtem_col(casa)
    return (lin - 1, col - 1)

# -----------------------------------------------------------------------------


# Seletores
def obtem_letra(t, c):
    """
    Devolve a letra contida numa casa do tabuleiro.

    Argumentos:
     -> t: tabuleiro - (list)
     -> c: casa (linha, coluna) - (tuple)

    Return:
     -> Letra presente na casa - (str)
    """
    linha, coluna = ajustar_casa(c)

    return t[linha][coluna]

# Moificadores
def insere_letra(t, c, l):
    """
    Coloca uma letra numa casa do tabuleiro.

    Argumentos:
     -> t: tabuleiro - (list)
     -> c: casa (linha, coluna) - (tuple)
     -> l: letra a inserir - (str)

    Return:
     -> Próprio tabuleiro com a letra inserida - (list)
    """
    linha, coluna = ajustar_casa(c)
    t[linha][coluna] = l

    return t

# Reconhecedor
def eh_tabuleiro(arg):
    """
    Verifica se o argumento é um tabuleiro válido.

    Argumentos:
     -> arg: valor qualquer - (qualquer tipo)

    Return:
     -> True se for um tabuleiro, False caso contrário - (bool)
    """
    if isinstance(arg, list) and len(arg) == NUM_MAX_LINHAS:
        for linha in arg:
            if not isinstance(linha, list) or len(linha) != NUM_MAX_COLUNAS:
                return False
            for coluna in linha:
                if not isinstance(coluna, str) or len(coluna) != 1:
                    return False
        return True
    return False

def eh_tabuleiro_vazio(arg):
    """
    Verifica se o tabuleiro está vazio (sem letras).

    Argumentos:
     -> arg: valor qualquer - (qualquer tipo)

    Return:
     -> True se for um tabuleiro vazio, False caso contrário - (bool)
    """
    if eh_tabuleiro(arg):
        for l in arg:
            for c in l:
                if c != ".":
                    return False
        return True
    return False

# Teste
def tabuleiros_iguais(t1, t2):
    """
    Verifica se dois tabuleiros são iguais.

    Argumentos:
     -> t1: primeiro tabuleiro - (list)
     -> t2: segundo tabuleiro - (list)

    Return:
     -> True se ambos forem tabuleiros e iguais, False caso contrário - (bool)
    """
    if eh_tabuleiro(t1) and eh_tabuleiro(t2):
        return t1 == t2
    return False

# Transformador
def tabuleiro_para_str(t):
    """
    Converte o tabuleiro numa cadeia de caracteres para visualização.

    Argumentos:
     -> t: tabuleiro - (list)

    Return:
     -> String representando o tabuleiro com linhas, colunas e letras - (str)
    """
    tabuleiro_para_str = ""
    tabuleiro_para_str += "                       1 1 1 1 1 1\n"
    tabuleiro_para_str += "     1 2 3 4 5 6 7 8 9 0 1 2 3 4 5\n"
    tabuleiro_para_str += "   +-------------------------------+\n"

    for i in range(1, NUM_MAX_LINHAS + 1):
            tabuleiro_para_str += f"{i:2d} |"
            for e in t[i-1]:
                tabuleiro_para_str += f" {e}"
            tabuleiro_para_str += " |\n"

    tabuleiro_para_str += "   +-------------------------------+"

    return tabuleiro_para_str

# Funções de Alto Nível
def obtem_padrao(t, i, f):
    """
    Devolve a sequência de letras entre duas casas do tabuleiro, horizontal ou vertical.

    Argumentos:
     -> t: tabuleiro - (list)
     -> i: casa inicial - (tuple)
     -> f: casa final - (tuple)

    Return:
     -> String com as letras entre i e f, ou "" se inválido - (str)
    """
    if not eh_casa(i) or not eh_casa(f):
        return ""

    if obtem_lin(i) == obtem_lin(f):
        direcao = "H"
        tamanho = obtem_col(f) - obtem_col(i) + 1
    elif obtem_col(i) == obtem_col(f):
        direcao = "V"
        tamanho = obtem_lin(f) - obtem_lin(i) + 1
    else:
        return ""

    if tamanho <= 0:
        return ""
    
    cadeia_caracteres = ""
    for tam in range(tamanho):
        if direcao == "H":
            cadeia_caracteres += obtem_letra(t, incrementa_casa(i, direcao, tam))
        elif direcao == "V":
            cadeia_caracteres += obtem_letra(t, incrementa_casa(i, direcao, tam))

    return cadeia_caracteres

def insere_palavra(t, c, d, p):
    """
    Insere uma palavra no tabuleiro numa direção específica.

    Argumentos:
     -> t: tabuleiro - (list)
     -> c: casa inicial - (tuple)
     -> d: direção, 'H' ou 'V' - (str)
     -> p: palavra a inserir - (str)

    Return:
     -> Próprio tabuleiro com a palavra inserida - (list)
    """
    linha, coluna = obtem_lin(c), obtem_col(c)

    for i in range(len(p)):
        if d == "H":
            insere_letra(t, incrementa_casa(c, d, i), p[i])
        elif d == "V":
            insere_letra(t, incrementa_casa(c, d, i), p[i])
    return t

def obtem_subpadroes(t, i, f, l):
    """
    Devolve subpadrões viáveis a partir de um padrão entre duas casas, considerando um máximo de espaços livres.

    Argumentos:
     -> t: tabuleiro - (list)
     -> i: casa inicial - (tuple)
     -> f: casa final - (tuple)
     -> l: número máximo de espaços livres - (int)

    Return:
     -> Tuplo de subpadrões e tuplo de casas iniciais correspondentes - (tuple, tuple)
    """
    sub_padrao = []
    casas = []

    p = obtem_padrao(t, i, f)

    if not p:
        return (), ()

    for i_p in range(len(p)):
        for j_p in range(len(p), i_p, -1):
            cont_pontos = 0
            cont_letras = 0
            sub_padrao_valido = True
            sub = p[i_p:j_p]
            
            for c in sub:
                if c == ".":
                    cont_pontos += 1
                elif c in LETRAS:
                    cont_letras += 1

            if cont_pontos == 0 or cont_letras == 0 or cont_pontos > l:
                sub_padrao_valido = False

            if i_p > 0 and p[i_p - 1] in LETRAS:
                sub_padrao_valido = False

            if j_p < len(p) and p[j_p] in LETRAS:
                sub_padrao_valido = False

            if obtem_lin(i) == obtem_lin(f):
                d = "H"
            elif obtem_col(i) == obtem_col(f):
                d = "V"
            else:
                sub_padrao_valido = False

            if sub_padrao_valido:
                if d == "H":
                    casa = incrementa_casa(i, d, i_p)
                else:
                    casa = incrementa_casa(i, d, i_p)

                sub_padrao.append(sub)
                casas.append(casa)

    return tuple(sub_padrao), tuple(casas)

def gera_todos_padroes(t, l):
    """
    Gera todos os subpadrões viáveis do tabuleiro com até l espaços livres.

    Argumentos:
     -> t: tabuleiro - (list)
     -> l: número máximo de espaços livres - (int)

    Return:
     -> Tuplos: (subpadrões, casas iniciais, direção de cada subpadrão) - (tuple, tuple, tuple)
    """
    sub_padroes = []
    casas = []
    direcao = []

    for linha in range(1, NUM_MAX_LINHAS + 1):
        casa_inicial = cria_casa(linha, 1)
        casa_final = cria_casa(linha, NUM_MAX_COLUNAS)
        subs, cas = obtem_subpadroes(t, casa_inicial, casa_final, l)
    
        for i in range(len(subs)):
            sub_padroes.append(subs[i])
            casas.append(cas[i])
            direcao.append("H")
    
    for coluna in range(1, NUM_MAX_COLUNAS + 1):
        casa_inicial = cria_casa(1, coluna)
        casa_final = cria_casa(NUM_MAX_LINHAS, coluna)
        subs, cas = obtem_subpadroes(t, casa_inicial, casa_final, l)
    
        for i in range(len(subs)):
            sub_padroes.append(subs[i])
            casas.append(cas[i])
            direcao.append("V")

    return tuple(sub_padroes), tuple(casas), tuple(direcao)


# -----------------------------------------------------------------------------

def cria_conjunto(let, occ):
    """
    Cria um conjunto de letras a partir de dois tuplos.

    Argumentos:
     -> let : tuplo de letras únicas do alfabeto (LETRAS) - (tuple)
     -> occ : tuplo de números inteiros positivos que indicam quantas vezes cada letra aparece - (tuple)

    Return:
     -> Dicionário que representa o conjunto de letras, com letras como chave e quantidade como valor (dict)

    Se algum dos argumentos for inválido, gera o erro:
     ->  ValueError: cria_conjunto: argumentos inválidos
    """
    if not isinstance(let, tuple) or not isinstance(occ, tuple) or len(let) != len(occ):
        raise ValueError ("cria_conjunto: argumentos inválidos")
    
    conj = {}
    for i in range(len(let)):
        if let[i] not in LETRAS or occ[i] <= 0 or let[i] in conj:
            raise ValueError ("cria_conjunto: argumentos inválidos")

        conj[let[i]] = occ[i]

    return conj

def gera_numero_aleatorio(estado):
    """
    Gera um número pseudoaleatório a partir de um estado inicial.

    Argumentos:
     -> estado: número inteiro positivo que serve como estado inicial - (int)

    Return:
     -> Um número pseudoaleatório gerado - (int)
    """
    estado ^= (estado << 13) & 0xFFFFFFFF
    estado ^= (estado >> 17) & 0xFFFFFFFF
    estado ^= (estado << 5) & 0xFFFFFFFF

    return estado

def permuta_letras(letras, estado):
    """
    Permuta os elementos de uma lista de letras de forma pseudoaleatória.

    Argumentos:
     -> letras : lista de letras a ser permutada - (list)
     -> estado : inteiro positivo representando o estado inicial do gerador pseudoaleatório - (int)

    Return:
     -> A lista 'letras' é modificada destrutivamente
    """
    for i in range(len(letras)-1, 0, -1):
        estado = gera_numero_aleatorio(estado)
        j = estado % (i + 1)
        letras[i], letras[j] = letras[j], letras[i]

def baralha_conjunto(conj, estado):
    """
    Cria uma lista baralhada com todas as letras de um conjunto.

    Argumentos:
     -> conj : conjunto de letras, com letras como chave e quantidade como valor - (dict)
     -> estado : inteiro positivo que representa o estado inicial do gerador pseudoaleatório - (int)

    Return:
     -> Lista com todas as letras do conjunto baralhadas
    """
    lista_baralhada = []

    for e in LETRAS:
        if e in conj:
            repeticoes = conj[e]
            while repeticoes != 0:
                lista_baralhada.append(e)
                repeticoes -= 1
    
    permuta_letras(lista_baralhada, estado)

    return lista_baralhada

def obtem_sequencia_de_casas(casa, direcao, tamanho):
    """
    Devolve uma sequência de coordenadas de casas, a partir de uma certa casa numa respetiva direção com um certo tamanho
    
    Ao contrário da função obtem_sequencia, que devolve os valores das casas, esta função retorna a sequência de casas por si só do tipo (linha, coluna). Isto será útil para verificar certas jogadas específicas sem precisar do conteúdo das casas.

    Argumentos:
     ->  Casa, com as coordenadas do tipo (linha, coluna) - (tuple)
     ->  Direção, "H" para Horizontal ou "V" para Vertical - (str)
     ->  Numero de casas da sequência - (int)

    Return:
     ->  Tuplo com a sequência de todas as casas selecionadas do tipo (linha, coluna)
    """
    linha = obtem_lin(casa)
    coluna = obtem_col(casa)

    sequencia = ()

    for tam in range(tamanho):
        if direcao == "H":
            sequencia += ((linha, coluna + tam),)
        else:
            sequencia += ((linha + tam, coluna),)

    return sequencia

def joga_palavra(vocabulario, tab, palavra, casa, direcao, conj_letras, primeira):
    """
    Executa uma jogada no tabuleiro, validando e inserindo uma palavra segundo as regras do jogo.

    Argumentos:
     -> vocabulario : vocabulário de Scrabble utilizado para validar palavras - (dict)
     -> tab : tabuleiro do jogo, como lista de listas de caracteres - (list)
     -> palavra : palavra a ser jogada - (str)
     -> casa : casa inicial (linha, coluna) onde a palavra será colocada - (tuple)
     -> direcao : 'H' para horizontal ou 'V' para vertical - (str)
     -> conj_letras : letras disponíveis do jogador, com letras como chave e quantidade como valor - (dict)
     -> primeira : True se for a primeira jogada do jogo, False caso contrário - (bool)

    Return:
     -> Tuplo com as letras utilizadas se a jogada for válida, tuplo vazio caso contrário
    """
    let = ()
    tamanho = len(palavra)

    casa_f = incrementa_casa(casa, direcao, tamanho - 1)
    padrao = obtem_padrao(tab, casa, casa_f)

    linha, coluna = ajustar_casa(casa)

    if direcao == "H" and coluna + tamanho > NUM_MAX_COLUNAS or \
       direcao == "V" and linha + tamanho > NUM_MAX_LINHAS:
        return ()

    if primeira:
        if not testa_palavra_padrao(vocabulario, palavra, padrao, conj_letras) or \
           CASA_CENTRAL not in obtem_sequencia_de_casas(casa, direcao, tamanho):
            return ()

        insere_palavra(tab, casa, direcao, palavra)

        for letra in LETRAS:
            for i in range(len(palavra)):
               if palavra[i] == letra and palavra[i] != padrao[i]:
                    let += (letra,)

        return let
    
    else:
        if not testa_palavra_padrao(vocabulario, palavra, padrao, conj_letras):
            return ()

        sobreposicao = False

        for i in range(len(palavra)):
            if padrao[i] != ".":
                if padrao[i] != palavra[i]:
                    return ()
                else:
                    sobreposicao = True

        if not sobreposicao:
            return ()

        insere_palavra(tab, casa, direcao, palavra)

        for letra in LETRAS:
            for i in range(len(palavra)):
               if palavra[i] == letra and padrao[i] == ".":
                    let += (letra,)

        return let

# -----------------------------------------------------------------------------


# Funções Principais ----------------------------------------------------------

def baralha_saco(seed):
    """
    Baralha o saco de Scrabble utilizando um estado inicial do gerador pseudo-aleatório.

    Argumentos:
     -> seed: inteiro positivo que define o estado inicial do gerador pseudo-aleatório - (int)

    Return:
     -> Lista de letras do saco de Scrabble baralhadas - (list)
    """
    return baralha_conjunto(cria_conjunto(LETRAS, OCORRENCIAS_LETRAS), seed)


def jogada_humano(tab, jog, vocab, pilha):
    """
    Processa o turno completo de um jogador humano, permitindo passar, trocar letras ou jogar.

    Argumentos:
     -> tab: tabuleiro atual - (list)
     -> jog: jogador humano que vai jogar - (dict)
     -> vocab: vocabulário de palavras válidas - (dict)
     -> pilha: lista de letras disponíveis no saco - (list)

    Return:
     -> False se o jogador passar a jogada
     -> True se o jogador efetuar uma jogada válida (troca ou joga)
    """
    if not jogador_letras(jog) and not pilha:
        print(f"Jogada {jogador_identidade(jog)}: P")
        return False
    
    while True:
        jogada = str(input(f"Jogada {jogador_identidade(jog)}: ")).strip().split()

        if not jogada:
            continue

        elif jogada[0] == "P":
            return False

        elif jogada[0] == "T":
            if not pilha:
                continue

            seq_letras = jogada[1:]
 
            letras_validas = list(filter(lambda x: x in jogador_letras(jog), seq_letras))

            if not seq_letras or len(seq_letras) != len(letras_validas):
                continue

            for letra in seq_letras:
                usa_letra(jog, letra)
            distribui_letras(jog, pilha, len(seq_letras))
                
            return True
        
        elif jogada[0] == "J":
            if len(jogada) != 5 or (type(eval(jogada[1])) != int or type(eval(jogada[2])) != int):
                continue

            casa_i = cria_casa(int(jogada[1]), int(jogada[2]))
            direcao = jogada[3]
            palavra = jogada[4]
            if (direcao == "H" and obtem_col(casa_i) + len(palavra) - 1> NUM_MAX_COLUNAS) or \
               (direcao == "V" and obtem_lin(casa_i) + len(palavra) - 1> NUM_MAX_LINHAS):
                continue

            letras = jogador_letras(jog)
            primeira = eh_tabuleiro_vazio(tab)
            letras_usadas = joga_palavra(vocab, tab, palavra, casa_i, direcao, letras, primeira)

            if not letras_usadas:
                continue

            for letra in letras_usadas:
                if letra in jogador_letras(jog):
                    usa_letra(jog, letra)
            
            soma_pontos(jog, obtem_pontos(vocab, palavra))    
            distribui_letras(jog, pilha, len(letras_usadas))
            
            return True


def jogada_agente(tab, jog, vocab, pilha):
    """
    Processa o turno completo de um jogador agente, permitindo passar, trocar todas as letras ou jogar automaticamente.

    Argumentos:
     -> tab: tabuleiro atual - (list)
     -> jog: jogador agente que vai jogar - (dict)
     -> vocab: vocabulário de palavras válidas - (dict)
     -> pilha: lista de letras disponíveis no saco - (list)

    Return:
     -> False se o jogador passar a jogada
     -> True se o jogador efetuar uma jogada válida (troca ou joga)
    """
    pode_jogar = True
    pode_trocar = False
    pode_passar = False

    if eh_tabuleiro_vazio(tab):
        pode_jogar = False
        pode_trocar = False
        pode_passar = True

    while True:
        if pode_jogar:
            l = (len(jogador_letras(jog)))

            todos_padroes, casas, direcoes = gera_todos_padroes(tab, l)
            
            if jogador_identidade(jog) == "FACIL":
                N = 100
            elif jogador_identidade(jog) == "MEDIO":
                N = 50
            elif jogador_identidade(jog) == "DIFICIL":
                N = 10
            
            todos_padroes = todos_padroes[::N]
            casas = casas[::N]
            direcoes = direcoes[::N]

            if len(todos_padroes) == 0:
                pode_jogar = False
                pode_trocar = True
                pode_passar = False
                continue

            letras = jogador_letras(jog)
            maior = ("", 0)
            min_pontos = maior[1]

            casa = casas[0]
            direcao = direcoes[0]
            palavra = maior[0]

            for i in range(1, len(todos_padroes)):
                tuplo = procura_palavra_padrao(vocab, todos_padroes[i], letras, min_pontos)
                if tuplo[1] > min_pontos:
                    maior = tuplo
                    min_pontos = maior[1]
            
                    casa = casas[i]
                    direcao = direcoes[i]
                    palavra = maior[0]

            if maior == ("", 0):
                pode_jogar = False
                pode_trocar = True
                pode_passar = False
                continue
            
            letras_usadas = joga_palavra(vocab, tab, palavra, casa, direcao, letras, False)

            if not letras_usadas:
                pode_jogar = False
                pode_trocar = True
                pode_passar = False
                continue

            for letra in letras_usadas:
                if letra in jogador_letras(jog):
                    usa_letra(jog, letra)
            
            soma_pontos(jog, obtem_pontos(vocab, palavra))
            distribui_letras(jog, pilha, len(letras_usadas))
            
            print(f"Jogada {jogador_identidade(jog)}: J {obtem_lin(casa)} {obtem_col(casa)} {direcao} {palavra}")
            return True

        elif pode_trocar:
            if len(pilha) < NUM_MAX_JOG_LETRAS:
                pode_jogar = False
                pode_trocar = False
                pode_passar = True
                continue
            
            print(f"Jogada {jogador_identidade(jog)}: T {' '.join(jogador_letras(jog))}")
            jog["letras"] = {}
            distribui_letras(jog, pilha, NUM_MAX_JOG_LETRAS)

            return True

        elif pode_passar:
            print(f"Jogada {jogador_identidade(jog)}: P")
            return False


def scrabble2(jogadores, nome_fich, seed):
    """
    Executa um jogo completo de Scrabble2 com dois a quatro jogadores, humanos e agentes.

    Argumentos:
     -> jogadores: tuplo com nomes de jogadores humanos (cadeias não vazias) ou agentes (cadeias iniciadas por '@' seguidas do nível: 'FACIL', 'MEDIO', 'DIFICIL') - (tuple)
     -> nome_fich: nome do ficheiro que contém o vocabulário - (str)
     -> seed: inteiro positivo que define o estado inicial do gerador pseudo-aleatório - (int)

    Return:
     -> Tuplo com a pontuação final de cada jogador, na mesma ordem da lista de jogadores - (tuple)

    Se algum dos argumentos for inválido, gera o erro:
     -> ValueError: scrabble2: argumentos inválidos
    """
    if type(jogadores) != tuple or not NUM_MIN_DE_JOGADORES <= len(jogadores) <= NUM_MAX_DE_JOGADORES or type(nome_fich) != str or type(seed) != int:
        raise ValueError ("scrabble2: argumentos inválidos")

    tab = cria_tabuleiro()
    pontuacao_final = ()
    jogadas_passadas = 0
    jogadores_list = []
    saco = baralha_saco(seed)
    vocabulario = ficheiro_para_vocabulario(nome_fich)

    for id in jogadores:
        if id[0] == "@":
            nivel = id[1:]
            if nivel in NIVEL_DO_AGENTE:
                jog = cria_agente(nivel)
                distribui_letras(jog, saco, NUM_MAX_JOG_LETRAS)
            else:
                raise ValueError ("scrabble2: argumentos inválidos")
        else:
            jog = cria_humano(id)
            distribui_letras(jog, saco, NUM_MAX_JOG_LETRAS)

        jogadores_list.append(jog)

    for i in range(len(jogadores_list)):
        for l in range(i+1, len(jogadores_list)):
            if jogadores_iguais(jogadores_list[i], jogadores_list[l]):
                raise ValueError ("scrabble2: argumentos inválidos")

    print("Bem-vindo ao SCRABBLE2.")
    while True:
        if jogadas_passadas == len(jogadores):
            break

        for i in range(len(jogadores)):
            print(tabuleiro_para_str(tab))
            for jog in jogadores_list:

                print(jogador_para_str(jog))

            if eh_humano(jogadores_list[i]):
                jogada = jogada_humano(tab, jogadores_list[i], vocabulario, saco)
            else:
                jogada = jogada_agente(tab, jogadores_list[i], vocabulario, saco)

            jogadas_passadas = jogadas_passadas + 1 if not jogada else 0

            if jogadas_passadas == len(jogadores) or (not saco and not jogadores_list[i]["letras"]):
                break

    for jog in jogadores_list:
        pontuacao_final += (jogador_pontos(jog),)

    return pontuacao_final
