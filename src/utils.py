import json
from datetime import datetime
from typing import Dict, List, Optional


class Utils:
    @staticmethod
    def carregar_json(caminho: str) -> Dict:
        try:
            with open(caminho, "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Arquivo nao encontrado: {caminho}")
            return {}
        except json.JSONDecodeError:
            print(f"Erro ao decodificar JSON: {caminho}")
            return {}

    @staticmethod
    def salvar_json(dados: Dict, caminho: str) -> bool:
        try:
            with open(caminho, "w", encoding="utf-8") as f:
                json.dump(dados, f, ensure_ascii=False, indent=2)
            return True
        except OSError as e:
            print(f"Erro ao salvar JSON: {e}")
            return False

    @staticmethod
    def limpar_entrada(texto: str) -> str:
        return texto.strip().lower()

    @staticmethod
    def extrair_palavras_chave(texto: str) -> List[str]:
        palavras_comuns = {
            "o", "a", "os", "as", "um", "uma", "uns", "umas",
            "de", "em", "para", "por", "com", "sem", "sob",
            "sobre", "e", "sao", "esta", "estao", "foi", "foram",
        }
        palavras = texto.lower().split()
        return [p.strip(".,!?;:") for p in palavras if p not in palavras_comuns]

    @staticmethod
    def calcular_similaridade(texto1: str, texto2: str) -> float:
        palavras1 = set(Utils.extrair_palavras_chave(texto1))
        palavras2 = set(Utils.extrair_palavras_chave(texto2))
        if not palavras1 or not palavras2:
            return 0.0
        intersecao = len(palavras1 & palavras2)
        uniao = len(palavras1 | palavras2)
        return intersecao / uniao if uniao > 0 else 0.0

    @staticmethod
    def gerar_timestamp() -> str:
        return datetime.now().isoformat()

    @staticmethod
    def obter_estatisticas(historico: List[Dict]) -> Dict:
        usuario = len([h for h in historico if h["tipo"] == "usuario"])
        assistente = len([h for h in historico if h["tipo"] == "assistente"])
        return {
            "total_mensagens": len(historico),
            "mensagens_usuario": usuario,
            "mensagens_assistente": assistente,
            "taxa_resposta": (assistente / usuario) if usuario > 0 else 0,
        }


class Validador:
    @staticmethod
    def validar_pergunta(texto: str) -> tuple[bool, str]:
        if not texto:
            return False, "Pergunta vazia"
        if len(texto.strip()) < 3:
            return False, "Pergunta muito curta"
        if len(texto) > 1000:
            return False, "Pergunta muito longa"
        if not any(c.isalpha() for c in texto):
            return False, "Pergunta sem caracteres alfabeticos"
        return True, "OK"


if __name__ == "__main__":
    print("Testando Utils")

    texto_sujo = "  BRASIL  "
    print(f"Limpeza: '{texto_sujo}' -> '{Utils.limpar_entrada(texto_sujo)}'")

    pergunta = "Qual e o grupo do Brasil na Copa 2026?"
    print(f"Palavras-chave: {Utils.extrair_palavras_chave(pergunta)}")

    valido, motivo = Validador.validar_pergunta("Qual e a data da final?")
    print(f"Validacao: {valido} ({motivo})")

    sim = Utils.calcular_similaridade("Brasil na Copa", "Copa do Brasil")
    print(f"Similaridade: {sim:.2%}")

    print("Testes concluidos.")
