import pytest 
import sys
import testes_lab as fp  # <--- Change the name projectoFP to the file name with your project


class TestPublicCasa:

    def test_1(self):
        with pytest.raises(ValueError) as excinfo:
            fp.cria_casa(-1, 12) 
        assert "cria_casa: argumentos inválidos" == str(excinfo.value)

    def test_2(self):
        c1 = fp.cria_casa(1, 2)
        c2 = fp.cria_casa(12, 15)
        assert not fp.casas_iguais(c1, c2)
        
    def test_3(self):
        c2 = fp.cria_casa(12, 15)
        assert fp.casa_para_str(c2) == '(12,15)'
    
    def test_4(self):
        c1 = fp.cria_casa(1, 2)
        assert fp.casas_iguais(c1, fp.str_para_casa('(1,2)'))
           
    def test_5(self):
        c1 = fp.cria_casa(1, 2)
        assert fp.casa_para_str(fp.incrementa_casa(c1, 'H', 2)) == '(1,4)'
        
    def test_6(self):
        c2 = fp.cria_casa(12, 15)
        assert fp.casas_iguais(c2, fp.incrementa_casa(c2, 'H', 1))


class TestPublicJogador:
    def test_1(self):
        jog1 = fp.cria_humano('Maria')
        jog2 = fp.cria_agente('FACIL')
        assert not fp.jogadores_iguais(jog1, jog2)
        
    def test_2(self):
        jog1 = fp.cria_humano('Maria')
        _ = fp.recebe_letra(jog1, 'A')
        letras = ['A', 'B', 'C', 'A', 'D']
        _ = fp.distribui_letras(jog1, letras, 3)
        assert letras == ['A', 'B'] and fp.jogador_para_str(fp.soma_pontos(jog1, 17)) == 'Maria ( 17): A A C D'
        
        
    def test_3(self):
        jog1 = fp.cria_humano('Maria')
        jog2 = fp.cria_agente('FACIL')
        _ = fp.recebe_letra(jog1, 'A')
        letras = ['A', 'B', 'C', 'A', 'D']
        _ = fp.distribui_letras(jog1, letras, 3)
        _ = fp.soma_pontos(jog1, 17)
        assert fp.jogador_para_str(fp.distribui_letras(jog2, letras, 10)) == 'BOT(FACIL) (  0): A B'
        
    def test_4(self):
        with pytest.raises(ValueError) as excinfo:
            fp.cria_agente('NIGHTMARE') 
        assert "cria_agente: argumento inválido" == str(excinfo.value)


class TestPublicVocabulario:
    def test_1(self):
        vocab = fp.cria_vocabulario(('AULA', 'CAO', 'ASA', 'CEGO', 'CEGA', 'CONE', 'COÇA', 'VACA', 'CASA'))
        assert fp.obtem_palavras(vocab, 4, 'C') == (('CEGA', 8), ('CEGO', 8), ('COÇA', 7), ('CONE', 7), ('CASA', 5))
        
    def test_2(self):
        vocab = fp.cria_vocabulario(('AULA', 'CAO', 'ASA', 'CEGO', 'CEGA', 'CONE', 'COÇA', 'VACA', 'CASA'))
        assert fp.vocabulario_para_str(vocab) == 'ASA\nCAO\nAULA\nCEGA\nCEGO\nCOÇA\nCONE\nCASA\nVACA'
        
    def test_3(self):
        vocab = fp.cria_vocabulario(('AULA', 'CAO', 'ASA', 'CEGO', 'CEGA', 'CONE', 'COÇA', 'VACA', 'CASA'))
        assert fp.testa_palavra_padrao(vocab, 'CASA', 'C.SA', 'BCA') and \
                    not fp.testa_palavra_padrao(vocab, 'BOLA', '.OLA', 'BCA')  and \
                        not fp.testa_palavra_padrao(vocab, 'CASA', 'CA.A', 'BCA')
                        
                    
    def test_4(self):
        vocab = fp.cria_vocabulario(('AULA', 'CAO', 'ASA', 'CEGO', 'CEGA', 'CONE', 'COÇA', 'VACA', 'CASA'))
        assert fp.procura_palavra_padrao(vocab, '.A.A', 'CCVVA', 0) == ('VACA', 8)
    
    def test_5(self):
        vocab = fp.cria_vocabulario(('AULA', 'CAO', 'ASA', 'CEGO', 'CEGA', 'CONE', 'COÇA', 'VACA', 'CASA'))
        assert fp.procura_palavra_padrao(vocab, '.A.A', 'CCVVA', 8) == ('VACA', 8)
        
    def test_6(self):
        vocab = fp.cria_vocabulario(('AULA', 'CAO', 'ASA', 'CEGO', 'CEGA', 'CONE', 'COÇA', 'VACA', 'CASA'))
        assert fp.procura_palavra_padrao(vocab, '.A.A', 'CCVVA', 9) == ('', 0)
        
    def test_7(self):
        content ='Asa\nAuLa\ncao\nCAsa\nINCONSTITUCIONALISSIMAMENTE\nCOME\nvacA'
        with open('vocab_tmp.txt', 'w') as file:
            file.write(content)
        assert fp.vocabulario_para_str(fp.ficheiro_para_vocabulario('vocab_tmp.txt')) == 'ASA\nCAO\nAULA\nCASA\nCOME\nVACA'

    def test_8(self):
        with pytest.raises(ValueError) as excinfo:
            vocab = fp.cria_vocabulario(('asa', 'AULA', 'CAO', 'CASA', 'COME', 'VACA'))
        assert "cria_vocabulario: argumento inválido" == str(excinfo.value)

    def test_9(self):
        vocab = fp.cria_vocabulario(('AULA', 'CAO', 'ASA', 'CEGO', 'CEGA', 'CONE', 'COÇA', 'VACA', 'CASA'))
        assert fp.obtem_pontos(vocab, 'CASA') == 5
        
        

class TestPublicTabuleiro:
    def test_1(self):
        tab = fp.cria_tabuleiro()
        c1, c2 = fp.cria_casa(8,6), fp.cria_casa(6,8)
        tab = fp.insere_letra(tab, c1, 'A')
        tab = fp.insere_letra(tab, c2, 'B')
        
        assert (fp.obtem_letra(tab, c1),  fp.obtem_letra(tab, c2)) == ('A', 'B')
        
    def test_2(self):
        tab = fp.cria_tabuleiro()
        tab = fp.insere_palavra(tab, fp.cria_casa(8,3), 'H', 'COMPUTADOR')
        
        assert fp.obtem_padrao(tab, fp.cria_casa(8,10), fp.cria_casa(8,12)) == 'DOR'
        
    def test_3(self):
        tab = fp.cria_tabuleiro()
        tab = fp.insere_palavra(tab, fp.cria_casa(8,3), 'H', 'COMPUTADOR')
        
        assert fp.obtem_padrao(tab, fp.cria_casa(7,5), fp.cria_casa(10,5)) == '.M..'
        
        
    def test_4(self):
        tab = fp.cria_tabuleiro()
        stab = \
            '''                       1 1 1 1 1 1
     1 2 3 4 5 6 7 8 9 0 1 2 3 4 5
   +-------------------------------+
 1 | . . . . . . . . . . . . . . . |
 2 | . . . . . . . . . . . . . . . |
 3 | . . . . . . . . . . . . . . . |
 4 | . . . . . . . . . . . . . . . |
 5 | . . . . . . . . . . . . . . . |
 6 | . . . . . . . . . . . . . . . |
 7 | . . . . . . . . . . . . . . . |
 8 | . . . . . . . . . . . . . . . |
 9 | . . . . . . . . . . . . . . . |
10 | . . . . . . . . . . . . . . . |
11 | . . . . . . . . . . . . . . . |
12 | . . . . . . . . . . . . . . . |
13 | . . . . . . . . . . . . . . . |
14 | . . . . . . . . . . . . . . . |
15 | . . . . . . . . . . . . . . . |
   +-------------------------------+'''
        assert fp.tabuleiro_para_str(tab) == stab
       
    def test_5(self):
        tab = fp.cria_tabuleiro()
        fp.insere_palavra(tab, fp.cria_casa(8,1), 'H', 'FUNDAMENTOS')
        fp.insere_palavra(tab, fp.cria_casa(8,4), 'V', 'DA')
        fp.insere_palavra(tab, fp.cria_casa(2,6), 'V', 'PROGRAMAÇAO')
        stab = \
            '''                       1 1 1 1 1 1
     1 2 3 4 5 6 7 8 9 0 1 2 3 4 5
   +-------------------------------+
 1 | . . . . . . . . . . . . . . . |
 2 | . . . . . P . . . . . . . . . |
 3 | . . . . . R . . . . . . . . . |
 4 | . . . . . O . . . . . . . . . |
 5 | . . . . . G . . . . . . . . . |
 6 | . . . . . R . . . . . . . . . |
 7 | . . . . . A . . . . . . . . . |
 8 | F U N D A M E N T O S . . . . |
 9 | . . . A . A . . . . . . . . . |
10 | . . . . . Ç . . . . . . . . . |
11 | . . . . . A . . . . . . . . . |
12 | . . . . . O . . . . . . . . . |
13 | . . . . . . . . . . . . . . . |
14 | . . . . . . . . . . . . . . . |
15 | . . . . . . . . . . . . . . . |
   +-------------------------------+'''
        assert fp.tabuleiro_para_str(tab) == stab 
        
    def test_6(self):
        tab = fp.cria_tabuleiro()
        fp.insere_palavra(tab, fp.cria_casa(8,1), 'H', 'FUNDAMENTOS')
        fp.insere_palavra(tab, fp.cria_casa(8,4), 'V', 'DA')
        fp.insere_palavra(tab, fp.cria_casa(2,6), 'V', 'PROGRAMAÇAO')
        pat, _ = fp.obtem_subpadroes(tab, fp.cria_casa(1,6), fp.cria_casa(15,6), 4)
        assert pat == ('.PROGRAMAÇAO...', '.PROGRAMAÇAO..', '.PROGRAMAÇAO.', '.PROGRAMAÇAO', 'PROGRAMAÇAO...', 'PROGRAMAÇAO..', 'PROGRAMAÇAO.')

    def test_8(self):
        tab = fp.cria_tabuleiro()
        fp.insere_palavra(tab, fp.cria_casa(8,1), 'H', 'FUNDAMENTOS')
        fp.insere_palavra(tab, fp.cria_casa(8,4), 'V', 'DA')
        fp.insere_palavra(tab, fp.cria_casa(2,6), 'V', 'PROGRAMAÇAO')
        pat, _ = fp.obtem_subpadroes(tab, fp.cria_casa(1,6), fp.cria_casa(15,6), 3)
        assert pat == ('.PROGRAMAÇAO..', '.PROGRAMAÇAO.', '.PROGRAMAÇAO', 'PROGRAMAÇAO...', 'PROGRAMAÇAO..', 'PROGRAMAÇAO.')


    def test_7(self):
        tab = fp.cria_tabuleiro()
        fp.insere_palavra(tab, fp.cria_casa(8,1), 'H', 'FUNDAMENTOS')
        fp.insere_palavra(tab, fp.cria_casa(8,4), 'V', 'DA')
        fp.insere_palavra(tab, fp.cria_casa(2,6), 'V', 'PROGRAMAÇAO')
        _, cas = fp.obtem_subpadroes(tab, fp.cria_casa(1,6), fp.cria_casa(15,6), 4)
        assert tuple(fp.casa_para_str(c) for c in cas) == \
            ('(1,6)', '(1,6)', '(1,6)', '(1,6)', '(2,6)', '(2,6)', '(2,6)')
        
    def test_9(self):
        tab = fp.cria_tabuleiro()
        fp.insere_palavra(tab, fp.cria_casa(8,1), 'H', 'FUNDAMENTOS')
        fp.insere_palavra(tab, fp.cria_casa(8,4), 'V', 'DA')
        fp.insere_palavra(tab, fp.cria_casa(2,6), 'V', 'PROGRAMAÇAO')
        pat, cas, dir = fp.gera_todos_padroes(tab,7)
        assert (len(pat), len(cas), len(dir)) == (680, 680, 680)
        
    def test_10(self):
        tab = fp.cria_tabuleiro()
        fp.insere_palavra(tab, fp.cria_casa(8,1), 'H', 'FUNDAMENTOS')
        fp.insere_palavra(tab, fp.cria_casa(8,4), 'V', 'DA')
        fp.insere_palavra(tab, fp.cria_casa(2,6), 'V', 'PROGRAMAÇAO')
        pat, _, _ = fp.gera_todos_padroes(tab,7)
        assert  pat[::100] == ('.....P..', '....G..', '...A', '...O...', '....N...', '.PROGRAMAÇAO.', '.T..')
        
   
    def test_11(self):
        tab = fp.cria_tabuleiro()
        fp.insere_palavra(tab, fp.cria_casa(8,1), 'H', 'FUNDAMENTOS')
        fp.insere_palavra(tab, fp.cria_casa(8,4), 'V', 'DA')
        fp.insere_palavra(tab, fp.cria_casa(2,6), 'V', 'PROGRAMAÇAO')
        pat, cas, dir = fp.gera_todos_padroes(tab,7)
        assert tuple(fp.casa_para_str(c) for c in cas[::100]) == \
            ('(2,1)', '(5,2)', '(9,1)', '(12,3)', '(4,3)', '(1,6)', '(7,9)')
        
    def test_12(self):
        tab = fp.cria_tabuleiro()
        fp.insere_palavra(tab, fp.cria_casa(8,1), 'H', 'FUNDAMENTOS')
        fp.insere_palavra(tab, fp.cria_casa(8,4), 'V', 'DA')
        fp.insere_palavra(tab, fp.cria_casa(2,6), 'V', 'PROGRAMAÇAO')
        pat, cas, dir = fp.gera_todos_padroes(tab,7)
        assert dir[::100] == ('H', 'H', 'H', 'H', 'V', 'V', 'V')
  
class TestBaralhaSaco:
    def test_1(self):
        saco = fp.baralha_saco(9)
        assert saco == ['S', 'N', 'A', 'J', 'U', 'T', 'S', 'U', 'M', 'C', 'I', 'V', 'L', 'M', 'A', 'U', 'E', 'R', 'Z', 'U', 'N', 'E', 'L', 'I', 'R', 'E', 'D', 'L', 'A', 'A', 'I', 'S', 'X', 'U', 'D', 'L', 'Q', 'T', 'R', 'A', 'M', 'I', 'F', 'O', 'I', 'B', 'U', 'O', 'S', 'D', 'P', 'H', 'E', 'H', 'I', 'N', 'B', 'T', 'D', 'E', 'S', 'A', 'R', 'P', 'I', 'M', 'I', 'A', 'R', 'C', 'O', 'M', 'O', 'E', 'M', 'F', 'E', 'A', 'O', 'L', 'G', 'O', 'T', 'B', 'E', 'P', 'G', 'S', 'S', 'I', 'C', 'T', 'Ç', 'E', 'C', 'R', 'P', 'E', 'A', 'V', 'O', 'J', 'A', 'S', 'Ç', 'N', 'A', 'A', 'A', 'O', 'D', 'U', 'E', 'I', 'O', 'A', 'O']
    
    def test_2(self):
        saco = fp.baralha_saco(10)
        assert saco == ['T', 'O', 'L', 'I', 'O', 'C', 'G', 'H', 'S', 'O', 'E', 'O', 'I', 'U', 'O', 'D', 'I', 'O', 'Ç', 'S', 'L', 'D', 'E', 'R', 'E', 'N', 'M', 'T', 'E', 'B', 'L', 'B', 'A', 'I', 'X', 'R', 'E', 'R', 'D', 'V', 'T', 'T', 'I', 'F', 'A', 'F', 'C', 'A', 'U', 'N', 'E', 'R', 'I', 'S', 'A', 'E', 'L', 'A', 'M', 'P', 'U', 'R', 'Z', 'A', 'O', 'E', 'P', 'M', 'D', 'U', 'M', 'A', 'C', 'Ç', 'A', 'U', 'A', 'U', 'I', 'E', 'A', 'A', 'P', 'J', 'R', 'T', 'B', 'U', 'S', 'D', 'E', 'O', 'L', 'M', 'A', 'H', 'A', 'N', 'C', 'V', 'Q', 'O', 'S', 'I', 'N', 'O', 'E', 'P', 'S', 'J', 'M', 'I', 'A', 'S', 'G', 'S', 'I']
        
class TestJogadaHumano:
    def test_1(self):
        tab = fp.cria_tabuleiro()
        jog1 = fp.cria_humano('Maria')
        for let in 'AAUOTXF': _ = fp.recebe_letra(jog1, let)
        pilha = ['S', 'B', 'P', 'E', 'C', 'E', 'E', 'S', 'J', 'D', 'I']
        vocab = fp.cria_vocabulario(('TOFU', 'LUTA', 'USA'))
        
        res, text = False, 'Jogada Maria: Jogada Maria: '
        assert jogada_humano_offline(tab, jog1, vocab, pilha, "olà\nP\n") == (res, text)

    def test_2(self):
        tab = fp.cria_tabuleiro()
        jog1 = fp.cria_humano('Maria')
        for let in 'AAUOTXF': _ = fp.recebe_letra(jog1, let)
        pilha = ['S', 'B', 'P', 'E', 'C', 'E', 'E', 'S', 'J', 'D', 'I']
        vocab = fp.cria_vocabulario(('TOFU', 'LUTA', 'USA'))
        
        res, text = True, 'Jogada Maria: '
        assert jogada_humano_offline(tab, jog1, vocab, pilha, "T X A\n") == (res, text) and \
            fp.jogador_para_str(jog1) == 'Maria (  0): A D F I O T U' and \
                pilha == ['S', 'B', 'P', 'E', 'C', 'E', 'E', 'S', 'J']

    def test_3(self):
        tab = fp.cria_tabuleiro()
        jog1 = fp.cria_humano('Maria')
        for let in 'AAUOTXF': _ = fp.recebe_letra(jog1, let)
        pilha = ['S', 'B', 'P', 'E', 'C', 'E', 'E', 'S', 'J', 'D', 'I']
        vocab = fp.cria_vocabulario(('TOFU', 'LUTA', 'USA'))
        
        jogada_humano_offline(tab, jog1, vocab, pilha, "T X A\n")
        res, text = True, 'Jogada Maria: Jogada Maria: '
        assert jogada_humano_offline(tab, jog1, vocab, pilha, "J 7 8 V LUTA\nJ 7 8 V TOFU\n") == (res, text) and \
            fp.jogador_para_str(jog1) == 'Maria (  7): A D E E I J S' 

    def test_4(self):
        tab = fp.cria_tabuleiro()
        jog1 = fp.cria_humano('Maria')
        for let in 'AAUOTXF': _ = fp.recebe_letra(jog1, let)
        pilha = ['S', 'B', 'P', 'E', 'C', 'E', 'E', 'S', 'J', 'D', 'I']
        vocab = fp.cria_vocabulario(('TOFU', 'LUTA', 'USA'))
        
        jogada_humano_offline(tab, jog1, vocab, pilha, "T X A\n")
        jogada_humano_offline(tab, jog1, vocab, pilha, "J 7 8 V LUTA\nJ 7 8 V TOFU\n")
        
        res, text = True, 'Jogada Maria: Jogada Maria: '
        assert jogada_humano_offline(tab, jog1, vocab, pilha, "Maria: J 10 6 H SEU\nJ 10 8 H USA\n") == (res, text) and \
            fp.jogador_para_str(jog1) == 'Maria ( 10): C D E E E I J' and \
                pilha == ['S', 'B', 'P']
        
    def test_5(self):
        tab = fp.cria_tabuleiro()
        jog1 = fp.cria_humano('Maria')
        for let in 'AAUOTXF': _ = fp.recebe_letra(jog1, let)
        pilha = ['S', 'B', 'P', 'E', 'C', 'E', 'E', 'S', 'J', 'D', 'I']
        vocab = fp.cria_vocabulario(('TOFU', 'LUTA', 'USA'))
        
        jogada_humano_offline(tab, jog1, vocab, pilha, "T X A\n")
        jogada_humano_offline(tab, jog1, vocab, pilha, "J 7 8 V LUTA\nJ 7 8 V TOFU\n")
        jogada_humano_offline(tab, jog1, vocab, pilha, "Maria: J 10 6 H SEU\nJ 10 8 H USA\n")
        
        stab = """                       1 1 1 1 1 1
     1 2 3 4 5 6 7 8 9 0 1 2 3 4 5
   +-------------------------------+
 1 | . . . . . . . . . . . . . . . |
 2 | . . . . . . . . . . . . . . . |
 3 | . . . . . . . . . . . . . . . |
 4 | . . . . . . . . . . . . . . . |
 5 | . . . . . . . . . . . . . . . |
 6 | . . . . . . . . . . . . . . . |
 7 | . . . . . . . T . . . . . . . |
 8 | . . . . . . . O . . . . . . . |
 9 | . . . . . . . F . . . . . . . |
10 | . . . . . . . U S A . . . . . |
11 | . . . . . . . . . . . . . . . |
12 | . . . . . . . . . . . . . . . |
13 | . . . . . . . . . . . . . . . |
14 | . . . . . . . . . . . . . . . |
15 | . . . . . . . . . . . . . . . |
   +-------------------------------+"""
   
        res, text = True, 'Jogada Maria: Jogada Maria: '
        assert fp.tabuleiro_para_str(tab) == stab
        
     
                
class TestJogadaAgenteFacil:
    def test_1(self):
        tab = fp.cria_tabuleiro()
        pilha = ['N', 'R', 'R', 'S', 'S', 'B', 'A', 'L', 'V', 'M', 'D', 
             'A', 'E', 'R', 'E', 'M', 'I', 'O', 'G', 'O']
        bot = fp.cria_agente('FACIL')
        vocab = fp.ficheiro_para_vocabulario('vocab25k.txt')
        _ = fp.distribui_letras(bot, pilha, 7)
        res, text = False, "Jogada FACIL: P\n" 
        assert jogada_agente_output(tab, bot, vocab, pilha) == (res, text)
            
    def test_2(self):
        tab = fp.cria_tabuleiro()
        pilha = ['N', 'R', 'R', 'S', 'S', 'B', 'A', 'L', 'V', 'M', 'D', 
             'A', 'E', 'R', 'E', 'M', 'I', 'O', 'G', 'O']
        bot = fp.cria_agente('FACIL')
        vocab = fp.ficheiro_para_vocabulario('vocab25k.txt')
        _ = fp.distribui_letras(bot, pilha, 7)
        
        _ = fp.insere_palavra(tab, fp.cria_casa(8,1), 'H', 'FUNDAMENTOS')
        _ = fp.insere_palavra(tab, fp.cria_casa(8,4), 'V', 'DA')
        _ = fp.insere_palavra(tab, fp.cria_casa(2,6), 'V', 'PROGRAMAÇAO')

        res, text = True, "Jogada FACIL: J 9 1 H GERA\n" 
        assert jogada_agente_output(tab, bot, vocab, pilha) == (res, text)
    
    def test_3(self):
        tab = fp.cria_tabuleiro()
        pilha = ['N', 'R', 'R', 'S', 'S', 'B', 'A', 'L', 'V', 'M', 'D', 
             'A', 'E', 'R', 'E', 'M', 'I', 'O', 'G', 'O']
        bot = fp.cria_agente('FACIL')
        vocab = fp.ficheiro_para_vocabulario('vocab25k.txt')
        _ = fp.distribui_letras(bot, pilha, 7)
        
        _ = fp.insere_palavra(tab, fp.cria_casa(8,1), 'H', 'FUNDAMENTOS')
        _ = fp.insere_palavra(tab, fp.cria_casa(8,4), 'V', 'DA')
        _ = fp.insere_palavra(tab, fp.cria_casa(2,6), 'V', 'PROGRAMAÇAO')

        _ = jogada_agente_output(tab, bot, vocab, pilha)
        
        res, text = True, "Jogada FACIL: T A D E I M O O\n" 
        assert jogada_agente_output(tab, bot, vocab, pilha) == (res, text)
    
    def test_4(self):
        tab = fp.cria_tabuleiro()
        pilha = ['N', 'R', 'R', 'S', 'S', 'B', 'A', 'L', 'V', 'M', 'D', 
             'A', 'E', 'R', 'E', 'M', 'I', 'O', 'G', 'O']
        bot = fp.cria_agente('FACIL')
        vocab = fp.ficheiro_para_vocabulario('vocab25k.txt')
        _ = fp.distribui_letras(bot, pilha, 7)
        
        _ = fp.insere_palavra(tab, fp.cria_casa(8,1), 'H', 'FUNDAMENTOS')
        _ = fp.insere_palavra(tab, fp.cria_casa(8,4), 'V', 'DA')
        _ = fp.insere_palavra(tab, fp.cria_casa(2,6), 'V', 'PROGRAMAÇAO')

        _ = jogada_agente_output(tab, bot, vocab, pilha)
        _ = jogada_agente_output(tab, bot, vocab, pilha)
        
        res, text = False, "Jogada FACIL: P\n" 
        assert jogada_agente_output(tab, bot, vocab, pilha) == (res, text)
    
    
    def test_5(self):
        tab = fp.cria_tabuleiro()
        pilha = ['N', 'R', 'R', 'S', 'S', 'B', 'A', 'L', 'V', 'M', 'D', 
             'A', 'E', 'R', 'E', 'M', 'I', 'O', 'G', 'O']
        bot = fp.cria_agente('FACIL')
        vocab = fp.ficheiro_para_vocabulario('vocab25k.txt')
        _ = fp.distribui_letras(bot, pilha, 7)
        
        _ = fp.insere_palavra(tab, fp.cria_casa(8,1), 'H', 'FUNDAMENTOS')
        _ = fp.insere_palavra(tab, fp.cria_casa(8,4), 'V', 'DA')
        _ = fp.insere_palavra(tab, fp.cria_casa(2,6), 'V', 'PROGRAMAÇAO')

        _ = jogada_agente_output(tab, bot, vocab, pilha)
        _ = jogada_agente_output(tab, bot, vocab, pilha)
        _ = jogada_agente_output(tab, bot, vocab, pilha)
        
        assert fp.jogador_para_str(bot) == 'BOT(FACIL) (  7): A B L M S S V' and \
            pilha == ['N', 'R', 'R']
                      
        
class TestJogadaAgenteMedio:
    def test_1(self):
        tab = fp.cria_tabuleiro()
        pilha = ['N', 'R', 'R', 'S', 'S', 'B', 'A', 'L', 'V', 'M', 'D', 
             'A', 'E', 'R', 'E', 'M', 'I', 'O', 'G', 'O']
        bot = fp.cria_agente('MEDIO')
        vocab = fp.ficheiro_para_vocabulario('vocab25k.txt')
        _ = fp.distribui_letras(bot, pilha, 7)
        res, text = False, "Jogada MEDIO: P\n" 
        assert jogada_agente_output(tab, bot, vocab, pilha) == (res, text)
            
    def test_2(self):
        tab = fp.cria_tabuleiro()
        pilha = ['N', 'R', 'R', 'S', 'S', 'B', 'A', 'L', 'V', 'M', 'D', 
             'A', 'E', 'R', 'E', 'M', 'I', 'O', 'G', 'O']
        bot = fp.cria_agente('MEDIO')
        vocab = fp.ficheiro_para_vocabulario('vocab25k.txt')
        _ = fp.distribui_letras(bot, pilha, 7)
        
        _ = fp.insere_palavra(tab, fp.cria_casa(8,1), 'H', 'FUNDAMENTOS')
        _ = fp.insere_palavra(tab, fp.cria_casa(8,4), 'V', 'DA')
        _ = fp.insere_palavra(tab, fp.cria_casa(2,6), 'V', 'PROGRAMAÇAO')

        res, text = True, "Jogada MEDIO: J 9 1 H GERA\n" 
        assert jogada_agente_output(tab, bot, vocab, pilha) == (res, text)
    
    def test_3(self):
        tab = fp.cria_tabuleiro()
        pilha = ['N', 'R', 'R', 'S', 'S', 'B', 'A', 'L', 'V', 'M', 'D', 
             'A', 'E', 'R', 'E', 'M', 'I', 'O', 'G', 'O']
        bot = fp.cria_agente('MEDIO')
        vocab = fp.ficheiro_para_vocabulario('vocab25k.txt')
        _ = fp.distribui_letras(bot, pilha, 7)
        
        _ = fp.insere_palavra(tab, fp.cria_casa(8,1), 'H', 'FUNDAMENTOS')
        _ = fp.insere_palavra(tab, fp.cria_casa(8,4), 'V', 'DA')
        _ = fp.insere_palavra(tab, fp.cria_casa(2,6), 'V', 'PROGRAMAÇAO')

        _ = jogada_agente_output(tab, bot, vocab, pilha)
        
        res, text = True, "Jogada MEDIO: J 8 8 V NODOA\n" 
        assert jogada_agente_output(tab, bot, vocab, pilha) == (res, text)
    
    def test_4(self):
        tab = fp.cria_tabuleiro()
        pilha = ['N', 'R', 'R', 'S', 'S', 'B', 'A', 'L', 'V', 'M', 'D', 
             'A', 'E', 'R', 'E', 'M', 'I', 'O', 'G', 'O']
        bot = fp.cria_agente('MEDIO')
        vocab = fp.ficheiro_para_vocabulario('vocab25k.txt')
        _ = fp.distribui_letras(bot, pilha, 7)
        
        _ = fp.insere_palavra(tab, fp.cria_casa(8,1), 'H', 'FUNDAMENTOS')
        _ = fp.insere_palavra(tab, fp.cria_casa(8,4), 'V', 'DA')
        _ = fp.insere_palavra(tab, fp.cria_casa(2,6), 'V', 'PROGRAMAÇAO')

        _ = jogada_agente_output(tab, bot, vocab, pilha)
        _ = jogada_agente_output(tab, bot, vocab, pilha)
        
        res, text = True, "Jogada MEDIO: J 5 4 V AVIDA\n" 
        assert jogada_agente_output(tab, bot, vocab, pilha) == (res, text)
    
    def test_5(self):
        tab = fp.cria_tabuleiro()
        pilha = ['N', 'R', 'R', 'S', 'S', 'B', 'A', 'L', 'V', 'M', 'D', 
             'A', 'E', 'R', 'E', 'M', 'I', 'O', 'G', 'O']
        bot = fp.cria_agente('MEDIO')
        vocab = fp.ficheiro_para_vocabulario('vocab25k.txt')
        _ = fp.distribui_letras(bot, pilha, 7)
        
        _ = fp.insere_palavra(tab, fp.cria_casa(8,1), 'H', 'FUNDAMENTOS')
        _ = fp.insere_palavra(tab, fp.cria_casa(8,4), 'V', 'DA')
        _ = fp.insere_palavra(tab, fp.cria_casa(2,6), 'V', 'PROGRAMAÇAO')

        _ = jogada_agente_output(tab, bot, vocab, pilha)
        _ = jogada_agente_output(tab, bot, vocab, pilha)
        _ = jogada_agente_output(tab, bot, vocab, pilha)
        
        res, text = True, "Jogada MEDIO: J 5 1 H BELA\n" 
        assert jogada_agente_output(tab, bot, vocab, pilha) == (res, text)
    
    
    def test_6(self):
        tab = fp.cria_tabuleiro()
        pilha = ['N', 'R', 'R', 'S', 'S', 'B', 'A', 'L', 'V', 'M', 'D', 
             'A', 'E', 'R', 'E', 'M', 'I', 'O', 'G', 'O']
        bot = fp.cria_agente('MEDIO')
        vocab = fp.ficheiro_para_vocabulario('vocab25k.txt')
        _ = fp.distribui_letras(bot, pilha, 7)
        
        _ = fp.insere_palavra(tab, fp.cria_casa(8,1), 'H', 'FUNDAMENTOS')
        _ = fp.insere_palavra(tab, fp.cria_casa(8,4), 'V', 'DA')
        _ = fp.insere_palavra(tab, fp.cria_casa(2,6), 'V', 'PROGRAMAÇAO')

        _ = jogada_agente_output(tab, bot, vocab, pilha)
        _ = jogada_agente_output(tab, bot, vocab, pilha)
        _ = jogada_agente_output(tab, bot, vocab, pilha)
        _ = jogada_agente_output(tab, bot, vocab, pilha)
        
        res, text = True, "Jogada MEDIO: J 12 5 H MORA\n" 
        assert jogada_agente_output(tab, bot, vocab, pilha) == (res, text)
    
    def test_7(self):
        tab = fp.cria_tabuleiro()
        pilha = ['N', 'R', 'R', 'S', 'S', 'B', 'A', 'L', 'V', 'M', 'D', 
             'A', 'E', 'R', 'E', 'M', 'I', 'O', 'G', 'O']
        bot = fp.cria_agente('MEDIO')
        vocab = fp.ficheiro_para_vocabulario('vocab25k.txt')
        _ = fp.distribui_letras(bot, pilha, 7)
        
        _ = fp.insere_palavra(tab, fp.cria_casa(8,1), 'H', 'FUNDAMENTOS')
        _ = fp.insere_palavra(tab, fp.cria_casa(8,4), 'V', 'DA')
        _ = fp.insere_palavra(tab, fp.cria_casa(2,6), 'V', 'PROGRAMAÇAO')

        _ = jogada_agente_output(tab, bot, vocab, pilha)
        _ = jogada_agente_output(tab, bot, vocab, pilha)
        _ = jogada_agente_output(tab, bot, vocab, pilha)
        _ = jogada_agente_output(tab, bot, vocab, pilha)
        _ = jogada_agente_output(tab, bot, vocab, pilha)
        
        res, text = False, "Jogada MEDIO: P\n"
        
        assert jogada_agente_output(tab, bot, vocab, pilha) == (res, text) and \
            fp.jogador_para_str(bot) == 'BOT(MEDIO) ( 35): M N R S S' and \
            pilha == []
                     

class TestJogadaAgenteDificil:
    def test_1(self):
        tab = fp.cria_tabuleiro()
        pilha = ['N', 'R', 'R', 'S', 'S', 'B', 'A', 'L', 'V', 'M', 'D', 
             'A', 'E', 'R', 'E', 'M', 'I', 'O', 'G', 'O']
        bot = fp.cria_agente('DIFICIL')
        vocab = fp.ficheiro_para_vocabulario('vocab25k.txt')
        _ = fp.distribui_letras(bot, pilha, 7)
        res, text = False, "Jogada DIFICIL: P\n" 
        assert jogada_agente_output(tab, bot, vocab, pilha) == (res, text)
            
    def test_2(self):
        tab = fp.cria_tabuleiro()
        pilha = ['N', 'R', 'R', 'S', 'S', 'B', 'A', 'L', 'V', 'M', 'D', 
             'A', 'E', 'R', 'E', 'M', 'I', 'O', 'G', 'O']
        bot = fp.cria_agente('DIFICIL')
        vocab = fp.ficheiro_para_vocabulario('vocab25k.txt')
        _ = fp.distribui_letras(bot, pilha, 7)
        
        _ = fp.insere_palavra(tab, fp.cria_casa(8,1), 'H', 'FUNDAMENTOS')
        _ = fp.insere_palavra(tab, fp.cria_casa(8,4), 'V', 'DA')
        _ = fp.insere_palavra(tab, fp.cria_casa(2,6), 'V', 'PROGRAMAÇAO')

        res, text = True, "Jogada DIFICIL: J 6 3 V IGNOREM\n" 
        assert jogada_agente_output(tab, bot, vocab, pilha) == (res, text)
    
    def test_3(self):
        tab = fp.cria_tabuleiro()
        pilha = ['N', 'R', 'R', 'S', 'S', 'B', 'A', 'L', 'V', 'M', 'D', 
             'A', 'E', 'R', 'E', 'M', 'I', 'O', 'G', 'O']
        bot = fp.cria_agente('DIFICIL')
        vocab = fp.ficheiro_para_vocabulario('vocab25k.txt')
        _ = fp.distribui_letras(bot, pilha, 7)
        
        _ = fp.insere_palavra(tab, fp.cria_casa(8,1), 'H', 'FUNDAMENTOS')
        _ = fp.insere_palavra(tab, fp.cria_casa(8,4), 'V', 'DA')
        _ = fp.insere_palavra(tab, fp.cria_casa(2,6), 'V', 'PROGRAMAÇAO')

        _ = jogada_agente_output(tab, bot, vocab, pilha)
        
        res, text = True, "Jogada DIFICIL: J 5 4 H LEGADO\n" 
        assert jogada_agente_output(tab, bot, vocab, pilha) == (res, text)
    
    def test_4(self):
        tab = fp.cria_tabuleiro()
        pilha = ['N', 'R', 'R', 'S', 'S', 'B', 'A', 'L', 'V', 'M', 'D', 
             'A', 'E', 'R', 'E', 'M', 'I', 'O', 'G', 'O']
        bot = fp.cria_agente('DIFICIL')
        vocab = fp.ficheiro_para_vocabulario('vocab25k.txt')
        _ = fp.distribui_letras(bot, pilha, 7)
        
        _ = fp.insere_palavra(tab, fp.cria_casa(8,1), 'H', 'FUNDAMENTOS')
        _ = fp.insere_palavra(tab, fp.cria_casa(8,4), 'V', 'DA')
        _ = fp.insere_palavra(tab, fp.cria_casa(2,6), 'V', 'PROGRAMAÇAO')

        _ = jogada_agente_output(tab, bot, vocab, pilha)
        _ = jogada_agente_output(tab, bot, vocab, pilha)
        
        res, text = True, "Jogada DIFICIL: J 4 2 H BRAVO\n" 
        assert jogada_agente_output(tab, bot, vocab, pilha) == (res, text)
    
    def test_5(self):
        tab = fp.cria_tabuleiro()
        pilha = ['N', 'R', 'R', 'S', 'S', 'B', 'A', 'L', 'V', 'M', 'D', 
             'A', 'E', 'R', 'E', 'M', 'I', 'O', 'G', 'O']
        bot = fp.cria_agente('DIFICIL')
        vocab = fp.ficheiro_para_vocabulario('vocab25k.txt')
        _ = fp.distribui_letras(bot, pilha, 7)
        
        _ = fp.insere_palavra(tab, fp.cria_casa(8,1), 'H', 'FUNDAMENTOS')
        _ = fp.insere_palavra(tab, fp.cria_casa(8,4), 'V', 'DA')
        _ = fp.insere_palavra(tab, fp.cria_casa(2,6), 'V', 'PROGRAMAÇAO')

        _ = jogada_agente_output(tab, bot, vocab, pilha)
        _ = jogada_agente_output(tab, bot, vocab, pilha)
        _ = jogada_agente_output(tab, bot, vocab, pilha)
        
        res, text = True, "Jogada DIFICIL: J 7 10 V SONS\n" 
        assert jogada_agente_output(tab, bot, vocab, pilha) == (res, text)
    
    
    def test_6(self):
        tab = fp.cria_tabuleiro()
        pilha = ['N', 'R', 'R', 'S', 'S', 'B', 'A', 'L', 'V', 'M', 'D', 
             'A', 'E', 'R', 'E', 'M', 'I', 'O', 'G', 'O']
        bot = fp.cria_agente('DIFICIL')
        vocab = fp.ficheiro_para_vocabulario('vocab25k.txt')
        _ = fp.distribui_letras(bot, pilha, 7)
        
        _ = fp.insere_palavra(tab, fp.cria_casa(8,1), 'H', 'FUNDAMENTOS')
        _ = fp.insere_palavra(tab, fp.cria_casa(8,4), 'V', 'DA')
        _ = fp.insere_palavra(tab, fp.cria_casa(2,6), 'V', 'PROGRAMAÇAO')

        _ = jogada_agente_output(tab, bot, vocab, pilha)
        _ = jogada_agente_output(tab, bot, vocab, pilha)
        _ = jogada_agente_output(tab, bot, vocab, pilha)
        _ = jogada_agente_output(tab, bot, vocab, pilha)
        
        res, text = True, "Jogada DIFICIL: J 6 2 H MIR\n" 
        assert jogada_agente_output(tab, bot, vocab, pilha) == (res, text)
    
    def test_7(self):
        tab = fp.cria_tabuleiro()
        pilha = ['N', 'R', 'R', 'S', 'S', 'B', 'A', 'L', 'V', 'M', 'D', 
             'A', 'E', 'R', 'E', 'M', 'I', 'O', 'G', 'O']
        bot = fp.cria_agente('DIFICIL')
        vocab = fp.ficheiro_para_vocabulario('vocab25k.txt')
        _ = fp.distribui_letras(bot, pilha, 7)
        
        _ = fp.insere_palavra(tab, fp.cria_casa(8,1), 'H', 'FUNDAMENTOS')
        _ = fp.insere_palavra(tab, fp.cria_casa(8,4), 'V', 'DA')
        _ = fp.insere_palavra(tab, fp.cria_casa(2,6), 'V', 'PROGRAMAÇAO')

        _ = jogada_agente_output(tab, bot, vocab, pilha)
        _ = jogada_agente_output(tab, bot, vocab, pilha)
        _ = jogada_agente_output(tab, bot, vocab, pilha)
        _ = jogada_agente_output(tab, bot, vocab, pilha)
        _ = jogada_agente_output(tab, bot, vocab, pilha)
        
        res, text = False, "Jogada DIFICIL: P\n"
        
        assert jogada_agente_output(tab, bot, vocab, pilha) == (res, text) and \
            fp.jogador_para_str(bot) == 'BOT(DIFICIL) ( 42):' and \
            pilha == []
            
class TestScrabble2:
    def test_1(self):
        jog = ('Maria', '@MEDIO', '@DIFICIL', )
        res = (75, 60, 93)
        assert scrabble2_offline(jog, 'vocab25k.txt',  32, JOGADA_PUBLIC_1) == (res, OUTPUT_PUBLIC_1) 
    
    def test_3(self):
        jog = ('Maria', 'João','Pedro', 'Rita')
        res = (35, 25, 24, 22)
        assert scrabble2_offline(jog, 'vocab25k.txt',  4, JOGADA_PUBLIC_2) == (res, OUTPUT_PUBLIC_2) 




### AUXILIAR CODE NECESSARY TO REPLACE STANDARD INPUT 
class ReplaceStdIn:
    def __init__(self, input_handle):
        self.input = input_handle.split('\n')
        self.line = 0

    def readline(self):
        if len(self.input) == self.line:
            return ''
        result = self.input[self.line]
        self.line += 1
        return result

class ReplaceStdOut:
    def __init__(self):
        self.output = ''

    def write(self, s):
        self.output += s
        return len(s)

    def flush(self):
        return 


def jogada_humano_offline(tabuleiro, jogador, vocab, pilha, input_jogo):
    oldstdin = sys.stdin
    sys.stdin = ReplaceStdIn(input_handle=input_jogo)
    
    oldstdout, newstdout = sys.stdout,  ReplaceStdOut()
    sys.stdout = newstdout

    try:
        res = fp.jogada_humano(tabuleiro, jogador, vocab, pilha)
        text = newstdout.output
        return res, text
    except ValueError as e:
        raise e
    finally:
        sys.stdin = oldstdin
        sys.stdout = oldstdout
        

def jogada_agente_output(tabuleiro, jogador, vocab, pilha):

    oldstdout, newstdout = sys.stdout,  ReplaceStdOut()
    sys.stdout = newstdout

    try:
        res = fp.jogada_agente(tabuleiro, jogador, vocab, pilha)
        text = newstdout.output
        return res, text
    except ValueError as e:
        raise e
    finally:
        sys.stdout = oldstdout
        

def scrabble2_offline(jogadores, vocab_file, seed, input_jogo):
    oldstdin = sys.stdin
    sys.stdin = ReplaceStdIn(input_handle=input_jogo)
    
    oldstdout, newstdout = sys.stdout,  ReplaceStdOut()
    sys.stdout = newstdout

    try:
        res = fp.scrabble2(jogadores, vocab_file, seed)
        text = newstdout.output
        return res, text
    except ValueError as e:
        raise e
    finally:
        sys.stdin = oldstdin
        sys.stdout = oldstdout


JOGADA_PUBLIC_1 = \
"""J 8 6 H MUDO
J 3 9 V RENOVOU
J 11 3 H CABEÇAS
T Ç P U
J 3 9 H REPETIU
J 4 9 H ESTUDO
J 14 5 H MISTER
J 9 11 H HAJA
J 6 7 H NAO
J 7 8 H BVL
T C D I I I L Q
P
P
"""

OUTPUT_PUBLIC_1 = \
"""Bem-vindo ao SCRABBLE2.
                       1 1 1 1 1 1
     1 2 3 4 5 6 7 8 9 0 1 2 3 4 5
   +-------------------------------+
 1 | . . . . . . . . . . . . . . . |
 2 | . . . . . . . . . . . . . . . |
 3 | . . . . . . . . . . . . . . . |
 4 | . . . . . . . . . . . . . . . |
 5 | . . . . . . . . . . . . . . . |
 6 | . . . . . . . . . . . . . . . |
 7 | . . . . . . . . . . . . . . . |
 8 | . . . . . . . . . . . . . . . |
 9 | . . . . . . . . . . . . . . . |
10 | . . . . . . . . . . . . . . . |
11 | . . . . . . . . . . . . . . . |
12 | . . . . . . . . . . . . . . . |
13 | . . . . . . . . . . . . . . . |
14 | . . . . . . . . . . . . . . . |
15 | . . . . . . . . . . . . . . . |
   +-------------------------------+
Maria (  0): B Ç D E M O U
BOT(MEDIO) (  0): A B I N O O V
BOT(DIFICIL) (  0): A A B C E I T
Jogada Maria:                        1 1 1 1 1 1
     1 2 3 4 5 6 7 8 9 0 1 2 3 4 5
   +-------------------------------+
 1 | . . . . . . . . . . . . . . . |
 2 | . . . . . . . . . . . . . . . |
 3 | . . . . . . . . . . . . . . . |
 4 | . . . . . . . . . . . . . . . |
 5 | . . . . . . . . . . . . . . . |
 6 | . . . . . . . . . . . . . . . |
 7 | . . . . . . . . . . . . . . . |
 8 | . . . . . M U D O . . . . . . |
 9 | . . . . . . . . . . . . . . . |
10 | . . . . . . . . . . . . . . . |
11 | . . . . . . . . . . . . . . . |
12 | . . . . . . . . . . . . . . . |
13 | . . . . . . . . . . . . . . . |
14 | . . . . . . . . . . . . . . . |
15 | . . . . . . . . . . . . . . . |
   +-------------------------------+
Maria (  5): A B Ç E R S U
BOT(MEDIO) (  0): A B I N O O V
BOT(DIFICIL) (  0): A A B C E I T
Jogada MEDIO: J 5 9 V NOVO
                       1 1 1 1 1 1
     1 2 3 4 5 6 7 8 9 0 1 2 3 4 5
   +-------------------------------+
 1 | . . . . . . . . . . . . . . . |
 2 | . . . . . . . . . . . . . . . |
 3 | . . . . . . . . . . . . . . . |
 4 | . . . . . . . . . . . . . . . |
 5 | . . . . . . . . N . . . . . . |
 6 | . . . . . . . . O . . . . . . |
 7 | . . . . . . . . V . . . . . . |
 8 | . . . . . M U D O . . . . . . |
 9 | . . . . . . . . . . . . . . . |
10 | . . . . . . . . . . . . . . . |
11 | . . . . . . . . . . . . . . . |
12 | . . . . . . . . . . . . . . . |
13 | . . . . . . . . . . . . . . . |
14 | . . . . . . . . . . . . . . . |
15 | . . . . . . . . . . . . . . . |
   +-------------------------------+
Maria (  5): A B Ç E R S U
BOT(MEDIO) (  9): A A B E I O O
BOT(DIFICIL) (  0): A A B C E I T
Jogada DIFICIL: J 6 8 V ABDICA
                       1 1 1 1 1 1
     1 2 3 4 5 6 7 8 9 0 1 2 3 4 5
   +-------------------------------+
 1 | . . . . . . . . . . . . . . . |
 2 | . . . . . . . . . . . . . . . |
 3 | . . . . . . . . . . . . . . . |
 4 | . . . . . . . . . . . . . . . |
 5 | . . . . . . . . N . . . . . . |
 6 | . . . . . . . A O . . . . . . |
 7 | . . . . . . . B V . . . . . . |
 8 | . . . . . M U D O . . . . . . |
 9 | . . . . . . . I . . . . . . . |
10 | . . . . . . . C . . . . . . . |
11 | . . . . . . . A . . . . . . . |
12 | . . . . . . . . . . . . . . . |
13 | . . . . . . . . . . . . . . . |
14 | . . . . . . . . . . . . . . . |
15 | . . . . . . . . . . . . . . . |
   +-------------------------------+
Maria (  5): A B Ç E R S U
BOT(MEDIO) (  9): A A B E I O O
BOT(DIFICIL) ( 10): A E M O O O T
Jogada Maria:                        1 1 1 1 1 1
     1 2 3 4 5 6 7 8 9 0 1 2 3 4 5
   +-------------------------------+
 1 | . . . . . . . . . . . . . . . |
 2 | . . . . . . . . . . . . . . . |
 3 | . . . . . . . . R . . . . . . |
 4 | . . . . . . . . E . . . . . . |
 5 | . . . . . . . . N . . . . . . |
 6 | . . . . . . . A O . . . . . . |
 7 | . . . . . . . B V . . . . . . |
 8 | . . . . . M U D O . . . . . . |
 9 | . . . . . . . I U . . . . . . |
10 | . . . . . . . C . . . . . . . |
11 | . . . . . . . A . . . . . . . |
12 | . . . . . . . . . . . . . . . |
13 | . . . . . . . . . . . . . . . |
14 | . . . . . . . . . . . . . . . |
15 | . . . . . . . . . . . . . . . |
   +-------------------------------+
Maria ( 17): A B C Ç E I S
BOT(MEDIO) (  9): A A B E I O O
BOT(DIFICIL) ( 10): A E M O O O T
Jogada MEDIO: J 5 9 H NBA
                       1 1 1 1 1 1
     1 2 3 4 5 6 7 8 9 0 1 2 3 4 5
   +-------------------------------+
 1 | . . . . . . . . . . . . . . . |
 2 | . . . . . . . . . . . . . . . |
 3 | . . . . . . . . R . . . . . . |
 4 | . . . . . . . . E . . . . . . |
 5 | . . . . . . . . N B A . . . . |
 6 | . . . . . . . A O . . . . . . |
 7 | . . . . . . . B V . . . . . . |
 8 | . . . . . M U D O . . . . . . |
 9 | . . . . . . . I U . . . . . . |
10 | . . . . . . . C . . . . . . . |
11 | . . . . . . . A . . . . . . . |
12 | . . . . . . . . . . . . . . . |
13 | . . . . . . . . . . . . . . . |
14 | . . . . . . . . . . . . . . . |
15 | . . . . . . . . . . . . . . . |
   +-------------------------------+
Maria ( 17): A B C Ç E I S
BOT(MEDIO) ( 16): A E E I O O S
BOT(DIFICIL) ( 10): A E M O O O T
Jogada DIFICIL: J 10 8 H COMETA
                       1 1 1 1 1 1
     1 2 3 4 5 6 7 8 9 0 1 2 3 4 5
   +-------------------------------+
 1 | . . . . . . . . . . . . . . . |
 2 | . . . . . . . . . . . . . . . |
 3 | . . . . . . . . R . . . . . . |
 4 | . . . . . . . . E . . . . . . |
 5 | . . . . . . . . N B A . . . . |
 6 | . . . . . . . A O . . . . . . |
 7 | . . . . . . . B V . . . . . . |
 8 | . . . . . M U D O . . . . . . |
 9 | . . . . . . . I U . . . . . . |
10 | . . . . . . . C O M E T A . . |
11 | . . . . . . . A . . . . . . . |
12 | . . . . . . . . . . . . . . . |
13 | . . . . . . . . . . . . . . . |
14 | . . . . . . . . . . . . . . . |
15 | . . . . . . . . . . . . . . . |
   +-------------------------------+
Maria ( 17): A B C Ç E I S
BOT(MEDIO) ( 16): A E E I O O S
BOT(DIFICIL) ( 17): F G H O O O T
Jogada Maria:                        1 1 1 1 1 1
     1 2 3 4 5 6 7 8 9 0 1 2 3 4 5
   +-------------------------------+
 1 | . . . . . . . . . . . . . . . |
 2 | . . . . . . . . . . . . . . . |
 3 | . . . . . . . . R . . . . . . |
 4 | . . . . . . . . E . . . . . . |
 5 | . . . . . . . . N B A . . . . |
 6 | . . . . . . . A O . . . . . . |
 7 | . . . . . . . B V . . . . . . |
 8 | . . . . . M U D O . . . . . . |
 9 | . . . . . . . I U . . . . . . |
10 | . . . . . . . C O M E T A . . |
11 | . . C A B E Ç A S . . . . . . |
12 | . . . . . . . . . . . . . . . |
13 | . . . . . . . . . . . . . . . |
14 | . . . . . . . . . . . . . . . |
15 | . . . . . . . . . . . . . . . |
   +-------------------------------+
Maria ( 29): Ç I P P T U U
BOT(MEDIO) ( 16): A E E I O O S
BOT(DIFICIL) ( 17): F G H O O O T
Jogada MEDIO: T A E E I O O S
                       1 1 1 1 1 1
     1 2 3 4 5 6 7 8 9 0 1 2 3 4 5
   +-------------------------------+
 1 | . . . . . . . . . . . . . . . |
 2 | . . . . . . . . . . . . . . . |
 3 | . . . . . . . . R . . . . . . |
 4 | . . . . . . . . E . . . . . . |
 5 | . . . . . . . . N B A . . . . |
 6 | . . . . . . . A O . . . . . . |
 7 | . . . . . . . B V . . . . . . |
 8 | . . . . . M U D O . . . . . . |
 9 | . . . . . . . I U . . . . . . |
10 | . . . . . . . C O M E T A . . |
11 | . . C A B E Ç A S . . . . . . |
12 | . . . . . . . . . . . . . . . |
13 | . . . . . . . . . . . . . . . |
14 | . . . . . . . . . . . . . . . |
15 | . . . . . . . . . . . . . . . |
   +-------------------------------+
Maria ( 29): Ç I P P T U U
BOT(MEDIO) ( 16): A A E H L M P
BOT(DIFICIL) ( 17): F G H O O O T
Jogada DIFICIL: J 10 4 V FATO
                       1 1 1 1 1 1
     1 2 3 4 5 6 7 8 9 0 1 2 3 4 5
   +-------------------------------+
 1 | . . . . . . . . . . . . . . . |
 2 | . . . . . . . . . . . . . . . |
 3 | . . . . . . . . R . . . . . . |
 4 | . . . . . . . . E . . . . . . |
 5 | . . . . . . . . N B A . . . . |
 6 | . . . . . . . A O . . . . . . |
 7 | . . . . . . . B V . . . . . . |
 8 | . . . . . M U D O . . . . . . |
 9 | . . . . . . . I U . . . . . . |
10 | . . . F . . . C O M E T A . . |
11 | . . C A B E Ç A S . . . . . . |
12 | . . . T . . . . . . . . . . . |
13 | . . . O . . . . . . . . . . . |
14 | . . . . . . . . . . . . . . . |
15 | . . . . . . . . . . . . . . . |
   +-------------------------------+
Maria ( 29): Ç I P P T U U
BOT(MEDIO) ( 16): A A E H L M P
BOT(DIFICIL) ( 24): E G H O O O R
Jogada Maria:                        1 1 1 1 1 1
     1 2 3 4 5 6 7 8 9 0 1 2 3 4 5
   +-------------------------------+
 1 | . . . . . . . . . . . . . . . |
 2 | . . . . . . . . . . . . . . . |
 3 | . . . . . . . . R . . . . . . |
 4 | . . . . . . . . E . . . . . . |
 5 | . . . . . . . . N B A . . . . |
 6 | . . . . . . . A O . . . . . . |
 7 | . . . . . . . B V . . . . . . |
 8 | . . . . . M U D O . . . . . . |
 9 | . . . . . . . I U . . . . . . |
10 | . . . F . . . C O M E T A . . |
11 | . . C A B E Ç A S . . . . . . |
12 | . . . T . . . . . . . . . . . |
13 | . . . O . . . . . . . . . . . |
14 | . . . . . . . . . . . . . . . |
15 | . . . . . . . . . . . . . . . |
   +-------------------------------+
Maria ( 29): E E I P T T U
BOT(MEDIO) ( 16): A A E H L M P
BOT(DIFICIL) ( 24): E G H O O O R
Jogada MEDIO: J 12 4 H TALHA
                       1 1 1 1 1 1
     1 2 3 4 5 6 7 8 9 0 1 2 3 4 5
   +-------------------------------+
 1 | . . . . . . . . . . . . . . . |
 2 | . . . . . . . . . . . . . . . |
 3 | . . . . . . . . R . . . . . . |
 4 | . . . . . . . . E . . . . . . |
 5 | . . . . . . . . N B A . . . . |
 6 | . . . . . . . A O . . . . . . |
 7 | . . . . . . . B V . . . . . . |
 8 | . . . . . M U D O . . . . . . |
 9 | . . . . . . . I U . . . . . . |
10 | . . . F . . . C O M E T A . . |
11 | . . C A B E Ç A S . . . . . . |
12 | . . . T A L H A . . . . . . . |
13 | . . . O . . . . . . . . . . . |
14 | . . . . . . . . . . . . . . . |
15 | . . . . . . . . . . . . . . . |
   +-------------------------------+
Maria ( 29): E E I P T T U
BOT(MEDIO) ( 25): A E E I M P U
BOT(DIFICIL) ( 24): E G H O O O R
Jogada DIFICIL: J 9 11 V HERGE
                       1 1 1 1 1 1
     1 2 3 4 5 6 7 8 9 0 1 2 3 4 5
   +-------------------------------+
 1 | . . . . . . . . . . . . . . . |
 2 | . . . . . . . . . . . . . . . |
 3 | . . . . . . . . R . . . . . . |
 4 | . . . . . . . . E . . . . . . |
 5 | . . . . . . . . N B A . . . . |
 6 | . . . . . . . A O . . . . . . |
 7 | . . . . . . . B V . . . . . . |
 8 | . . . . . M U D O . . . . . . |
 9 | . . . . . . . I U . H . . . . |
10 | . . . F . . . C O M E T A . . |
11 | . . C A B E Ç A S . R . . . . |
12 | . . . T A L H A . . G . . . . |
13 | . . . O . . . . . . E . . . . |
14 | . . . . . . . . . . . . . . . |
15 | . . . . . . . . . . . . . . . |
   +-------------------------------+
Maria ( 29): E E I P T T U
BOT(MEDIO) ( 25): A E E I M P U
BOT(DIFICIL) ( 35): G L N O O O S
Jogada Maria:                        1 1 1 1 1 1
     1 2 3 4 5 6 7 8 9 0 1 2 3 4 5
   +-------------------------------+
 1 | . . . . . . . . . . . . . . . |
 2 | . . . . . . . . . . . . . . . |
 3 | . . . . . . . . R E P E T I U |
 4 | . . . . . . . . E . . . . . . |
 5 | . . . . . . . . N B A . . . . |
 6 | . . . . . . . A O . . . . . . |
 7 | . . . . . . . B V . . . . . . |
 8 | . . . . . M U D O . . . . . . |
 9 | . . . . . . . I U . H . . . . |
10 | . . . F . . . C O M E T A . . |
11 | . . C A B E Ç A S . R . . . . |
12 | . . . T A L H A . . G . . . . |
13 | . . . O . . . . . . E . . . . |
14 | . . . . . . . . . . . . . . . |
15 | . . . . . . . . . . . . . . . |
   +-------------------------------+
Maria ( 37): D M O S T T U
BOT(MEDIO) ( 25): A E E I M P U
BOT(DIFICIL) ( 35): G L N O O O S
Jogada MEDIO: J 9 12 V ATUM
                       1 1 1 1 1 1
     1 2 3 4 5 6 7 8 9 0 1 2 3 4 5
   +-------------------------------+
 1 | . . . . . . . . . . . . . . . |
 2 | . . . . . . . . . . . . . . . |
 3 | . . . . . . . . R E P E T I U |
 4 | . . . . . . . . E . . . . . . |
 5 | . . . . . . . . N B A . . . . |
 6 | . . . . . . . A O . . . . . . |
 7 | . . . . . . . B V . . . . . . |
 8 | . . . . . M U D O . . . . . . |
 9 | . . . . . . . I U . H A . . . |
10 | . . . F . . . C O M E T A . . |
11 | . . C A B E Ç A S . R U . . . |
12 | . . . T A L H A . . G M . . . |
13 | . . . O . . . . . . E . . . . |
14 | . . . . . . . . . . . . . . . |
15 | . . . . . . . . . . . . . . . |
   +-------------------------------+
Maria ( 37): D M O S T T U
BOT(MEDIO) ( 29): A E E I P R X
BOT(DIFICIL) ( 35): G L N O O O S
Jogada DIFICIL: J 10 2 H GNFL
                       1 1 1 1 1 1
     1 2 3 4 5 6 7 8 9 0 1 2 3 4 5
   +-------------------------------+
 1 | . . . . . . . . . . . . . . . |
 2 | . . . . . . . . . . . . . . . |
 3 | . . . . . . . . R E P E T I U |
 4 | . . . . . . . . E . . . . . . |
 5 | . . . . . . . . N B A . . . . |
 6 | . . . . . . . A O . . . . . . |
 7 | . . . . . . . B V . . . . . . |
 8 | . . . . . M U D O . . . . . . |
 9 | . . . . . . . I U . H A . . . |
10 | . G N F L . . C O M E T A . . |
11 | . . C A B E Ç A S . R U . . . |
12 | . . . T A L H A . . G M . . . |
13 | . . . O . . . . . . E . . . . |
14 | . . . . . . . . . . . . . . . |
15 | . . . . . . . . . . . . . . . |
   +-------------------------------+
Maria ( 37): D M O S T T U
BOT(MEDIO) ( 29): A E E I P R X
BOT(DIFICIL) ( 48): A D O O O R S
Jogada Maria:                        1 1 1 1 1 1
     1 2 3 4 5 6 7 8 9 0 1 2 3 4 5
   +-------------------------------+
 1 | . . . . . . . . . . . . . . . |
 2 | . . . . . . . . . . . . . . . |
 3 | . . . . . . . . R E P E T I U |
 4 | . . . . . . . . E S T U D O . |
 5 | . . . . . . . . N B A . . . . |
 6 | . . . . . . . A O . . . . . . |
 7 | . . . . . . . B V . . . . . . |
 8 | . . . . . M U D O . . . . . . |
 9 | . . . . . . . I U . H A . . . |
10 | . G N F L . . C O M E T A . . |
11 | . . C A B E Ç A S . R U . . . |
12 | . . . T A L H A . . G M . . . |
13 | . . . O . . . . . . E . . . . |
14 | . . . . . . . . . . . . . . . |
15 | . . . . . . . . . . . . . . . |
   +-------------------------------+
Maria ( 44): E I I L M S T
BOT(MEDIO) ( 29): A E E I P R X
BOT(DIFICIL) ( 48): A D O O O R S
Jogada MEDIO: J 10 10 V MEXER
                       1 1 1 1 1 1
     1 2 3 4 5 6 7 8 9 0 1 2 3 4 5
   +-------------------------------+
 1 | . . . . . . . . . . . . . . . |
 2 | . . . . . . . . . . . . . . . |
 3 | . . . . . . . . R E P E T I U |
 4 | . . . . . . . . E S T U D O . |
 5 | . . . . . . . . N B A . . . . |
 6 | . . . . . . . A O . . . . . . |
 7 | . . . . . . . B V . . . . . . |
 8 | . . . . . M U D O . . . . . . |
 9 | . . . . . . . I U . H A . . . |
10 | . G N F L . . C O M E T A . . |
11 | . . C A B E Ç A S E R U . . . |
12 | . . . T A L H A . X G M . . . |
13 | . . . O . . . . . E E . . . . |
14 | . . . . . . . . . R . . . . . |
15 | . . . . . . . . . . . . . . . |
   +-------------------------------+
Maria ( 44): E I I L M S T
BOT(MEDIO) ( 41): A C I P S S V
BOT(DIFICIL) ( 48): A D O O O R S
Jogada DIFICIL: J 7 2 V DROGAS
                       1 1 1 1 1 1
     1 2 3 4 5 6 7 8 9 0 1 2 3 4 5
   +-------------------------------+
 1 | . . . . . . . . . . . . . . . |
 2 | . . . . . . . . . . . . . . . |
 3 | . . . . . . . . R E P E T I U |
 4 | . . . . . . . . E S T U D O . |
 5 | . . . . . . . . N B A . . . . |
 6 | . . . . . . . A O . . . . . . |
 7 | . D . . . . . B V . . . . . . |
 8 | . R . . . M U D O . . . . . . |
 9 | . O . . . . . I U . H A . . . |
10 | . G N F L . . C O M E T A . . |
11 | . A C A B E Ç A S E R U . . . |
12 | . S . T A L H A . X G M . . . |
13 | . . . O . . . . . E E . . . . |
14 | . . . . . . . . . R . . . . . |
15 | . . . . . . . . . . . . . . . |
   +-------------------------------+
Maria ( 44): E I I L M S T
BOT(MEDIO) ( 41): A C I P S S V
BOT(DIFICIL) ( 58): D J L M M O O
Jogada Maria:                        1 1 1 1 1 1
     1 2 3 4 5 6 7 8 9 0 1 2 3 4 5
   +-------------------------------+
 1 | . . . . . . . . . . . . . . . |
 2 | . . . . . . . . . . . . . . . |
 3 | . . . . . . . . R E P E T I U |
 4 | . . . . . . . . E S T U D O . |
 5 | . . . . . . . . N B A . . . . |
 6 | . . . . . . . A O . . . . . . |
 7 | . D . . . . . B V . . . . . . |
 8 | . R . . . M U D O . . . . . . |
 9 | . O . . . . . I U . H A . . . |
10 | . G N F L . . C O M E T A . . |
11 | . A C A B E Ç A S E R U . . . |
12 | . S . T A L H A . X G M . . . |
13 | . . . O . . . . . E E . . . . |
14 | . . . . M I S T E R . . . . . |
15 | . . . . . . . . . . . . . . . |
   +-------------------------------+
Maria ( 50): A D I J L N Q
BOT(MEDIO) ( 41): A C I P S S V
BOT(DIFICIL) ( 58): D J L M M O O
Jogada MEDIO: J 2 14 V PIO
                       1 1 1 1 1 1
     1 2 3 4 5 6 7 8 9 0 1 2 3 4 5
   +-------------------------------+
 1 | . . . . . . . . . . . . . . . |
 2 | . . . . . . . . . . . . . P . |
 3 | . . . . . . . . R E P E T I U |
 4 | . . . . . . . . E S T U D O . |
 5 | . . . . . . . . N B A . . . . |
 6 | . . . . . . . A O . . . . . . |
 7 | . D . . . . . B V . . . . . . |
 8 | . R . . . M U D O . . . . . . |
 9 | . O . . . . . I U . H A . . . |
10 | . G N F L . . C O M E T A . . |
11 | . A C A B E Ç A S E R U . . . |
12 | . S . T A L H A . X G M . . . |
13 | . . . O . . . . . E E . . . . |
14 | . . . . M I S T E R . . . . . |
15 | . . . . . . . . . . . . . . . |
   +-------------------------------+
Maria ( 50): A D I J L N Q
BOT(MEDIO) ( 45): A C I S S V Z
BOT(DIFICIL) ( 58): D J L M M O O
Jogada DIFICIL: J 2 12 H OLP
                       1 1 1 1 1 1
     1 2 3 4 5 6 7 8 9 0 1 2 3 4 5
   +-------------------------------+
 1 | . . . . . . . . . . . . . . . |
 2 | . . . . . . . . . . . O L P . |
 3 | . . . . . . . . R E P E T I U |
 4 | . . . . . . . . E S T U D O . |
 5 | . . . . . . . . N B A . . . . |
 6 | . . . . . . . A O . . . . . . |
 7 | . D . . . . . B V . . . . . . |
 8 | . R . . . M U D O . . . . . . |
 9 | . O . . . . . I U . H A . . . |
10 | . G N F L . . C O M E T A . . |
11 | . A C A B E Ç A S E R U . . . |
12 | . S . T A L H A . X G M . . . |
13 | . . . O . . . . . E E . . . . |
14 | . . . . M I S T E R . . . . . |
15 | . . . . . . . . . . . . . . . |
   +-------------------------------+
Maria ( 50): A D I J L N Q
BOT(MEDIO) ( 45): A C I S S V Z
BOT(DIFICIL) ( 63): D F J M M O U
Jogada Maria:                        1 1 1 1 1 1
     1 2 3 4 5 6 7 8 9 0 1 2 3 4 5
   +-------------------------------+
 1 | . . . . . . . . . . . . . . . |
 2 | . . . . . . . . . . . O L P . |
 3 | . . . . . . . . R E P E T I U |
 4 | . . . . . . . . E S T U D O . |
 5 | . . . . . . . . N B A . . . . |
 6 | . . . . . . . A O . . . . . . |
 7 | . D . . . . . B V . . . . . . |
 8 | . R . . . M U D O . . . . . . |
 9 | . O . . . . . I U . H A J A . |
10 | . G N F L . . C O M E T A . . |
11 | . A C A B E Ç A S E R U . . . |
12 | . S . T A L H A . X G M . . . |
13 | . . . O . . . . . E E . . . . |
14 | . . . . M I S T E R . . . . . |
15 | . . . . . . . . . . . . . . . |
   +-------------------------------+
Maria ( 61): C D I L L N Q
BOT(MEDIO) ( 45): A C I S S V Z
BOT(DIFICIL) ( 63): D F J M M O U
Jogada MEDIO: J 13 2 H AVOS
                       1 1 1 1 1 1
     1 2 3 4 5 6 7 8 9 0 1 2 3 4 5
   +-------------------------------+
 1 | . . . . . . . . . . . . . . . |
 2 | . . . . . . . . . . . O L P . |
 3 | . . . . . . . . R E P E T I U |
 4 | . . . . . . . . E S T U D O . |
 5 | . . . . . . . . N B A . . . . |
 6 | . . . . . . . A O . . . . . . |
 7 | . D . . . . . B V . . . . . . |
 8 | . R . . . M U D O . . . . . . |
 9 | . O . . . . . I U . H A J A . |
10 | . G N F L . . C O M E T A . . |
11 | . A C A B E Ç A S E R U . . . |
12 | . S . T A L H A . X G M . . . |
13 | . A V O S . . . . E E . . . . |
14 | . . . . M I S T E R . . . . . |
15 | . . . . . . . . . . . . . . . |
   +-------------------------------+
Maria ( 61): C D I L L N Q
BOT(MEDIO) ( 52): A C I R S S Z
BOT(DIFICIL) ( 63): D F J M M O U
Jogada DIFICIL: J 7 14 V FUA
                       1 1 1 1 1 1
     1 2 3 4 5 6 7 8 9 0 1 2 3 4 5
   +-------------------------------+
 1 | . . . . . . . . . . . . . . . |
 2 | . . . . . . . . . . . O L P . |
 3 | . . . . . . . . R E P E T I U |
 4 | . . . . . . . . E S T U D O . |
 5 | . . . . . . . . N B A . . . . |
 6 | . . . . . . . A O . . . . . . |
 7 | . D . . . . . B V . . . . F . |
 8 | . R . . . M U D O . . . . U . |
 9 | . O . . . . . I U . H A J A . |
10 | . G N F L . . C O M E T A . . |
11 | . A C A B E Ç A S E R U . . . |
12 | . S . T A L H A . X G M . . . |
13 | . A V O S . . . . E E . . . . |
14 | . . . . M I S T E R . . . . . |
15 | . . . . . . . . . . . . . . . |
   +-------------------------------+
Maria ( 61): C D I L L N Q
BOT(MEDIO) ( 52): A C I R S S Z
BOT(DIFICIL) ( 69): A D I J M M O
Jogada Maria:                        1 1 1 1 1 1
     1 2 3 4 5 6 7 8 9 0 1 2 3 4 5
   +-------------------------------+
 1 | . . . . . . . . . . . . . . . |
 2 | . . . . . . . . . . . O L P . |
 3 | . . . . . . . . R E P E T I U |
 4 | . . . . . . . . E S T U D O . |
 5 | . . . . . . . . N B A . . . . |
 6 | . . . . . . N A O . . . . . . |
 7 | . D . . . . . B V . . . . F . |
 8 | . R . . . M U D O . . . . U . |
 9 | . O . . . . . I U . H A J A . |
10 | . G N F L . . C O M E T A . . |
11 | . A C A B E Ç A S E R U . . . |
12 | . S . T A L H A . X G M . . . |
13 | . A V O S . . . . E E . . . . |
14 | . . . . M I S T E R . . . . . |
15 | . . . . . . . . . . . . . . . |
   +-------------------------------+
Maria ( 66): C D I I L L Q
BOT(MEDIO) ( 52): A C I R S S Z
BOT(DIFICIL) ( 69): A D I J M M O
Jogada MEDIO: J 8 1 H AR
                       1 1 1 1 1 1
     1 2 3 4 5 6 7 8 9 0 1 2 3 4 5
   +-------------------------------+
 1 | . . . . . . . . . . . . . . . |
 2 | . . . . . . . . . . . O L P . |
 3 | . . . . . . . . R E P E T I U |
 4 | . . . . . . . . E S T U D O . |
 5 | . . . . . . . . N B A . . . . |
 6 | . . . . . . N A O . . . . . . |
 7 | . D . . . . . B V . . . . F . |
 8 | A R . . . M U D O . . . . U . |
 9 | . O . . . . . I U . H A J A . |
10 | . G N F L . . C O M E T A . . |
11 | . A C A B E Ç A S E R U . . . |
12 | . S . T A L H A . X G M . . . |
13 | . A V O S . . . . E E . . . . |
14 | . . . . M I S T E R . . . . . |
15 | . . . . . . . . . . . . . . . |
   +-------------------------------+
Maria ( 66): C D I I L L Q
BOT(MEDIO) ( 54): C I P R S S Z
BOT(DIFICIL) ( 69): A D I J M M O
Jogada DIFICIL: J 14 5 H MISTERIO
                       1 1 1 1 1 1
     1 2 3 4 5 6 7 8 9 0 1 2 3 4 5
   +-------------------------------+
 1 | . . . . . . . . . . . . . . . |
 2 | . . . . . . . . . . . O L P . |
 3 | . . . . . . . . R E P E T I U |
 4 | . . . . . . . . E S T U D O . |
 5 | . . . . . . . . N B A . . . . |
 6 | . . . . . . N A O . . . . . . |
 7 | . D . . . . . B V . . . . F . |
 8 | A R . . . M U D O . . . . U . |
 9 | . O . . . . . I U . H A J A . |
10 | . G N F L . . C O M E T A . . |
11 | . A C A B E Ç A S E R U . . . |
12 | . S . T A L H A . X G M . . . |
13 | . A V O S . . . . E E . . . . |
14 | . . . . M I S T E R I O . . . |
15 | . . . . . . . . . . . . . . . |
   +-------------------------------+
Maria ( 66): C D I I L L Q
BOT(MEDIO) ( 54): C I P R S S Z
BOT(DIFICIL) ( 77): A D I J M M N
Jogada Maria:                        1 1 1 1 1 1
     1 2 3 4 5 6 7 8 9 0 1 2 3 4 5
   +-------------------------------+
 1 | . . . . . . . . . . . . . . . |
 2 | . . . . . . . . . . . O L P . |
 3 | . . . . . . . . R E P E T I U |
 4 | . . . . . . . . E S T U D O . |
 5 | . . . . . . . . N B A . . . . |
 6 | . . . . . . N A O . . . . . . |
 7 | . D . . . . . B V L . . . F . |
 8 | A R . . . M U D O . . . . U . |
 9 | . O . . . . . I U . H A J A . |
10 | . G N F L . . C O M E T A . . |
11 | . A C A B E Ç A S E R U . . . |
12 | . S . T A L H A . X G M . . . |
13 | . A V O S . . . . E E . . . . |
14 | . . . . M I S T E R I O . . . |
15 | . . . . . . . . . . . . . . . |
   +-------------------------------+
Maria ( 75): C D I I I L Q
BOT(MEDIO) ( 54): C I P R S S Z
BOT(DIFICIL) ( 77): A D I J M M N
Jogada MEDIO: J 2 15 V IU
                       1 1 1 1 1 1
     1 2 3 4 5 6 7 8 9 0 1 2 3 4 5
   +-------------------------------+
 1 | . . . . . . . . . . . . . . . |
 2 | . . . . . . . . . . . O L P I |
 3 | . . . . . . . . R E P E T I U |
 4 | . . . . . . . . E S T U D O . |
 5 | . . . . . . . . N B A . . . . |
 6 | . . . . . . N A O . . . . . . |
 7 | . D . . . . . B V L . . . F . |
 8 | A R . . . M U D O . . . . U . |
 9 | . O . . . . . I U . H A J A . |
10 | . G N F L . . C O M E T A . . |
11 | . A C A B E Ç A S E R U . . . |
12 | . S . T A L H A . X G M . . . |
13 | . A V O S . . . . E E . . . . |
14 | . . . . M I S T E R I O . . . |
15 | . . . . . . . . . . . . . . . |
   +-------------------------------+
Maria ( 75): C D I I I L Q
BOT(MEDIO) ( 56): C P R R S S Z
BOT(DIFICIL) ( 77): A D I J M M N
Jogada DIFICIL: J 4 7 V JAN
                       1 1 1 1 1 1
     1 2 3 4 5 6 7 8 9 0 1 2 3 4 5
   +-------------------------------+
 1 | . . . . . . . . . . . . . . . |
 2 | . . . . . . . . . . . O L P I |
 3 | . . . . . . . . R E P E T I U |
 4 | . . . . . . J . E S T U D O . |
 5 | . . . . . . A . N B A . . . . |
 6 | . . . . . . N A O . . . . . . |
 7 | . D . . . . . B V L . . . F . |
 8 | A R . . . M U D O . . . . U . |
 9 | . O . . . . . I U . H A J A . |
10 | . G N F L . . C O M E T A . . |
11 | . A C A B E Ç A S E R U . . . |
12 | . S . T A L H A . X G M . . . |
13 | . A V O S . . . . E E . . . . |
14 | . . . . M I S T E R I O . . . |
15 | . . . . . . . . . . . . . . . |
   +-------------------------------+
Maria ( 75): C D I I I L Q
BOT(MEDIO) ( 56): C P R R S S Z
BOT(DIFICIL) ( 86): D I M M N
Jogada Maria: Jogada Maria:                        1 1 1 1 1 1
     1 2 3 4 5 6 7 8 9 0 1 2 3 4 5
   +-------------------------------+
 1 | . . . . . . . . . . . . . . . |
 2 | . . . . . . . . . . . O L P I |
 3 | . . . . . . . . R E P E T I U |
 4 | . . . . . . J . E S T U D O . |
 5 | . . . . . . A . N B A . . . . |
 6 | . . . . . . N A O . . . . . . |
 7 | . D . . . . . B V L . . . F . |
 8 | A R . . . M U D O . . . . U . |
 9 | . O . . . . . I U . H A J A . |
10 | . G N F L . . C O M E T A . . |
11 | . A C A B E Ç A S E R U . . . |
12 | . S . T A L H A . X G M . . . |
13 | . A V O S . . . . E E . . . . |
14 | . . . . M I S T E R I O . . . |
15 | . . . . . . . . . . . . . . . |
   +-------------------------------+
Maria ( 75): C D I I I L Q
BOT(MEDIO) ( 56): C P R R S S Z
BOT(DIFICIL) ( 86): D I M M N
Jogada MEDIO: J 8 1 H ARC
                       1 1 1 1 1 1
     1 2 3 4 5 6 7 8 9 0 1 2 3 4 5
   +-------------------------------+
 1 | . . . . . . . . . . . . . . . |
 2 | . . . . . . . . . . . O L P I |
 3 | . . . . . . . . R E P E T I U |
 4 | . . . . . . J . E S T U D O . |
 5 | . . . . . . A . N B A . . . . |
 6 | . . . . . . N A O . . . . . . |
 7 | . D . . . . . B V L . . . F . |
 8 | A R C . . M U D O . . . . U . |
 9 | . O . . . . . I U . H A J A . |
10 | . G N F L . . C O M E T A . . |
11 | . A C A B E Ç A S E R U . . . |
12 | . S . T A L H A . X G M . . . |
13 | . A V O S . . . . E E . . . . |
14 | . . . . M I S T E R I O . . . |
15 | . . . . . . . . . . . . . . . |
   +-------------------------------+
Maria ( 75): C D I I I L Q
BOT(MEDIO) ( 60): P R R S S Z
BOT(DIFICIL) ( 86): D I M M N
Jogada DIFICIL: J 5 4 H DINA
                       1 1 1 1 1 1
     1 2 3 4 5 6 7 8 9 0 1 2 3 4 5
   +-------------------------------+
 1 | . . . . . . . . . . . . . . . |
 2 | . . . . . . . . . . . O L P I |
 3 | . . . . . . . . R E P E T I U |
 4 | . . . . . . J . E S T U D O . |
 5 | . . . D I N A . N B A . . . . |
 6 | . . . . . . N A O . . . . . . |
 7 | . D . . . . . B V L . . . F . |
 8 | A R C . . M U D O . . . . U . |
 9 | . O . . . . . I U . H A J A . |
10 | . G N F L . . C O M E T A . . |
11 | . A C A B E Ç A S E R U . . . |
12 | . S . T A L H A . X G M . . . |
13 | . A V O S . . . . E E . . . . |
14 | . . . . M I S T E R I O . . . |
15 | . . . . . . . . . . . . . . . |
   +-------------------------------+
Maria ( 75): C D I I I L Q
BOT(MEDIO) ( 60): P R R S S Z
BOT(DIFICIL) ( 93): M M
Jogada Maria:                        1 1 1 1 1 1
     1 2 3 4 5 6 7 8 9 0 1 2 3 4 5
   +-------------------------------+
 1 | . . . . . . . . . . . . . . . |
 2 | . . . . . . . . . . . O L P I |
 3 | . . . . . . . . R E P E T I U |
 4 | . . . . . . J . E S T U D O . |
 5 | . . . D I N A . N B A . . . . |
 6 | . . . . . . N A O . . . . . . |
 7 | . D . . . . . B V L . . . F . |
 8 | A R C . . M U D O . . . . U . |
 9 | . O . . . . . I U . H A J A . |
10 | . G N F L . . C O M E T A . . |
11 | . A C A B E Ç A S E R U . . . |
12 | . S . T A L H A . X G M . . . |
13 | . A V O S . . . . E E . . . . |
14 | . . . . M I S T E R I O . . . |
15 | . . . . . . . . . . . . . . . |
   +-------------------------------+
Maria ( 75): C D I I I L Q
BOT(MEDIO) ( 60): P R R S S Z
BOT(DIFICIL) ( 93): M M
Jogada MEDIO: P
                       1 1 1 1 1 1
     1 2 3 4 5 6 7 8 9 0 1 2 3 4 5
   +-------------------------------+
 1 | . . . . . . . . . . . . . . . |
 2 | . . . . . . . . . . . O L P I |
 3 | . . . . . . . . R E P E T I U |
 4 | . . . . . . J . E S T U D O . |
 5 | . . . D I N A . N B A . . . . |
 6 | . . . . . . N A O . . . . . . |
 7 | . D . . . . . B V L . . . F . |
 8 | A R C . . M U D O . . . . U . |
 9 | . O . . . . . I U . H A J A . |
10 | . G N F L . . C O M E T A . . |
11 | . A C A B E Ç A S E R U . . . |
12 | . S . T A L H A . X G M . . . |
13 | . A V O S . . . . E E . . . . |
14 | . . . . M I S T E R I O . . . |
15 | . . . . . . . . . . . . . . . |
   +-------------------------------+
Maria ( 75): C D I I I L Q
BOT(MEDIO) ( 60): P R R S S Z
BOT(DIFICIL) ( 93): M M
Jogada DIFICIL: P
"""

JOGADA_PUBLIC_2 = \
"""J 8 4 H URINA
J 5 8 V FINAL
J 9 2 H ENDEMOL
J 3 7 V HERMANOS
J 7 5 H APANHAR
T Ç E M N R R S
J 3 4 H JULHO
J 10 1 H CITADAS
J 7 5 H APANHARAM
J 8 2 V PEIXES
P
P
P
P
"""

OUTPUT_PUBLIC_2 = \
"""Bem-vindo ao SCRABBLE2.
                       1 1 1 1 1 1
     1 2 3 4 5 6 7 8 9 0 1 2 3 4 5
   +-------------------------------+
 1 | . . . . . . . . . . . . . . . |
 2 | . . . . . . . . . . . . . . . |
 3 | . . . . . . . . . . . . . . . |
 4 | . . . . . . . . . . . . . . . |
 5 | . . . . . . . . . . . . . . . |
 6 | . . . . . . . . . . . . . . . |
 7 | . . . . . . . . . . . . . . . |
 8 | . . . . . . . . . . . . . . . |
 9 | . . . . . . . . . . . . . . . |
10 | . . . . . . . . . . . . . . . |
11 | . . . . . . . . . . . . . . . |
12 | . . . . . . . . . . . . . . . |
13 | . . . . . . . . . . . . . . . |
14 | . . . . . . . . . . . . . . . |
15 | . . . . . . . . . . . . . . . |
   +-------------------------------+
Maria (  0): A H I N P R U
João (  0): Ç F I L N N S
Pedro (  0): D E E J M N O
Rita (  0): A E H M R S T
Jogada Maria:                        1 1 1 1 1 1
     1 2 3 4 5 6 7 8 9 0 1 2 3 4 5
   +-------------------------------+
 1 | . . . . . . . . . . . . . . . |
 2 | . . . . . . . . . . . . . . . |
 3 | . . . . . . . . . . . . . . . |
 4 | . . . . . . . . . . . . . . . |
 5 | . . . . . . . . . . . . . . . |
 6 | . . . . . . . . . . . . . . . |
 7 | . . . . . . . . . . . . . . . |
 8 | . . . U R I N A . . . . . . . |
 9 | . . . . . . . . . . . . . . . |
10 | . . . . . . . . . . . . . . . |
11 | . . . . . . . . . . . . . . . |
12 | . . . . . . . . . . . . . . . |
13 | . . . . . . . . . . . . . . . |
14 | . . . . . . . . . . . . . . . |
15 | . . . . . . . . . . . . . . . |
   +-------------------------------+
Maria (  7): A A B E H P R
João (  0): Ç F I L N N S
Pedro (  0): D E E J M N O
Rita (  0): A E H M R S T
Jogada João:                        1 1 1 1 1 1
     1 2 3 4 5 6 7 8 9 0 1 2 3 4 5
   +-------------------------------+
 1 | . . . . . . . . . . . . . . . |
 2 | . . . . . . . . . . . . . . . |
 3 | . . . . . . . . . . . . . . . |
 4 | . . . . . . . . . . . . . . . |
 5 | . . . . . . . F . . . . . . . |
 6 | . . . . . . . I . . . . . . . |
 7 | . . . . . . . N . . . . . . . |
 8 | . . . U R I N A . . . . . . . |
 9 | . . . . . . . L . . . . . . . |
10 | . . . . . . . . . . . . . . . |
11 | . . . . . . . . . . . . . . . |
12 | . . . . . . . . . . . . . . . |
13 | . . . . . . . . . . . . . . . |
14 | . . . . . . . . . . . . . . . |
15 | . . . . . . . . . . . . . . . |
   +-------------------------------+
Maria (  7): A A B E H P R
João ( 11): Ç E M N R R S
Pedro (  0): D E E J M N O
Rita (  0): A E H M R S T
Jogada Pedro:                        1 1 1 1 1 1
     1 2 3 4 5 6 7 8 9 0 1 2 3 4 5
   +-------------------------------+
 1 | . . . . . . . . . . . . . . . |
 2 | . . . . . . . . . . . . . . . |
 3 | . . . . . . . . . . . . . . . |
 4 | . . . . . . . . . . . . . . . |
 5 | . . . . . . . F . . . . . . . |
 6 | . . . . . . . I . . . . . . . |
 7 | . . . . . . . N . . . . . . . |
 8 | . . . U R I N A . . . . . . . |
 9 | . E N D E M O L . . . . . . . |
10 | . . . . . . . . . . . . . . . |
11 | . . . . . . . . . . . . . . . |
12 | . . . . . . . . . . . . . . . |
13 | . . . . . . . . . . . . . . . |
14 | . . . . . . . . . . . . . . . |
15 | . . . . . . . . . . . . . . . |
   +-------------------------------+
Maria (  7): A A B E H P R
João ( 11): Ç E M N R R S
Pedro ( 11): A I J L O U U
Rita (  0): A E H M R S T
Jogada Rita:                        1 1 1 1 1 1
     1 2 3 4 5 6 7 8 9 0 1 2 3 4 5
   +-------------------------------+
 1 | . . . . . . . . . . . . . . . |
 2 | . . . . . . . . . . . . . . . |
 3 | . . . . . . H . . . . . . . . |
 4 | . . . . . . E . . . . . . . . |
 5 | . . . . . . R F . . . . . . . |
 6 | . . . . . . M I . . . . . . . |
 7 | . . . . . . A N . . . . . . . |
 8 | . . . U R I N A . . . . . . . |
 9 | . E N D E M O L . . . . . . . |
10 | . . . . . . S . . . . . . . . |
11 | . . . . . . . . . . . . . . . |
12 | . . . . . . . . . . . . . . . |
13 | . . . . . . . . . . . . . . . |
14 | . . . . . . . . . . . . . . . |
15 | . . . . . . . . . . . . . . . |
   +-------------------------------+
Maria (  7): A A B E H P R
João ( 11): Ç E M N R R S
Pedro ( 11): A I J L O U U
Rita ( 13): A A C D I Q T
Jogada Maria:                        1 1 1 1 1 1
     1 2 3 4 5 6 7 8 9 0 1 2 3 4 5
   +-------------------------------+
 1 | . . . . . . . . . . . . . . . |
 2 | . . . . . . . . . . . . . . . |
 3 | . . . . . . H . . . . . . . . |
 4 | . . . . . . E . . . . . . . . |
 5 | . . . . . . R F . . . . . . . |
 6 | . . . . . . M I . . . . . . . |
 7 | . . . . A P A N H A R . . . . |
 8 | . . . U R I N A . . . . . . . |
 9 | . E N D E M O L . . . . . . . |
10 | . . . . . . S . . . . . . . . |
11 | . . . . . . . . . . . . . . . |
12 | . . . . . . . . . . . . . . . |
13 | . . . . . . . . . . . . . . . |
14 | . . . . . . . . . . . . . . . |
15 | . . . . . . . . . . . . . . . |
   +-------------------------------+
Maria ( 20): A B B E I M S
João ( 11): Ç E M N R R S
Pedro ( 11): A I J L O U U
Rita ( 13): A A C D I Q T
Jogada João:                        1 1 1 1 1 1
     1 2 3 4 5 6 7 8 9 0 1 2 3 4 5
   +-------------------------------+
 1 | . . . . . . . . . . . . . . . |
 2 | . . . . . . . . . . . . . . . |
 3 | . . . . . . H . . . . . . . . |
 4 | . . . . . . E . . . . . . . . |
 5 | . . . . . . R F . . . . . . . |
 6 | . . . . . . M I . . . . . . . |
 7 | . . . . A P A N H A R . . . . |
 8 | . . . U R I N A . . . . . . . |
 9 | . E N D E M O L . . . . . . . |
10 | . . . . . . S . . . . . . . . |
11 | . . . . . . . . . . . . . . . |
12 | . . . . . . . . . . . . . . . |
13 | . . . . . . . . . . . . . . . |
14 | . . . . . . . . . . . . . . . |
15 | . . . . . . . . . . . . . . . |
   +-------------------------------+
Maria ( 20): A B B E I M S
João ( 11): A E P S U U X
Pedro ( 11): A I J L O U U
Rita ( 13): A A C D I Q T
Jogada Pedro:                        1 1 1 1 1 1
     1 2 3 4 5 6 7 8 9 0 1 2 3 4 5
   +-------------------------------+
 1 | . . . . . . . . . . . . . . . |
 2 | . . . . . . . . . . . . . . . |
 3 | . . . J U L H O . . . . . . . |
 4 | . . . . . . E . . . . . . . . |
 5 | . . . . . . R F . . . . . . . |
 6 | . . . . . . M I . . . . . . . |
 7 | . . . . A P A N H A R . . . . |
 8 | . . . U R I N A . . . . . . . |
 9 | . E N D E M O L . . . . . . . |
10 | . . . . . . S . . . . . . . . |
11 | . . . . . . . . . . . . . . . |
12 | . . . . . . . . . . . . . . . |
13 | . . . . . . . . . . . . . . . |
14 | . . . . . . . . . . . . . . . |
15 | . . . . . . . . . . . . . . . |
   +-------------------------------+
Maria ( 20): A B B E I M S
João ( 11): A E P S U U X
Pedro ( 24): A C I J O T U
Rita ( 13): A A C D I Q T
Jogada Rita:                        1 1 1 1 1 1
     1 2 3 4 5 6 7 8 9 0 1 2 3 4 5
   +-------------------------------+
 1 | . . . . . . . . . . . . . . . |
 2 | . . . . . . . . . . . . . . . |
 3 | . . . J U L H O . . . . . . . |
 4 | . . . . . . E . . . . . . . . |
 5 | . . . . . . R F . . . . . . . |
 6 | . . . . . . M I . . . . . . . |
 7 | . . . . A P A N H A R . . . . |
 8 | . . . U R I N A . . . . . . . |
 9 | . E N D E M O L . . . . . . . |
10 | C I T A D A S . . . . . . . . |
11 | . . . . . . . . . . . . . . . |
12 | . . . . . . . . . . . . . . . |
13 | . . . . . . . . . . . . . . . |
14 | . . . . . . . . . . . . . . . |
15 | . . . . . . . . . . . . . . . |
   +-------------------------------+
Maria ( 20): A B B E I M S
João ( 11): A E P S U U X
Pedro ( 24): A C I J O T U
Rita ( 22): A B D G I L Q
Jogada Maria:                        1 1 1 1 1 1
     1 2 3 4 5 6 7 8 9 0 1 2 3 4 5
   +-------------------------------+
 1 | . . . . . . . . . . . . . . . |
 2 | . . . . . . . . . . . . . . . |
 3 | . . . J U L H O . . . . . . . |
 4 | . . . . . . E . . . . . . . . |
 5 | . . . . . . R F . . . . . . . |
 6 | . . . . . . M I . . . . . . . |
 7 | . . . . A P A N H A R A M . . |
 8 | . . . U R I N A . . . . . . . |
 9 | . E N D E M O L . . . . . . . |
10 | C I T A D A S . . . . . . . . |
11 | . . . . . . . . . . . . . . . |
12 | . . . . . . . . . . . . . . . |
13 | . . . . . . . . . . . . . . . |
14 | . . . . . . . . . . . . . . . |
15 | . . . . . . . . . . . . . . . |
   +-------------------------------+
Maria ( 35): B B D E I O S
João ( 11): A E P S U U X
Pedro ( 24): A C I J O T U
Rita ( 22): A B D G I L Q
Jogada João:                        1 1 1 1 1 1
     1 2 3 4 5 6 7 8 9 0 1 2 3 4 5
   +-------------------------------+
 1 | . . . . . . . . . . . . . . . |
 2 | . . . . . . . . . . . . . . . |
 3 | . . . J U L H O . . . . . . . |
 4 | . . . . . . E . . . . . . . . |
 5 | . . . . . . R F . . . . . . . |
 6 | . . . . . . M I . . . . . . . |
 7 | . . . . A P A N H A R A M . . |
 8 | . P . U R I N A . . . . . . . |
 9 | . E N D E M O L . . . . . . . |
10 | C I T A D A S . . . . . . . . |
11 | . X . . . . . . . . . . . . . |
12 | . E . . . . . . . . . . . . . |
13 | . S . . . . . . . . . . . . . |
14 | . . . . . . . . . . . . . . . |
15 | . . . . . . . . . . . . . . . |
   +-------------------------------+
Maria ( 35): B B D E I O S
João ( 25): A G O T U U Z
Pedro ( 24): A C I J O T U
Rita ( 22): A B D G I L Q
Jogada Pedro:                        1 1 1 1 1 1
     1 2 3 4 5 6 7 8 9 0 1 2 3 4 5
   +-------------------------------+
 1 | . . . . . . . . . . . . . . . |
 2 | . . . . . . . . . . . . . . . |
 3 | . . . J U L H O . . . . . . . |
 4 | . . . . . . E . . . . . . . . |
 5 | . . . . . . R F . . . . . . . |
 6 | . . . . . . M I . . . . . . . |
 7 | . . . . A P A N H A R A M . . |
 8 | . P . U R I N A . . . . . . . |
 9 | . E N D E M O L . . . . . . . |
10 | C I T A D A S . . . . . . . . |
11 | . X . . . . . . . . . . . . . |
12 | . E . . . . . . . . . . . . . |
13 | . S . . . . . . . . . . . . . |
14 | . . . . . . . . . . . . . . . |
15 | . . . . . . . . . . . . . . . |
   +-------------------------------+
Maria ( 35): B B D E I O S
João ( 25): A G O T U U Z
Pedro ( 24): A C I J O T U
Rita ( 22): A B D G I L Q
Jogada Rita:                        1 1 1 1 1 1
     1 2 3 4 5 6 7 8 9 0 1 2 3 4 5
   +-------------------------------+
 1 | . . . . . . . . . . . . . . . |
 2 | . . . . . . . . . . . . . . . |
 3 | . . . J U L H O . . . . . . . |
 4 | . . . . . . E . . . . . . . . |
 5 | . . . . . . R F . . . . . . . |
 6 | . . . . . . M I . . . . . . . |
 7 | . . . . A P A N H A R A M . . |
 8 | . P . U R I N A . . . . . . . |
 9 | . E N D E M O L . . . . . . . |
10 | C I T A D A S . . . . . . . . |
11 | . X . . . . . . . . . . . . . |
12 | . E . . . . . . . . . . . . . |
13 | . S . . . . . . . . . . . . . |
14 | . . . . . . . . . . . . . . . |
15 | . . . . . . . . . . . . . . . |
   +-------------------------------+
Maria ( 35): B B D E I O S
João ( 25): A G O T U U Z
Pedro ( 24): A C I J O T U
Rita ( 22): A B D G I L Q
Jogada Maria:                        1 1 1 1 1 1
     1 2 3 4 5 6 7 8 9 0 1 2 3 4 5
   +-------------------------------+
 1 | . . . . . . . . . . . . . . . |
 2 | . . . . . . . . . . . . . . . |
 3 | . . . J U L H O . . . . . . . |
 4 | . . . . . . E . . . . . . . . |
 5 | . . . . . . R F . . . . . . . |
 6 | . . . . . . M I . . . . . . . |
 7 | . . . . A P A N H A R A M . . |
 8 | . P . U R I N A . . . . . . . |
 9 | . E N D E M O L . . . . . . . |
10 | C I T A D A S . . . . . . . . |
11 | . X . . . . . . . . . . . . . |
12 | . E . . . . . . . . . . . . . |
13 | . S . . . . . . . . . . . . . |
14 | . . . . . . . . . . . . . . . |
15 | . . . . . . . . . . . . . . . |
   +-------------------------------+
Maria ( 35): B B D E I O S
João ( 25): A G O T U U Z
Pedro ( 24): A C I J O T U
Rita ( 22): A B D G I L Q
Jogada João: """
