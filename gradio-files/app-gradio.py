import gradio as gr
import requests
import json

def envia(audio):
    url = "http://backend:9000/asr/"
    with open(audio,'rb') as f:
        r = requests.post(url, files={"audio_file": f})
    return r.content

ui = gr.Interface(fn=envia, inputs=gr.Audio(sources="microphone", type="filepath"), outputs="text")
    
if __name__ == "__main__":
    ui.launch(server_name="0.0.0.0", server_port=7861, show_api=False)
