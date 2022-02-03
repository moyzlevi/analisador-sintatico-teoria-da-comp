# Trabalho por Moyses Levi Zalewski Pietsch dos Santos - aluno de Informática Biomédica (UFCSPA)

# Imports de pacotes 
import string
from typing import List
from tabulate import tabulate
from dataclasses import dataclass
from enum import Enum
from io import StringIO

# Declaração de classes de estrutura

class Simbolo(Enum):
     ID = 'id'
     OP_IGUAL = 'op=' 
     NUM = 'num'
     SIMBESP = 'simbesp'
     OP_SOMA = 'op+'
     OP_DIVIDE = 'op/'
     OP_MULTIPLICA= 'op*'
     OP_SUBTRAI = 'op-'
     NENHUM = ''

class Palavra:
    def __init__(self, token, simbolo):
         self.token = token
         self.simbolo = simbolo
         self.posicoes_no_codigo = []
   
    def adicionar_posicao(self, posicao):
        self.posicoes_no_codigo.append(posicao)
    
    def __str__(self):
        return f"{str(self.token)}|{self.simbolo}|{self.posicoes_no_codigo}"

# Leitura do input (código) a ser analisado
linhas_do_arquivo = []
with open("input/codigo.txt", 'r') as file:
    linhas_do_arquivo = file.read().splitlines()

# Analisador sintático
palavras = []
buffer_codigo_reescrito = StringIO()

def escreve_no_buffer_reescricao(buffer_codigo_reescrito,enum):
    if enum == Simbolo.OP_IGUAL:
        buffer_codigo_reescrito.write("= ")
    
def checa_operador_ou_simbesp(letra):
    operadores_ou_simbolosesp = [';','/','+','=','-','*','(',')']
    return letra in operadores_ou_simbolosesp

def checa_simbesp(letra):
   operadores_ou_simbolosesp = [';',')','(']
   return letra in operadores_ou_simbolosesp

def checa_numero_ou_ponto(letra):
    return letra.isnumeric() or letra == '.'

def retorna_enum_simbolo(letra):
    if letra.isnumeric():
        return Simbolo.NUM
    if letra.isalpha():
        return Simbolo.ID
    if letra == '/':
        return Simbolo.OP_DIVIDE
    if letra == '+':
        return Simbolo.OP_SOMA
    if letra == '-':
        return Simbolo.OP_SUBTRAI
    if letra == '*':
        return Simbolo.OP_MULTIPLICA
    if letra in [';','(',')']:
        return Simbolo.SIMBESP
    if letra == '=':
        return Simbolo.OP_IGUAL
    
for index_linha_atual, linha in enumerate(linhas_do_arquivo):
    
    buffer = StringIO()
    palavras_para_o_buffer = []
    simbolo_atual = Simbolo.NENHUM
    # print(linha)
    for index_letra_atual,letra in enumerate(linha):
        if letra == ' ':
            continue
        
        if simbolo_atual == Simbolo.NENHUM:
            simbolo_atual = retorna_enum_simbolo(letra)
        
        if checa_operador_ou_simbesp(letra) and (simbolo_atual == Simbolo.ID or simbolo_atual == Simbolo.NUM):
            valor_do_buffer = buffer.getvalue()
            
            valor_do_buffer_repetido = False
            valor_do_letra_repetida = False

            for palavra in palavras:
                 if valor_do_buffer == palavra.token:
                    palavra.adicionar_posicao(index_linha_atual+1)
                   
                    if checa_simbesp(palavra.token):
                        palavras_para_o_buffer.append(palavra.token+ " ")
                    else:
                         palavras_para_o_buffer.append(palavra.simbolo.name+ " ")
                    valor_do_buffer_repetido = True
            
            for palavra in palavras:
                if letra == palavra.token:
                    palavra.adicionar_posicao(index_linha_atual+1)
                    if checa_simbesp(palavra.token):
                        palavras_para_o_buffer.append(palavra.token + " ")
                    else:
                        palavras_para_o_buffer.append(palavra.simbolo.name+ " ")
                    valor_do_letra_repetida = True
                    
            if not valor_do_buffer_repetido:
                nova_palavra_encontrada = Palavra(valor_do_buffer, simbolo_atual)
                nova_palavra_encontrada.adicionar_posicao(index_linha_atual+1)

                if checa_simbesp(valor_do_buffer):
                    palavras_para_o_buffer.append(valor_do_buffer+ " ")
                else:
                    palavras_para_o_buffer.append(simbolo_atual.name+ " ")
                
                palavras.append(nova_palavra_encontrada)
                buffer.truncate(0)
            
            if not valor_do_letra_repetida:
                novo_simbolo_encontrado = Palavra(letra, retorna_enum_simbolo(letra))
                novo_simbolo_encontrado.adicionar_posicao(index_linha_atual+1)
                
                if checa_simbesp(letra):
                    palavras_para_o_buffer.append(letra+ " ")
                else:
                    palavras_para_o_buffer.append(retorna_enum_simbolo(letra).name+ " ")

                palavras.append(novo_simbolo_encontrado)

            buffer.truncate(0)
            simbolo_atual = Simbolo.NENHUM
            if not valor_do_buffer_repetido and valor_do_letra_repetida:
                palavras_para_o_buffer.reverse()
        elif checa_operador_ou_simbesp(letra):
            valor_do_letra_repetida = False
            for palavra in palavras:
                 if letra == palavra.token:
                    palavra.adicionar_posicao(index_linha_atual+1)
                    valor_do_letra_repetida = True
                    if checa_simbesp(letra):
                      palavras_para_o_buffer.append(letra+ " ")
                    else:
                      palavras_para_o_buffer.append(palavra.simbolo.name+ " ")
            if not valor_do_letra_repetida:
                novo_simbolo_encontrado = Palavra(letra, retorna_enum_simbolo(letra))
                novo_simbolo_encontrado.adicionar_posicao(index_linha_atual+1)
                if checa_simbesp(letra):
                      palavras_para_o_buffer.append(letra+ " ")
                else:
                      palavras_para_o_buffer.append(retorna_enum_simbolo(letra).name+ " ")
                palavras.append(novo_simbolo_encontrado)
                buffer.truncate(0)
                simbolo_atual = Simbolo.NENHUM    
        else:
            buffer.write(letra)
        for index, palavra in enumerate(palavras_para_o_buffer):
            buffer_codigo_reescrito.write(palavras_para_o_buffer[index])
        palavras_para_o_buffer = []

palavras_to_string = []
for x in palavras:
    palavra_atual = [x.token.lstrip('\x00'), x.simbolo.value, x.posicoes_no_codigo]
    palavras_to_string.append(palavra_atual)

l = palavras_to_string
table = tabulate(l, headers=['Token', 'Simbolo', 'Posicao no codigo (linha)'], tablefmt='simple')

with open("output/lista_de_tokens.txt", 'w') as file:
    file.write(table)

palavras_do_codigo_reescrito = buffer_codigo_reescrito.getvalue().split(' ')
buffer_pos = StringIO()

for palavra in palavras_do_codigo_reescrito:
    if palavra == 'OP_IGUAL':
        buffer_pos.write("= ")
    else:
        buffer_pos.write(palavra+" ")
        
with open("output/codigo_reescrito.txt", 'w') as file:
    file.write(buffer_pos.getvalue())
