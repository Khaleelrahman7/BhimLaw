"""
BhimLaw AI - PDF Report Generator
Comprehensive PDF generation system for legal analysis reports
"""

import logging
from datetime import datetime
from typing import Dict, Any, List, Optional
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor, black, blue, red, green
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.platypus.tableofcontents import TableOfContents
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
from reportlab.pdfgen import canvas
from reportlab.lib import colors
import io
import base64

# Configure logging
logger = logging.getLogger("BhimLaw_PDF_Generator")

class BhimLawPDFGenerator:
    """
    Advanced PDF generator for BhimLaw AI legal analysis reports
    Creates professional, comprehensive legal documents with proper formatting
    """
    
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self.setup_custom_styles()
        logger.info("BhimLaw PDF Generator initialized")
    
    def setup_custom_styles(self):
        """Setup custom styles for legal documents"""
        # Title style
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Title'],
            fontSize=24,
            spaceAfter=30,
            textColor=HexColor('#2c3e50'),
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        ))
        
        # Subtitle style
        self.styles.add(ParagraphStyle(
            name='CustomSubtitle',
            parent=self.styles['Heading1'],
            fontSize=16,
            spaceAfter=20,
            textColor=HexColor('#34495e'),
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        ))
        
        # Section heading style
        self.styles.add(ParagraphStyle(
            name='SectionHeading',
            parent=self.styles['Heading2'],
            fontSize=14,
            spaceAfter=12,
            spaceBefore=20,
            textColor=HexColor('#2980b9'),
            fontName='Helvetica-Bold',
            borderWidth=1,
            borderColor=HexColor('#2980b9'),
            borderPadding=5
        ))
        
        # Legal text style
        self.styles.add(ParagraphStyle(
            name='LegalText',
            parent=self.styles['Normal'],
            fontSize=11,
            spaceAfter=8,
            alignment=TA_JUSTIFY,
            fontName='Helvetica',
            leading=14
        ))
        
        # Important note style
        self.styles.add(ParagraphStyle(
            name='ImportantNote',
            parent=self.styles['Normal'],
            fontSize=10,
            spaceAfter=10,
            textColor=HexColor('#e74c3c'),
            fontName='Helvetica-Bold',
            borderWidth=1,
            borderColor=HexColor('#e74c3c'),
            borderPadding=8,
            backColor=HexColor('#fdf2f2')
        ))
        
        # Footer style
        self.styles.add(ParagraphStyle(
            name='Footer',
            parent=self.styles['Normal'],
            fontSize=8,
            textColor=HexColor('#7f8c8d'),
            alignment=TA_CENTER,
            fontName='Helvetica'
        ))

    def create_header_footer(self, canvas, doc):
        """Create header and footer for each page"""
        canvas.saveState()
        
        # Header
        canvas.setFont('Helvetica-Bold', 12)
        canvas.setFillColor(HexColor('#2c3e50'))
        canvas.drawString(50, letter[1] - 50, "BhimLaw AI - Legal Analysis Report")
        canvas.drawRightString(letter[0] - 50, letter[1] - 50, f"Generated: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
        
        # Header line
        canvas.setStrokeColor(HexColor('#2980b9'))
        canvas.setLineWidth(2)
        canvas.line(50, letter[1] - 60, letter[0] - 50, letter[1] - 60)
        
        # Footer
        canvas.setFont('Helvetica', 8)
        canvas.setFillColor(HexColor('#7f8c8d'))
        canvas.drawString(50, 30, "© 2024 BhimLaw AI - Revolutionary Legal Technology")
        canvas.drawRightString(letter[0] - 50, 30, f"Page {doc.page}")
        
        # Footer line
        canvas.setStrokeColor(HexColor('#bdc3c7'))
        canvas.setLineWidth(1)
        canvas.line(50, 40, letter[0] - 50, 40)
        
        canvas.restoreState()

    def generate_legal_analysis_pdf(self, analysis_data: Dict[str, Any], 
                                  agent_info: Dict[str, Any] = None) -> bytes:
        """
        Generate comprehensive PDF report for legal analysis
        
        Args:
            analysis_data: Complete analysis results from specialized agent
            agent_info: Information about the analyzing agent
            
        Returns:
            bytes: PDF content as bytes
        """
        try:
            # Create PDF buffer
            buffer = io.BytesIO()
            
            # Create document
            doc = SimpleDocTemplate(
                buffer,
                pagesize=letter,
                rightMargin=50,
                leftMargin=50,
                topMargin=80,
                bottomMargin=80
            )
            
            # Build story (content)
            story = []
            
            # Title page
            story.extend(self._create_title_page(analysis_data, agent_info))
            story.append(PageBreak())
            
            # Executive summary
            story.extend(self._create_executive_summary(analysis_data))
            story.append(PageBreak())
            
            # Detailed analysis
            story.extend(self._create_detailed_analysis(analysis_data))
            
            # Legal procedures
            if analysis_data.get('procedures'):
                story.append(PageBreak())
                story.extend(self._create_procedures_section(analysis_data))
            
            # Precedent cases
            if analysis_data.get('precedents'):
                story.append(PageBreak())
                story.extend(self._create_precedents_section(analysis_data))
            
            # Recommendations
            story.append(PageBreak())
            story.extend(self._create_recommendations_section(analysis_data))
            
            # Appendices
            story.append(PageBreak())
            story.extend(self._create_appendices(analysis_data))
            
            # Build PDF
            doc.build(story, onFirstPage=self.create_header_footer, 
                     onLaterPages=self.create_header_footer)
            
            # Get PDF bytes
            pdf_bytes = buffer.getvalue()
            buffer.close()
            
            logger.info(f"Generated PDF report: {len(pdf_bytes)} bytes")
            return pdf_bytes
            
        except Exception as e:
            logger.error(f"Error generating PDF: {str(e)}")
            raise

    def _create_title_page(self, analysis_data: Dict[str, Any], 
                          agent_info: Dict[str, Any] = None) -> List:
        """Create title page content"""
        content = []
        
        # Main title
        content.append(Paragraph("BhimLaw AI", self.styles['CustomTitle']))
        content.append(Spacer(1, 20))
        
        # Subtitle
        content.append(Paragraph("Comprehensive Legal Analysis Report", self.styles['CustomSubtitle']))
        content.append(Spacer(1, 40))
        
        # Case information table
        case_info = [
            ['Case Type:', analysis_data.get('case_type', 'General Legal Matter')],
            ['Analysis Date:', datetime.now().strftime('%d %B %Y')],
            ['Analyzing Agent:', analysis_data.get('agent_name', 'BhimLaw AI')],
            ['Specialization:', analysis_data.get('specialization', 'General Legal Practice')],
            ['Report ID:', f"BLA-{datetime.now().strftime('%Y%m%d')}-{analysis_data.get('case_type', 'GEN')[:3].upper()}"]
        ]
        
        case_table = Table(case_info, colWidths=[2*inch, 4*inch])
        case_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), HexColor('#ecf0f1')),
            ('TEXTCOLOR', (0, 0), (-1, -1), black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 11),
            ('GRID', (0, 0), (-1, -1), 1, HexColor('#bdc3c7')),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('ROWBACKGROUNDS', (0, 0), (-1, -1), [HexColor('#ffffff'), HexColor('#f8f9fa')])
        ]))
        
        content.append(case_table)
        content.append(Spacer(1, 60))
        
        # Disclaimer
        disclaimer = """
        <b>LEGAL DISCLAIMER:</b><br/>
        This report is generated by BhimLaw AI for informational purposes only. 
        It does not constitute legal advice and should not be relied upon as a substitute 
        for consultation with qualified legal professionals. The analysis is based on 
        available information and applicable laws as of the report generation date.
        """
        content.append(Paragraph(disclaimer, self.styles['ImportantNote']))
        
        return content

    def _create_executive_summary(self, analysis_data: Dict[str, Any]) -> List:
        """Create executive summary section"""
        content = []
        
        content.append(Paragraph("EXECUTIVE SUMMARY", self.styles['SectionHeading']))
        content.append(Spacer(1, 12))
        
        # Legal issues identified
        if analysis_data.get('legal_issues'):
            content.append(Paragraph("<b>Key Legal Issues Identified:</b>", self.styles['LegalText']))
            for issue in analysis_data['legal_issues']:
                content.append(Paragraph(f"• {issue}", self.styles['LegalText']))
            content.append(Spacer(1, 12))
        
        # Risk assessment summary
        if analysis_data.get('risk_assessment'):
            content.append(Paragraph("<b>Risk Assessment Summary:</b>", self.styles['LegalText']))
            risk_data = analysis_data['risk_assessment']
            for key, value in risk_data.items():
                formatted_key = key.replace('_', ' ').title()
                content.append(Paragraph(f"• <b>{formatted_key}:</b> {value}", self.styles['LegalText']))
            content.append(Spacer(1, 12))
        
        # Primary recommendations
        if analysis_data.get('recommendations'):
            content.append(Paragraph("<b>Primary Recommendations:</b>", self.styles['LegalText']))
            for i, rec in enumerate(analysis_data['recommendations'][:3], 1):
                content.append(Paragraph(f"{i}. {rec}", self.styles['LegalText']))
        
        return content

    def _create_detailed_analysis(self, analysis_data: Dict[str, Any]) -> List:
        """Create detailed analysis section"""
        content = []

        content.append(Paragraph("DETAILED LEGAL ANALYSIS", self.styles['SectionHeading']))
        content.append(Spacer(1, 12))

        # Applicable laws
        if analysis_data.get('applicable_laws'):
            content.append(Paragraph("<b>Applicable Laws and Regulations:</b>", self.styles['LegalText']))
            for law in analysis_data['applicable_laws']:
                content.append(Paragraph(f"• {law}", self.styles['LegalText']))
            content.append(Spacer(1, 12))

        # Legal issues analysis
        if analysis_data.get('legal_issues'):
            content.append(Paragraph("<b>Legal Issues Analysis:</b>", self.styles['LegalText']))
            for issue in analysis_data['legal_issues']:
                content.append(Paragraph(f"<b>{issue}:</b>", self.styles['LegalText']))
                content.append(Paragraph("This legal issue requires careful consideration of applicable statutory provisions and judicial precedents. The analysis involves examining the factual matrix against established legal principles.", self.styles['LegalText']))
                content.append(Spacer(1, 8))

        # Penalties and consequences
        if analysis_data.get('penalties'):
            content.append(Paragraph("<b>Penalties and Legal Consequences:</b>", self.styles['LegalText']))
            for penalty in analysis_data['penalties']:
                content.append(Paragraph(f"• {penalty}", self.styles['LegalText']))
            content.append(Spacer(1, 12))

        return content

    def _create_procedures_section(self, analysis_data: Dict[str, Any]) -> List:
        """Create legal procedures section"""
        content = []

        content.append(Paragraph("LEGAL PROCEDURES", self.styles['SectionHeading']))
        content.append(Spacer(1, 12))

        if analysis_data.get('procedures'):
            content.append(Paragraph("<b>Step-by-Step Legal Procedures:</b>", self.styles['LegalText']))
            content.append(Spacer(1, 8))

            for step in analysis_data['procedures']:
                content.append(Paragraph(step, self.styles['LegalText']))
                content.append(Spacer(1, 4))

        return content

    def _create_precedents_section(self, analysis_data: Dict[str, Any]) -> List:
        """Create precedent cases section"""
        content = []

        content.append(Paragraph("RELEVANT PRECEDENT CASES", self.styles['SectionHeading']))
        content.append(Spacer(1, 12))

        if analysis_data.get('precedents'):
            for precedent in analysis_data['precedents']:
                content.append(Paragraph(f"<b>{precedent.get('case', 'Case Name Not Available')}</b>", self.styles['LegalText']))
                content.append(Paragraph(f"<b>Citation:</b> {precedent.get('citation', 'Citation not available')}", self.styles['LegalText']))
                content.append(Paragraph(f"<b>Relevance:</b> {precedent.get('relevance', 'Relevance not specified')}", self.styles['LegalText']))
                content.append(Paragraph(f"<b>Legal Principle:</b> {precedent.get('principle', 'Principle not specified')}", self.styles['LegalText']))
                content.append(Spacer(1, 12))

        return content

    def _create_recommendations_section(self, analysis_data: Dict[str, Any]) -> List:
        """Create recommendations section"""
        content = []

        content.append(Paragraph("RECOMMENDATIONS & ACTION PLAN", self.styles['SectionHeading']))
        content.append(Spacer(1, 12))

        if analysis_data.get('recommendations'):
            content.append(Paragraph("<b>Recommended Actions:</b>", self.styles['LegalText']))
            content.append(Spacer(1, 8))

            for i, recommendation in enumerate(analysis_data['recommendations'], 1):
                content.append(Paragraph(f"{i}. {recommendation}", self.styles['LegalText']))
                content.append(Spacer(1, 6))

        # Compliance requirements
        if analysis_data.get('compliance_requirements'):
            content.append(Spacer(1, 12))
            content.append(Paragraph("<b>Compliance Requirements:</b>", self.styles['LegalText']))
            for req in analysis_data['compliance_requirements']:
                content.append(Paragraph(f"• {req}", self.styles['LegalText']))

        return content

    def _create_appendices(self, analysis_data: Dict[str, Any]) -> List:
        """Create appendices section"""
        content = []

        content.append(Paragraph("APPENDICES", self.styles['SectionHeading']))
        content.append(Spacer(1, 12))

        # Appendix A - Analysis metadata
        content.append(Paragraph("<b>Appendix A: Analysis Metadata</b>", self.styles['LegalText']))
        content.append(Spacer(1, 8))

        metadata = [
            ['Analysis Timestamp:', analysis_data.get('analysis_timestamp', 'Not available')],
            ['Agent Name:', analysis_data.get('agent_name', 'BhimLaw AI')],
            ['Specialization:', analysis_data.get('specialization', 'General Legal Practice')],
            ['Case Type:', analysis_data.get('case_type', 'General Legal Matter')]
        ]

        metadata_table = Table(metadata, colWidths=[2*inch, 4*inch])
        metadata_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), HexColor('#ecf0f1')),
            ('TEXTCOLOR', (0, 0), (-1, -1), black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 1, HexColor('#bdc3c7')),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE')
        ]))

        content.append(metadata_table)
        content.append(Spacer(1, 20))

        # Appendix B - Important notice
        content.append(Paragraph("<b>Appendix B: Important Legal Notice</b>", self.styles['LegalText']))
        content.append(Spacer(1, 8))

        notice = """
        This analysis is provided by BhimLaw AI, an advanced artificial intelligence system
        designed to assist with legal research and analysis. While every effort has been made
        to ensure accuracy, this report should be reviewed by qualified legal professionals
        before making any legal decisions. Laws and regulations may change, and specific
        circumstances may require different approaches than those suggested in this analysis.

        For complex legal matters, it is strongly recommended to consult with experienced
        legal practitioners who can provide personalized advice based on the complete
        factual and legal context of your specific situation.
        """

        content.append(Paragraph(notice, self.styles['LegalText']))

        return content

    def generate_case_summary_pdf(self, case_data: Dict[str, Any]) -> bytes:
        """Generate a quick case summary PDF"""
        try:
            buffer = io.BytesIO()
            doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=50, leftMargin=50, topMargin=80, bottomMargin=80)

            story = []

            # Title
            story.append(Paragraph("BhimLaw AI - Case Summary", self.styles['CustomTitle']))
            story.append(Spacer(1, 30))

            # Case details
            story.append(Paragraph(f"<b>Case Type:</b> {case_data.get('case_type', 'General')}", self.styles['LegalText']))
            story.append(Paragraph(f"<b>Date:</b> {datetime.now().strftime('%d %B %Y')}", self.styles['LegalText']))
            story.append(Spacer(1, 20))

            # Quick summary
            if case_data.get('legal_issues'):
                story.append(Paragraph("<b>Legal Issues:</b>", self.styles['LegalText']))
                for issue in case_data['legal_issues']:
                    story.append(Paragraph(f"• {issue}", self.styles['LegalText']))

            doc.build(story, onFirstPage=self.create_header_footer, onLaterPages=self.create_header_footer)

            pdf_bytes = buffer.getvalue()
            buffer.close()
            return pdf_bytes

        except Exception as e:
            logger.error(f"Error generating case summary PDF: {str(e)}")
            raise

# Global PDF generator instance
pdf_generator = BhimLawPDFGenerator()