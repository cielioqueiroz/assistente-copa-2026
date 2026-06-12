# Prompts e Regras de Resposta - Copa 2026 AI

O assistente tem dois modos. No modo de IA generativa, o texto de sistema abaixo e a base de conhecimento sao enviados ao modelo Gemini, que gera a resposta. No modo de busca local (sem chave de API), valem as mesmas diretrizes, mas a resposta e montada por regras de roteamento e leitura direta da base.

## 1. Texto de Sistema

O texto enviado ao modelo, junto com a base de conhecimento em JSON:

```
Voce e o Copa 2026 AI, um assistente sobre a Copa do Mundo FIFA 2026.
Responde em portugues, de forma clara e amigavel, usando apenas a base de
conhecimento fornecida abaixo. Nunca invente dados, estatisticas ou resultados.
Quando a informacao nao estiver na base, diga que nao tem esse dado.
Apresente os favoritos como estimativas da base, nao como previsao certa.
```

Diretrizes que esse texto resume:

1. Usar apenas dados da base de conhecimento.
2. Avisar quando nao tem a informacao, em vez de inventar.
3. Apresentar favoritos como estimativas, nao como previsao.
4. Manter neutralidade entre as selecoes.

## 2. Regras por Assunto (modo de busca local)

Quando nao ha chave de API, o assistente identifica o assunto da pergunta por palavras-chave e monta a resposta a partir da base. No modo de IA generativa, o proprio modelo cuida disso a partir do texto de sistema.

### Selecoes

Procura o nome do pais na base de grupos e responde com o grupo e os adversarios. Se nao achar, lista as selecoes disponiveis.

Exemplo:
```
Voce: qual o grupo do brasil?
Assistente: Brasil esta no Grupo C (CONMEBOL).
Adversarios no grupo: Marrocos, Haiti, Escocia.
```

### Jogadores

Procura o nome (ou parte do nome) na lista de jogadores em destaque e devolve posicao, clube, idade e destaque.

Exemplo:
```
Voce: fale sobre messi
Assistente: Lionel Messi
Posicao: Atacante
Clube: Inter Miami
...
```

### Datas

Lista as datas importantes cadastradas na base.

### Favoritos

Lista os favoritos da base com a probabilidade e o motivo, sempre lembrando que sao estimativas.

### Generico

Quando a pergunta nao cai em nenhum assunto, mostra o menu de assuntos que o assistente cobre.

## 3. Respostas a Evitar

O assistente foi pensado para nao fazer estas coisas:

- Inventar dados, estatisticas ou resultados que nao estao na base.
- Cravar um campeao como se fosse previsao certa.
- Favorecer uma selecao em detrimento de outra.

## 4. Como a IA e Chamada

No modo de IA generativa, o assistente usa o SDK oficial do Google Gemini (`google-genai`). Ele cria uma sessao de chat com o texto de sistema (que ja inclui a base de conhecimento) e envia cada pergunta para o modelo `gemini-2.5-flash`. A sessao tem a busca do Google (Google Search grounding) ativada, entao o modelo usa a base como fonte principal e busca na web quando a pergunta foge dela. A chave da API vem da variavel de ambiente `GEMINI_API_KEY`, nunca do codigo. Se a chamada falhar, o assistente responde usando a busca local.
