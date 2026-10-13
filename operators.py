import bpy
import threading
from . import ollama_client, utils


class BO_OT_TestConnection(bpy.types.Operator):
    bl_idname = "bo.test_connection"
    bl_label = "Testar Conexão com Ollama"
    bl_options = {'REGISTER'}

    def execute(self, context):
        try:
            message = ollama_client.check_connection()
            self.report({'INFO'}, f"BenderOllama: {message}")
        except Exception as e:
            self.report({'ERROR'}, f"BenderOllama: {str(e)}")
        return {'FINISHED'}


class BO_OT_ExecutePrompt(bpy.types.Operator):
    bl_idname = "bo.execute_prompt"
    bl_label = "Execute Ollama Prompt"
    bl_options = {'REGISTER', 'UNDO'}

    _timer = None
    _thread = None
    _result = None
    _error = None
    _done = False
    _prompt = ""

    def execute(self, context):
        prompt = context.scene.bo_prompt
        if not prompt.strip():
            self.report({'WARNING'}, "Digite um prompt antes de executar.")
            return {'CANCELLED'}

        self._prompt = prompt
        self._result = None
        self._error = None
        self._done = False
        context.scene.bo_is_processing = True
        self.report({'INFO'}, f"BenderOllama processando: {prompt}")

        self._thread = threading.Thread(target=self._generate_in_thread, args=(prompt,))
        self._thread.start()

        wm = context.window_manager
        self._timer = wm.event_timer_add(0.1, window=context.window)
        wm.modal_handler_add(self)

        return {'RUNNING_MODAL'}

    def _generate_in_thread(self, prompt):
        try:
            self._result = ollama_client.generate(prompt)
        except Exception as e:
            self._error = str(e)
        finally:
            self._done = True

    def modal(self, context, event):
        if event.type == 'TIMER':
            if self._done:
                return self._finish(context)
        return {'PASS_THROUGH'}

    def _finish(self, context):
        wm = context.window_manager
        if self._timer:
            wm.event_timer_remove(self._timer)
            self._timer = None

        context.scene.bo_is_processing = False

        try:
            if self._error:
                raise Exception(self._error)

            utils.execute_code(self._result)
            self.add_to_history(context, self._prompt, self._result, success=True)
            self.report({'INFO'}, "BenderOllama: Comando executado!")
        except Exception as e:
            error_message = str(e)
            self.add_to_history(context, self._prompt, error_message, success=False)
            self.report({'ERROR'}, f"BenderOllama errou: {error_message}")
        finally:
            for area in context.screen.areas:
                area.tag_redraw()

        return {'FINISHED'}

    def add_to_history(self, context, prompt, response, success):
        item = context.scene.bo_history.add()
        item.prompt = prompt
        item.response = response
        item.success = success


class BO_OT_ClearHistory(bpy.types.Operator):
    bl_idname = "bo.clear_history"
    bl_label = "Limpar Histórico"
    bl_options = {'REGISTER'}

    def execute(self, context):
        context.scene.bo_history.clear()
        context.scene.bo_history_index = -1
        self.report({'INFO'}, "Histórico limpo.")
        return {'FINISHED'}


class BO_OT_OpenPopup(bpy.types.Operator):
    """Open BenderOllama in a floating popup panel."""
    bl_idname = "bo.open_popup"
    bl_label = "BenderOllama"
    bl_options = {'REGISTER'}

    def execute(self, context):
        return {'FINISHED'}

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self, width=400)

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        layout.label(text="BenderOllama", icon='CONSOLE')
        layout.prop(scene, "bo_prompt", text="Prompt")

        row = layout.row()
        row.enabled = not scene.bo_is_processing
        row.operator("bo.execute_prompt", text="Executar", icon='LIGHT_DATA')

        if scene.bo_is_processing:
            layout.label(text="Processando...", icon='TEMP')

        if scene.bo_history:
            layout.separator()
            layout.label(text="Últimos comandos:")
            for item in list(scene.bo_history)[-3:]:
                status = "OK" if item.success else "Erro"
                layout.label(text=f"{status}: {item.prompt[:40]}{'...' if len(item.prompt) > 40 else ''}")


classes = [BO_OT_TestConnection, BO_OT_ExecutePrompt, BO_OT_ClearHistory, BO_OT_OpenPopup]


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
