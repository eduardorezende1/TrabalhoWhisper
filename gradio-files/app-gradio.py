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

with gr.Blocks(css="""
body {
    background-color: #f4f4f4;
    font-family: 'Segoe UI', sans-serif;
}

.container {
    max-width: 900px;
    margin: auto;
}

.card {
    background-color: #ffffff;
    padding: 20px;
    border-radius: 16px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.05);
    margin-bottom: 20px;
    border: 1px solid #e0e0e0;
}

h1 {
    color: #003366;
    margin-bottom: 5px;
}

h3 {
    color: #003366;
    margin-top: 0;
}

p {
    color: #333;
}

.gr-button {
    background-color: #003366 !important;
    color: white !important;
    border-radius: 8px;
}

.gr-button:hover {
    background-color: #00509e !important;
}
""") as ui:
    
    with gr.Column(elem_classes="container"):
        gr.HTML("""
        <div class="card" style="text-align: center;">
            <div style="display: flex; flex-direction: column; align-items: center;">
                <img src="https://maua.br/images/logo-IMT.png" alt="Logo IMT" style="height: 80px; margin-bottom: 10px;" />
                <h1>Instituto Mauá de Tecnologia</h1>
            </div>
            <h3>Transcrição de Áudio com Geração de Imagens</h3>
            <p>Fale normalmente ou diga <strong>'desenhe um(a)...'</strong> para gerar uma imagem via IA.</p>
        </div>
        """)


        with gr.Row(equal_height=True, elem_classes="card"):
            audio_input = gr.Audio(type="filepath", label="🎤 Grave seu áudio")
            text_output = gr.Textbox(label="📝 Transcrição", lines=2, interactive=False)

        with gr.Column(elem_classes="card"):
            image_output = gr.Image(label="🖼️ Imagem gerada (se você pedir um desenho)", show_label=True)

        gr.Markdown(
            "<div style='text-align: center; margin-top: 30px;'>"
            "Desenvolvido por <strong>Eduardo Rezende e Luca Zanfelici Fanucchi</strong> – Projeto IMT 2025"
            "</div>"
        )

        audio_input.change(fn=envia, inputs=audio_input, outputs=[text_output, image_output])

if __name__ == "__main__":
    ui.launch(server_name="0.0.0.0", server_port=7861)
