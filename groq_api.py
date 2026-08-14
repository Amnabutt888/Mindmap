import os
from groq import Groq
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from llms.schema.json_structure import Output
from llms.schema.json_validation import validate_json


def groq_api_call(api: str, user_message:str) ->str | None:

    client = Groq(api_key=api)

    try:
        completion = client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=[
            {
                "role": "system",
                "content": """
    Return ONLY valid JSON in exactly this structure:
    {
    "sections": [
        {
        "title": "Section Name",
        "topics": [
            {
            "title": "Topic Name",
            "points": ["point 1", "point 2"]
            }
        ]
        }
    ]
    }
    """
            },
            {
                "role": "user",
                "content": f"""
            You are an educational mind-map generator.
            Analyze the following book content and extract its most important ideas into a clear hierarchical mind map.
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
            """
            }
        ],
            temperature=1,
            max_completion_tokens=2048,
            top_p=1,
            reasoning_effort="medium",
            stream=False,
            response_format={"type": "json_object"},
            stop=None
        )

        return completion.choices[0].message.content

    except Exception as e:
        print("Groq Api Failed")
        return None


if __name__ == "__main__":

    load_dotenv()
    api_key             = os.getenv("GROQ_API")

    content             = """
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
    output_json         = r"D:\000-University\Uni_Code_Prac\Rooman_Code\mind map\groq_mind_map.json"

    # 1. Calling LLM Api
    raw_response        = groq_api_call(api= api_key, user_message= content)
    print("Raw Groq Response:")
    print(raw_response)

    # 2. Validate JSON
    response = validate_json(raw_json=raw_response, output_json_path=output_json)

    # 3. Use validated Pydantic object
    if response is not None:
        print("\nValidated Response:")
        print(response.model_dump_json(indent=4))
    else:
        print("Invalid JSON response.")