from collections import defaultdict, deque
from itertools import permutations

class Grafo:
    def __init__(self, arestas):
        self.grafo = defaultdict(set)
        for u, v in arestas:
            self.grafo[u].add(v)
            self.grafo[v].add(u)

    def _dfs(self, no, visitados):
        visitados.add(no)
        for vizinho in self.grafo[no]:
            if vizinho not in visitados:
                self._dfs(vizinho, visitados)

    def componentes_conexas(self):
        visitados = set()
        componentes = []
        for no in self.grafo:
            if no not in visitados:
                componente = []
                self._dfs_coletar(no, visitados, componente)
                componentes.append(componente)
        return componentes

    def _dfs_coletar(self, no, visitados, componente):
        visitados.add(no)
        componente.append(no)
        for vizinho in self.grafo[no]:
            if vizinho not in visitados:
                self._dfs_coletar(vizinho, visitados, componente)

    def eh_completo(self):
        n = len(self.grafo)
        for no in self.grafo:
            if len(self.grafo[no]) != n - 1:
                return False
        return True

    def possui_ciclo(self):
        visitados = set()
        
        def dfs(no, pai):
            visitados.add(no)
            for vizinho in self.grafo[no]:
                if vizinho not in visitados:
                    if dfs(vizinho, no):
                        return True
                elif vizinho != pai:
                    return True
            return False

        for no in self.grafo:
            if no not in visitados:
                if dfs(no, None):
                    return True
        return False

    def eh_bipartido(self):
        cor = {}

        def bfs(no):
            fila = deque([no])
            cor[no] = 0
            while fila:
                atual = fila.popleft()
                for vizinho in self.grafo[atual]:
                    if vizinho not in cor:
                        cor[vizinho] = 1 - cor[atual]
                        fila.append(vizinho)
                    elif cor[vizinho] == cor[atual]:
                        return False
            return True

        for no in self.grafo:
            if no not in cor:
                if not bfs(no):
                    return False
        return True

    def possui_caminho_fechado(self):
        for no in self.grafo:
            if len(self.grafo[no]) % 2 != 0:
                return False
        return True

    def possui_circuito_euleriano(self):
        if not self.possui_caminho_fechado():
            return False

        visitados = set()
        for no in self.grafo:
            if len(self.grafo[no]) > 0:
                self._dfs(no, visitados)
                break

        for no in self.grafo:
            if no not in visitados and len(self.grafo[no]) > 0:
                return False

        return True

    def sao_isomorfos(self, outro):
        if len(self.grafo) != len(outro.grafo):
            return False
        
        for perm in permutations(self.grafo.keys()):
            mapeamento = {list(self.grafo.keys())[i]: perm[i] for i in range(len(self.grafo))}
            if all(
                set(mapeamento[vizinho] for vizinho in self.grafo[no]) == outro.grafo[mapeamento[no]]
                for no in self.grafo
            ):
                return True
        return False

# Exemplo de Teste
grafo1 = Grafo([["A", "B"], ["B", "C"], ["A", "C"]])
grafo2 = Grafo([["A", "B"], ["B", "C"], ["C", "D"], ["D", "A"]])
grafo3 = Grafo([["A", "B"], ["B", "C"], ["C", "A"], ["A", "D"], ["D", "E"], ["E", "A"]])

print("Componentes Conexas:", grafo3.componentes_conexas())
print("É Completo:", grafo3.eh_completo())
print("Possui Ciclo:", grafo3.possui_ciclo())
print("É Bipartido:", grafo3.eh_bipartido())
print("Possui Caminho Fechado:", grafo3.possui_caminho_fechado())
print("Possui Circuito Euleriano:", grafo3.possui_circuito_euleriano())
print("São Isomorfos:", grafo3.sao_isomorfos(grafo2))
