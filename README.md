# BenderOllama

IA para automação do Blender via Ollama local ou provedores OpenAI-compatible — inspirado no BlenderGPT, mas com suporte a modelos locais **e** modelos cloud como `kimi-k2.70code:cloud`.

[![Release](https://img.shields.io/github/v/release/arisimoes/BlenderOllama)](https://github.com/arisimoes/BlenderOllama/releases/latest)

## O que faz

BenderOllama adiciona uma aba lateral dentro do Blender. Você digita o que quer criar em linguagem natural, o add-on consulta o modelo de IA escolhido, recebe código Python e executa automaticamente dentro do Blender — sem travar a interface.

## Requisitos

- **Blender 5.2 ou superior** (extensões do novo sistema de add-ons do Blender 5.x)
- Ollama rodando localmente **ou** uma API key de provedor compatível com OpenAI

## Instalação

### 1. Baixe o add-on

Vá até a [página de releases](https://github.com/arisimoes/BlenderOllama/releases/latest) e baixe o arquivo **`BenderOllama.zip`**.

> Não baixe o código-fonte diretamente pelo botão verde `<> Code` — o zip da release já tem a estrutura correta para instalação no Blender.

### 2. Instale no Blender 5.2

1. Abra o Blender.
2. Vá em **Edit > Preferences > Add-ons > Install Extension from Disk...**
3. Selecione o `BenderOllama.zip` baixado.
4. O add-on aparecerá em **Extensions > User Default**. Ative-o clicando na caixa de seleção.

### 3. Configure o backend

#### Opção A: Ollama local (grátis, 100% local)

1. Baixe e instale o Ollama: https://ollama.com
2. Baixe um modelo recomendado:
   ```bash
   ollama pull llama3
   ```
3. Garanta que o servidor está rodando:
   ```bash
   ollama serve
   ```

#### Opção B: Provedor cloud compatível (Kimi, OpenRouter, Together, etc.)

1. Crie uma conta no provedor e gere uma **API key**.
2. Anote a **Base URL** e o nome exato do modelo.

## Uso

1. Abra o painel lateral no 3D Viewport pressionando `N`.
2. Clique na aba **BenderOllama** (ou use **Object > BenderOllama** no menu superior).
3. Digite o comando, por exemplo: `Crie um cubo no centro da cena com escala 2`.
4. Clique em **Executar Comando**.

O Blender mostrará uma barra de progresso enquanto o modelo processa a resposta. O código gerado é executado automaticamente na cena.

## Configuração

Em **Edit > Preferences > Add-ons > BenderOllama**, você pode alterar:

- **Backend**: `Ollama Nativo` ou `OpenAI-Compatible`
- **Base URL**: ex. `http://localhost:11434`, `https://api.moonshot.cn`, `https://openrouter.ai/api`
- **API Key**: chave do provedor cloud (deixe vazio para Ollama local)
- **Modelo padrão**: ex. `llama3`, `kimi-k2.70code:cloud`, `mistral`
- **System Prompt**: instrução enviada ao modelo
- **Timeout**: tempo máximo de espera pela resposta

Use o botão **Testar Conexão** para verificar se a API está acessível.

### Exemplos de configuração

| Provedor | Backend | Base URL | Modelo |
|----------|---------|----------|--------|
| Ollama local | Ollama Nativo | `http://localhost:11434` | `llama3` |
| Kimi (Moonshot) | OpenAI-Compatible | `https://api.moonshot.cn` | `kimi-k2.70code:cloud` |
| OpenRouter | OpenAI-Compatible | `https://openrouter.ai/api` | `qwen/qwen-2.5-coder:free` |
| OpenAI | OpenAI-Compatible | `https://api.openai.com/v1` | `gpt-4o-mini` |

## Dicas de Prompt

- Seja específico: "Crie 5 esferas distribuídas aleatoriamente na cena."
- Mencione propriedades: "Crie um material vermelho e aplique ao objeto selecionado."
- Para transformações: "Rotacione o objeto selecionado 45 graus no eixo Y."
- O add-on mantém um histórico de comandos para você reutilizar ou consultar.

## Estrutura do Projeto

```
blanderollama/
├── __init__.py        # Registro do add-on
├── preferences.py     # Configurações
├── ollama_client.py   # Comunicação com a API local
├── ui.py              # Painéis da interface
├── operators.py       # Botões e ações
└── utils.py           # Sanitização e execução segura
```

## Licença

MIT — veja [LICENSE](LICENSE).
