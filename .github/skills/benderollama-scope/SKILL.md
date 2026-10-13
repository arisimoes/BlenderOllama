---
name: benderollama-scope
description: 'Escopo e regras do projeto BenderOllama. Use sempre que o usuário falar sobre "BenderOllama", "BlenderOllama", "Blender GPT", "Ollama no Blender", "automação do Blender com IA local" ou ao implementar funcionalidades deste add-on.'
argument-hint: 'Contexto de implementação ou dúvida sobre o BenderOllama'
user-invocable: true
---

# BenderOllama — Escopo do Projeto

## Propósito

Criar um add-on para o Blender que se conecte ao servidor local do Ollama e gera/executa scripts Python automaticamente, sem depender de APIs pagas ou de nuvem.

## Terminologia

- **Nome do projeto:** BenderOllama
- **Namespace de IDs do Blender:** `BO` / `bender_ollama` / `bo_`
- **Categoria da UI:** Sidebar do 3D Viewport chamada "BenderOllama"

## Arquitetura do Add-on

O add-on é dividido em módulos independentes:

| Arquivo | Responsabilidade |
|---------|-------------------|
| `__init__.py` | Registro/deregistro de classes, bl_info, entrypoint |
| `preferences.py` | Preferências do Blender (backend, base URL, API key, modelo, system prompt, timeout) |
| `ollama_client.py` | Chamadas HTTP para Ollama nativo (`/api/generate`) ou provedores OpenAI-Compatible (`/v1/chat/completions`) |
| `ui.py` | Painéis da interface (prompt, histórico, botão executar) |
| `operators.py` | Operadores do Blender (enviar prompt, testar conexão, limpar histórico) |
| `utils.py` | Sanitização de código, logging, execução segura com `exec()` |

## Regras de Implementação

1. **Apenas código Python puro:** A resposta da IA deve ser sanitizada para remover markdown (```python, ```, explicações, etc.) antes de ser executada.
2. **Execução segura:** Todo código gerado deve rodar dentro de `try/except` e reportar erros claros no UI do Blender.
3. **Configurável:** O usuário pode escolher entre backend Ollama nativo ou OpenAI-Compatible, definir base URL, API key, modelo e system prompt nas preferências.
4. **Feedback imediato:** Usar `self.report({'INFO'}/{'ERROR'})` e atualizar a interface durante processamento.
5. **Histórico:** Armazenar os prompts e as respostas no `bpy.types.Scene` para consulta rápida.
6. **Privacidade da chave:** A API key é armazenada como `subtype='PASSWORD'` nas preferências do Blender.

## System Prompt Padrão

```text
You are BenderOllama, a coding assistant specialized in Blender's Python API (bpy). 
Respond ONLY with valid Python code for Blender. 
Do not write explanations, comments, markdown code fences, or any other text. 
Your entire response must be executable Python code that manipulates Blender objects, materials, meshes, or scene data.
```

## Comportamentos Esperados

- O usuário digita o prompt na sidebar e clica em "Executar Comando".
- O add-on envia o prompt para o backend configurado (Ollama local/remoto ou provedor OpenAI-Compatible) com o system prompt.
- A resposta é sanitizada e executada no Blender.
- Em caso de erro de sintaxe ou execução, o erro é exibido no UI e logado no console.
- O usuário pode testar a conexão com o botão "Testar Conexão" nas preferências.

## Exemplos de Prompts Válidos

- "Crie um cubo no centro da cena com escala 2."
- "Adicione uma Suzanne e rotacione 45 graus no eixo Y."
- "Crie um material vermelho e aplique ao objeto selecionado."
- "Delete todos os objetos da cena e crie 5 esferas aleatórias."

## Não-fazeres

- Não conectar a APIs pagas externas (OpenAI, Anthropic, etc.).
- Não executar código sem sanitização ou sem captura de exceção.
- Não modificar preferências de sistema do usuário sem permissão explícita.
- Não usar nomes de classes, IDs ou propriedades fora do namespace `bo_`/`bender_ollama`.

## Setup do Ambiente (para testes)

### Ollama local
1. Instalar o Ollama: https://ollama.com
2. Baixar um modelo compatível: `ollama pull llama3` ou `ollama pull codellama`
3. Garantir que o servidor está rodando: `ollama serve` ou via app do Ollama
4. Instalar o add-on no Blender via `Edit > Preferences > Add-ons > Install from Disk`

### Provedor cloud (OpenAI-Compatible)
1. Obter uma API key do provedor escolhido.
2. Configurar nas preferências: backend `OpenAI-Compatible`, base URL, API key e nome exato do modelo.
3. Usar o botão "Testar Conexão" antes de executar o primeiro prompt.
