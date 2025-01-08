from openai import OpenAI
import os
from dotenv import load_dotenv

# Load the API key from the .env file
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def generate_cover_letter(inputs):
    """
    Generate a professional cover letter using OpenAI's GPT API with streaming.

    Args:
        inputs (dict): A dictionary containing:
            - 'name': Applicant's name.
            - 'contact_info': Applicant's contact information.
            - 'company': Name of the company.
            - 'job_description': Description of the job.
            - 'company_info': Information about the company.
            - 'projects': Applicant's projects and skills.

    Returns:
        str: The generated cover letter.
    """
    # Construct the prompt
    prompt = (
        f"Write a professional cover letter for {inputs['name']} applying to the position described as:\n"
        f"'{inputs['job_description']}'\nat {inputs['company']}. Include the following company details:\n{inputs['company_info']}.\n"
        f"Highlight the applicant's projects and skills:\n{inputs['projects']}.\n"
        f"Format the letter professionally and include the contact information: {inputs['contact_info']}."
    )

    try:
        # Call OpenAI's ChatCompletion API with streaming
        stream = client.chat.completions.create(
            model="gpt-4o-mini",  # Update to the correct model name
            messages=[
                {"role": "system",
                 "content": "You are a professional AI assistant specializing in generating cover letters."},
                {"role": "user", "content": prompt}
            ],
            stream=True,  # Enable streaming
        )

        # Collect and return the response in chunks
        cover_letter = ""
        for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                cover_letter += chunk.choices[0].delta.content

        return cover_letter.strip()
    except Exception as e:
        # Handle errors and raise meaningful messages
        raise RuntimeError(f"Failed to generate cover letter: {e}")
