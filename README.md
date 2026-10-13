# BenderOllama

IA Local via Ollama para automação do Blender — inspirado no BlenderGPT, mas executa modelos de linguagem 100% localmente no seu computador.

## O que faz

BenderOllama adiciona uma aba lateral dentro do Blender. Você digita o que quer criar em linguagem natural, o add-on consulta o seu servidor local do Ollama, recebe código Python e executa automaticamente dentro do Blender.

## Instalação

### Opção A: Ollama local (grátis, 100% local)

1. Baixe o Ollama em https://ollama.com.
2. Baixe um modelo recomendado:
   ```bash
   ollama pull llama3
   ```
3. Garanta que o servidor está rodando:
   ```bash
   ollama serve
   ```

### Opção B: Provedor cloud compatível (Kimi, OpenRouter, Together, etc.)

1. Crie uma conta no provedor e gere uma API key.
2. Anote a **Base URL** e o nome exato do modelo.

### Instale o add-on no Blender

1. Faça o download deste repositório como `.zip`.
2. No Blender, vá em **Edit > Preferences > Add-ons > Install from Disk...**
3. Selecione o arquivo `.zip` do BenderOllama.
4. Ative o add-on marcando a caixa de seleção.

## Uso

1. Abra o painel lateral no 3D Viewport pressionando `N`.
2. Clique na aba **BenderOllama**.
3. Digite o comando, por exemplo: `Crie um cubo no centro da cena com escala 2`.
4. Clique em **Executar Comando**.

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

## Dicas de Prompt

- Seja específico: "Crie 5 esferas distribuídas aleatoriamente na cena."
- Mencione propriedades: "Crie um material vermelho e aplique ao objeto selecionado."
- Para transformações: "Rotacione o objeto selecionado 45 graus no eixo Y."

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
