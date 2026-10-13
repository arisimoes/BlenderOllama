import json
import urllib.request
import urllib.error
import base64
import pathlib
import bpy


def _image_to_base64(path: str) -> str | None:
    """Return a base64 data URI for an image file, or None if path is empty/invalid."""
    if not path:
        return None
    p = pathlib.Path(path)
    if not p.is_file():
        return None
    ext = p.suffix.lower().lstrip('.')
    if ext in ('jpg', 'jpeg'):
        mime = 'image/jpeg'
    elif ext == 'png':
        mime = 'image/png'
    else:
        mime = 'image/png'
    try:
        data = p.read_bytes()
        b64 = base64.b64encode(data).decode('utf-8')
        return f"data:{mime};base64,{b64}"
    except Exception as e:
        raise RuntimeError(f"Não foi possível ler a imagem {path}: {e}") from e


def get_preferences():
    return bpy.context.preferences.addons[__package__].preferences


def _make_request(url: str, payload: dict | None, headers: dict, timeout: int, method: str = "POST") -> dict:
    data = None
    if payload is not None:
        data = json.dumps(payload).encode("utf-8")

    request = urllib.request.Request(
        url,
        data=data,
        headers=headers,
        method=method,
    )

    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            raw = response.read().decode("utf-8")
            if not raw:
                return {}
            return json.loads(raw)
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8")
        raise RuntimeError(f"Erro HTTP {e.code}: {body}") from e
    except urllib.error.URLError as e:
        raise RuntimeError(f"Não foi possível conectar ao servidor. O serviço está rodando? ({e.reason})") from e
    except json.JSONDecodeError as e:
        raise RuntimeError(f"Resposta inválida do servidor: {e}") from e


def _default_headers(prefs) -> dict:
    headers = {"Content-Type": "application/json"}
    if prefs.api_key:
        headers["Authorization"] = f"Bearer {prefs.api_key}"
    return headers


def _normalize_base_url(url: str) -> str:
    return url.rstrip("/")


def generate_ollama(prompt: str, model: str | None = None, system: str | None = None, image_path: str | None = None) -> str:
    prefs = get_preferences()
    url = f"{_normalize_base_url(prefs.base_url)}/api/generate"

    payload = {
        "model": model or prefs.ollama_model,
        "prompt": prompt,
        "system": system or prefs.system_prompt,
        "stream": False,
    }

    image_b64 = _image_to_base64(image_path) if image_path else None
    if image_b64:
        payload["images"] = [image_b64]

    result = _make_request(url, payload, _default_headers(prefs), prefs.request_timeout)
    return result.get("response", "")


def generate_openai(prompt: str, model: str | None = None, system: str | None = None, image_path: str | None = None) -> str:
    prefs = get_preferences()
    url = f"{_normalize_base_url(prefs.base_url)}/v1/chat/completions"

    content = [{"type": "text", "text": prompt}]
    image_b64 = _image_to_base64(image_path) if image_path else None
    if image_b64:
        content.append({"type": "image_url", "image_url": {"url": image_b64}})

    payload = {
        "model": model or prefs.ollama_model,
        "messages": [
            {"role": "system", "content": system or prefs.system_prompt},
            {"role": "user", "content": content},
        ],
        "temperature": 0.2,
    }

    result = _make_request(url, payload, _default_headers(prefs), prefs.request_timeout)
    choices = result.get("choices", [])
    if not choices:
        raise RuntimeError("Resposta da API não contém choices.")
    return choices[0].get("message", {}).get("content", "")


def generate(prompt: str, model: str | None = None, system: str | None = None, image_path: str | None = None) -> str:
    """Send a generate request to the configured backend and return the response text."""
    prefs = get_preferences()
    if prefs.backend == 'OPENAI':
        return generate_openai(prompt, model, system, image_path)
    return generate_ollama(prompt, model, system, image_path)


def list_models() -> list[str]:
    """Return the list of model ids/names available on the configured backend."""
    prefs = get_preferences()
    base = _normalize_base_url(prefs.base_url)

    if prefs.backend == 'OPENAI':
        url = f"{base}/v1/models"
        result = _make_request(url, None, _default_headers(prefs), 5, method="GET")
        return [m.get("id", "?") for m in result.get("data", [])]

    # Ollama native
    url = f"{base}/api/tags"
    result = _make_request(url, None, _default_headers(prefs), 5, method="GET")
    return [m.get("name", "?") for m in result.get("models", [])]


def check_connection() -> str:
    """Verify connectivity with the configured backend."""
    try:
        models = list_models()
        if models:
            return f"Conectado! Modelos disponíveis: {', '.join(models[:5])}"
        return "Conectado, mas nenhum modelo foi encontrado."
    except Exception as e:
        backend_name = "OpenAI-Compatible" if get_preferences().backend == 'OPENAI' else "Ollama"
        raise RuntimeError(f"Falha na conexão {backend_name}: {e}") from e
