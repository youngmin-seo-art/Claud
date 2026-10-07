import re
import os

def ascii_box_to_md_table(text):
    """
    Converts ASCII box-drawing tables (┌──┬──┐) to standard markdown tables (| col1 | col2 |).
    """
    lines = text.split('\n')
    new_lines = []
    in_box = False
    box_lines = []

    for line in lines:
        stripped = line.strip()
        # Detect ASCII box start
        if re.match(r'^[┌╔]', stripped):
            in_box = True
            box_lines = [line]
            continue
        
        if in_box:
            box_lines.append(line)
            # Detect ASCII box end
            if re.match(r'^[└╚]', stripped):
                in_box = False
                # Process box lines
                converted = parse_box_to_table(box_lines)
                new_lines.extend(converted)
                box_lines = []
            continue
        
        new_lines.append(line)

    return '\n'.join(new_lines)

def parse_box_to_table(box_lines):
    cleaned_rows = []
    is_table_content = False

    for bline in box_lines:
        s = bline.strip()
        # Skip top/bottom/middle boundary lines that don't have column pipes
        if re.match(r'^[┌╔].*[┐╗]$', s) or re.match(r'^[└╚].*[┘╝]$', s):
            continue
        if re.match(r'^[├╠].*[┤╣]$', s):
            continue
        if not s.startswith('│') and not s.startswith('|'):
            continue

        # Extract cells separated by │ or |
        inner = s[1:-1] if (s.startswith('│') and s.endswith('│')) or (s.startswith('|') and s.endswith('|')) else s
        # Split by │ or |
        cells = [c.strip() for c in re.split(r'[│|]', inner)]
        
        # Check if this is a title bar (single large cell with no separator or mostly whitespace)
        if len(cells) == 1 and ('==' in cells[0] or '--' in cells[0] or len(cells[0]) > 0):
            # Check if it looks like a section header inside a box
            title = cells[0].strip()
            if title and not re.match(r'^[-=]+$', title):
                cleaned_rows.append([title])
            continue
        
        # Filter out purely dashed lines
        if all(re.match(r'^[-=─═\s]+$', c) for c in cells if c):
            continue
            
        if any(c for c in cells):
            cleaned_rows.append(cells)

    if not cleaned_rows:
        return box_lines

    # Check max cols
    max_cols = max(len(r) for r in cleaned_rows)
    
    # If all rows have 1 cell, it might be a callout note box
    if max_cols == 1:
        md_res = ["> " + r[0] for r in cleaned_rows if r[0]]
        return md_res

    # Normalize rows to max_cols
    normalized = []
    for r in cleaned_rows:
        while len(r) < max_cols:
            r.append("")
        normalized.append(r)

    # Build markdown table
    md_res = []
    # Header
    header = normalized[0]
    md_res.append("| " + " | ".join(header) + " |")
    md_res.append("| " + " | ".join(["---"] * max_cols) + " |")
    for row in normalized[1:]:
        md_res.append("| " + " | ".join(row) + " |")
    
    return md_res

if __name__ == "__main__":
    base_dir = r"c:\Users\immnu\Desktop\Claud\OnyuwolKorea\프로젝트 팀\국가재난_긴급_유무선_통합통신시스템_컨설팅\04_산출물"
    for fname in os.listdir(base_dir):
        if fname.endswith(".md"):
            fpath = os.path.join(base_dir, fname)
            with open(fpath, 'r', encoding='utf-8') as f:
                content = f.read()
            converted = ascii_box_to_md_table(content)
            with open(fpath, 'w', encoding='utf-8') as f:
                f.write(converted)
            print(f"Processed: {fname}")
