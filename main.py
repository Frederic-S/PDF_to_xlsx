import tkinter as tk
from tkinter import filedialog, messagebox
import openai
import os

# Make sure to replace 'YOUR_OPENAI_API_KEY' with your actual OpenAI API key.
openai.api_key = 'YOUR_OPENAI_API_KEY'

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

        self.pdf_path = None

    def select_pdf(self):
        self.pdf_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
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
                response = openai.File.create(
                    file=pdf_file,
                    purpose='fine-tune'
                )

                if 'id' in response:
                    fine_tune_response = openai.FineTune.create(
                        training_file=response['id'],
                        model='gpt-3.5-turbo',
                        n_epochs=1,
                        prompt=fine_tuning_info
                    )

                    if 'id' in fine_tune_response:
                        messagebox.showinfo("Success", "File uploaded and fine-tuning started successfully")
                    else:
                        messagebox.showerror("Error", "Failed to start fine-tuning")
                else:
                    messagebox.showerror("Error", "Failed to upload file")

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

if __name__ == "__main__":
    app = PDFUploader()
    app.mainloop()
