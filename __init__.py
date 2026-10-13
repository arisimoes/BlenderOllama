import bpy
from . import utils
from . import preferences, ui, operators


# Register PropertyGroup types first, since other classes depend on them.
property_group_classes = [
    utils.BenderOllamaHistoryItem,
    utils.BenderOllamaModelItem,
]

addon_classes = [
    preferences.BenderOllamaPreferences,
    operators.BO_OT_TestConnection,
    operators.BO_OT_RefreshModels,
    operators.BO_OT_ExecutePrompt,
    operators.BO_OT_PasteImagePath,
    operators.BO_OT_ClearImagePath,
    operators.BO_OT_RerunHistoryItem,
    operators.BO_OT_ClearHistory,
    operators.BO_OT_OpenPopup,
    ui.BENDER_OLLAMA_PT_Panel,
    ui.BENDER_OLLAMA_PT_HistoryPanel,
    ui.BENDER_OLLAMA_MT_Menu,
]


def register():
    for cls in property_group_classes:
        bpy.utils.register_class(cls)

    for cls in addon_classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.bo_prompt = bpy.props.StringProperty(
        name="Prompt",
        description="Digite o comando para a IA local",
        default="Crie um macaco (Suzanne) no centro da cena"
    )

    bpy.types.Scene.bo_image_path = bpy.props.StringProperty(
        name="Imagem de Referência",
        description="Caminho absoluto de uma imagem PNG/JPG para enviar junto ao prompt",
        default="",
        subtype='FILE_PATH'
    )

    bpy.types.Scene.bo_history = bpy.props.CollectionProperty(
        type=utils.BenderOllamaHistoryItem
    )
    bpy.types.Scene.bo_history_index = bpy.props.IntProperty(default=-1)

    bpy.types.Scene.bo_is_processing = bpy.props.BoolProperty(default=False)

    bpy.types.Scene.bo_progress = bpy.props.FloatProperty(
        name="Progresso",
        default=0.0,
        min=0.0,
        max=1.0,
        subtype='FACTOR'
    )

    bpy.types.Scene.bo_available_models = bpy.props.CollectionProperty(
        type=utils.BenderOllamaModelItem
    )
    bpy.types.Scene.bo_available_models_index = bpy.props.IntProperty(default=-1)

    bpy.types.Scene.bo_selected_model = bpy.props.StringProperty(
        name="Modelo",
        description="Modelo selecionado para execução do prompt",
        default=""
    )


def unregister():
    for cls in reversed(addon_classes):
        bpy.utils.unregister_class(cls)

    for cls in reversed(property_group_classes):
        bpy.utils.unregister_class(cls)

    del bpy.types.Scene.bo_prompt
    del bpy.types.Scene.bo_image_path
    del bpy.types.Scene.bo_history
    del bpy.types.Scene.bo_history_index
    del bpy.types.Scene.bo_is_processing
    del bpy.types.Scene.bo_available_models
    del bpy.types.Scene.bo_available_models_index
    del bpy.types.Scene.bo_selected_model
    del bpy.types.Scene.bo_progress


if __name__ == "__main__":
    register()
