from tkinter import *
from tkinter.filedialog import askopenfilename, asksaveasfilename
from tkinter import ttk, messagebox
import threading
from ai_generator import generate_cover_letter
import PyPDF2

# Global variable to store the uploaded resume text
resume_text = ""


def apply_dark_theme(widget):
    """
    Apply a dark theme to the given widget, ensuring that only things that have these properties are set.
    """
    if isinstance(widget, (Text)):
        widget.configure(
            bg="#2E2E2E",  # dark background color
            fg="#FFFFFF",  # White
            insertbackground="#FFFFFF",
            highlightbackground="#444444",
            highlightcolor="#000000"
        )
    elif isinstance(widget, Entry):
        widget.configure(
            bg="#2E2E2E",
            fg="#FFFFFF"
        )
    elif isinstance(widget, Tk):
        widget.configure(
            bg="#2E2E2E"
        )


def style_ttk():
    style = ttk.Style()
    style.theme_use("clam")
    style.configure(
        "TButton",
        background="#444444",
        foreground="#FFFFFF",
        borderwidth=1,
        focuscolor="none",
        padding=5
    )
    style.map(
        "TButton",
        background=[("active", "#666666")],
        foreground=[("active", "#FFFFFF")],
    )

    style.configure(
        "TLabel",
        background="#2E2E2E",
        foreground="#FFFFFF",
        padding=5
    )

    style.configure(
        "TFrame",
        background="#2E2E2E"
    )

    style.configure(
        "TOptionMenu",
        background="#444444",
        foreground="#FFFFFF",
        highlightbackground="#444444"
    )


# Apply dark theme to app
style_ttk()


def show_output(cover_letter):
    """
    Display the generated cover letter in a new window with options to save and analyze.
    """
    output_window = Toplevel(root)
    output_window.title("Generated Cover Letter")
    apply_dark_theme(output_window)

    # Display the cover letter in a text widget
    output_text = Text(output_window, wrap="word")
    apply_dark_theme(output_text)
    output_text.insert("1.0", cover_letter)
    output_text.config(state="disabled")  # Make the text read-only
    output_text.pack(expand=True, fill="both")

    # Character and word count
    char_count = len(cover_letter)
    word_count = len(cover_letter.split())
    stats_label = Label(output_window, text=f"Characters: {char_count} | Words: {word_count}")
    apply_dark_theme(stats_label)
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

    save_button = Button(output_window, text="Save", command=save_to_file, bg="#2E2E2E", fg="#FFFFFF")
    save_button.pack(side="bottom")

    # Add a "Go Back" button
    back_button = Button(output_window, text="Go Back", command=output_window.destroy, bg="#2E2E2E", fg="#FFFFFF" )
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
    Generate the cover letter and update the GUI in real time.
    """

    def update_text(chunk):
        # Append each chunk to the output widget
        output_text.insert("end", chunk)
        output_text.see("end")  # Scroll to the end

    try:
        # Create a new window to show the output in real-time
        output_window = Toplevel(root)
        output_window.title("Generating Cover Letter...")
        apply_dark_theme(output_window)

        # Create a text widget for the output
        global output_text
        output_text = Text(output_window, wrap="word")
        apply_dark_theme(output_text)
        output_text.pack(expand=True, fill="both")

        # Add a "Go Back" button
        back_button = Button(output_window, text="Go Back", command=output_window.destroy)
        back_button.pack()

        # Call the generator function
        generate_cover_letter(inputs, update_text)

    except Exception as e:
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
apply_dark_theme(root)

# Input fields
Label(root, text="Your Name:", bg="#2E2E2E", fg="#FFFFFF").pack()
name_entry = Entry(root, width=50)
apply_dark_theme(name_entry)
name_entry.pack()

Label(root, text="Contact Info (Address, Phone, Email):", bg="#2E2E2E", fg="#FFFFFF").pack()
contact_entry = Entry(root, width=50)
apply_dark_theme(contact_entry)
contact_entry.pack()

Label(root, text="Company Name:", bg="#2E2E2E", fg="#FFFFFF").pack()
company_entry = Entry(root, width=50)
apply_dark_theme(company_entry)
company_entry.pack()

Label(root, text="Job Description:", bg="#2E2E2E", fg="#FFFFFF").pack()
job_text = Text(root, height=5, width=50)
apply_dark_theme(job_text)
job_text.pack()

Label(root, text="Company Information:", bg="#2E2E2E", fg="#FFFFFF").pack()
company_info_text = Text(root, height=5, width=50)
apply_dark_theme(company_info_text)
company_info_text.pack()

Label(root, text="Projects and Skills:", bg="#2E2E2E", fg="#FFFFFF").pack()
projects_text = Text(root, height=5, width=50)
apply_dark_theme(projects_text)
projects_text.pack()

# Tone selection
Label(root, text="Select Tone:", bg="#2E2E2E", fg="#FFFFFF").pack()
tone_var = StringVar(value="Formal")
tone_dropdown = ttk.OptionMenu(root, tone_var, "Formal", "Casual", "Creative", "Formal")
tone_dropdown.pack()

# Upload Resume Button
upload_button = Button(root, text="Upload Resume", command=upload_resume , bg="#2E2E2E", fg="#FFFFFF")
upload_button.pack()

# Loading label (hidden initially)
loading_label = Label(root, text="", fg="blue")
apply_dark_theme(loading_label)
# Generate button
generate_button = Button(root, text="Generate Cover Letter", command=handle_generate, bg="#2E2E2E", fg="#FFFFFF")
generate_button.pack()

# Run the application
root.mainloop()
