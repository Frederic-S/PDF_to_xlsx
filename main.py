import tkinter as tk
from tkinter import filedialog, messagebox
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
# Make sure to replace 'YOUR_OPENAI_API_KEY' with your actual OpenAI API key.
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

class PDFUploader(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("PDF Uploader")
        self.geometry("400x300")

        # Label and entry for fine-tuning information
        self.label_info = tk.Label(self, text="Fine-tuning Information:")
        self.label_info.pack(pady=10)

        self.entry_info = tk.Entry(self, width=50)
        self.entry_info.pack(pady=5)

        # Button to select PDF
        self.btn_select_pdf = tk.Button(self, text="Select PDF", command=self.select_pdf)
        self.btn_select_pdf.pack(pady=10)

        # Label to show selected PDF file
        self.label_pdf = tk.Label(self, text="")
        self.label_pdf.pack(pady=5)

        # Button to send to API
        self.btn_send = tk.Button(self, text="Send to API", command=self.send_to_api)
        self.btn_send.pack(pady=10)

        self.assistant = client.beta.assistants.create(
            name="PDF data extraktor.",instructions="You scan the given PDFs. Extract the Mathematical exercises and save them in LaTeX formation in a .xlsx file."            tools=[{"type": "file_search"}],)
        self.store = client.beta.vector_stores.create(name="PDF Scan")

        self.pdf_path = None

    def select_pdf(self):
        self.pdf_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.txt")])
        if self.pdf_path:
            self.label_pdf.config(text=f"Selected: {self.pdf_path}")

    def send_to_api(self):
        if not self.pdf_path:
            messagebox.showerror("Error", "No PDF file selected")
            return

        fine_tuning_info = self.entry_info.get()
        if not fine_tuning_info:
            messagebox.showerror("Error", "No fine-tuning information provided")
            return

        try:
            with open(self.pdf_path, "rb") as pdf_file:
                file_batch = client.beta.vector_stores.file_batches.upload_and_poll(
                self.store.id,
                files=pdf_file,
                )
                print(file_batch.status)


        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

        self.assistant = client.beta.assistants.update(
            assistant_id=self.assistant.id,
            tool_resources={"file_search": {"vector_store_ids": [self.store.id]}},
        )

if __name__ == "__main__":
    app = PDFUploader()
    app.mainloop()
