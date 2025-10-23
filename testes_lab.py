# FP 2025/2026 - Projeto 2
# Scrabble com TADs e IA

# ==================== CONSTANTES ====================

# Alfabeto português na ordem canónica
letras = ('A', 'B', 'C', 'Ç', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'L', 'M', 'N', 'O',
          'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'X', 'Z')
letras_set = set(letras)

# Constantes do gerador xorshift
bits = 0xFFFFFFFF
shift_1 = 13
shift_2 = 17
shift_3 = 5

# Configurações do tabuleiro
tamanho_tabuleiro = 15
coordenada_minima = 1
coordenada_maxima = 15
casa_vazia = '.'
CASA_CENTRAL = (8, 8)
TAMANHO_MAO = 7

# Tabela 2: Número de ocorrências das letras no saco
ocorrencias_saco = {
    'A': 14, 'B': 3, 'C': 4, 'Ç': 2, 'D': 5, 'E': 11, 'F': 2,
    'G': 2, 'H': 2, 'I': 10, 'J': 2, 'L': 5, 'M': 6, 'N': 4,
    'O': 10, 'P': 4, 'Q': 1, 'R': 6, 'S': 8, 'T': 5,
    'U': 7, 'V': 2, 'X': 1, 'Z': 1
}


# ==================== GERADOR PSEUDO-ALEATÓRIO ====================

def gera_numero_aleatorio(estado: int) -> int:
    """
    Implementação do algoritmo Xorshift para geração de números pseudo-aleatórios.
    Recebe um estado e devolve o próximo número da sequência.
    """
    estado &= bits
    estado = (estado ^ (estado << shift_1)) & bits
    estado = (estado ^ (estado >> shift_2)) & bits
    estado = (estado ^ (estado << shift_3)) & bits
    return estado


# ==================== TAD casa ====================

def cria_casa(lin: int, col: int) -> tuple:
    """
    Construtor: Cria uma casa do tabuleiro.
    Recebe linha e coluna (inteiros entre 1 e 15) e devolve a casa correspondente.
    Levanta ValueError se os argumentos forem inválidos.
    """
    if not (isinstance(lin, int) and isinstance(col, int) and 
            coordenada_minima <= lin <= coordenada_maxima and 
            coordenada_minima <= col <= coordenada_maxima):
        raise ValueError('cria_casa: argumentos inválidos')
    return (lin, col)


def obtem_lin(c: tuple) -> int:
    """Seletor: Devolve a linha da casa c."""
    return c[0]


def obtem_col(c: tuple) -> int:
    """Seletor: Devolve a coluna da casa c."""
    return c[1]


def eh_casa(arg) -> bool:
    """
    Reconhecedor: Verifica se arg é um TAD casa válido.
    Devolve True se for uma casa válida, False caso contrário.
    """
    return (isinstance(arg, tuple) and len(arg) == 2 and
            isinstance(arg[0], int) and isinstance(arg[1], int) and
            coordenada_minima <= arg[0] <= coordenada_maxima and
            coordenada_minima <= arg[1] <= coordenada_maxima)


def casas_iguais(c1, c2) -> bool:
    """
    Teste: Verifica se c1 e c2 são casas iguais.
    Devolve True apenas se ambos são casas e são iguais.
    """
    return eh_casa(c1) and eh_casa(c2) and c1 == c2


def casa_para_str(c: tuple) -> str:
    """
    Transformador: Converte casa para string no formato '(lin,col)'.
    """
    return f"({obtem_lin(c)},{obtem_col(c)})"


def str_para_casa(s: str) -> tuple:
    """
    Transformador: Converte string no formato '(lin,col)' para casa.
    """
    s = s.strip('()')
    partes = s.split(',')
    lin = int(partes[0])
    col = int(partes[1])
    return cria_casa(lin, col)


def incrementa_casa(c: tuple, d: str, s: int) -> tuple:
    """
    Função de alto nível: Devolve a casa a seguir de c na direção d 
    a distância s (inteiro positivo).
    Se a casa resultante não existir no tabuleiro, devolve a casa c.
    d pode ser 'H' (horizontal) ou 'V' (vertical).
    """
    lin = obtem_lin(c)
    col = obtem_col(c)
    
    if d == 'H':
        nova_col = col + s
        if coordenada_minima <= nova_col <= coordenada_maxima:
            return cria_casa(lin, nova_col)
    else:  # d == 'V'
        nova_lin = lin + s
        if coordenada_minima <= nova_lin <= coordenada_maxima:
            return cria_casa(nova_lin, col)
    
    return c


# ==================== TAD jogador ====================

def cria_humano(nome: str) -> dict:
    """
    Construtor: Cria um jogador humano com nome (cadeia não vazia),
    0 pontos e sem letras.
    Levanta ValueError se o argumento for inválido.
    """
    if not (isinstance(nome, str) and nome.strip()):
        raise ValueError('cria_humano: argumento inválido')
    return {
        'tipo': 'humano',
        'nome': nome,
        'pontos': 0,
        'letras': []
    }


def cria_agente(nivel: str) -> dict:
    """
    Construtor: Cria um jogador agente com nível ('FACIL', 'MEDIO' ou 'DIFICIL'),
    0 pontos e sem letras.
    Levanta ValueError se o argumento for inválido.
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
    Seletor: Devolve o nome do jogador j se é humano,
    ou o nível se é agente.
    """
    if j['tipo'] == 'humano':
        return j['nome']
    else:  # agente
        return j['nivel']


def jogador_pontos(j: dict) -> int:
    """
    Seletor: Devolve os pontos do jogador j.
    """
    return j['pontos']


def jogador_letras(j: dict) -> str:
    """
    Seletor: Devolve a cadeia de caracteres ordenada 
    com todas as letras do jogador j.
    """
    letras_ordenadas = sorted(j['letras'], key=lambda l: letras.index(l))
    return ''.join(letras_ordenadas)


def recebe_letra(j: dict, l: str) -> dict:
    """
    Modificador: Adiciona destrutivamente a letra l às letras do jogador j.
    Devolve o próprio jogador.
    """
    j['letras'].append(l)
    return j


def usa_letra(j: dict, l: str) -> dict:
    """
    Modificador: Remove destrutivamente a letra l das letras do jogador j.
    Devolve o próprio jogador.
    """
    j['letras'].remove(l)
    return j


def soma_pontos(j: dict, p: int) -> dict:
    """
    Modificador: Soma destrutivamente os pontos p à pontuação do jogador j.
    Devolve o próprio jogador.
    """
    j['pontos'] += p
    return j


def eh_jogador(arg) -> bool:
    """
    Reconhecedor: Verifica se arg é um TAD jogador válido.
    Devolve True se for jogador, False caso contrário.
    """
    if not isinstance(arg, dict):
        return False
    
    if 'tipo' not in arg or 'pontos' not in arg or 'letras' not in arg:
        return False
    
    if arg['tipo'] not in ('humano', 'agente'):
        return False
    
    if not isinstance(arg['pontos'], int) or arg['pontos'] < 0:
        return False
    
    if not isinstance(arg['letras'], list):
        return False
    
    if arg['tipo'] == 'humano':
        if 'nome' not in arg or not isinstance(arg['nome'], str):
            return False
    else:
        if 'nivel' not in arg or arg['nivel'] not in ('FACIL', 'MEDIO', 'DIFICIL'):
            return False
    
    return True


def eh_humano(arg) -> bool:
    """
    Reconhecedor: Verifica se arg é um TAD jogador humano.
    Devolve True se for jogador humano, False caso contrário.
    """
    return eh_jogador(arg) and arg['tipo'] == 'humano'


def eh_agente(arg) -> bool:
    """
    Reconhecedor: Verifica se arg é um TAD jogador agente.
    Devolve True se for jogador agente, False caso contrário.
    """
    return eh_jogador(arg) and arg['tipo'] == 'agente'


def jogadores_iguais(j1, j2) -> bool:
    """
    Teste: Verifica se j1 e j2 são jogadores iguais.
    Devolve True apenas se ambos forem jogadores e forem iguais.
    """
    if not (eh_jogador(j1) and eh_jogador(j2)):
        return False
    
    if j1['tipo'] != j2['tipo']:
        return False
    
    if j1['tipo'] == 'humano':
        return j1['nome'] == j2['nome']
    else:
        return j1['nivel'] == j2['nivel']


def jogador_para_str(j: dict) -> str:
    """
    Transformador: Devolve a cadeia de caracteres que representa o jogador,
    como mostrado nos exemplos.
    """
    identidade = jogador_identidade(j)
    pontos = jogador_pontos(j)
    letras_str = jogador_letras(j)
    
    letras_formatadas = ' '.join(letras_str)
    
    return f"{identidade} ({pontos:3d}): {letras_formatadas}"


def distribui_letras(jog: dict, saco: list, num: int) -> dict:
    """
    Função de alto nível: Retira no máximo num letras do final da lista saco
    (potencialmente vazia) e acrescenta-as ao jogador jog.
    Modifica destrutivamente a lista de letras e o jogador.
    Devolve o jogador.
    """
    letras_retiradas = min(num, len(saco))
    
    for _ in range(letras_retiradas):
        letra = saco.pop()
        recebe_letra(jog, letra)
    
    return jog


# ==================== TAD vocabulario ====================

def cria_vocabulario(t: tuple) -> dict:
    """
    Construtor: Cria um vocabulário que contém as palavras do tuplo t.
    O construtor verifica a validade do argumento, gerando ValueError
    com a mensagem 'cria_vocabulario: argumento inválido'.
    """
    if not isinstance(t, tuple) or len(t) == 0:
        raise ValueError('cria_vocabulario: argumento inválido')
    
    palavras_vistas = set()
    
    for palavra in t:
        if not isinstance(palavra, str):
            raise ValueError('cria_vocabulario: argumento inválido')
        
        if len(palavra) < 2 or len(palavra) > 15:
            raise ValueError('cria_vocabulario: argumento inválido')
        
        if not all(c in letras_set for c in palavra):
            raise ValueError('cria_vocabulario: argumento inválido')
        
        if palavra in palavras_vistas:
            raise ValueError('cria_vocabulario: argumento inválido')
        
        palavras_vistas.add(palavra)
    
    vocab = {}
    
    for palavra in palavras_vistas:
        comp = len(palavra)
        primeira = palavra[0]
        
        if comp not in vocab:
            vocab[comp] = {}
        
        if primeira not in vocab[comp]:
            vocab[comp][primeira] = []
        
        vocab[comp][primeira].append(palavra)
    
    for comp in vocab:
        for letra in vocab[comp]:
            vocab[comp][letra].sort()
    
    return vocab


def obtem_pontos(vocabulario: dict, palavra: str) -> int:
    """
    Seletor: Devolve os pontos da palavra do vocabulário,
    ou 0 caso não se encontre.
    """
    comp = len(palavra)
    if comp not in vocabulario:
        return 0
    
    primeira = palavra[0]
    if primeira not in vocabulario[comp]:
        return 0
    
    if palavra in vocabulario[comp][primeira]:
        return comp
    
    return 0


def obtem_palavras(vocabulario: dict, comp: int, letra: str) -> tuple:
    """
    Seletor: Devolve um tuplo de pares que correspondem a todas as palavras
    com comprimento comp e primeira letra letra.
    """
    if comp not in vocabulario or letra not in vocabulario[comp]:
        return ()
    
    palavras = vocabulario[comp][letra]
    return tuple((p, len(p)) for p in palavras)


def testa_palavra_padrao(vocabulario: dict, palavra: str, padrao: str, letras_disp: str) -> bool:
    """
    Teste: Devolve True caso exista a palavra no vocabulário e seja possível
    formar a palavra fornecida substituindo os caracteres '.' do padrão
    por letras de letras_disp.
    """
    comp = len(palavra)
    if comp != len(padrao):
        return False
    
    if comp not in vocabulario:
        return False
    
    primeira = palavra[0]
    if primeira not in vocabulario[comp]:
        return False
    
    if palavra not in vocabulario[comp][primeira]:
        return False
    
    letras_disponiveis = list(letras_disp)
    
    for i in range(len(palavra)):
        if padrao[i] == '.':
            if palavra[i] not in letras_disponiveis:
                return False
            letras_disponiveis.remove(palavra[i])
        else:
            if padrao[i] != palavra[i]:
                return False
    
    return True


def ficheiro_para_vocabulario(nome_fich: str) -> dict:
    """
    Transformador: Devolve o vocabulário formado a partir das palavras
    contidas no ficheiro nome_fich.
    """
    with open(nome_fich, 'r', encoding='utf-8') as f:
        linhas = f.readlines()
    
    palavras_validas = []
    
    for linha in linhas:
        palavra = linha.strip().upper()
        
        if not palavra:
            continue
        
        if len(palavra) < 2 or len(palavra) > 15:
            continue
        
        if all(c in letras_set for c in palavra):
            palavras_validas.append(palavra)
    
    palavras_unicas = []
    vistas = set()
    for p in palavras_validas:
        if p not in vistas:
            palavras_unicas.append(p)
            vistas.add(p)
    
    return cria_vocabulario(tuple(palavras_unicas))


def vocabulario_para_str(vocabulario: dict) -> str:
    """
    Transformador: Devolve uma cadeia de caracteres que concatena
    todas as palavras guardadas no vocabulário, separadas por mudança de linha.
    """
    resultado = []
    
    comprimentos = sorted(vocabulario.keys())
    
    for comp in comprimentos:
        primeiras = sorted(vocabulario[comp].keys(), key=lambda l: letras.index(l))
        
        for letra in primeiras:
            for palavra in vocabulario[comp][letra]:
                resultado.append(palavra)
    
    return '\n'.join(resultado)


def procura_palavra_padrao(vocabulario: dict, padrao: str, letras_disp: str, min_pontos: int) -> tuple:
    """
    Função de alto nível: Devolve o tuplo formado pela palavra e a pontuação,
    que correspondem à palavra do vocabulário com maior pontuação que é possível
    formar utilizando as letras da cadeia de caracteres letras_disp.
    """
    comp = len(padrao)
    melhor_palavra = ''
    melhor_pontuacao = 0
    
    if padrao[0] != '.':
        primeira = padrao[0]
        
        if comp in vocabulario and primeira in vocabulario[comp]:
            for palavra in vocabulario[comp][primeira]:
                if testa_palavra_padrao(vocabulario, palavra, padrao, letras_disp):
                    pontuacao = obtem_pontos(vocabulario, palavra)
                    
                    if pontuacao >= min_pontos:
                        if pontuacao > melhor_pontuacao:
                            melhor_pontuacao = pontuacao
                            melhor_palavra = palavra
    else:
        letras_tentadas = sorted(set(letras_disp), key=lambda l: letras.index(l))
        
        for letra_inicial in letras_tentadas:
            if comp in vocabulario and letra_inicial in vocabulario[comp]:
                for palavra in vocabulario[comp][letra_inicial]:
                    if testa_palavra_padrao(vocabulario, palavra, padrao, letras_disp):
                        pontuacao = obtem_pontos(vocabulario, palavra)
                        
                        if pontuacao >= min_pontos:
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
    """
    Construtor: Devolve um tabuleiro de Scrabble vazio (sem letras).
    """
    return [[casa_vazia] * tamanho_tabuleiro for _ in range(tamanho_tabuleiro)]


def obtem_letra(t: list, c: tuple) -> str:
    """
    Seletor: Devolve a letra contida na casa c do tabuleiro t.
    """
    lin = obtem_lin(c)
    col = obtem_col(c)
    return t[lin - 1][col - 1]


def insere_letra(t: list, c: tuple, l: str) -> list:
    """
    Modificador: Modifica destrutivamente o tabuleiro t colocando
    a letra l na casa c, e devolve o próprio tabuleiro.
    """
    lin = obtem_lin(c)
    col = obtem_col(c)
    t[lin - 1][col - 1] = l
    return t


def eh_tabuleiro(arg) -> bool:
    """
    Reconhecedor: Devolve True caso o seu argumento seja um TAD tabuleiro,
    e False caso contrário.
    """
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
            if celula != casa_vazia and celula not in letras_set:
                return False
    
    return True


def eh_tabuleiro_vazio(arg) -> bool:
    """
    Reconhecedor: Devolve True caso o seu argumento seja um TAD tabuleiro
    e estiver vazio (sem letras), e False caso contrário.
    """
    if not eh_tabuleiro(arg):
        return False
    
    for linha in arg:
        for celula in linha:
            if celula != casa_vazia:
                return False
    
    return True


def tabuleiros_iguais(t1, t2) -> bool:
    """
    Teste: Devolve True apenas se t1 e t2 forem tabuleiros e forem iguais.
    """
    if not (eh_tabuleiro(t1) and eh_tabuleiro(t2)):
        return False
    
    for i in range(tamanho_tabuleiro):
        for j in range(tamanho_tabuleiro):
            if t1[i][j] != t2[i][j]:
                return False
    
    return True


def tabuleiro_para_str(t: list) -> str:
    """
    Transformador: Devolve a cadeia de caracteres que representa o tabuleiro
    como mostrado nos exemplos.
    """
    linha1 = ' ' * 23 + '1 1 1 1 1 1\n'
    linha2 = ' ' * 5 + '1 2 3 4 5 6 7 8 9 0 1 2 3 4 5\n'
    separador = ' ' * 3 + '+' + '-' * 31 + '+\n'
    
    resultado = linha1 + linha2 + separador
    
    for i in range(tamanho_tabuleiro):
        linha_str = f'{i + 1:2d} | '
        linha_str += ' '.join(t[i])
        linha_str += ' |\n'
        resultado += linha_str
    
    resultado += ' ' * 3 + '+' + '-' * 31 + '+'
    
    return resultado


def obtem_padrao(t: list, i: tuple, f: tuple) -> str:
    """
    Função de alto nível: Devolve a sequência de letras contida no tabuleiro t
    entre a casa i e a casa f (ambas inclusive).
    """
    lin_i = obtem_lin(i)
    col_i = obtem_col(i)
    lin_f = obtem_lin(f)
    col_f = obtem_col(f)
    
    resultado = []
    
    if lin_i == lin_f:
        col_inicio = min(col_i, col_f)
        col_fim = max(col_i, col_f)
        for col in range(col_inicio, col_fim + 1):
            casa = cria_casa(lin_i, col)
            resultado.append(obtem_letra(t, casa))
    else:
        lin_inicio = min(lin_i, lin_f)
        lin_fim = max(lin_i, lin_f)
        for lin in range(lin_inicio, lin_fim + 1):
            casa = cria_casa(lin, col_i)
            resultado.append(obtem_letra(t, casa))
    
    return ''.join(resultado)


def insere_palavra(t: list, c: tuple, d: str, p: str) -> list:
    """
    Função de alto nível: Modifica destrutivamente o tabuleiro t colocando
    a palavra p na casa c na direção d, e devolve o próprio tabuleiro.
    """
    for i, letra in enumerate(p):
        if d == 'H':
            casa_atual = incrementa_casa(c, 'H', i)
        else:
            casa_atual = incrementa_casa(c, 'V', i)
        
        insere_letra(t, casa_atual, letra)
    
    return t


def obtem_subpadroes(t: list, i: tuple, f: tuple) -> tuple:
    """
    Função de alto nível: Devolve dois tuplos de igual tamanho com os sub-padrões
    viáveis e suas casas iniciais.
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
    
    for i_sub in range(n):
        for j_sub in range(i_sub + 1, n + 1):
            subpadrao = padrao[i_sub:j_sub]
            
            tem_letra = any(c != '.' for c in subpadrao)
            if not tem_letra:
                continue
            
            tem_espaco = '.' in subpadrao
            if not tem_espaco:
                continue
            
            tem_letra_antes = i_sub > 0 and padrao[i_sub - 1] != '.'
            tem_letra_depois = j_sub < n and padrao[j_sub] != '.'
            if tem_letra_antes or tem_letra_depois:
                continue
            
            subpadroes_validos.append(subpadrao)
            
            if direcao == 'H':
                casa_inicial = incrementa_casa(i, 'H', i_sub)
            else:
                casa_inicial = incrementa_casa(i, 'V', i_sub)
            
            casas_iniciais.append(casa_inicial)
    
    return (tuple(subpadroes_validos), tuple(casas_iniciais))


def gera_todos_padroes(t: list, l: int) -> tuple:
    """
    Função de alto nível: Devolve três tuplos com todos os sub-padrões viáveis,
    suas casas e direções.
    """
    todos_padroes = []
    todas_casas = []
    todas_direcoes = []
    
    for lin in range(1, tamanho_tabuleiro + 1):
        casa_inicio = cria_casa(lin, 1)
        casa_fim = cria_casa(lin, tamanho_tabuleiro)
        
        subpadroes, casas = obtem_subpadroes(t, casa_inicio, casa_fim)
        
        for idx, subpadrao in enumerate(subpadroes):
            num_espacos = subpadrao.count('.')
            if num_espacos <= l:
                todos_padroes.append(subpadrao)
                todas_casas.append(casas[idx])
                todas_direcoes.append('H')
    
    for col in range(1, tamanho_tabuleiro + 1):
        casa_inicio = cria_casa(1, col)
        casa_fim = cria_casa(tamanho_tabuleiro, col)
        
        subpadroes, casas = obtem_subpadroes(t, casa_inicio, casa_fim)
        
        for idx, subpadrao in enumerate(subpadroes):
            num_espacos = subpadrao.count('.')
            if num_espacos <= l:
                todos_padroes.append(subpadrao)
                todas_casas.append(casas[idx])
                todas_direcoes.append('V')
    
    return (tuple(todos_padroes), tuple(todas_casas), tuple(todas_direcoes))


# ==================== FUNÇÕES ADICIONAIS ====================

def baralha_saco(seed: int) -> list:
    """
    Função auxiliar que recebe um inteiro positivo seed e devolve uma lista
    baralhada com todas as letras contidas no saco de Scrabble.
    """
    lista_letras = []
    for letra in letras:
        if letra in ocorrencias_saco:
            lista_letras.extend([letra] * ocorrencias_saco[letra])
    
    n = len(lista_letras)
    estado = seed
    for i in range(n - 1, 0, -1):
        estado = gera_numero_aleatorio(estado)
        j = estado % (i + 1)
        lista_letras[i], lista_letras[j] = lista_letras[j], lista_letras[i]
    
    return lista_letras


def valida_jogada(tab: list, casa: tuple, direcao: str, palavra: str, letras_jog: str, primeira: bool) -> bool:
    """
    Função auxiliar para validar se uma jogada é válida.
    """
    lin = obtem_lin(casa)
    col = obtem_col(casa)
    
    if direcao == 'H':
        if col + len(palavra) - 1 > coordenada_maxima:
            return False
    else:
        if lin + len(palavra) - 1 > coordenada_maxima:
            return False
    
    letras_necessarias = []
    toca_tabuleiro = False
    
    for i, letra in enumerate(palavra):
        if direcao == 'H':
            casa_atual = incrementa_casa(casa, 'H', i)
        else:
            casa_atual = incrementa_casa(casa, 'V', i)
        
        letra_tab = obtem_letra(tab, casa_atual)
        
        if letra_tab == '.':
            letras_necessarias.append(letra)
        elif letra_tab == letra:
            toca_tabuleiro = True
        else:
            return False
    
    letras_disponiveis = list(letras_jog)
    for letra in letras_necessarias:
        if letra in letras_disponiveis:
            letras_disponiveis.remove(letra)
        else:
            return False
    
    if primeira:
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
        if not toca_tabuleiro:
            return False
    
    return True


def jogada_humano(tab: list, jog: dict, vocab: dict, pilha: list) -> bool:
    """
    Função auxiliar que recebe um tabuleiro, um jogador humano, um vocabulário
    e uma lista de letras. A função processa o turno completo do jogador humano.
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
            return False
        
        elif comando == 'T' and len(partes) >= 2:
            letras_trocar = partes[1:]
            letras_jog = jogador_letras(jog)
            
            if len(letras_trocar) > len(pilha):
                continue
            
            letras_disponiveis = list(letras_jog)
            pode_trocar = True
            
            for letra in letras_trocar:
                if letra in letras_disponiveis:
                    letras_disponiveis.remove(letra)
                else:
                    pode_trocar = False
                    break
            
            if pode_trocar:
                for letra in letras_trocar:
                    usa_letra(jog, letra)
                
                num_letras_atuais = len(jogador_letras(jog))
                num_distribuir = min(TAMANHO_MAO - num_letras_atuais, len(pilha))
                distribui_letras(jog, pilha, num_distribuir)
                
                return True
        
        elif comando == 'J' and len(partes) == 5:
            try:
                linha = int(partes[1])
                coluna = int(partes[2])
                direcao = partes[3]
                palavra = partes[4]
                
                if not (coordenada_minima <= linha <= coordenada_maxima and
                        coordenada_minima <= coluna <= coordenada_maxima):
                    continue
                
                if direcao not in ('H', 'V'):
                    continue
                
                casa = cria_casa(linha, coluna)
                
                comp_palavra = len(palavra)
                if comp_palavra not in vocab:
                    continue
                
                primeira_letra = palavra[0]
                if primeira_letra not in vocab[comp_palavra]:
                    continue
                
                if palavra not in vocab[comp_palavra][primeira_letra]:
                    continue
                
                if not valida_jogada(tab, casa, direcao, palavra, jogador_letras(jog), primeira_jogada):
                    continue
                
                pontuacao = obtem_pontos(vocab, palavra)
                soma_pontos(jog, pontuacao)
                
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
                
                insere_palavra(tab, casa, direcao, palavra)
                
                num_letras_atuais = len(jogador_letras(jog))
                num_distribuir = min(TAMANHO_MAO - num_letras_atuais, len(pilha))
                distribui_letras(jog, pilha, num_distribuir)
                
                return True
                
            except (ValueError, IndexError):
                continue


def jogada_agente(tab: list, jog: dict, vocab: dict, pilha: list) -> bool:
    """
    Função auxiliar que recebe um tabuleiro, um jogador agente, um vocabulário
    e uma lista de letras, e realiza uma das ações: Passar, Trocar ou Jogar.
    """
    nivel = jogador_identidade(jog)
    primeira_jogada = eh_tabuleiro_vazio(tab)
    letras_jog = jogador_letras(jog)
    num_letras = len(letras_jog)
    
    if primeira_jogada:
        print(f"Jogada {nivel}: P")
        return False
    
    if nivel == 'FACIL':
        n = 100
    elif nivel == 'MEDIO':
        n = 50
    else:
        n = 10
    
    padroes, casas, direcoes = gera_todos_padroes(tab, num_letras)
    
    padroes_selecionados = padroes[::n]
    casas_selecionadas = casas[::n]
    direcoes_selecionadas = direcoes[::n]
    
    melhor_palavra = ''
    melhor_pontuacao = 0
    melhor_casa = None
    melhor_direcao = None
    
    for i in range(len(padroes_selecionados)):
        padrao = padroes_selecionados[i]
        casa = casas_selecionadas[i]
        direcao = direcoes_selecionadas[i]
        
        palavra, pontuacao = procura_palavra_padrao(vocab, padrao, letras_jog, 0)
        
        if palavra and pontuacao > melhor_pontuacao:
            melhor_palavra = palavra
            melhor_pontuacao = pontuacao
            melhor_casa = casa
            melhor_direcao = direcao
    
    if melhor_palavra:
        lin = obtem_lin(melhor_casa)
        col = obtem_col(melhor_casa)
        
        print(f"Jogada {nivel}: J {lin} {col} {melhor_direcao} {melhor_palavra}")
        
        soma_pontos(jog, melhor_pontuacao)
        
        for i, letra in enumerate(melhor_palavra):
            if melhor_direcao == 'H':
                casa_atual = incrementa_casa(melhor_casa, 'H', i)
            else:
                casa_atual = incrementa_casa(melhor_casa, 'V', i)
            
            if obtem_letra(tab, casa_atual) == '.':
                usa_letra(jog, letra)
        
        insere_palavra(tab, melhor_casa, melhor_direcao, melhor_palavra)
        
        num_letras_atuais = len(jogador_letras(jog))
        num_distribuir = min(TAMANHO_MAO - num_letras_atuais, len(pilha))
        distribui_letras(jog, pilha, num_distribuir)
        
        return True
    
    if len(pilha) >= 7:
        print(f"Jogada {nivel}: T {' '.join(letras_jog)}")
        
        for letra in list(letras_jog):
            usa_letra(jog, letra)
        
        distribui_letras(jog, pilha, min(7, len(pilha)))
        
        return True
    
    print(f"Jogada {nivel}: P")
    return False


def scrabble2(jog: tuple, nome_fich: str, seed: int) -> tuple:
    """
    Função principal que permite jogar um jogo completo de Scrabble2 de dois 
    a quatro jogadores. A função recebe um tuplo com nomes dos jogadores humanos 
    (cadeia de caracteres não vazia) e o nível dos jogadores agentes (cadeia de 
    caracteres a começar por '@' seguido do nível) na ordem em que jogam, um 
    inteiro positivo representando o estado inicial do gerador pseudo-aleatório, 
    e devolve um tuplo com a pontuação final obtida pelos jogadores em ordem.
    
    O jogo começa baralhando o saco de letras e distribuindo o conjunto de 7 letras 
    a cada um dos jogadores em ordem. O jogo desenrola-se depois conforme as regras 
    e como mostrado no exemplo a seguir. O jogo termina quando todos os jogadores 
    passam ou quando um jogador fica sem letras e o saco estiver esgotado. A função 
    deve verificar a validade dos seus argumentos, gerando um erro com a mensagem 
    'scrabble2: argumentos inválidos'.
    """
    # Validação de argumentos
    if not isinstance(jog, tuple) or not isinstance(nome_fich, str) or not isinstance(seed, int):
        raise ValueError('scrabble2: argumentos inválidos')
    
    if len(jog) < 2 or len(jog) > 4:
        raise ValueError('scrabble2: argumentos inválidos')
    
    if seed <= 0:
        raise ValueError('scrabble2: argumentos inválidos')
    
    # Cria jogadores
    jogadores = []
    for info in jog:
        if not isinstance(info, str) or not info:
            raise ValueError('scrabble2: argumentos inválidos')
        
        if info.startswith('@'):
            nivel = info[1:]
            if nivel not in ('MEDIO', 'DIFICIL', 'FACIL'):
                raise ValueError('scrabble2: argumentos inválidos')
            jogadores.append(cria_agente(nivel))
        else:
            jogadores.append(cria_humano(info))
    
    # Carrega vocabulário
    vocab = ficheiro_para_vocabulario(nome_fich)
    
    # Baralha saco e distribui letras iniciais
    pilha = baralha_saco(seed)
    
    for jogador in jogadores:
        distribui_letras(jogador, pilha, TAMANHO_MAO)
    
    # Inicializa tabuleiro
    tab = cria_tabuleiro()
    
    print("Bem-vindo ao SCRABBLE2.")
    print(tabuleiro_para_str(tab))
    
    for jogador in jogadores:
        print(jogador_para_str(jogador))
    
    # Loop principal do jogo
    passes_consecutivos = 0
    num_jogadores = len(jogadores)
    
    while passes_consecutivos < num_jogadores:
        for jogador in jogadores:
            # Verifica condição de término
            if len(jogador_letras(jogador)) == 0 and len(pilha) == 0:
                passes_consecutivos = num_jogadores
                break
            
            # Processa jogada
            if eh_humano(jogador):
                jogou = jogada_humano(tab, jogador, vocab, pilha)
            else:
                jogou = jogada_agente(tab, jogador, vocab, pilha)
            
            if jogou:
                passes_consecutivos = 0
                print(tabuleiro_para_str(tab))
                for j in jogadores:
                    print(jogador_para_str(j))
            else:
                passes_consecutivos += 1
                if passes_consecutivos < num_jogadores:
                    print(tabuleiro_para_str(tab))
                    for j in jogadores:
                        print(jogador_para_str(j))
            
            if passes_consecutivos >= num_jogadores:
                break
    
    # Devolve pontuações finais
    return tuple(jogador_pontos(j) for j in jogadores)