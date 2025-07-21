# 🚀 Guia de Instalação

Este guia fornece instruções detalhadas para instalar e executar o **Combate por Turnos com IA**.

## 📋 Pré-requisitos

### Sistema Operacional

- ✅ Windows 10/11
- ✅ macOS 10.14+
- ✅ Linux (Ubuntu 18.04+, Fedora 30+, etc.)

### Software Necessário

- **Python 3.7+** ([Download](https://python.org/downloads/))
- **pip** (incluído com Python)
- **Git** ([Download](https://git-scm.com/downloads))

### Verificar Instalação

```bash
python --version    # Deve mostrar 3.7+
pip --version      # Deve mostrar versão do pip
git --version      # Deve mostrar versão do git
```

---

## 🎯 Instalação Rápida

### Método 1: Clone e Execute (Recomendado)

```bash
# 1. Clone o repositório
git clone https://github.com/rafajovaneli/turnbased-ai.git
cd turnbased-ai

# 2. Instale dependências
pip install -r requirements.txt

# 3. Execute o jogo
python run_window_manager.py
```

### Método 2: Instalação via pip (Futuro)

```bash
# Quando disponível no PyPI
pip install combate-turnos-ia

# Execute
combate-turnos
```

---

## 🔧 Instalação Detalhada

### 1. Preparar Ambiente

#### Windows

```cmd
# Abra o Command Prompt ou PowerShell
# Navegue para onde deseja instalar
cd C:\Projetos

# Clone o repositório
git clone https://github.com/rafajovaneli/turnbased-ai.git
cd combate-turnos-ia
```

#### macOS/Linux

```bash
# Abra o Terminal
# Navegue para onde deseja instalar
cd ~/Projetos

# Clone o repositório
git clone https://github.com/rafajovaneli/turnbased-ai.git
cd turnbased-ai
```

### 2. Ambiente Virtual (Recomendado)

```bash
# Crie um ambiente virtual
python -m venv venv

# Ative o ambiente virtual
# Windows:
venv\Scripts\activate

# macOS/Linux:
source venv/bin/activate

# Você deve ver (venv) no início do prompt
```

### 3. Instalar Dependências

```bash
# Dependências obrigatórias
pip install numpy

# Dependências opcionais (recomendadas)
pip install Pillow

# Ou instale todas de uma vez
pip install -r requirements.txt
```

### 4. Verificar Instalação

```bash
# Execute os testes
python -m unittest discover tests/ -v

# Se todos passarem, a instalação está correta
```

---

## 🎮 Executar o Jogo

### Interface Completa (Recomendado)

```bash
python run_window_manager.py
```

- Menu principal com seleção de IA
- Interface moderna
- Todas as funcionalidades

### Console Clássico

```bash
python main.py
```

- Versão em linha de comando
- Ideal para servidores sem GUI

### Demo da IA Neural

```bash
python demo_neural_ai.py
```

- Demonstração das capacidades
- Menu interativo

---

## 🛠️ Instalação para Desenvolvimento

### Configuração Completa

```bash
# 1. Clone e navegue
git clone https://github.com/rafajovaneli/turnbased-ai.git
cd turnbased-ai

# 2. Ambiente virtual
python -m venv venv
source venv/bin/activate  # ou venv\Scripts\activate no Windows

# 3. Instale em modo desenvolvimento
pip install -e .

# 4. Instale dependências de desenvolvimento
pip install -e ".[dev]"

# 5. Configure pre-commit hooks (opcional)
pre-commit install
```

### Ferramentas de Desenvolvimento

```bash
# Formatação de código
black game/ tests/

# Linting
flake8 game/ tests/

# Type checking
mypy game/

# Testes com cobertura
pytest --cov=game tests/
```

---

## 🐛 Solução de Problemas

### Erro: "ModuleNotFoundError: No module named 'numpy'"

```bash
# Instale numpy
pip install numpy

# Ou instale todas as dependências
pip install -r requirements.txt
```

### Erro: "tkinter not found"

#### Ubuntu/Debian:

```bash
sudo apt-get install python3-tk
```

#### CentOS/RHEL/Fedora:

```bash
sudo yum install tkinter
# ou
sudo dnf install python3-tkinter
```

#### macOS:

```bash
# Tkinter vem com Python no macOS
# Se não funcionar, reinstale Python via Homebrew
brew install python-tk
```

### Erro: "Permission denied"

#### Linux/macOS:

```bash
# Adicione permissões de execução
chmod +x run_window_manager.py

# Ou execute com python
python run_window_manager.py
```

#### Windows:

```cmd
# Execute como administrador se necessário
# Ou use:
python run_window_manager.py
```

### Erro: "Git not found"

- Instale Git: https://git-scm.com/downloads
- Ou baixe o ZIP do repositório diretamente

### Performance Lenta

```bash
# Verifique se numpy está instalado
python -c "import numpy; print(numpy.__version__)"

# Se não estiver, instale:
pip install numpy
```

---

## 📦 Estrutura Após Instalação

```
combate-turnos-ia/
├── 📁 game/                 # Código principal
├── 📁 tests/                # Testes automatizados
├── 📁 venv/                 # Ambiente virtual (se criado)
├── 🎮 run_window_manager.py # Launcher principal
├── 🎯 demo_neural_ai.py     # Demo da IA
├── 📚 README.md             # Documentação
├── ⚙️ requirements.txt      # Dependências
└── 📄 LICENSE               # Licença
```

---

## 🔄 Atualização

### Atualizar o Código

```bash
# Navegue para o diretório do projeto
cd turnbased-ai

# Puxe as últimas mudanças
git pull origin main

# Atualize dependências se necessário
pip install -r requirements.txt --upgrade
```

### Verificar Versão

```bash
# Execute o jogo e verifique a versão no título
python run_window_manager.py

# Ou verifique no código
python -c "from game import __version__; print(__version__)"
```

---

## 🆘 Suporte

### Problemas Comuns

1. **Erro de importação**: Verifique se está no diretório correto
2. **Interface não abre**: Verifique se tkinter está instalado
3. **IA lenta**: Instale numpy para melhor performance

### Obter Ajuda

- 📖 Leia a [documentação completa](README.md)
- 🐛 Reporte bugs nas [Issues](https://github.com/rafajovaneli/turnbased-ai/issues)
- 💬 Faça perguntas na seção de [Discussions](https://github.com/rafajovaneli/turnbased-ai/discussions)
- 📧 Contato direto: rafajovaneli@gmail.com

---

## ✅ Próximos Passos

Após a instalação bem-sucedida:

1. 🎮 **Execute o jogo**: `python run_window_manager.py`
2. 🤖 **Teste ambas as IAs**: Minimax vs Neural
3. 📊 **Explore as estatísticas**: Veja como a IA aprende
4. 🎯 **Experimente o demo**: `python demo_neural_ai.py`
5. 🧪 **Execute os testes**: `python -m unittest discover tests/`

**Divirta-se jogando e explorando a IA! 🎉**
