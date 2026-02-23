from flask import Flask, render_template, request, session, send_file
import config
from utils import CREDIT_RISK_ASSESMENT
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_LEFT
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from datetime import datetime

app = Flask(__name__)
app.config["SECRET_KEY"] = config.SECRET_KEY

REPORT_LABELS = {
    "person_age": "Age",
    "person_income": "Income",
    "person_home_ownership": "Home Ownership",
    "person_emp_length": "Employment Length (years)",
    "loan_intent": "Loan Intent",
    "loan_grade": "Loan Grade",
    "loan_amnt": "Loan Amount",
    "loan_int_rate": "Loan Interest Rate (%)",
    "loan_percent_income": "Loan % of Income",
    "cb_person_default_on_file": "Default on File",
    "cb_person_cred_hist_length": "Credit History Length (years)",
}


@app.route("/")
def get_home():
    return render_template("html1.html")


@app.route("/Predict", methods=["POST"])
def home():
    person_age = int(request.form["person_age"])
    person_income = int(request.form["person_income"])
    person_home_ownership = request.form["person_home_ownership"]
    person_emp_length = int(request.form["person_emp_length"])
    loan_intent = request.form["loan_intent"]
    loan_grade = request.form["loan_grade"]
    loan_amnt = eval(request.form["loan_amnt"])
    loan_int_rate = eval(request.form["loan_int_rate"])
    loan_percent_income = eval(request.form["loan_percent_income"])
    cb_person_default_on_file = request.form["cb_person_default_on_file"]
    cb_person_cred_hist_length = eval(request.form["cb_person_cred_hist_length"])
    obj = CREDIT_RISK_ASSESMENT(
        person_age, person_income, person_home_ownership, person_emp_length,
        loan_intent, loan_grade, loan_amnt, loan_int_rate, loan_percent_income,
        cb_person_default_on_file, cb_person_cred_hist_length,
    )
    res1 = obj.get_Credit_Risk()

    inputs = {k: request.form.get(k, "") for k in REPORT_LABELS}
    session["report_inputs"] = inputs
    session["report_result"] = int(res1)

    return render_template("Final.html", data=res1, inputs=inputs)


@app.route("/download-report")
def download_report():
    inputs = session.get("report_inputs")
    result = session.get("report_result")
    if inputs is None or result is None:
        return "No report data. Submit the form first.", 404

    buf = BytesIO()
    doc = SimpleDocTemplate(
        buf, pagesize=letter,
        rightMargin=0.75 * inch, leftMargin=0.75 * inch,
        topMargin=0.6 * inch, bottomMargin=0.6 * inch,
    )
    styles = getSampleStyleSheet()

    brand = colors.HexColor("#355872")
    primary = colors.HexColor("#7AAACE")
    accent = colors.HexColor("#9CD5FF")
    cream = colors.HexColor("#F7F8F0")
    green = colors.HexColor("#0d9488")
    red = colors.HexColor("#b91c1c")

    title_style = ParagraphStyle(
        name="ReportTitle",
        parent=styles["Heading1"],
        fontSize=22,
        textColor=brand,
        spaceAfter=4,
        fontName="Helvetica-Bold",
    )
    subtitle_style = ParagraphStyle(
        name="ReportSubtitle",
        parent=styles["Normal"],
        fontSize=9,
        textColor=colors.HexColor("#64748b"),
        spaceAfter=24,
    )
    section_style = ParagraphStyle(
        name="SectionHead",
        parent=styles["Heading2"],
        fontSize=12,
        textColor=brand,
        fontName="Helvetica-Bold",
        spaceBefore=16,
        spaceAfter=10,
        alignment=TA_LEFT,
    )

    story = []

    story.append(Paragraph("Credit Risk Assessment", title_style))
    story.append(Paragraph(f"Report generated on {datetime.now().strftime('%B %d, %Y at %I:%M %p')}", subtitle_style))

    story.append(Paragraph("Applicant details", section_style))
    table_data = [["Field", "Value"]]
    for key, label in REPORT_LABELS.items():
        value = inputs.get(key, "")
        table_data.append([label, str(value)])
    t = Table(table_data, colWidths=[2.6 * inch, 3.4 * inch])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), brand),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, 0), 11),
        ("TOPPADDING", (0, 0), (-1, 0), 12),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
        ("LEFTPADDING", (0, 0), (-1, -1), 14),
        ("RIGHTPADDING", (0, 0), (-1, -1), 14),
        ("BACKGROUND", (0, 1), (-1, -1), cream),
        ("TEXTCOLOR", (0, 1), (-1, -1), brand),
        ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
        ("FONTSIZE", (0, 1), (-1, -1), 10),
        ("TOPPADDING", (0, 1), (-1, -1), 10),
        ("BOTTOMPADDING", (0, 1), (-1, -1), 10),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [cream, colors.white]),
        ("LINEBELOW", (0, 0), (-1, 0), 0, colors.white),
        ("BOX", (0, 0), (-1, -1), 0.5, accent),
        ("INNERGRID", (0, 0), (-1, -1), 0.25, accent),
    ]))
    story.append(t)
    story.append(Spacer(1, 0.35 * inch))

    story.append(Paragraph("Assessment of risk", section_style))
    outcome_text = "Non-Default — Low credit risk" if result == 0 else "Default — High credit risk"
    outcome_color = green if result == 0 else red
    outcome_data = [[outcome_text]]
    outcome_table = Table(outcome_data, colWidths=[6 * inch])
    outcome_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), accent),
        ("TEXTCOLOR", (0, 0), (-1, -1), outcome_color),
        ("FONTNAME", (0, 0), (-1, -1), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 12),
        ("TOPPADDING", (0, 0), (-1, -1), 14),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 14),
        ("LEFTPADDING", (0, 0), (-1, -1), 16),
        ("RIGHTPADDING", (0, 0), (-1, -1), 16),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("BOX", (0, 0), (-1, -1), 1, primary),
    ]))
    story.append(outcome_table)
    story.append(Spacer(1, 0.25 * inch))

    footer_text = "This report was generated by the Credit Risk Assessment application. For internal use."
    footer_style = ParagraphStyle(
        name="Footer",
        parent=styles["Normal"],
        fontSize=8,
        textColor=colors.HexColor("#94a3b8"),
        alignment=1,
    )
    story.append(Spacer(1, 0.3 * inch))
    story.append(Paragraph(footer_text, footer_style))

    doc.build(story)
    buf.seek(0)
    filename = f"credit_risk_report_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf"
    return send_file(buf, mimetype="application/pdf", as_attachment=True, download_name=filename)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=config.PORT_NUM, debug=config.DEBUG)