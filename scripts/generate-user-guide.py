"""Generate the static user handbook from the guide page's shared content."""
import json
import subprocess
from pathlib import Path
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Image

ROOT = Path(__file__).resolve().parents[1]
guide = json.loads((ROOT / "src/content/user-guide.json").read_text())
for name, family in [("GuideSans", "DejaVu Sans"), ("GuideBold", "DejaVu Sans:bold"), ("GuideSerif", "DejaVu Serif")]:
    path = subprocess.check_output(["fc-match", "-f", "%{file}", family], text=True).strip()
    pdfmetrics.registerFont(TTFont(name, path))

NAVY = colors.HexColor("#002868")
RED = colors.HexColor("#BF0A30")
INK = colors.HexColor("#151B26")
MUTED = colors.HexColor("#526071")
BORDER = colors.HexColor("#DDE3EB")
styles = {
    "eyebrow": ParagraphStyle("eyebrow", fontName="GuideBold", fontSize=9, leading=14, textColor=NAVY, spaceAfter=12),
    "cover": ParagraphStyle("cover", fontName="GuideSerif", fontSize=38, leading=45, textColor=INK, spaceAfter=20),
    "title": ParagraphStyle("title", fontName="GuideSerif", fontSize=23, leading=29, textColor=INK, spaceAfter=12),
    "summary": ParagraphStyle("summary", fontName="GuideSans", fontSize=11, leading=17, textColor=MUTED, spaceAfter=15),
    "body": ParagraphStyle("body", fontName="GuideSans", fontSize=9.5, leading=15, textColor=INK, spaceAfter=9),
    "step": ParagraphStyle("step", fontName="GuideSans", fontSize=9.5, leading=15, textColor=INK, leftIndent=20, firstLineIndent=-20, spaceAfter=9),
    "note": ParagraphStyle("note", fontName="GuideSans", fontSize=9, leading=14, textColor=MUTED, borderColor=BORDER, borderWidth=0.5, borderPadding=10, spaceBefore=8, spaceAfter=16),
    "toc": ParagraphStyle("toc", fontName="GuideSans", fontSize=10, leading=17, textColor=INK, spaceAfter=6),
}
output = ROOT / "public/downloads/american-corner-kamenge-user-guide.pdf"
output.parent.mkdir(parents=True, exist_ok=True)
doc = SimpleDocTemplate(str(output), pagesize=A4, rightMargin=48, leftMargin=48, topMargin=66, bottomMargin=54,
                        title="American Corner Kamenge — User Guide", author="American Corner Kamenge", pageCompression=1)

def chrome(canvas, document):
    width, height = A4
    canvas.saveState()
    canvas.setFillColor(NAVY)
    canvas.rect(0, height-6, width*2/3, 6, fill=1, stroke=0)
    canvas.setFillColor(RED)
    canvas.rect(width*2/3, height-6, width/3, 6, fill=1, stroke=0)
    canvas.setFont("GuideBold", 8)
    canvas.setFillColor(NAVY)
    canvas.drawString(48, height-35, guide["organization"].upper())
    canvas.setFont("GuideSans", 8)
    canvas.setFillColor(MUTED)
    canvas.drawRightString(width-48, height-35, "USER GUIDE")
    canvas.setStrokeColor(BORDER)
    canvas.line(48, 40, width-48, 40)
    canvas.setFont("GuideSans", 7)
    canvas.drawString(48, 26, "© 2026 American Corner Kamenge · Made with love by Freeti")
    canvas.linkURL("https://www.freeti.org", (48, 21, 365, 34), relative=0)
    canvas.drawRightString(width-48, 26, f"{document.page} / 6")
    canvas.restoreState()

story = [Spacer(1, 18), Image(str(ROOT / "public/logo-gss.png"), width=60, height=60, kind="proportional", hAlign="LEFT"), Spacer(1, 28),
         Paragraph("STAFF HANDBOOK · " + guide["edition"].upper(), styles["eyebrow"]),
         Paragraph("American Corner<br/>Kamenge", styles["cover"]),
         Paragraph("User Guide", styles["title"]), Paragraph(guide["subtitle"], styles["summary"]), Spacer(1, 22),
         Paragraph("IN THIS GUIDE", styles["eyebrow"])]
for i, section in enumerate(guide["sections"]):
    page = 2 + i//2
    story.append(Paragraph(f"{i+1:02d} &nbsp; {escape(section['title'])} <font color='#526071'>· {page}</font>", styles["toc"]))
story.extend([Spacer(1, 16), Paragraph("For staff using the member, center-visit and program-attendance tools. Administrator sections apply only to authorized accounts.", styles["summary"])])
for i, section in enumerate(guide["sections"]):
    if i % 2 == 0:
        story.append(PageBreak())
    else:
        story.append(Spacer(1, 18))
    story.append(Paragraph(f"{i+1:02d} / {escape(section['title'])}", styles["title"]))
    story.append(Paragraph(escape(section["summary"]), styles["summary"]))
    for j, step in enumerate(section["steps"]):
        story.append(Paragraph(f"<font name='GuideBold' color='#002868'>{j+1}.</font> &nbsp; {escape(step)}", styles["step"]))
    story.append(Paragraph("<font name='GuideBold'>Good to know</font><br/>" + escape(section["note"]), styles["note"]))
doc.build(story, onFirstPage=chrome, onLaterPages=chrome)
print(f"Generated {output.name} ({output.stat().st_size} bytes)")