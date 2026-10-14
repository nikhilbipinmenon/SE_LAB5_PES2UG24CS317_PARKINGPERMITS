import sys
import os
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle, PageBreak, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super(NumberedCanvas, self).__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super(NumberedCanvas, self).showPage()
        super(NumberedCanvas, self).save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#5E6C84"))
        
        # Header
        if self._pageNumber > 1:
            self.drawString(54, 802, "PES University | CSE Dept | SE Lab (UE23CS252A) — Lab 5 Static Code Analysis")
            self.drawRightString(541, 802, "Topic: Parking Permits | SRN: PES2UG24CS317")
            self.setStrokeColor(colors.HexColor("#DFE1E6"))
            self.setLineWidth(0.5)
            self.line(54, 796, 541, 796)

        # Footer
        self.drawRightString(541, 30, f"Page {self._pageNumber} of {page_count}")
        self.drawString(54, 30, "Confidential — Academic Laboratory Deliverable | PES2UG24CS317 (Nikhil B Menon)")
        self.setStrokeColor(colors.HexColor("#DFE1E6"))
        self.setLineWidth(0.5)
        self.line(54, 40, 541, 40)
        self.restoreState()

def build_pdf(before_img="/Users/nikhilbmenon/Sem 5 Labs/SE Lab/L5_10_parking_permits/screenshot_before_analysis.png", 
              after_img="/Users/nikhilbmenon/Sem 5 Labs/SE Lab/L5_10_parking_permits/screenshot_after_analysis.png"):
    pdf_path = "/Users/nikhilbmenon/Sem 5 Labs/SE Lab/L5_10_parking_permits/Lab5_Static_Code_Analysis_Report.pdf"
    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=A4,
        leftMargin=48,
        rightMargin=48,
        topMargin=46,
        bottomMargin=46
    )

    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle('DocTitle', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=15, leading=19, textColor=colors.HexColor('#0052CC'), spaceAfter=3)
    sub_title_style = ParagraphStyle('DocSubTitle', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=10, leading=13, textColor=colors.HexColor('#172B4D'), spaceAfter=4)
    h1_style = ParagraphStyle('H1', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=11, leading=14, textColor=colors.HexColor('#0052CC'), spaceBefore=6, spaceAfter=4, keepWithNext=True)
    body_style = ParagraphStyle('Body', parent=styles['Normal'], fontName='Helvetica', fontSize=8, leading=11, textColor=colors.HexColor('#172B4D'), spaceAfter=3)
    caption_style = ParagraphStyle('Caption', parent=styles['Normal'], fontName='Helvetica-Oblique', fontSize=7.5, leading=9.5, textColor=colors.HexColor('#5E6C84'), alignment=1, spaceAfter=5)
    
    th_style = ParagraphStyle('TH', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=7.5, leading=9.5, textColor=colors.white)
    td_style = ParagraphStyle('TD', parent=styles['Normal'], fontName='Helvetica', fontSize=7, leading=9, textColor=colors.HexColor('#172B4D'))
    td_bold = ParagraphStyle('TDBold', parent=td_style, fontName='Helvetica-Bold')

    story = []

    # Academic Header
    hdr = Table([[
        Paragraph("<b>PES UNIVERSITY</b><br/>Department of Computer Science & Engineering<br/>Software Engineering Laboratory (UE23CS252A) — Academic Year 2026-2027", ParagraphStyle('H1', parent=body_style, fontSize=8.5, leading=11, textColor=colors.HexColor('#0052CC'))),
        Paragraph("<b>Lab 5: Static Code Analysis</b><br/><b>Student:</b> Nikhil B Menon<br/><b>SRN:</b> PES2UG24CS317", ParagraphStyle('H2', parent=body_style, fontSize=8, leading=11, alignment=2, textColor=colors.HexColor('#172B4D')))
    ]], colWidths=[315, 184])
    hdr.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
        ('TOPPADDING', (0,0), (-1,-1), 0),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
    ]))
    story.append(hdr)
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#0052CC'), spaceAfter=5, spaceBefore=2))

    story.append(Paragraph("Lab 5: Static Code Analysis — Campus Parking Permit Manager", title_style))
    story.append(Paragraph("Automated Defect Detection, Security Audit, Refactoring & Verification via Pylint, Bandit, and Flake8", sub_title_style))
    story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor('#DFE1E6'), spaceAfter=5, spaceBefore=2))

    # Executive Metrics Summary
    summary_data = [
        [Paragraph("Tool", th_style), Paragraph("Initial State (PRE / Before Fixes)", th_style), Paragraph("Final Cleaned State (POST / After Fixes)", th_style), Paragraph("Status", th_style)],
        [Paragraph("<b>Pylint</b>", td_bold), Paragraph("Score: <b>6.32 / 10</b> (Mutable args, bare excepts, missing docstrings, global state)", td_style), Paragraph("Score: <b>10.00 / 10</b> (+3.68 improvement, zero defects)", td_style), Paragraph("<b>PASSED (10/10)</b>", td_bold)],
        [Paragraph("<b>Bandit</b>", td_bold), Paragraph("<b>2 Security Issues</b> (B311: Insecure PRNG, B110: Try-except-pass)", td_style), Paragraph("<b>No issues identified</b> (0 High, 0 Medium, 0 Low)", td_style), Paragraph("<b>PASSED (Clean)</b>", td_bold)],
        [Paragraph("<b>Flake8</b>", td_bold), Paragraph("<b>8 Style Errors</b> (E302 spacing, E501 line length >79 chars, E722 bare excepts)", td_style), Paragraph("<b>0 Errors / 0 Warnings</b> (100% PEP 8 compliant)", td_style), Paragraph("<b>PASSED (Clean)</b>", td_bold)],
    ]
    t_sum = Table(summary_data, colWidths=[60, 180, 180, 79])
    t_sum.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#0052CC')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#DFE1E6')),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.HexColor('#FFFFFF'), colors.HexColor('#F4F5F7')]),
    ]))
    story.append(t_sum)
    story.append(Spacer(1, 4))

    # Section 1: Issues Table
    story.append(Paragraph("1. Issues Documentation Log (From issues.md)", h1_style))
    issues_table_data = [
        [Paragraph("Defect", th_style), Paragraph("Type & Tool", th_style), Paragraph("Line", th_style), Paragraph("Description", th_style), Paragraph("Fix Approach", th_style)],
        [
            Paragraph("<b>Insecure PRNG</b>", td_bold),
            Paragraph("Security (Bandit B311)", td_style),
            Paragraph("11", td_style),
            Paragraph("Using <code>random.randint()</code> for permit IDs is cryptographically predictable.", td_style),
            Paragraph("Replaced with secure <code>secrets.randbelow(90000) + 10000</code>.", td_style)
        ],
        [
            Paragraph("<b>Bare Except</b>", td_bold),
            Paragraph("Security (Bandit B110 / Pylint W0702 / Flake8 E722)", td_style),
            Paragraph("22", td_style),
            Paragraph("Bare <code>except: pass</code> silently conceals critical runtime exceptions.", td_style),
            Paragraph("Replaced with atomic <code>permits.pop()</code> and specific handlers.", td_style)
        ],
        [
            Paragraph("<b>Mutable Default</b>", td_bold),
            Paragraph("Bug (Pylint W0102)", td_style),
            Paragraph("9", td_style),
            Paragraph("<code>zone_records=[]</code> retains list mutations across multiple calls.", td_style),
            Paragraph("Default set to <code>None</code>; initialized inside method.", td_style)
        ],
        [
            Paragraph("<b>Unclosed File</b>", td_bold),
            Paragraph("Resource Leak (Pylint R1732 / W1514)", td_style),
            Paragraph("42, 47", td_style),
            Paragraph("Calling <code>open()</code> without context manager risks leaks; missing UTF-8.", td_style),
            Paragraph("Refactored to <code>with open(file, mode, encoding='utf-8') as f:</code>.", td_style)
        ],
        [
            Paragraph("<b>Global State</b>", td_bold),
            Paragraph("Code Smell (Pylint W0603)", td_style),
            Paragraph("40", td_style),
            Paragraph("Function mutated <code>global permits</code>, breaking encapsulation.", td_style),
            Paragraph("Updated in-place via <code>permits.clear()</code> and <code>permits.update()</code>.", td_style)
        ],
        [
            Paragraph("<b>Naming Style</b>", td_bold),
            Paragraph("Style (Pylint C0103)", td_style),
            Paragraph("51", td_style),
            Paragraph("Function <code>setExpiry</code> used camelCase instead of PEP 8 snake_case.", td_style),
            Paragraph("Renamed to <code>set_expiry</code> with backward-compatible alias.", td_style)
        ],
        [
            Paragraph("<b>Missing Docs</b>", td_bold),
            Paragraph("Convention (Pylint C0114 / C0116)", td_style),
            Paragraph("Module", td_style),
            Paragraph("Module and 7 functions lacked docstrings explaining behavior & params.", td_style),
            Paragraph("Added comprehensive PEP 257 compliant docstrings to all methods.", td_style)
        ],
        [
            Paragraph("<b>PEP 8 Format</b>", td_bold),
            Paragraph("Style (Flake8 E302 / E501)", td_style),
            Paragraph("Various", td_style),
            Paragraph("Lines exceeded 79 characters; single blank line instead of two.", td_style),
            Paragraph("Formatted spacing to PEP 8 standards and wrapped long lines.", td_style)
        ],
        [
            Paragraph("<b>Logic Bugs</b>", td_bold),
            Paragraph("Domain Logic Bug", td_style),
            Paragraph("56–60", td_style),
            Paragraph("Accepted empty plates and invalid zones; expiry crashed on <code>%d/%m/%Y</code>.", td_style),
            Paragraph("Added plate sanitization, zone membership check, and date parsing.", td_style)
        ]
    ]
    t_issues = Table(issues_table_data, colWidths=[68, 85, 26, 160, 160])
    t_issues.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#0052CC')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#DFE1E6')),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING', (0,0), (-1,-1), 2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.HexColor('#FFFFFF'), colors.HexColor('#F4F5F7')]),
    ]))
    story.append(t_issues)

    # PAGE 2: The Two Terminal Screenshots
    story.append(PageBreak())
    story.append(Paragraph("2. Terminal Verification Screenshots: PRE and POST Static Analysis Runs", h1_style))
    story.append(Paragraph("<b>Figure 1: PRE-Analysis Terminal Run (Before Fixes)</b> — Initial static code audit on uncleaned starter code, displaying Bandit security detection (B110 Try-except-pass, Low severity: 2), and Flake8 style violations (E302 spacing, E501 line length >79 chars, E722 bare excepts):", body_style))
    if os.path.exists(before_img):
        # 1024x712 -> scale to width 440, height 306
        story.append(Image(before_img, width=440, height=306))
    story.append(Paragraph("Figure 1: Live terminal capture of PRE-analysis run on initial code showing security and style defects.", caption_style))
    story.append(Spacer(1, 4))

    story.append(Paragraph("<b>Figure 2: POST-Analysis Terminal Run (After Fixes)</b> — Rerun on refactored code demonstrating Pylint rated at a perfect <b>10.00/10</b> (+3.68 score improvement), Bandit finding <b>0 vulnerabilities</b>, Flake8 exiting completely clean, and valid Python execution:", body_style))
    if os.path.exists(after_img):
        # 1024x582 -> scale to width 440, height 250
        story.append(Image(after_img, width=440, height=250))
    story.append(Paragraph("Figure 2: Live terminal capture of POST-analysis run showing verified clean code (Pylint 10.00/10, Bandit clean).", caption_style))

    # PAGE 3: Reflection Questions
    story.append(PageBreak())
    story.append(Paragraph("3. Answers to Lab Reflection Questions (From reflection.md)", h1_style))

    def make_q_box(q_num, q_title, q_full, a_text):
        content = [
            Paragraph(f"<b>{q_num}: {q_title}</b>", ParagraphStyle('QT', parent=body_style, fontName='Helvetica-Bold', textColor=colors.HexColor('#0052CC'), fontSize=8.5, leading=11, spaceAfter=2)),
            Paragraph(f"<i>Q: {q_full}</i>", ParagraphStyle('QF', parent=body_style, fontName='Helvetica-Oblique', fontSize=7.2, leading=9.5, textColor=colors.HexColor('#5E6C84'), spaceAfter=3)),
            Paragraph(a_text, ParagraphStyle('A', parent=body_style, fontSize=7.8, leading=11, textColor=colors.HexColor('#172B4D')))
        ]
        t = Table([[content]], colWidths=[499])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F4F5F7')),
            ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#0052CC')),
            ('LEFTPADDING', (0,0), (-1,-1), 9),
            ('RIGHTPADDING', (0,0), (-1,-1), 9),
            ('TOPPADDING', (0,0), (-1,-1), 6),
            ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ]))
        return t

    story.append(make_q_box(
        "Reflection Question 1", "Tool Comparison & Effectiveness",
        "Which tool (Pylint, Flake8, or Bandit) found the most critical or actionable issues, and why?",
        "<b>Bandit</b> and <b>Pylint</b> uncovered the most critical and actionable issues. <b>Bandit</b> flagged high-impact security vulnerabilities: <code>B311</code> (insecure pseudo-random number generation for parking permits, exposing predictable credentials) and <code>B110</code> (bare <code>except: pass</code> suppressing errors). <b>Pylint</b> detected an insidious Python logic bug: the <b>mutable default argument</b> (<code>zone_records=[]</code>), which causes cross-invocation state leakage across calls. <b>Flake8</b> was essential for enforcing PEP 8 style formatting."
    ))
    story.append(Spacer(1, 6))

    story.append(make_q_box(
        "Reflection Question 2", "Contribution to Quality & Security",
        "How does static code analysis improve overall software quality, maintainability, and security before runtime or testing?",
        "Static code analysis enables <b>Shift-Left Quality and Security</b>. It acts as an automated first line of defense, discovering latent memory/resource leaks (unclosed file handles), type errors, and cryptographic weaknesses without executing code or waiting for runtime production failures. Furthermore, enforcing strict conventions (PEP 8) ensures readability and long-term codebase maintainability across multi-engineer teams."
    ))
    story.append(Spacer(1, 6))

    story.append(make_q_box(
        "Reflection Question 3", "Challenges and Limitations",
        "What challenges or limitations did you encounter with static analysis tools?",
        "Static analysis tools are <b>context-insensitive and cannot reason about business domain semantics</b>. While the tools flagged line lengths, naming styles, and library anti-patterns, they completely missed business logic bugs: the starter code accepted invalid parking zone 'Z', accepted empty strings <code>\"\"</code> or <code>None</code> as vehicle plates, and crashed on alternative date formats like <code>01/01/2020</code>. Thus, static analysis must always be paired with functional unit testing."
    ))
    story.append(Spacer(1, 6))

    story.append(make_q_box(
        "Reflection Question 4", "CI/CD Pipeline Integration",
        "How would you integrate static analysis tools into a continuous integration (CI/CD) pipeline for team development?",
        "In a CI/CD pipeline (e.g. GitHub Actions), static analysis tools run on every pull request as automated quality gates. Merges are blocked if Bandit flags High/Medium severity vulnerabilities or if the Pylint score falls below 9.0/10. Pre-commit hooks run Flake8 locally before committing, and findings are exported in SARIF format to the GitHub Security tab for centralized vulnerability tracking."
    ))

    doc.build(story, canvasmaker=NumberedCanvas)
    print("Lab 5 Deliverables PDF built successfully with user screenshots at:", pdf_path)

if __name__ == '__main__':
    build_pdf()
