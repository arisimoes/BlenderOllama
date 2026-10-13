import re
import bpy

DEFAULT_SYSTEM_PROMPT = (
    "You are BenderOllama, a coding assistant specialized in Blender's Python API (bpy). "
    "Respond ONLY with valid Python code for Blender. "
    "Do not write explanations, comments, markdown code fences, or any other text. "
    "Your entire response must be executable Python code that manipulates Blender objects, materials, meshes, armatures, or scene data. "
    "Prefer direct data access (bpy.data.objects, bpy.data.meshes, object.data, armature.pose.bones) over bpy.ops when possible. "
    "When you must use bpy.ops that require an active object or selection (e.g., select_all, join, delete, mode_set), "
    "use context-aware patterns such as setting context.view_layer.objects.active and calling bpy.ops with context_override or bpy.context. "
    "Assume the variable 'context' is available in the execution namespace and represents the current Blender context. "
    "When creating primitive meshes via bpy.ops.mesh.primitive_*_add, ALWAYS provide 'location' and use ONLY "
    "the exact operator parameters documented in Blender 4.x/5.x Python API. For a UV sphere use "
    "bpy.ops.mesh.primitive_uv_sphere_add(radius=..., segments=..., ring_count=..., location=(...)). "
    "Never use nonexistent parameters such as 'rings', 'stacks', 'enter_editmode', or 'align'. "
    "When manipulating armatures/bones: switch to POSE mode with bpy.ops.object.mode_set(mode='POSE'), "
    "select the target bone by setting bone.bone.select=True and armature.data.bones.active=bone.bone, "
    "and rotate using bone.rotation_euler or bone.matrix_basis. "
    "If a bone or object name cannot be found, raise a clear ValueError listing the available names. "
    "Always call bpy.context.view_layer.update() after transforms."
)


def sanitize_code(response_text: str) -> str:
    """Remove markdown code fences and any non-Python text from the model response."""
    text = response_text.strip()

    # Remove code fences like ```python ... ```
    fence_pattern = re.compile(r"```(?:python)?\s*(.*?)\s*```", re.DOTALL | re.IGNORECASE)
    match = fence_pattern.search(text)
    if match:
        return match.group(1).strip()

    # If no fences, remove leading language markers
    text = re.sub(r"^\s*python\s*\n", "", text, flags=re.IGNORECASE)

    # Strip trailing explanatory sentences that often follow the code
    lines = text.splitlines()
    code_lines = []
    for line in lines:
        if line.strip().lower().startswith("here") and "code" in line.lower():
            break
        code_lines.append(line)

    return "\n".join(code_lines).strip()


def execute_code(code: str, context=None):
    """Execute sanitized Python code inside Blender with error capture.

    The optional Blender context is injected into the namespace so generated
    scripts can call context-dependent bpy.ops safely.
    """
    code = sanitize_code(code)
    if not code:
        raise ValueError("Nenhum código Python válido foi gerado pela IA.")

    compiled_code = compile(code, "<ollama_generated>", "exec")

    namespace = {"bpy": bpy}
    if context is not None:
        namespace["context"] = context
    exec(compiled_code, namespace)


class BenderOllamaHistoryItem(bpy.types.PropertyGroup):
    prompt: bpy.props.StringProperty(name="Prompt")
    response: bpy.props.StringProperty(name="Response")
    success: bpy.props.BoolProperty(name="Success", default=True)


class BenderOllamaModelItem(bpy.types.PropertyGroup):
    name: bpy.props.StringProperty(name="Model Name")


classes = [BenderOllamaHistoryItem, BenderOllamaModelItem]


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
