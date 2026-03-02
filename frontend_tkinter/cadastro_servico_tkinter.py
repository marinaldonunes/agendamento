import tkinter as tk
from tkinter import messagebox, ttk

from servico import Servico
from servicoDao import ServicoDao

try:
    from ._common import criar_conexao
except ImportError:
    from _common import criar_conexao


class TelaCadastroServico(ttk.Frame):
    def __init__(self, master, conexao):
        super().__init__(master, padding=12)
        self.conexao = conexao
        self.columnconfigure(1, weight=1)
        self._montar_form()
        self._montar_lista()
        self._carregar_servicos()

    def _montar_form(self):
        ttk.Label(self, text="Nome do serviço").grid(row=0, column=0, sticky="w", pady=4)
        self.nome_var = tk.StringVar()
        ttk.Entry(self, textvariable=self.nome_var).grid(row=0, column=1, sticky="ew", pady=4)

        ttk.Label(self, text="Duração (minutos)").grid(row=1, column=0, sticky="w", pady=4)
        self.duracao_var = tk.StringVar()
        ttk.Entry(self, textvariable=self.duracao_var).grid(row=1, column=1, sticky="ew", pady=4)

        botoes = ttk.Frame(self)
        botoes.grid(row=2, column=0, columnspan=2, sticky="e", pady=(8, 6))
        ttk.Button(botoes, text="Limpar", command=self._limpar).grid(row=0, column=0, padx=(0, 8))
        ttk.Button(botoes, text="Salvar", command=self._salvar).grid(row=0, column=1)

    def _montar_lista(self):
        cols = ("id", "nome_servico", "duracao_minutos")
        self.tree = ttk.Treeview(self, columns=cols, show="headings", height=10)
        self.tree.heading("id", text="ID")
        self.tree.heading("nome_servico", text="Serviço")
        self.tree.heading("duracao_minutos", text="Duração")
        self.tree.grid(row=3, column=0, columnspan=2, sticky="nsew")
        self.rowconfigure(3, weight=1)

    def _limpar(self):
        self.nome_var.set("")
        self.duracao_var.set("")

    def _salvar(self):
        nome = self.nome_var.get().strip()
        duracao_txt = self.duracao_var.get().strip()
        if not nome or not duracao_txt:
            messagebox.showerror("Validação", "Preencha nome e duração.")
            return
        if not duracao_txt.isdigit():
            messagebox.showerror("Validação", "Duração deve conter apenas números.")
            return

        serv = Servico(nome, int(duracao_txt))
        novo_id = ServicoDao.inserir_servico(self.conexao, serv)
        if novo_id == -1:
            messagebox.showerror("Erro", "Não foi possível cadastrar o serviço.")
            return

        messagebox.showinfo("Sucesso", f"Serviço cadastrado. ID: {novo_id}")
        self._limpar()
        self._carregar_servicos()

    def _carregar_servicos(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        registros = ServicoDao.consultar_servicos(self.conexao)
        if registros == -1:
            return
        for reg in registros:
            self.tree.insert("", tk.END, values=reg)


def main():
    conexao = criar_conexao()
    root = tk.Tk()
    root.title("Cadastro de Serviço")
    root.geometry("640x420")
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    frame = TelaCadastroServico(root, conexao)
    frame.grid(sticky="nsew")

    def ao_fechar():
        conexao.close()
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", ao_fechar)
    root.mainloop()


if __name__ == "__main__":
    main()
