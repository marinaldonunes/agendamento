import tkinter as tk
from tkinter import messagebox, ttk

from profissional import Profissional
from profissionalDao import ProfissionalDao

try:
    from ._common import criar_conexao
except ImportError:
    from _common import criar_conexao


class TelaCadastroProfissional(ttk.Frame):
    def __init__(self, master, conexao):
        super().__init__(master, padding=12)
        self.conexao = conexao
        self.columnconfigure(1, weight=1)
        self._montar_form()
        self._montar_lista()
        self._carregar_profissionais()

    def _montar_form(self):
        ttk.Label(self, text="Nome").grid(row=0, column=0, sticky="w", pady=3)
        self.nome_var = tk.StringVar()
        ttk.Entry(self, textvariable=self.nome_var).grid(row=0, column=1, sticky="ew", pady=3)

        ttk.Label(self, text="Sobrenome").grid(row=1, column=0, sticky="w", pady=3)
        self.sobrenome_var = tk.StringVar()
        ttk.Entry(self, textvariable=self.sobrenome_var).grid(row=1, column=1, sticky="ew", pady=3)

        ttk.Label(self, text="N. registro").grid(row=2, column=0, sticky="w", pady=3)
        self.registro_var = tk.StringVar()
        ttk.Entry(self, textvariable=self.registro_var).grid(row=2, column=1, sticky="ew", pady=3)

        ttk.Label(self, text="UF").grid(row=3, column=0, sticky="w", pady=3)
        self.uf_var = tk.StringVar()
        ttk.Entry(self, textvariable=self.uf_var, width=4).grid(row=3, column=1, sticky="w", pady=3)

        ttk.Label(self, text="Conselho").grid(row=4, column=0, sticky="w", pady=3)
        self.conselho_var = tk.StringVar()
        ttk.Entry(self, textvariable=self.conselho_var).grid(row=4, column=1, sticky="ew", pady=3)

        ttk.Label(self, text="Contatos (um por linha)").grid(row=5, column=0, sticky="nw", pady=3)
        self.contatos_txt = tk.Text(self, height=4, width=40)
        self.contatos_txt.grid(row=5, column=1, sticky="ew", pady=3)

        botoes = ttk.Frame(self)
        botoes.grid(row=6, column=0, columnspan=2, sticky="e", pady=(8, 6))
        ttk.Button(botoes, text="Limpar", command=self._limpar).grid(row=0, column=0, padx=(0, 8))
        ttk.Button(botoes, text="Salvar", command=self._salvar).grid(row=0, column=1)

    def _montar_lista(self):
        cols = ("id", "nome", "sobrenome", "registro", "uf", "conselho")
        self.tree = ttk.Treeview(self, columns=cols, show="headings", height=8)
        for col, texto in (
            ("id", "ID"),
            ("nome", "Nome"),
            ("sobrenome", "Sobrenome"),
            ("registro", "Registro"),
            ("uf", "UF"),
            ("conselho", "Conselho"),
        ):
            self.tree.heading(col, text=texto)
        self.tree.grid(row=7, column=0, columnspan=2, sticky="nsew")
        self.rowconfigure(7, weight=1)

    def _limpar(self):
        self.nome_var.set("")
        self.sobrenome_var.set("")
        self.registro_var.set("")
        self.uf_var.set("")
        self.conselho_var.set("")
        self.contatos_txt.delete("1.0", tk.END)

    def _salvar(self):
        nome = self.nome_var.get().strip()
        sobrenome = self.sobrenome_var.get().strip()
        if not nome or not sobrenome:
            messagebox.showerror("Validação", "Nome e sobrenome são obrigatórios.")
            return

        prof = Profissional(
            nome,
            sobrenome,
            self.registro_var.get().strip() or " ",
            self.uf_var.get().strip().upper() or " ",
            self.conselho_var.get().strip().upper() or " ",
        )
        contatos = [linha.strip() for linha in self.contatos_txt.get("1.0", tk.END).splitlines() if linha.strip()]
        prof.set_contatos(contatos)

        novo_id = ProfissionalDao.insere_profissional(self.conexao, prof)
        if novo_id == -1:
            messagebox.showerror("Erro", "Não foi possível salvar o profissional.")
            return

        messagebox.showinfo("Sucesso", f"Profissional cadastrado. ID: {novo_id}")
        self._limpar()
        self._carregar_profissionais()

    def _carregar_profissionais(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for reg in ProfissionalDao.consulta_profissionais(self.conexao):
            self.tree.insert("", tk.END, values=reg)


def main():
    conexao = criar_conexao()
    root = tk.Tk()
    root.title("Cadastro de Profissional")
    root.geometry("760x520")
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    frame = TelaCadastroProfissional(root, conexao)
    frame.grid(sticky="nsew")

    def ao_fechar():
        conexao.close()
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", ao_fechar)
    root.mainloop()


if __name__ == "__main__":
    main()
