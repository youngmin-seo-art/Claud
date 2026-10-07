import os
import re
import sys
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=120, bottom=120, left=140, right=140):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>')
    tcPr.append(tcMar)

def set_table_borders(table, color="CBD5E1"):
    tblPr = table._tbl.tblPr
    borders = parse_xml(f'''
        <w:tblBorders {nsdecls("w")}>
            <w:top w:val="single" w:sz="12" w:space="0" w:color="1B365D"/>
            <w:bottom w:val="single" w:sz="12" w:space="0" w:color="1B365D"/>
            <w:left w:val="none"/>
            <w:right w:val="none"/>
            <w:insideH w:val="single" w:sz="4" w:space="0" w:color="{color}"/>
            <w:insideV w:val="none"/>
        </w:tblBorders>
    ''')
    tblPr.append(borders)

def make_row_cant_split(row):
    trPr = row._tr.get_or_add_trPr()
    trPr.append(parse_xml(f'<w:cantSplit {nsdecls("w")}/>'))

def make_row_header(row):
    trPr = row._tr.get_or_add_trPr()
    trPr.append(parse_xml(f'<w:tblHeader {nsdecls("w")}/>'))

def clean_math_text(text):
    if not text:
        return text
    t = text
    replacements = [
        (r'\\Delta\s*t', 'Δt'),
        (r'\\Delta', 'Δ'),
        (r'\\lambda', 'λ'),
        (r'\\cdot', ' · '),
        (r'\\times', ' × '),
        (r'\\partial', '∂'),
        (r'\\mathbb\{E\}', 'E'),
        (r'\\mathbb\{R\}', 'R'),
        (r'\\max_\\theta', 'max_θ'),
        (r'\\max', 'max'),
        (r'\\min', 'min'),
        (r'\\sum_\{t=0\}\^T', '∑(t=0 to T)'),
        (r'\\sum', '∑'),
        (r'\\gamma', 'γ'),
        (r'\\alpha', 'α'),
        (r'\\beta_0', 'β₀'),
        (r'\\beta_1', 'β₁'),
        (r'\\beta_2', 'β₂'),
        (r'\\beta_3', 'β₃'),
        (r'\\beta_k', 'β_k'),
        (r'\\beta', 'β'),
        (r'\\theta', 'θ'),
        (r'\\sigma', 'σ'),
        (r'\\varepsilon', 'ε'),
        (r'\\mu_i', 'μᵢ'),
        (r'\\mu', 'μ'),
        (r'\\ln', 'ln'),
        (r'\\exp', 'exp'),
        (r'\\ge', '≥'),
        (r'\\le', '≤'),
        (r'\\pm', '±'),
        (r'\\text\{casualty\}', 'casualty'),
        (r'\\text\{urban\}', 'urban'),
        (r'\\text\{confined\}', 'confined'),
        (r'\\text\{voice\}', 'voice'),
        (r'\\text\{video\}', 'video'),
        (r'\\text\{Loss\}', 'Loss'),
        (r'\\text\{Delay\}', 'Delay'),
        (r'\\text\{Bandwidth\}', 'Bandwidth'),
        (r'\\text\{Packet Loss\}', 'Packet Loss'),
        (r'\\text\{Latency\}', 'Latency'),
        (r'\\text\{Queue Length\}', 'Queue Length'),
        (r'\\text\{min\}', 'min'),
        (r'\\text\{CI\}', 'CI'),
        (r'\\text\{IRR\}', 'IRR'),
        (r'\\text\{response\}', 'response'),
        (r'\\text\{detect\}', 'detect'),
        (r'\\text\{dispatch\}', 'dispatch'),
        (r'\\text\{comm_setup\}', 'comm_setup'),
        (r'\\text\{travel\}', 'travel'),
        (r'\\text\{abs\}', 'abs'),
        (r'\\text\{([^}]+)\}', r'\1'),
        (r'T_\{response\}', 'T_response'),
        (r'T_\{detect\}', 'T_detect'),
        (r'T_\{dispatch\}', 'T_dispatch'),
        (r'T_\{comm\\_setup\}', 'T_comm_setup'),
        (r'T_\{comm_setup\}', 'T_comm_setup'),
        (r'T_\{travel\}', 'T_travel'),
        (r'N_\{casualty\}', 'N_casualty'),
        (r'N_\{0,\s*i\}', 'N₀,ᵢ'),
        (r'N_0', 'N₀'),
        (r'\\left\(', '('),
        (r'\\right\)', ')'),
        (r'\\left\[', '['),
        (r'\\right\]', ']'),
        (r'\^t', 'ᵗ'),
        (r'\^2', '²'),
        (r'_i', 'ᵢ'),
        (r'_t', 'ₜ'),
        (r'_0', '₀'),
        (r'_1', '₁'),
        (r'_2', '₂'),
        (r'_3', '₃'),
        (r'\\', ''),
        (r'\$', ''),
    ]
    for pattern, repl in replacements:
        t = re.sub(pattern, repl, t)
    return t

def calculate_column_widths(table_rows, page_width_inches=6.5):
    num_cols = max(len(r) for r in table_rows)
    if num_cols == 0:
        return [Inches(page_width_inches)]
    
    # Calculate average and max length of text in each column
    max_lens = [0] * num_cols
    for row in table_rows:
        for c_idx in range(num_cols):
            val = row[c_idx] if c_idx < len(row) else ""
            clean_len = len(val.replace('<br>', '\n').replace('**', ''))
            if clean_len > max_lens[c_idx]:
                max_lens[c_idx] = clean_len
    
    # Floor minimum weight
    weights = [max(l, 8) for l in max_lens]
    
    # Special cases for 2 columns:
    if num_cols == 2:
        ratio = weights[0] / (weights[0] + weights[1])
        # If ratio is between 0.4 and 0.6, make them equal 50/50
        if 0.38 <= ratio <= 0.62:
            return [Inches(page_width_inches * 0.5), Inches(page_width_inches * 0.5)]
        elif ratio < 0.38:
            w1 = max(1.5, page_width_inches * (weights[0] / sum(weights)))
            w1 = min(w1, 2.2)
            w2 = page_width_inches - w1
            return [Inches(w1), Inches(w2)]
        else:
            w2 = max(1.5, page_width_inches * (weights[1] / sum(weights)))
            w2 = min(w2, 2.2)
            w1 = page_width_inches - w2
            return [Inches(w1), Inches(w2)]
            
    # For 3 or more columns, calculate proportional widths with bounds
    total_weight = sum(weights)
    raw_widths = [(w / total_weight) * page_width_inches for w in weights]
    
    # Clamp minimum width to 0.8 inches
    min_w = 0.8
    adjusted_widths = [max(w, min_w) for w in raw_widths]
    scale = page_width_inches / sum(adjusted_widths)
    final_widths = [Inches(w * scale) for w in adjusted_widths]
    return final_widths

def build_docx_from_markdown(md_path, docx_path, title_main):
    doc = docx.Document()
    
    # Page margins: 1.0 inch (body width = 6.5 inches)
    page_width_inches = 6.5
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)
        
        # Header
        header = section.header
        hp = header.paragraphs[0]
        hp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        hrun = hp.add_run(f"ITS 컨버젼스 | {title_main}")
        hrun.font.size = Pt(8.5)
        hrun.font.color.rgb = RGBColor(100, 116, 139)
        hrun.font.name = "맑은 고딕"
        
        # Footer
        footer = section.footer
        fp = footer.paragraphs[0]
        fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
        frun = fp.add_run("오뉴월 코리아 프로젝트팀 | [대외비 - Confidential]")
        frun.font.size = Pt(8.5)
        frun.font.color.rgb = RGBColor(100, 116, 139)
        frun.font.name = "맑은 고딕"

    normal_style = doc.styles['Normal']
    normal_style.font.name = '맑은 고딕'
    normal_style.font.size = Pt(10)
    normal_style.font.color.rgb = RGBColor(30, 41, 59)

    with open(md_path, 'r', encoding='utf-8') as f:
        text = f.read()

    lines = text.split('\n')

    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        if not stripped or stripped == '---':
            i += 1
            continue

        # 0. Check for Image (![alt](path))
        img_match = re.match(r'^!\[(.*)\]\((.*?)\)$', stripped)
        if img_match:
            alt_text = img_match.group(1).strip()
            img_rel_path = img_match.group(2).strip()
            
            md_dir = os.path.dirname(os.path.abspath(md_path))
            full_img_path = os.path.normpath(os.path.join(md_dir, img_rel_path))
            
            if not os.path.exists(full_img_path):
                alt_img = os.path.join(md_dir, "images", os.path.basename(img_rel_path))
                if os.path.exists(alt_img):
                    full_img_path = alt_img
            
            if os.path.exists(full_img_path):
                p_img = doc.add_paragraph()
                p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
                p_img.paragraph_format.space_before = Pt(14)
                p_img.paragraph_format.space_after = Pt(4)
                p_img.paragraph_format.keep_with_next = True
                run_img = p_img.add_run()
                run_img.add_picture(full_img_path, width=Inches(page_width_inches))
                
                if alt_text:
                    p_cap = doc.add_paragraph()
                    p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
                    p_cap.paragraph_format.space_before = Pt(2)
                    p_cap.paragraph_format.space_after = Pt(14)
                    p_cap.paragraph_format.keep_with_next = False
                    
                    cap_run = p_cap.add_run(f"▲ {alt_text}")
                    cap_run.font.bold = True
                    cap_run.font.size = Pt(9.5)
                    cap_run.font.name = "맑은 고딕"
                    cap_run.font.color.rgb = RGBColor(27, 54, 93)
                i += 1
                continue
            else:
                print(f"  [WARNING] Image file not found: {img_rel_path}")

        # 1. Check for Table Caption ([표 X-X] ...)
        if re.match(r'^(\[표\s*[^\]]+\]|■\s*표|▲\s*표)', stripped):
            p_cap = doc.add_paragraph()
            p_cap.paragraph_format.space_before = Pt(16)
            p_cap.paragraph_format.space_after = Pt(5)
            p_cap.paragraph_format.keep_with_next = True
            
            cap_run = p_cap.add_run(f"■ {clean_math_text(stripped)}")
            cap_run.font.bold = True
            cap_run.font.size = Pt(10.5)
            cap_run.font.name = "맑은 고딕"
            cap_run.font.color.rgb = RGBColor(27, 54, 93)
            i += 1
            continue

        # 2. Check for Math Formula Block ($$ ... $$)
        if stripped.startswith('$$'):
            if stripped.endswith('$$') and len(stripped) > 4:
                math_raw = stripped[2:-2].strip()
            else:
                math_lines = [stripped[2:].strip()]
                i += 1
                while i < len(lines):
                    m_line = lines[i].strip()
                    if m_line.endswith('$$'):
                        math_lines.append(m_line[:-2].strip())
                        break
                    math_lines.append(m_line)
                    i += 1
                math_raw = " ".join(math_lines)
            
            clean_math = clean_math_text(math_raw)
            
            tbl = doc.add_table(rows=1, cols=1)
            tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
            cell = tbl.cell(0, 0)
            cell.width = Inches(page_width_inches)
            set_cell_background(cell, "F8FAFC")
            set_cell_margins(cell, top=140, bottom=140, left=180, right=180)
            
            tcPr = cell._tc.get_or_add_tcPr()
            tcBorders = parse_xml(f'''
                <w:tcBorders {nsdecls("w")}>
                    <w:left w:val="single" w:sz="24" w:space="0" w:color="1B365D"/>
                    <w:top w:val="single" w:sz="4" w:space="0" w:color="CBD5E1"/>
                    <w:bottom w:val="single" w:sz="4" w:space="0" w:color="CBD5E1"/>
                    <w:right w:val="single" w:sz="4" w:space="0" w:color="CBD5E1"/>
                </w:tcBorders>
            ''')
            tcPr.append(tcBorders)
            
            cp = cell.paragraphs[0]
            cp.alignment = WD_ALIGN_PARAGRAPH.CENTER
            cp.paragraph_format.space_before = Pt(4)
            cp.paragraph_format.space_after = Pt(4)
            crun = cp.add_run(clean_math)
            crun.font.name = '맑은 고딕'
            crun.font.size = Pt(11)
            crun.font.bold = True
            crun.font.color.rgb = RGBColor(27, 54, 93)
            doc.add_paragraph()
            i += 1
            continue

        # 3. Check for Code Block (```)
        if stripped.startswith('```') or stripped == '`':
            code_type = stripped[3:].strip() if stripped.startswith('```') else ''
            code_lines = []
            i += 1
            while i < len(lines):
                cur_line = lines[i].strip()
                if cur_line.startswith('```') or (stripped == '`' and cur_line == '`'):
                    break
                code_lines.append(lines[i])
                i += 1
            i += 1

            code_text = "\n".join(code_lines)
            tbl = doc.add_table(rows=1, cols=1)
            tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
            cell = tbl.cell(0, 0)
            cell.width = Inches(page_width_inches)
            
            set_cell_background(cell, "F8FAFC")
            set_cell_margins(cell, top=140, bottom=140, left=180, right=180)
            
            tcPr = cell._tc.get_or_add_tcPr()
            tcBorders = parse_xml(f'''
                <w:tcBorders {nsdecls("w")}>
                    <w:left w:val="single" w:sz="24" w:space="0" w:color="1B365D"/>
                    <w:top w:val="single" w:sz="4" w:space="0" w:color="E2E8F0"/>
                    <w:bottom w:val="single" w:sz="4" w:space="0" w:color="E2E8F0"/>
                    <w:right w:val="single" w:sz="4" w:space="0" w:color="E2E8F0"/>
                </w:tcBorders>
            ''')
            tcPr.append(tcBorders)

            cp = cell.paragraphs[0]
            cp.paragraph_format.space_before = Pt(3)
            cp.paragraph_format.space_after = Pt(3)
            crun = cp.add_run(code_text.strip())
            crun.font.name = 'Consolas'
            crun.font.size = Pt(8.5)
            crun.font.color.rgb = RGBColor(15, 23, 42)
            doc.add_paragraph()
            continue

        # 4. Check for Table (| ... |)
        if stripped.startswith('|') and stripped.endswith('|'):
            table_rows = []
            while i < len(lines) and lines[i].strip().startswith('|') and lines[i].strip().endswith('|'):
                tline = lines[i].strip()
                parts = [p.strip() for p in tline.split('|')[1:-1]]
                if all(re.match(r'^:?-+:?$', p) for p in parts if p):
                    i += 1
                    continue
                table_rows.append(parts)
                i += 1

            if table_rows:
                # If the first row was an accidental single title row with empty trailing cells, extract it as caption
                if len(table_rows) > 1 and len(table_rows[0]) > 0 and all(c == '' for c in table_rows[0][1:]):
                    title_text = table_rows[0][0]
                    p = doc.add_paragraph()
                    p.paragraph_format.space_before = Pt(16)
                    p.paragraph_format.space_after = Pt(5)
                    p.paragraph_format.keep_with_next = True
                    run = p.add_run(f"■ {title_text}")
                    run.font.bold = True
                    run.font.size = Pt(10.5)
                    run.font.name = "맑은 고딕"
                    run.font.color.rgb = RGBColor(27, 54, 93)
                    table_rows = table_rows[1:]

                num_cols = max(len(r) for r in table_rows)
                # Pad all rows to num_cols
                for r in table_rows:
                    while len(r) < num_cols:
                        r.append("")

                tbl = doc.add_table(rows=len(table_rows), cols=num_cols)
                tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
                set_table_borders(tbl, "CBD5E1")

                col_widths = calculate_column_widths(table_rows, page_width_inches)

                for r_idx, r_data in enumerate(table_rows):
                    row = tbl.rows[r_idx]
                    make_row_cant_split(row)
                    is_header = (r_idx == 0)
                    if is_header:
                        make_row_header(row)

                    row_text_joined = " ".join(r_data)
                    is_summary_row = not is_header and any(k in row_text_joined for k in ['소계', '총계', '합계', '총투자비용', '종합 결과'])

                    for c_idx in range(num_cols):
                        cell = row.cells[c_idx]
                        cell.width = col_widths[c_idx]
                        cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
                        set_cell_margins(cell, top=100, bottom=100, left=120, right=120)
                        
                        if is_header:
                            set_cell_background(cell, "1B365D") # Dark Navy Header
                        elif is_summary_row:
                            set_cell_background(cell, "E2E8F0") # Accent Slate Shading for Totals
                        elif r_idx % 2 == 1:
                            set_cell_background(cell, "FFFFFF")
                        else:
                            set_cell_background(cell, "F8FAFC") # Subtle Zebra Shading

                        val = r_data[c_idx]
                        val_clean = clean_math_text(val.replace('•', '·'))
                        
                        cell_lines = val_clean.split('<br>')
                        
                        for p_i, line_text in enumerate(cell_lines):
                            if p_i == 0:
                                p = cell.paragraphs[0]
                            else:
                                p = cell.add_paragraph()
                                
                            p.paragraph_format.space_before = Pt(1)
                            p.paragraph_format.space_after = Pt(1)
                            p.paragraph_format.line_spacing = 1.15

                            # Handle bullet points
                            line_str = line_text.strip()
                            if line_str.startswith('·') or line_str.startswith('-'):
                                p.paragraph_format.left_indent = Inches(0.12)
                            
                            parts = re.split(r'(\*\*.*?\*\*)', line_str)
                            for part in parts:
                                if not part:
                                    continue
                                if part.startswith('**') and part.endswith('**'):
                                    run = p.add_run(part[2:-2])
                                    run.font.bold = True
                                else:
                                    run = p.add_run(part)
                                
                                run.font.name = '맑은 고딕'
                                if is_header:
                                    run.font.bold = True
                                    run.font.size = Pt(9.5)
                                    run.font.color.rgb = RGBColor(255, 255, 255)
                                elif is_summary_row:
                                    run.font.bold = True
                                    run.font.size = Pt(9)
                                    run.font.color.rgb = RGBColor(27, 54, 93)
                                else:
                                    run.font.size = Pt(9)
                                    run.font.color.rgb = RGBColor(30, 41, 59)

                doc.add_paragraph()
            continue

        # 5. Headings
        if stripped.startswith('# '):
            p = doc.add_paragraph()
            p.paragraph_format.space_before = Pt(22)
            p.paragraph_format.space_after = Pt(10)
            p.paragraph_format.keep_with_next = True
            run = p.add_run(clean_math_text(stripped[2:].strip()))
            run.font.bold = True
            run.font.size = Pt(18)
            run.font.color.rgb = RGBColor(27, 54, 93)
            run.font.name = '맑은 고딕'
        elif stripped.startswith('## '):
            p = doc.add_paragraph()
            p.paragraph_format.space_before = Pt(18)
            p.paragraph_format.space_after = Pt(8)
            p.paragraph_format.keep_with_next = True
            run = p.add_run(clean_math_text(stripped[3:].strip()))
            run.font.bold = True
            run.font.size = Pt(14)
            run.font.color.rgb = RGBColor(43, 84, 126)
            run.font.name = '맑은 고딕'
        elif stripped.startswith('### '):
            p = doc.add_paragraph()
            p.paragraph_format.space_before = Pt(14)
            p.paragraph_format.space_after = Pt(6)
            p.paragraph_format.keep_with_next = True
            run = p.add_run(clean_math_text(stripped[4:].strip()))
            run.font.bold = True
            run.font.size = Pt(11.5)
            run.font.color.rgb = RGBColor(30, 41, 59)
            run.font.name = '맑은 고딕'
        elif stripped.startswith('#### '):
            p = doc.add_paragraph()
            p.paragraph_format.space_before = Pt(10)
            p.paragraph_format.space_after = Pt(4)
            p.paragraph_format.keep_with_next = True
            run = p.add_run(clean_math_text(stripped[5:].strip()))
            run.font.bold = True
            run.font.size = Pt(10.5)
            run.font.color.rgb = RGBColor(51, 65, 85)
            run.font.name = '맑은 고딕'
        elif stripped.startswith('> '):
            alert_text = clean_math_text(stripped[2:].replace('[!IMPORTANT]', '★ [중요]').replace('[!NOTE]', '■ [참고]'))
            tbl = doc.add_table(rows=1, cols=1)
            tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
            cell = tbl.cell(0, 0)
            cell.width = Inches(page_width_inches)
            set_cell_background(cell, "EFF6FF")
            set_cell_margins(cell, top=100, bottom=100, left=150, right=150)
            tcPr = cell._tc.get_or_add_tcPr()
            tcBorders = parse_xml(f'''
                <w:tcBorders {nsdecls("w")}>
                    <w:left w:val="single" w:sz="18" w:space="0" w:color="2563EB"/>
                    <w:top w:val="none"/>
                    <w:bottom w:val="none"/>
                    <w:right w:val="none"/>
                </w:tcBorders>
            ''')
            tcPr.append(tcBorders)
            cp = cell.paragraphs[0]
            cp.paragraph_format.space_before = Pt(2)
            cp.paragraph_format.space_after = Pt(2)
            crun = cp.add_run(alert_text.strip())
            crun.font.size = Pt(9.5)
            crun.font.color.rgb = RGBColor(30, 58, 138)
            crun.font.name = '맑은 고딕'
            doc.add_paragraph()
        else:
            p = doc.add_paragraph()
            p.paragraph_format.space_before = Pt(2)
            p.paragraph_format.space_after = Pt(3)
            p.paragraph_format.line_spacing = 1.25

            content = clean_math_text(stripped)
            if content.startswith('- ') or content.startswith('* '):
                p.paragraph_format.left_indent = Inches(0.2)
                content = "• " + content[2:]
            elif re.match(r'^\d+\.\s', content):
                p.paragraph_format.left_indent = Inches(0.2)

            parts = re.split(r'(\*\*.*?\*\*)', content)
            for part in parts:
                if not part:
                    continue
                if part.startswith('**') and part.endswith('**'):
                    run = p.add_run(part[2:-2])
                    run.font.bold = True
                    run.font.color.rgb = RGBColor(15, 23, 42)
                else:
                    run = p.add_run(part)
                run.font.name = '맑은 고딕'
                run.font.size = Pt(10)

        i += 1

    try:
        doc.save(docx_path)
        print(f"[SUCCESS] Saved: {docx_path}")
    except PermissionError:
        alt_path = docx_path.replace(".docx", "_완성본.docx")
        doc.save(alt_path)
        print(f"[WARNING] Original locked by Word, saved to: {alt_path}")
        return alt_path
    return docx_path

if __name__ == "__main__":
    base_dir = r"c:\Users\immnu\Desktop\Claud\OnyuwolKorea\프로젝트 팀\국가재난_긴급_유무선_통합통신시스템_컨설팅\04_산출물"
    
    # 1. 요약본 변환
    sum_md = os.path.join(base_dir, "요약본.md")
    for sum_name in ["국가재난_긴급_유무선_통합통신시스템_구축컨설팅_요약본.docx", 
                     "국가재난_긴급_유무선_통합통신시스템_구축컨설팅_마스터요약본_완성본.docx"]:
        sum_docx = os.path.join(base_dir, sum_name)
        build_docx_from_markdown(sum_md, sum_docx, "국가재난 긴급 유무선 통합 통신 시스템 구축 컨설팅 [요약본]")

    # 2. 본보고서 종합본 변환
    main_md = os.path.join(base_dir, "본보고서_종합.md")
    for main_name in ["국가재난_긴급_유무선_통합통신시스템_구축컨설팅_본보고서_종합.docx", 
                      "국가재난_긴급_유무선_통합통신시스템_구축컨설팅_마스터본보고서_완성본.docx"]:
        main_docx = os.path.join(base_dir, main_name)
        build_docx_from_markdown(main_md, main_docx, "국가재난 긴급 유무선 통합 통신 시스템 구축 컨설팅 [본보고서]")
