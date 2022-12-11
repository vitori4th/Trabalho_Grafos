#Em um grafo não-ponderado, o caminho máximo entre dois vértices v (origem) e u (destino) é aquele que possui a maior quantidade de arestas entre eles.

def encontra_todos_caminhos(grafo, inicio, fim, caminho=[]):
    caminho = caminho + [inicio]
    if inicio == fim:
        return [caminho]
    if inicio not in grafo:
        return []
    caminhos = []
    for no in grafo[inicio]:
        if no not in caminho:
            novos_caminhos = encontra_todos_caminhos(grafo, no, fim, caminho)
            for novo_caminho in novos_caminhos:
                caminhos.append(novo_caminho)
    return caminhos

def monta_grade(historico_disciplinas, periodo,disciplina_falta_fazer=[] ):
    disciplinas_fazer =[] #disciplinas que o aluno irá fazer esse semestre
    disciplinas_impossivel_fazer=[] #disciplinas que ele não pode fazer
    disciplinas_mais_importantes=[] # disciplinas mais importantes (críticas) serão feitas no semestre que ele está
    # dicionario com periodo(chave) e disciplinas (valor)
    disciplinas_semestres ={ 1:['A','B','C'], 2:['D','E','F'],3:['G','H','I'] }
    #quantidade de disciplinas que ele pega no semestre em que ele está
    quantidade_disciplinas_periodo = len(disciplinas_semestres[periodo])
    #Grafo com as relações de pré requisito das disciplinas
    grafo ={'A': ['G'],
        'B': ['E'],
        'C': ['F'],
        'D': ['G'],
         'E': ['H'],
         'F': ['I'],
        'G': ['fim'],
         'H': ['fim'],
         'I': ['fim'],
            'fim':[]}
    grafo1 = {'A': ['fim'],
             'B': ['D'],
             'C': ['fim'],
             'D': ['fim'],
             'E': ['fim'],
             'F': ['fim'],
             'G': ['fim'],
             'H': ['fim'],
             'I': ['fim'],
            'fim':[]}

    # verifica quais disciplinas dos semestres anteriores ele deixou de fazer e quais as disciplinas do semestre q ele está
    for posicao in range(1,periodo+1):
        # para cada disciplinas já cursada
        for disciplina in historico_disciplinas:
            if disciplina in disciplinas_semestres[posicao]:
                # remove a disciplina do semestre tal
                disciplinas_semestres[posicao].remove(disciplina)
        # adiciona as disciplinas que restaram no semestre x à lista de disciplinas faltantes
        disciplina_falta_fazer= disciplina_falta_fazer + disciplinas_semestres[posicao]
    disciplina_falta_fazer = list(set(disciplina_falta_fazer)) # remove duplicatas

    # para cada disciplina do grafo será verificado sua relação com as disciplinas já feitas pelo aluno e as faltantes do semestre
    for disciplina in disciplina_falta_fazer:
        caminhos = encontra_todos_caminhos(grafo, disciplina,'fim')
        # para cada materia retornada pela BFS da disciplina do grafo será analisada se o aluno pode/precisa ou não fazer
        for caminho in caminhos:
            for x in range(1, len(caminho)-1):
                if caminho[x] not in disciplinas_impossivel_fazer:
                    disciplinas_impossivel_fazer.append(caminho[x])
            if disciplina not in disciplinas_impossivel_fazer:
                if disciplina not in disciplinas_fazer:
                    disciplinas_fazer.append(disciplina)

    #tira as disciplinas que ele não consegue fazer da lista de disciplinas que ele pode pegar para fazer (disciplinas_fazer)
    for x in disciplinas_impossivel_fazer:
        if x in disciplinas_fazer:
            disciplinas_fazer.remove(x)

    #para cada disciplinas das que ele pode fazer
    for disciplina in disciplinas_fazer:
        if len(disciplinas_mais_importantes)== quantidade_disciplinas_periodo:
            break
        caminhos = encontra_todos_caminhos(grafo, disciplina, 'fim')
        for caminho in caminhos:
            if caminho[1] !='fim':
                if periodo+1 in disciplinas_semestres:
                    if caminho[1] in disciplinas_semestres[periodo+1]:
                        #adiciona na lista de disciplinas críticas
                        disciplinas_mais_importantes.append(disciplina)

                if periodo+2 in disciplinas_semestres:
                    if caminho[1] in disciplinas_semestres[periodo + 2]:
                        # adiciona na lista de disciplinas críticas
                        disciplinas_mais_importantes.append(disciplina)

    #completa a lista de disciplinas criticas com o restante das disciplinas
    for disciplina in disciplinas_fazer:
        if len(disciplinas_mais_importantes) == quantidade_disciplinas_periodo:
            break
        if disciplina not in disciplinas_mais_importantes:
            disciplinas_mais_importantes.append(disciplina)

    # o histórico do aluno é atualizado com as disciplinas que ele fez no semestre
    historico_disciplinas = historico_disciplinas + disciplinas_mais_importantes

    # as disciplinas feitas são removidas da lista das que faltam fazer
    for disciplina in disciplinas_mais_importantes:
        disciplina_falta_fazer.remove(disciplina)

    print('semestre:',periodo,disciplinas_mais_importantes)

    #irá chamar novamente a função de montar grade, até que todos os periodos da lista dos semestres sejam analisados e não falta nenhuma disciplina
    if periodo <len(disciplinas_semestres):
        monta_grade(historico_disciplinas,periodo+1,disciplina_falta_fazer)
    else:
        if len(disciplina_falta_fazer) !=0:
            monta_grade(historico_disciplinas, periodo, disciplina_falta_fazer)

#disicplinas que o aluno ja fez
grafo = []
monta_grade(grafo, 1)
