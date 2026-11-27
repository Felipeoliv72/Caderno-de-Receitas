"""Interface de linha de comando (CLI) para o Caderno de Receitas."""

from __future__ import annotations

from src.storage import load_recipes, save_recipes
from src.tree import RecipeTree


def _ler_texto_obrigatorio(mensagem: str) -> str:
    """Solicita uma entrada de texto não vazia ao usuário."""
    while True:
        valor = input(mensagem).strip()
        if valor:
            return valor
        print("Valor inválido. Este campo não pode ficar vazio.")


def _ler_ingredientes() -> list[str]:
    """Lê uma lista de ingredientes separados por vírgula."""
    while True:
        entrada = input("Ingredientes (separados por vírgula): ").strip()
        ingredientes = [item.strip() for item in entrada.split(",") if item.strip()]
        if ingredientes:
            return ingredientes
        print("Informe pelo menos um ingrediente válido.")


def _ler_estrelas() -> int:
    """Lê e valida a avaliação de 1 a 5 estrelas."""
    while True:
        entrada = input("Avaliação (1 a 5 estrelas): ").strip()
        try:
            estrelas = int(entrada)
            if 1 <= estrelas <= 5:
                return estrelas
        except ValueError:
            pass
        print("Digite um número inteiro entre 1 e 5.")


def _exibir_menu() -> None:
    """Exibe as opções principais do sistema."""
    print("\n=== 📖 Caderno de Receitas (BST) ===")
    print("1. Cadastrar / Atualizar receita")
    print("2. Buscar receita por nome")
    print("3. Listar todas as receitas (A-Z)")
    print("4. Filtrar receitas por ingrediente")
    print("5. Remover receita")
    print("6. Sair")


def _cadastrar_ou_atualizar(tree: RecipeTree) -> None:
    print("\n--- Cadastrar / Atualizar Receita ---")
    nome = _ler_texto_obrigatorio("Nome do prato: ")
    tempo_preparo = _ler_texto_obrigatorio("Tempo de preparo (ex: 30 min): ")
    ingredientes = _ler_ingredientes()
    modo_preparo = _ler_texto_obrigatorio("Modo de preparo: ")
    estrelas = _ler_estrelas()

    inserida = tree.insert(nome, tempo_preparo, ingredientes, modo_preparo, estrelas)
    save_recipes(tree)

    if inserida:
        print(f"Receita '{nome}' cadastrada com sucesso!")
    else:
        print(f"Receita '{nome}' já existia e foi atualizada com sucesso!")


def _buscar_receita(tree: RecipeTree) -> None:
    print("\n--- Buscar Receita ---")
    nome = _ler_texto_obrigatorio("Nome do prato: ")
    receita = tree.search(nome)
    if receita is None:
        print(f"Nenhuma receita encontrada com o nome '{nome}'.")
        return
    print(receita.formatar_ficha())


def _listar_receitas(tree: RecipeTree) -> None:
    print("\n--- Receitas Cadastradas (A-Z) ---")
    receitas = tree.in_order()
    if not receitas:
        print("O caderno de receitas está vazio.")
        return

    for idx, receita in enumerate(receitas, start=1):
        estrelas = "★" * receita.estrelas + "☆" * (5 - receita.estrelas)
        print(f"{idx}. {receita.nome} | {estrelas} | {receita.tempo_preparo}")


def _filtrar_por_ingrediente(tree: RecipeTree) -> None:
    print("\n--- Filtrar por Ingrediente ---")
    termo = _ler_texto_obrigatorio("Ingrediente desejado: ")
    encontradas = tree.filter_by_ingredient(termo)
    if not encontradas:
        print(f"Nenhuma receita encontrada com o ingrediente '{termo}'.")
        return

    print(f"\nReceitas com '{termo}' ({len(encontradas)}):")
    for idx, receita in enumerate(encontradas, start=1):
        estrelas = "★" * receita.estrelas + "☆" * (5 - receita.estrelas)
        print(f"{idx}. {receita.nome} | {estrelas} | {receita.tempo_preparo}")


def _remover_receita(tree: RecipeTree) -> None:
    print("\n--- Remover Receita ---")
    nome = _ler_texto_obrigatorio("Nome do prato a remover: ")
    if tree.delete(nome):
        save_recipes(tree)
        print(f"Receita '{nome}' removida com sucesso!")
    else:
        print(f"Nenhuma receita encontrada com o nome '{nome}'.")


def run_cli() -> None:
    """Inicia o loop interativo do Caderno de Receitas."""
    tree = load_recipes()
    acoes = {
        "1": _cadastrar_ou_atualizar,
        "2": _buscar_receita,
        "3": _listar_receitas,
        "4": _filtrar_por_ingrediente,
        "5": _remover_receita,
    }

    try:
        while True:
            _exibir_menu()
            opcao = input("Escolha uma opção: ").strip()

            if opcao == "6":
                save_recipes(tree)
                print("Dados salvos. Até logo!")
                break

            acao = acoes.get(opcao)
            if acao is None:
                print("Opção inválida. Escolha um número de 1 a 6.")
                continue

            acao(tree)
    except (KeyboardInterrupt, EOFError):
        save_recipes(tree)
        print("\nEncerrando... Dados salvos.")
