
from __future__ import annotations


class RecipeNode:

    def __init__(
        self,
        nome: str,
        tempo_preparo: str,
        ingredientes: list[str],
        modo_preparo: str,
        estrelas: int,
    ) -> None:
        nome_limpo = nome.strip()
        if not nome_limpo:
            raise ValueError("O nome da receita não pode ser vazio.")

        self.nome = nome_limpo
        self.tempo_preparo = tempo_preparo.strip()
        self.ingredientes = [item.strip() for item in ingredientes if item.strip()]
        self.modo_preparo = modo_preparo.strip()
        self.estrelas = self._validar_estrelas(estrelas)
        self.left: RecipeNode | None = None
        self.right: RecipeNode | None = None

    @staticmethod
    def _validar_estrelas(estrelas: int) -> int:
        """Garante que a avaliação esteja entre 1 e 5 estrelas."""
        valor = int(estrelas)
        if valor < 1 or valor > 5:
            raise ValueError("A avaliação em estrelas deve estar entre 1 e 5.")
        return valor

    @property
    def chave(self) -> str:
        """Retorna a chave de ordenação case-insensitive da receita."""
        return self.nome.lower()

    def atualizar(
        self,
        tempo_preparo: str,
        ingredientes: list[str],
        modo_preparo: str,
        estrelas: int,
    ) -> None:
        """Atualiza os dados da receita mantendo sua posição na árvore."""
        self.tempo_preparo = tempo_preparo.strip()
        self.ingredientes = [item.strip() for item in ingredientes if item.strip()]
        self.modo_preparo = modo_preparo.strip()
        self.estrelas = self._validar_estrelas(estrelas)

    def contem_ingrediente(self, termo: str) -> bool:
        """Verifica se algum ingrediente contém o termo buscado (case-insensitive)."""
        termo_limpo = termo.strip().lower()
        if not termo_limpo:
            return False
        return any(termo_limpo in ing.lower() for ing in self.ingredientes)

    def to_dict(self) -> dict[str, object]:
        """Converte os dados da receita em dicionário para serialização JSON."""
        return {
            "nome": self.nome,
            "tempo_preparo": self.tempo_preparo,
            "ingredientes": self.ingredientes,
            "modo_preparo": self.modo_preparo,
            "estrelas": self.estrelas,
        }

    @classmethod
    def from_dict(cls, dados: dict[str, object]) -> RecipeNode:
        """Cria um RecipeNode a partir de um dicionário carregado do JSON."""
        return cls(
            nome=str(dados["nome"]),
            tempo_preparo=str(dados["tempo_preparo"]),
            ingredientes=[str(item) for item in dados["ingredientes"]],  # type: ignore[union-attr]
            modo_preparo=str(dados["modo_preparo"]),
            estrelas=int(dados["estrelas"]),  # type: ignore[arg-type]
        )

    def formatar_ficha(self) -> str:
        """Retorna a ficha completa da receita formatada para exibição no terminal."""
        estrelas_visuais = "★" * self.estrelas + "☆" * (5 - self.estrelas)
        lista_ingredientes = "\n".join(f"  - {ing}" for ing in self.ingredientes)
        return (
            f"========================================\n"
            f"Prato: {self.nome}\n"
            f"Avaliação: {estrelas_visuais} ({self.estrelas}/5)\n"
            f"Tempo de preparo: {self.tempo_preparo}\n"
            f"Ingredientes:\n{lista_ingredientes}\n"
            f"Modo de preparo:\n  {self.modo_preparo}\n"
            f"========================================"
        )
