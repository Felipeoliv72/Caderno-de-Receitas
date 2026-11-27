"""Módulo que implementa a Árvore Binária de Busca de receitas (RecipeTree)."""

from __future__ import annotations

from src.node import RecipeNode


class RecipeTree:
    """Árvore Binária de Busca (BST) ordenada pelo nome da receita (case-insensitive)."""

    def __init__(self) -> None:
        self.root: RecipeNode | None = None

    def is_empty(self) -> bool:
        """Retorna True se a árvore estiver vazia, caso contrário False."""
        return self.root is None

    def insert(
        self,
        nome: str,
        tempo_preparo: str,
        ingredientes: list[str],
        modo_preparo: str,
        estrelas: int,
    ) -> bool:
        """Insere uma nova receita ou atualiza os dados se o nome já existir.

        Retorna True para nova inserção e False para atualização.
        """
        novo_no = RecipeNode(nome, tempo_preparo, ingredientes, modo_preparo, estrelas)
        return self.insert_node(novo_no)

    def insert_node(self, new_node: RecipeNode) -> bool:
        """Insere um RecipeNode na árvore (ou atualiza se a chave já existir)."""
        if self.is_empty():
            self.root = new_node
            return True
        return self._insert_recursive(self.root, new_node)  # type: ignore[arg-type]

    def _insert_recursive(self, current_node: RecipeNode, new_node: RecipeNode) -> bool:
        if new_node.chave < current_node.chave:
            if current_node.left is None:
                current_node.left = new_node
                return True
            return self._insert_recursive(current_node.left, new_node)

        if new_node.chave > current_node.chave:
            if current_node.right is None:
                current_node.right = new_node
                return True
            return self._insert_recursive(current_node.right, new_node)

        current_node.atualizar(
            new_node.tempo_preparo,
            new_node.ingredientes,
            new_node.modo_preparo,
            new_node.estrelas,
        )
        return False

    def search(self, nome: str) -> RecipeNode | None:
        """Busca uma receita pelo nome em O(log n) médio (case-insensitive)."""
        chave = nome.strip().lower()
        if not chave:
            return None
        return self._search_recursive(self.root, chave)

    def _search_recursive(
        self, current_node: RecipeNode | None, chave: str
    ) -> RecipeNode | None:
        if current_node is None:
            return None
        if chave == current_node.chave:
            return current_node
        if chave < current_node.chave:
            return self._search_recursive(current_node.left, chave)
        return self._search_recursive(current_node.right, chave)

    def in_order(self) -> list[RecipeNode]:
        """Retorna todas as receitas em ordem alfabética (Esq -> Raiz -> Dir)."""
        resultado: list[RecipeNode] = []
        self._in_order_recursive(self.root, resultado)
        return resultado

    def _in_order_recursive(
        self, node: RecipeNode | None, resultado: list[RecipeNode]
    ) -> None:
        if node:
            self._in_order_recursive(node.left, resultado)
            resultado.append(node)
            self._in_order_recursive(node.right, resultado)

    def filter_by_ingredient(self, termo: str) -> list[RecipeNode]:
        """Retorna em ordem alfabética as receitas que contêm o ingrediente buscado."""
        return [
            node for node in self.in_order() if node.contem_ingrediente(termo)
        ]

    def pre_order(self) -> list[RecipeNode]:
        """Retorna as receitas em Pre-Order (Raiz -> Esq -> Dir) para persistência."""
        resultado: list[RecipeNode] = []
        self._pre_order_recursive(self.root, resultado)
        return resultado

    def _pre_order_recursive(
        self, node: RecipeNode | None, resultado: list[RecipeNode]
    ) -> None:
        if node:
            resultado.append(node)
            self._pre_order_recursive(node.left, resultado)
            self._pre_order_recursive(node.right, resultado)

    def delete(self, nome: str) -> bool:
        """Remove uma receita tratando os 3 casos da BST. Retorna True se removida."""
        chave = nome.strip().lower()
        if not chave:
            return False
        self.root, removed = self._delete_recursive(self.root, chave)
        return removed

    def _delete_recursive(
        self, current_node: RecipeNode | None, chave: str
    ) -> tuple[RecipeNode | None, bool]:
        if current_node is None:
            return None, False

        if chave < current_node.chave:
            current_node.left, removed = self._delete_recursive(
                current_node.left, chave
            )
            return current_node, removed

        if chave > current_node.chave:
            current_node.right, removed = self._delete_recursive(
                current_node.right, chave
            )
            return current_node, removed

        # Caso 1: nó folha
        if current_node.left is None and current_node.right is None:
            return None, True

        # Caso 2: nó com apenas 1 filho
        if current_node.left is None:
            return current_node.right, True
        if current_node.right is None:
            return current_node.left, True

        # Caso 3: nó com 2 filhos -> substitui pelo sucessor In-Order
        sucessor = self._min_node(current_node.right)
        current_node.nome = sucessor.nome
        current_node.atualizar(
            sucessor.tempo_preparo,
            sucessor.ingredientes,
            sucessor.modo_preparo,
            sucessor.estrelas,
        )
        current_node.right, _ = self._delete_recursive(
            current_node.right, sucessor.chave
        )
        return current_node, True

    @staticmethod
    def _min_node(node: RecipeNode) -> RecipeNode:
        """Retorna o nó com a menor chave da subárvore informada."""
        atual = node
        while atual.left is not None:
            atual = atual.left
        return atual
