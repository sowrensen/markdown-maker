import gradio as gr
from markitdown import MarkItDown
from pathlib import Path
import tempfile

store = {}


def upload(filepath):
    filename = Path(filepath).name
    store["original_filename"] = Path(filepath).stem
    return [gr.UploadButton(visible=False),
            gr.ClearButton(visible=True),
            gr.Markdown(f"**{filename}**"),
            gr.Button("Convert", visible=True)]


def toggle():
    return [gr.UploadButton(visible=True),
            gr.ClearButton(visible=False),
            gr.Button(visible=False),
            gr.DownloadButton(visible=False)]


def convert(file):
    markitdown = MarkItDown()
    result = markitdown.convert(file.name)
    content = result.text_content
    return [gr.Markdown(content),
            gr.DownloadButton(value=store_markdown(content), visible=True)]


def store_markdown(content):
    output_path = Path(tempfile.gettempdir()) / (store.get("original_filename") + ".md")
    with open(output_path, "w") as f:
        f.write(content)

    return output_path


with gr.Blocks(title="Markdown Maker",
               theme=gr.themes.Soft(font=gr.themes.GoogleFont("Inter"))) as interface:
    gr.Markdown("✅ Upload a file and click **Convert** to see the markdown text."
    )
    md_preview = gr.Markdown(label="Preview",
                             show_copy_button=True,
                             min_height=500,
                             max_height=500,
                             container=True,
                             line_breaks=True)
    fn_preview = gr.Markdown("")
    with gr.Row():
        upload_btn = gr.UploadButton(label="Select a file", file_types=[".docx", ".xlsx", ".pdf"])
        clear_btn = gr.ClearButton(visible=False)
        convert_btn = gr.Button("Convert", visible=False)
        download_btn = gr.DownloadButton("Download", visible=False)

    upload_btn.upload(fn=upload, inputs=upload_btn, outputs=[upload_btn, clear_btn, fn_preview, convert_btn])
    clear_btn.add([upload_btn, convert_btn, download_btn, md_preview, fn_preview])
    clear_btn.click(fn=toggle, outputs=[upload_btn, clear_btn, convert_btn, download_btn])
    convert_btn.click(fn=convert, inputs=upload_btn, outputs=[md_preview, download_btn])

interface.launch()
