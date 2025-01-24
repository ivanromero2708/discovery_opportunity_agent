# src/utils/report_generator.py
from docx import Document
from docx.shared import Pt
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT

def convert_markdown_to_word(report: str, industry: str, region: str) -> str:
    """
    Convierte un reporte en formato Markdown a un documento Word con formato profesional.
    
    Args:
        report (str): Contenido del reporte en Markdown
        industry (str): Industria objetivo
        region (str): Región objetivo
    
    Returns:
        str: Ruta del archivo generado
    """
    try:
        doc = Document()
        
        # Configuración de estilos
        styles = doc.styles
        heading_style = styles['Heading 1']
        heading_font = heading_style.font
        heading_font.name = 'Arial'
        heading_font.size = Pt(16)
        heading_font.bold = True

        # Metadatos del documento
        doc.core_properties.title = f"Market Research Report - {industry} - {region}"
        doc.core_properties.author = "AI Research Assistant"

        # Procesar contenido
        lines = report.split('\n')
        current_section = None
        
        for line in lines:
            line = line.strip()
            if not line:
                continue

            # Manejo de encabezados
            if line.startswith('# '):
                current_section = doc.add_heading(line[2:], level=1)
            elif line.startswith('## '):
                current_section = doc.add_heading(line[3:], level=2)
            elif line.startswith('### '):
                current_section = doc.add_heading(line[4:], level=3)
            else:
                # Texto normal con formato
                para = doc.add_paragraph()
                para.add_run(line).font.size = Pt(11)
                
                # Alineación justificada para texto normal
                para.alignment = WD_PARAGRAPH_ALIGNMENT.JUSTIFY

        # Generar nombre de archivo seguro
        filename = f"reports/Market_Research_{industry.replace(' ', '_')}_{region.replace(' ', '_')}.docx"
        doc.save(filename)
        
        return filename
        
    except Exception as e:
        raise RuntimeError(f"Error en la generación de Word: {str(e)}")