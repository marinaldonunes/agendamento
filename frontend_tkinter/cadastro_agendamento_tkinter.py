import datetime as dt
import tkinter as tk
from tkinter import messagebox, ttk

from agendamento import Agendamento
from agendamentoDao import AgendamentoDao
from agenda import Agenda
from agendaDao import AgendaDao
from clienteDao import ClienteDao
from profissionalDao import ProfissionalDao
from servicoDao import ServicoDao

try:
    from ._common import criar_conexao
except ImportError:
    from _common import criar_conexao


class TelaCadastroAgendamento(ttk.Frame):
    def __init__(self, master, conexao):
        super().__init__(master, padding=12)
        self.conexao = conexao
        self.cliente_map = {}
        self.servico_map = {}
        self.prof_map = {}
        self.agenda_map = {}
        self.columnconfigure(1, weight=1)
        self._montar_form()
        self._montar_lista()
        self._carregar_combos()

    def _montar_form(self):
        ttk.Label(self, text="Cliente").grid(row=0, column=0, sticky="w", pady=4)
        self.cliente_var = tk.StringVar()
        self.cliente_combo = ttk.Combobox(self, textvariable=self.cliente_var, state="readonly")
        self.cliente_combo.grid(row=0, column=1, sticky="ew", pady=4)
        self.cliente_combo.bind("<<ComboboxSelected>>", lambda _: self._carregar_agendamentos_cliente())

        ttk.Label(self, text="Serviço").grid(row=1, column=0, sticky="w", pady=4)
        self.servico_var = tk.StringVar()
        self.servico_combo = ttk.Combobox(self, textvariable=self.servico_var, state="readonly")
        self.servico_combo.grid(row=1, column=1, sticky="ew", pady=4)

        ttk.Label(self, text="Profissional").grid(row=2, column=0, sticky="w", pady=4)
        self.prof_var = tk.StringVar()
        self.prof_combo = ttk.Combobox(self, textvariable=self.prof_var, state="readonly")
        self.prof_combo.grid(row=2, column=1, sticky="ew", pady=4)
        self.prof_combo.bind("<<ComboboxSelected>>", lambda _: self._carregar_agendas_disponiveis())

        ttk.Label(self, text="Agenda disponivel").grid(row=3, column=0, sticky="w", pady=4)
        self.agenda_var = tk.StringVar()
        self.agenda_combo = ttk.Combobox(self, textvariable=self.agenda_var, state="readonly")
        self.agenda_combo.grid(row=3, column=1, sticky="ew", pady=4)

        botoes = ttk.Frame(self)
        botoes.grid(row=4, column=0, columnspan=2, sticky="e", pady=(8, 6))
        ttk.Button(botoes, text="Salvar", command=self._salvar).grid(row=0, column=0, padx=(0, 8))
        ttk.Button(botoes, text="Atualizar combos", command=self._carregar_combos).grid(row=0, column=1)

    def _montar_lista(self):
        cols = ("id", "cliente", "servico", "profissional", "data", "hora")
        self.tree = ttk.Treeview(self, columns=cols, show="headings", height=10)
        self.tree.heading("id", text="ID")
        self.tree.heading("cliente", text="Cliente")
        self.tree.heading("servico", text="Serviço")
        self.tree.heading("profissional", text="Profissional")
        self.tree.heading("data", text="Data")
        self.tree.heading("hora", text="Hora")
        self.tree.grid(row=6, column=0, columnspan=2, sticky="nsew")
        self.rowconfigure(6, weight=1)

    def _carregar_combos(self):
        self._carregar_clientes()
        self._carregar_servicos()
        self._carregar_profissionais()
        self._carregar_agendas_disponiveis()
        self._carregar_agendamentos_cliente()

    def _carregar_clientes(self):
        self.cliente_map.clear()
        valores = []
        for reg in ClienteDao.consulta_clientes(self.conexao):
            chave = f"{reg[0]} - {reg[1]} {reg[2]}"
            self.cliente_map[chave] = reg[0]
            valores.append(chave)
        self.cliente_combo["values"] = valores
        self.cliente_var.set("")

    def _carregar_servicos(self):
        self.servico_map.clear()
        valores = []
        servicos = ServicoDao.consultar_servicos(self.conexao)
        if servicos == -1:
            self.servico_combo["values"] = []
            return
        for reg in servicos:
            chave = f"{reg[0]} - {reg[1]} ({reg[2]} min)"
            self.servico_map[chave] = reg[0]
            valores.append(chave)
        self.servico_combo["values"] = valores
        self.servico_var.set("")

    def _carregar_profissionais(self):
        self.prof_map.clear()
        valores = []
        for reg in ProfissionalDao.consulta_profissionais(self.conexao):
            chave = f"{reg[0]} - {reg[1]} {reg[2]}"
            self.prof_map[chave] = reg[0]
            valores.append(chave)
        self.prof_combo["values"] = valores
        self.prof_var.set("")

    def _carregar_agendas_disponiveis(self):
        self.agenda_map.clear()
        valores = []
        prof_id = self.prof_map.get(self.prof_var.get().strip())
        if not prof_id:
            self.agenda_combo["values"] = []
            return

        agendas = AgendaDao.consulta_agendas_prof(self.conexao, prof_id)
        if agendas == -1:
            self.agenda_combo["values"] = []
            return

        ocupados = set()
        regs = AgendamentoDao.consultar_agendamentos_profissional(self.conexao, prof_id)
        if regs != -1:
            for reg in regs:
                ocupados.add((reg[4], reg[5]))

        for data, hora in agendas:
            if (data, hora) in ocupados:
                continue
            data_fmt = self._formatar_data(data)
            chave = f"{data_fmt} {hora}"
            self.agenda_map[chave] = (data, hora)
            valores.append(chave)

        self.agenda_combo["values"] = valores
        self.agenda_var.set("")

    def _formatar_data(self, data):
        if isinstance(data, str):
            try:
                return dt.datetime.strptime(data, "%Y-%m-%d").strftime("%d/%m/%Y")
            except ValueError:
                return data
        if hasattr(data, "strftime"):
            return data.strftime("%d/%m/%Y")
        return str(data)

    def _objetos_selecionados(self):
        cliente_id = self.cliente_map.get(self.cliente_var.get().strip())
        servico_id = self.servico_map.get(self.servico_var.get().strip())
        prof_id = self.prof_map.get(self.prof_var.get().strip())
        if not cliente_id or not servico_id or not prof_id:
            return None, None, None
        cliente = ClienteDao.consulta_cliente_id(self.conexao, cliente_id)
        servico = ServicoDao.consultar_servico_id(self.conexao, servico_id)
        profissional = ProfissionalDao.consulta_profissional_id(self.conexao, prof_id)
        return cliente, servico, profissional

    def _salvar(self):
        cliente, servico, profissional = self._objetos_selecionados()
        if not cliente or not servico or not profissional:
            messagebox.showerror("Validação", "Selecione cliente, serviço e profissional válidos.")
            return

        agenda_sel = self.agenda_var.get().strip()
        agenda = self.agenda_map.get(agenda_sel)
        if not agenda:
            messagebox.showerror("Validação", "Selecione uma agenda disponível.")
            return
        data, hora = agenda

        agenda = Agenda(profissional, data, hora)
        agd = Agendamento(0, cliente, servico, agenda)
        novo_id = AgendamentoDao.inserir_agendamentos(self.conexao, agd)
        if novo_id == -1:
            messagebox.showerror("Erro", "Falha ao cadastrar agendamento.")
            return

        messagebox.showinfo("Sucesso", f"Agendamento cadastrado. ID: {novo_id}")
        self.cliente_var.set("")
        self.servico_var.set("")
        self.prof_var.set("")
        self.agenda_var.set("")
        self._carregar_agendas_disponiveis()
        self._carregar_agendamentos_cliente()

    def _carregar_agendamentos_cliente(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        cliente_id = self.cliente_map.get(self.cliente_var.get().strip())
        if not cliente_id:
            return
        regs = AgendamentoDao.consultar_agendamentos_cliente(self.conexao, cliente_id)
        if regs == -1:
            return
        for reg in regs:
            cid = reg[1]
            sid = reg[2]
            pid = reg[3]
            cli = ClienteDao.consulta_cliente_id(self.conexao, cid)
            serv = ServicoDao.consultar_servico_id(self.conexao, sid)
            prof = ProfissionalDao.consulta_profissional_id(self.conexao, pid)
            self.tree.insert(
                "",
                tk.END,
                values=(
                    reg[0],
                    f"{cid} - {cli.get_nome() if cli else ''}",
                    f"{sid} - {serv.get_nome_servico() if serv else ''}",
                    f"{pid} - {prof.get_nome() if prof else ''}",
                    reg[4],
                    reg[5],
                ),
            )


def main():
    conexao = criar_conexao()
    root = tk.Tk()
    root.title("Cadastro de Agendamento")
    root.geometry("900x520")
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    frame = TelaCadastroAgendamento(root, conexao)
    frame.grid(sticky="nsew")

    def ao_fechar():
        conexao.close()
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", ao_fechar)
    root.mainloop()


if __name__ == "__main__":
    main()
