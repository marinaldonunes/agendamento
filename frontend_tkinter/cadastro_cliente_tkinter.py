import datetime as dt
import sys
import tkinter as tk
from pathlib import Path
from tkinter import messagebox, ttk

# Permite importar módulos do projeto ao executar este arquivo diretamente.
ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from cliente import Cliente
from clienteDao import ClienteDao

try:
    from ._common import criar_conexao
except ImportError:
    from _common import criar_conexao


class TelaCadastroCliente(ttk.Frame):
    def __init__(self, master, conexao):
        super().__init__(master, padding=16)
        self.conexao = conexao
        self._monta_tela()
        self._monta_lista()
        self._carregar_clientes()

    def _monta_tela(self):
        self.columnconfigure(1, weight=1)

        ttk.Label(self, text="ID").grid(row=7, column=0, sticky="w", pady=4)
        self.id_var = tk.StringVar()
        ttk.Entry(self, textvariable=self.id_var, state="readonly", width=10).grid(
            row=7, column=1, sticky="w", pady=4
        )

        ttk.Label(self, text="Nome").grid(row=0, column=0, sticky="w", pady=4)
        self.nome_var = tk.StringVar()
        ttk.Entry(self, textvariable=self.nome_var).grid(row=0, column=1, sticky="ew", pady=4)

        ttk.Label(self, text="Sobrenome").grid(row=1, column=0, sticky="w", pady=4)
        self.sobrenome_var = tk.StringVar()
        ttk.Entry(self, textvariable=self.sobrenome_var).grid(row=1, column=1, sticky="ew", pady=4)

        ttk.Label(self, text="Data de nascimento (dd/mm/aaaa)").grid(row=2, column=0, sticky="w", pady=4)
        self.dtnasc_var = tk.StringVar()
        ttk.Entry(self, textvariable=self.dtnasc_var).grid(row=2, column=1, sticky="ew", pady=4)

        ttk.Label(self, text="CPF (somente números)").grid(row=3, column=0, sticky="w", pady=4)
        self.cpf_var = tk.StringVar()
        ttk.Entry(self, textvariable=self.cpf_var).grid(row=3, column=1, sticky="ew", pady=4)

        ttk.Label(self, text="Nome da mãe").grid(row=4, column=0, sticky="w", pady=4)
        self.nome_mae_var = tk.StringVar()
        ttk.Entry(self, textvariable=self.nome_mae_var).grid(row=4, column=1, sticky="ew", pady=4)

        ttk.Label(self, text="Sexo").grid(row=5, column=0, sticky="w", pady=4)
        self.sexo_var = tk.StringVar()
        ttk.Combobox(
            self,
            textvariable=self.sexo_var,
            values=("M", "F", "O"),
            state="readonly",
            width=5,
        ).grid(row=5, column=1, sticky="w", pady=4)

        ttk.Label(self, text="Contatos (um por linha)").grid(row=6, column=0, sticky="nw", pady=4)
        self.contatos_txt = tk.Text(self, height=5, width=40)
        self.contatos_txt.grid(row=6, column=1, sticky="ew", pady=4)

        botoes = ttk.Frame(self)
        botoes.grid(row=8, column=0, columnspan=2, sticky="e", pady=(12, 0))
        ttk.Button(botoes, text="Pesquisar nome", command=self._pesquisar_nome).grid(row=0, column=0, padx=(0, 8))
        ttk.Button(botoes, text="Atualizar", command=self._atualizar).grid(row=0, column=1, padx=(0, 8))
        ttk.Button(botoes, text="Excluir", command=self._excluir).grid(row=0, column=2, padx=(0, 8))
        ttk.Button(botoes, text="Limpar", command=self._limpar).grid(row=0, column=3, padx=(0, 8))
        ttk.Button(botoes, text="Salvar", command=self._salvar).grid(row=0, column=4)

    def _monta_lista(self):
        cols = ("id", "nome", "sobrenome", "nome_mae", "cpf", "dt_nasc", "sexo", "contatos")
        self.tree = ttk.Treeview(self, columns=cols, show="headings", height=8)
        self.tree.heading("id", text="ID")
        self.tree.heading("nome", text="Nome")
        self.tree.heading("sobrenome", text="Sobrenome")
        self.tree.heading("nome_mae", text="Nome da mae")
        self.tree.heading("cpf", text="CPF")
        self.tree.heading("dt_nasc", text="Nascimento")
        self.tree.heading("sexo", text="Sexo")
        self.tree.heading("contatos", text="Contatos")
        self.tree.column("id", width=60, anchor="center")
        self.tree.column("nome", width=160, anchor="w")
        self.tree.column("sobrenome", width=160, anchor="w")
        self.tree.column("nome_mae", width=180, anchor="w")
        self.tree.column("cpf", width=110, anchor="center")
        self.tree.column("dt_nasc", width=110, anchor="center")
        self.tree.column("sexo", width=60, anchor="center")
        self.tree.column("contatos", width=220, anchor="w")
        self.tree.grid(row=9, column=0, columnspan=2, sticky="nsew", pady=(10, 0))
        self.rowconfigure(9, weight=1)
        self.tree.bind("<Double-1>", self._on_tree_double_click)

    def _carregar_clientes(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        registros = ClienteDao.consulta_clientes(self.conexao)
        if not registros:
            return

        for reg in registros:
            cli_id, nome, sobrenome, dtnasc, nome_mae, cpf, sexo = reg
            if hasattr(dtnasc, "strftime"):
                dtnasc_txt = dtnasc.strftime("%d/%m/%Y")
            else:
                try:
                    dtnasc_txt = dt.datetime.strptime(str(dtnasc), "%Y-%m-%d").strftime("%d/%m/%Y")
                except (ValueError, TypeError):
                    dtnasc_txt = str(dtnasc)
            contatos = ClienteDao.consulta_contatos_cliente(self.conexao, cli_id)
            contatos_txt = " / ".join(self._formatar_contato(c) for c in contatos) if contatos else ""
            self.tree.insert(
                "",
                tk.END,
                values=(cli_id, nome, sobrenome, nome_mae, cpf, dtnasc_txt, sexo, contatos_txt),
            )

    @staticmethod
    def _formatar_contato(contato):
        if not contato:
            return ""
        digitos = "".join(ch for ch in str(contato) if ch.isdigit())
        if len(digitos) == 11:
            return f"({digitos[:2]}){digitos[2:7]}-{digitos[7:]}"
        if len(digitos) == 10:
            return f"({digitos[:2]}){digitos[2:6]}-{digitos[6:]}"
        return str(contato)

    def _on_tree_double_click(self, _event):
        selecionado = self.tree.selection()
        if not selecionado:
            return
        valores = self.tree.item(selecionado[0], "values")
        if not valores:
            return
        cli_id = valores[0]
        if not str(cli_id).isdigit():
            return
        cliente = ClienteDao.consulta_cliente_id(self.conexao, int(cli_id))
        if cliente:
            self._preencher_form(cliente)

    def _limpar(self):
        self.id_var.set("")
        self.nome_var.set("")
        self.sobrenome_var.set("")
        self.dtnasc_var.set("")
        self.cpf_var.set("")
        self.nome_mae_var.set("")
        self.sexo_var.set("")
        self.contatos_txt.delete("1.0", tk.END)

    def _salvar(self):
        nome = self.nome_var.get().strip()
        sobrenome = self.sobrenome_var.get().strip()
        dtnasc_txt = self.dtnasc_var.get().strip()
        cpf = self.cpf_var.get().strip()
        nome_mae = self.nome_mae_var.get().strip()
        sexo = self.sexo_var.get().strip()
        contatos_texto = self.contatos_txt.get("1.0", tk.END)
        contatos = [linha.strip() for linha in contatos_texto.splitlines() if linha.strip()]

        if not nome or not sobrenome or not dtnasc_txt or not cpf or not nome_mae or not sexo:
            messagebox.showerror("Validação", "Preencha todos os campos obrigatórios.")
            return

        if not cpf.isdigit():
            messagebox.showerror("Validação", "CPF deve conter apenas números.")
            return

        try:
            dtnasc = dt.datetime.strptime(dtnasc_txt, "%d/%m/%Y")
        except ValueError:
            messagebox.showerror("Validação", "Data inválida. Use o formato dd/mm/aaaa.")
            return

        cliente = Cliente(
            nome=nome,
            sobrenome=sobrenome,
            dtnascimento=dtnasc,
            cpf=cpf,
            nome_mae=nome_mae,
            sexo=sexo,
        )
        cliente.set_contatos(contatos)

        novo_id = ClienteDao.insere_cliente(self.conexao, cliente)
        if novo_id == -1:
            messagebox.showerror("Erro", "Não foi possível salvar o cliente.")
            return

        messagebox.showinfo("Sucesso", f"Cliente cadastrado com sucesso. ID: {novo_id}")
        self._limpar()
        self._carregar_clientes()

    def _pesquisar_nome(self):
        nome = self.nome_var.get().strip()
        if not nome:
            messagebox.showerror("ValidaÃ§Ã£o", "Informe o nome para pesquisar.")
            return

        clientes = ClienteDao.consulta_cliente_nome(self.conexao, f"%{nome}%")
        if not clientes:
            messagebox.showinfo("Resultado", "Nenhum cliente encontrado.")
            return

        if len(clientes) > 1:
            resumo = ", ".join(f"{c.get_id()} - {c.get_nome()} {c.get_sobrenome()}" for c in clientes)
            messagebox.showinfo("Resultado", f"Foram encontrados {len(clientes)} clientes: {resumo}.")
            return

        self._preencher_form(clientes[0])

    def _preencher_form(self, cliente):
        self.id_var.set(str(cliente.get_id()))
        self.nome_var.set(cliente.get_nome())
        self.sobrenome_var.set(cliente.get_sobrenome())
        dtnasc = cliente.get_dtnascimento()
        if hasattr(dtnasc, "strftime"):
            dtnasc_txt = dtnasc.strftime("%d/%m/%Y")
        else:
            try:
                dtnasc_txt = dt.datetime.strptime(str(dtnasc), "%Y-%m-%d").strftime("%d/%m/%Y")
            except (ValueError, TypeError):
                try:
                    dtnasc_txt = dt.datetime.strptime(str(dtnasc), "%d/%m/%Y").strftime("%d/%m/%Y")
                except (ValueError, TypeError):
                    dtnasc_txt = str(dtnasc)
        self.dtnasc_var.set(dtnasc_txt)
        self.cpf_var.set(cliente.get_cpf())
        self.nome_mae_var.set(cliente.get_nome_mae())
        self.sexo_var.set(cliente.get_sexo())
        self.contatos_txt.delete("1.0", tk.END)
        for contato in cliente.get_contatos():
            self.contatos_txt.insert(tk.END, contato + "\n")

    def _atualizar(self):
        id_txt = self.id_var.get().strip()
        if not id_txt.isdigit():
            messagebox.showerror("ValidaÃ§Ã£o", "Selecione um cliente pelo ID.")
            return

        nome = self.nome_var.get().strip()
        sobrenome = self.sobrenome_var.get().strip()
        dtnasc_txt = self.dtnasc_var.get().strip()
        cpf = self.cpf_var.get().strip()
        nome_mae = self.nome_mae_var.get().strip()
        sexo = self.sexo_var.get().strip()
        contatos_texto = self.contatos_txt.get("1.0", tk.END)
        contatos = [linha.strip() for linha in contatos_texto.splitlines() if linha.strip()]

        if not nome or not sobrenome or not dtnasc_txt or not cpf or not nome_mae or not sexo:
            messagebox.showerror("ValidaÃ§Ã£o", "Preencha todos os campos obrigatÃ³rios.")
            return

        if not cpf.isdigit():
            messagebox.showerror("ValidaÃ§Ã£o", "CPF deve conter apenas nÃºmeros.")
            return

        try:
            dtnasc = dt.datetime.strptime(dtnasc_txt, "%d/%m/%Y")
        except ValueError:
            messagebox.showerror("ValidaÃ§Ã£o", "Data invÃ¡lida. Use o formato dd/mm/aaaa.")
            return

        cliente_atual = ClienteDao.consulta_cliente_id(self.conexao, int(id_txt))
        if not cliente_atual:
            messagebox.showerror("Erro", "Cliente nÃ£o encontrado.")
            return

        cliente_novo = Cliente(
            nome=nome,
            sobrenome=sobrenome,
            dtnascimento=dtnasc,
            cpf=cpf,
            nome_mae=nome_mae,
            sexo=sexo,
            p_id=cliente_atual.get_id(),
        )
        cliente_novo.set_contatos(contatos)

        ret = ClienteDao.atualiza_cliente(self.conexao, cliente_atual, cliente_novo)
        if ret == cliente_atual:
            messagebox.showerror("Erro", "NÃ£o foi possÃ­vel atualizar o cliente.")
            return

        messagebox.showinfo("Sucesso", "Cliente atualizado com sucesso.")
        self._preencher_form(cliente_novo)
        self._carregar_clientes()

    def _excluir(self):
        id_txt = self.id_var.get().strip()
        if not id_txt.isdigit():
            messagebox.showerror("ValidaÃ§Ã£o", "Selecione um cliente pelo ID.")
            return

        if not messagebox.askyesno("Confirmar", "Deseja excluir este cliente?"):
            return

        ret = ClienteDao.exclui_cliente(self.conexao, int(id_txt))
        if ret == -1:
            messagebox.showerror("Erro", "NÃ£o foi possÃ­vel excluir o cliente.")
            return

        messagebox.showinfo("Sucesso", "Cliente excluÃ­do com sucesso.")
        self._limpar()
        self._carregar_clientes()


def main():
    conexao = criar_conexao()

    root = tk.Tk()
    root.title("Cadastro de Cliente")
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    root.geometry("560x420")

    app = TelaCadastroCliente(root, conexao)
    app.grid(sticky="nsew")

    def ao_fechar():
        conexao.close()
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", ao_fechar)
    root.mainloop()


if __name__ == "__main__":
    main()
