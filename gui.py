from tkinter import Tk, Label, Entry, Text, Button, messagebox, Toplevel, filedialog, StringVar, OptionMenu
from tkinter.filedialog import askopenfilename, asksaveasfilename
import threading
from ai_generator import generate_cover_letter
import PyPDF2

# Global variable to store the uploaded resume text
resume_text = ""

def show_output(cover_letter):
    """
    Display the generated cover letter in a new window with options to save and analyze.
    """
    output_window = Toplevel(root)
    output_window.title("Generated Cover Letter")

    # Display the cover letter in a text widget
    output_text = Text(output_window, wrap="word")
    output_text.insert("1.0", cover_letter)
    output_text.config(state="disabled")  # Make the text read-only
    output_text.pack(expand=True, fill="both")

    # Character and word count
    char_count = len(cover_letter)
    word_count = len(cover_letter.split())
    stats_label = Label(output_window, text=f"Characters: {char_count} | Words: {word_count}")
    stats_label.pack()

    # Add a "Save" button
    def save_to_file():
        file_path = asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
        )
        if file_path:
            with open(file_path, "w") as file:
                file.write(cover_letter)
            messagebox.showinfo("Success", "Cover letter saved successfully!")

    save_button = Button(output_window, text="Save Cover Letter", command=save_to_file)
    save_button.pack()

    # Add a "Go Back" button
    back_button = Button(output_window, text="Go Back", command=output_window.destroy)
    back_button.pack()


def handle_generate():
    """
    Handle the generation process by validating inputs, showing a loading indicator,
    and starting the API call in a separate thread.
    """
    global resume_text  # Access the global resume text

    inputs = {
        "name": name_entry.get(),
        "contact_info": contact_entry.get(),
        "company": company_entry.get(),
        "job_description": job_text.get("1.0", "end-1c").strip(),
        "company_info": company_info_text.get("1.0", "end-1c").strip(),
        "projects": projects_text.get("1.0", "end-1c").strip(),
        "resume": resume_text.strip(),  # Include the uploaded resume text as its own input
        "tone": tone_var.get(),
    }

    # Validate inputs
    if not all(inputs.values()):
        messagebox.showerror("Error", "Please fill out all fields!")
        return

    # Show the loading label
    loading_label.config(text="Generating cover letter, please wait...")
    loading_label.pack()

    # Start the API call in a new thread to prevent freezing the GUI
    threading.Thread(target=generate_and_show, args=(inputs,)).start()


def generate_and_show(inputs):
    """
    Generate the cover letter and update the GUI once complete.
    """
    try:
        # Generate the cover letter
        cover_letter = generate_cover_letter(inputs)

        # Hide the loading label and show the output
        loading_label.pack_forget()
        show_output(cover_letter)
    except Exception as e:
        # Hide the loading label and show an error message
        loading_label.pack_forget()
        messagebox.showerror("Error", f"Failed to generate cover letter: {e}")


def upload_resume():
    """
    Allow the user to upload a resume and extract text to save as a separate input.
    """
    global resume_text  # Access the global resume text variable

    file_path = askopenfilename(filetypes=[("PDF Files", "*.pdf"), ("Text Files", "*.txt"), ("All Files", "*.*")])
    if file_path:
        if file_path.endswith(".pdf"):
            try:
                with open(file_path, "rb") as pdf_file:
                    pdf_reader = PyPDF2.PdfReader(pdf_file)
                    resume_text = " ".join(page.extract_text() for page in pdf_reader.pages)
                    messagebox.showinfo("Success", "Resume uploaded successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to extract text from PDF: {e}")
        elif file_path.endswith(".txt"):
            try:
                with open(file_path, "r") as txt_file:
                    resume_text = txt_file.read()
                    messagebox.showinfo("Success", "Resume uploaded successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to extract text from file: {e}")
        else:
            messagebox.showerror("Error", "Unsupported file type!")


# Create the main GUI window
root = Tk()
root.title("SmartLetter - AI Cover Letter Generator")

# Input fields
Label(root, text="Your Name:").pack()
name_entry = Entry(root, width=50)
name_entry.pack()

Label(root, text="Contact Info (Address, Phone, Email):").pack()
contact_entry = Entry(root, width=50)
contact_entry.pack()

Label(root, text="Company Name:").pack()
company_entry = Entry(root, width=50)
company_entry.pack()

Label(root, text="Job Description:").pack()
job_text = Text(root, height=5, width=50)
job_text.pack()

Label(root, text="Company Information:").pack()
company_info_text = Text(root, height=5, width=50)
company_info_text.pack()

Label(root, text="Projects and Skills:").pack()
projects_text = Text(root, height=5, width=50)
projects_text.pack()

# Tone selection
Label(root, text="Select Tone:").pack()
tone_var = StringVar(value="Formal")
tone_dropdown = OptionMenu(root, tone_var, "Formal", "Casual", "Creative")
tone_dropdown.pack()

# Upload Resume Button
upload_button = Button(root, text="Upload Resume", command=upload_resume)
upload_button.pack()

# Loading label (hidden initially)
loading_label = Label(root, text="", fg="blue")

# Generate button
generate_button = Button(root, text="Generate Cover Letter", command=handle_generate)
generate_button.pack()

# Run the application
root.mainloop()
