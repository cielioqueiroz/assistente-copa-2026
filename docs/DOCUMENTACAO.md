# Documentacao Tecnica - Copa 2026 AI

## 1. Visao Geral

O Copa 2026 AI e um assistente que responde perguntas sobre a Copa do Mundo 2026 a partir de uma base de conhecimento em JSON. Ele pode ser usado de tres formas: no terminal, num notebook Jupyter e num chat web (Streamlit). O fluxo de uma pergunta e:

```
Pergunta -> normalizacao do texto -> identificacao do assunto -> base de conhecimento (e busca web no modo IA) -> resposta
```

A normalizacao deixa o texto em minusculas e remove acentos, para que "Suica" e "Suica" sejam tratados igual.

## 2. Persona e Tom de Voz

- Quem ele e: um especialista entusiasmado em futebol e na Copa do Mundo 2026.
- Como fala: em portugues, de forma clara, amigavel e objetiva. Usa listas e destaques quando ajuda a entender.
- Postura: neutro entre as selecoes, nao torce nem favorece ninguem.
- Honestidade: prefere dizer "nao tenho esse dado" a inventar uma resposta. Apresenta favoritos como estimativas, nunca como previsao certa.
- Limites: foca em assuntos da Copa 2026 (selecoes, grupos, jogadores, datas, favoritos).

## 3. Base de Conhecimento

Arquivo: `data/base_conhecimento.json`

Estrutura principal:

```json
{
  "copa_2026": {
    "informacoes_gerais": {},
    "grupos_e_chaveamento": {},
    "favoritos": {},
    "jogadores_destaque": {},
    "datas_importantes": [],
    "curiosidades": []
  }
}
```

O assistente le essa base na inicializacao e usa os dados para montar as respostas. Para incluir uma nova selecao ou jogador, basta editar o JSON, sem mexer no codigo.

## 4. Componentes do Codigo

### src/assistente.py

Classe `AssistenteCopa2026`:

- `_carregar_base_conhecimento()`: le o JSON e retorna o no `copa_2026`.
- `_iniciar_ia()`: ativa o modo de IA generativa se houver chave de API.
- `responder(pergunta)`: registra a pergunta no historico, gera a resposta e registra a resposta.
- `_responder_com_ia(pergunta)`: chama o modelo Gemini (com tentativas automaticas em erros temporarios).
- `_gerar_resposta(pergunta)`: no modo local, identifica o assunto por palavras-chave e chama o metodo correspondente.
- `_responder_selecoes`, `_responder_jogadores`, `_responder_datas`, `_responder_favoritos`, `_responder_generico`: montam a resposta a partir da base.

Funcao `normalizar(texto)`: minusculas e remocao de acentos.

### src/app.py

Chat web em Streamlit que reutiliza a classe `AssistenteCopa2026`. Mostra o modo ativo (IA ou local) e mantem o historico da conversa na sessao.

### src/utils.py

Funcoes auxiliares independentes (carregar/salvar JSON, extrair palavras-chave, similaridade simples entre textos, validacao de pergunta).

## 5. Roteamento de Assuntos (modo local)

| Assunto | Palavras-chave (exemplos) |
|---------|---------------------------|
| Favoritos | favorito, campeao, vai ganhar, chance |
| Datas | data, quando, calendario, final, abertura |
| Jogadores | jogador, tecnico, messi, neymar, mbappe |
| Selecoes | selecao, grupo, equipe, pais, time |
| Generico | qualquer pergunta que nao caia nos anteriores |

## 6. Tratamento de Casos

- Pergunta sem assunto reconhecido: resposta generica com o menu de assuntos.
- Selecao ou jogador nao encontrado na base: aviso de que o dado nao existe.
- Entrada vazia: pedido para digitar uma pergunta.

## 7. Modos de Funcionamento

O assistente tem dois modos, escolhidos automaticamente na inicializacao:

- IA generativa: ativado quando existe a variavel de ambiente `GEMINI_API_KEY`. O metodo `_responder_com_ia` usa o SDK oficial do Google Gemini (`google-genai`) e chama o modelo `gemini-2.5-flash` numa sessao de chat que ja recebe o texto de sistema com a base de conhecimento em JSON. O modelo responde em linguagem natural usando a base como fonte principal. A sessao tambem tem a ferramenta de busca do Google (Google Search grounding) ativada: quando a pergunta foge da base, o modelo busca na web em tempo real e cita a fonte.
- Busca local: usado quando nao ha chave. As respostas vem do roteamento por palavras-chave descrito acima, sem depender de internet nem de API.

Se uma chamada a API falhar, o assistente cai automaticamente para a busca local, entao ele nunca fica sem resposta.

A chave da API e lida da variavel de ambiente (ou de um arquivo `.env`), nunca do codigo.

## 8. Seguranca e Anti-Alucinacao

O setor onde o assistente atua exige cuidado para nao passar informacao errada. As protecoes:

- Resposta ancorada na base: o prompt de sistema instrui o modelo a usar primeiro a base de conhecimento e a nao inventar dados.
- Admitir limites: quando a informacao nao existe, o assistente diz que nao tem o dado, em vez de chutar.
- Busca com fonte: no modo IA, perguntas fora da base sao respondidas com busca na web e citacao da fonte, o que reduz alucinacao.
- Favoritos como estimativa: probabilidades e palpites sao apresentados como opiniao/estimativa, nunca como fato.
- Fallback seguro: se a IA falhar, a resposta vem da base local, que so contem dados conferidos.
- Chave protegida: a chave de API fica no arquivo `.env`, fora do controle de versao (`.gitignore`).

## 9. Possiveis Extensoes

- Conectar a uma API esportiva para dados de jogos em tempo real.
- Ampliar a base de conhecimento (mais jogadores, tabela de jogos).
- Adicionar suporte a mais idiomas.
- Publicar o chat web (Streamlit) online.
