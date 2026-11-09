#!/usr/bin/env python3
"""
IHMS Database Specification & Normalization Document Generator
Produces a comprehensive, publication-grade Word document (.docx) detailing:
- System Overview & Requirements (Group 39 IHMS Paper)
- Normalization Journey (UNF -> 1NF -> 2NF -> 3NF / BCNF)
- Embedded High-Resolution ERD and Engine Workflow Diagrams
- Relational Inventory & Cardinality Mappings
- Complete 16-Table Data Dictionary with SQL Types and Constraints
- Business Logic & Integrity Constraints (Anti-Double Allocation, SLA, Multi-tier Escalation, Recurring Faults)
- SQLAlchemy 2.0 Code Implementation & Migration Runbook
"""

import os
from datetime import datetime
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL

# Palette definitions
NAVY_PRIMARY = "1B365D"      # Main titles & table headers
CYAN_ACCENT = "0284C7"       # Section subtitles & secondary headers
TEAL_ACCENT = "0F766E"       # Feature highlights & unit tags
DARK_SLATE = "1E293B"        # Primary body text
MUTED_SLATE = "475569"       # Captions & secondary notes
BORDER_GREY = "CBD5E1"       # Subtle table borders
ROW_ALT_BG = "F8FAFC"        # Alternating table row background
CALLOUT_BLUE_BG = "EFF6FF"   # Alert background
CALLOUT_BLUE_BORDER = "2563EB" # Alert accent border
CODE_BG = "F1F5F9"           # Monospace code background

def set_cell_background(cell, hex_color):
    """Sets background shading of a table cell."""
    tc_pr = cell._tc.get_or_add_tcPr()
    # Remove existing shading if any
    for child in list(tc_pr):
        if child.tag.endswith('shd'):
            tc_pr.remove(child)
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>')
    tc_pr.append(shd)

def set_table_styling(table, col_widths=None):
    """Applies clean borders, padding, and alignment to a table."""
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_pr = table._tbl.tblPr
    
    # Set borders: subtle grey horizontal and vertical lines
    borders_xml = f'''
    <w:tblBorders {nsdecls("w")}>
        <w:top w:val="single" w:sz="4" w:space="0" w:color="{BORDER_GREY}"/>
        <w:bottom w:val="single" w:sz="6" w:space="0" w:color="{NAVY_PRIMARY}"/>
        <w:left w:val="none"/>
        <w:right w:val="none"/>
        <w:insideH w:val="single" w:sz="4" w:space="0" w:color="{BORDER_GREY}"/>
        <w:insideV w:val="none"/>
    </w:tblBorders>
    '''
    tbl_pr.append(parse_xml(borders_xml))

    # Cell padding
    tbl_cell_mar = parse_xml(f'''
    <w:tblCellMar {nsdecls("w")}>
        <w:top w:w="120" w:type="dxa"/>
        <w:bottom w:w="120" w:type="dxa"/>
        <w:left w:w="140" w:type="dxa"/>
        <w:right w:w="140" w:type="dxa"/>
    </w:tblCellMar>
    ''')
    tbl_pr.append(tbl_cell_mar)

    if col_widths:
        for row in table.rows:
            for idx, width in enumerate(col_widths):
                if idx < len(row.cells):
                    row.cells[idx].width = Inches(width)

def style_header_row(row, headers, col_widths=None):
    """Formats the table header row with navy background and bold white text."""
    for idx, text in enumerate(headers):
        cell = row.cells[idx]
        set_cell_background(cell, NAVY_PRIMARY)
        cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.space_before = Pt(4)
        p.paragraph_format.space_after = Pt(4)
        run = p.add_run(text)
        run.bold = True
        run.font.color.rgb = RGBColor(255, 255, 255)
        run.font.name = "Calibri"
        run.font.size = Pt(9.5)
        if col_widths and idx < len(col_widths):
            cell.width = Inches(col_widths[idx])

def add_table_data_row(row, values, is_alt=False, col_widths=None):
    """Adds a data row to a table with clean font and alternating background."""
    bg = ROW_ALT_BG if is_alt else "FFFFFF"
    for idx, val in enumerate(values):
        cell = row.cells[idx]
        set_cell_background(cell, bg)
        cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.space_before = Pt(3)
        p.paragraph_format.space_after = Pt(3)
        run = p.add_run(str(val))
        run.font.name = "Calibri"
        run.font.size = Pt(9)
        run.font.color.rgb = RGBColor(30, 41, 59)
        if col_widths and idx < len(col_widths):
            cell.width = Inches(col_widths[idx])

def add_callout(doc, title, text, bg_color=CALLOUT_BLUE_BG, border_color=CALLOUT_BLUE_BORDER):
    """Adds a standout alert/callout box with a colored left border."""
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = tbl.rows[0].cells[0]
    cell.width = Inches(6.5)
    set_cell_background(cell, bg_color)
    
    # Left border only
    borders_xml = f'''
    <w:tcBorders {nsdecls("w")}>
        <w:top w:val="none"/>
        <w:left w:val="single" w:sz="24" w:space="0" w:color="{border_color}"/>
        <w:bottom w:val="none"/>
        <w:right w:val="none"/>
    </w:tcBorders>
    '''
    cell._tc.get_or_add_tcPr().append(parse_xml(borders_xml))
    
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.left_indent = Inches(0.1)
    run_title = p.add_run(f"★ {title}\n")
    run_title.bold = True
    run_title.font.name = "Calibri"
    run_title.font.size = Pt(10)
    run_title.font.color.rgb = RGBColor(27, 54, 93)
    
    run_text = p.add_run(text)
    run_text.font.name = "Calibri"
    run_text.font.size = Pt(9.5)
    run_text.font.color.rgb = RGBColor(30, 41, 59)
    doc.add_paragraph().paragraph_format.space_after = Pt(4)

def add_code_block(doc, code_str):
    """Adds a styled code snippet block with monospaced font and shading."""
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = tbl.rows[0].cells[0]
    cell.width = Inches(6.5)
    set_cell_background(cell, CODE_BG)
    
    borders_xml = f'''
    <w:tcBorders {nsdecls("w")}>
        <w:top w:val="single" w:sz="4" w:space="0" w:color="{BORDER_GREY}"/>
        <w:left w:val="single" w:sz="12" w:space="0" w:color="{TEAL_ACCENT}"/>
        <w:bottom w:val="single" w:sz="4" w:space="0" w:color="{BORDER_GREY}"/>
        <w:right w:val="single" w:sz="4" w:space="0" w:color="{BORDER_GREY}"/>
    </w:tcBorders>
    '''
    cell._tc.get_or_add_tcPr().append(parse_xml(borders_xml))
    
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.left_indent = Inches(0.1)
    
    run = p.add_run(code_str)
    run.font.name = "Consolas"
    run.font.size = Pt(8.5)
    run.font.color.rgb = RGBColor(15, 23, 42)
    doc.add_paragraph().paragraph_format.space_after = Pt(4)

def build_document():
    doc = docx.Document()
    
    # Page setup - Standard Letter with 0.8 inch margins
    sections = doc.sections
    for section in sections:
        section.top_margin = Inches(0.8)
        section.bottom_margin = Inches(0.8)
        section.left_margin = Inches(0.8)
        section.right_margin = Inches(0.8)
    
    # -------------------------------------------------------------
    # COVER / HEADER TITLE BLOCK
    # -------------------------------------------------------------
    title_p = doc.add_paragraph()
    title_p.paragraph_format.space_before = Pt(12)
    title_p.paragraph_format.space_after = Pt(4)
    run_super = title_p.add_run("NILE UNIVERSITY OF NIGERIA • FACULTY OF COMPUTING\nDEPARTMENT OF COMPUTER SCIENCE • GROUP 39\n")
    run_super.font.name = "Calibri"
    run_super.font.size = Pt(10)
    run_super.font.color.rgb = RGBColor(2, 132, 199)
    run_super.bold = True
    
    run_main_title = title_p.add_run("Intelligent Hostel Management System (IHMS)\n")
    run_main_title.font.name = "Calibri"
    run_main_title.font.size = Pt(22)
    run_main_title.font.color.rgb = RGBColor(27, 54, 93)
    run_main_title.bold = True

    run_sub = title_p.add_run("Complete Well-Normalized Relational Database Architecture, Data Dictionary, Integrity Constraints & Implementation Specification")
    run_sub.font.name = "Calibri"
    run_sub.font.size = Pt(13)
    run_sub.font.color.rgb = RGBColor(71, 85, 105)

    # Document Control Metadata Box
    doc.add_paragraph().paragraph_format.space_after = Pt(4)
    meta_table = doc.add_table(rows=5, cols=2)
    col_w = [2.2, 4.3]
    set_table_styling(meta_table, col_w)
    
    meta_rows = [
        ("Project Title", "Intelligent Hostel Management System: Automated Complaint Triage and Escalation for University Hostels"),
        ("Project Group", "Group 39 (Lead: Chidubem Barack-Judah Oka, Abdullah Bukola Ahmad, Khalid Onimisi Jimoh, Tirzah Ubong Akpakip, Alerege Olumayowa Jude, Chukuladi Obowu, Johnwendy C.N.)"),
        ("Target Platform", "FastAPI (Python Logic Tier), SQLAlchemy 2.0 ORM, PostgreSQL / MySQL Relational Engine, Alembic Migrations"),
        ("Documentation Scope", "Relational Normalization (1NF–BCNF), Entity-Relationship Diagram (ERD), Engine Workflow, 16-Table Data Dictionary, Anti-Double Allocation Constraints, and Code Reference"),
        ("Specification Date", f"Academic Session 2025/2026 (Generated: {datetime.now().strftime('%B %d, %Y')})")
    ]
    for idx, (label, val) in enumerate(meta_rows):
        row = meta_table.rows[idx]
        add_table_data_row(row, [label, val], is_alt=(idx % 2 == 1), col_widths=col_w)
        row.cells[0].paragraphs[0].runs[0].bold = True
        row.cells[0].paragraphs[0].runs[0].font.color.rgb = RGBColor(27, 54, 93)

    doc.add_paragraph().paragraph_format.space_after = Pt(10)

    # -------------------------------------------------------------
    # SECTION 1: EXECUTIVE SUMMARY & SYSTEM DOMAIN OVERVIEW
    # -------------------------------------------------------------
    h1 = doc.add_heading(level=1)
    run_h1 = h1.add_run("1. Executive Summary & System Domain Requirements")
    run_h1.font.name = "Calibri"
    run_h1.font.color.rgb = RGBColor(27, 54, 93)
    run_h1.bold = True

    p = doc.add_paragraph()
    p.add_run(
        "Student accommodation represents one of the most critical operational services in modern universities. "
        "As established in the empirical research paper 'Intelligent Hostel Management System: Automated Complaint Triage "
        "and Escalation for University Hostels' (Oka et al., Nile Journal of Computing, 2026), manual and legacy semi-automated "
        "hostel operations suffer from four foundational pathologies:\n"
    )
    bullet_points = [
        ("Manual Counter Allocation: ", "Counter-based queues cause data duplication, paper loss, and critical room misallocation or double-booking where multiple students are assigned the same bed space."),
        ("Queue-Blind Complaint Intake: ", "Maintenance faults are recorded without urgency classification; an emergency burst pipe or exposed electrical wire sits in the exact same static queue as a squeaking hinge or scuffed paint."),
        ("Lack of Resolution Deadlines & Escalation: ", "Existing systems fail to enforce service level agreements (SLAs) or resolution deadlines. Ignored complaints remain unattended indefinitely because staff notifications remain passive and internal to the app."),
        ("Fragmented Records: ", "Occupancy, payment clearance, and facility maintenance data reside in disparate silos, preventing hall administrators and Student Affairs from having an authoritative, real-time single source of truth.")
    ]
    for b_title, b_desc in bullet_points:
        bp = doc.add_paragraph(style='List Bullet')
        r_bt = bp.add_run(b_title)
        r_bt.bold = True
        r_bt.font.color.rgb = RGBColor(2, 132, 199)
        bp.add_run(b_desc)

    p_arch = doc.add_paragraph()
    p_arch.add_run(
        "To resolve these operational bottlenecks, the Intelligent Hostel Management System (IHMS) implements a robust "
        "four-tier architecture comprising: (1) Client Presentation Tier (Student, Staff, and Admin Portals), (2) Logic Tier "
        "(User Management, Rule-Based Room Allocation, Complaint Management, Automated Complaint Triage & Escalation Engine, "
        "and Analytics), (3) Relational Data Tier (PostgreSQL / MySQL engine governed by strict relational constraints and foreign "
        "key integrities), and (4) Output Tier (Asynchronous SMTP Email Dispatcher and Report Exporters). "
        "This specification establishes the complete, production-ready, well-normalized relational database schema underpinning IHMS."
    )

    # -------------------------------------------------------------
    # SECTION 2: DATABASE NORMALIZATION ANALYSIS
    # -------------------------------------------------------------
    h2 = doc.add_heading(level=1)
    run_h2 = h2.add_run("2. Database Normalization Analysis (UNF to 3NF & BCNF)")
    run_h2.font.name = "Calibri"
    run_h2.font.color.rgb = RGBColor(27, 54, 93)
    run_h2.bold = True

    p_norm = doc.add_paragraph()
    p_norm.add_run(
        "A relational database must adhere to strict normalization principles to eliminate insert, update, and delete anomalies "
        "while ensuring data integrity and minimal redundancy. Below is the rigorous mathematical and structural decomposition "
        "of the IHMS data model across normalization stages."
    )

    # Sub-heading: UNF
    h_unf = doc.add_heading(level=2)
    h_unf.add_run("2.1 Unnormalized Form (UNF)")
    doc.add_paragraph(
        "In a flat, unnormalized spreadsheet or paper log, a single record contains repeating groups, multi-valued attributes, "
        "and mixed domain entities:"
    )
    add_callout(
        doc,
        "UNF Representation (Anomalous Flat Model)",
        "HOSTEL_RECORD = (StudentMatric, StudentName, StudentEmail, StudentPhone, Gender, Level, Department, "
        "FeeClearanceStatus, HostelName, HostelCode, RoomNumber, Floor, BedSpaceLabel, SessionName, Semester, "
        "ComplaintCode, ComplaintTitle, ComplaintDesc, Category, Urgency, MaintenanceUnit, UnitEmail, "
        "AssignedStaff, Status, EscalationLevel, SubmittedTime, DeadlineTime, ResolvedTime, EscalationAlerts...)\n\n"
        "Anomalies: Inserting a room requires a dummy student; deleting a complaint may delete hostel history; updating a student phone number requires touching dozens of historical complaint rows."
    )

    # Sub-heading: 1NF
    h_1nf = doc.add_heading(level=2)
    h_1nf.add_run("2.2 First Normal Form (1NF)")
    doc.add_paragraph(
        "A relation is in 1NF if and only if all column domains contain exclusively atomic (indivisible) values, "
        "and there are no repeating groups or multi-valued attributes. Every row is uniquely identifiable by a Primary Key."
    )
    doc.add_paragraph(
        "Transformations applied to achieve 1NF in IHMS:\n"
        "• Splitting multi-valued roles: Users can possess multiple roles; instead of storing a comma-separated string ('student,admin'), a discrete junction entity 'user_role' is created.\n"
        "• Atomicity of student & room attributes: Names are decomposed into 'first_name' and 'last_name'; bed spaces are modeled as individual atomic records rather than an array of beds inside a room.\n"
        "• Primary Key Assignment: Every entity receives a distinct surrogate or natural primary key ('id', 'complaint_code', 'matric_number')."
    )

    # Sub-heading: 2NF
    h_2nf = doc.add_heading(level=2)
    h_2nf.add_run("2.3 Second Normal Form (2NF)")
    doc.add_paragraph(
        "A relation is in 2NF if it is in 1NF and every non-prime attribute is fully functionally dependent on the entire "
        "primary key (no partial functional dependencies on composite keys)."
    )
    doc.add_paragraph(
        "Decompositions applied to achieve 2NF in IHMS:\n"
        "• Composite Key Analysis in 'user_role': The primary key is (user_id, role_id). The non-key attribute 'assigned_at' depends fully on both keys. User details (email, password) and role details (name, description) are decoupled into independent tables 'users' and 'roles'.\n"
        "• Room & Bed Space Decoupling: In a composite identification of a bed space, attributes describing the room (floor, capacity) depend only on 'room_id', while attributes describing the hostel (name, gender_target) depend only on 'hostel_id'. Thus, 'hostels', 'rooms', and 'bed_spaces' are partitioned into distinct relations where each attribute depends entirely on its own table's primary key."
    )

    # Sub-heading: 3NF & BCNF
    h_3nf = doc.add_heading(level=2)
    h_3nf.add_run("2.4 Third Normal Form (3NF) & Boyce-Codd Normal Form (BCNF)")
    doc.add_paragraph(
        "A relation is in 3NF if it is in 2NF and no non-prime attribute is transitively dependent on the primary key "
        "(i.e., X → Y and Y → Z where Y is not a candidate key is disallowed). A relation is in BCNF if for every functional "
        "dependency X → Y, X is a superkey."
    )
    doc.add_paragraph(
        "Decompositions applied to achieve 3NF and BCNF in IHMS:\n"
        "• Separation of Student and Staff Profiles from Users: If matric_number, level, and bursary fee clearance were stored directly in 'users', non-student users (maintenance officers, wardens) would hold nulls, and departmental attributes would be transitively dependent on matric numbers. By separating 'student_profiles' and 'staff_profiles' with 1:1 foreign keys to 'users', all attributes depend directly and only on their respective candidate keys.\n"
        "• Maintenance Units Decoupling: In complaints, the maintenance unit details (unit name, dispatch email) are determined by 'assigned_unit_id', not by 'complaint_id'. Storing unit email in 'complaints' would create a transitive dependency: complaint_id → assigned_unit_id → unit_email. This is fully normalized into 'maintenance_units'.\n"
        "• Complaint History & Audit Isolation: Each status change and escalation event is isolated in 'complaint_history', preventing historical escalation timestamps from creating update anomalies on active complaint records."
    )

    # -------------------------------------------------------------
    # SECTION 3: SYSTEM ARCHITECTURE & RELATIONAL DIAGRAMS
    # -------------------------------------------------------------
    h3 = doc.add_heading(level=1)
    run_h3 = h3.add_run("3. System Architecture & Relational Diagrams")
    run_h3.font.name = "Calibri"
    run_h3.font.color.rgb = RGBColor(27, 54, 93)
    run_h3.bold = True

    doc.add_paragraph(
        "The complete IHMS relational schema models the entire university accommodation and maintenance ecosystem. "
        "Figure 3.1 below presents the Entity-Relationship Diagram (ERD), detailing all 16 tables, primary keys, "
        "foreign key linkages, and relational cardinalities."
    )

    erd_img_path = "/home/judah/Work/school/IHMS/docs/assets/ihms_erd.png"
    if os.path.exists(erd_img_path):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_before = Pt(8)
        p_img.paragraph_format.space_after = Pt(4)
        run_img = p_img.add_run()
        run_img.add_picture(erd_img_path, width=Inches(6.4))
        
        cap = doc.add_paragraph()
        cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        cap.paragraph_format.space_after = Pt(12)
        r_cap = cap.add_run("Figure 3.1: Complete Entity-Relationship Diagram (ERD) of the Normalized IHMS Database")
        r_cap.font.name = "Calibri"
        r_cap.font.size = Pt(9)
        r_cap.italic = True
        r_cap.font.color.rgb = RGBColor(71, 85, 105)

    doc.add_paragraph(
        "Figure 3.2 illustrates the operational logic and state-transition pipeline of the Complaint Triage and "
        "Multi-Tier Escalation Engine, mapping directly to the relational tables 'complaints', 'complaint_history', "
        "and 'notification_logs'."
    )

    workflow_img_path = "/home/judah/Work/school/IHMS/docs/assets/ihms_engine_workflow.png"
    if os.path.exists(workflow_img_path):
        p_img2 = doc.add_paragraph()
        p_img2.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img2.paragraph_format.space_before = Pt(8)
        p_img2.paragraph_format.space_after = Pt(4)
        run_img2 = p_img2.add_run()
        run_img2.add_picture(workflow_img_path, width=Inches(6.2))
        
        cap2 = doc.add_paragraph()
        cap2.alignment = WD_ALIGN_PARAGRAPH.CENTER
        cap2.paragraph_format.space_after = Pt(12)
        r_cap2 = cap2.add_run("Figure 3.2: Automated Complaint Triage, SLA Deadline & Multi-Tier Escalation Engine Architecture")
        r_cap2.font.name = "Calibri"
        r_cap2.font.size = Pt(9)
        r_cap2.italic = True
        r_cap2.font.color.rgb = RGBColor(71, 85, 105)

    # Relational Inventory Table
    h_rel = doc.add_heading(level=2)
    h_rel.add_run("3.1 Relational Inventory & Cardinality Mapping")
    doc.add_paragraph("Table 3.1 outlines the primary relationships, cardinalities, foreign key references, and delete integrity rules across all entities:")

    rel_table = doc.add_table(rows=1, cols=6)
    rel_widths = [1.1, 1.2, 1.1, 0.7, 1.0, 1.4]
    set_table_styling(rel_table, rel_widths)
    style_header_row(rel_table.rows[0], ["Parent Entity", "Child Entity", "Foreign Key", "Card.", "On Delete", "Business Constraint"], rel_widths)

    rel_data = [
        ("users", "user_role", "user_id", "1:N", "CASCADE", "User deletion cleans up role memberships"),
        ("roles", "user_role", "role_id", "1:N", "CASCADE", "Role deletion purges role linkages"),
        ("users", "student_profiles", "user_id", "1:1", "CASCADE", "Student profile exists strictly for a user"),
        ("users", "staff_profiles", "user_id", "1:1", "CASCADE", "Staff profile exists strictly for a user"),
        ("maintenance_units", "staff_profiles", "unit_id", "1:N", "SET NULL", "Unit reorganization preserves staff"),
        ("hostels", "staff_profiles", "assigned_hostel_id", "1:N", "SET NULL", "Preserves warden if hostel archived"),
        ("hostels", "rooms", "hostel_id", "1:N", "CASCADE", "Deleting hostel cascades to rooms"),
        ("rooms", "bed_spaces", "room_id", "1:N", "CASCADE", "Deleting room cascades to bed spaces"),
        ("student_profiles", "allocations", "student_id", "1:N", "CASCADE", "Allocations tied to student profile"),
        ("bed_spaces", "allocations", "bed_space_id", "1:N", "CASCADE", "Allocations tied to specific bed space"),
        ("academic_sessions", "allocations", "session_id", "1:N", "RESTRICT", "Cannot delete session with active beds"),
        ("student_profiles", "complaints", "student_id", "1:N", "CASCADE", "Complaints linked to resident student"),
        ("rooms", "complaints", "room_id", "1:N", "CASCADE", "Complaints linked to physical room"),
        ("maintenance_units", "complaints", "assigned_unit_id", "1:N", "RESTRICT", "Cannot delete active maintenance unit"),
        ("staff_profiles", "complaints", "assigned_officer_id", "1:N", "SET NULL", "Unassigning officer keeps complaint"),
        ("complaints", "complaint_history", "complaint_id", "1:N", "CASCADE", "Deleting complaint removes audit trail"),
        ("complaints", "notification_logs", "complaint_id", "1:N", "SET NULL", "Outbound email log retained for audits"),
        ("users", "audit_logs", "user_id", "1:N", "SET NULL", "System transactions retained on user deletion")
    ]
    for idx, r in enumerate(rel_data):
        row = rel_table.add_row()
        add_table_data_row(row, r, is_alt=(idx % 2 == 1), col_widths=rel_widths)

    doc.add_paragraph().paragraph_format.space_after = Pt(10)

    # -------------------------------------------------------------
    # SECTION 4: COMPREHENSIVE DATA DICTIONARY
    # -------------------------------------------------------------
    h4 = doc.add_heading(level=1)
    run_h4 = h4.add_run("4. Comprehensive Data Dictionary & Schema Specification")
    run_h4.font.name = "Calibri"
    run_h4.font.color.rgb = RGBColor(27, 54, 93)
    run_h4.bold = True

    doc.add_paragraph(
        "This section documents all 16 tables comprising the IHMS database. Each table definition specifies the column name, "
        "SQL storage datatype (portable across PostgreSQL and MySQL), nullability, default values, key/index constraints, "
        "and business semantics."
    )

    data_dictionary = [
        {
            "name": "1. users",
            "desc": "Primary authentication, credential storage, and identity entity for all system actors.",
            "cols": [
                ("id", "INTEGER", "NO", "AUTO_INCREMENT", "PK", "Primary surrogate identifier for user"),
                ("username", "VARCHAR(50)", "NO", "None", "UQ, IX", "Unique university portal username / handle"),
                ("email", "VARCHAR(100)", "NO", "None", "UQ, IX", "Official institutional email address"),
                ("password", "VARCHAR(255)", "NO", "None", "-", "Bcrypt-hashed password string"),
                ("first_name", "VARCHAR(50)", "NO", "''", "-", "User legal first name"),
                ("last_name", "VARCHAR(50)", "NO", "''", "-", "User legal surname / family name"),
                ("phone_number", "VARCHAR(20)", "YES", "NULL", "-", "Contact telephone / mobile number"),
                ("is_active", "BOOLEAN", "NO", "TRUE", "-", "Account active status flag"),
                ("created_at", "DATETIME", "NO", "CURRENT_TIMESTAMP", "-", "Timestamp of account registration"),
                ("updated_at", "DATETIME", "NO", "CURRENT_TIMESTAMP", "-", "Timestamp of latest account profile update")
            ]
        },
        {
            "name": "2. roles",
            "desc": "System role definitions establishing access boundaries for the four authorized user groups.",
            "cols": [
                ("id", "INTEGER", "NO", "AUTO_INCREMENT", "PK", "Primary surrogate identifier for role"),
                ("name", "VARCHAR(50)", "NO", "None", "UQ, IX", "Role name: student, maintenance_officer, hall_warden, administrator"),
                ("description", "VARCHAR(255)", "YES", "NULL", "-", "Human-readable description of permission scope"),
                ("created_at", "DATETIME", "NO", "CURRENT_TIMESTAMP", "-", "Role initialization timestamp")
            ]
        },
        {
            "name": "3. user_role",
            "desc": "Junction table implementing many-to-many relationship between users and roles.",
            "cols": [
                ("user_id", "INTEGER", "NO", "None", "PK, FK", "Foreign key referencing users.id (ON DELETE CASCADE)"),
                ("role_id", "INTEGER", "NO", "None", "PK, FK", "Foreign key referencing roles.id (ON DELETE CASCADE)"),
                ("assigned_at", "DATETIME", "NO", "CURRENT_TIMESTAMP", "-", "Timestamp when role was granted")
            ]
        },
        {
            "name": "4. maintenance_units",
            "desc": "Departments responsible for executing maintenance requests (Plumbing, Electrical, Carpentry, Sanitation, Other).",
            "cols": [
                ("id", "INTEGER", "NO", "AUTO_INCREMENT", "PK", "Primary surrogate identifier for unit"),
                ("code", "VARCHAR(30)", "NO", "None", "UQ, IX", "Department code (e.g., PLUMBING, ELECTRICAL, CARPENTRY)"),
                ("name", "VARCHAR(100)", "NO", "None", "-", "Descriptive department name"),
                ("description", "VARCHAR(255)", "YES", "NULL", "-", "Department operational scope"),
                ("email", "VARCHAR(100)", "NO", "None", "-", "Unit centralized dispatch / alert email address"),
                ("is_active", "BOOLEAN", "NO", "TRUE", "-", "Department operational status"),
                ("created_at", "DATETIME", "NO", "CURRENT_TIMESTAMP", "-", "Unit record creation timestamp")
            ]
        },
        {
            "name": "5. hostels",
            "desc": "Hostel building blocks and halls of residence with demographic eligibility policies.",
            "cols": [
                ("id", "INTEGER", "NO", "AUTO_INCREMENT", "PK", "Primary surrogate identifier for hostel"),
                ("name", "VARCHAR(100)", "NO", "None", "UQ, IX", "Hostel hall name (e.g., Nelson Mandela Hall)"),
                ("code", "VARCHAR(20)", "NO", "None", "UQ, IX", "Short hostel abbreviation / code (e.g., NMH)"),
                ("gender_target", "VARCHAR(20)", "NO", "'mixed'", "-", "Gender policy constraint: 'male', 'female', 'mixed'"),
                ("description", "VARCHAR(255)", "YES", "NULL", "-", "Hostel location and descriptive details"),
                ("total_capacity", "INTEGER", "NO", "0", "-", "Total physical bed space capacity"),
                ("is_active", "BOOLEAN", "NO", "TRUE", "-", "Hostel operational availability flag"),
                ("created_at", "DATETIME", "NO", "CURRENT_TIMESTAMP", "-", "Creation timestamp"),
                ("updated_at", "DATETIME", "NO", "CURRENT_TIMESTAMP", "-", "Last update timestamp")
            ]
        },
        {
            "name": "6. rooms",
            "desc": "Individual room enclosures inside hostel blocks. Unique constraint on (hostel_id, room_number).",
            "cols": [
                ("id", "INTEGER", "NO", "AUTO_INCREMENT", "PK", "Primary surrogate identifier for room"),
                ("hostel_id", "INTEGER", "NO", "None", "FK, IX", "Foreign key referencing hostels.id (ON DELETE CASCADE)"),
                ("room_number", "VARCHAR(20)", "NO", "None", "-", "Room identifier (e.g., 'A-101', 'B-204')"),
                ("floor", "INTEGER", "NO", "1", "-", "Floor level number"),
                ("capacity", "INTEGER", "NO", "4", "-", "Number of bed spaces permitted in room"),
                ("current_occupancy", "INTEGER", "NO", "0", "-", "Count of actively allocated students"),
                ("is_available", "BOOLEAN", "NO", "TRUE", "-", "Room availability status (false if under repair)"),
                ("created_at", "DATETIME", "NO", "CURRENT_TIMESTAMP", "-", "Creation timestamp")
            ]
        },
        {
            "name": "7. bed_spaces",
            "desc": "Individual atomic bed spaces within rooms. Unique constraint on (room_id, bed_label).",
            "cols": [
                ("id", "INTEGER", "NO", "AUTO_INCREMENT", "PK", "Primary surrogate identifier for bed space"),
                ("room_id", "INTEGER", "NO", "None", "FK, IX", "Foreign key referencing rooms.id (ON DELETE CASCADE)"),
                ("bed_label", "VARCHAR(10)", "NO", "None", "-", "Bed identifier within room (e.g., 'Bed-1', 'Bed-2', 'Bed-A')"),
                ("is_occupied", "BOOLEAN", "NO", "FALSE", "-", "Live occupancy flag (true if actively allocated)"),
                ("is_active", "BOOLEAN", "NO", "TRUE", "-", "Operational readiness flag (false if damaged)"),
                ("created_at", "DATETIME", "NO", "CURRENT_TIMESTAMP", "-", "Creation timestamp")
            ]
        },
        {
            "name": "8. student_profiles",
            "desc": "Specialized student domain attributes, bursary fee clearance status, and emergency contacts.",
            "cols": [
                ("id", "INTEGER", "NO", "AUTO_INCREMENT", "PK", "Primary surrogate identifier for student profile"),
                ("user_id", "INTEGER", "NO", "None", "FK, UQ, IX", "1:1 Foreign key referencing users.id (ON DELETE CASCADE)"),
                ("matric_number", "VARCHAR(50)", "NO", "None", "UQ, IX", "Unique university student matriculation number"),
                ("gender", "VARCHAR(20)", "NO", "None", "-", "Student biological gender ('male', 'female')"),
                ("level", "INTEGER", "NO", "None", "-", "Academic study level (100, 200, 300, 400, 500)"),
                ("department", "VARCHAR(100)", "NO", "None", "-", "Academic department"),
                ("faculty", "VARCHAR(100)", "YES", "NULL", "-", "Academic faculty (e.g., Computing)"),
                ("fee_cleared", "BOOLEAN", "NO", "FALSE", "-", "Bursary fee clearance prerequisite check"),
                ("fee_cleared_at", "DATETIME", "YES", "NULL", "-", "Timestamp of bursary financial clearance"),
                ("emergency_contact_name", "VARCHAR(100)", "YES", "NULL", "-", "Name of emergency contact guardian"),
                ("emergency_contact_phone", "VARCHAR(20)", "YES", "NULL", "-", "Telephone number of emergency guardian"),
                ("created_at", "DATETIME", "NO", "CURRENT_TIMESTAMP", "-", "Profile creation timestamp"),
                ("updated_at", "DATETIME", "NO", "CURRENT_TIMESTAMP", "-", "Profile update timestamp")
            ]
        },
        {
            "name": "9. staff_profiles",
            "desc": "Specialized staff profile attributes linking officers to maintenance units or assigned hostels.",
            "cols": [
                ("id", "INTEGER", "NO", "AUTO_INCREMENT", "PK", "Primary surrogate identifier for staff profile"),
                ("user_id", "INTEGER", "NO", "None", "FK, UQ, IX", "1:1 Foreign key referencing users.id (ON DELETE CASCADE)"),
                ("staff_number", "VARCHAR(50)", "NO", "None", "UQ, IX", "Unique university employee staff ID number"),
                ("unit_id", "INTEGER", "YES", "NULL", "FK, IX", "FK referencing maintenance_units.id (for maintenance officers)"),
                ("assigned_hostel_id", "INTEGER", "YES", "NULL", "FK, IX", "FK referencing hostels.id (for assigned hall wardens)"),
                ("designation", "VARCHAR(100)", "YES", "NULL", "-", "Job designation (e.g., Chief Warden, Senior Electrician)"),
                ("office_location", "VARCHAR(100)", "YES", "NULL", "-", "Campus office or workshop location"),
                ("created_at", "DATETIME", "NO", "CURRENT_TIMESTAMP", "-", "Profile creation timestamp"),
                ("updated_at", "DATETIME", "NO", "CURRENT_TIMESTAMP", "-", "Profile update timestamp")
            ]
        },
        {
            "name": "10. academic_sessions",
            "desc": "Academic year and semester records. Unique constraint on (session_name, semester).",
            "cols": [
                ("id", "INTEGER", "NO", "AUTO_INCREMENT", "PK", "Primary surrogate identifier for session"),
                ("session_name", "VARCHAR(50)", "NO", "None", "-", "Academic session name (e.g., '2025/2026')"),
                ("semester", "VARCHAR(20)", "NO", "'first'", "-", "Semester: 'first', 'second'"),
                ("is_current", "BOOLEAN", "NO", "FALSE", "IX", "Active semester flag for current allocations"),
                ("start_date", "DATE", "NO", "None", "-", "Commencement date of academic semester"),
                ("end_date", "DATE", "NO", "None", "-", "Conclusion date of academic semester"),
                ("created_at", "DATETIME", "NO", "CURRENT_TIMESTAMP", "-", "Session registration timestamp")
            ]
        },
        {
            "name": "11. allocations",
            "desc": "Bed space allocation records with database-level anti-double-allocation and anti-double-booking constraints.",
            "cols": [
                ("id", "INTEGER", "NO", "AUTO_INCREMENT", "PK", "Primary surrogate identifier for allocation"),
                ("student_id", "INTEGER", "NO", "None", "FK, IX", "FK referencing student_profiles.id (ON DELETE CASCADE)"),
                ("bed_space_id", "INTEGER", "NO", "None", "FK, IX", "FK referencing bed_spaces.id (ON DELETE CASCADE)"),
                ("session_id", "INTEGER", "NO", "None", "FK, IX", "FK referencing academic_sessions.id (ON DELETE RESTRICT)"),
                ("status", "VARCHAR(20)", "NO", "'active'", "IX", "Status: 'pending', 'active', 'revoked', 'expired', 'cancelled'"),
                ("active_bed_marker", "INTEGER", "YES", "NULL", "UQ", "Holds bed_space_id ONLY when active; strictly enforces no double allocation"),
                ("active_student_session_marker", "VARCHAR(100)", "YES", "NULL", "UQ", "Holds f'{student_id}_{session_id}' ONLY when active; prevents double booking"),
                ("allocated_at", "DATETIME", "NO", "CURRENT_TIMESTAMP", "-", "Timestamp of bed space allotment"),
                ("expires_at", "DATETIME", "YES", "NULL", "-", "Expiration timestamp if temporary hold"),
                ("checked_in_at", "DATETIME", "YES", "NULL", "-", "Timestamp when student physical check-in occurred"),
                ("checked_out_at", "DATETIME", "YES", "NULL", "-", "Timestamp when student physical check-out occurred"),
                ("allocated_by_user_id", "INTEGER", "YES", "NULL", "FK", "FK referencing users.id (NULL if auto-allocated by algorithm)"),
                ("notes", "VARCHAR(255)", "YES", "NULL", "-", "Administrative notes or special accommodation conditions")
            ]
        },
        {
            "name": "12. complaints",
            "desc": "Primary complaint intake, auto-triage, SLA deadline calculation, and tracking entity.",
            "cols": [
                ("id", "INTEGER", "NO", "AUTO_INCREMENT", "PK", "Primary surrogate identifier for complaint"),
                ("complaint_code", "VARCHAR(50)", "NO", "None", "UQ, IX", "Unique complaint tracking reference (e.g., 'CMP-2026-0001')"),
                ("student_id", "INTEGER", "NO", "None", "FK, IX", "FK referencing student_profiles.id (lodging student)"),
                ("room_id", "INTEGER", "NO", "None", "FK, IX", "FK referencing rooms.id (room where fault exists)"),
                ("title", "VARCHAR(150)", "NO", "None", "-", "Short summary of fault"),
                ("description", "TEXT", "NO", "None", "-", "Detailed fault narrative lodged by student"),
                ("category", "VARCHAR(30)", "NO", "None", "IX", "Triaged category: plumbing, electrical, carpentry, sanitation, other"),
                ("urgency", "VARCHAR(20)", "NO", "None", "IX", "Urgency level: urgent (24h), normal (72h), low (7 days)"),
                ("triage_source", "VARCHAR(20)", "NO", "'keyword'", "-", "Triage mechanism: 'keyword', 'jev_ai', 'manual'"),
                ("triage_confidence", "FLOAT", "YES", "NULL", "-", "Confidence probability if AI/Jev triaged (0.00 - 1.00)"),
                ("assigned_unit_id", "INTEGER", "NO", "None", "FK, IX", "FK referencing maintenance_units.id (responsible department)"),
                ("assigned_officer_id", "INTEGER", "YES", "NULL", "FK, IX", "FK referencing staff_profiles.id (specific technician assigned)"),
                ("status", "VARCHAR(30)", "NO", "'open'", "IX", "Status: open, assigned, in_progress, resolved, closed, rejected"),
                ("escalation_level", "INTEGER", "NO", "0", "IX", "Escalation tier: 0 (Normal Unit), 1 (Hall Warden), 2 (Student Affairs)"),
                ("submitted_at", "DATETIME", "NO", "CURRENT_TIMESTAMP", "IX", "Exact timestamp of submission"),
                ("deadline_at", "DATETIME", "NO", "None", "IX", "Resolution SLA deadline (submitted_at + 24h/72h/7d)"),
                ("escalated_to_warden_at", "DATETIME", "YES", "NULL", "-", "Timestamp when Level 1 escalation fired (t >= d)"),
                ("escalated_to_admin_at", "DATETIME", "YES", "NULL", "-", "Timestamp when Level 2 escalation fired (t >= 2d)"),
                ("resolved_at", "DATETIME", "YES", "NULL", "IX", "Timestamp when maintenance officer marked fault resolved"),
                ("resolution_notes", "TEXT", "YES", "NULL", "-", "Technician repair notes and work summary"),
                ("student_feedback_rating", "INTEGER", "YES", "NULL", "-", "Student satisfaction rating (1 to 5 stars)"),
                ("student_feedback_comment", "TEXT", "YES", "NULL", "-", "Student qualitative review of completed repair")
            ]
        },
        {
            "name": "13. complaint_history",
            "desc": "Append-only chronological audit log of all status transitions, triage events, and automated escalations.",
            "cols": [
                ("id", "INTEGER", "NO", "AUTO_INCREMENT", "PK", "Primary surrogate identifier for history record"),
                ("complaint_id", "INTEGER", "NO", "None", "FK, IX", "FK referencing complaints.id (ON DELETE CASCADE)"),
                ("action_type", "VARCHAR(50)", "NO", "None", "IX", "Action: created, triaged, assigned, status_changed, escalated_level_1, escalated_level_2, resolved"),
                ("from_status", "VARCHAR(50)", "YES", "NULL", "-", "Previous complaint lifecycle status"),
                ("to_status", "VARCHAR(50)", "YES", "NULL", "-", "New complaint lifecycle status"),
                ("from_escalation_level", "INTEGER", "YES", "NULL", "-", "Previous escalation tier"),
                ("to_escalation_level", "INTEGER", "YES", "NULL", "-", "New escalation tier"),
                ("performed_by_user_id", "INTEGER", "YES", "NULL", "FK, IX", "FK referencing users.id (NULL if automated background engine)"),
                ("notes", "TEXT", "YES", "NULL", "-", "System reason or technician explanation"),
                ("created_at", "DATETIME", "NO", "CURRENT_TIMESTAMP", "IX", "Timestamp of action execution")
            ]
        },
        {
            "name": "14. notification_logs",
            "desc": "Outbound SMTP dispatch audit trail recording all automated emails sent to wardens, staff, and students.",
            "cols": [
                ("id", "INTEGER", "NO", "AUTO_INCREMENT", "PK", "Primary surrogate identifier for dispatch record"),
                ("recipient_email", "VARCHAR(100)", "NO", "None", "IX", "Target recipient email address"),
                ("recipient_role", "VARCHAR(50)", "NO", "None", "-", "Recipient role (hall_warden, administrator, student, officer)"),
                ("recipient_user_id", "INTEGER", "YES", "NULL", "FK, IX", "FK referencing users.id (recipient user account)"),
                ("subject", "VARCHAR(200)", "NO", "None", "-", "Email subject header"),
                ("body", "TEXT", "NO", "None", "-", "Full email body content / message text"),
                ("event_type", "VARCHAR(50)", "NO", "None", "IX", "Trigger event: allocation_confirmed, complaint_assigned, escalated_level_1, escalated_level_2, complaint_resolved"),
                ("complaint_id", "INTEGER", "YES", "NULL", "FK, IX", "FK referencing complaints.id (if notification pertains to fault)"),
                ("status", "VARCHAR(20)", "NO", "'sent'", "IX", "Delivery status: 'queued', 'sent', 'failed'"),
                ("error_message", "TEXT", "YES", "NULL", "-", "SMTP server error trace if delivery failed"),
                ("sent_at", "DATETIME", "NO", "CURRENT_TIMESTAMP", "IX", "Exact timestamp of outbound transmission")
            ]
        },
        {
            "name": "15. triage_keywords",
            "desc": "Configurable keyword-to-category dictionary supporting live triage adjustments without redeployment.",
            "cols": [
                ("id", "INTEGER", "NO", "AUTO_INCREMENT", "PK", "Primary surrogate identifier for dictionary keyword"),
                ("keyword", "VARCHAR(100)", "NO", "None", "IX", "Keyword string (e.g., 'burst', 'flood', 'spark', 'leaking tap')"),
                ("category", "VARCHAR(30)", "NO", "None", "IX", "Target maintenance category (plumbing, electrical, etc.)"),
                ("urgency", "VARCHAR(20)", "NO", "None", "IX", "Associated urgency level (urgent, normal, low)"),
                ("weight", "INTEGER", "NO", "1", "-", "Matching priority weight in text scoring"),
                ("is_active", "BOOLEAN", "NO", "TRUE", "-", "Keyword active matching status"),
                ("created_at", "DATETIME", "NO", "CURRENT_TIMESTAMP", "-", "Rule entry timestamp")
            ]
        },
        {
            "name": "16. audit_logs",
            "desc": "System-wide transaction and security change tracking for administrative governance.",
            "cols": [
                ("id", "INTEGER", "NO", "AUTO_INCREMENT", "PK", "Primary surrogate identifier for audit entry"),
                ("user_id", "INTEGER", "YES", "NULL", "FK, IX", "FK referencing users.id (actor initiating operation)"),
                ("ip_address", "VARCHAR(50)", "YES", "NULL", "-", "Client IP address originating request"),
                ("action", "VARCHAR(100)", "NO", "None", "IX", "Action performed (e.g., CREATE_USER, ALLOCATE_BED, UPDATE_STATUS)"),
                ("entity_name", "VARCHAR(50)", "NO", "None", "IX", "Target table modified (e.g., allocations, complaints)"),
                ("entity_id", "INTEGER", "YES", "NULL", "-", "Target record primary key"),
                ("old_values", "TEXT", "YES", "NULL", "-", "JSON representation of state prior to mutation"),
                ("new_values", "TEXT", "YES", "NULL", "-", "JSON representation of state following mutation"),
                ("created_at", "DATETIME", "NO", "CURRENT_TIMESTAMP", "IX", "Timestamp of recorded mutation")
            ]
        }
    ]

    col_widths_dd = [1.3, 1.1, 0.6, 1.1, 0.7, 1.7]

    for table_meta in data_dictionary:
        h_tbl = doc.add_heading(level=2)
        h_tbl.add_run(table_meta["name"])
        doc.add_paragraph(f"Purpose: {table_meta['desc']}")

        tbl = doc.add_table(rows=1, cols=6)
        set_table_styling(tbl, col_widths_dd)
        style_header_row(tbl.rows[0], ["Column Name", "Data Type", "Null", "Default", "Key / Index", "Description & Semantics"], col_widths_dd)

        for idx, col in enumerate(table_meta["cols"]):
            row = tbl.add_row()
            add_table_data_row(row, col, is_alt=(idx % 2 == 1), col_widths=col_widths_dd)
            # Make column name bold
            row.cells[0].paragraphs[0].runs[0].bold = True

        doc.add_paragraph().paragraph_format.space_after = Pt(8)

    # -------------------------------------------------------------
    # SECTION 5: ADVANCED BUSINESS INTEGRITY CONSTRAINTS
    # -------------------------------------------------------------
    h5 = doc.add_heading(level=1)
    run_h5 = h5.add_run("5. Advanced Business Integrity Constraints & Engine Formulations")
    run_h5.font.name = "Calibri"
    run_h5.font.color.rgb = RGBColor(27, 54, 93)
    run_h5.bold = True

    doc.add_paragraph(
        "A relational database for a critical institutional infrastructure system must not rely solely on application-level "
        "code to enforce integrity. IHMS embeds foundational business invariants directly into the database engine."
    )

    # Sub-heading 5.1: Double Allocation
    h_double = doc.add_heading(level=2)
    h_double.add_run("5.1 Mathematical Anti-Double-Allocation Constraint Formulation")
    doc.add_paragraph(
        "In manual hostel administration, double-allocating a bed space is the single most common failure mode. "
        "As established in Section 3.3 and Section 3.6 of the research paper (Oka et al., 2026), IHMS mandates a database-level "
        "unique constraint that renders double allocation mathematically impossible."
    )
    add_callout(
        doc,
        "The Anti-Double-Allocation Invariant",
        "Problem: A bed space must have at most ONE active allocation at any given moment in time, while permitting unlimited "
        "historical (revoked, expired, cancelled) records.\n\n"
        "PostgreSQL Solution: Partial unique index:\n"
        "CREATE UNIQUE INDEX uq_active_bed ON allocations(bed_space_id) WHERE status = 'active';\n\n"
        "Universal ANSI SQL / MySQL / PostgreSQL Solution (Implemented in IHMS):\n"
        "Under ANSI SQL standards, NULL != NULL in unique indexes. We define an active tracker column:\n"
        "active_bed_marker = bed_space_id  (when status = 'active')\n"
        "active_bed_marker = NULL          (when status IN ('revoked', 'expired', 'cancelled'))\n"
        "CONSTRAINT uq_active_bed_allocation UNIQUE (active_bed_marker)\n\n"
        "Result: If Bed #10 is active, active_bed_marker = 10. Any concurrent attempt to insert another active row for Bed #10 "
        "raises a fatal DB UniqueConstraint IntegrityError. If the allocation is terminated, the marker becomes NULL, freeing the bed."
    )

    # Sub-heading 5.2: Double Booking
    h_book = doc.add_heading(level=2)
    h_book.add_run("5.2 Anti-Double-Booking Constraint Formulation")
    doc.add_paragraph(
        "Similarly, a student must not hold more than one active bed space during the same academic session. "
        "IHMS enforces the constraint 'uq_active_student_session_allocation' on column 'active_student_session_marker'. "
        "When active, this marker holds f'{student_id}_{session_id}'. When terminated, it becomes NULL. "
        "This completely eliminates opportunistic multi-room reservations."
    )

    # Sub-heading 5.3: SLA & Escalation
    h_sla = doc.add_heading(level=2)
    h_sla.add_run("5.3 SLA Deadlines and Two-Tier Escalation Formulation")
    doc.add_paragraph(
        "The Complaint Triage and Escalation Engine computes the resolution deadline d from the triage urgency level "
        "established in Table IV of the research paper:\n"
        "• Urgent (burst, flood, spark, exposed wire, no water, broken lock): d = 24 hours\n"
        "• Normal (leaking tap, faulty socket, broken bed, blocked drain): d = 72 hours\n"
        "• Low (paint, loose handle, squeaking door): d = 7 days (168 hours)"
    )
    doc.add_paragraph(
        "A background daemon (APScheduler) executes every 15 minutes. For each open complaint, it evaluates the elapsed time "
        "t = (now() - submitted_at) against the deadline d using Equation (1) from the research paper:"
    )
    add_callout(
        doc,
        "Equation (1): Two-Level Escalation Computation",
        "L = 0   if   t < d             (Level 0: Normal Unit Queue)\n"
        "L = 1   if   d <= t < 2d       (Level 1: Overdue -> Automated SMTP Alert to Hall Warden)\n"
        "L = 2   if   t >= 2d           (Level 2: Severe Breach -> Automated SMTP Alert to Student Affairs + Admin Dashboard Flag)\n\n"
        "Every escalation event writes an immutable entry to 'complaint_history' and 'notification_logs', establishing legal "
        "and operational traceability of exactly who was alerted and when."
    )

    # Sub-heading 5.4: Recurring Faults
    h_recur = doc.add_heading(level=2)
    h_recur.add_run("5.4 Recurring Fault Room Detection Logic")
    doc.add_paragraph(
        "The Reporting module identifies compromised infrastructure by tracking recurring faults, defined in Section 3.3 "
        "of the paper as three or more complaints of the same category lodged against the same room within 30 days. "
        "To guarantee high-performance query execution across millions of records, IHMS implements a composite database index:"
    )
    add_code_block(
        doc,
        "-- Composite index on complaints table:\n"
        "CREATE INDEX ix_complaint_room_category_submitted ON complaints (room_id, category, submitted_at);\n\n"
        "-- Optimized SQL query for recurring fault detection:\n"
        "SELECT room_id, category, COUNT(id) AS complaint_count\n"
        "FROM complaints\n"
        "WHERE submitted_at >= NOW() - INTERVAL '30 DAYS'\n"
        "GROUP BY room_id, category\n"
        "HAVING COUNT(id) >= 3\n"
        "ORDER BY complaint_count DESC;"
    )

    # -------------------------------------------------------------
    # SECTION 6: IMPLEMENTATION GUIDE & CODE REFERENCE
    # -------------------------------------------------------------
    h6 = doc.add_heading(level=1)
    run_h6 = h6.add_run("6. SQLAlchemy 2.0 Model Implementation Reference")
    run_h6.font.name = "Calibri"
    run_h6.font.color.rgb = RGBColor(27, 54, 93)
    run_h6.bold = True

    doc.add_paragraph(
        "The complete schema has been fully implemented in the project repository under 'app/model/'. "
        "Below is the code layout and core model definitions for group member replication."
    )

    doc.add_paragraph(
        "Module Layout:\n"
        "• app/model/enums.py: Enum definitions (UserRoleEnum, ComplaintCategoryEnum, ComplaintUrgencyEnum, etc.)\n"
        "• app/model/user.py & role.py & user_role.py: Authentication and role-based access control\n"
        "• app/model/maintenance_unit.py: Maintenance departments\n"
        "• app/model/hostel.py, room.py, bed_space.py: Hostel facility hierarchy\n"
        "• app/model/student_profile.py & staff_profile.py: Specialized user extensions\n"
        "• app/model/academic_session.py & allocation.py: Session and anti-double allocation logic\n"
        "• app/model/complaint.py, complaint_history.py, notification_log.py, triage_keyword.py, audit_log.py: Complaint management & audit trail\n"
        "• app/model/__init__.py: Centralized export namespace"
    )

    doc.add_paragraph("Key Model Excerpt: Allocation (Anti-Double Allocation Implementation):")
    add_code_block(
        doc,
        "class Allocation(Base):\n"
        "    __tablename__ = 'allocations'\n\n"
        "    id = Column(Integer, primary_key=True, index=True)\n"
        "    student_id = Column(Integer, ForeignKey('student_profiles.id', ondelete='CASCADE'), nullable=False, index=True)\n"
        "    bed_space_id = Column(Integer, ForeignKey('bed_spaces.id', ondelete='CASCADE'), nullable=False, index=True)\n"
        "    session_id = Column(Integer, ForeignKey('academic_sessions.id', ondelete='RESTRICT'), nullable=False, index=True)\n"
        "    status = Column(SQLEnum(AllocationStatusEnum, native_enum=False), default=AllocationStatusEnum.ACTIVE, nullable=False)\n"
        "    active_bed_marker = Column(Integer, nullable=True)\n"
        "    active_student_session_marker = Column(String(100), nullable=True)\n"
        "    allocated_at = Column(DateTime, default=datetime.utcnow, nullable=False)\n\n"
        "    __table_args__ = (\n"
        "        UniqueConstraint('active_bed_marker', name='uq_active_bed_allocation'),\n"
        "        UniqueConstraint('active_student_session_marker', name='uq_active_student_session_allocation'),\n"
        "    )\n\n"
        "    def sync_active_markers(self):\n"
        "        if self.status == AllocationStatusEnum.ACTIVE:\n"
        "            self.active_bed_marker = self.bed_space_id\n"
        "            self.active_student_session_marker = f'{self.student_id}_{self.session_id}'\n"
        "        else:\n"
        "            self.active_bed_marker = None\n"
        "            self.active_student_session_marker = None"
    )

    # -------------------------------------------------------------
    # SECTION 7: MIGRATION & REPLICATION RUNBOOK
    # -------------------------------------------------------------
    h7 = doc.add_heading(level=1)
    run_h7 = h7.add_run("7. Database Migration & Replication Runbook for Group Members")
    run_h7.font.name = "Calibri"
    run_h7.font.color.rgb = RGBColor(27, 54, 93)
    run_h7.bold = True

    doc.add_paragraph(
        "To replicate this database and run the IHMS backend locally or on a server, group members should follow these exact steps:"
    )

    runbook_steps = [
        ("Step 1: Clone Repository & Configure Environment (.env)",
         "Configure the database connection string in .env:\n"
         "# MySQL Configuration:\n"
         "DATABASE_URL=mysql+pymysql://root:password@localhost:3306/ihms_db\n"
         "# OR PostgreSQL Configuration:\n"
         "DATABASE_URL=postgresql://postgres:password@localhost:5432/ihms_db"),
        
        ("Step 2: Install Virtual Environment Dependencies",
         "pip install fastapi uvicorn sqlalchemy alembic pymysql psycopg2-binary python-dotenv python-docx"),
        
        ("Step 3: Execute Alembic Database Migrations",
         "The FastAPI application lifespan in app/main.py automatically checks and applies migrations on startup.\n"
         "Alternatively, run migrations manually via CLI:\n"
         "alembic revision --autogenerate -m 'Complete IHMS normalized schema'\n"
         "alembic upgrade head"),
        
        ("Step 4: Seed Foundational Roles, Units, and Triage Keywords",
         "Boot the FastAPI server:\n"
         "python app/main.py\n"
         "Send a POST request to seed foundational data:\n"
         "curl -X POST http://127.0.0.1:8000/seed-data\n"
         "This automatically populates the 4 core roles, the 5 maintenance departments, default triage keywords (Table IV), and a test admin user."),
        
        ("Step 5: Access Interactive API Documentation",
         "Open browser at http://127.0.0.1:8000/docs (Swagger UI) to test endpoints, view schemas, and query relational models.")
    ]

    for title, details in runbook_steps:
        add_callout(doc, title, details, bg_color="F8FAFC", border_color="0284C7")

    # Document sign-off footer
    p_footer = doc.add_paragraph()
    p_footer.paragraph_format.space_before = Pt(20)
    p_footer.alignment = WD_ALIGN_PARAGRAPH.CENTER
    rf = p_footer.add_run("— End of Specification • Group 39 IHMS Technical Documentation —")
    rf.font.name = "Calibri"
    rf.font.size = Pt(9)
    rf.italic = True
    rf.font.color.rgb = RGBColor(148, 163, 184)

    output_path = "/home/judah/Work/school/IHMS/IHMS_Normalized_Database_Specification.docx"
    doc.save(output_path)
    print(f"✅ IHMS Database Specification successfully generated at: {output_path}")

if __name__ == "__main__":
    build_document()
