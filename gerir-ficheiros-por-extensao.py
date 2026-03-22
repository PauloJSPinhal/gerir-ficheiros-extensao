#!/usr/bin/env python3
#
# ============================================================================
# SCRIPT: Gerir Ficheiros por Extensão
# ============================================================================
# Descrição: Interface GTK para gerir ficheiros por extensão no Nautilus
# Funcionalidades: Copiar, Mover, Reciclagem, Eliminar, Backup
# Compatibilidade: Debian 13+ / GNOME / Nautilus
# Instalação: ~/.local/share/nautilus/scripts/"Gerir Ficheiros por Extensão"
# ============================================================================

# ============================================================
# CONFIGURAÇÕES GERAIS
# ============================================================
# Define o número máximo de caracteres para considerar como extensão válida
# Exemplo: "pdf" (3), "docx" (4), "html" (4) são válidos
# "Memória Descritiva" (18 caracteres) NÃO é válido
MAX_EXTENSION_LENGTH = 5

# Define o número mínimo de caracteres para considerar como extensão válida
# Exemplo: "a" (1) é válido, "" (0) não é válido
MIN_EXTENSION_LENGTH = 1
# ============================================================

# ============================================================
# IMPORTAÇÃO DE MÓDULOS DO SISTEMA
# ============================================================
import os          # Operações com sistema de ficheiros
import shutil      # Operações de copiar/mover ficheiros
import subprocess  # Executar comandos externos
from collections import defaultdict  # Dicionário com valores padrão
# ============================================================

# ============================================================
# IMPORTAÇÃO DE MÓDULOS GTK (INTERFACE GRÁFICA)
# ============================================================
import gi
gi.require_version('Gtk', '3.0')  # Define versão do GTK (3.0)
from gi.repository import Gtk, Gdk, GLib, Gio  # Importa componentes GTK
# ============================================================

# ============================================================
# CLASSE PRINCIPAL: FileExtensionManager
# ============================================================================
# Esta classe cria a janela principal da aplicação e gere toda
# a lógica de seleção de extensões e execução de ações
# ============================================================
class FileExtensionManager(Gtk.Window):
    
    # --------------------------------------------------------
    # MÉTODO: __init__ (Construtor da Classe)
    # --------------------------------------------------------
    # Executado automaticamente quando a classe é instanciada
    # Configura a janela principal e carrega os ficheiros
    # --------------------------------------------------------
    def __init__(self):
        # Chama o construtor da classe pai (Gtk.Window)
        super().__init__(title="Gerir Ficheiros por Extensão")
        
        # Configurações da janela principal
        self.set_default_size(700, 600)      # Tamanho inicial: 700x600 pixels
        self.set_position(Gtk.WindowPosition.CENTER)  # Centraliza na tela
        self.set_resizable(False)            # Não permite redimensionar
        self.set_border_width(15)            # Margem interna de 15 pixels
        
        # ----------------------------------------------------
        # VARIÁVEIS DE ARMAZENAMENTO DE DADOS
        # ----------------------------------------------------
        self.all_files = []              # Lista de TODOS os ficheiros selecionados
        self.ext_counts = defaultdict(int)  # Contagem de ficheiros por extensão
        self.ext_files = defaultdict(list)  # Lista de ficheiros por extensão
        self.filtered_files = []         # Lista de ficheiros após filtragem
        self.selected_action = None      # Ação selecionada pelo utilizador
        # ----------------------------------------------------
        
        # Constrói a interface gráfica (botões, checkboxes, etc.)
        self.build_ui()
        
        # Carrega os ficheiros selecionados no Nautilus
        self.load_selected_files()
        
        # Configura teclas de atalho (Enter para executar, Esc para cancelar)
        self.connect("key-press-event", self.on_key_press)
    
    # --------------------------------------------------------
    # MÉTODO: build_ui
    # --------------------------------------------------------
    # Constrói toda a interface gráfica da janela
    # Divide-se em 4 secções: Título, Extensões, Ações, Botões
    # --------------------------------------------------------
    def build_ui(self):
        # Cria caixa vertical principal (organiza elementos de cima para baixo)
        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        self.add(main_box)  # Adiciona caixa à janela
        
        # ========================================================
        # SECÇÃO 1: TÍTULO E INFORMAÇÃO
        # ========================================================
        
        # Cria label do título com formatação HTML-like
        title_label = Gtk.Label()
        title_label.set_markup("<span size='large' weight='bold'>📁 Gerir Ficheiros por Extensão</span>")
        main_box.pack_start(title_label, False, False, 5)
        
        # Cria label de informação (atualizado após carregar ficheiros)
        self.info_label = Gtk.Label()
        self.info_label.set_markup("<span size='small'>A carregar ficheiros...</span>")
        self.info_label.get_style_context().add_class('dim-label')  # Texto cinzento
        main_box.pack_start(self.info_label, False, False, 5)
        
        # ========================================================
        # SECÇÃO 2: SELEÇÃO DE EXTENSÕES (Checkboxes)
        # ========================================================
        
        # Cria frame (caixa com borda) para agrupar extensões
        ext_frame = Gtk.Frame()
        ext_label = Gtk.Label()
        # Mostra o limite máximo de caracteres da configuração
        ext_label.set_markup(f"<b>1️⃣ Selecione as Extensões</b> <span size='small'>(max {MAX_EXTENSION_LENGTH} caracteres)</span>")
        ext_frame.set_label_widget(ext_label)  # Define label do frame
        main_box.pack_start(ext_frame, False, False, 5)
        
        # Cria caixa vertical dentro do frame
        ext_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        ext_box.set_margin_start(10)   # Margem esquerda: 10px
        ext_box.set_margin_end(10)     # Margem direita: 10px
        ext_box.set_margin_top(10)     # Margem superior: 10px
        ext_box.set_margin_bottom(10)  # Margem inferior: 10px
        ext_frame.add(ext_box)
        
        # Cria janela de scroll (caso haja muitas extensões)
        scrolled = Gtk.ScrolledWindow()
        scrolled.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)  # Scroll vertical automático
        scrolled.set_min_content_height(180)  # Altura mínima: 180px
        scrolled.set_min_content_width(550)   # Largura mínima: 550px
        ext_box.pack_start(scrolled, True, True, 0)
        
        # Cria lista para organizar os checkboxes
        self.ext_listbox = Gtk.ListBox()
        self.ext_listbox.set_selection_mode(Gtk.SelectionMode.NONE)  # Não seleciona linhas
        scrolled.add(self.ext_listbox)
        
        # Dicionário para armazenar referência aos checkboxes
        self.ext_checkboxes = {}
        
        # ========================================================
        # SECÇÃO 3: BOTÕES DE AÇÃO (5 botões)
        # ========================================================
        
        # Cria frame para agrupar botões de ação
        action_frame = Gtk.Frame()
        action_label = Gtk.Label()
        action_label.set_markup("<b>2️⃣ Escolha a Ação</b>")
        action_frame.set_label_widget(action_label)
        main_box.pack_start(action_frame, False, False, 5)
        
        # Cria caixa horizontal para os botões
        action_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        action_box.set_margin_start(10)
        action_box.set_margin_end(10)
        action_box.set_margin_top(10)
        action_box.set_margin_bottom(10)
        action_box.set_halign(Gtk.Align.CENTER)  # Centraliza botões
        action_frame.add(action_box)
        
        # Lista de ações: (Texto do botão, Ícone, ID interno)
        # ORDEM ALTERADA: Backup agora vem antes de Copiar
        actions = [
            ("Backup", "drive-harddisk", "backup"),      # 1º: Backup
            ("Copiar", "document-copy", "copy"),         # 2º: Copiar
            ("Mover", "document-send", "move"),          # 3º: Mover
            ("Reciclagem", "user-trash", "trash"),       # 4º: Reciclagem
            ("Eliminar", "edit-delete", "delete"),       # 5º: Eliminar
        ]
        
        # Dicionário para armazenar referência aos botões
        self.action_buttons = {}
        
        # Cria cada botão de ação
        for label, icon, action_id in actions:
            button = Gtk.Button(label=label)  # Cria botão com texto
            button.set_image(Gtk.Image.new_from_icon_name(icon, Gtk.IconSize.BUTTON))  # Adiciona ícone
            button.set_always_show_image(True)  # Mostra ícone sempre
            button.set_size_request(120, 60)  # Tamanho mínimo: 120x60px
            button.set_sensitive(False)  # Desativado inicialmente (até selecionar extensão)
            button.connect("clicked", self.on_action_selected, action_id)  # Conecta clique ao método
            action_box.pack_start(button, False, False, 0)  # Adiciona à caixa
            self.action_buttons[action_id] = button  # Guarda referência
        
        # ========================================================
        # SECÇÃO 4: BOTÕES FINAIS (Cancelar e Executar)
        # ========================================================
        
        # Cria caixa horizontal para botões finais
        final_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=15)
        final_box.set_margin_top(15)
        final_box.set_margin_bottom(10)
        final_box.set_halign(Gtk.Align.CENTER)
        main_box.pack_start(final_box, False, False, 10)
        
        # Botão Cancelar (sempre ativo, estilo destrutivo/vermelho)
        cancel_btn = Gtk.Button(label="❌ Cancelar")
        cancel_btn.set_size_request(150, 50)
        cancel_btn.get_style_context().add_class('destructive-action')
        cancel_btn.connect("clicked", self.on_cancel_clicked)
        final_box.pack_start(cancel_btn, False, False, 0)
        
        # Botão Executar (desativado inicialmente, estilo sugerido/verde)
        self.exec_btn = Gtk.Button(label="✅ Executar")
        self.exec_btn.set_size_request(150, 50)
        self.exec_btn.get_style_context().add_class('suggested-action')
        self.exec_btn.set_sensitive(False)  # Desativado até selecionar extensão e ação
        self.exec_btn.connect("clicked", self.on_execute_clicked)
        final_box.pack_start(self.exec_btn, False, False, 0)
        
        # Label de status (mostra informação sobre seleção atual)
        self.status_label = Gtk.Label()
        self.status_label.set_markup("<span size='small' style='italic'>Selecione pelo menos uma extensão</span>")
        self.status_label.get_style_context().add_class('dim-label')
        main_box.pack_start(self.status_label, False, False, 5)
        
        # Mostra todos os elementos da interface
        self.show_all()
    
    # --------------------------------------------------------
    # MÉTODO: extract_extension
    # --------------------------------------------------------
    # Extrai e valida a extensão de um ficheiro
    # Regras:
    #   - Considera texto após o último ponto
    #   - Mínimo: MIN_EXTENSION_LENGTH caracteres
    #   - Máximo: MAX_EXTENSION_LENGTH caracteres
    #   - Apenas caracteres alfanuméricos
    #   - Se não cumprir regras, retorna "[Sem Extensão]"
    # --------------------------------------------------------
    def extract_extension(self, filename):
        # Verifica se há ponto no nome do ficheiro
        if '.' not in filename:
            return "[Sem Extensão]"
        
        # Ignora ficheiros que começam com ponto (ex: .hidden)
        # A menos que tenham outro ponto (ex: .config.txt)
        if filename.startswith('.'):
            if '.' not in filename[1:]:
                return "[Sem Extensão]"
        
        # Obtém texto após o último ponto
        # Exemplo: "arquivo.tar.gz" → "gz"
        ext = filename.rsplit('.', 1)[-1]
        
        # Valida comprimento da extensão
        if len(ext) < MIN_EXTENSION_LENGTH or len(ext) > MAX_EXTENSION_LENGTH:
            return "[Sem Extensão]"
        
        # Valida se contém apenas caracteres alfanuméricos
        # Permite underscore (_) e hífen (-) em alguns casos
        if not ext.replace('_', '').replace('-', '').isalnum():
            return "[Sem Extensão]"
        
        # Retorna em minúsculas para consistência
        # Exemplo: "PDF" → "pdf"
        return ext.lower()
    
    # --------------------------------------------------------
    # MÉTODO: load_selected_files
    # --------------------------------------------------------
    # Carrega os ficheiros selecionados no Nautilus
    # Lê da variável de ambiente NAUTILUS_SCRIPT_SELECTED_FILE_PATHS
    # --------------------------------------------------------
    def load_selected_files(self):
        # Obtém caminhos dos ficheiros selecionados (separados por nova linha)
        paths = os.environ.get('NAUTILUS_SCRIPT_SELECTED_FILE_PATHS', '')
        
        # Verifica se há ficheiros selecionados
        if not paths.strip():
            self.show_error("Nenhum ficheiro selecionado.")
            self.close()
            return
        
        # Divide string em lista de caminhos
        selected = [p for p in paths.strip().split('\n') if p.strip()]
        
        # Processa cada caminho
        for path in selected:
            # Verifica se é ficheiro (não pasta)
            if os.path.isfile(path):
                self.all_files.append(path)  # Adiciona à lista geral
                filename = os.path.basename(path)  # Obtém apenas nome do ficheiro
                
                # Extrai e valida extensão
                ext = self.extract_extension(filename)
                
                # Atualiza contagem e lista por extensão
                self.ext_counts[ext] += 1
                self.ext_files[ext].append(path)
        
        # Verifica se há ficheiros válidos
        if not self.all_files:
            self.show_error("A seleção não contém ficheiros válidos (apenas pastas).")
            self.close()
            return
        
        # Calcula estatísticas
        no_ext_count = self.ext_counts.get("[Sem Extensão]", 0)
        with_ext_count = len(self.all_files) - no_ext_count
        
        # Atualiza label de informação
        self.info_label.set_markup(
            f"<b>Total:</b> {len(self.all_files)} ficheiros | "
            f"<b>Com extensão:</b> {with_ext_count} | "
            f"<b>Sem extensão:</b> {no_ext_count}"
        )
        
        # Preenche lista de checkboxes
        self.populate_extension_list()
    
    # --------------------------------------------------------
    # MÉTODO: populate_extension_list
    # --------------------------------------------------------
    # Cria checkboxes para cada extensão encontrada
    # Nenhum checkbox começa selecionado
    # --------------------------------------------------------
    def populate_extension_list(self):
        # Itera sobre extensões ordenadas alfabeticamente
        for ext in sorted(self.ext_counts.keys()):
            # Cria linha da lista
            row = Gtk.ListBoxRow()
            row.set_activatable(False)  # Linha não é clicável (apenas checkbox)
            
            # Cria caixa horizontal para checkbox + contador
            hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=15)
            hbox.set_margin_start(10)
            hbox.set_margin_end(10)
            hbox.set_margin_top(8)
            hbox.set_margin_bottom(8)
            
            # Cria checkbox (NÃO selecionado inicialmente)
            checkbox = Gtk.CheckButton(label=ext)
            checkbox.set_active(False)  # Garante que começa desmarcado
            checkbox.connect("toggled", self.on_extension_toggled, ext)  # Conecta evento
            
            # Cria label com quantidade de ficheiros
            count_label = Gtk.Label()
            count_label.set_markup(f"<b>{self.ext_counts[ext]}</b> ficheiros")
            count_label.set_halign(Gtk.Align.END)  # Alinha à direita
            count_label.set_hexpand(True)  # Expande para ocupar espaço
            
            # Adiciona elementos à caixa
            hbox.pack_start(checkbox, False, False, 0)
            hbox.pack_start(count_label, False, False, 0)
            row.add(hbox)
            
            # Adiciona linha à lista
            self.ext_listbox.add(row)
            self.ext_checkboxes[ext] = checkbox  # Guarda referência
        
        # Mostra todos os elementos
        self.ext_listbox.show_all()
    
    # --------------------------------------------------------
    # MÉTODO: on_extension_toggled
    # --------------------------------------------------------
    # Executado quando um checkbox é marcado/desmarcado
    # Atualiza estado dos botões e status
    # --------------------------------------------------------
    def on_extension_toggled(self, checkbox, ext):
        self.update_buttons_state()  # Ativa/desativa botões
        self.update_status()  # Atualiza label de status
    
    # --------------------------------------------------------
    # MÉTODO: update_buttons_state
    # --------------------------------------------------------
    # Ativa ou desativa botões conforme seleção do utilizador
    # Regras:
    #   - Botões de ação: ativos se houver extensão selecionada
    #   - Botão Executar: ativo se houver extensão E ação selecionada
    # --------------------------------------------------------
    def update_buttons_state(self):
        # Verifica se há pelo menos um checkbox marcado
        has_selection = any(cb.get_active() for cb in self.ext_checkboxes.values())
        
        # Ativa/desativa todos os botões de ação
        for btn in self.action_buttons.values():
            btn.set_sensitive(has_selection)
        
        # Ativa/desativa botão Executar
        self.exec_btn.set_sensitive(has_selection and self.selected_action is not None)
    
    # --------------------------------------------------------
    # MÉTODO: on_action_selected
    # --------------------------------------------------------
    # Executado quando um botão de ação é clicado
    # Highlight do botão selecionado e atualiza estado
    # --------------------------------------------------------
    def on_action_selected(self, button, action_id):
        # Remove highlight de todos os botões
        for btn in self.action_buttons.values():
            btn.get_style_context().remove_class('suggested-action')
        
        # Adiciona highlight ao botão selecionado
        button.get_style_context().add_class('suggested-action')
        
        # Guarda ID da ação selecionada
        self.selected_action = action_id
        
        # Verifica se há extensão selecionada
        has_selection = any(cb.get_active() for cb in self.ext_checkboxes.values())
        
        # Ativa botão Executar se houver seleção
        self.exec_btn.set_sensitive(has_selection)
        
        # Atualiza label de status
        self.update_status()
    
    # --------------------------------------------------------
    # MÉTODO: update_status
    # --------------------------------------------------------
    # Atualiza label de status com informação da seleção atual
    # Mostra: extensões selecionadas, ação, número de ficheiros
    # --------------------------------------------------------
    def update_status(self):
        selected_count = 0   # Contador de ficheiros selecionados
        selected_exts = []   # Lista de extensões selecionadas
        
        # Itera sobre checkboxes
        for ext, checkbox in self.ext_checkboxes.items():
            if checkbox.get_active():  # Se checkbox estiver marcado
                selected_count += self.ext_counts[ext]  # Soma contagem
                selected_exts.append(ext)  # Adiciona à lista
        
        # Se houver seleção
        if selected_count > 0:
            # Cria string com extensões (mostra máx 3, depois "+X")
            exts_str = ", ".join(selected_exts[:3])
            if len(selected_exts) > 3:
                exts_str += f" (+{len(selected_exts) - 3})"
            
            # Se ação já estiver selecionada
            if self.selected_action:
                self.status_label.set_markup(
                    f"<span weight='bold'>Extensões:</span> {exts_str} | "
                    f"<span weight='bold'>Ação:</span> {self.selected_action.upper()} | "
                    f"<span weight='bold'>Ficheiros:</span> {selected_count}"
                )
            else:
                # Ação ainda não selecionada
                self.status_label.set_markup(
                    f"<span weight='bold'>Extensões:</span> {exts_str} | "
                    f"<span weight='bold'>Ficheiros:</span> {selected_count} | "
                    f"<span style='italic'>Selecione uma ação</span>"
                )
        else:
            # Nenhuma seleção
            self.status_label.set_markup(
                "<span size='small' style='italic'>Selecione pelo menos uma extensão</span>"
            )
    
    # --------------------------------------------------------
    # MÉTODO: filter_files
    # --------------------------------------------------------
    # Filtra ficheiros pelas extensões selecionadas
    # Cria lista filtered_files com todos os ficheiros das extensões marcadas
    # --------------------------------------------------------
    def filter_files(self):
        self.filtered_files = []  # Limpa lista anterior
        
        # Itera sobre checkboxes
        for ext, checkbox in self.ext_checkboxes.items():
            if checkbox.get_active():  # Se checkbox estiver marcado
                # Adiciona todos os ficheiros dessa extensão
                self.filtered_files.extend(self.ext_files[ext])
    
    # --------------------------------------------------------
    # MÉTODO: on_key_press
    # --------------------------------------------------------
    # Handler para eventos de teclado
    # Atalhos: Enter = Executar, Esc = Cancelar
    # --------------------------------------------------------
    def on_key_press(self, widget, event):
        # Tecla Enter ou Enter do teclado numérico
        if event.keyval == Gdk.KEY_Return or event.keyval == Gdk.KEY_KP_Enter:
            if self.exec_btn.get_sensitive():  # Se botão estiver ativo
                self.on_execute_clicked(None)
            return True
        # Tecla Escape
        elif event.keyval == Gdk.KEY_Escape:
            self.on_cancel_clicked(None)
            return True
        return False
    
    # --------------------------------------------------------
    # MÉTODO: on_cancel_clicked
    # --------------------------------------------------------
    # Executado quando botão Cancelar é clicado
    # Fecha a janela sem executar nenhuma ação
    # --------------------------------------------------------
    def on_cancel_clicked(self, button):
        self.close()
    
    # --------------------------------------------------------
    # MÉTODO: on_execute_clicked
    # --------------------------------------------------------
    # Método principal que executa a ação selecionada
    # Divide-se em 3 tipos: Copiar/Mover (pede pasta), 
    # Eliminar/Reciclagem/Backup (pede confirmação)
    # --------------------------------------------------------
    def on_execute_clicked(self, button):
        # Verifica se há ação selecionada
        if not self.selected_action:
            self.show_error("Selecione uma ação primeiro.")
            return
        
        # Filtra ficheiros pelas extensões selecionadas
        self.filter_files()
        
        # Verifica se há ficheiros para processar
        if not self.filtered_files:
            self.show_error("Nenhum ficheiro selecionado.")
            return
        
        # Dicionário com nomes das ações para exibição
        action_names = {
            "copy": "COPIAR",
            "move": "MOVER",
            "trash": "ENVIAR PARA RECICLAGEM",
            "delete": "ELIMINAR PERMANENTEMENTE",
            "backup": "BACKUP"
        }
        
        # Obtém nome da ação selecionada
        action_name = action_names.get(self.selected_action, self.selected_action)
        
        # ========================================================
        # AÇÕES QUE PRECISAM DE SELETOR DE PASTA (Copiar e Mover)
        # ========================================================
        if self.selected_action in ["copy", "move"]:
            # Abre janela de seleção de pasta
            dest = self.select_folder_dialog(f"Selecione a Pasta de Destino para {action_name}")
            
            # Se utilizador cancelou seleção
            if not dest or dest == "":
                return
            
            # Valida se pasta existe
            if not os.path.isdir(dest):
                self.show_error("Pasta de destino inválida.")
                return
            
            # Executa ação em cada ficheiro
            count = 0   # Contador de sucesso
            errors = 0  # Contador de erros
            for f in self.filtered_files:
                try:
                    if self.selected_action == "copy":
                        shutil.copy2(f, dest)  # Copia mantendo metadata
                    else:
                        shutil.move(f, dest)   # Move ficheiro
                    count += 1
                except Exception as e:
                    errors += 1
                    print(f"Erro: {e}")
            
            # Mostra resultado ao utilizador
            if errors == 0:
                self.show_info(
                    f"✅ {action_name} CONCLUÍDA",
                    f"{count} ficheiros {action_name.lower()} para:\n<span font='monospace'>{dest}</span>"
                )
            else:
                self.show_info(
                    f"⚠️ {action_name} PARCIAL",
                    f"{count} ficheiros {action_name.lower()} com sucesso.\n{errors} falharam."
                )
            
            # Fecha janela
            self.close()
            return
        
        # ========================================================
        # AÇÕES QUE PRECISAM DE CONFIRMAÇÃO (Eliminar, Reciclagem, Backup)
        # ========================================================
        
        # --------------------------------------------------------
        # AÇÃO: ELIMINAR PERMANENTEMENTE
        # --------------------------------------------------------
        if self.selected_action == "delete":
            msg = "⚠️ <b>ELIMINAÇÃO PERMANENTE</b> ⚠️\n\n"
            msg += f"<b>{len(self.filtered_files)}</b> ficheiros serão eliminados\n\n"
            msg += "<span color='red' weight='bold'>NÃO poderão ser recuperados!</span>"
            confirm = self.show_confirm("Confirmar Eliminação", msg, danger=True)
            
            if not confirm:
                return
            
            count = 0
            for f in self.filtered_files:
                try:
                    os.remove(f)  # Elimina ficheiro permanentemente
                    count += 1
                except Exception as e:
                    print(f"Erro: {e}")
            self.show_info("⚠️ ELIMINAÇÃO CONCLUÍDA", f"{count} ficheiros eliminados permanentemente.")
            self.close()
        
        # --------------------------------------------------------
        # AÇÃO: ENVIAR PARA RECICLAGEM
        # --------------------------------------------------------
        elif self.selected_action == "trash":
            msg = "🗑️ <b>RECICLAGEM</b>\n\n"
            msg += f"<b>{len(self.filtered_files)}</b> ficheiros serão enviados para o lixo\n\n"
            msg += "Poderá recuperá-los do lixo mais tarde."
            confirm = self.show_confirm("Confirmar Reciclagem", msg, danger=False)
            
            if not confirm:
                return
            
            count = 0
            errors = 0
            error_details = []
            
            for f in self.filtered_files:
                try:
                    # Método 1: Usar comando 'gio trash' (mais robusto no GNOME)
                    if subprocess.run(["gio", "trash", f], 
                                    capture_output=True, 
                                    timeout=30).returncode == 0:
                        count += 1
                        continue
                    
                    # Método 2: Fallback para Gio.File.trash()
                    file = Gio.File.new_for_path(f)
                    result, error = file.trash(None)
                    
                    if result:
                        count += 1
                    else:
                        # Gio.trash() retornou False com erro
                        if error:
                            error_details.append(f"{os.path.basename(f)}: {error.message}")
                        else:
                            error_details.append(f"{os.path.basename(f)}: Falha desconhecida")
                        errors += 1
                        
                except Exception as e:
                    # Método 3: Fallback manual (mover para ~/.local/share/Trash/files)
                    try:
                        trash_files = os.path.expanduser("~/.local/share/Trash/files")
                        trash_info = os.path.expanduser("~/.local/share/Trash/info")
                        
                        # Criar pastas do lixo se não existirem
                        os.makedirs(trash_files, exist_ok=True)
                        os.makedirs(trash_info, exist_ok=True)
                        
                        # Gerar nome único para evitar conflitos
                        dest_name = os.path.basename(f)
                        dest_path = os.path.join(trash_files, dest_name)
                        
                        # Se já existir, adicionar sufixo
                        counter = 1
                        while os.path.exists(dest_path):
                            name, ext = os.path.splitext(dest_name)
                            dest_name = f"{name}_{counter}{ext}"
                            dest_path = os.path.join(trash_files, dest_name)
                        
                        # Mover ficheiro
                        shutil.move(f, dest_path)
                        
                        # Criar ficheiro .trashinfo (formato FreeDesktop)
                        info_path = os.path.join(trash_info, f"{dest_name}.trashinfo")
                        with open(info_path, 'w', encoding='utf-8') as info_file:
                            info_file.write("[Trash Info]\n")
                            info_file.write(f"Path={os.path.abspath(f)}\n")
                            info_file.write(f"DeletionDate={GLib.DateTime.new_now_local().format('%Y-%m-%dT%H:%M:%S')}\n")
                        
                        count += 1
                        
                    except Exception as fallback_error:
                        errors += 1
                        error_details.append(f"{os.path.basename(f)}: {str(e)}")
                        print(f"Erro fallback trash {f}: {fallback_error}")
            
            # Mostrar resultado ao utilizador
            if errors == 0:
                self.show_info("🗑️ RECICLAGEM CONCLUÍDA", 
                             f"{count} ficheiros enviados para o lixo.")
            elif count > 0:
                # Parcialmente concluído
                self.show_info("⚠️ RECICLAGEM PARCIAL", 
                             f"{count} ficheiros enviados para o lixo.\n"
                             f"{errors} falharam:\n\n" + "\n".join(error_details[:5]))
            else:
                # Tudo falhou
                self.show_error("❌ RECICLAGEM FALHOU\n\n" + 
                              "Nenhum ficheiro foi enviado para o lixo.\n\n" +
                              "Possíveis causas:\n"
                              "• Ficheiros em uso por outra aplicação\n"
                              "• Sem permissões de escrita\n"
                              "• Sistema de ficheiros não suporta lixo\n\n" +
                              "Erros:\n" + "\n".join(error_details[:3]))
            
            self.close()        
        # --------------------------------------------------------
        # AÇÃO: BACKUP
        # --------------------------------------------------------
        elif self.selected_action == "backup":
            msg = "💾 <b>BACKUP</b>\n\n"
            msg += f"<b>{len(self.filtered_files)}</b> ficheiros serão copiados para:\n"
            msg += "<b>pasta 'backup'</b> na mesma localização\n\n"
            msg += "Os ficheiros originais não serão alterados."
            confirm = self.show_confirm("Confirmar Backup", msg, danger=False)
            
            if not confirm:
                return
            
            if self.filtered_files:
                # Obtém pasta do primeiro ficheiro
                first_file = self.filtered_files[0]
                # Cria caminho da pasta backup
                backup_dir = os.path.join(os.path.dirname(first_file), "backup")
                # Cria pasta se não existir
                os.makedirs(backup_dir, exist_ok=True)
                
                count = 0
                for f in self.filtered_files:
                    try:
                        shutil.copy2(f, backup_dir)  # Copia para pasta backup
                        count += 1
                    except Exception as e:
                        print(f"Erro: {e}")
                
                self.show_info("💾 BACKUP CONCLUÍDO", f"{count} ficheiros copiados para:\n<span font='monospace'>{backup_dir}</span>")
            
            self.close()
    
    # --------------------------------------------------------
    # MÉTODO: select_folder_dialog
    # --------------------------------------------------------
    # Abre janela de seleção de pastas
    # Retorna caminho da pasta selecionada ou None se cancelar
    # --------------------------------------------------------
    def select_folder_dialog(self, title):
        # Cria diálogo de seleção de ficheiro/pasta
        dialog = Gtk.FileChooserDialog(
            title=title,
            parent=self,
            action=Gtk.FileChooserAction.SELECT_FOLDER,  # Modo: selecionar pasta
            buttons=(
                "_Cancelar",
                Gtk.ResponseType.CANCEL,
                "_Selecionar Pasta",
                Gtk.ResponseType.OK
            )
        )
        dialog.set_position(Gtk.WindowPosition.CENTER_ON_PARENT)  # Centraliza na janela pai
        dialog.set_modal(True)  # Modal (bloqueia janela pai)
        dialog.set_select_multiple(False)  # Apenas uma pasta
        
        # Executa diálogo e espera resposta
        response = dialog.run()
        
        # Processa resposta
        if response == Gtk.ResponseType.OK:
            folder = None
            
            # Método 1: get_filename()
            folder = dialog.get_filename()
            
            # Método 2: get_uri() e converter para caminho
            if not folder:
                uri = dialog.get_uri()
                if uri:
                    folder = Gio.File.new_for_uri(uri).get_path()
            
            # Método 3: get_current_folder()
            if not folder:
                folder = dialog.get_current_folder()
        else:
            folder = None
        
        # Fecha diálogo
        dialog.destroy()
        return folder
    
    # --------------------------------------------------------
    # MÉTODO: show_confirm
    # --------------------------------------------------------
    # Mostra diálogo de confirmação (Sim/Não)
    # Retorna True se utilizador clicar em Sim, False caso contrário
    # --------------------------------------------------------
    def show_confirm(self, title, message, danger=False):
        dialog = Gtk.MessageDialog(
            parent=self,
            flags=Gtk.DialogFlags.MODAL,  # Modal
            message_type=Gtk.MessageType.WARNING if danger else Gtk.MessageType.QUESTION,
            buttons=Gtk.ButtonsType.YES_NO,
            text=title,
        )
        dialog.format_secondary_markup(message)  # Texto secundário com formatação
        dialog.set_position(Gtk.WindowPosition.CENTER_ON_PARENT)
        
        response = dialog.run()
        dialog.destroy()
        return response == Gtk.ResponseType.YES
    
    # --------------------------------------------------------
    # MÉTODO: show_info
    # --------------------------------------------------------
    # Mostra diálogo de informação (apenas botão OK)
    # Usado para confirmar conclusão de operações
    # --------------------------------------------------------
    def show_info(self, title, message):
        dialog = Gtk.MessageDialog(
            parent=self,
            flags=Gtk.DialogFlags.MODAL,
            message_type=Gtk.MessageType.INFO,
            buttons=Gtk.ButtonsType.OK,
            text=title,
        )
        dialog.format_secondary_markup(message)
        dialog.set_position(Gtk.WindowPosition.CENTER_ON_PARENT)
        dialog.run()
        dialog.destroy()
    
    # --------------------------------------------------------
    # MÉTODO: show_error
    # --------------------------------------------------------
    # Mostra diálogo de erro (apenas botão OK)
    # Usado para notificar problemas ao utilizador
    # --------------------------------------------------------
    def show_error(self, message):
        dialog = Gtk.MessageDialog(
            parent=self,
            flags=Gtk.DialogFlags.MODAL,
            message_type=Gtk.MessageType.ERROR,
            buttons=Gtk.ButtonsType.OK,
            text="Erro",
        )
        dialog.format_secondary_markup(message)
        dialog.set_position(Gtk.WindowPosition.CENTER_ON_PARENT)
        dialog.run()
        dialog.destroy()


# ============================================================
# PONTO DE ENTRADA PRINCIPAL
# ============================================================
# Este código é executado quando o script é iniciado
# Cria a janela e inicia o loop principal do GTK
# ============================================================
if __name__ == "__main__":
    # Inicializa biblioteca GTK
    Gtk.init()
    
    # Cria instância da janela principal
    window = FileExtensionManager()
    
    # Conecta evento de fechar janela ao fim do programa
    window.connect("destroy", Gtk.main_quit)
    
    # Mostra todos os elementos da janela
    window.show_all()
    
    # Inicia loop principal do GTK (aguarda eventos do utilizador)
    Gtk.main()