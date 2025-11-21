# tests/test_classificacao.py

from app.services.classificacao_avancada import classificar_inteligente


def test_classificacao_regras_simples():
    texto = "Preciso de um bom pintor"
    categoria = classificar_inteligente(texto)
    assert categoria == "pintor"


def test_classificacao_embedding_sem_palavra_clara():
    texto = "ele arrumou meu disjuntor"
    categoria = classificar_inteligente(texto)
    assert categoria == "eletricista"