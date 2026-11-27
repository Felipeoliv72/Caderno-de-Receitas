"""Módulo de persistência em JSON e carga inicial de receitas."""

from __future__ import annotations

import json
import os

from src.node import RecipeNode
from src.tree import RecipeTree

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_DATA_PATH = os.path.join(BASE_DIR, "data", "receitas.json")

EXEMPLOS_INICIAIS: list[dict[str, object]] = [
    {
        "nome": "Macarrão à Bolonhesa",
        "tempo_preparo": "40 min",
        "ingredientes": ["macarrão", "carne moída", "molho de tomate", "alho", "cebola", "azeite"],
        "modo_preparo": "Refogue a carne moída com alho e cebola, adicione o molho e sirva sobre o macarrão cozido.",
        "estrelas": 5,
    },
    {
        "nome": "Feijoada Simples",
        "tempo_preparo": "1h 30min",
        "ingredientes": ["feijão preto", "linguiça calabresa", "bacon", "alho", "cebola"],
        "modo_preparo": "Cozinhe o feijão na pressão, refogue as carnes com alho e cebola e junte tudo para apurar.",
        "estrelas": 5,
    },
    {
        "nome": "Salada Caesar",
        "tempo_preparo": "20 min",
        "ingredientes": ["alface americana", "peito de frango", "croutons", "queijo parmesão", "molho caesar"],
        "modo_preparo": "Grelhe o frango em tiras, misture com a alface rasgada, croutons, parmesão e o molho.",
        "estrelas": 4,
    },
    {
        "nome": "Bolo de Cenoura",
        "tempo_preparo": "45 min",
        "ingredientes": ["cenoura", "ovos", "óleo", "açúcar", "farinha de trigo", "fermento"],
        "modo_preparo": "Bata cenoura, ovos e óleo no liquidificador, misture aos secos e asse a 180°C por 35 minutos.",
        "estrelas": 5,
    },
    {
        "nome": "Guacamole",
        "tempo_preparo": "15 min",
        "ingredientes": ["abacate", "tomate", "cebola roxa", "limão", "coentro", "sal"],
        "modo_preparo": "Amasse o abacate, misture os demais ingredientes picados e tempere com limão e sal.",
        "estrelas": 4,
    },
    {
        "nome": "Panqueca de Banana",
        "tempo_preparo": "15 min",
        "ingredientes": ["banana", "ovo", "aveia", "canela"],
        "modo_preparo": "Amasse a banana, misture com ovo, aveia e canela e doure dos dois lados na frigideira.",
        "estrelas": 4,
    },
    {
        "nome": "Torta de Limão",
        "tempo_preparo": "50 min",
        "ingredientes": ["biscoito maisena", "manteiga", "leite condensado", "creme de leite", "limão"],
        "modo_preparo": "Faça a base com biscoito e manteiga, cubra com o mousse de limão e leve para gelar.",
        "estrelas": 5,
    },
]


def save_recipes(tree: RecipeTree, filepath: str = DEFAULT_DATA_PATH) -> None:
    """Salva as receitas da árvore em JSON usando percurso Pre-Order."""
    pasta = os.path.dirname(filepath)
    if pasta:
        os.makedirs(pasta, exist_ok=True)

    dados = [node.to_dict() for node in tree.pre_order()]
    with open(filepath, "w", encoding="utf-8") as arquivo:
        json.dump(dados, arquivo, ensure_ascii=False, indent=2)


def load_recipes(filepath: str = DEFAULT_DATA_PATH) -> RecipeTree:
    """Carrega as receitas do JSON preservando a topologia, ou cria exemplos iniciais."""
    tree = RecipeTree()

    if not os.path.exists(filepath):
        for exemplo in EXEMPLOS_INICIAIS:
            tree.insert_node(RecipeNode.from_dict(exemplo))
        save_recipes(tree, filepath)
        return tree

    try:
        with open(filepath, "r", encoding="utf-8") as arquivo:
            dados = json.load(arquivo)
    except (json.JSONDecodeError, OSError):
        return tree

    if isinstance(dados, list):
        for item in dados:
            if isinstance(item, dict):
                tree.insert_node(RecipeNode.from_dict(item))

    return tree
