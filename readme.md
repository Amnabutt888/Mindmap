# 🧠 Mind Maper

Turn any PDF into a clean, interactive mind map — automatically.

Mind Maper extracts text from a PDF, sends it to an LLM (Gemini, Groq, or Hugging Face — with automatic fallback), and renders the result as an **interactive HTML mind map** and a **PNG image**.

---

## ✨ Features

- 📄 **PDF text extraction** — reads and cleans raw PDF content
- 🤖 **Multi-LLM support** — Gemini, Groq, Hugging Face, with automatic fallback between providers/keys
- ✅ **Validated JSON output** — structured `sections → topics → points` schema
- 🗺️ **Interactive mind maps** — HTML (zoomable) + PNG export
- 📚 **Handles large documents** — auto-splits into multiple maps when a PDF has more than 4 sections

---

## ⚡ Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Add your API keys to .env
cp .env.example .env

# 3. Run it
python main.py
```

You'll be prompted for a PDF path and an output location — the mind map (HTML + PNG) is generated automatically.

---

## 🔄 How It Works

```
PDF → Extract Text → Clean Text → LLM (JSON) → Validate → Mind Map (HTML + PNG)
```

1. Extract & clean text from the PDF
2. Send it to an LLM, which returns structured JSON (`sections → topics → points`)
3. Validate the JSON — if invalid, automatically retry with the next provider
4. Convert JSON into an interactive HTML mind map + PNG snapshot
5. If the document has more than 4 sections, generate separate maps + an index page

---

## 📁 Project Structure

```
Mind-Maper/
├── main.py
├── requirements.txt
├── .env
├── llms/
│   ├── gemni_api.py
│   ├── groq_api.py
│   ├── hugging_face_api.py
│   └── schema/json_validation.py
├── pdf_utilities/
│   ├── data_extractor.py
│   └── check_pdf.py
├── input/
└── output/
```

---

## 📦 Output Schema

```json
{
  "sections": [
    {
      "title": "Section Name",
      "topics": [
        { "title": "Topic Name", "points": ["point 1", "point 2"] }
      ]
    }
  ]
}
```

---

## 🛠️ Tech Stack

Python · Gemini · Groq · Hugging Face · Pydantic · AsyncIO · Playwright (PNG rendering) · Markmap (HTML)

---

## 🚀 Roadmap

- [ ] OCR support for scanned PDFs
- [ ] Web interface / drag-and-drop upload
- [ ] DOCX & TXT support
- [ ] Editable mind map nodes
