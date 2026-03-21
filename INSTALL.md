# 📦 Guia de Instalação Detalhado

Este guia fornece instruções passo a passo para instalar o script **Gerir Ficheiros por Extensão** no seu sistema Linux com GNOME/Nautilus.

## 📋 Pré-requisitos

Antes de começar, verifique se tem os seguintes componentes instalados:

### 1. Sistema Operativo

- Debian 13 (Trixie) ou superior
- Ubuntu 20.04 ou superior
- Fedora 35 ou superior
- Qualquer distribuição Linux com GNOME 40+

### 2. Verificar Versões

```bash
# Verificar versão do Python
python3 --version
# Deve ser 3.6 ou superior

# Verificar versão do GNOME
gnome-shell --version
# Deve ser 40 ou superior

# Verificar Nautilus
nautilus --version
# Deve ser 40 ou superior
```





## 🚀 Instalação Passo a Passo
### Passo 1: Atualizar Sistema
```bash
sudo apt update
sudo apt upgrade -y
```
### Passo 2: Instalar Dependências
```bash
# Dependências GTK e Python
sudo apt install python3-gi python3-gi-cairo gir1.2-gtk-3.0 -y

# Verificar instalação
python3 -c "import gi; print('GTK OK')"
```
### Passo 3: Criar Pasta de Scripts
```bash
# Criar diretório (se não existir)
mkdir -p ~/.local/share/nautilus/scripts/

# Verificar permissões
ls -la ~/.local/share/nautilus/
```
### Passo 4: Obter o Script
#### Opção A: Git Clone
```bash
cd ~
git clone https://github.com/SEU_USERNAME/gerir-ficheiros-extensao.git
cd gerir-ficheiros-extensao
cp "Gerir Ficheiros" ~/.local/share/nautilus/scripts/
```
#### Opção B: Download Manual
1. Descarregue o ficheiro **Gerir Ficheiros**
2. Copie para *~/.local/share/nautilus/scripts/*
```bash
cp ~/Downloads/"Gerir Ficheiros" ~/.local/share/nautilus/scripts/
```
#### Opção C: Criar Manualmente
```bash
nano ~/.local/share/nautilus/scripts/"Gerir Ficheiros"
# Cole o código do script
# Ctrl+O para guardar, Ctrl+X para sair
```
### Passo 5: Definir Permissões

```
# Tornar executável
chmod +x ~/.local/share/nautilus/scripts/"Gerir Ficheiros"

# Verificar permissões
ls -la ~/.local/share/nautilus/scripts/
# Deve mostrar: -rwxr-xr-x
```


### Passo 6: Reiniciar Nautilus
```bash
# Fechar Nautilus
nautilus -q

# Abrir Nautilus (opcional, abre automaticamente quando necessário)
nautilus &
```
### Passo 7: Verificar Instalação
1. Abra o **Nautilus**
2. Selecione alguns ficheiros
3. Clique direito → **Scripts**
4. Verifique se **Gerir Ficheiros** aparece na lista
## 🔧 Configuração Opcional
### Personalizar Limite de Extensão
Edite o script:
```bash
nano ~/.local/share/nautilus/scripts/"Gerir Ficheiros"
```
Altere as variáveis no início:
```bash
MAX_EXTENSION_LENGTH = 5  # Altere conforme necessário (1-10)
MIN_EXTENSION_LENGTH = 1
```
## Adicionar Atalho de Teclado
Pode criar um atalho personalizado nas definições do GNOME:
1. **Definições** → **Teclado** → ***Atalhos Personalizados**
2. Adicionar novo atalho
3. Comando: *~/.local/share/nautilus/scripts/"Gerir Ficheiros"*
4. Definir tecla de atalho

## ✅ Testar Instalação
### Teste Básico
```bash
# Criar ficheiros de teste
mkdir -p ~/teste_script
touch ~/teste_script/arquivo1.jpg
touch ~/teste_script/arquivo2.jpg
touch ~/teste_script/documento.pdf

# Selecionar e executar no Nautilus
nautilus ~/teste_script
# Selecione os ficheiros → Botão direito → Scripts → Gerir Ficheiros
```
### Teste de Funcionalidades
```
┌──────────────────────────┬─────────────────────────────────────┐
│   Teste                  │  Ação Esperada                      │
├──────────────────────────┼─────────────────────────────────────┤
│   Selecionar extensões   │  Checkboxes aparecem corretamente   │
├──────────────────────────┼─────────────────────────────────────┤
│   Clicar em Backup       │  Abre confirmação                   │
├──────────────────────────┼─────────────────────────────────────┤
│   Clicar em Copiar       │ Abre seletor de pasta               │
├──────────────────────────┼─────────────────────────────────────┤
│   Clicar em Eliminar     │  Abre aviso de perigo               │
├──────────────────────────┼─────────────────────────────────────┤
│   Tecla Enter            │  Executa ação selecionada           │
├──────────────────────────┼─────────────────────────────────────┤
│   Tecla Esc              │  ancela e fecha                     │
└──────────────────────────┴─────────────────────────────────────┘
```

## 🐛 Resolução de Problemas
### Problema: Script não aparece no menu
Solução:
```bash
# Verificar se ficheiro existe
ls -la ~/.local/share/nautilus/scripts/"Gerir Ficheiros"

# Verificar permissões
chmod +x ~/.local/share/nautilus/scripts/"Gerir Ficheiros"

# Reiniciar Nautilus
nautilus -q
nautilus &
```
### Problema: Erro ao abrir (GTK)
Solução:
```bash
# Reinstalar dependências
sudo apt install --reinstall python3-gi gir1.2-gtk-3.0

# Verificar import Python
python3 -c "from gi.repository import Gtk; print('OK')"
```
### Problema: Erro de permissão
Solução:
```bash
# Corrigir proprietário
chown $USER:$USER ~/.local/share/nautilus/scripts/"Gerir Ficheiros"

# Corrigir permissões
chmod 755 ~/.local/share/nautilus/scripts/"Gerir Ficheiros"
```
### Problema: Interface não abre
Solução:
```bash
# Testar execução manual
NAUTILUS_SCRIPT_SELECTED_FILE_PATHS="" python3 ~/.local/share/nautilus/scripts/"Gerir Ficheiros"

# Verificar erros no terminal
```
## 📞 Suporte
Se encontrar problemas não listados:

1. Verifique os Issues no GitHub
2. Crie um novo issue com detalhes do erro
3. Inclua a versão do sistema e GNOME 

Última atualização: 2026-03-21