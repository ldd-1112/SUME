import gradio as gr
from backend import summarize_text, extend_summary, extend_summary_custom, translate_text, get_text_from_url, clear_cache, get_cache_stats, summarize_file
with gr.Blocks(theme=gr.themes.Soft()) as demo:
    gr.HTML("""
    <style>
        .title-text {
            font-size: 36px;
            font-weight: bold;
            color: #2c3e50;
            text-align: center;
        }
    </style>
    """)
    gr.Markdown("<div class='title-text'>SUME - Smart Summarizer</div>")
    
    # Performance controls
    with gr.Row():
        clear_cache_btn = gr.Button("Clear Cache", size="sm")
        cache_stats_btn = gr.Button("Cache Stats", size="sm")
        cache_info = gr.Textbox(label="Cache Information", interactive=False, lines=1)
    
    clear_cache_btn.click(fn=clear_cache, outputs=cache_info)
    cache_stats_btn.click(fn=get_cache_stats, outputs=cache_info)

    with gr.Tabs():
        # === TEXT TAB ===
        with gr.Tab("Text"):
            with gr.Tabs():
                # Text Input Sub-tab
                with gr.Tab("Direct Text"):
                    text_input = gr.Textbox(label="Enter text to summarize", lines=8, placeholder="Paste your text here...")
                    summarize_btn_text = gr.Button("Summarize", variant="primary")
                    summary_output_text = gr.Textbox(label="Summary", lines=10)
                    
                    with gr.Row():
                        extend_btn_text = gr.Button("Quick Extend", variant="secondary")
                        custom_extend_btn_text = gr.Button("Custom Extend", variant="secondary")
                    
                    # Custom extend section (collapsible)
                    with gr.Group(visible=False) as custom_extend_group_text:
                        gr.Markdown("### Custom Extend Summary")
                        custom_prompt_text = gr.Textbox(
                            label="What specific details should I focus on?",
                            placeholder="e.g., technical details, examples, statistics, background information, implications...",
                            lines=3
                        )
                        custom_extend_confirm_text = gr.Button("Extend with Details", variant="primary")
                    
                    extended_output_text = gr.Textbox(label="Extended Summary", lines=10)
                    translate_lang_text = gr.Dropdown(["English","Vietnamese","French","Spanish"], label="Translate to")
                    translate_btn_text = gr.Button("Translate")
                    translated_output_text = gr.Textbox(label="Translation", lines=10)

                    def custom_extend_text(summary, custom_prompt):
                        if not custom_prompt.strip():
                            return "⚠️ Please enter specific details to focus on."
                        return extend_summary_custom(summary, custom_prompt)

                    def toggle_custom_extend_text():
                        return gr.Group(visible=True)
                    
                    def hide_custom_extend_text():
                        return gr.Group(visible=False)

                    summarize_btn_text.click(fn=summarize_text, inputs=text_input, outputs=summary_output_text)
                    extend_btn_text.click(fn=extend_summary, inputs=summary_output_text, outputs=extended_output_text)
                    custom_extend_btn_text.click(fn=toggle_custom_extend_text, outputs=custom_extend_group_text)
                    custom_extend_confirm_text.click(
                        fn=custom_extend_text, 
                        inputs=[summary_output_text, custom_prompt_text], 
                        outputs=extended_output_text
                    ).then(fn=hide_custom_extend_text, outputs=custom_extend_group_text)
                    translate_btn_text.click(fn=translate_text, inputs=[summary_output_text, translate_lang_text], outputs=translated_output_text)

                # File Input Sub-tab
                with gr.Tab("Text File"):
                    text_file_input = gr.File(label="Upload text file (.txt, .md, .docx, .pdf)", file_types=[".txt", ".md", ".docx", ".pdf"])
                    summarize_btn_text_file = gr.Button("Summarize", variant="primary")
                    summary_output_text_file = gr.Textbox(label="Summary", lines=10)
                    
                    with gr.Row():
                        extend_btn_text_file = gr.Button("Quick Extend", variant="secondary")
                        custom_extend_btn_text_file = gr.Button("Custom Extend", variant="secondary")
                    
                    # Custom extend section (collapsible)
                    with gr.Group(visible=False) as custom_extend_group_text_file:
                        gr.Markdown("### Custom Extend Summary")
                        custom_prompt_text_file = gr.Textbox(
                            label="What specific details should I focus on?",
                            placeholder="e.g., technical details, examples, statistics, background information, implications...",
                            lines=3
                        )
                        custom_extend_confirm_text_file = gr.Button("Extend with Details", variant="primary")
                    
                    extended_output_text_file = gr.Textbox(label="Extended Summary", lines=10)
                    translate_lang_text_file = gr.Dropdown(["English","Vietnamese","French","Spanish"], label="Translate to")
                    translate_btn_text_file = gr.Button("Translate")
                    translated_output_text_file = gr.Textbox(label="Translation", lines=10)

                    def summarize_text_file(file):
                        if file is None:
                            return "⚠️ No file uploaded."
                        
                        try:
                            # Use the specialized summarize_file function
                            return summarize_file(file.name)
                        except Exception as e:
                            return f"⚠️ Error processing file: {e}"

                    def custom_extend_text_file(summary, custom_prompt):
                        if not custom_prompt.strip():
                            return "⚠️ Please enter specific details to focus on."
                        return extend_summary_custom(summary, custom_prompt)

                    def toggle_custom_extend_text_file():
                        return gr.Group(visible=True)
                    
                    def hide_custom_extend_text_file():
                        return gr.Group(visible=False)

                    summarize_btn_text_file.click(fn=summarize_text_file, inputs=text_file_input, outputs=summary_output_text_file)
                    extend_btn_text_file.click(fn=extend_summary, inputs=summary_output_text_file, outputs=extended_output_text_file)
                    custom_extend_btn_text_file.click(fn=toggle_custom_extend_text_file, outputs=custom_extend_group_text_file)
                    custom_extend_confirm_text_file.click(
                        fn=custom_extend_text_file, 
                        inputs=[summary_output_text_file, custom_prompt_text_file], 
                        outputs=extended_output_text_file
                    ).then(fn=hide_custom_extend_text_file, outputs=custom_extend_group_text_file)
                    translate_btn_text_file.click(fn=translate_text, inputs=[summary_output_text_file, translate_lang_text_file], outputs=translated_output_text_file)

                # URL Input Sub-tab
                with gr.Tab("Webpage URL"):
                    url_input = gr.Textbox(label="Enter webpage URL", placeholder="https://example.com/article")
                    summarize_btn_url = gr.Button("Summarize", variant="primary")
                    summary_output_url = gr.Textbox(label="Summary", lines=10)
                    
                    with gr.Row():
                        extend_btn_url = gr.Button("Quick Extend", variant="secondary")
                        custom_extend_btn_url = gr.Button("Custom Extend", variant="secondary")
                    
                    # Custom extend section (collapsible)
                    with gr.Group(visible=False) as custom_extend_group_url:
                        gr.Markdown("### 🎯 Custom Extend Summary")
                        custom_prompt_url = gr.Textbox(
                            label="What specific details should I focus on?",
                            placeholder="e.g., technical details, examples, statistics, background information, implications...",
                            lines=3
                        )
                        custom_extend_confirm_url = gr.Button("Extend with Details", variant="primary")
                    
                    extended_output_url = gr.Textbox(label="Extended Summary", lines=10)
                    translate_lang_url = gr.Dropdown(["English","Vietnamese","French","Spanish"], label="Translate to")
                    translate_btn_url = gr.Button("Translate")
                    translated_output_url = gr.Textbox(label="Translation", lines=10)

                    def summarize_url(url):
                        if not url:
                            return "⚠️ Please enter a URL."
                        text = get_text_from_url(url, "Webpage")
                        if text.startswith("⚠️"):
                            return text
                        return summarize_text(text)

                    def custom_extend_url(summary, custom_prompt):
                        if not custom_prompt.strip():
                            return "⚠️ Please enter specific details to focus on."
                        return extend_summary_custom(summary, custom_prompt)

                    def toggle_custom_extend_url():
                        return gr.Group(visible=True)
                    
                    def hide_custom_extend_url():
                        return gr.Group(visible=False)

                    summarize_btn_url.click(fn=summarize_url, inputs=url_input, outputs=summary_output_url)
                    extend_btn_url.click(fn=extend_summary, inputs=summary_output_url, outputs=extended_output_url)
                    custom_extend_btn_url.click(fn=toggle_custom_extend_url, outputs=custom_extend_group_url)
                    custom_extend_confirm_url.click(
                        fn=custom_extend_url, 
                        inputs=[summary_output_url, custom_prompt_url], 
                        outputs=extended_output_url
                    ).then(fn=hide_custom_extend_url, outputs=custom_extend_group_url)
                    translate_btn_url.click(fn=translate_text, inputs=[summary_output_url, translate_lang_url], outputs=translated_output_url)

        # === MEDIA TAB ===
        with gr.Tab("Media"):
            with gr.Tabs():
                # Video/Audio URL Sub-tab
                with gr.Tab("Media URL"):
                    media_url_input = gr.Textbox(label="Enter media URL (YouTube, etc.)", placeholder="https://youtube.com/watch?v=...")
                    summarize_btn_media_url = gr.Button("Summarize", variant="primary")
                    summary_output_media_url = gr.Textbox(label="Summary", lines=10)
                    
                    with gr.Row():
                        extend_btn_media_url = gr.Button("Quick Extend", variant="secondary")
                        custom_extend_btn_media_url = gr.Button("Custom Extend", variant="secondary")
                    
                    # Custom extend section (collapsible)
                    with gr.Group(visible=False) as custom_extend_group_media_url:
                        gr.Markdown("### Custom Extend Summary")
                        custom_prompt_media_url = gr.Textbox(
                            label="What specific details should I focus on?",
                            placeholder="e.g., technical details, examples, statistics, background information, implications...",
                            lines=3
                        )
                        custom_extend_confirm_media_url = gr.Button("Extend with Details", variant="primary")
                    
                    extended_output_media_url = gr.Textbox(label="Extended Summary", lines=10)
                    translate_lang_media_url = gr.Dropdown(["English","Vietnamese","French","Spanish"], label="Translate to")
                    translate_btn_media_url = gr.Button("Translate")
                    translated_output_media_url = gr.Textbox(label="Translation", lines=10)

                    def summarize_media_url(url):
                        if not url:
                            return "⚠️ Please enter a media URL."
                        text = get_text_from_url(url, "Media")
                        if text.startswith("⚠️"):
                            return text
                        return summarize_text(text)

                    def custom_extend_media_url(summary, custom_prompt):
                        if not custom_prompt.strip():
                            return "⚠️ Please enter specific details to focus on."
                        return extend_summary_custom(summary, custom_prompt)

                    def toggle_custom_extend_media_url():
                        return gr.Group(visible=True)
                    
                    def hide_custom_extend_media_url():
                        return gr.Group(visible=False)

                    summarize_btn_media_url.click(fn=summarize_media_url, inputs=media_url_input, outputs=summary_output_media_url)
                    extend_btn_media_url.click(fn=extend_summary, inputs=summary_output_media_url, outputs=extended_output_media_url)
                    custom_extend_btn_media_url.click(fn=toggle_custom_extend_media_url, outputs=custom_extend_group_media_url)
                    custom_extend_confirm_media_url.click(
                        fn=custom_extend_media_url, 
                        inputs=[summary_output_media_url, custom_prompt_media_url], 
                        outputs=extended_output_media_url
                    ).then(fn=hide_custom_extend_media_url, outputs=custom_extend_group_media_url)
                    translate_btn_media_url.click(fn=translate_text, inputs=[summary_output_media_url, translate_lang_media_url], outputs=translated_output_media_url)

                # File Upload Sub-tab
                with gr.Tab("File Upload"):
                    media_input = gr.File(label="Upload Media File (Audio/Video)", file_types=["audio", "video"])
                    summarize_btn_media = gr.Button("Summarize", variant="primary")
                    summary_output_media = gr.Textbox(label="Summary", lines=10)
                    
                    with gr.Row():
                        extend_btn_media = gr.Button("Quick Extend", variant="secondary")
                        custom_extend_btn_media = gr.Button("Custom Extend", variant="secondary")
                    
                    # Custom extend section (collapsible)
                    with gr.Group(visible=False) as custom_extend_group_media:
                        gr.Markdown("### Custom Extend Summary")
                        custom_prompt_media = gr.Textbox(
                            label="What specific details should I focus on?",
                            placeholder="e.g., technical details, examples, statistics, background information, implications...",
                            lines=3
                        )
                        custom_extend_confirm_media = gr.Button("Extend with Details", variant="primary")
                    
                    extended_output_media = gr.Textbox(label="Extended Summary", lines=10)
                    translate_lang_media = gr.Dropdown(["English","Vietnamese","French","Spanish"], label="Translate to")
                    translate_btn_media = gr.Button("Translate")
                    translated_output_media = gr.Textbox(label="Translation", lines=10)

                    def summarize_uploaded_media(file):
                        if file is None:
                            return "⚠️ No file uploaded."
                        
                        from backend import speech_to_text
                        transcript = speech_to_text(file.name)
                        return summarize_text(transcript)

                    def custom_extend_media(summary, custom_prompt):
                        if not custom_prompt.strip():
                            return "⚠️ Please enter specific details to focus on."
                        return extend_summary_custom(summary, custom_prompt)

                    def toggle_custom_extend_media():
                        return gr.Group(visible=True)
                    
                    def hide_custom_extend_media():
                        return gr.Group(visible=False)

                    summarize_btn_media.click(fn=summarize_uploaded_media, inputs=media_input, outputs=summary_output_media)
                    extend_btn_media.click(fn=extend_summary, inputs=summary_output_media, outputs=extended_output_media)
                    custom_extend_btn_media.click(fn=toggle_custom_extend_media, outputs=custom_extend_group_media)
                    custom_extend_confirm_media.click(
                        fn=custom_extend_media, 
                        inputs=[summary_output_media, custom_prompt_media], 
                        outputs=extended_output_media
                    ).then(fn=hide_custom_extend_media, outputs=custom_extend_group_media)
                    translate_btn_media.click(fn=translate_text, inputs=[summary_output_media, translate_lang_media], outputs=translated_output_media)

def main():
    """Main entry point for SUME application"""
    demo.launch()

if __name__ == "__main__":
    main()