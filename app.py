import gradio as gr
from app.func import classify_text, classify_file

def interface_text(email_text):
    result = classify_text(email_text)
    return result

def interface_file(file_obj):
    if file_obj is None:
        return {"error": "Nenhum arquivo enviado"}
    return classify_file(file_obj.name)

with gr.Blocks() as demo:
    gr.Markdown("## Classificador de E-mails")

    with gr.Tab("Classificar Texto"):
        email_input = gr.Textbox(lines=10, label="Digite o e-mail")
        output_text = gr.JSON(label="Resultado")
        btn_text = gr.Button("Classificar")
        btn_text.click(fn=interface_text, inputs=email_input, outputs=output_text)

    with gr.Tab("Classificar Arquivo"):
        file_input = gr.File(label="Envie um arquivo", file_types=[".pdf", ".txt", ".eml"])
        output_file = gr.JSON(label="Resultado")
        btn_file = gr.Button("Classificar")
        btn_file.click(fn=interface_file, inputs=file_input, outputs=output_file)

if __name__ == "__main__":
    demo.launch()
