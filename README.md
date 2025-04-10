# Projeto para a matéria de Serviços de Software 2025


Eduardo José Rezende Cardozo 19.00100-2

Luca Zanfelici Fanucchi 19.00228-9

# Projeto Whisper + Pollinations

Este projeto integra a API do [Whisper](https://openai.com/research/whisper) para transcrição automática de áudio com a geração de imagens baseada em comandos de voz, utilizando a API do [Pollinations](https://pollinations.ai/).

# Funcionalidades

- **Transcrição de Áudio com Whisper**  
  O usuário grava um áudio, e a API do Whisper converte a fala em texto.

- **Interpretação de Comandos de Voz**  
  O sistema detecta comandos iniciados com frases como "desenhe uma...". O conteúdo posterior é extraído como *prompt* para gerar uma imagem.

- **Geração de Imagens com Pollinations.ai**  
  O texto extraído é enviado como prompt para a API do Pollinations, que retorna uma imagem gerada com base na descrição do usuário.

- **Histórico Local**  
  O sistema mantém os últimos registros de uso, permitindo que o usuário acesse:
  - As **10 últimas imagens** geradas.
  - Os **10 últimos áudios** gravados.


---

