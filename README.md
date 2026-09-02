# NotaCerta

Aplicativo desktop simples para registrar acertos e erros de questões por matéria durante os estudos, acompanhar o percentual de acerto e exportar os resultados em CSV.

## Funcionalidades

- Registro de acertos e erros por matéria.
- Contadores em tempo real (acertos, erros, total).
- Tabela com histórico de todas as matérias registradas, incluindo percentual de acerto e data do último registro.
- Seleção de uma matéria na tabela (clique) para marcá-la.
- Exclusão de matérias (com confirmação).
- Zerar contadores de uma matéria (com confirmação).
- Exportação dos resultados para `resultados_materias.csv`.

## Como executar

### Opção 1 — Executável (`NotaCerta.exe`)

Basta rodar `NotaCerta.exe`, sem necessidade de instalar Python ou dependências.

### Opção 2 — Código-fonte (`NotaCerta.py`)

Requer Python 3.10+ instalado.

```bash
pip install -r requirements.txt
python NotaCerta.py
```

> No Windows, se o comando `python` não for encontrado, use `py` no lugar (`py NotaCerta.py`).

## Gerando o executável

O `.exe` é gerado com [PyInstaller](https://pyinstaller.org/). Como o app usa `ttkbootstrap` (fontes/ícones do tema são carregados como arquivos, não como código), é necessário incluir `--collect-all ttkbootstrap` no build:

```bash
pip install pyinstaller
pyinstaller --onefile --windowed --name NotaCerta --collect-all ttkbootstrap NotaCerta.py
```

O executável gerado fica na raiz do projeto (`dist/` é ignorado pelo `.gitignore` — mova o `.exe` para a raiz, ou ajuste `--distpath .`).

## Estrutura do projeto

| Arquivo | Descrição |
|---|---|
| `NotaCerta.py` | Código-fonte da aplicação (Tkinter + ttkbootstrap). |
| `NotaCerta.exe` | Executável standalone para Windows. |
| `requirements.txt` | Dependências Python do projeto. |
| `resultados_materias.csv` | Gerado ao clicar em "Salvar CSV" (não versionado). |

## Stack

- Python 3 + Tkinter (`ttk.Treeview` para a tabela)
- [ttkbootstrap](https://ttkbootstrap.readthedocs.io/) para o tema visual (`flatly`)
