from tkinter import messagebox
import ttkbootstrap as tb
import csv
from datetime import datetime

# Variáveis globais
resultados = {}  # chave = matéria, valor = dict com acertos, erros, total, data
materia_atual = None
arquivo_csv = "resultados_materias.csv"
linhas_selecionadas = set()  # para simular checkbox único

# --- Paleta de cores ---
FONTE = "Segoe UI"

COR_FUNDO = "#F8FAFC"
COR_SUPERFICIE = "#FFFFFF"
COR_TEXTO = "#1E293B"
COR_TEXTO_SECUNDARIO = "#64748B"
COR_BORDA = "#E2E8F0"

COR_SUCESSO = "#2E7D32"
COR_SUCESSO_HOVER = "#256428"
COR_PERIGO = "#DC2626"
COR_PERIGO_HOVER = "#B91C1C"
COR_ALERTA = "#F59E0B"
COR_ALERTA_HOVER = "#D97F06"
COR_SECUNDARIO = "#475569"
COR_SECUNDARIO_HOVER = "#334155"

COR_LINHA_PAR = "#FFFFFF"
COR_LINHA_IMPAR = "#F1F5F9"
COR_LINHA_SELECIONADA_BG = "#DBEAFE"
COR_CABECALHO_BG = "#EEF2F7"
COR_CABECALHO_FG = "#334155"

# Funções
def atualizar_labels():
    if materia_atual:
        dados = resultados[materia_atual]
        lbl_acertos.config(text=f"Acertos: {dados['acertos']}")
        lbl_erros.config(text=f"Erros: {dados['erros']}")
        lbl_total.config(text=f"Total: {dados['total']}")
    else:
        lbl_acertos.config(text="Acertos: 0")
        lbl_erros.config(text="Erros: 0")
        lbl_total.config(text="Total: 0")

def registrar_acerto():
    global materia_atual
    mat = material.get().strip()
    if not mat:
        messagebox.showwarning("Atenção", "Digite o nome da matéria!")
        return
    if mat not in resultados:
        resultados[mat] = {"acertos":0, "erros":0, "total":0, "data": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
    materia_atual = mat
    resultados[mat]["acertos"] += 1
    resultados[mat]["total"] = resultados[mat]["acertos"] + resultados[mat]["erros"]
    resultados[mat]["data"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    atualizar_labels()
    atualizar_tabela()

def registrar_erro():
    global materia_atual
    mat = material.get().strip()
    if not mat:
        messagebox.showwarning("Atenção", "Digite o nome da matéria!")
        return
    if mat not in resultados:
        resultados[mat] = {"acertos":0, "erros":0, "total":0, "data": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
    materia_atual = mat
    resultados[mat]["erros"] += 1
    resultados[mat]["total"] = resultados[mat]["acertos"] + resultados[mat]["erros"]
    resultados[mat]["data"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    atualizar_labels()
    atualizar_tabela()

def zerar():
    global materia_atual
    if materia_atual:
        confirmar = messagebox.askyesno(
            "Confirmar",
            f"Deseja realmente zerar os contadores de \"{materia_atual}\"?\n\nEssa ação não pode ser desfeita."
        )
        if not confirmar:
            return
        resultados[materia_atual] = {"acertos":0, "erros":0, "total":0, "data": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
        atualizar_labels()
        atualizar_tabela()
        material.set("")

def proxima():
    global materia_atual
    materia_atual = None
    material.set("")
    # Desmarca qualquer linha marcada
    linhas_selecionadas.clear()
    atualizar_tabela()
    atualizar_labels()

def salvar():
    if not resultados:
        messagebox.showwarning("Atenção", "Não há resultados para salvar!")
        return
    try:
        with open(arquivo_csv, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["Selecionado","Matéria", "Acertos", "Erros", "Total", "Porcentagem", "Data"])
            for mat, dados in resultados.items():
                pct = calcular_porcentagem(dados)
                sel = "✅" if mat in linhas_selecionadas else "⬜"
                writer.writerow([sel, mat, dados["acertos"], dados["erros"], dados["total"], f"{pct:.1f}%", dados["data"]])
        messagebox.showinfo("Salvo", f"Resultados salvos no arquivo '{arquivo_csv}'")
    except Exception as e:
        messagebox.showerror("Erro", f"Não foi possível salvar o arquivo: {e}")

def excluir():
    global materia_atual
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Atenção", "Selecione uma matéria para excluir!")
        return
    materias = [tree.item(item, 'values')[1] for item in selected]
    lista = ", ".join(f'"{m}"' for m in materias)
    rotulo = "a matéria" if len(materias) == 1 else "as matérias"
    confirmar = messagebox.askyesno(
        "Confirmar exclusão",
        f"Deseja realmente excluir {rotulo} {lista}?\n\n"
        "Essa ação não pode ser desfeita e os dados serão perdidos caso ainda não tenham sido salvos em CSV."
    )
    if not confirmar:
        return
    for item in selected:
        mat = tree.item(item, 'values')[1]
        if mat in resultados:
            del resultados[mat]
        if mat in linhas_selecionadas:
            linhas_selecionadas.remove(mat)
    atualizar_tabela()
    materia_atual = None
    atualizar_labels()

def calcular_porcentagem(dados):
    if dados["total"] == 0:
        return 0
    return (dados["acertos"] / dados["total"]) * 100

def atualizar_tabela():
    for item in tree.get_children():
        tree.delete(item)
    for i, (mat, dados) in enumerate(resultados.items()):
        pct = calcular_porcentagem(dados)
        sel = "✅" if mat in linhas_selecionadas else "⬜"
        tag = 'evenrow' if i % 2 == 0 else 'oddrow'
        tree.insert("", "end", values=(sel, mat, dados["acertos"], dados["erros"], dados["total"], f"{pct:.1f}%", dados["data"]), tags=(tag,))

def toggle_checkbox(event):
    item = tree.identify_row(event.y)
    if item:
        mat = tree.item(item, "values")[1]
        # Limpa seleção anterior (apenas um checkbox marcado)
        linhas_selecionadas.clear()
        linhas_selecionadas.add(mat)
        atualizar_tabela()

def selecionar_materia(event):
    global materia_atual
    selected = tree.selection()
    if selected:
        item = selected[0]
        mat = tree.item(item, 'values')[1]
        materia_atual = mat
        material.set(mat)
        atualizar_labels()

def sair():
    root.destroy()

# --- Janela principal ---
root = tb.Window(title="Contador de Acertos e Erros", themename="flatly", size=(900, 580), resizable=(False, False))
root.configure(background=COR_FUNDO)

style = root.style

# Estilos base
style.configure("TFrame", background=COR_FUNDO)
style.configure("TLabel", background=COR_FUNDO, foreground=COR_TEXTO, font=(FONTE, 12))
style.configure("TEntry", fieldbackground=COR_SUPERFICIE, foreground=COR_TEXTO, padding=6)

# Estilos de métricas
style.configure("Metric.Success.TLabel", background=COR_FUNDO, foreground=COR_SUCESSO, font=(FONTE, 14, "bold"))
style.configure("Metric.Danger.TLabel", background=COR_FUNDO, foreground=COR_PERIGO, font=(FONTE, 14, "bold"))
style.configure("Metric.TLabel", background=COR_FUNDO, foreground=COR_TEXTO, font=(FONTE, 14, "bold"))

# Estilos de botões (ação principal, em negrito, cores com contraste WCAG AA)
style.configure("Success.TButton", background=COR_SUCESSO, foreground="white", font=(FONTE, 11, "bold"), padding=8)
style.map("Success.TButton", background=[("active", COR_SUCESSO_HOVER)])

style.configure("Danger.TButton", background=COR_PERIGO, foreground="white", font=(FONTE, 11, "bold"), padding=8)
style.map("Danger.TButton", background=[("active", COR_PERIGO_HOVER)])

style.configure("Warning.TButton", background=COR_ALERTA, foreground=COR_TEXTO, font=(FONTE, 11, "bold"), padding=8)
style.map("Warning.TButton", background=[("active", COR_ALERTA_HOVER)])

# Estilos de botões secundários (ações neutras/menos frequentes)
style.configure("Secondary.TButton", background=COR_SECUNDARIO, foreground="white", font=(FONTE, 11), padding=8)
style.map("Secondary.TButton", background=[("active", COR_SECUNDARIO_HOVER)])

style.configure("Outline.TButton", background=COR_FUNDO, foreground=COR_TEXTO_SECUNDARIO, font=(FONTE, 10), padding=6)

root.title("Contador de Acertos e Erros")

# Container geral com margem uniforme
container = tb.Frame(root, padding=20)
container.pack(fill="both", expand=True)

# Top
top_frame = tb.Frame(container, padding=(0, 0, 0, 10))
top_frame.pack(fill="x")
tb.Label(top_frame, text="Qual é a matéria?", font=(FONTE, 12)).pack(side="left", padx=8)
material = tb.StringVar()
tb.Entry(top_frame, textvariable=material, width=35, font=(FONTE, 12)).pack(side="left", padx=8)
tb.Button(top_frame, text="Próxima", width=10, style="Secondary.TButton", command=proxima).pack(side="left", padx=8)

# Contadores
count_frame = tb.Frame(container, padding=(0, 0, 0, 10))
count_frame.pack()
tb.Button(count_frame, text="Acerto", width=14, style="Success.TButton", command=registrar_acerto).pack(side="left", padx=8)
tb.Button(count_frame, text="Erro", width=14, style="Danger.TButton", command=registrar_erro).pack(side="left", padx=8)
tb.Button(count_frame, text="Zerar", width=14, style="Warning.TButton", command=zerar).pack(side="left", padx=8)

# Labels
lbl_frame = tb.Frame(container, padding=(0, 0, 0, 10))
lbl_frame.pack()
lbl_acertos = tb.Label(lbl_frame, text="Acertos: 0", style="Metric.Success.TLabel")
lbl_acertos.pack(side="left", padx=25)
lbl_erros = tb.Label(lbl_frame, text="Erros: 0", style="Metric.Danger.TLabel")
lbl_erros.pack(side="left", padx=25)
lbl_total = tb.Label(lbl_frame, text="Total: 0", style="Metric.TLabel")
lbl_total.pack(side="left", padx=25)

# Ações
action_frame = tb.Frame(container, padding=(0, 0, 0, 10))
action_frame.pack()
tb.Button(action_frame, text="Excluir", width=12, style="Danger.TButton", command=excluir).pack(side="left", padx=5)
tb.Button(action_frame, text="Salvar CSV", width=12, style="Secondary.TButton", command=salvar).pack(side="left", padx=5)
tb.Button(action_frame, text="Sair", width=12, style="Outline.TButton", command=sair).pack(side="left", padx=30)

# Tabela com checkbox
tabela_frame = tb.Frame(container)
tabela_frame.pack(pady=10, fill="both", expand=True)

style.configure(
    "Treeview",
    background=COR_SUPERFICIE,
    fieldbackground=COR_SUPERFICIE,
    foreground=COR_TEXTO,
    rowheight=28,
    font=(FONTE, 10),
    bordercolor=COR_BORDA,
    borderwidth=1,
)
style.configure(
    "Treeview.Heading",
    background=COR_CABECALHO_BG,
    foreground=COR_CABECALHO_FG,
    font=(FONTE, 10, "bold"),
    relief="flat",
)
style.map(
    "Treeview",
    background=[("selected", COR_LINHA_SELECIONADA_BG)],
    foreground=[("selected", COR_TEXTO)],
)

tree = tb.Treeview(
    tabela_frame,
    columns=("sel","matéria", "acertos", "erros", "total", "pct", "data"),
    show="headings",
    height=12
)
tree.heading("sel", text="✔")
tree.heading("matéria", text="Matéria")
tree.heading("acertos", text="Acertos")
tree.heading("erros", text="Erros")
tree.heading("total", text="Total")
tree.heading("pct", text="% de Acerto")
tree.heading("data", text="Último registro")
tree.column("sel", width=40, anchor="center")
tree.column("matéria", width=200)
tree.column("acertos", width=80, anchor="center")
tree.column("erros", width=80, anchor="center")
tree.column("total", width=80, anchor="center")
tree.column("pct", width=100, anchor="center")
tree.column("data", width=180, anchor="center")
tree.pack(fill="both", expand=True)

# Configura cores alternadas das linhas
tree.tag_configure('evenrow', background=COR_LINHA_PAR)
tree.tag_configure('oddrow', background=COR_LINHA_IMPAR)

tree.bind("<Button-1>", toggle_checkbox)
tree.bind("<<TreeviewSelect>>", selecionar_materia)

root.mainloop()
