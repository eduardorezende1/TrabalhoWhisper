import gradio as gr
import requests

def envia(audio):
    url = "http://backend:9000/asr/?language=pt"
    with open(audio, 'rb') as f:
        r = requests.post(url, files={"audio_file": f})

    texto = r.content.decode("utf-8").strip()
    imagem_url = None

    if texto.lower().startswith("desenhe") or texto.lower().startswith("desenha"):
        prompt = texto.lower().replace("desenhe", "").replace("desenha", "").strip()
        prompt = prompt or "uma imagem aleatória"
        imagem_url = f"https://image.pollinations.ai/prompt/{prompt.replace(' ', '%20')}"

    return texto, imagem_url

ui = gr.Interface(
    fn=envia,
    inputs=gr.Audio(sources="microphone", type="filepath", label="Fale algo..."),
    outputs=[
        gr.Textbox(label="Transcrição", lines=2, interactive=False),
        gr.Image(label="Imagem gerada (se você pedir um desenho)")
    ],
    title="Transcrição + Geração de Imagem com Pollinations.AI",
    description="Fale normalmente ou diga 'desenhe um(a)...' para gerar uma imagem."
)

if __name__ == "__main__":
    ui.launch(server_name="0.0.0.0", server_port=7861)
