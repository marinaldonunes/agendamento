import tkinter as tk
from pathlib import Path
from tkinter import ttk

try:
    from PIL import Image, ImageTk
except ImportError:
    Image = None
    ImageTk = None

try:
    from ._common import criar_conexao
    from .cadastro_agenda_tkinter import TelaCadastroAgenda
    from .cadastro_agendamento_tkinter import TelaCadastroAgendamento
    from .cadastro_cliente_tkinter import TelaCadastroCliente
    from .cadastro_profissional_tkinter import TelaCadastroProfissional
    from .cadastro_servico_tkinter import TelaCadastroServico
except ImportError:
    from _common import criar_conexao
    from cadastro_agenda_tkinter import TelaCadastroAgenda
    from cadastro_agendamento_tkinter import TelaCadastroAgendamento
    from cadastro_cliente_tkinter import TelaCadastroCliente
    from cadastro_profissional_tkinter import TelaCadastroProfissional
    from cadastro_servico_tkinter import TelaCadastroServico


def carregar_logomarca():
    pasta = Path(__file__).resolve().parent / "assets" / "logomarca"
    candidatos = [
        pasta / "logmarca.jpg",
        pasta / "logmarca.jpeg",
        pasta / "logmarca.png",
        pasta / "logmarca.gif",
    ]
    caminho_logo = next((p for p in candidatos if p.exists()), None)
    if caminho_logo is None:
        return None

    if caminho_logo.suffix.lower() in {".png", ".gif"} and (Image is None or ImageTk is None):
        try:
            return tk.PhotoImage(file=str(caminho_logo))
        except tk.TclError:
            return None

    if Image is None or ImageTk is None:
        return None

    try:
        imagem = Image.open(caminho_logo)
        largura_max = 600
        if imagem.width > largura_max:
            nova_altura = int((largura_max / imagem.width) * imagem.height)
            imagem = imagem.resize((largura_max, nova_altura), Image.Resampling.LANCZOS)
        return ImageTk.PhotoImage(imagem)
    except Exception:
        return None


class TelaSobre(ttk.Frame):
    def __init__(self, master):
        super().__init__(master, padding=20)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(2, weight=1)
        self._logo_ref = None
        self._montar_tela()

    def _montar_tela(self):
        ttk.Label(self, text="Sistema de Agendamento", font=("Segoe UI", 16, "bold")).grid(
            row=0, column=0, sticky="n", pady=(0, 8)
        )

        logo = carregar_logomarca()
        if logo:
            self._logo_ref = logo
            ttk.Label(self, image=logo, anchor="center").grid(row=1, column=0, pady=(0, 12))
        else:
            ttk.Label(
                self,
                text="Logomarca nao encontrada em frontend_tkinter/assets/logomarca.",
                anchor="center",
            ).grid(row=1, column=0, pady=(0, 12))

        info = (
            "Sobre\n\n"
            "Aplicacao para gestao de clientes, profissionais, servicos,\n"
            "agendas e agendamentos.\n\n"
            "Versao: 1.0.0\n"
            "Autor: Informe aqui o nome da equipe/sistema.\n"
            "Contato: Informe aqui e-mail/telefone."
        )
        ttk.Label(self, text=info, justify="center").grid(row=2, column=0, sticky="n")


class AppAgendamento(ttk.Frame):
    def __init__(self, master, conexao):
        super().__init__(master)
        self.conexao = conexao

        self.grid(sticky="nsew")
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self._montar_abas()

    def _montar_abas(self):
        notebook = ttk.Notebook(self)
        notebook.grid(row=0, column=0, sticky="nsew")

        aba_clientes = TelaCadastroCliente(notebook, self.conexao)
        aba_profissionais = TelaCadastroProfissional(notebook, self.conexao)
        aba_servicos = TelaCadastroServico(notebook, self.conexao)
        aba_agendas = TelaCadastroAgenda(notebook, self.conexao)
        aba_agendamentos = TelaCadastroAgendamento(notebook, self.conexao)
        aba_sobre = TelaSobre(notebook)

        notebook.add(aba_clientes, text="Clientes")
        notebook.add(aba_profissionais, text="Profissionais")
        notebook.add(aba_servicos, text="Servicos")
        notebook.add(aba_agendas, text="Agendas")
        notebook.add(aba_agendamentos, text="Agendamentos")
        notebook.add(aba_sobre, text="Sobre")


class SplashScreen(tk.Toplevel):
    def __init__(self, master, duracao_ms=3000):
        super().__init__(master)
        self.overrideredirect(True)
        self.configure(bg="white")

        frame = ttk.Frame(self, padding=12)
        frame.grid(row=0, column=0, sticky="nsew")
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        logo = carregar_logomarca()
        label = ttk.Label(frame, anchor="center")
        label.grid(row=0, column=0, sticky="nsew")
        frame.columnconfigure(0, weight=1)
        frame.rowconfigure(0, weight=1)

        if logo:
            self._logo_ref = logo
            label.configure(image=logo)
        else:
            label.configure(text="Logomarca nao encontrada em assets/logomarca.")

        self.update_idletasks()
        largura = max(500, self.winfo_reqwidth())
        altura = max(320, self.winfo_reqheight())
        x = (self.winfo_screenwidth() - largura) // 2
        y = (self.winfo_screenheight() - altura) // 2
        self.geometry(f"{largura}x{altura}+{x}+{y}")

        self.after(duracao_ms, self.destroy)


def main():
    conexao = criar_conexao()
    root = tk.Tk()
    root.title("Sistema de Agendamento")
    root.geometry("1280x760")
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    root.withdraw()

    AppAgendamento(root, conexao)

    def ao_fechar():
        conexao.close()
        root.destroy()

    splash = SplashScreen(root, duracao_ms=3000)
    splash.wait_window()
    root.deiconify()

    root.protocol("WM_DELETE_WINDOW", ao_fechar)
    root.mainloop()


if __name__ == "__main__":
    main()
