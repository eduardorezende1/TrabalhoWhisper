import gradio as gr
import requests
import json
import os

# Caminho para armazenar o histórico
HISTORICO_PATH = "historico.json"

# Função para carregar histórico
def carregar_historico():
    if os.path.exists(HISTORICO_PATH):
        with open(HISTORICO_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

# Função para salvar histórico
def salvar_historico(dado):
    historico = carregar_historico()
    historico.insert(0, dado)  # adiciona no início
    with open(HISTORICO_PATH, "w", encoding="utf-8") as f:
        json.dump(historico[:10], f, indent=2)  # salva no máximo 10 entradas

# Função principal
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

    salvar_historico({"texto": texto, "imagem": imagem_url})
    return texto, imagem_url, atualizar_historico(), atualizar_galeria()

# Atualiza lista de transcrições
def atualizar_historico():
    historico = carregar_historico()
    return [item["texto"] for item in historico if item["texto"]]

# Atualiza galeria de imagens
def atualizar_galeria():
    historico = carregar_historico()
    return [item["imagem"] for item in historico if item["imagem"]]

# INTERFACE
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
                <img src="https://maua.br/images/logo-IMT.png" alt="Logo IMT" style="height: 70px; margin-bottom: 10px;" />
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

        with gr.Row(elem_classes="card"):
            historico_textos = gr.List(label="📜 Histórico de Transcrições")
            galeria_imagens = gr.Gallery(label="🎨 Galeria de Imagens", columns=3, object_fit="contain")

        gr.Markdown(
            "<div style='text-align: center; margin-top: 30px;'>"
            "Desenvolvido por <strong>Eduardo Rezende e Luca Zanfelici Fanucchi</strong> – Projeto IMT 2025"
            "</div>"
        )

        # Conexão da entrada com a função
        audio_input.change(
            fn=envia,
            inputs=audio_input,
            outputs=[text_output, image_output, historico_textos, galeria_imagens]
        )

if __name__ == "__main__":
    ui.launch(server_name="0.0.0.0", server_port=7861)
