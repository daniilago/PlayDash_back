# 🎮 PlayDash_back

Backend do projeto PlayDash, utilizando Flask e gerenciamento de ambiente com `uv`.

## 🚀 Como rodar o projeto

Navegue até a pasta do projeto: 
```bash
cd PlayDash_back/
```

### 1. Instale o uv

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 2. Sincronize o ambiente virtual

```bash
uv sync
```
Isso criará automaticamente um ambiente virtual e instalará as dependências listadas em `pyproject.toml`.

### 3. Ative o ambiente virtual

```bash
source .venv/bin/activate  # Linux/macOS
# ou
venv\Scripts\activate     # Windows
```

Navegue até a pasta playdash: 
```bash
cd playdash/
```

### 4. Exporte a variável do Flask

```bash
# Linux/macOS
export FLASK_APP=__init__.py     
# ou no Windows (cmd)
set FLASK_APP=__init__.py
# ou no PowerShell
$env:FLASK_APP="__init__.py"
```

### 5. Execute o servidor

```bash
flask run --debug
```
Acesse o servidor a partir da porta gerada no navegador.

# 🧹 Finalizando

Para desativar o ambiente virtual:
```bash
deactivate
```