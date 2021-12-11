# -*- coding: utf-8 -*-
"""GeraModeloTrab2Bim.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/18Vxr8IVZ77vUjTrKLTv6qOItckmb_-V3
"""

!pip install fastapi nest-asyncio pyngrok uvicorn jinja2

class Cidade :
    """
        Classe que representa uma cidade no mapa.
    """
    def __init__(self, nome, caminhos=[]):
        self.nome = nome
        
        # contabiliza a distância desde a origem no trajeto realizado
        self.distanciaOrigem = 0
        # indica se esta cidade já foi visitada, para não repetir caminhos
        self.visitada = False
        # uma lista de tuplas utilizada para determinar os caminhos possíveis e
        # calcular a distância percorrida a cada passo
        self.caminhos = caminhos
    
    def trafegar(self, distancia):
        """
            Este método é utilizado durante a busca heurística para contabilizar
            a distância percorrida e quais cidades já foram visitadas.
        """
        self.distanciaOrigem = self.distanciaOrigem + distancia
        self.visitada = True
        self.caminhos = [(nome, distancia + self.distanciaOrigem) for (nome, distancia) in self.caminhos]
        return self
    
    def resetar(self):
        """
            Este método é utilizado antes de iniciar a busca heurística, para
            limpar os resultados de execuções anteriores.
        """
        self.distanciaOrigem = 0
        self.visitada = False
        return self

class FilaPrioritariaMin:
    """
        Uma fila que sempre retorna o menor item seguindo um critério de ordenação.
    """
    def __init__(self, lst=[], key=None):
        #chave para ordenação da fila
        self.key = key
        self.lst = sorted(lst, key=key)
        
    def adicionar(self, elem):
        try:
            self.lst.extend(elem)
        except:
            self.lst.append(elem)
        self.lst.sort(key=self.key)
    
    def remover(self):
        if not self.estaVazia():
            elem, *self.lst = self.lst
            return elem
        else: 
            return None
    
    def estaVazia(self):
        return len(self.lst) == 0
    
class BuscadorHeuristicoMin:
    
    # grafo contendo as cidades e os trajetos a partir delas
    grafo_mapa = {
        'Arad'           : Cidade('Arad', [('Zerind', 75), ('Sibiu', 140), ('Timisoara', 118)]),
        'Bucharest'      : Cidade('Bucharest', [('Giurgiu', 90), ('Pitesti', 101), ('Urziceni', 85), ('Fagaras', 211)]),
        'Craiova'        : Cidade('Craiova', [('Pitesti', 138), ('Dobreta', 120), ('Rimnicu Vilcea', 146)]),
        'Dobrieta'       : Cidade('Dobrieta', [('Craiova', 120), ('Mehadia', 75)]),
        'Eforie'         : Cidade('Eforie', [('Hirsova', 86)]),
        'Fagaras'        : Cidade('Fagaras', [('Bucharest', 211), ('Sibiu', 99)]),
        'Giurgiu'        : Cidade('Giurgiu', [('Bucharest', 90)]),
        'Hirsova'        : Cidade('Hirsova', [('Eforie', 86), ('Urziceni', 98)]),
        'Iasi'           : Cidade('Iasi', [('Neamt', 87), ('Vaslui', 92)]),
        'Lugoj'          : Cidade('Lugoj', [('Mehadia', 70), ('Timisoara', 111)]),
        'Mehadia'        : Cidade('Mehadia', [('Dobreta', 75), ('Lugoj', 70)]),
        'Neamt'          : Cidade('Neamt', [('Iasi', 87)]),
        'Oradea'         : Cidade('Oradea', [('Sibiu', 151), ('Zerind', 71)]),
        'Pitesti'        : Cidade('Pitesti', [('Bucharest', 101), ('Craiova', 138), ('Rimnicu Vilcea', 97)]),
        'Rimnicu Vilcea' : Cidade('Rimnicu Vilcea', [('Pitesti', 97), ('Sibiu', 80), ('Craiova', 146)]),
        'Sibiu'          : Cidade('Sibiu', [('Fagaras', 99), ('Arad', 140), ('Oradea', 151), ('Rimnicu Vilcea', 80)]),
        'Timisoara'      : Cidade('Timisoara', [('Lugoj', 111), ('Arad', 118)]),
        'Urziceni'       : Cidade('Urziceni', [('Vaslui', 142), ('Hirsova', 98), ('Bucharest', 85) ]),
        'Vaslui'         : Cidade('Vaslui', [('Iasi', 92), ('Urziceni', 142)]),
        'Zerind'         : Cidade('Zerind', [('Oradea', 71), ('Arad', 75)])    
    }
    
    def __init__(self, heuristicas, gulosa=False):
        """
            Inicializa o buscador com as heurísticas a serem utilizadas, 
            e configura a busca se é A* ou gulosa
        """
        self.heuristicas = heuristicas
        self.gulosa = gulosa
        
    def prioridade(self, cidade, destino):
        # calcula a prioridade das cidades na fila
        if cidade.nome == destino:
            return -1
        elif self.gulosa:
            return self.heuristicas[cidade.nome]
        else:
            return cidade.distanciaOrigem + self.heuristicas[cidade.nome]
    
    def buscar(self, origem, destino):        
        
        # busca a cidade de origem no grafo
        raiz = self.grafo_mapa[origem]
        
        # insere a cidade de origem na fila
        fila = FilaPrioritariaMin([raiz], key=lambda cidade: self.prioridade(cidade, destino))
        
        # contabiliza o caminho percorrido para retornar ao usuário do método
        caminhoPercorrido = []
        
        while not fila.estaVazia():
            # remove a trajetória de maior prioridade
            cidade = fila.remover()   
            
            
            # contabiliza a trajetória
            caminhoPercorrido.append(cidade.nome)
            
            if cidade.nome == destino:
                # caso a cidade atual seja o destino procurado, retorne o custo
                # mínimo e o caminho percorrido
                resultado = {'custo' : cidade.distanciaOrigem, 'caminho' : caminhoPercorrido}
                
                # limpa o trabalho realizado no grafo para a próxima execução
                for cidade in self.grafo_mapa.keys():
                    self.grafo_mapa[cidade].resetar()
                    
                return resultado
            else:
                # calcula as próximas trajetórias e adiciona na fila
                for nome, dist in cidade.caminhos:
                    cidadeCaminho = self.grafo_mapa[nome]
                    if not cidadeCaminho.visitada:
                        self.grafo_mapa[nome] = cidadeCaminho.trafegar(dist)
                        fila.adicionar(cidadeCaminho)
            
        # se não encontrar caminho até o destino, proclame fracasso
        return False
    
heuristicasBucharest = {
    'Arad'           : 366,
    'Bucharest'      : 0,
    'Craiova'        : 160,
    'Dobrieta'       : 242,
    'Eforie'         : 161,
    'Fagaras'        : 178,
    'Giurgiu'        : 77,
    'Hirsova'        : 151,
    'Iasi'           : 226,
    'Lugoj'          : 244,
    'Mehadia'        : 241,
    'Neamt'          : 234,
    'Oradea'         : 380,
    'Pitesti'        : 98,
    'Rimnicu Vilcea' : 193,
    'Sibiu'          : 253,
    'Timisoara'      : 329,
    'Urziceni'       : 80,
    'Vaslui'         : 199,
    'Zerind'         : 374,
}

buscador = BuscadorHeuristicoMin(heuristicasBucharest, gulosa=True)
print(buscador.buscar('Arad', 'Bucharest'))

from fastapi import FastAPI, Request
import nest_asyncio
from pyngrok import ngrok
import uvicorn
import json 
import warnings

from pydantic import BaseModel

from starlette.responses import FileResponse
from fastapi.responses import HTMLResponse
from fastapi import Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

warnings.filterwarnings('ignore')

app = FastAPI()

templates = Jinja2Templates(directory="templates2")


@app.get("/",response_class=HTMLResponse)
async def get(request: Request):
  return templates.TemplateResponse('index.html', {'request':request})


@app.get('/index')
async def home():
  return "Hello World"

class Query(BaseModel):
  origem: str
  destino: str

@app.post('/query/')
async def create_query(query: Query):
  return buscador.buscar(query.origem, query.destino)

ngrok_tunnel = ngrok.connect(8000)
print('Public URL: ',ngrok_tunnel.public_url ) 
nest_asyncio.apply()
uvicorn.run(app,port=8000)