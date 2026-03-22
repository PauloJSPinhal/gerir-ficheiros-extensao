# 📁 Gerir Ficheiros por Extensão

[![GNOME](https://img.shields.io/badge/GNOME-40+-blue.svg)](https://www.gnome.org/)
[![Nautilus](https://img.shields.io/badge/Nautilus-Script-green.svg)](https://wiki.gnome.org/Apps/Files)
[![Python](https://img.shields.io/badge/Python-3.6+-yellow.svg)](https://www.python.org/)
[![GTK](https://img.shields.io/badge/GTK-3.0-red.svg)](https://www.gtk.org/)

Um script Python com interface GTK para gerir ficheiros por extensão no Nautilus (GNOME Files). Permite selecionar múltiplas extensões e executar ações em lote: copiar, mover, enviar para reciclagem, eliminar permanentemente ou criar backup.

## ✨ Funcionalidades

- 🔍 **Seleção Inteligente por Extensão**: Visualiza todas as extensões dos ficheiros selecionados com contagem
- ✅ **Checkboxes Múltiplos**: Selecione uma ou várias extensões simultaneamente
- 🔢 **Validação de Extensões**: Configuração flexível do número de caracteres (1-5 por padrão)
- 🎯 **5 Ações Disponíveis**:
  - 💾 **Backup**: Copia para pasta "backup" na mesma localização
  - 📋 **Copiar**: Copia para pasta personalizada
  - 📁 **Mover**: Move para pasta personalizada
  - 🗑️ **Reciclagem**: Envia para o lixo (recuperável)
  - ⚠️ **Eliminar**: Apaga permanentemente (irrecuperável)
- ⌨️ **Navegação por Teclado**: Use Tab, Setas, Enter e Esc
- 🎨 **Interface GTK Nativa**: Integração perfeita com GNOME
- 🔒 **Confirmações de Segurança**: Confirmação para ações destrutivas

## 📸 Screenshots
### Janela Principal
```
┌─────────────────────────────────────────────────────────────┐
│           📁 Gerir Ficheiros por Extensão                   │
│  Total: 50 ficheiros | Com extensão: 45 | Sem extensão: 5   │
├─────────────────────────────────────────────────────────────┤
│  1️⃣ Selecione as Extensões (max 5 caracteres)               │
│  ┌──────────────────────────────────────────────────────┐   │
│  │ ☐ jpg                    20 ficheiros                │   │
│  │ ☐ pdf                    15 ficheiros                │   │
│  │ ☐ txt                    10 ficheiros                │   │
│  │ ☐ [Sem Extensão]         5 ficheiros                 │   │
│  └──────────────────────────────────────────────────────┘   │
├─────────────────────────────────────────────────────────────┤
│  2️⃣ Escolha a Ação                                          │
│  ┌────────┐ ┌────────┐ ┌────────┐ ┌──────────┐ ┌────────┐   │
│  │ Backup │ │ Copiar │ │  Mover │ │Reciclagem│ │Eliminar│   │
│  └────────┘ └────────┘ └────────┘ └──────────┘ └────────┘   │
├─────────────────────────────────────────────────────────────┤
│           ┌──────────┐            ┌──────────┐              │
│           │ Cancelar │            │ Executar │              │
│           └──────────┘            └──────────┘              │
└─────────────────────────────────────────────────────────────┘
```


## 📋 Requisitos

- **Sistema Operativo**: Linux (Debian 13+, Ubuntu 20.04+, Fedora, etc.)
- **Ambiente de Trabalho**: GNOME 40+
- **Gestor de Ficheiros**: Nautilus 40+
- **Python**: 3.6 ou superior
- **GTK**: 3.0 ou superior

### Dependências

```bash
python3-gi
python3-gi-cairo
gir1.2-gtk-3.0
```
## 🚀 Instalação
Consultar **INSTALL.md**

## 📖 Utilização
### Passo a Passo
1. Selecione os ficheiros no Nautilus:
	- Use *Ctrl + Clique* para seleção múltipla
	- Use *Shift + Clique* para seleção de intervalo
	- Use *Ctrl + A* para selecionar todos
2. Abra o script:
	- Clique direito nos ficheiros selecionados
	- Menu Scripts → Gerir Ficheiros por Extensão
3. Selecione as extensões:
	- Marque os checkboxes das extensões desejadas
	- Pode selecionar uma ou várias extensões
	- Visualize o número de ficheiros por extensão
4. Escolha a ação:
	- Clique num dos 5 botões de ação
	- O botão selecionado fica destacado
5. Execute:
	- Clique em ✅ Executar ou pressione Enter
	- Para ações que necessitam de pasta, selecione o destino
	- Confirme as ações destrutivas

### Atalhos de Teclado
```
┌────────────┬──────────────────────────────────┐
│   Tecla    │  Função                          │
├────────────┼──────────────────────────────────┤
│   ↑ ↓      │  Navegar entre extensões         │
├────────────┼──────────────────────────────────┤
│   Espaço   │  Marcar/desmarcar checkbox       │
├────────────┼──────────────────────────────────┤
│   Tab      │  Navegar entre botões            │
├────────────┼──────────────────────────────────┤
│   Enter    │  Executar ação (se disponível)   │
├────────────┼──────────────────────────────────┤
│   Esc      │  Cancelar e fechar               │
└────────────┴──────────────────────────────────┘
```

## ⚙️ Configuração
### Personalizar Limite de Caracteres
Edite as variáveis no início do script:

```python
MAX_EXTENSION_LENGTH = 5  # Máximo de caracteres (padrão: 5)
MIN_EXTENSION_LENGTH = 1  # Mínimo de caracteres (padrão: 1)
```
## 🎯 Casos de Uso
#### 1. Backup de Imagens
**Selecione ficheiros mistos:** Marque jpg/png → Backup → Executar
#### 2. Organizar Documentos
**Selecione Transferências:** Marque pdf → Mover → Selecione Documentos → Executar
#### 3. Limpeza de Temporários
**Selecione pasta:** Marque tmp/log/bak → Reciclagem → Executar
#### 4. Eliminação Permanente
**Selecione ficheiros:** Marque extensão → Eliminar → Confirme → Executar
## 🔧 Resolução de Problemas
```
┌───────────────────────────┬───────────────────────────────────────────────┐
│   Problema                │  Solução                                      │
├───────────────────────────┼───────────────────────────────────────────────┤
│   Script não aparece      │  chmod +x e nautilus -q                       │
├───────────────────────────┼───────────────────────────────────────────────┤
│   Erro GTK                │  sudo apt install python3-gi gir1.2-gtk-3.0   │
├───────────────────────────┼───────────────────────────────────────────────┤
│   Não encontra extensões  │  Ajuste MAX_EXTENSION_LENGTH                  │
└───────────────────────────┴───────────────────────────────────────────────┘
```

## 🤝 Contribuir

1. Faça **Fork** do projeto
2. Crie uma **Branch** (*git checkout -b feature/Novidade*)
3. Faça **Commit** (*git commit -m 'Adiciona funcionalidade'*)
4. Faça **Push** (*git push origin feature/Novidade*)
5. Abra um *Pull Request**