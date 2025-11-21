# tests/test_autocategoria.py

from app.services.autocategoria import (
    detectar_nova_categoria,
    registrar_sugestao_categoria,
    promover_categorias
)


def test_detectar_nova_categoria_simples():
    texto = "ele instala esquadrias de alumínio"
    categoria = detectar_nova_categoria(texto)
    assert categoria == "esquadrias"


def test_registrar_e_promover_categoria(db_session):
    termo = "esquadrias"

    # Registrar 3 vezes → suficiente para promover
    for _ in range(3):
        registrar_sugestao_categoria(db_session, termo)

    promovidas = promover_categorias(db_session)

    assert "esquadrias" in promovidas