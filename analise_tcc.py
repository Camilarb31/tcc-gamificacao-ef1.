#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
analise_tcc.py - Script de analise do TCC
"Gamificacao e plataformas educacionais digitais: a percepcao de professores
sobre o engajamento de alunos do Ensino Fundamental I" (Univesp, TCC530).

Reproduz os numeros das secoes 5.1 a 5.7 a partir da base anonimizada.

Requisitos: Python 3.9+ e pandas (pip install pandas)
Uso:        python analise_tcc.py base_anonimizada.csv
"""
import sys
import math
import pandas as pd

# ----------------------------------------------------------------- utilidades
def limpa(txt):
    """Remove espacos e o ponto final das alternativas do formulario."""
    return str(txt).strip().rstrip(".").strip()

def itens(serie):
    """Transforma respostas de multipla escolha (separadas por ';') em listas."""
    saida = []
    for v in serie:
        if pd.isna(v):
            saida.append([])
        else:
            saida.append([limpa(p) for p in str(v).split(";") if limpa(p)])
    return saida

def tem(lista, trecho):
    """Verdadeiro se alguma alternativa da lista contem o trecho (sem diferenciar maiusculas)."""
    return any(trecho.lower() in a.lower() for a in lista)

def wilson(k, n, z=1.96):
    """Intervalo de confianca de 95% de Wilson para uma proporcao k/n (em %)."""
    if n == 0:
        return (float("nan"), float("nan"))
    p = k / n
    den = 1 + z ** 2 / n
    centro = (p + z ** 2 / (2 * n)) / den
    marg = z * math.sqrt(p * (1 - p) / n + z ** 2 / (4 * n ** 2)) / den
    return (100 * max(0.0, centro - marg), 100 * min(1.0, centro + marg))

def pct(k, n):
    return 100 * k / n if n else float("nan")

def fmt(x, casas=1):
    return f"{x:.{casas}f}".replace(".", ",")

def linha(rotulo, k, n):
    return f"  {rotulo:<68} {k:>3} de {n:<3} {fmt(pct(k, n)):>6}%"

def contagem(listas, n, ordem=None):
    """Conta alternativas em uma lista de listas e imprime ordenado."""
    cont = {}
    for l in listas:
        for a in l:
            cont[a] = cont.get(a, 0) + 1
    for a, k in sorted(cont.items(), key=lambda x: -x[1]):
        print(linha(a, k, n))

def titulo(txt):
    print("\n" + "=" * 78)
    print(txt)
    print("=" * 78)

def media(serie):
    s = serie.dropna()
    return s.mean() if len(s) else float("nan")

# ----------------------------------------------------------------- leitura
if len(sys.argv) < 2:
    print("Uso: python analise_tcc.py base_anonimizada.csv")
    sys.exit(1)

df = pd.read_csv(sys.argv[1], encoding="utf-8-sig")
titulo("BASE")
print(f"Respostas na base: {len(df)}")

# Filtro de elegibilidade (questao 2): atua ou atuou nos ultimos dois anos
df["elegivel"] = df["q2_atua_ef1"].fillna("").str.lower().str.startswith("sim")
v = df[df["elegivel"]].copy()
n = len(v)
print(f"Respostas validas (docentes do EF I): {n}")

# Listas de multipla escolha
for col in ["q4_rede", "q7_plataformas", "q8_finalidade", "q10_sinais",
            "q11_elementos", "q15_limitacoes", "q16_condicoes"]:
    v[col + "_l"] = itens(v[col])

# Escala de engajamento (questao 9): numero inicial; NaN se "nao tenho experiencia"
def nota(txt):
    t = str(txt).strip()
    return int(t[0]) if t and t[0].isdigit() else float("nan")
v["nota"] = v["q9_engajamento"].apply(nota)

# Categorias do Quadro 2 (a partir da questao 7)
def tradicional(l):
    return (tem(l, "Plataforma própria") or tem(l, "Google Classroom")
            or tem(l, "videoconferência"))

def gamificada(l):
    return (tem(l, "quizzes") or tem(l, "elementos de gamificação")
            or tem(l, "Escola games"))

v["trad"] = v["q7_plataformas_l"].apply(tradicional)
v["gami"] = v["q7_plataformas_l"].apply(gamificada)
v["nenhuma"] = v["q7_plataformas_l"].apply(lambda l: tem(l, "Não utilizei plataformas"))

# Docentes com experiencia em gamificacao (questao 11)
v["exp_gami"] = ~v["q11_elementos_l"].apply(lambda l: tem(l, "Não utilizei ou não observei"))
g = v[v["exp_gami"]]
ng = len(g)

# ----------------------------------------------------------------- 5.1 Perfil
titulo(f"5.1 PERFIL DOS PARTICIPANTES (Tabela 1) - n = {n}")
print("Situacao")
for r, k in v["q2_atua_ef1"].value_counts().items():
    print(linha(limpa(r), k, n))
print("Estado")
for r, k in v["q3_estado"].value_counts().items():
    print(linha(limpa(r), k, n))
print("Rede de ensino")
redes = v["q4_rede_l"].apply(lambda l: " e ".join([l[0]] + [x.lower() for x in l[1:]]))
for r, k in redes.value_counts().items():
    print(linha(r, k, n))
print("Tempo de docencia")
ordem_t = ["Menos de 1 ano", "De 1 a 3 anos", "De 4 a 10 anos",
           "De 11 a 20 anos", "Mais de 20 anos"]
ct = v["q5_tempo"].apply(limpa).value_counts()
for r in ordem_t:
    print(linha(r, int(ct.get(r, 0)), n))
print("Frequencia de uso de plataformas")
ordem_f = ["Diariamente", "De duas a quatro vezes por semana", "Uma vez por semana",
           "Algumas vezes por mês", "Raramente", "Nunca utilizei"]
cf = v["q6_frequencia"].apply(limpa).value_counts()
for r in ordem_f:
    print(linha(r, int(cf.get(r, 0)), n))
semanal = sum(int(cf.get(r, 0)) for r in ordem_f[:3])
print(linha("Uso ao menos uma vez por semana", semanal, n))

# ----------------------------------------------------------------- 5.2 Plataformas
titulo(f"5.2 PLATAFORMAS E FERRAMENTAS (Figura 1) - n = {n}, resposta multipla")
contagem(v["q7_plataformas_l"], n)
print("\nCategorias do Quadro 2")
print(linha("Usam ferramentas gamificadas", int(v["gami"].sum()), n))
print(linha("Usam plataformas tradicionais", int(v["trad"].sum()), n))
print(linha("Usam ambas", int((v["gami"] & v["trad"]).sum()), n))
print(linha("Nao utilizaram plataformas digitais (q7)", int(v["nenhuma"].sum()), n))
print("\nFinalidade (questao 8)")
contagem(v["q8_finalidade_l"], n)

# ----------------------------------------------------------------- 5.3 Engajamento
av = v[v["nota"].notna()]
na = len(av)
titulo(f"5.3 ENGAJAMENTO DOS ALUNOS (Figura 2, Tabela 2, Figura 3)")
print(f"Docentes que avaliaram: {na} de {n} ({n - na} sem experiencia para avaliar)")
print(f"Media: {fmt(av['nota'].mean(), 2)} | Mediana: {fmt(av['nota'].median(), 0)}")
alto = int((av["nota"] >= 4).sum())
print(linha("Engajamento alto ou muito alto (4 ou 5)", alto, na))
print("Distribuicao das notas:", av["nota"].astype(int).value_counts().sort_index().to_dict())

print("\nTabela 2 - media por tipo de ferramenta")
a_gami = av[av["gami"]]
a_trad = av[av["trad"] & ~av["gami"]]
print(f"  Usam ferramentas gamificadas: n = {len(a_gami)}, media = {fmt(media(a_gami['nota']), 2)}")
print(f"  Usam apenas plataformas tradicionais: n = {len(a_trad)}, media = {fmt(media(a_trad['nota']), 2)}")
print(f"  Total: n = {na}, media = {fmt(av['nota'].mean(), 2)}")
print(f"  Notas do grupo apenas tradicional: {sorted(a_trad['nota'].astype(int).tolist())}")

# Sinais de engajamento: exclui a resposta aberta de quem informou nao usar as plataformas
sin = v[~v["q10_sinais_l"].apply(lambda l: tem(l, "ainda não utiliza as plataformas"))]
sin = sin[sin["q10_sinais_l"].apply(len) > 0]
ns = len(sin)
print(f"\nSinais de engajamento (Figura 3) - n = {ns}, resposta multipla")
contagem(sin["q10_sinais_l"], ns)

# ----------------------------------------------------------------- 5.4 Gamificacao
titulo(f"5.4 ELEMENTOS DE GAMIFICACAO E COMPARACAO (Figuras 4 e 5)")
print(f"Elementos usados ou observados (Figura 4) - n = {n}, resposta multipla")
contagem(v["q11_elementos_l"], n)
print(f"\nDocentes com experiencia em gamificacao: {ng} de {n}")

def comparacao(base, rotulo):
    nb = len(base)
    print(f"\n{rotulo} (n = {nb})")
    for col, nome in [("q12_interesse", "Interesse"),
                      ("q13_persistencia", "Persistencia"),
                      ("q14_conclusao", "Conclusao das atividades")]:
        print(f" {nome}")
        for r, k in base[col].apply(limpa).value_counts().items():
            print(linha(r, k, nb))

comparacao(g, "Base principal: docentes com experiencia em gamificacao")
comparacao(v, "Analise de sensibilidade: base geral")

# ----------------------------------------------------------------- 5.5 Limitacoes
titulo(f"5.5 LIMITACOES, RISCOS E CONDICOES (Figuras 6 e 7) - n = {n}")
print("Limitacoes e riscos (Figura 6)")
contagem(v["q15_limitacoes_l"], n)
print("\nCondicoes (Figura 7)")
contagem(v["q16_condicoes_l"], n)

# ----------------------------------------------------------------- 5.6 Tabela 3
titulo("5.6 PRECISAO DAS ESTIMATIVAS (Tabela 3) - IC 95% de Wilson")
def cmp_maior(base, col):
    return int(base[col].apply(lambda t: "COM elementos" in str(t)).sum())

resultados = [
    ("Interesse maior com gamificacao (docentes com experiencia)", cmp_maior(g, "q12_interesse"), ng),
    ("Persistencia maior com gamificacao (docentes com experiencia)", cmp_maior(g, "q13_persistencia"), ng),
    ("Conclusao maior com gamificacao (docentes com experiencia)", cmp_maior(g, "q14_conclusao"), ng),
    ("Interesse maior com gamificacao (base geral; sensibilidade)", cmp_maior(v, "q12_interesse"), n),
    ("Engajamento geral alto ou muito alto", alto, na),
    ("Alinhamento aos objetivos pedagogicos",
     int(v["q16_condicoes_l"].apply(lambda l: tem(l, "alinhados aos objetivos")).sum()), n),
    ("Adequacao a idade e a turma",
     int(v["q16_condicoes_l"].apply(lambda l: tem(l, "adequados à idade")).sum()), n),
    ("Mediacao e acompanhamento do professor",
     int(v["q16_condicoes_l"].apply(lambda l: tem(l, "mediação e acompanhamento")).sum()), n),
    ("Falta de equipamentos, conexao ou suporte",
     int(v["q15_limitacoes_l"].apply(lambda l: tem(l, "Falta de equipamentos")).sum()), n),
    ("Competicao excessiva entre alunos",
     int(v["q15_limitacoes_l"].apply(lambda l: tem(l, "Competição excessiva")).sum()), n),
]
print(f"  {'Resultado':<62} {'Base':>4} {'n':>3} {'%':>6}   IC 95% (%)")
for rot, k, nb in resultados:
    lo, hi = wilson(k, nb)
    print(f"  {rot:<62} {nb:>4} {k:>3} {fmt(pct(k, nb)):>6}   {lo:.0f} a {hi:.0f}")

# ----------------------------------------------------------------- 5.7 Cruzamentos
titulo("5.7 CRUZAMENTOS EXPLORATORIOS (Tabela 4)")
v["infra"] = v["q15_limitacoes_l"].apply(lambda l: tem(l, "Falta de equipamentos"))
print("Estado x falta de infraestrutura")
for est in ["São Paulo", "Bahia"]:
    b = v[v["q3_estado"].str.contains(est, na=False)]
    print(linha(est, int(b["infra"].sum()), len(b)))

av = v[v["nota"].notna()].copy()
ate10 = ["Menos de 1 ano", "De 1 a 3 anos", "De 4 a 10 anos"]
av["carreira"] = av["q5_tempo"].apply(limpa).apply(lambda t: "Até 10 anos" if t in ate10 else "Mais de 10 anos")
print("\nTempo de docencia x engajamento (media, 1 a 5)")
for gr in ["Até 10 anos", "Mais de 10 anos"]:
    b = av[av["carreira"] == gr]
    print(f"  {gr:<36} n = {len(b)}  media = {fmt(media(b['nota']), 2)}")

print("\nFrequencia de uso x engajamento (media, 1 a 5)")
for r in ordem_f:
    b = av[av["q6_frequencia"].apply(limpa) == r]
    if len(b):
        print(f"  {r:<36} n = {len(b)}  media = {fmt(media(b['nota']), 2)}")

sem = av[av["nota"] != 1]
b = sem[sem["carreira"] == "Mais de 10 anos"]
print(f"\nSem a resposta de nota 1, media de 'Mais de 10 anos': {fmt(media(b['nota']), 2)} (n = {len(b)})")
print("\nFim da analise.")
