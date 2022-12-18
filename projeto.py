disciplinas_semestres = {1: ['XDES01', 'SAHC04', 'SAHC05', 'MAT00A', 'IEPG01', 'IEPG22'],
                             2: ['XDES02', 'XDES04', 'STC001', 'XMAC01', 'IEPG04'],
                             3: ['ECN01', 'STC002', 'SRSC03', 'SDES05', 'XDES03'],
                             4: ['SRSC02', 'XPAD01', 'SMAC03', 'XMAC02', 'IEPG14'],
                             # 5:['ADM51E','SPAD03','SPA02','XRSC01'],
                             # 6:['SDES06','XMC001', 'IEPG10'],
                             # 7:['XAHC02','SDES07'],
                             # 8:['XAHC01','XAHC03','TCC1','ADM03E'],
                             # 9:['TCC2','SADG01']
                             }
optativasi=['A']
optativasp=['B']

#verifica se o fecho transitivo indireto da disciplina optativa já esta na lista de disciplias feitas
def verificaop(op,grafo, diciplinas):
    for x in grafo:
        if op in grafo[x] and x not in diciplinas:
            return op
    return 0

def bfs(grafo, v):
    lista=[]
    q=[]
    q.append(v)
    while q!=[]:
        v=q.pop()
        for adjacente in grafo[v]:
            if adjacente not in q:
                q.append(adjacente)
                continue
        lista.append(v)
    return lista

def monta_grade(historico_disciplinas, periodo, numero, disciplina_falta_fazer=[]):
    disciplinas_pode_fazer = []  # disciplinas que o aluno pode fazer esse semestre
    disciplinas_impossivel_fazer = []  # disciplinas que ele não pode fazer (por conta de préq requisitos ou questão de oferta
    disciplinas_mais_importantes = []  # disciplinas mais importantes (críticas) serem feitas no semestre que ele está

    # verifica se o periodo é par ou impar, para definir quais disciplinas ele pode ou não pegar
    periodo_impar = True
    optativas=optativasp
    if numero % 2 == 0:
        periodo_impar = False
        optativas =optativasi

    # quantidade de disciplinas que ele irá pegar
    if len(disciplinas_semestres[periodo]) < 4:
        quantidade_disciplinas_periodo = 4
    else:
        quantidade_disciplinas_periodo = len(disciplinas_semestres[periodo])

    # Grafo com as relações de pré requisito das disciplinas
    grafo = {'XDES01': ['XDES02'], 'SAHC04': ['XDES02'], 'SAHC05': ['XDES04','SDES05'], 'MAT00A': [],'IEPG01': [],'IEPG22': [],
            'XDES02': [],'XDES04': [],'STC001': [],'XMAC01': [],'IEPG04': [],'ECN01': [], 'STC002': ['B'], 'SRSC03': [], 'SDES05': [], 'XDES03': [],
             'SRSC02': [], 'XPAD01': [], 'SMAC03': [], 'XMAC02': [], 'IEPG14': [],'B':[]
             }

    # verifica quais disciplinas dos semestres anteriores ele deixou de fazer e quais as disciplinas do semestre q ele está
    for posicao in range(1, periodo + 1):
        # para cada disciplina já cursada
        for disciplina in historico_disciplinas:
            if disciplina in disciplinas_semestres[posicao]:
                # remove a disciplina do semestre tal
                disciplinas_semestres[posicao].remove(disciplina)
        # adiciona as disciplinas que restaram no semestre x à lista de disciplinas faltantes
        disciplina_falta_fazer = disciplina_falta_fazer + disciplinas_semestres[posicao]
    disciplina_falta_fazer = list(set(disciplina_falta_fazer))  # remove duplicatas

    # para cada disciplina do grafo será verificado sua relação com as disciplinas já feitas pelo aluno e as faltantes do semestre através de uma bfs
    for disciplina in disciplina_falta_fazer:
        resultado_bfs = bfs(grafo, disciplina)
        for materia in resultado_bfs:
            if materia == disciplina:
                continue
            if materia not in disciplinas_impossivel_fazer:
                disciplinas_impossivel_fazer.append(materia)
        if disciplina not in disciplinas_impossivel_fazer:
            if disciplina not in disciplinas_pode_fazer:
                disciplinas_pode_fazer.append(disciplina)
    # remove as disciplinas que ele não consegue fazer por conta dos pré requisitos
    for x in disciplinas_impossivel_fazer:
        if x in disciplinas_pode_fazer:
            disciplinas_pode_fazer.remove(x)

    # tira as disciplinas que não são ofertadas naquele semestre, da lista disciplinas_pode_fazer
    for tam in range(1, len(disciplinas_semestres)):
        # verifica em qual semestre está a disciplina
        teste = tam % 2 != 0
        if teste == periodo_impar:
            continue
        for disciplina in disciplinas_pode_fazer:
            if disciplina in disciplinas_semestres[tam]:
                disciplinas_pode_fazer.remove(disciplina)

    #Definindo prioridade das disciplinas de acordo com a bfs
    for disciplina in disciplinas_pode_fazer:
        if len(disciplinas_mais_importantes) == quantidade_disciplinas_periodo:
            break
        result = bfs(grafo,disciplina)
        for materia in result:
            if periodo + 1 in disciplinas_semestres:
                if materia in disciplinas_semestres[periodo + 1]:
                    # adiciona na lista de disciplinas críticas
                    if disciplina not in disciplinas_mais_importantes:
                        disciplinas_mais_importantes.append(disciplina)
            if periodo + 2 in disciplinas_semestres:
                if materia in disciplinas_semestres[periodo + 2]:
                    # adiciona na lista de disciplinas críticas
                    if disciplina not in disciplinas_mais_importantes:
                        disciplinas_mais_importantes.append(disciplina)

    # completa a lista de disciplinas críticas com o restante das disciplinas
    for disciplina in disciplinas_pode_fazer:
        if len(disciplinas_mais_importantes) == quantidade_disciplinas_periodo:
            break
        if disciplina not in disciplinas_mais_importantes:
            disciplinas_mais_importantes.append(disciplina)

    # as disciplinas feitas são removidas da lista das que faltam fazer
    for disciplina in disciplinas_mais_importantes:
        disciplina_falta_fazer.remove(disciplina)
    while len(disciplinas_mais_importantes)<quantidade_disciplinas_periodo:
        add_optativa=input('Deseja adicionar uma optativa? (S-sim N-não) \n')
        if add_optativa != 'S':
            break
        result = input('Digite qual disciplina deseja fazer: ')
        op=verificaop(result,grafo, historico_disciplinas)
        if op==0:
            disciplinas_mais_importantes.append(result)
            print('Adicionada')
        else:
            print('Não adicionada, possui pré-requisito')
    # o histórico do aluno é atualizado com as disciplinas que ele fez no semestre
    historico_disciplinas = historico_disciplinas + disciplinas_mais_importantes

    print('semestre:', numero, disciplinas_mais_importantes)

    # irá chamar novamente a função de montar grade, até que todos os periodos da lista dos semestres sejam analisados e não fale nenhuma disciplina
    if periodo < len(disciplinas_semestres):
        monta_grade(historico_disciplinas, periodo + 1, numero + 1, disciplina_falta_fazer)
    else:
        if len(disciplina_falta_fazer) != 0:
            monta_grade(historico_disciplinas, periodo, numero + 1, disciplina_falta_fazer)


# disicplinas que o aluno ja fez
grafo = ['ECN01']
monta_grade(grafo, 1, 1)
