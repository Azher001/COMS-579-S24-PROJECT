import gradio as gr
from main import upload_file
from retrive import retriveQuery

with gr.Blocks() as demo:
    pdf_file_path = gr.File(label="Upload PDF file", file_types=["pdf"], type="filepath", file_count='single')
    upload_status = gr.Textbox(label="Status", type="text")
    upload_button = gr.Button("Submit")
    upload_button.click(
            fn = upload_file,
            inputs = pdf_file_path,
            outputs = upload_status
    )


    query = gr.Textbox(label="Your Query", type="text", placeholder="Enter Your Query")
    open_AI_API_Key = gr.Textbox(label="Your Open AI API Key", type="text", placeholder="Enter Your OPEN AI API Key")
    query_button = gr.Button("Query")
    query_result = gr.Textbox(label="Generated Answer", type="text")
    query_button.click(
            fn = retriveQuery,
            inputs = [query,open_AI_API_Key],
            outputs = query_result
    )

demo.launch()