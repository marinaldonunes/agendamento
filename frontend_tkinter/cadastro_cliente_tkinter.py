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

    def _monta_tela(self):
        self.columnconfigure(1, weight=1)

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
        self.sexo_var = tk.StringVar(value="M")
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
        botoes.grid(row=7, column=0, columnspan=2, sticky="e", pady=(12, 0))
        ttk.Button(botoes, text="Limpar", command=self._limpar).grid(row=0, column=0, padx=(0, 8))
        ttk.Button(botoes, text="Salvar", command=self._salvar).grid(row=0, column=1)

    def _limpar(self):
        self.nome_var.set("")
        self.sobrenome_var.set("")
        self.dtnasc_var.set("")
        self.cpf_var.set("")
        self.nome_mae_var.set("")
        self.sexo_var.set("M")
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
