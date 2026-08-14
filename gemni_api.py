import os
import json
from typing import List
from llms.schema.json_structure import Output
from google import genai
from pydantic import BaseModel, Field, ValidationError
from dotenv import load_dotenv
from llms.schema.json_validation import validate_json


# ============================================================
# Gemini API Call
# ============================================================

def gemini_api_call(api: str,user_message: str, output_token_limit: int = 2000) -> str | None:

    client = genai.Client(api_key= api)

    try:
        interaction = client.interactions.create(
            model="gemini-3.6-flash",
            input=f"""
You are an educational mind-map generator.

Analyze the following book content and extract its most important
ideas into a clear hierarchical mind map.

CONTENT:
{user_message}

RULES:
- Return ONLY the requested structured output. No explanations.
- Organize information into logical sections and topics.
- Every section title, topic title, and point must contain a maximum of 3 words.
- Use keywords or short phrases only; never write sentences.
- Keep language simple and easy for students to understand.
- Include only important concepts; remove unnecessary details.
- Preserve the key meaning of the original content.
- Avoid duplicate or overlapping points.
- Create a logical hierarchy from broad concepts to specific ideas.
""",
            generation_config={
                "max_output_tokens": output_token_limit
            },
            response_format={
                "type": "text",
                "mime_type": "application/json",
                "schema": Output.model_json_schema(),
            },
        )

        return interaction.output_text

    except Exception as e:
        print("Gemini Api Failed.")
        return None



# ============================================================
# Main
# ============================================================

if __name__ == "__main__":

    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")

    content = """
Communication

Communication is derived from the Latin word ‘Communico’ which means
“to share”. Hence the word “communication” means: the process of sharing.
One may ask, sharing what? Obviously – sharing information, which could
be facts, ideas, thoughts, feelings, needs, etc.

This sharing takes place from one person to another so that it is understood.
This process involves systematic and continuous process of speaking,
listening, and understanding.

Therefore, Communication is a process, which involves sharing of
information between people through a continuous activity of speaking,
listening, and understanding.
"""
    output_token_limit = 2000
    output_json = r"D:\000-University\Uni_Code_Prac\Rooman_Code\mind map\gemini_mind_map.json"

    # 1. Call Gemini
    raw_response = gemini_api_call(
        api=api_key,
        user_message=content,
        output_token_limit=output_token_limit
    )

    print("Raw Gemini Response:")
    print(raw_response)

    # 2. Validate JSON
    response = validate_json(
        raw_json=raw_response,
        output_json_path=output_json
    )

    # 3. Use validated Pydantic object
    if response is not None:
        print("\nValidated Response:")
        print(response.model_dump_json(indent=4))
    else:
        print("Invalid JSON response.")