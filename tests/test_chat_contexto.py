# tests/test_chat_contexto.py

from app.services.chat_busca_contexto import buscar_contexto_do_vcf


def test_busca_contexto():
    linhas = [
        "oi pessoal",
        "segue o contato",
        "fulanodasilva.vcf",
        "ele é muito bom",
        "recomendo"
    ]

    contexto = buscar_contexto_do_vcf(linhas, "fulanodasilva.vcf")
    assert "ele é muito bom" in contexto