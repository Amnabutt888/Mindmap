import os
import re
import json
import asyncio
from playwright.async_api import async_playwright


# ===========================================================
# STEP 1: JSON Adapter (sections/topics/points -> Markmap Tree)
# ===========================================================
def convert_json_to_markmap_tree(input_data, main_title="Mindmap"):
    root = {"content": main_title, "children": []}

    for section in input_data.get("sections", []):
        section_node = {"content": section.get("title", ""), "children": []}

        for topic in section.get("topics", []):
            topic_node = {"content": topic.get("title", ""), "children": []}

            for point in topic.get("points", []):
                topic_node["children"].append({"content": point})

            section_node["children"].append(topic_node)

        root["children"].append(section_node)   # <-- ab loop ke andar hai (fix)

    return root


# ===========================================================
# STEP 2: HTML Generator
# ===========================================================
def generate_interactive_html(tree_data, base_name):
    html_file = f"{base_name}_mindmap.html"

    html_template = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{base_name} Mindmap</title>
    <style>
        body {{ margin: 0; padding: 0; width: 100vw; height: 100vh; overflow: hidden; background: #ffffff; }}
        #mindmap {{ width: 100%; height: 100%; }}
        .markmap-node {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; font-size: 15px; }}
    </style>
    <script src="https://cdn.jsdelivr.net/npm/d3@7"></script>
    <script src="https://cdn.jsdelivr.net/npm/markmap-view"></script>
</head>
<body>
    <svg id="mindmap"></svg>
    <script>
        const treeData = {json.dumps(tree_data)};
        const {{ Markmap }} = window.markmap;
        const mm = Markmap.create('#mindmap', {{
            duration: 0,
            colorFreezeLevel: 3,
            initialExpandLevel: 4
        }}, treeData);
        setTimeout(() => {{ mm.fit(); }}, 500);
    </script>
</body>
</html>"""

    with open(html_file, "w", encoding="utf-8") as f:
        f.write(html_template)

    return html_file


# ===========================================================
# STEP 3: Convert HTML to High-Res PNG via System Chrome
# ===========================================================
async def convert_html_to_png(html_path, png_path):
    async with async_playwright() as p:
        browser = await p.chromium.launch(channel="chrome", headless=True)
        page = await browser.new_page(viewport={"width": 2560, "height": 1440})

        abs_path = "file://" + os.path.abspath(html_path)
        await page.goto(abs_path)

        await page.wait_for_timeout(2000)
        await page.screenshot(path=png_path, full_page=True)
        await browser.close()


def safe_filename(text, max_len=30):
    """Section title ko safe filename mein badalta hai (special chars hata kar)."""
    text = re.sub(r'[\\/*?:"<>|]', "", text)
    return text.strip()[:max_len].strip()


# ===========================================================
# STEP 4: Har section ki ALAG mind map banana (bara PDF ke liye)
# ===========================================================
async def make_separate_maps(input_data, base_name="mindmap"):
    sections = input_data.get("sections", [])
    index_links = []

    for i, section in enumerate(sections, start=1):
        section_title = section.get("title", f"Section {i}")
        file_base = f"{base_name}_part{i}_{safe_filename(section_title)}"

        single_section_data = {"sections": [section]}
        tree = convert_json_to_markmap_tree(single_section_data, main_title=section_title)

        html_path = generate_interactive_html(tree, file_base)
        png_path = f"{file_base}_mindmap.png"

        print(f"[+] Building part {i}/{len(sections)}: {section_title}")
        await convert_html_to_png(html_path, png_path)

        index_links.append((section_title, html_path))

    make_index_page(index_links, base_name)
    print(f"\n[✓] {len(sections)} alag mind maps ban gayi + index page")


def make_index_page(index_links, base_name="mindmap"):
    items = ""
    for title, link in index_links:
        items += f'<li><a href="{link}" target="_blank">{title}</a></li>\n'

    html = f"""<!DOCTYPE html>
<html>
<head><meta charset="UTF-8"><title>{base_name} - Index</title>
<style>
body {{ font-family: 'Segoe UI', sans-serif; padding: 40px; }}
li {{ margin: 10px 0; font-size: 16px; }}
a {{ text-decoration: none; color: #2563eb; }}
</style>
</head>
<body>
<h1>{base_name} — Mind Map Sections</h1>
<ul>
{items}
</ul>
</body>
</html>"""

    filename = f"{base_name}_index.html"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"[✓] Index page saved: {filename}")


# ===========================================================
# MAIN EXECUTION
# ===========================================================
if __name__ == "__main__":
    json_input_file = input("Enter JSON file path (or press Enter if using sample): ").strip().strip('"').strip("'")

    if json_input_file and os.path.exists(json_input_file):
        with open(json_input_file, "r", encoding="utf-8") as f:
            input_data = json.load(f)
        base_name = os.path.splitext(os.path.basename(json_input_file))[0]
    else:
        input_data = {
            "sections": [
                {"title": "Origin And Meaning",
                 "topics": [{"title": "Latin Root", "points": ["Communico root", "Means to share"]},
                            {"title": "Core Definition", "points": ["Sharing information", "Between people", "Mutual understanding"]}]},
                {"title": "Shared Content", "topics":
                 [{"title": "Information Types", "points": ["Facts and ideas", "Thoughts and feelings", "Personal needs"]}]}
            ]
        }
        base_name = "Communication_Concept"

    print(f"\n[+] Processing JSON data for '{base_name}'...")

    if len(input_data.get("sections", [])) > 4:
        asyncio.run(make_separate_maps(input_data, base_name))
    else:
        markmap_tree = convert_json_to_markmap_tree(input_data, main_title=base_name)
        out_html = generate_interactive_html(markmap_tree, base_name)
        out_png = f"{base_name}_mindmap.png"
        try:
            asyncio.run(convert_html_to_png(out_html, out_png))
            print(f"\n[✓] Success! Mindmap PNG: {out_png}")
            print(f"[✓] Saved Interactive HTML: {out_html}")
        except Exception as e:
            print(f"\n[!] PNG Error: {e}")