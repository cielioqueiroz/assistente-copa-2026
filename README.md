# Copa 2026 AI: Assistente Virtual sobre a Copa do Mundo

Assistente virtual que responde perguntas sobre a Copa do Mundo FIFA 2026 a partir de uma base de conhecimento estruturada. Projeto final do Lab "Construa Seu Assistente Virtual Com Inteligencia Artificial" da DIO.

## Visao Geral

O Copa 2026 AI recebe uma pergunta em texto e responde com base nos dados do arquivo `data/base_conhecimento.json`. Quando a informacao nao existe na base, ele avisa que nao tem o dado em vez de inventar uma resposta.

O assistente funciona em dois modos:

- IA generativa: quando ha uma chave da API do Google Gemini configurada, ele envia a pergunta, a base de conhecimento e as instrucoes do sistema para o modelo Gemini, que entende a linguagem natural e responde de forma contextualizada. Ele usa a base como fonte principal e, quando a pergunta foge da base, faz uma busca na web em tempo real (Google Search) e cita a fonte.
- Busca local: quando nao ha chave configurada, ele cai num modo offline que identifica o assunto por palavras-chave e monta a resposta direto da base. Assim o projeto roda sem custo e sem internet.

Publico-alvo: torcedores e qualquer pessoa que queira consultar rapidamente informacoes da Copa 2026.

## O que o assistente faz

- Responde sobre selecoes e em qual grupo cada uma esta
- Mostra os jogadores em destaque cadastrados na base
- Lista as datas importantes do torneio
- Apresenta os favoritos segundo a base, deixando claro que sao estimativas
- Avisa quando nao tem a informacao pedida
- Guarda o historico da conversa em memoria durante a sessao

## Estrutura do Projeto

```
assistente-copa-2026/
├── README.md
├── PITCH.md
├── requirements.txt
├── demo_notebook.ipynb
├── data/
│   └── base_conhecimento.json
├── docs/
│   ├── DOCUMENTACAO.md
│   ├── PROMPTS.md
│   └── METRICAS.md
└── src/
    ├── assistente.py
    └── utils.py
```

## Como Rodar

Requer Python 3.9 ou superior.

Instale as dependencias:

```bash
pip install -r requirements.txt
```

### Configurar a IA generativa (opcional)

Para usar o modo de IA generativa, pegue uma chave gratuita do Google Gemini em https://aistudio.google.com/apikey, copie `.env.example` para `.env` e preencha:

```
GEMINI_API_KEY=sua-chave-aqui
```

Sem essa chave, o assistente roda no modo de busca local.

### Chat web (recomendado)

```bash
streamlit run src/app.py
```

Abre um chat no navegador. A barra lateral mostra o modo ativo (IA ou local).

### No terminal

```bash
python src/assistente.py
```

O assistente mostra na abertura qual modo esta ativo (IA generativa ou busca local). Digite suas perguntas e use `sair` para encerrar.

### No navegador (Jupyter Notebook)

```bash
pip install -r requirements.txt
jupyter notebook demo_notebook.ipynb
```

O notebook abre no navegador e roda o assistente passo a passo.

## Exemplos de Uso

```
Voce: qual o grupo do brasil?
Assistente: Brasil esta no Grupo E (CONMEBOL).
Adversarios no grupo: Colombia, Suica, Coreia do Sul.

Voce: quem sao os favoritos?
Assistente: Favoritos para a Copa 2026 (segundo a base): ...

Voce: quando e a final?
Assistente: Datas importantes da Copa 2026: ...
```

## Os 6 Passos do Desafio

1. Documentacao: este README e a pasta `docs/`
2. Base de conhecimento: `data/base_conhecimento.json`
3. Prompts: `docs/PROMPTS.md` e o roteamento em `src/assistente.py`
4. Aplicacao funcional: `src/assistente.py` e `demo_notebook.ipynb`
5. Avaliacao e metricas: `docs/METRICAS.md`
6. Pitch: `PITCH.md`

## Limitacoes Conhecidas

- A base de conhecimento e pequena e cobre apenas parte das selecoes e jogadores.
- No modo de busca local (sem chave de API), o entendimento e por palavras-chave, entao perguntas muito fora dos exemplos caem na resposta generica.
- O modo de IA generativa depende de uma chave do Google Gemini (nivel gratuito).
- Os dados sao estaticos e precisam ser atualizados manualmente no JSON.

## Possiveis Melhorias

- Ampliar a base com todas as selecoes e mais jogadores
- Conectar a uma API esportiva para dados atualizados
- Criar uma interface web de chat
- Suporte a mais idiomas

## Autor

Jacielio (Cielio) Queiroz

Projeto desenvolvido para o Desafio Final da DIO, Trilha Bradesco Dados, Ciberseguranca e GenAI.
