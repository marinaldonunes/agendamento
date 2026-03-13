import datetime as dt
import tkinter as tk
from tkinter import messagebox, ttk

from agenda import Agenda
from agendaDao import AgendaDao
from profissionalDao import ProfissionalDao

try:
    from ._common import criar_conexao
except ImportError:
    from _common import criar_conexao


class TelaCadastroAgenda(ttk.Frame):
    def __init__(self, master, conexao):
        super().__init__(master, padding=12)
        self.conexao = conexao
        self.prof_map = {}
        self.columnconfigure(1, weight=1)
        self._montar_form()
        self._montar_lista()
        self._carregar_profissionais()

    def _montar_form(self):
        ttk.Label(self, text="Profissional").grid(row=0, column=0, sticky="w", pady=4)
        self.prof_var = tk.StringVar()
        self.prof_combo = ttk.Combobox(self, textvariable=self.prof_var, state="readonly")
        self.prof_combo.grid(row=0, column=1, sticky="ew", pady=4)
        self.prof_combo.bind("<<ComboboxSelected>>", lambda _: self._carregar_agendas_do_profissional())

        ttk.Label(self, text="Data (dd/mm/aaaa)").grid(row=1, column=0, sticky="w", pady=4)
        self.data_var = tk.StringVar()
        ttk.Entry(self, textvariable=self.data_var).grid(row=1, column=1, sticky="ew", pady=4)

        ttk.Label(self, text="Hora (HHMM)").grid(row=2, column=0, sticky="w", pady=4)
        self.hora_var = tk.StringVar()
        ttk.Entry(self, textvariable=self.hora_var).grid(row=2, column=1, sticky="ew", pady=4)

        botoes = ttk.Frame(self)
        botoes.grid(row=3, column=0, columnspan=2, sticky="e", pady=(8, 6))
        ttk.Button(botoes, text="Salvar", command=self._salvar).grid(row=0, column=0, padx=(0, 8))
        ttk.Button(botoes, text="Atualizar lista", command=self._carregar_profissionais).grid(row=0, column=1)

    def _montar_lista(self):
        cols = ("data", "hora")
        self.tree = ttk.Treeview(self, columns=cols, show="headings", height=12)
        self.tree.heading("data", text="Data")
        self.tree.heading("hora", text="Hora")
        self.tree.grid(row=4, column=0, columnspan=2, sticky="nsew")
        self.rowconfigure(4, weight=1)

    def _carregar_profissionais(self):
        self.prof_map.clear()
        valores = []
        for reg in ProfissionalDao.consulta_profissionais(self.conexao):
            chave = f"{reg[0]} - {reg[1]} {reg[2]}"
            self.prof_map[chave] = reg[0]
            valores.append(chave)
        self.prof_combo["values"] = valores
        self.prof_var.set("")

    def _profissional_selecionado(self):
        chave = self.prof_var.get().strip()
        if not chave or chave not in self.prof_map:
            return None
        return ProfissionalDao.consulta_profissional_id(self.conexao, self.prof_map[chave])

    def _salvar(self):
        prof = self._profissional_selecionado()
        if not prof:
            messagebox.showerror("Validação", "Selecione um profissional.")
            return

        data_txt = self.data_var.get().strip()
        hora = self.hora_var.get().strip()
        if not data_txt or len(hora) != 4 or not hora.isdigit():
            messagebox.showerror("Validação", "Informe data e hora no formato HHMM.")
            return

        try:
            data = dt.datetime.strptime(data_txt, "%d/%m/%Y")
        except ValueError:
            messagebox.showerror("Validação", "Data inválida. Use dd/mm/aaaa.")
            return

        agenda = Agenda(prof, data, hora)
        ret = AgendaDao.inserir_agenda(self.conexao, agenda)
        if ret == -1:
            messagebox.showerror("Erro", "Não foi possível inserir a agenda.")
            return

        messagebox.showinfo("Sucesso", "Horário de agenda cadastrado.")
        self.data_var.set("")
        self.hora_var.set("")
        self.prof_var.set("")
        self._carregar_agendas_do_profissional()

    def _carregar_agendas_do_profissional(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        prof = self._profissional_selecionado()
        if not prof:
            return
        registros = AgendaDao.consulta_agendas_prof(self.conexao, prof.get_id())
        if registros == -1:
            return
        for data, hora in registros:
            self.tree.insert("", tk.END, values=(data, hora))


def main():
    conexao = criar_conexao()
    root = tk.Tk()
    root.title("Cadastro de Agenda")
    root.geometry("640x460")
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    frame = TelaCadastroAgenda(root, conexao)
    frame.grid(sticky="nsew")

    def ao_fechar():
        conexao.close()
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", ao_fechar)
    root.mainloop()


if __name__ == "__main__":
    main()
