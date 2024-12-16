import gradio as gr
from markitdown import MarkItDown


def convert(file):
    markitdown = MarkItDown()
    result = markitdown.convert(file.name)
    return result.text_content


with gr.Blocks(title="Markdown Maker",
               theme=gr.themes.Soft(font=gr.themes.GoogleFont("Inter"))) as interface:
    gr.Markdown("Upload a file and click **Convert** to see the markdown text.")
    file_input = gr.File(label="Select a file", file_types=[".docx", ".xlsx", ".pdf"])
    markdown_output = gr.Markdown(label="Preview",
                                  show_copy_button=True,
                                  min_height=300,
                                  max_height=500,
                                  container=True,
                                  line_breaks=True)
    btn = gr.Button("Convert")
    btn.click(fn=convert, inputs=file_input, outputs=markdown_output)

    file_input.clear(fn=lambda file: "", inputs=file_input, outputs=markdown_output)

interface.launch()
