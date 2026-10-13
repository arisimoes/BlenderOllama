import bpy


class BENDER_OLLAMA_PT_Panel(bpy.types.Panel):
    bl_label = "BenderOllama Assistant"
    bl_idname = "BENDER_OLLAMA_PT_Panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'BenderOllama'

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        layout.label(text="O que vamos construir, humano?", icon='CONSOLE')
        layout.prop(scene, "bo_prompt", text="")

        # Reference image UI
        img_box = layout.box()
        img_box.label(text="Imagem de Referência", icon='IMAGE')
        row = img_box.row(align=True)
        row.prop(scene, "bo_image_path", text="")
        row.operator("bo.capture_viewport", text="", icon='RESTRICT_RENDER_OFF')
        row.operator("bo.paste_image_path", text="", icon='PASTEDOWN')
        row.operator("bo.clear_image_path", text="", icon='X')
        if scene.bo_image_path and "blenderollama_viewport" in scene.bo_image_path:
            img_box.label(text="Imagem: screenshot da viewport", icon='SCENE')

        # Model selection UI
        box = layout.box()
        box.label(text="Modelo", icon='PRESET')
        row = box.row(align=True)
        row.prop(scene, "bo_selected_model", text="")
        row.operator("bo.refresh_models", text="", icon='FILE_REFRESH')

        if len(scene.bo_available_models) == 0:
            box.label(text="Clique em refresh para listar modelos", icon='INFO')
        else:
            row2 = box.row()
            row2.prop_search(scene, "bo_selected_model", scene, "bo_available_models", text="Escolher")
            if scene.bo_selected_model:
                box.label(text=f"Selecionado: {scene.bo_selected_model[:40]}", icon='CHECKMARK')

        row = layout.row()
        row.enabled = not scene.bo_is_processing
        row.operator("bo.execute_prompt", text="Executar Comando", icon='LIGHT_DATA')

        if scene.bo_is_processing:
            box = layout.box()
            box.alert = True
            box.label(text="⏳ BenderOllama está pensando...", icon='TEMP')
            box.progress(factor=scene.bo_progress, text="Aguardando resposta do modelo")
            box.label(text="O Blender continua respondendo.", icon='INFO')


class BENDER_OLLAMA_PT_HistoryPanel(bpy.types.Panel):
    bl_label = "Histórico"
    bl_idname = "BENDER_OLLAMA_PT_HistoryPanel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'BenderOllama'

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        if not scene.bo_history:
            layout.label(text="Nenhum comando executado ainda.")
            return

        for idx, item in enumerate(reversed(scene.bo_history)):
            box = layout.box()
            box.label(text=f"Prompt: {item.prompt[:60]}{'...' if len(item.prompt) > 60 else ''}")
            status = "Sucesso" if item.success else "Erro"
            icon = 'CHECKMARK' if item.success else 'ERROR'
            box.label(text=f"Status: {status}", icon=icon)
            col = box.column(align=True)
            for line in item.response.splitlines()[:8]:
                col.label(text=line[:55])
            if len(item.response.splitlines()) > 8:
                col.label(text="...")
            rerun = box.operator("bo.rerun_history_item", text="Reexecutar", icon='FILE_REFRESH')
            rerun.item_index = idx

        layout.separator()
        layout.operator("bo.clear_history", text="Limpar Histórico", icon='TRASH')


class BENDER_OLLAMA_MT_Menu(bpy.types.Menu):
    bl_label = "BenderOllama"
    bl_idname = "BENDER_OLLAMA_MT_Menu"

    def draw(self, context):
        layout = self.layout
        layout.operator("bo.open_popup", text="Abrir BenderOllama", icon='CONSOLE')
        layout.separator()
        layout.operator("bo.execute_prompt", text="Executar Último Prompt", icon='LIGHT_DATA')


classes = [BENDER_OLLAMA_PT_Panel, BENDER_OLLAMA_PT_HistoryPanel, BENDER_OLLAMA_MT_Menu]


def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.VIEW3D_MT_object.append(menu_draw)


def unregister():
    bpy.types.VIEW3D_MT_object.remove(menu_draw)

    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)


def menu_draw(self, context):
    self.layout.separator()
    self.layout.menu("BENDER_OLLAMA_MT_Menu", icon='CONSOLE')
