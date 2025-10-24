# FP 2025/2026 - Projeto 2
# Scrabble com TADs e IA
# Versão com comentários para estudo

# ==================== CONSTANTES ====================

# Alfabeto português na ordem canónica (com Ç entre C e D)
letras = ('A', 'B', 'C', 'Ç', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'L', 'M', 'N', 'O',
          'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'X', 'Z')
letras_set = set(letras)  # Para verificar rapidamente se uma letra é válida

# Constantes do gerador xorshift (para números aleatórios)
bits = 0xFFFFFFFF
shift_1 = 13
shift_2 = 17
shift_3 = 5

# Configurações do tabuleiro
tamanho_tabuleiro = 15
coordenada_minima = 1
coordenada_maxima = 15
casa_vazia = '.'
CASA_CENTRAL = (8, 8)  # Centro do tabuleiro
TAMANHO_MAO = 7  # Número máximo de letras por jogador

# Quantas vezes cada letra aparece no saco
ocorrencias_saco = {
    'A': 14, 'B': 3, 'C': 4, 'Ç': 2, 'D': 5, 'E': 11, 'F': 2,
    'G': 2, 'H': 2, 'I': 10, 'J': 2, 'L': 5, 'M': 6, 'N': 4,
    'O': 10, 'P': 4, 'Q': 1, 'R': 6, 'S': 8, 'T': 5,
    'U': 7, 'V': 2, 'X': 1, 'Z': 1
}

# Pontos que cada letra vale
pontuacao_letras = {
    'A': 1, 'B': 3, 'C': 2, 'Ç': 3, 'D': 2, 'E': 1, 'F': 4,
    'G': 4, 'H': 4, 'I': 1, 'J': 5, 'L': 2, 'M': 1, 'N': 3,
    'O': 1, 'P': 2, 'Q': 6, 'R': 1, 'S': 1, 'T': 1,
    'U': 1, 'V': 4, 'X': 8, 'Z': 8
}


# ==================== GERADOR PSEUDO-ALEATÓRIO ====================

def gera_numero_aleatorio(estado: int) -> int:
    """
    Gera um número pseudo-aleatório usando o algoritmo Xorshift.
    Recebe o estado atual e devolve o próximo número.
    """
    # Aplica as operações do Xorshift
    estado &= bits
    estado = (estado ^ (estado << shift_1)) & bits
    estado = (estado ^ (estado >> shift_2)) & bits
    estado = (estado ^ (estado << shift_3)) & bits
    return estado


# ==================== TAD casa ====================

def cria_casa(lin: int, col: int) -> tuple:
    """
    Cria uma casa do tabuleiro com linha e coluna.
    As coordenadas têm que estar entre 1 e 15.
    """
    # Verifica se os argumentos são válidos
    if not (isinstance(lin, int) and isinstance(col, int) and 
            coordenada_minima <= lin <= coordenada_maxima and 
            coordenada_minima <= col <= coordenada_maxima):
        raise ValueError('cria_casa: argumentos inválidos')
    
    # Uma casa é simplesmente um tuplo (linha, coluna)
    return (lin, col)


def obtem_lin(c: tuple) -> int:
    """Devolve a linha da casa."""
    return c[0]


def obtem_col(c: tuple) -> int:
    """Devolve a coluna da casa."""
    return c[1]


def eh_casa(arg) -> bool:
    """
    Verifica se o argumento é uma casa válida.
    Uma casa tem que ser um tuplo com 2 inteiros entre 1 e 15.
    """
    return (isinstance(arg, tuple) and len(arg) == 2 and
            isinstance(arg[0], int) and isinstance(arg[1], int) and
            coordenada_minima <= arg[0] <= coordenada_maxima and
            coordenada_minima <= arg[1] <= coordenada_maxima)


def casas_iguais(c1, c2) -> bool:
    """Verifica se duas casas são iguais."""
    return eh_casa(c1) and eh_casa(c2) and c1 == c2


def casa_para_str(c: tuple) -> str:
    """Converte uma casa para string no formato '(lin,col)'."""
    return f"({obtem_lin(c)},{obtem_col(c)})"


def str_para_casa(s: str) -> tuple:
    """Converte uma string '(lin,col)' para casa."""
    # Remove os parênteses e separa por vírgula
    s = s.strip('()')
    partes = s.split(',')
    lin = int(partes[0])
    col = int(partes[1])
    return cria_casa(lin, col)


def incrementa_casa(c: tuple, d: str, s: int) -> tuple:
    """
    Devolve a casa seguinte na direção d a distância s.
    Se sair do tabuleiro, devolve a casa original.
    """
    lin = obtem_lin(c)
    col = obtem_col(c)
    
    if d == 'H':  # Horizontal - mexe na coluna
        nova_col = col + s
        if coordenada_minima <= nova_col <= coordenada_maxima:
            return cria_casa(lin, nova_col)
    else:  # Vertical - mexe na linha
        nova_lin = lin + s
        if coordenada_minima <= nova_lin <= coordenada_maxima:
            return cria_casa(nova_lin, col)
    
    # Se não for válido, devolve a casa original
    return c


# ==================== TAD jogador ====================

def cria_humano(nome: str) -> dict:
    """
    Cria um jogador humano com um nome.
    Começa com 0 pontos e sem letras.
    """
    if not (isinstance(nome, str) and nome.strip()):
        raise ValueError('cria_humano: argumento inválido')
    
    # Um jogador é um dicionário com várias informações
    return {
        'tipo': 'humano',
        'nome': nome,
        'pontos': 0,
        'letras': []
    }


def cria_agente(nivel: str) -> dict:
    """
    Cria um jogador computador (bot) com um nível de dificuldade.
    Pode ser 'FACIL', 'MEDIO' ou 'DIFICIL'.
    """
    niveis_validos = ('FACIL', 'MEDIO', 'DIFICIL')
    if not (isinstance(nivel, str) and nivel in niveis_validos):
        raise ValueError('cria_agente: argumento inválido')
    
    return {
        'tipo': 'agente',
        'nivel': nivel,
        'pontos': 0,
        'letras': []
    }


def jogador_identidade(j: dict) -> str:
    """
    Devolve o nome do jogador (se humano) ou o nível (se bot).
    """
    if j['tipo'] == 'humano':
        return j['nome']
    else:
        return j['nivel']


def jogador_pontos(j: dict) -> int:
    """Devolve quantos pontos o jogador tem."""
    return j['pontos']


def jogador_letras(j: dict) -> str:
    """
    Devolve as letras do jogador ordenadas pela ordem canónica.
    """
    # Ordena as letras pela posição no alfabeto português
    letras_ordenadas = sorted(j['letras'], key=lambda l: letras.index(l))
    return ''.join(letras_ordenadas)


def recebe_letra(j: dict, l: str) -> dict:
    """Adiciona uma letra ao jogador."""
    j['letras'].append(l)
    return j


def usa_letra(j: dict, l: str) -> dict:
    """Remove uma letra do jogador (quando joga)."""
    j['letras'].remove(l)
    return j


def soma_pontos(j: dict, p: int) -> dict:
    """Adiciona pontos ao jogador."""
    j['pontos'] += p
    return j


def eh_jogador(arg) -> bool:
    """Verifica se o argumento é um jogador válido."""
    # Tem que ser um dicionário
    if not isinstance(arg, dict):
        return False
    
    # Tem que ter os campos necessários
    if 'tipo' not in arg or 'pontos' not in arg or 'letras' not in arg:
        return False
    
    # O tipo tem que ser válido
    if arg['tipo'] not in ('humano', 'agente'):
        return False
    
    # Os pontos têm que ser positivos
    if not isinstance(arg['pontos'], int) or arg['pontos'] < 0:
        return False
    
    # As letras têm que ser uma lista
    if not isinstance(arg['letras'], list):
        return False
    
    # Verificações específicas por tipo
    if arg['tipo'] == 'humano':
        if 'nome' not in arg or not isinstance(arg['nome'], str):
            return False
    else:
        if 'nivel' not in arg or arg['nivel'] not in ('FACIL', 'MEDIO', 'DIFICIL'):
            return False
    
    return True


def eh_humano(arg) -> bool:
    """Verifica se é um jogador humano."""
    return eh_jogador(arg) and arg['tipo'] == 'humano'


def eh_agente(arg) -> bool:
    """Verifica se é um jogador bot."""
    return eh_jogador(arg) and arg['tipo'] == 'agente'


def jogadores_iguais(j1, j2) -> bool:
    """Verifica se dois jogadores são iguais."""
    if not (eh_jogador(j1) and eh_jogador(j2)):
        return False
    
    if j1['tipo'] != j2['tipo']:
        return False
    
    # Compara pelo nome (humano) ou nível (agente)
    if j1['tipo'] == 'humano':
        return j1['nome'] == j2['nome']
    else:
        return j1['nivel'] == j2['nivel']


def jogador_para_str(j: dict) -> str:
    """
    Converte o jogador para string para mostrar no ecrã.
    Formato: "Nome (pontos): letras" ou "BOT(nivel) (pontos): letras"
    """
    identidade = jogador_identidade(j)
    pontos = jogador_pontos(j)
    letras_str = jogador_letras(j)
    
    if letras_str:
        # Coloca espaços entre as letras
        letras_formatadas = ' '.join(letras_str)
        if eh_agente(j):
            return f"BOT({identidade}) ({pontos:3d}): {letras_formatadas}"
        else:
            return f"{identidade} ({pontos:3d}): {letras_formatadas}"
    else:
        # Sem letras
        if eh_agente(j):
            return f"BOT({identidade}) ({pontos:3d}):"
        else:
            return f"{identidade} ({pontos:3d}):"


def distribui_letras(jog: dict, saco: list, num: int) -> dict:
    """
    Retira letras do saco e dá ao jogador.
    Retira no máximo 'num' letras (ou quantas houver no saco).
    """
    # Calcula quantas letras podemos retirar
    letras_a_retirar = min(num, len(saco))
    
    # Retira letras do fim do saco
    for _ in range(letras_a_retirar):
        letra = saco.pop()
        recebe_letra(jog, letra)
    
    return jog


# ==================== TAD vocabulario ====================

def cria_vocabulario(t: tuple) -> dict:
    """
    Cria um vocabulário a partir de um tuplo de palavras.
    O vocabulário organiza as palavras por comprimento e primeira letra.
    """
    if not isinstance(t, tuple) or len(t) == 0:
        raise ValueError('cria_vocabulario: argumento inválido')
    
    palavras_vistas = set()
    
    # Primeiro valida todas as palavras
    for palavra in t:
        # Tem que ser string
        if not isinstance(palavra, str):
            raise ValueError('cria_vocabulario: argumento inválido')
        
        # Comprimento entre 2 e 15
        if len(palavra) < 2 or len(palavra) > 15:
            raise ValueError('cria_vocabulario: argumento inválido')
        
        # Só pode ter letras portuguesas
        if not all(c in letras_set for c in palavra):
            raise ValueError('cria_vocabulario: argumento inválido')
        
        # Não pode haver palavras repetidas
        if palavra in palavras_vistas:
            raise ValueError('cria_vocabulario: argumento inválido')
        
        palavras_vistas.add(palavra)
    
    # Agora constrói o vocabulário
    vocab = {}
    
    for palavra in t:
        comp = len(palavra)
        primeira = palavra[0]
        
        # Cria a estrutura se ainda não existir
        if comp not in vocab:
            vocab[comp] = {}
        
        if primeira not in vocab[comp]:
            vocab[comp][primeira] = []
        
        vocab[comp][primeira].append(palavra)
    
    # Ordena as palavras: primeiro por pontuação (maior para menor),
    # depois por ordem canónica (alfabética portuguesa)
    for comp in vocab:
        for letra in vocab[comp]:
            vocab[comp][letra].sort(
                key=lambda p: (
                    -sum(pontuacao_letras.get(c, 0) for c in p),  # Pontos (negativo para ordem decrescente)
                    tuple(letras.index(c) for c in p)  # Ordem canónica
                )
            )
    
    return vocab


def obtem_pontos(vocabulario: dict, palavra: str) -> int:
    """
    Calcula quantos pontos vale uma palavra.
    Se a palavra não existir no vocabulário, devolve 0.
    """
    comp = len(palavra)
    if comp not in vocabulario:
        return 0
    
    primeira = palavra[0]
    if primeira not in vocabulario[comp]:
        return 0
    
    # Verifica se a palavra existe
    if palavra in vocabulario[comp][primeira]:
        # Soma os pontos de cada letra
        return sum(pontuacao_letras.get(letra, 0) for letra in palavra)
    
    return 0


def obtem_palavras(vocabulario: dict, comp: int, letra: str) -> tuple:
    """
    Devolve todas as palavras com um certo comprimento e primeira letra.
    Já vêm ordenadas por pontuação (maior primeiro).
    """
    if comp not in vocabulario or letra not in vocabulario[comp]:
        return ()
    
    palavras = vocabulario[comp][letra]
    # Cria pares (palavra, pontos)
    pares = [(p, obtem_pontos(vocabulario, p)) for p in palavras]
    
    # Ordena por pontuação e depois por ordem canónica
    def chave_canonica(palavra):
        return tuple(letras.index(c) for c in palavra)
    
    pares.sort(key=lambda x: (-x[1], chave_canonica(x[0])))
    
    return tuple(pares)


def testa_palavra_padrao(vocabulario: dict, palavra: str, padrao: str, letras_disp: str) -> bool:
    """
    Verifica se podemos formar uma palavra a partir de um padrão.
    O padrão tem '.' onde precisamos colocar letras.
    """
    comp = len(palavra)
    if comp != len(padrao):
        return False
    
    # Verifica se a palavra existe no vocabulário
    if comp not in vocabulario:
        return False
    
    primeira = palavra[0]
    if primeira not in vocabulario[comp]:
        return False
    
    if palavra not in vocabulario[comp][primeira]:
        return False
    
    # Verifica se temos as letras necessárias
    letras_disponiveis = list(letras_disp)
    
    for i in range(len(palavra)):
        if padrao[i] == '.':
            # Precisamos desta letra
            if palavra[i] not in letras_disponiveis:
                return False
            letras_disponiveis.remove(palavra[i])
        else:
            # A letra já está no tabuleiro
            if padrao[i] != palavra[i]:
                return False
    
    return True


def ficheiro_para_vocabulario(nome_fich: str) -> dict:
    """
    Lê um ficheiro de texto e cria um vocabulário com as palavras.
    """
    with open(nome_fich, 'r', encoding='utf-8') as f:
        linhas = f.readlines()
    
    palavras_validas = []
    
    for linha in linhas:
        palavra = linha.strip().upper()  # Remove espaços e põe em maiúsculas
        
        if not palavra:
            continue
        
        # Só aceita palavras entre 2 e 15 letras
        if len(palavra) < 2 or len(palavra) > 15:
            continue
        
        # Só aceita letras portuguesas
        if all(c in letras_set for c in palavra):
            palavras_validas.append(palavra)
    
    # Remove duplicados mantendo a ordem
    palavras_unicas = []
    vistas = set()
    for p in palavras_validas:
        if p not in vistas:
            palavras_unicas.append(p)
            vistas.add(p)
    
    return cria_vocabulario(tuple(palavras_unicas))


def vocabulario_para_str(vocabulario: dict) -> str:
    """
    Converte o vocabulário para string (todas as palavras separadas por linha).
    """
    resultado = []
    
    # Ordena por comprimento
    comprimentos = sorted(vocabulario.keys())
    
    for comp in comprimentos:
        # Ordena as primeiras letras pela ordem canónica
        primeiras = sorted(vocabulario[comp].keys(), key=lambda l: letras.index(l))
        
        for letra in primeiras:
            # As palavras já estão ordenadas
            for palavra in vocabulario[comp][letra]:
                resultado.append(palavra)
    
    return '\n'.join(resultado)


def procura_palavra_padrao(vocabulario: dict, padrao: str, letras_disp: str, min_pontos: int) -> tuple:
    """
    Procura a melhor palavra que podemos formar com um padrão.
    Devolve (palavra, pontos) ou ('', 0) se não encontrar.
    """
    comp = len(padrao)
    melhor_palavra = ''
    melhor_pontuacao = 0
    
    if padrao[0] != '.':
        # A primeira letra já está definida
        primeira = padrao[0]
        
        if comp in vocabulario and primeira in vocabulario[comp]:
            for palavra in vocabulario[comp][primeira]:
                if testa_palavra_padrao(vocabulario, palavra, padrao, letras_disp):
                    pontuacao = obtem_pontos(vocabulario, palavra)
                    
                    if pontuacao >= min_pontos and pontuacao > melhor_pontuacao:
                        melhor_pontuacao = pontuacao
                        melhor_palavra = palavra
    else:
        # Temos que tentar todas as letras disponíveis
        letras_tentadas = sorted(set(letras_disp), key=lambda l: letras.index(l))
        
        for letra_inicial in letras_tentadas:
            if comp in vocabulario and letra_inicial in vocabulario[comp]:
                for palavra in vocabulario[comp][letra_inicial]:
                    if testa_palavra_padrao(vocabulario, palavra, padrao, letras_disp):
                        pontuacao = obtem_pontos(vocabulario, palavra)
                        
                        if pontuacao >= min_pontos:
                            # Escolhe a palavra com mais pontos, ou em caso de empate, a primeira alfabeticamente
                            if pontuacao > melhor_pontuacao or \
                               (pontuacao == melhor_pontuacao and palavra < melhor_palavra):
                                melhor_pontuacao = pontuacao
                                melhor_palavra = palavra
    
    if melhor_palavra:
        return (melhor_palavra, melhor_pontuacao)
    else:
        return ('', 0)


# ==================== TAD tabuleiro ====================

def cria_tabuleiro() -> list:
    """Cria um tabuleiro vazio (15x15 com '.')."""
    return [[casa_vazia] * tamanho_tabuleiro for _ in range(tamanho_tabuleiro)]


def obtem_letra(t: list, c: tuple) -> str:
    """Devolve a letra numa casa do tabuleiro."""
    lin = obtem_lin(c)
    col = obtem_col(c)
    # Os índices internos começam em 0, mas as casas começam em 1
    return t[lin - 1][col - 1]


def insere_letra(t: list, c: tuple, l: str) -> list:
    """Coloca uma letra numa casa do tabuleiro."""
    lin = obtem_lin(c)
    col = obtem_col(c)
    t[lin - 1][col - 1] = l
    return t


def eh_tabuleiro(arg) -> bool:
    """Verifica se o argumento é um tabuleiro válido."""
    if not isinstance(arg, list):
        return False
    
    if len(arg) != tamanho_tabuleiro:
        return False
    
    for linha in arg:
        if not isinstance(linha, list):
            return False
        if len(linha) != tamanho_tabuleiro:
            return False
        for celula in linha:
            if not isinstance(celula, str):
                return False
            # Só pode ter '.' ou letras válidas
            if celula != casa_vazia and celula not in letras_set:
                return False
    
    return True


def eh_tabuleiro_vazio(arg) -> bool:
    """Verifica se o tabuleiro está vazio (sem letras)."""
    if not eh_tabuleiro(arg):
        return False
    
    for linha in arg:
        for celula in linha:
            if celula != casa_vazia:
                return False
    
    return True


def tabuleiros_iguais(t1, t2) -> bool:
    """Verifica se dois tabuleiros são iguais."""
    if not (eh_tabuleiro(t1) and eh_tabuleiro(t2)):
        return False
    
    for i in range(tamanho_tabuleiro):
        for j in range(tamanho_tabuleiro):
            if t1[i][j] != t2[i][j]:
                return False
    
    return True


def tabuleiro_para_str(t: list) -> str:
    """
    Converte o tabuleiro para string para mostrar no ecrã.
    """
    # Primeira linha com os números das colunas
    linha1 = ' ' * 23 + '1 1 1 1 1 1\n'
    linha2 = ' ' * 5 + '1 2 3 4 5 6 7 8 9 0 1 2 3 4 5\n'
    separador = ' ' * 3 + '+' + '-' * 31 + '+\n'
    
    resultado = linha1 + linha2 + separador
    
    # Linhas do tabuleiro
    for i in range(tamanho_tabuleiro):
        linha_str = f'{i + 1:2d} | '
        linha_str += ' '.join(t[i])
        linha_str += ' |\n'
        resultado += linha_str
    
    resultado += ' ' * 3 + '+' + '-' * 31 + '+'
    
    return resultado


def obtem_padrao(t: list, i: tuple, f: tuple) -> str:
    """
    Devolve uma sequência de letras entre duas casas (linha ou coluna).
    """
    lin_i = obtem_lin(i)
    col_i = obtem_col(i)
    lin_f = obtem_lin(f)
    col_f = obtem_col(f)
    
    resultado = []
    
    if lin_i == lin_f:
        # Mesma linha - vai na horizontal
        col_inicio = min(col_i, col_f)
        col_fim = max(col_i, col_f)
        for col in range(col_inicio, col_fim + 1):
            casa = cria_casa(lin_i, col)
            resultado.append(obtem_letra(t, casa))
    else:
        # Mesma coluna - vai na vertical
        lin_inicio = min(lin_i, lin_f)
        lin_fim = max(lin_i, lin_f)
        for lin in range(lin_inicio, lin_fim + 1):
            casa = cria_casa(lin, col_i)
            resultado.append(obtem_letra(t, casa))
    
    return ''.join(resultado)


def insere_palavra(t: list, c: tuple, d: str, p: str) -> list:
    """
    Coloca uma palavra no tabuleiro a partir de uma casa numa direção.
    """
    for i, letra in enumerate(p):
        if d == 'H':
            casa_atual = incrementa_casa(c, 'H', i)
        else:
            casa_atual = incrementa_casa(c, 'V', i)
        
        insere_letra(t, casa_atual, letra)
    
    return t


def obtem_subpadroes(t: list, i: tuple, f: tuple, l: int) -> tuple:
    """
    Encontra todos os sub-padrões válidos numa linha/coluna.
    Um sub-padrão é válido se tiver letras, espaços livres, e não ultrapassar o limite.
    """
    padrao = obtem_padrao(t, i, f)
    lin_i = obtem_lin(i)
    col_i = obtem_col(i)
    lin_f = obtem_lin(f)
    col_f = obtem_col(f)
    
    if lin_i == lin_f:
        direcao = 'H'
    else:
        direcao = 'V'
    
    subpadroes_validos = []
    casas_iniciais = []
    
    n = len(padrao)
    
    # Percorre todas as posições possíveis
    for i_sub in range(n):
        for j_sub in range(n, i_sub, -1):
            subpadrao = padrao[i_sub:j_sub]
            
            # Não pode ter muitos espaços livres
            if subpadrao.count('.') > l:
                continue
            
            # Tem que ter pelo menos uma letra
            tem_letra = any(c != '.' for c in subpadrao)
            if not tem_letra:
                continue
            
            # Tem que ter pelo menos um espaço livre
            tem_espaco = '.' in subpadrao
            if not tem_espaco:
                continue
            
            # Não pode estar encostado a outras letras
            tem_letra_antes = i_sub > 0 and padrao[i_sub - 1] != '.'
            tem_letra_depois = j_sub < n and padrao[j_sub] != '.'
            if tem_letra_antes or tem_letra_depois:
                continue
            
            subpadroes_validos.append(subpadrao)
            
            # Guarda a casa inicial
            if direcao == 'H':
                casa_inicial = incrementa_casa(i, 'H', i_sub)
            else:
                casa_inicial = incrementa_casa(i, 'V', i_sub)
            
            casas_iniciais.append(casa_inicial)
    
    return (tuple(subpadroes_validos), tuple(casas_iniciais))


def gera_todos_padroes(t: list, l: int) -> tuple:
    """
    Encontra todos os sub-padrões possíveis no tabuleiro inteiro.
    """
    todos_padroes = []
    todas_casas = []
    todas_direcoes = []
    
    # Percorre todas as linhas
    for lin in range(1, tamanho_tabuleiro + 1):
        casa_inicio = cria_casa(lin, 1)
        casa_fim = cria_casa(lin, tamanho_tabuleiro)
        
        subpadroes, casas = obtem_subpadroes(t, casa_inicio, casa_fim, l)
        
        for idx in range(len(subpadroes)):
            todos_padroes.append(subpadroes[idx])
            todas_casas.append(casas[idx])
            todas_direcoes.append('H')
    
    # Percorre todas as colunas
    for col in range(1, tamanho_tabuleiro + 1):
        casa_inicio = cria_casa(1, col)
        casa_fim = cria_casa(tamanho_tabuleiro, col)
        
        subpadroes, casas = obtem_subpadroes(t, casa_inicio, casa_fim, l)
        
        for idx in range(len(subpadroes)):
            todos_padroes.append(subpadroes[idx])
            todas_casas.append(casas[idx])
            todas_direcoes.append('V')
    
    return (tuple(todos_padroes), tuple(todas_casas), tuple(todas_direcoes))


# ==================== FUNÇÕES ADICIONAIS ====================

def baralha_saco(seed: int) -> list:
    """
    Cria e baralha o saco de letras usando um número seed.
    """
    lista_letras = []
    
    # Adiciona todas as letras conforme as ocorrências
    for letra in letras:
        if letra in ocorrencias_saco:
            lista_letras.extend([letra] * ocorrencias_saco[letra])
    
    # Algoritmo de Fisher-Yates para baralhar
    n = len(lista_letras)
    estado = seed
    for i in range(n - 1, 0, -1):
        estado = gera_numero_aleatorio(estado)
        j = estado % (i + 1)
        # Troca as posições i e j
        lista_letras[i], lista_letras[j] = lista_letras[j], lista_letras[i]
    
    return lista_letras


def valida_jogada(tab: list, casa: tuple, direcao: str, palavra: str, letras_jog: str, primeira: bool) -> bool:
    """
    Verifica se uma jogada é válida.
    Tem que caber no tabuleiro, usar letras disponíveis, e tocar no centro (se for primeira).
    """
    lin = obtem_lin(casa)
    col = obtem_col(casa)
    
    # Verifica se a palavra cabe no tabuleiro
    if direcao == 'H':
        if col + len(palavra) - 1 > coordenada_maxima:
            return False
    else:
        if lin + len(palavra) - 1 > coordenada_maxima:
            return False
    
    letras_necessarias = []
    toca_tabuleiro = False
    
    # Verifica cada posição da palavra
    for i, letra in enumerate(palavra):
        if direcao == 'H':
            casa_atual = incrementa_casa(casa, 'H', i)
        else:
            casa_atual = incrementa_casa(casa, 'V', i)
        
        letra_tab = obtem_letra(tab, casa_atual)
        
        if letra_tab == '.':
            # Precisamos colocar esta letra
            letras_necessarias.append(letra)
        elif letra_tab == letra:
            # A letra já está no tabuleiro
            toca_tabuleiro = True
        else:
            # Conflito!
            return False
    
    # Verifica se temos as letras necessárias
    letras_disponiveis = list(letras_jog)
    for letra in letras_necessarias:
        if letra in letras_disponiveis:
            letras_disponiveis.remove(letra)
        else:
            return False
    
    if primeira:
        # A primeira jogada tem que passar pelo centro
        cobre_central = False
        for i in range(len(palavra)):
            if direcao == 'H':
                casa_i = incrementa_casa(casa, 'H', i)
            else:
                casa_i = incrementa_casa(casa, 'V', i)
            
            if casas_iguais(casa_i, CASA_CENTRAL):
                cobre_central = True
                break
        
        if not cobre_central:
            return False
    else:
        # Jogadas seguintes têm que tocar em letras existentes
        if not toca_tabuleiro:
            return False
    
    return True


def jogada_humano(tab: list, jog: dict, vocab: dict, pilha: list) -> bool:
    """
    Processa a jogada de um jogador humano.
    Pede input e valida até conseguir uma jogada válida.
    """
    nome = jogador_identidade(jog)
    primeira_jogada = eh_tabuleiro_vazio(tab)
    
    while True:
        print(f"Jogada {nome}: ", end='')
        entrada = input().strip().upper()
        
        if not entrada:
            continue
        
        partes = entrada.split()
        comando = partes[0]
        
        if comando == 'P' and len(partes) == 1:
            # Passar
            return False
        
        elif comando == 'T' and len(partes) >= 2:
            # Trocar letras
            letras_trocar = partes[1:]
            letras_jog = jogador_letras(jog)
            
            # Tem que haver letras suficientes no saco
            if len(letras_trocar) > len(pilha):
                continue
            
            # Verifica se o jogador tem estas letras
            letras_disponiveis = list(letras_jog)
            pode_trocar = True
            
            for letra in letras_trocar:
                if letra in letras_disponiveis:
                    letras_disponiveis.remove(letra)
                else:
                    pode_trocar = False
                    break
            
            if pode_trocar:
                # Remove as letras
                for letra in letras_trocar:
                    usa_letra(jog, letra)
                
                # Dá novas letras
                num_letras_atuais = len(jogador_letras(jog))
                num_distribuir = min(TAMANHO_MAO - num_letras_atuais, len(pilha))
                distribui_letras(jog, pilha, num_distribuir)
                
                return True
        
        elif comando == 'J' and len(partes) == 5:
            # Jogar palavra
            try:
                linha = int(partes[1])
                coluna = int(partes[2])
                direcao = partes[3]
                palavra = partes[4]
                
                # Valida as coordenadas
                if not (coordenada_minima <= linha <= coordenada_maxima and
                        coordenada_minima <= coluna <= coordenada_maxima):
                    continue
                
                if direcao not in ('H', 'V'):
                    continue
                
                casa = cria_casa(linha, coluna)
                
                # Verifica se a palavra existe no vocabulário
                comp_palavra = len(palavra)
                if comp_palavra not in vocab:
                    continue
                
                primeira_letra = palavra[0]
                if primeira_letra not in vocab[comp_palavra]:
                    continue
                
                if palavra not in vocab[comp_palavra][primeira_letra]:
                    continue
                
                # Valida a jogada
                if not valida_jogada(tab, casa, direcao, palavra, jogador_letras(jog), primeira_jogada):
                    continue
                
                # Jogada válida! Atualiza tudo
                pontuacao = obtem_pontos(vocab, palavra)
                soma_pontos(jog, pontuacao)
                
                # Remove as letras usadas
                letras_usadas = []
                for i, letra in enumerate(palavra):
                    if direcao == 'H':
                        casa_atual = incrementa_casa(casa, 'H', i)
                    else:
                        casa_atual = incrementa_casa(casa, 'V', i)
                    
                    if obtem_letra(tab, casa_atual) == '.':
                        letras_usadas.append(letra)
                
                for letra in letras_usadas:
                    usa_letra(jog, letra)
                
                # Coloca a palavra no tabuleiro
                insere_palavra(tab, casa, direcao, palavra)
                
                # Dá novas letras
                num_letras_atuais = len(jogador_letras(jog))
                num_distribuir = min(TAMANHO_MAO - num_letras_atuais, len(pilha))
                distribui_letras(jog, pilha, num_distribuir)
                
                return True
                
            except (ValueError, IndexError):
                continue


def jogada_agente(tab: list, jog: dict, vocab: dict, pilha: list) -> bool:
    """
    Processa a jogada de um bot.
    Escolhe a melhor jogada dependendo do nível de dificuldade.
    """
    nivel = jogador_identidade(jog)
    primeira_jogada = eh_tabuleiro_vazio(tab)
    letras_jog = jogador_letras(jog)
    num_letras = len(letras_jog)
    
    # Na primeira jogada, passa
    if primeira_jogada:
        print(f"Jogada {nivel}: P")
        return False
    
    # Define quantos padrões vai analisar (depende do nível)
    if nivel == 'FACIL':
        n = 100  # Analisa menos padrões
    elif nivel == 'MEDIO':
        n = 50
    else:  # DIFICIL
        n = 10  # Analisa mais padrões
    
    # Obtém todos os padrões possíveis
    padroes, casas, direcoes = gera_todos_padroes(tab, num_letras)
    
    # Seleciona apenas alguns padrões para analisar
    padroes_selecionados = padroes[::n]
    casas_selecionadas = casas[::n]
    direcoes_selecionadas = direcoes[::n]
    
    # Procura a melhor jogada
    melhor_palavra = ''
    melhor_pontuacao = 0
    melhor_casa = None
    melhor_direcao = None
    
    for i in range(len(padroes_selecionados)):
        padrao = padroes_selecionados[i]
        casa = casas_selecionadas[i]
        direcao = direcoes_selecionadas[i]
        
        # Procura a melhor palavra para este padrão
        palavra, pontuacao = procura_palavra_padrao(vocab, padrao, letras_jog, 0)
        
        if palavra and pontuacao > melhor_pontuacao:
            melhor_palavra = palavra
            melhor_pontuacao = pontuacao
            melhor_casa = casa
            melhor_direcao = direcao
    
    if melhor_palavra:
        # Encontrou uma jogada!
        lin = obtem_lin(melhor_casa)
        col = obtem_col(melhor_casa)
        
        print(f"Jogada {nivel}: J {lin} {col} {melhor_direcao} {melhor_palavra}")
        
        soma_pontos(jog, melhor_pontuacao)
        
        # Remove as letras usadas
        for i, letra in enumerate(melhor_palavra):
            if melhor_direcao == 'H':
                casa_atual = incrementa_casa(melhor_casa, 'H', i)
            else:
                casa_atual = incrementa_casa(melhor_casa, 'V', i)
            
            if obtem_letra(tab, casa_atual) == '.':
                usa_letra(jog, letra)
        
        # Coloca a palavra
        insere_palavra(tab, melhor_casa, melhor_direcao, melhor_palavra)
        
        # Recebe novas letras
        num_letras_atuais = len(jogador_letras(jog))
        num_distribuir = min(TAMANHO_MAO - num_letras_atuais, len(pilha))
        distribui_letras(jog, pilha, num_distribuir)
        
        return True
    
    # Se não encontrou jogada, tenta trocar letras
    if len(pilha) >= 7:
        print(f"Jogada {nivel}: T {' '.join(letras_jog)}")
        
        # Troca todas as letras
        for letra in list(letras_jog):
            usa_letra(jog, letra)
        
        distribui_letras(jog, pilha, min(7, len(pilha)))
        
        return True
    
    # Caso contrário, passa
    print(f"Jogada {nivel}: P")
    return False


def scrabble2(jog: tuple, nome_fich: str, seed: int) -> tuple:
    """
    Função principal do jogo.
    Recebe os jogadores, o ficheiro de vocabulário e a seed.
    """
    # Valida os argumentos
    if not isinstance(jog, tuple) or not isinstance(nome_fich, str) or not isinstance(seed, int):
        raise ValueError('scrabble2: argumentos inválidos')
    
    if len(jog) < 2 or len(jog) > 4:
        raise ValueError('scrabble2: argumentos inválidos')
    
    if seed <= 0:
        raise ValueError('scrabble2: argumentos inválidos')
    
    # Cria os jogadores
    jogadores = []
    for info in jog:
        if not isinstance(info, str) or not info:
            raise ValueError('scrabble2: argumentos inválidos')
        
        if info.startswith('@'):
            # É um bot
            nivel = info[1:]
            if nivel not in ('MEDIO', 'DIFICIL', 'FACIL'):
                raise ValueError('scrabble2: argumentos inválidos')
            jogadores.append(cria_agente(nivel))
        else:
            # É humano
            jogadores.append(cria_humano(info))
    
    # Carrega o vocabulário
    vocab = ficheiro_para_vocabulario(nome_fich)
    
    # Baralha o saco
    pilha = baralha_saco(seed)
    
    # Distribui letras iniciais
    for jogador in jogadores:
        distribui_letras(jogador, pilha, TAMANHO_MAO)
    
    # Cria o tabuleiro
    tab = cria_tabuleiro()
    
    # Mostra o estado inicial
    print("Bem-vindo ao SCRABBLE2.")
    print(tabuleiro_para_str(tab))
    
    for jogador in jogadores:
        print(jogador_para_str(jogador))
    
    # Loop principal do jogo
    passes_consecutivos = 0
    num_jogadores = len(jogadores)
    
    while passes_consecutivos < num_jogadores:
        for jogador in jogadores:
            # Verifica se acabou (ninguém tem letras e saco vazio)
            if len(jogador_letras(jogador)) == 0 and len(pilha) == 0:
                passes_consecutivos = num_jogadores
                break
            
            # Processa a jogada
            if eh_humano(jogador):
                jogou = jogada_humano(tab, jogador, vocab, pilha)
            else:
                jogou = jogada_agente(tab, jogador, vocab, pilha)
            
            if jogou:
                # Reset do contador de passes
                passes_consecutivos = 0
                # Mostra o estado
                print(tabuleiro_para_str(tab))
                for j in jogadores:
                    print(jogador_para_str(j))
            else:
                # Passou
                passes_consecutivos += 1
                if passes_consecutivos < num_jogadores:
                    print(tabuleiro_para_str(tab))
                    for j in jogadores:
                        print(jogador_para_str(j))
            
            # Se todos passaram, acaba
            if passes_consecutivos >= num_jogadores:
                break
    
    # Devolve as pontuações finais
    return tuple(jogador_pontos(j) for j in jogadores)
