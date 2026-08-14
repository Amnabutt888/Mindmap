import pdfplumber

# ===========================================================
# PDF se text nikalna
# ===========================================================
def get_all_lines(pdf_path):
    lines = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                lines.extend(text.split("\n"))
    return lines


def clean_lines(lines):
    result = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
        if line in ["•", "-", "–", "−"]:
            result.append(line)
            continue
        if result and result[-1] in ["•", "-", "–", "−"]:
            result[-1] = result[-1] + " " + line
            continue
        is_new_point = line.startswith(("•", "-", "–", "−", "Topic No"))
        if not is_new_point and result:
            last = result[-1]
            if not last.endswith(":") and not last.endswith("?"):
                result[-1] = last + " " + line
                continue
        result.append(line)
    return result

