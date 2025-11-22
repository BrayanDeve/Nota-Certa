import tkinter as tk
from tkinter import messagebox, ttk
import csv
from datetime import datetime

# Variáveis globais
resultados = {}  # chave = matéria, valor = dict com acertos, erros, total, data
materia_atual = None
arquivo_csv = "resultados_materias.csv"
linhas_selecionadas = set()  # para simular checkbox único

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
root = tk.Tk()
root.title("Contador de Acertos e Erros")
root.geometry("820x520")
root.resizable(False, False)

# Top
top_frame = tk.Frame(root, pady=10)
top_frame.pack(fill="x")
tk.Label(top_frame, text="Qual é a matéria?", font=("Arial", 12)).pack(side="left", padx=5)
material = tk.StringVar()
tk.Entry(top_frame, textvariable=material, width=35, font=("Arial", 12)).pack(side="left", padx=5)
tk.Button(top_frame, text="Próxima", width=10, font=("Arial", 11), command=proxima).pack(side="left", padx=5)

# Contadores
count_frame = tk.Frame(root, pady=10)
count_frame.pack()
tk.Button(count_frame, text="Acerto", width=12, font=("Arial", 11), bg="#4CAF50", fg="white", command=registrar_acerto).pack(side="left", padx=5)
tk.Button(count_frame, text="Erro", width=12, font=("Arial", 11), bg="#F44336", fg="white", command=registrar_erro).pack(side="left", padx=5)
tk.Button(count_frame, text="Zerar", width=12, font=("Arial", 11), bg="#FFC107", command=zerar).pack(side="left", padx=5)

# Labels
lbl_frame = tk.Frame(root, pady=10)
lbl_frame.pack()
lbl_acertos = tk.Label(lbl_frame, text="Acertos: 0", font=("Arial", 12))
lbl_acertos.pack(side="left", padx=15)
lbl_erros = tk.Label(lbl_frame, text="Erros: 0", font=("Arial", 12))
lbl_erros.pack(side="left", padx=15)
lbl_total = tk.Label(lbl_frame, text="Total: 0", font=("Arial", 12))
lbl_total.pack(side="left", padx=15)

# Ações
action_frame = tk.Frame(root, pady=10)
action_frame.pack()
tk.Button(action_frame, text="Excluir", width=12, font=("Arial", 11), command=excluir).pack(side="left", padx=5)
tk.Button(action_frame, text="Salvar CSV", width=12, font=("Arial", 11), command=salvar).pack(side="left", padx=5)
tk.Button(action_frame, text="Sair", width=12, font=("Arial", 11), bg="#9E9E9E", command=sair).pack(side="left", padx=30)

# Tabela com checkbox
tabela_frame = tk.Frame(root)
tabela_frame.pack(pady=10, fill="both", expand=True)
tree = ttk.Treeview(
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
tree.tag_configure('evenrow', background="#F0F0F0")
tree.tag_configure('oddrow', background="#FFFFFF")

tree.bind("<Button-1>", toggle_checkbox)
tree.bind("<<TreeviewSelect>>", selecionar_materia)

root.mainloop()
