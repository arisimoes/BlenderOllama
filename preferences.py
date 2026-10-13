import bpy
from . import utils


class BenderOllamaPreferences(bpy.types.AddonPreferences):
    bl_idname = __package__

    backend: bpy.props.EnumProperty(
        name="Backend",
        description="Protocolo da API a ser usado",
        items=[
            ('OLLAMA', "Ollama Nativo", "Usa /api/generate do Ollama (local ou remoto)"),
            ('OPENAI', "OpenAI-Compatible", "Usa /v1/chat/completions (Kimi, OpenRouter, Together, etc.)"),
        ],
        default='OLLAMA',
    )

    base_url: bpy.props.StringProperty(
        name="Base URL",
        description="URL base da API. Ex: http://localhost:11434 ou https://api.moonshot.cn",
        default="http://localhost:11434",
    )

    api_key: bpy.props.StringProperty(
        name="API Key",
        description="Chave de API para serviços cloud (deixe vazio para Ollama local sem autenticação)",
        default="",
        subtype='PASSWORD',
    )

    ollama_model: bpy.props.StringProperty(
        name="Modelo Padrão",
        description="Nome do modelo. Ex: llama3, codellama, mistral, kimi-k2.70code:cloud",
        default="llama3",
    )

    system_prompt: bpy.props.StringProperty(
        name="System Prompt",
        description="Instrução inicial enviada ao modelo",
        default=utils.DEFAULT_SYSTEM_PROMPT,
    )

    request_timeout: bpy.props.IntProperty(
        name="Timeout (segundos)",
        description="Tempo máximo de espera pela resposta",
        default=120,
        min=10,
        max=600,
    )

    def draw(self, context):
        layout = self.layout

        layout.prop(self, "backend")
        layout.prop(self, "base_url")
        layout.prop(self, "api_key")
        layout.prop(self, "ollama_model")
        layout.prop(self, "request_timeout")

        layout.separator()
        layout.label(text="System Prompt:")
        layout.prop(self, "system_prompt", text="")

        layout.separator()
        row = layout.row()
        row.operator("bo.test_connection", text="Testar Conexão", icon='PLUGIN')


classes = [BenderOllamaPreferences]


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
