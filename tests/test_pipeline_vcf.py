# tests/test_pipeline_vcf.py

import vobject
from app.routers.vcf import extrair_vcf
from app.services.classificacao_avancada import classificar_inteligente


def test_extrair_vcf():
    v = vobject.vCard()
    v.add('fn').value = "João Pintor"
    v.add('tel').value = "(11) 99999-1111"
    v.add('note').value = "pintura interna"
    raw = v.serialize().encode("utf-8")

    nome, telefone, email, notas = extrair_vcf(raw)

    assert nome == "João Pintor"
    assert "99999" in telefone
    assert notas == "pintura interna"


def test_classificacao_por_vcf():
    texto = "João Pintor pintura interna"
    categoria = classificar_inteligente(texto)
    assert categoria == "pintor"