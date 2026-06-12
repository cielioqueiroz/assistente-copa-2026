# Avaliacao - Copa 2026 AI

Este documento registra como o assistente foi testado. Os testes foram feitos manualmente, executando o assistente e comparando a resposta com o que esta na base de conhecimento.

## Como a avaliacao foi feita

Para cada pergunta, verifiquei dois pontos:

1. O assistente roteou para a categoria certa (selecoes, jogadores, datas ou favoritos)?
2. A resposta bate com o dado que esta em `data/base_conhecimento.json`?

## Casos de teste

| # | Pergunta | Esperado | Resultado |
|---|----------|----------|-----------|
| 1 | "qual o grupo do brasil?" | Grupo C (Marrocos, Haiti, Escocia) | OK |
| 2 | "quem sao os favoritos?" | Lista de favoritos da base | OK |
| 3 | "fale sobre messi" | Dados do Messi da base | OK |
| 4 | "quando e a final?" | 19 de julho de 2026, no MetLife Stadium | OK |
| 5 | "qual o grupo de portugal?" | Grupo K (RD Congo, Uzbequistao, Colombia) | OK |
| 6 | "quanto custa o ingresso?" | Resposta generica (dado nao existe na base) | OK |

## O que funcionou bem

- O roteamento por palavras-chave acerta as perguntas diretas usadas nos testes.
- O assistente le os dados da base, entao a resposta fica consistente com o JSON.
- Quando a informacao nao existe (caso 6), ele cai na resposta generica em vez de inventar.

## Limitacoes observadas

- Perguntas com escrita muito diferente dos exemplos podem cair na resposta generica.
- A base e pequena: selecoes e jogadores nao cadastrados nao tem resposta especifica.
- Nao ha analise de contexto entre perguntas (cada pergunta e tratada de forma isolada).

## Proximos passos de avaliacao

- Montar um conjunto maior de perguntas e medir a taxa de acerto de forma sistematica.
- Testar variacoes de escrita (apelidos, erros de digitacao) para medir a robustez do roteamento.
