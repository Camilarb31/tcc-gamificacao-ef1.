# Gamificação e plataformas educacionais digitais

Material complementar do Trabalho de Conclusão de Curso **"Gamificação e plataformas educacionais digitais: a percepção de professores sobre o engajamento de alunos do Ensino Fundamental I"**, do curso de Ciência de Dados da Univesp (TCC530, Turma 010).

Este repositório reúne a base de dados e o script usados no trabalho, para que os resultados possam ser reproduzidos (Apêndice C).

## Arquivos

| Arquivo | Descrição |
|---|---|
| `base_anonimizada.csv` | 23 respostas ao questionário on-line, coletadas de 23/09/2026 a 14/10/2026. |
| `analise_tcc.py` | Script em Python que calcula os resultados das seções 5.1 a 5.7 do trabalho. |
| `README.md` | Este arquivo. |

## Sobre a base

- Contém as 23 respostas recebidas até o encerramento da coleta. O script aplica o filtro de elegibilidade (questão 2) e chega às **17 respostas válidas**, de docentes que atuam ou atuaram no Ensino Fundamental I nos últimos dois anos.
- Cada linha é uma resposta, identificada por número sequencial (`id`).
- Colunas: `id`, `q1_consentimento`, `q2_atua_ef1`, `q3_estado`, `q4_rede`, `q5_tempo`, `q6_frequencia`, `q7_plataformas`, `q8_finalidade`, `q9_engajamento`, `q10_sinais`, `q11_elementos`, `q12_interesse`, `q13_persistencia`, `q14_conclusao`, `q15_limitacoes`, `q16_condicoes`.
- Nas questões de múltipla escolha, as alternativas aparecem separadas por ponto e vírgula (`;`).
- Foram removidos a data e hora de resposta e o contato opcional da questão 17. A base não contém nomes nem dados de contato.
- Arquivo em UTF-8. **Não altere a base**: os resultados do trabalho foram calculados sobre a base congelada na data de encerramento da coleta.

## Requisitos

- Python 3.9 ou superior
- Biblioteca `pandas`

```bash
pip install pandas
```

## Como executar

1. Salve `analise_tcc.py` e `base_anonimizada.csv` na mesma pasta.
2. Abra o terminal nessa pasta.
3. Execute:

```bash
python analise_tcc.py base_anonimizada.csv
```

O resultado é impresso no terminal, na ordem das seções do trabalho.

## O que o script calcula

| Seção do TCC | Conteúdo |
|---|---|
| 5.1 | Perfil dos participantes (Tabela 1) |
| 5.2 | Plataformas, ferramentas e finalidades (Figura 1; categorias do Quadro 2) |
| 5.3 | Engajamento: média, mediana e comparação por tipo de ferramenta (Figuras 2 e 3; Tabela 2) |
| 5.4 | Elementos de gamificação e comparação entre atividades (Figuras 4 e 5), com a base principal de 12 docentes e a análise de sensibilidade com os 17 |
| 5.5 | Limitações, riscos e condições (Figuras 6 e 7) |
| 5.6 | Principais resultados com intervalo de confiança de 95% pelo método de Wilson (Tabela 3) |
| 5.7 | Cruzamentos exploratórios (Tabela 4) |

## Resultados de referência

Para conferir se a execução deu certo, estes valores devem aparecer:

- Respostas na base: **23**; respostas válidas: **17**; docentes com experiência em gamificação: **12**.
- Interesse maior com gamificação (base de 12): **8 de 12 (66,7%; IC 95%: 39 a 86)**.
- Média de engajamento (12 docentes que avaliaram): **3,58**, mediana **4**.
- Falta de equipamentos, conexão ou suporte: **8 de 17 (47,1%)**.
- Alinhamento aos objetivos pedagógicos: **17 de 17**.

## Observações

- O script classifica as ferramentas em categorias conforme o Quadro 2 do trabalho. A resposta aberta "Escola games, elefante letrado, Matific, etc." é tratada como ferramenta gamificada, e o Canva não entra em nenhuma categoria.
- O script gera apenas tabelas em texto. Não produz os gráficos das Figuras 1 a 7.
- Os resultados descrevem o grupo estudado (amostra pequena e por conveniência) e não podem ser generalizados.

## Autores

Camila Rodrigues Batista, Elisabete Cezar de Paula, Guilherme Consolação Dias, José Roberto de Andrade Salgueiro, Josias Correa de Menezes e Wester Alexandre Gobetti.

Orientador: Gessé Gerônimo Pereira Evangelista.

Universidade Virtual do Estado de São Paulo (Univesp), 2026.
