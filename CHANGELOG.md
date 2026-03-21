
# 📝 Changelog (Histórico de Versões)

Todas as alterações notáveis neste projeto serão documentadas neste ficheiro.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/),
e este projeto adere ao [Versionamento Semântico](https://semver.org/lang/pt-BR/).

## [1.0.0] - 2026-03-21

### ✨ Adicionado

- **Interface GTK Nativa**
  - Janela única com todas as funcionalidades
  - Design limpo e intuitivo
  - Integração perfeita com GNOME
  
- **Seleção de Extensões**
  - Checkboxes para seleção múltipla
  - Contagem de ficheiros por extensão
  - Validação configurável de caracteres (1-5 por padrão)
  
- **5 Ações Principais**
  - 💾 **Backup**: Cria pasta "backup" na mesma localização
  - 📋 **Copiar**: Copia para pasta personalizada
  - 📁 **Mover**: Move para pasta personalizada
  - 🗑️ **Reciclagem**: Envia para lixo do sistema (recuperável)
  - ⚠️ **Eliminar**: Apaga permanentemente (irrecuperável)
  
- **Navegação por Teclado**
  - Setas ↑↓ para navegar entre extensões
  - Tab para navegar entre botões
  - Enter para executar ação
  - Esc para cancelar
  
- **Segurança**
  - Confirmação para ações destrutivas
  - Avisos de perigo para eliminação permanente
  - Validação de pasta de destino
  
- **Documentação**
  - README.md completo
  - INSTALL.md com guia passo a passo
  - CHANGELOG.md (este ficheiro)
  - LICENSE (MIT)
  - Comentários completos no código

### 🔧 Melhorado

- Extração de extensão robusta
  - Considera apenas texto após último ponto
  - Valida comprimento (MIN/MAX configurável)
  - Valida caracteres alfanuméricos
  - Exemplo: "07. Memória Descritiva" → [Sem Extensão]
  
- Interface de utilizador
  - Botões com ícones intuitivos
  - Status bar informativa
  - Highlight do botão selecionado
  - Mensagens de erro claras

### 🐛 Corrigido

- Problema com `get_label_widget()` no GTK Frame
- Seletor de pasta para Copiar/Mover
- Validação de caminhos com espaços
- Caracteres especiais em nomes de ficheiros

### 📦 Dependências

```bash
python3-gi
python3-gi-cairo
gir1.2-gtk-3.0