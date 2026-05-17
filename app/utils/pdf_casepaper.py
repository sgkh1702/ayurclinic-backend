from pathlib import Path
from html import escape

from playwright.async_api import async_playwright

APP_DIR = Path(__file__).resolve().parent.parent
FONT_PATH = APP_DIR / "assets" / "fonts" / "NotoSansDevanagari-VariableFont_wdth,wght.ttf"
FONT_URI = FONT_PATH.resolve().as_uri()


def safe(value):
    if value is None:
        return ""
    return escape(str(value))


def field_row(label, value):
    shown = safe(value) if value not in [None, ""] else "-"
    return f"""
    <div class="row">
      <div class="label">{safe(label)}</div>
      <div class="value">{shown}</div>
    </div>
    """


def section_html(title, value):
    if not value:
        return ""
    return f"""
    <div class="section">
      <div class="section-title">{safe(title)}</div>
      <div class="section-body">{safe(value)}</div>
    </div>
    """


def base_style():
    return f"""
    <style>
      @font-face {{
        font-family: 'NotoSansDevanagari';
        src: url('{FONT_URI}') format('truetype');
      }}

      body {{
        font-family: 'NotoSansDevanagari', sans-serif;
        font-size: 13px;
        color: #111;
        line-height: 1.5;
        margin: 0;
        padding: 0;
      }}

      .page {{
        padding: 18px 22px;
      }}

      .clinic-title {{
        font-size: 24px;
        font-weight: 700;
        margin-bottom: 12px;
      }}

      .sub-title {{
        font-size: 16px;
        font-weight: 700;
        margin-top: 14px;
        margin-bottom: 8px;
        border-bottom: 1px solid #999;
        padding-bottom: 4px;
      }}

      .row {{
        display: flex;
        margin-bottom: 4px;
      }}

      .label {{
        width: 180px;
        font-weight: 700;
        flex-shrink: 0;
      }}

      .value {{
        flex: 1;
      }}

      .section {{
        margin-top: 10px;
        margin-bottom: 10px;
        break-inside: avoid;
      }}

      .section-title {{
        font-weight: 700;
        margin-bottom: 4px;
      }}

      .section-body {{
        white-space: pre-wrap;
        border: 1px solid #ccc;
        padding: 8px;
        border-radius: 4px;
      }}

      .visit-block {{
        margin-top: 18px;
        padding-top: 10px;
        border-top: 2px solid #666;
        break-inside: avoid;
      }}

      .visit-heading {{
        font-size: 15px;
        font-weight: 700;
        margin-bottom: 8px;
      }}
    </style>
    """


def build_visit_html(patient, visit):
    return f"""
    <html>
      <head>
        <meta charset="utf-8">
        {base_style()}
      </head>
      <body>
        <div class="page">
          <div class="clinic-title">चन्द्रमां चिकित्सालय आणि पंचकर्म केंद्र</div>

          <div class="sub-title">Patient Master / रुग्ण माहिती</div>
          {field_row("नाव:", patient.patient_name)}
          {field_row("मोबाईल:", patient.mobile)}
          {field_row("ईमेल:", patient.email)}
          {field_row("वय:", patient.age)}
          {field_row("वजन:", patient.weight)}
          {field_row("लिंग:", patient.gender)}
          {field_row("जन्मदिनांक:", patient.birth_date)}
          {field_row("वेळ:", patient.birth_time)}
          {field_row("शिक्षण:", patient.education)}
          {field_row("व्यवसाय:", patient.occupation)}
          {field_row("पत्ता:", patient.address)}

          {section_html("कौटुंबिक इतिहास / Family History", patient.family_history)}
          {section_html("दिनचर्या / Routine", patient.baseline_notes)}

          <div class="sub-title">केस पेपर / Visit Details</div>
          {field_row("Visit ID:", visit.id)}
          {field_row("Case No:", visit.case_no)}
          {field_row("Visit Date:", visit.visit_date)}
          {field_row("Ref. By:", visit.ref_by)}
          {field_row("Next Follow-up:", visit.next_followup_date)}

          {section_html("तक्रारी / Symptoms", visit.symptoms)}
          {section_html("पूर्वीचे उपचार / Previous Treatment", visit.previous_treatment)}
          {section_html("नोंदी / Notes", visit.notes)}
          {section_html("निदान / Diagnosis", visit.diagnosis)}
          {section_html("सल्ला / Advice", visit.advice)}
          {section_html("औषधे / Prescription", visit.prescription)}
          {section_html("फॉलोअप नोंदी / Follow-up Notes", visit.followup_notes)}
        </div>
      </body>
    </html>
    """


def build_patient_history_html(patient, visits):
    visit_blocks = []

    for visit in visits:
        visit_blocks.append(f"""
        <div class="visit-block">
          <div class="visit-heading">Visit #{safe(visit.id)} | Date: {safe(visit.visit_date)}</div>
          {field_row("Case No:", visit.case_no)}
          {field_row("Ref. By:", visit.ref_by)}
          {field_row("Next Follow-up:", visit.next_followup_date)}

          {section_html("तक्रारी / Symptoms", visit.symptoms)}
          {section_html("पूर्वीचे उपचार / Previous Treatment", visit.previous_treatment)}
          {section_html("नोंदी / Notes", visit.notes)}
          {section_html("निदान / Diagnosis", visit.diagnosis)}
          {section_html("सल्ला / Advice", visit.advice)}
          {section_html("औषधे / Prescription", visit.prescription)}
          {section_html("फॉलोअप नोंदी / Follow-up Notes", visit.followup_notes)}
        </div>
        """)

    return f"""
    <html>
      <head>
        <meta charset="utf-8">
        {base_style()}
      </head>
      <body>
        <div class="page">
          <div class="clinic-title">चन्द्रमां चिकित्सालय आणि पंचकर्म केंद्र</div>

          <div class="sub-title">Consolidated Case Papers / सर्व जुने केस पेपर</div>
          {field_row("नाव:", patient.patient_name)}
          {field_row("मोबाईल:", patient.mobile)}
          {field_row("ईमेल:", patient.email)}
          {field_row("वय:", patient.age)}
          {field_row("वजन:", patient.weight)}
          {field_row("लिंग:", patient.gender)}
          {field_row("जन्मदिनांक:", patient.birth_date)}
          {field_row("वेळ:", patient.birth_time)}
          {field_row("शिक्षण:", patient.education)}
          {field_row("व्यवसाय:", patient.occupation)}
          {field_row("पत्ता:", patient.address)}

          {section_html("कौटुंबिक इतिहास / Family History", patient.family_history)}
          {section_html("दिनचर्या / Routine", patient.baseline_notes)}

          {''.join(visit_blocks)}
        </div>
      </body>
    </html>
    """


async def html_to_pdf_bytes(html: str) -> bytes:
    if not FONT_PATH.exists():
        raise FileNotFoundError(f"Font file not found: {FONT_PATH}")

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.set_content(html, wait_until="load")
        await page.evaluate("document.fonts.ready")
        pdf_bytes = await page.pdf(
            format="A4",
            print_background=True,
            margin={"top": "10mm", "right": "10mm", "bottom": "10mm", "left": "10mm"},
            prefer_css_page_size=True
        )
        await browser.close()
        return pdf_bytes


async def build_visit_pdf(patient, visit) -> bytes:
    html = build_visit_html(patient, visit)
    return await html_to_pdf_bytes(html)


async def build_patient_history_pdf(patient, visits) -> bytes:
    html = build_patient_history_html(patient, visits)
    return await html_to_pdf_bytes(html)