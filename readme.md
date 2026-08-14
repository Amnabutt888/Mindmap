# Mind Maper

## Overview

**Mind Maper** is a Python-based tool that converts the content of a PDF document into an interactive visual mind map.

The application follows an automated pipeline:

1. Extract text from a PDF.
2. Clean and preprocess the extracted content.
3. Send the content to one or more Large Language Models (LLMs).
4. Generate structured JSON representing sections, topics, and key points.
5. Validate the generated JSON.
6. Convert the JSON into a mind map structure.
7. Generate an interactive HTML mind map.
8. Export the mind map as a PNG image.

The project supports multiple LLM providers, allowing fallback to another model if one provider returns an invalid response.

---

## Features

* PDF text extraction
* Text cleaning and preprocessing
* Multi-LLM support
* Gemini API integration
* Groq API integration
* Hugging Face API integration
* Automatic fallback between API keys/providers
* Structured JSON generation
* JSON validation
* Interactive HTML mind map generation
* PNG export
* Automatic splitting into separate maps for large documents
* Environment variable support for API keys

---

## Example Output

The tool converts a PDF into a structured visual mind map.

Example hierarchy:

```text
sample
├── Policy Basics
│   ├── Guideline
│   ├── Standard
│   ├── In Practice
│   └── Examples
│
├── Program Steps
│   ├── Program Definition
│   ├── Step 4 Controls
│   ├── Step 5 Validate
│   ├── Step 6 Accreditation
│   └── Step 7 Monitor
│
├── Management Commitment
│   ├── Definition
│   ├── ISO Clause
│   ├── Tone Top
│   └── In Practice
│
└── Security Responsibility
    └── Default View
```

The generated output includes:

* An **interactive HTML mind map**
* A **PNG image** of the mind map

---

# Project Workflow

The complete processing pipeline is:

```text
                ┌─────────────┐
                │  Input PDF  │
                └──────┬──────┘
                       │
                       ▼
          ┌─────────────────────────┐
          │ Extract PDF Text        │
          │ get_all_lines()         │
          └────────────┬────────────┘
                       │
                       ▼
          ┌─────────────────────────┐
          │ Clean Extracted Text    │
          │ clean_lines()           │
          └────────────┬────────────┘
                       │
                       ▼
          ┌─────────────────────────┐
          │ Call LLM API            │
          │ Gemini / Groq / HF      │
          └────────────┬────────────┘
                       │
                       ▼
          ┌─────────────────────────┐
          │ Generate Structured     │
          │ JSON Response           │
          └────────────┬────────────┘
                       │
                       ▼
          ┌─────────────────────────┐
          │ Validate JSON           │
          │ validate_json()         │
          └────────────┬────────────┘
                       │
                       ▼
              ┌─────────────────┐
              │ Check Sections  │
              └────────┬────────┘
                       │
          ┌────────────┴────────────┐
          │                         │
     ≤ 4 Sections               > 4 Sections
          │                         │
          ▼                         ▼
  Generate One Map          Generate Separate Maps
          │                         │
          ▼                         ▼
 Interactive HTML              Multiple Maps
          │
          ▼
      PNG Export
```

---

# Project Structure

A recommended project structure is:

```text
Mind-Maper/
│
├── main.py
├── requirements.txt
├── .env
├── .gitignore
├── README.md
│
├── llms/
│   ├── __init__.py
│   ├── gemni_api.py
│   ├── groq_api.py
│   ├── hugging_face_api.py
│   │
│   └── schema/
│       ├── __init__.py
│       └── json_validation.py
│
├── pdf_utilities/
│   ├── __init__.py
│   ├── data_extractor.py
│   └── check_pdf.py
│
├── input/
│   └── sample_input.pdf
│
└── output/
    ├── sample_output.json
    ├── sample_mindmap.html
    └── sample_mindmap.png
```

> **Note:** The filename `gemni_api.py` appears to be intentionally used in the current project. If renaming it to `gemini_api.py`, make sure to update the corresponding imports.

---

# Modules

## `main.py`

The main entry point of the application.

It is responsible for:

* Loading environment variables
* Loading API keys
* Reading the input PDF path
* Extracting text from the PDF
* Cleaning the extracted text
* Calling available LLM APIs
* Validating the generated JSON
* Generating a mind map
* Saving HTML and PNG outputs

### Imported Modules

```python
import sys
import re
import os
import asyncio

from dotenv import load_dotenv

from llms.gemni_api import gemini_api_call
from llms.hugging_face_api import hugging_face_api_call
from llms.groq_api import groq_api_call

from llms.schema.json_validation import validate_json

from pdf_utilities.data_extractor import (
    get_all_lines,
    clean_lines
)

from pdf_utilities.check_pdf import (
    convert_json_to_markmap_tree,
    generate_interactive_html,
    convert_html_to_png,
    make_separate_maps
)
```

---

# LLM Modules

## Gemini

```text
llms/gemni_api.py
```

Provides:

```python
gemini_api_call()
```

This function sends the cleaned PDF text to a Gemini model and returns a structured response.

---

## Groq

```text
llms/groq_api.py
```

Provides:

```python
groq_api_call()
```

This function sends the extracted content to an LLM available through the Groq API.

---

## Hugging Face

```text
llms/hugging_face_api.py
```

Provides:

```python
hugging_face_api_call()
```

This function communicates with a model hosted or accessed through Hugging Face.

---

# PDF Processing

## `pdf_utilities/data_extractor.py`

This module is responsible for extracting and cleaning PDF content.

### Functions

#### `get_all_lines()`

Extracts text content from the PDF.

Example:

```python
raw_lines = get_all_lines(pdf_file)
```

---

#### `clean_lines()`

Cleans the extracted PDF text.

Example:

```python
clean_lines = clean_lines(raw_lines)
clean_text = " ".join(clean_lines)
```

The resulting `clean_text` is passed to the LLM.

---

# JSON Structure

The LLM is expected to return structured data in the following format:

```json
{
  "sections": [
    {
      "title": "Section Name",
      "topics": [
        {
          "title": "Topic Name",
          "points": [
            "point 1",
            "point 2"
          ]
        }
      ]
    },
    {
      "title": "Another Section",
      "topics": [
        {
          "title": "Another Topic",
          "points": [
            "point 1",
            "point 2"
          ]
        }
      ]
    }
  ]
}
```

## Structure Explanation

```text
sections
│
├── Section
│   │
│   ├── title
│   │
│   └── topics
│       │
│       ├── Topic
│       │   ├── title
│       │   └── points
│       │       ├── point 1
│       │       └── point 2
│       │
│       └── Topic
│
└── Section
```

This hierarchical structure is used to create the mind map.

---

# JSON Validation

The generated LLM response is validated using:

```python
validate_json()
```

Example:

```python
response = validate_json(
    raw_json=raw_response,
    output_json_path=output_json
)
```

If the JSON is valid:

* The validated response is returned.
* The structured JSON is saved to the specified output path.
* The application continues to generate the mind map.

If the JSON is invalid:

```text
Invalid JSON response.
```

The application then attempts the next configured LLM/API key.

---

# API Configuration

The project uses environment variables to store API keys.

Create a `.env` file in the project root.

```env
GEMINI_API_KEY=your_gemini_api_key
GROQ_API=your_groq_api_key
HUGGING_FACE_API=your_hugging_face_api_key

GEMINI_API_KEY_1=your_second_gemini_key
GEMINI_API_KEY_2=your_third_gemini_key
GEMINI_API_KEY_3=your_fourth_gemini_key
GEMINI_API_KEY_4=your_fifth_gemini_key
GEMINI_API_KEY_5=your_sixth_gemini_key
GEMINI_API_KEY_6=your_seventh_gemini_key
```

The application loads these values using:

```python
from dotenv import load_dotenv

load_dotenv()
```

---

# API Fallback Logic

The application supports multiple API keys and providers.

```python
api_keys = {
    "GEMINI": os.getenv("GEMINI_API_KEY"),
    "GROQ": os.getenv("GROQ_API"),
    "HUGGING_FACE": os.getenv("HUGGING_FACE_API"),
    "GEMINI_1": os.getenv("GEMINI_API_KEY_1"),
    "GEMINI_2": os.getenv("GEMINI_API_KEY_2"),
    "GEMINI_3": os.getenv("GEMINI_API_KEY_3"),
    "GEMINI_4": os.getenv("GEMINI_API_KEY_4"),
    "GEMINI_5": os.getenv("GEMINI_API_KEY_5"),
    "GEMINI_6": os.getenv("GEMINI_API_KEY_6")
}
```

The provider function mapping is:

```python
api_functions = {
    "GEMINI": "gemini_api_call",
    "HUGGING_FACE": "hugging_face_api_call",
    "GROQ": "groq_api_call"
}
```

For Gemini backup keys, the numeric suffix is removed:

```python
LLM = re.sub(r"_\d+$", "", LLM)
```

For example:

```text
GEMINI_1 → GEMINI
GEMINI_2 → GEMINI
GEMINI_3 → GEMINI
```

This allows all backup Gemini keys to use:

```python
gemini_api_call()
```

The application stops after receiving a valid response:

```python
break
```

This creates a fallback mechanism:

```text
Try Gemini
    │
    ├── Valid JSON ──────► Generate Mind Map
    │
    └── Failed
           │
           ▼
        Try Groq
           │
           ├── Valid JSON ──────► Generate Mind Map
           │
           └── Failed
                  │
                  ▼
           Try Hugging Face
                  │
                  ▼
             Try Backup Keys
```

---

# Mind Map Generation

The module:

```text
pdf_utilities/check_pdf.py
```

contains the mind map generation functionality.

## `convert_json_to_markmap_tree()`

Converts the structured JSON into a tree format suitable for mind map generation.

Example:

```python
tree = convert_json_to_markmap_tree(
    data,
    main_title=base_name
)
```

The PDF filename is used as the main title of the mind map.

---

## `generate_interactive_html()`

Generates an interactive HTML version of the mind map.

Example:

```python
html_path = generate_interactive_html(
    tree,
    base_name
)
```

The generated HTML can be opened in a browser.

---

## `convert_html_to_png()`

Converts the generated HTML mind map into a PNG image.

Example:

```python
asyncio.run(
    convert_html_to_png(
        html_path,
        f"{base_name}_mindmap.png"
    )
)
```

---

## `make_separate_maps()`

For large documents, generating one mind map can make the output difficult to read.

The application checks the number of sections:

```python
if len(data.get("sections", [])) > 4:
    asyncio.run(make_separate_maps(data, base_name))
```

If the document contains more than four sections, separate mind maps are generated.

Otherwise, a single mind map is created.

---

# Installation

## 1. Clone the Repository

```bash
git clone <repository-url>
```

```bash
cd Mind-Maper
```

---

## 2. Create a Virtual Environment

### Windows

```bash
python -m venv venv
```

```bash
venv\Scripts\activate
```

### Linux/macOS

```bash
python3 -m venv venv
```

```bash
source venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

A typical `requirements.txt` may include dependencies such as:

```text
python-dotenv
pydantic
```

Additional dependencies depend on the implementation used for:

* PDF extraction
* LLM APIs
* HTML rendering
* Browser automation
* PNG generation

---

## 4. Configure API Keys

Create a `.env` file:

```env
GEMINI_API_KEY=your_api_key
GROQ_API=your_api_key
HUGGING_FACE_API=your_api_key
```

Optionally configure additional Gemini API keys:

```env
GEMINI_API_KEY_1=your_api_key
GEMINI_API_KEY_2=your_api_key
GEMINI_API_KEY_3=your_api_key
```

---

# Usage

Update the input and output paths in `main.py`.

```python
pdf_file = r"path/to/input.pdf"

output_json = r"path/to/output.json"
```

For example:

```python
pdf_file = r"D:\Mind-Maper\input\sample_input.pdf"

output_json = r"D:\Mind-Maper\output\sample_output.json"
```

Then run:

```bash
python main.py
```

---

# Expected Console Output

A successful execution may look similar to:

```text
Extracting Content from PDF.

Content Extracted and Cleaned from PDF.

Calling LLM GEMINI.

Validated Response:
{
    "sections": [
        {
            "title": "Policy Basics",
            "topics": [
                {
                    "title": "Guideline",
                    "points": []
                }
            ]
        }
    ]
}

[✓] Done: sample_mindmap.png / sample_mindmap.html
```

If an LLM returns invalid JSON:

```text
Calling LLM GEMINI.

Invalid JSON response.

Calling LLM GROQ.
```

The application continues trying the next configured provider or API key.

---

# Input

The application expects:

```text
PDF Document
```

Example:

```text
sample_input.pdf
```

The PDF content should contain extractable text. Scanned PDFs may require OCR support if the current PDF extraction implementation does not support image-based text extraction.

---

# Output

Depending on the document structure, the application generates:

```text
sample_output.json
sample_mindmap.html
sample_mindmap.png
```

For large documents:

```text
sample_section_1.html
sample_section_1.png

sample_section_2.html
sample_section_2.png

sample_section_3.html
sample_section_3.png
```

The exact filenames depend on the implementation of `make_separate_maps()`.

---

# Example Processing Flow

Given a PDF containing:

```text
Policy Basics

Guidelines
Standards
Examples

Program Steps

Definition
Controls
Validation
Accreditation

Management Commitment

ISO Requirements
Leadership Responsibilities
Implementation
```

The LLM may generate:

```json
{
  "sections": [
    {
      "title": "Policy Basics",
      "topics": [
        {
          "title": "Guidelines",
          "points": [
            "General guidelines",
            "Policy requirements"
          ]
        },
        {
          "title": "Standards",
          "points": [
            "Applicable standards"
          ]
        }
      ]
    },
    {
      "title": "Program Steps",
      "topics": [
        {
          "title": "Definition",
          "points": [
            "Program definition"
          ]
        },
        {
          "title": "Controls",
          "points": [
            "Security controls",
            "Validation requirements"
          ]
        }
      ]
    }
  ]
}
```

The JSON is then transformed into a visual hierarchy.

---

# Error Handling

The project currently handles several failure scenarios.

## Invalid PDF Path

```python
if os.path.exists(pdf_file):
    ...
else:
    sys.exit("Invalid text file path.")
```

If the provided file does not exist, the application terminates.

> Consider changing the message from `Invalid text file path.` to `Invalid PDF file path.` for clarity.

---

## Invalid LLM Response

```python
if raw_response != None:
    response = validate_json(
        raw_json=raw_response,
        output_json_path=output_json
    )
```

If the response cannot be validated, the next LLM or API key can be attempted.

---

# Recommended Improvements

The current implementation can be extended with the following improvements.

## 1. Check for Missing API Keys

Before calling an API:

```python
if not API:
    print(f"Skipping {LLM}: API key not configured.")
    continue
```

This prevents unnecessary API calls with empty keys.

---

## 2. Add Exception Handling Around API Calls

Example:

```python
try:
    raw_response = llm_function(
        api=API,
        user_message=clean_text
    )
except Exception as e:
    print(f"Error calling {LLM}: {e}")
    continue
```

This ensures that one failed provider does not terminate the application.

---

## 3. Use `Pathlib`

Instead of manually handling paths:

```python
import os
```

consider:

```python
from pathlib import Path

pdf_file = Path("input/sample_input.pdf")
output_json = Path("output/sample_output.json")
```

This improves cross-platform compatibility.

---

## 4. Add Command-Line Arguments

Instead of editing paths directly in the source code:

```bash
python main.py --input sample_input.pdf --output sample_output.json
```

This could be implemented using `argparse`.

---

## 5. Add Logging

Replace basic `print()` statements with Python logging:

```python
import logging

logging.info("Extracting content from PDF.")
logging.error("Invalid JSON response.")
```

---

## 6. Add OCR Support

For scanned PDFs, integrate OCR so that image-based documents can also be processed.

---

# Suggested Future Features

* Drag-and-drop PDF upload interface
* Web application interface
* REST API
* Support for DOCX and TXT files
* OCR for scanned PDFs
* User-selectable LLM provider
* Mind map themes
* Custom node colors
* PDF export
* SVG export
* Zoom and pan controls
* Editable mind map nodes
* Download generated files from a web interface
* Docker support
* Batch PDF processing
* Progress indicators for long documents

---

# Technology Stack

| Component                  | Purpose                               |
| -------------------------- | ------------------------------------- |
| Python                     | Core application                      |
| PDF Utilities              | PDF text extraction and preprocessing |
| Gemini                     | LLM text structuring                  |
| Groq                       | Alternative LLM provider              |
| Hugging Face               | Alternative LLM provider              |
| Pydantic / JSON Validation | Structured response validation        |
| HTML                       | Interactive mind map output           |
| AsyncIO                    | Asynchronous output generation        |
| PNG Rendering              | Static image export                   |
| Python Dotenv              | Environment variable management       |

---

# Main Execution Logic

The core application workflow is:

```python
if __name__ == "__main__":

    load_dotenv()

    # Load API keys
    api_keys = {
        ...
    }

    # Configure input and output
    pdf_file = "sample_input.pdf"
    output_json = "sample_output.json"

    # Extract PDF text
    if os.path.exists(pdf_file):

        raw_lines = get_all_lines(pdf_file)

        cleaned_lines = clean_lines(raw_lines)

        clean_text = " ".join(cleaned_lines)

    else:
        sys.exit("Invalid PDF file path.")

    # Try available LLMs
    for LLM, API in api_keys.items():

        LLM = re.sub(r"_\d+$", "", LLM)

        llm_function = globals()[api_functions[LLM]]

        raw_response = llm_function(
            api=API,
            user_message=clean_text
        )

        # Validate response
        if raw_response is not None:

            response = validate_json(
                raw_json=raw_response,
                output_json_path=output_json
            )

        # Generate output
        if response is not None:

            data = response.model_dump()

            base_name = os.path.splitext(
                os.path.basename(pdf_file)
            )[0]

            if len(data.get("sections", [])) > 4:

                asyncio.run(
                    make_separate_maps(
                        data,
                        base_name
                    )
                )

            else:

                tree = convert_json_to_markmap_tree(
                    data,
                    main_title=base_name
                )

                html_path = generate_interactive_html(
                    tree,
                    base_name
                )

                asyncio.run(
                    convert_html_to_png(
                        html_path,
                        f"{base_name}_mindmap.png"
                    )
                )

            break
```

---

# Contributing

Contributions are welcome.

Possible areas for contribution include:

* Improving PDF extraction
* Adding additional LLM providers
* Improving JSON validation
* Adding new mind map layouts
* Improving large-document handling
* Adding a user interface
* Improving export formats
* Writing tests and documentation

A typical contribution workflow is:

```bash
git checkout -b feature/your-feature-name
```

Make your changes, test them, and submit a pull request.

---

# License

Add your preferred license here.

For example:

```text
MIT License
```

---

# Author

**Mind Maper**
A Python-based PDF-to-Mind-Map generation tool powered by Large Language Models.

---

## Summary

**Mind Maper** transforms PDF documents into structured and easy-to-understand visual mind maps.

```text
PDF
 │
 ▼
Text Extraction
 │
 ▼
Text Cleaning
 │
 ▼
LLM Processing
 │
 ▼
Structured JSON
 │
 ▼
JSON Validation
 │
 ▼
Mind Map Tree
 │
 ├── Interactive HTML
 │
 └── PNG Image
```

The project is designed to make large PDF documents easier to understand by automatically identifying their structure and converting that structure into an interactive visual representation.
