import tkinter as tk
from tkinter import messagebox, ttk

try:
    from ._common import criar_conexao
except ImportError:
    from _common import criar_conexao

from servico import Servico
from servicoDao import ServicoDao


class TelaCadastroServico(ttk.Frame):
    def __init__(self, master, conexao):
        super().__init__(master, padding=12)
        self.conexao = conexao
        self.columnconfigure(1, weight=1)
        self._montar_form()
        self._montar_lista()
        self._carregar_servicos()

    def _montar_form(self):
        ttk.Label(self, text="ID").grid(row=0, column=0, sticky="w", pady=4)
        self.id_var = tk.StringVar()
        ttk.Entry(self, textvariable=self.id_var, state="readonly", width=10).grid(
            row=0, column=1, sticky="w", pady=4
        )

        ttk.Label(self, text="Nome do serviço").grid(row=1, column=0, sticky="w", pady=4)
        self.nome_var = tk.StringVar()
        ttk.Entry(self, textvariable=self.nome_var).grid(row=1, column=1, sticky="ew", pady=4)

        ttk.Label(self, text="Duração (minutos)").grid(row=2, column=0, sticky="w", pady=4)
        self.duracao_var = tk.StringVar()
        ttk.Entry(self, textvariable=self.duracao_var).grid(row=2, column=1, sticky="ew", pady=4)

        botoes = ttk.Frame(self)
        botoes.grid(row=3, column=0, columnspan=2, sticky="e", pady=(8, 6))
        ttk.Button(botoes, text="Pesquisar nome", command=self._pesquisar_nome).grid(row=0, column=0, padx=(0, 8))
        ttk.Button(botoes, text="Atualizar", command=self._atualizar).grid(row=0, column=1, padx=(0, 8))
        ttk.Button(botoes, text="Excluir", command=self._excluir).grid(row=0, column=2, padx=(0, 8))
        ttk.Button(botoes, text="Limpar", command=self._limpar).grid(row=0, column=3, padx=(0, 8))
        ttk.Button(botoes, text="Salvar", command=self._salvar).grid(row=0, column=4)

    def _montar_lista(self):
        cols = ("id", "nome_servico", "duracao_minutos")
        self.tree = ttk.Treeview(self, columns=cols, show="headings", height=10)
        self.tree.heading("id", text="ID")
        self.tree.heading("nome_servico", text="Serviço")
        self.tree.heading("duracao_minutos", text="Duração")
        self.tree.grid(row=4, column=0, columnspan=2, sticky="nsew")
        self.rowconfigure(4, weight=1)

    def _limpar(self):
        self.id_var.set("")
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

    def _pesquisar_nome(self):
        nome = self.nome_var.get().strip()
        if not nome:
            messagebox.showerror("Validação", "Informe o nome para pesquisar.")
            return

        registros = ServicoDao.consultar_servico_nome(self.conexao, f"%{nome}%")
        if not registros:
            messagebox.showinfo("Resultado", "Nenhum serviço encontrado.")
            return

        if len(registros) > 1:
            resumo = ", ".join(f"{r[0]} - {r[1]}" for r in registros)
            messagebox.showinfo("Resultado", f"Foram encontrados {len(registros)} serviços: {resumo}.")
            return

        self._preencher_form(registros[0])

    def _preencher_form(self, servico):
        if hasattr(servico, "get_id"):
            serv_id = servico.get_id()
            nome = servico.get_nome_servico()
            duracao = servico.get_duracao()
        else:
            serv_id, nome, duracao = servico
        self.id_var.set(str(serv_id))
        self.nome_var.set(nome)
        self.duracao_var.set(str(duracao))

    def _atualizar(self):
        id_txt = self.id_var.get().strip()
        if not id_txt.isdigit():
            messagebox.showerror("Validação", "Selecione um serviço pelo ID.")
            return

        nome = self.nome_var.get().strip()
        duracao_txt = self.duracao_var.get().strip()
        if not nome or not duracao_txt:
            messagebox.showerror("Validação", "Preencha nome e duração.")
            return
        if not duracao_txt.isdigit():
            messagebox.showerror("Validação", "Duração deve conter apenas números.")
            return

        serv_atual = ServicoDao.consultar_servico_id(self.conexao, int(id_txt))
        if not serv_atual:
            messagebox.showerror("Erro", "Serviço não encontrado.")
            return

        ret = ServicoDao.atualiza_servico(self.conexao, serv_atual, nome, int(duracao_txt))
        if ret == -1:
            messagebox.showerror("Erro", "Não foi possível atualizar o serviço.")
            return

        messagebox.showinfo("Sucesso", "Serviço atualizado com sucesso.")
        self._preencher_form((serv_atual.get_id(), nome, int(duracao_txt)))
        self._carregar_servicos()

    def _excluir(self):
        id_txt = self.id_var.get().strip()
        if not id_txt.isdigit():
            messagebox.showerror("Validação", "Selecione um serviço pelo ID.")
            return

        if not messagebox.askyesno("Confirmar", "Deseja excluir este serviço?"):
            return

        ret = ServicoDao.excluir_servico(self.conexao, int(id_txt))
        if ret == -1:
            messagebox.showerror("Erro", "Não foi possível excluir o serviço.")
            return

        messagebox.showinfo("Sucesso", "Serviço excluído com sucesso.")
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
