# Caderno-de-Receitas
# 📖 Caderno de Receitas Pessoais (Árvore Binária de Busca)

Sistema de linha de comando (CLI) desenvolvido em **Python** para organizar, consultar e gerenciar receitas culinárias utilizando uma **Árvore Binária de Busca (BST)** como estrutura principal de armazenamento em memória e persistência em arquivo JSON.

---

## 🎯 Objetivo

Aplicar conceitos fundamentais de **Estrutura de Dados** — como modelagem de nós com múltiplos atributos, inserção recursiva ordenada, busca binária ($O(\log n)$), percursos em profundidade (*In-Order* e *Pre-Order*) e remoção de nós — em uma aplicação prática do dia a dia.

---

## 🧠 Como a Estrutura de Dados Funciona

Cada nó da árvore (`RecipeNode`) armazena uma receita completa, utilizando o **nome do prato** como chave de comparação para manter a ordenação alfabética:

* **Chave de ordenação:** `nome` (comparação *case-insensitive*, enviando valores menores para a subárvore esquerda e maiores para a direita).
* **Dados armazenados no nó:**
  * `tempo_preparo`: Tempo estimado de execução.
  * `ingredientes`: Lista de ingredientes do prato.
  * `modo_preparo`: Instruções de preparo.
  * `estrelas`: Avaliação pessoal de 1 a 5 estrelas.

### Uso dos Percursos na Aplicação

| Operação | Técnica / Percurso | Finalidade |
| :--- | :--- | :--- |
| **Busca por prato** | Busca Binária ($O(\log n)$) | Localiza uma receita exata descartando metade da árvore a cada nível. |
| **Listagem geral (A–Z)** | *In-Order* (`Esq -> Raiz -> Dir`) | Exibe todas as receitas cadastradas automaticamente em ordem alfabética. |
| **Filtro por ingrediente** | *In-Order* com filtro | Percorre os nós e retorna, em ordem alfabética, todos os pratos que contêm o ingrediente pesquisado. |
| **Salvar e carregar dados** | *Pre-Order* (`Raiz -> Esq -> Dir`) | Exporta os registros para `receitas.json` preservando a topologia original da árvore ao reiniciar o programa. |

---

## ✨ Funcionalidades

* **Cadastrar / Atualizar receita:** Insere um novo prato na árvore ou atualiza os dados caso o nome já exista.
* **Buscar receita por nome:** Exibe a ficha completa (tempo, ingredientes, preparo e nota) de um prato específico.
* **Listar receitas (A–Z):** Mostra o índice completo do caderno em ordem alfabética.
* **Filtrar por ingrediente:** Busca pratos com base em um ingrediente disponível (ex.: `"abacate"`, `"carne moída"`).
* **Remover receita:** Exclui um nó da árvore tratando os 3 casos da BST (nó folha, nó com 1 filho e nó com 2 filhos via sucessor *In-Order*).
* **Persistência automática:** Salva e carrega os dados localmente em `receitas.json`.

---

## 🛠️ Tecnologias Utilizadas

* **Python 3.x** (bibliotecas nativas `json` e `os`, sem dependências externas).
