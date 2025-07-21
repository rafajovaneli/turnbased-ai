# 🤝 Guia de Contribuição

Obrigado por considerar contribuir para o **Combate por Turnos com IA**!

## 📋 Como Contribuir

### 🐛 Reportar Bugs

1. Verifique se o bug já foi reportado nas [Issues](https://github.com/rafajovaneli/turnbased-ai/issues)
2. Se não encontrar, crie uma nova issue com:
   - **Título claro** descrevendo o problema
   - **Passos para reproduzir** o bug
   - **Comportamento esperado** vs **comportamento atual**
   - **Screenshots** se aplicável
   - **Informações do sistema** (OS, Python version, etc.)

### 💡 Sugerir Melhorias

1. Abra uma issue com a tag `enhancement`
2. Descreva claramente:
   - **O que** você gostaria de ver
   - **Por que** seria útil
   - **Como** poderia ser implementado

### 🔧 Contribuir com Código

#### Configuração do Ambiente

```bash
# 1. Fork o repositório
git clone https://github.com/rafajovaneli/turnbased-ai.git
cd turnbased-ai

# 2. Crie um ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows

# 3. Instale dependências
pip install -r requirements.txt

# 4. Execute os testes
python -m unittest discover tests/
```

#### Processo de Desenvolvimento

1. **Crie uma branch** para sua feature:

   ```bash
   git checkout -b feature/nome-da-feature
   ```

2. **Faça suas mudanças** seguindo os padrões:

   - Código Python seguindo PEP 8
   - Docstrings para funções e classes
   - Comentários explicativos quando necessário

3. **Adicione testes** para novas funcionalidades:

   ```python
   def test_nova_funcionalidade(self):
       # Teste sua funcionalidade aqui
       pass
   ```

4. **Execute os testes**:

   ```bash
   python -m unittest discover tests/ -v
   ```

5. **Commit suas mudanças**:

   ```bash
   git add .
   git commit -m "feat: adiciona nova funcionalidade"
   ```

6. **Push para sua branch**:

   ```bash
   git push origin feature/nome-da-feature
   ```

7. **Abra um Pull Request**

## 📝 Padrões de Código

### Python Style Guide

- Siga o [PEP 8](https://pep8.org/)
- Use nomes descritivos para variáveis e funções
- Mantenha funções pequenas e focadas
- Adicione docstrings para classes e funções públicas

```python
def calculate_damage(attacker, defender, base_damage):
    """
    Calcula o dano final considerando ataque e defesa.

    Args:
        attacker (Character): Personagem atacante
        defender (Character): Personagem defensor
        base_damage (int): Dano base do ataque

    Returns:
        int: Dano final calculado
    """
    # Implementação aqui
    pass
```

### Commits Semânticos

Use o padrão [Conventional Commits](https://www.conventionalcommits.org/):

- `feat:` nova funcionalidade
- `fix:` correção de bug
- `docs:` mudanças na documentação
- `style:` formatação, sem mudança de lógica
- `refactor:` refatoração de código
- `test:` adição ou correção de testes
- `chore:` tarefas de manutenção

Exemplos:

```
feat: adiciona sistema de som
fix: corrige bug na IA neural
docs: atualiza README com novas instruções
```

## 🧪 Testes

### Executar Testes

```bash
# Todos os testes
python -m unittest discover tests/

# Teste específico
python -m unittest tests.test_engine.TestGameEngine.test_character_attack

# Com verbose
python -m unittest discover tests/ -v
```

### Escrever Testes

- Teste todas as funcionalidades públicas
- Use nomes descritivos para os testes
- Organize testes em classes lógicas
- Teste casos extremos e de erro

```python
class TestNovaFuncionalidade(unittest.TestCase):
    def setUp(self):
        """Configuração executada antes de cada teste"""
        self.character = Character("Teste", 100, 20, 5)

    def test_funcionalidade_normal(self):
        """Testa comportamento normal"""
        result = self.character.nova_funcionalidade()
        self.assertEqual(result, expected_value)

    def test_funcionalidade_caso_extremo(self):
        """Testa caso extremo"""
        # Teste aqui
        pass
```

## 📚 Documentação

### Atualizando Documentação

- Mantenha o README.md atualizado
- Adicione docstrings para novas funções
- Atualize o CHANGELOG.md
- Inclua exemplos de uso quando relevante

### Estrutura de Docstrings

```python
def exemplo_funcao(param1, param2=None):
    """
    Breve descrição da função.

    Descrição mais detalhada se necessário, explicando
    o comportamento e casos especiais.

    Args:
        param1 (str): Descrição do primeiro parâmetro
        param2 (int, optional): Descrição do segundo parâmetro.
            Defaults to None.

    Returns:
        bool: Descrição do valor retornado

    Raises:
        ValueError: Quando param1 está vazio
        TypeError: Quando param2 não é int

    Example:
        >>> resultado = exemplo_funcao("teste", 42)
        >>> print(resultado)
        True
    """
    pass
```

## 🎯 Áreas que Precisam de Ajuda

### 🔥 Alta Prioridade

- [ ] Correções de bugs críticos
- [ ] Melhorias de performance
- [ ] Testes para funcionalidades não cobertas

### 🚀 Novas Funcionalidades

- [ ] Sistema de som
- [ ] Múltiplos tipos de personagens
- [ ] Salvamento de progresso
- [ ] Multiplayer local

### 📚 Documentação

- [ ] Tutoriais para iniciantes
- [ ] Documentação da API
- [ ] Exemplos de uso avançado

### 🎨 Interface

- [ ] Temas visuais
- [ ] Animações aprimoradas
- [ ] Responsividade

## ❓ Dúvidas?

- Abra uma [Issue](https://github.com/rafajovaneli/turnbased-ai/issues) com a tag `question`
- Entre em contato: rafajovaneli@gmail.com

## 🙏 Reconhecimento

Todos os contribuidores serão reconhecidos no README.md e releases.

Obrigado por contribuir! 🎉
