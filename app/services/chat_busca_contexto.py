# app/services/chat_busca_contexto.py

from typing import List, Optional

def carregar_chat(texto: str) -> List[str]:
    return texto.splitlines()


def buscar_contexto_do_vcf(linhas: List[str], nome_vcf: str, janela: int = 3) -> Optional[str]:
    nome_vcf = nome_vcf.lower()

    for idx, linha in enumerate(linhas):
        if nome_vcf in linha.lower():
            inicio = max(0, idx - janela)
            fim = min(len(linhas), idx + janela + 1)
            return "\n".join(linhas[inicio:fim])

    return None