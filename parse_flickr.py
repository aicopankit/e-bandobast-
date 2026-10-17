import re

def parse_flickr_file(filepath):
    print("=== Parsing:", filepath, "===")
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()

    title = re.search(r'<title>(.*?)</title>', text)
    print("Title:", title.group(1) if title else "N/A")

    # Meta tags
    for m in re.finditer(r'<meta property="([^"]+)" content="([^"]+)"', text):
        if 'image' in m.group(1) or 'description' in m.group(1) or 'title' in m.group(1):
            print(f"Meta {m.group(1)}: {m.group(2)}")

    # Model data or taken dates
    dates = re.findall(r'dateTaken["\']?\s*:\s*["\']?([^"\'\,]+)', text)
    if dates:
        print("Date taken:", dates[0])

parse_flickr_file(r'C:\Users\aicop\.gemini\antigravity\brain\f510f289-acc6-4433-8d04-3a51a88bc0ca\.system_generated\steps\44\content.md')
