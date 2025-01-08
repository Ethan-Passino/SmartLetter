from tkinter import Tk, Label, Entry, Text, Button, messagebox, Toplevel
from ai_generator import generate_cover_letter

def show_output(cover_letter):
    """
    Display the generated cover letter in a new window.
    """
    output_window = Toplevel(root)
    output_window.title("Generated Cover Letter")

    # Display the cover letter in a text widget
    output_text = Text(output_window, wrap="word")
    output_text.insert("1.0", cover_letter)
    output_text.config(state="disabled")  # Make the text read-only
    output_text.pack(expand=True, fill="both")

    # Add a "Go Back" button
    back_button = Button(output_window, text="Go Back", command=output_window.destroy)
    back_button.pack()

def handle_generate():
    """
    Generate the cover letter based on the inputs and display it.
    """
    inputs = {
        "name": name_entry.get(),
        "contact_info": contact_entry.get(),
        "company": company_entry.get(),
        "job_description": job_text.get("1.0", "end-1c").strip(),
        "company_info": company_info_text.get("1.0", "end-1c").strip(),
        "projects": projects_text.get("1.0", "end-1c").strip(),
    }

    # Validate inputs
    if not all(inputs.values()):
        messagebox.showerror("Error", "Please fill out all fields!")
        return

    try:
        # Generate the cover letter
        cover_letter = generate_cover_letter(inputs)
        show_output(cover_letter)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to generate cover letter: {e}")

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

# Generate button
generate_button = Button(root, text="Generate Cover Letter", command=handle_generate)
generate_button.pack()

# Run the application
root.mainloop()
