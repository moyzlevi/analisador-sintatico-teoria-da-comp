# Analisador Lexico por Moyses Santos

## Objetivo
O programa foi desenvolvido para a cadeira de Teoria da computação da UFCSPA do curso de informática biomédica com o objetivo de estudo de compiladores e mais especificamente analisadores lexicos

## Pacotes
Foram utilizados os seguintes pacotes, sendo apenas o tabulate de terceiros que foi utilizado para a geração da tabela em um arquivo .txt :
```python
import string
from typing import List
from tabulate import tabulate
from dataclasses import dataclass
from enum import Enum
from io import StringIO
```
## Estruturas de dados
Foram geradas duas estruturas de dados principais sendo a primeira delas uma enumeração com os tipos de token separados em símbolo e a segunda uma classe palavra com um método de adição de valores no terceiro atributo que corresponde as linhas de ocorrência da palavra.

```python
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
```
## Analisador sintático
A estrutura do analisador sintático desenvolvido neste trabalho pode ser simplificada em dois laços de repetição hierarquizados. O laço de repetição de segundo grau corresponde as linhas sendo atualmente percorridas pelo analisador sintático, já o laço de repetição interno, por sua vez, representa cada letra da linha atual.

O programa começa removendo os espaços, logo em seguida uma verificação é feita para controlar a escrita de palavras. Se a palavra escrita no buffer principal é do tipo ID ou NUM e a letra atual não for desses dois últimos tipos, o laço de repetição passa na verificação e começa a sua escrita e classificação na lista de palavras reconhecidas. Duas verificações são feitas para observar se as palavras atuais já não existem. Enquanto isso, um buffer guarda as informações das palavras para gerar o código reescrito.

Por fim, o analisador sintático utiliza a lista de palavras classificadas e gera um tabela utilizando o pacote tabulate. Logo após, um outro laço de repetição percorre o buffer de reescrita e escreve o código reescrito.