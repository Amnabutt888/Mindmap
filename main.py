import sys
import re
import os
import asyncio
from dotenv import load_dotenv
from llms.gemni_api import gemini_api_call
from llms.hugging_face_api import hugging_face_api_call
from llms.groq_api import groq_api_call
from llms.schema.json_validation import validate_json
from pdf_utilities.data_extractor import get_all_lines, clean_lines
from pdf_utilities.map_builder import convert_json_to_markmap_tree, generate_interactive_html, convert_html_to_png, make_separate_maps



if __name__ == "__main__":


#======================================================================
# Step 1. Loading API Keys and Inputing User Details
#======================================================================
    load_dotenv()
    api_keys      = {
        "GEMINI":       os.getenv("GEMINI_API_KEY"),
        "GROQ":         os.getenv("GROQ_API"),
        "HUGGING_FACE": os.getenv("HUGGING_FACE_API"),
        "GEMINI_1":     os.getenv("GEMINI_API_KEY_1"),
        "GEMINI_2":     os.getenv("GEMINI_API_KEY_2"),
        "GEMINI_3":     os.getenv("GEMINI_API_KEY_3"),
        "GEMINI_4":     os.getenv("GEMINI_API_KEY_4"),
        "GEMINI_5":     os.getenv("GEMINI_API_KEY_5"),
        "GEMINI_6":     os.getenv("GEMINI_API_KEY_6"),
    }

    api_functions = {
        "GEMINI" : "gemini_api_call",
        "HUGGING_FACE" : "hugging_face_api_call",
        "GROQ" : "groq_api_call"
    }
    pdf_file      = input("Enter PDF File:")
    output_json   = input("Enter the output json file path:")

#======================================================================
# Step 2. Extracting Clean Text From PDF + Error Handling
#======================================================================
    if os.path.exists(pdf_file):
        print("Extracting Content from PDF.")
        raw_lines   = get_all_lines(pdf_file)
        clean_lines = clean_lines(raw_lines)
        clean_text = " ".join(clean_lines)
        print("Content Extracted and Cleaned from PDF.")

    else:
        sys.exit("Invalid text file path.")


#======================================================================
# Step 3. LLM Api Call (Multiple in case of failure) | Generating Json
#======================================================================    
    for LLM, API in api_keys.items():

        LLM = re.sub(r"_\d+$", "", LLM)
        print(f"Calling LLM {LLM}.")

        llm_function        = globals()[api_functions[LLM]]
        raw_response        = llm_function(api=API, user_message=clean_text)


#======================================================================
# Step 4. Validating LLM Json Response (Saving in Json file if valid)
#====================================================================== 
        if raw_response != None:

            response        = validate_json(raw_json= raw_response, output_json_path=output_json)

        if raw_response is not None:

            response = validate_json(
                raw_json=raw_response,
                output_json_path=output_json
            )

        if response is not None:

            print("\nValidated Response:")
            print(response.model_dump_json(indent=4))

            data = response.model_dump()

            # Get PDF filename and directory
            base_name = os.path.splitext(os.path.basename(pdf_file))[0]
            output_dir = os.path.dirname(pdf_file)

            # Create output paths in the same directory as the PDF
            html_output_path = os.path.join(
                output_dir,
                f"{base_name}_mindmap.html"
            )

            png_output_path = os.path.join(
                output_dir,
                f"{base_name}_mindmap.png"
            )

            if len(data.get("sections", [])) > 4:

                asyncio.run(
                    make_separate_maps(data, base_name)
                )

            else:

                tree = convert_json_to_markmap_tree(
                    data,
                    main_title=base_name
                )

                # Generate HTML
                html_path = generate_interactive_html(
                    tree,
                    html_output_path
                )

                # Generate PNG
                asyncio.run(
                    convert_html_to_png(
                        html_path,
                        png_output_path
                    )
                )

                print(f"[✓] Done:")
                print(f"HTML: {html_path}")
                print(f"PNG : {png_output_path}")

            break

        else:
            print("Invalid JSON response.")