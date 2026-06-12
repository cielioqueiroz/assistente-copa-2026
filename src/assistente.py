import json
import os
import sys
import time
import unicodedata
from datetime import datetime

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

MODELO_IA = "gemini-2.5-flash"


def normalizar(texto):
    texto = texto.lower().strip()
    texto = unicodedata.normalize("NFD", texto)
    return "".join(c for c in texto if unicodedata.category(c) != "Mn")


class AssistenteCopa2026:
    def __init__(self):
        self.nome = "Copa 2026 AI"
        self.versao = "1.0"
        self.historico = []
        self.base = self._carregar_base_conhecimento()
        self.sistema_prompt = self._criar_sistema_prompt()
        self.chat_ia = self._iniciar_ia()

    def _iniciar_ia(self):
        chave = os.environ.get("GEMINI_API_KEY")
        if not chave:
            return None
        try:
            from google import genai
            from google.genai import types
        except ImportError:
            return None
        self.cliente_gemini = genai.Client(api_key=chave)
        config = types.GenerateContentConfig(
            system_instruction=self.sistema_prompt,
            tools=[types.Tool(google_search=types.GoogleSearch())],
        )
        return self.cliente_gemini.chats.create(model=MODELO_IA, config=config)

    def usando_ia(self):
        return self.chat_ia is not None

    def _carregar_base_conhecimento(self):
        caminho = os.path.join(os.path.dirname(__file__), "..", "data", "base_conhecimento.json")
        try:
            with open(caminho, "r", encoding="utf-8") as f:
                dados = json.load(f)
            return dados.get("copa_2026", {})
        except FileNotFoundError:
            print("Base de conhecimento nao encontrada. Usando dados vazios.")
            return {}
        except json.JSONDecodeError:
            print("Erro ao ler a base de conhecimento.")
            return {}

    def _criar_sistema_prompt(self):
        return (
            "Voce e o Copa 2026 AI, um assistente sobre a Copa do Mundo FIFA 2026. "
            "Responde em portugues, de forma clara e amigavel. "
            "Use sempre primeiro a base de conhecimento fornecida abaixo. "
            "Se a informacao nao estiver na base, use a busca no Google para encontrar "
            "dados atuais e cite a fonte. Nunca invente dados, estatisticas ou resultados. "
            "Apresente os favoritos como estimativas, nao como previsao certa.\n\n"
            "BASE DE CONHECIMENTO (JSON):\n"
            + json.dumps(self.base, ensure_ascii=False)
        )

    def _registrar(self, tipo, conteudo):
        self.historico.append({
            "timestamp": datetime.now().isoformat(),
            "tipo": tipo,
            "conteudo": conteudo,
        })

    def responder(self, pergunta_usuario):
        self._registrar("usuario", pergunta_usuario)
        if self.usando_ia():
            resposta = self._responder_com_ia(pergunta_usuario)
        else:
            resposta = self._gerar_resposta(pergunta_usuario)
        self._registrar("assistente", resposta)
        return resposta

    def _responder_com_ia(self, pergunta):
        transitorios = ["503", "UNAVAILABLE", "429", "overloaded", "high demand", "RESOURCE_EXHAUSTED"]
        ultimo_erro = None
        for tentativa in range(3):
            try:
                return self.chat_ia.send_message(pergunta).text
            except Exception as e:
                ultimo_erro = e
                if any(marca in str(e) for marca in transitorios):
                    time.sleep(2 * (tentativa + 1))
                    continue
                break
        return (
            "Nao consegui falar com a IA agora (" + str(ultimo_erro) + "). "
            "Respondendo com a busca local:\n\n" + self._gerar_resposta(pergunta)
        )

    def _gerar_resposta(self, pergunta):
        p = normalizar(pergunta)

        if any(t in p for t in ["favorito", "campeao", "vai ganhar", "vai vencer", "chance"]):
            return self._responder_favoritos()
        if any(t in p for t in ["data", "quando", "calendario", "jogo", "final", "abertura"]):
            return self._responder_datas()
        if any(t in p for t in ["jogador", "tecnico", "craque", "atacante", "messi", "neymar", "mbappe", "vinicius"]):
            return self._responder_jogadores(p)
        if any(t in p for t in ["selecao", "grupo", "equipe", "pais", "time"]):
            return self._responder_selecoes(p)
        return self._responder_generico()

    def _responder_selecoes(self, p):
        grupos = self.base.get("grupos_e_chaveamento", {})
        for grupo in grupos.values():
            for equipe in grupo.get("equipes", []):
                pais = equipe.get("pais", "")
                if pais and normalizar(pais) in p:
                    companheiros = [
                        e["pais"] for e in grupo["equipes"]
                        if normalizar(e["pais"]) != normalizar(pais)
                    ]
                    return (
                        f"{pais} esta no {grupo['nome']} ({equipe.get('confederacao', '')}).\n"
                        f"Adversarios no grupo: {', '.join(companheiros)}."
                    )

        nomes = []
        for grupo in grupos.values():
            for equipe in grupo.get("equipes", []):
                if equipe.get("pais") and equipe["pais"] != "Por ser confirmado":
                    nomes.append(equipe["pais"])
        if nomes:
            return (
                "Nao encontrei essa selecao na base. "
                "Selecoes disponiveis: " + ", ".join(sorted(set(nomes))) + "."
            )
        return "Nao tenho dados de selecoes na base."

    def _responder_jogadores(self, p):
        jogadores = self.base.get("jogadores_destaque", {})
        for lista in jogadores.values():
            for jogador in lista:
                nome = jogador.get("nome", "")
                partes = [normalizar(parte) for parte in nome.split()]
                if any(parte in p for parte in partes if len(parte) > 3):
                    return (
                        f"{nome}\n"
                        f"Posicao: {jogador.get('posicao', '')}\n"
                        f"Clube: {jogador.get('clube_atual', '')}\n"
                        f"Idade: {jogador.get('idade', '')}\n"
                        f"Destaque: {jogador.get('destaque', '')}"
                    )
        return "Nao tenho esse jogador na base. Pergunte sobre Neymar, Vinicius, Messi ou Mbappe."

    def _responder_datas(self):
        datas = self.base.get("datas_importantes", [])
        if not datas:
            return "Nao tenho datas na base."
        linhas = ["Datas importantes da Copa 2026:"]
        for item in datas:
            linhas.append(f"{item['data']}: {item['evento']} ({item['local']})")
        return "\n".join(linhas)

    def _responder_favoritos(self):
        favoritos = self.base.get("favoritos", {}).get("equipes_principais", [])
        if not favoritos:
            return "Nao tenho dados de favoritos na base."
        linhas = ["Favoritos para a Copa 2026 (segundo a base):"]
        for time in favoritos:
            linhas.append(f"{time['ranking']}. {time['pais']} - {time.get('motivo', '')}")
        linhas.append("Sao apenas estimativas: o titulo nao esta decidido.")
        return "\n".join(linhas)

    def _responder_generico(self):
        return (
            "Sou o Copa 2026 AI. Posso responder sobre:\n"
            "- Selecoes e grupos\n"
            "- Jogadores em destaque\n"
            "- Datas importantes\n"
            "- Favoritos\n"
            "O que voce gostaria de saber?"
        )

    def iniciar_conversa(self):
        print(f"{self.nome} v{self.versao}")
        print("Assistente sobre a Copa do Mundo 2026.")
        if self.usando_ia():
            print(f"Modo: IA generativa ({MODELO_IA}).")
        else:
            print("Modo: busca local (defina GEMINI_API_KEY para usar a IA generativa).")
        print("Digite sua pergunta ou 'sair' para encerrar.")

        while True:
            pergunta = input("\nVoce: ").strip()
            if pergunta.lower() in ["sair", "exit", "quit"]:
                print("Ate logo.")
                break
            if not pergunta:
                print("Por favor, digite uma pergunta.")
                continue
            print("\nAssistente:")
            print(self.responder(pergunta))

    def contar_interacoes(self):
        return len([h for h in self.historico if h["tipo"] == "usuario"])


def main():
    assistente = AssistenteCopa2026()
    assistente.iniciar_conversa()


if __name__ == "__main__":
    main()
