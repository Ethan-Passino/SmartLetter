from transformers import AutoModelForCausalLM, AutoTokenizer

# Load GPT-2 model and tokenizer
model_name = "gpt2"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)


def generate_cover_letter(inputs):
    """
    Generate a professional cover letter using the Hugging Face Transformers library.

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
    # Construct the input prompt
    prompt = (
        f"Write a professional cover letter for {inputs['name']} applying to the position described as:\n"
        f"'{inputs['job_description']}'\nat {inputs['company']}. Include the following company details:\n{inputs['company_info']}.\n"
        f"Highlight the applicant's projects and skills:\n{inputs['projects']}.\n"
        f"Format the letter professionally and include the contact information: {inputs['contact_info']}."
    )

    try:
        # Tokenize the input prompt without padding
        inputs_encoded = tokenizer(
            prompt,
            return_tensors="pt",
            truncation=True,
            max_length=512
        )

        # Generate text using GPT-2
        outputs = model.generate(
            inputs_encoded["input_ids"],
            attention_mask=inputs_encoded["attention_mask"],
            max_length=512,
            num_beams=5,
            temperature=0.7,
            do_sample=True,
            pad_token_id=tokenizer.eos_token_id  # Use eos_token_id for open-ended generation
        )

        # Decode the generated text
        generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
        return generated_text
    except Exception as e:
        # Raise an error if generation fails
        raise RuntimeError(f"Error generating cover letter: {e}")
