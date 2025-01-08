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
    # Merge "projects" and "resume" details for a comprehensive skillset
    combined_projects_and_skills = f"{inputs['projects']}\n\nAdditional details from resume:\n{inputs['resume']}"

    # Construct the prompt
    prompt = (
        f"Write a {inputs['tone'].lower()} professional cover letter for {inputs['name']} applying to the position described as:\n"
        f"'{inputs['job_description']}'\nat {inputs['company']}. Include the following company details:\n{inputs['company_info']}.\n"
        f"Highlight the applicant's projects, skills, and relevant experience:\n{combined_projects_and_skills}.\n"
        f"Format the letter professionally and include the contact information: {inputs['contact_info']}."
    )

    try:
        # Call OpenAI's ChatCompletion API with streaming
        stream = client.chat.completions.create(
            model="gpt-3.5-turbo",  # Update to the correct model name
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
