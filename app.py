"""
Aplicación Flask para gestión de matrices de seguridad
ISO 27001, COBIT, MAGERIT y NIST
"""
from flask import Flask, render_template, request, jsonify, send_file
from utils.csv_processor import CSVProcessor
import json
from datetime import datetime
import io
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.units import inch

app = Flask(__name__)
app.config['SECRET_KEY'] = 'tu-clave-secreta-aqui'

# Inicializar procesador de CSV
csv_processor = CSVProcessor()


@app.route('/')
def index():
    """Página principal - Dashboard"""
    return render_template('index.html')


@app.route('/api/data/all')
def get_all_data():
    """API para obtener todos los datos"""
    try:
        data = csv_processor.get_all_data()
        return jsonify({
            'success': True,
            'data': data
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/data/<csv_type>')
def get_csv_data(csv_type):
    """API para obtener datos de un CSV específico"""
    try:
        if csv_type == 'magerit':
            data = csv_processor.get_magerit_data()
        elif csv_type == 'anexo_a':
            data = csv_processor.get_anexo_a_data()
        elif csv_type == 'cobit':
            data = csv_processor.get_cobit_data()
        elif csv_type == 'nist':
            data = csv_processor.get_nist_data()
        else:
            return jsonify({
                'success': False,
                'error': 'Tipo de CSV no válido'
            }), 400
        
        return jsonify({
            'success': True,
            'data': data
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/magerit')
def magerit_view():
    """Vista de MAGERIT"""
    data = csv_processor.get_magerit_data()
    return render_template('magerit.html', data=data)


@app.route('/anexo-a')
def anexo_a_view():
    """Vista de ISO 27001 Anexo A"""
    data = csv_processor.get_anexo_a_data()
    return render_template('anexo_a.html', data=data)


@app.route('/cobit')
def cobit_view():
    """Vista de COBIT"""
    data = csv_processor.get_cobit_data()
    return render_template('cobit.html', data=data)


@app.route('/nist')
def nist_view():
    """Vista de NIST"""
    data = csv_processor.get_nist_data()
    return render_template('nist.html', data=data)


@app.route('/api/magerit/calculate', methods=['POST'])
def calculate_magerit_risk():
    """API para calcular riesgos de MAGERIT"""
    try:
        data = request.json
        frecuencia = float(data.get('frecuencia', 0))
        impacto = float(data.get('impacto', 0))
        salvaguarda_pct = float(data.get('salvaguarda_pct', 0))
        
        result = csv_processor.calculate_magerit_risk(frecuencia, impacto, salvaguarda_pct)
        
        return jsonify({
            'success': True,
            'data': result
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400


@app.route('/api/magerit/update/<int:row_index>', methods=['POST'])
def update_magerit_row(row_index):
    """API para actualizar una fila de MAGERIT"""
    try:
        data = request.json
        updated_row = csv_processor.update_magerit_row(row_index, data)
        
        return jsonify({
            'success': True,
            'message': f'Activo N° {row_index} actualizado correctamente',
            'data': updated_row
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400


@app.route('/api/magerit/add', methods=['POST'])
def add_magerit_asset():
    """API para agregar un nuevo activo a MAGERIT"""
    try:
        data = request.json
        
        # Validar campos requeridos
        required_fields = ['tipo_activo', 'activo', 'amenaza', 'valor_economico', 
                          'frecuencia', 'impacto', 'salvaguarda', 'valor_salvaguarda_pct']
        
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({
                    'success': False,
                    'error': f'Campo requerido faltante: {field}'
                }), 400
        
        new_row = csv_processor.add_magerit_asset(data)
        
        return jsonify({
            'success': True,
            'message': 'Nuevo activo agregado correctamente',
            'data': new_row
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400


@app.route('/reports')
def reports_view():
    """Vista de reportes"""
    return render_template('reports.html')


@app.route('/api/report/generate', methods=['POST'])
def generate_report():
    """Genera un reporte en PDF con todos los datos"""
    try:
        data_request = request.json
        include_sections = data_request.get('sections', ['magerit', 'anexo_a', 'cobit', 'nist'])
        
        # Crear buffer para el PDF
        buffer = io.BytesIO()
        
        # Crear documento PDF
        doc = SimpleDocTemplate(buffer, pagesize=A4)
        elements = []
        styles = getSampleStyleSheet()
        
        # Estilo personalizado para título
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=18,
            textColor=colors.HexColor('#2c3e50'),
            spaceAfter=30
        )
        
        # Título principal
        title = Paragraph("Reporte de Análisis de Seguridad de la Información", title_style)
        elements.append(title)
        elements.append(Spacer(1, 0.2*inch))
        
        # Información del reporte
        date_str = datetime.now().strftime('%d/%m/%Y %H:%M')
        info_text = f"<b>Fecha de generación:</b> {date_str}<br/><b>Proyecto:</b> Geotermia con CNN"
        elements.append(Paragraph(info_text, styles['Normal']))
        elements.append(Spacer(1, 0.3*inch))
        
        # Obtener todos los datos
        all_data = csv_processor.get_all_data()
        
        # MAGERIT
        if 'magerit' in include_sections:
            elements.append(Paragraph("1. Análisis de Riesgos (MAGERIT)", styles['Heading2']))
            elements.append(Spacer(1, 0.1*inch))
            
            magerit_data = all_data['magerit']
            if magerit_data['data']:
                # Preparar datos para la tabla
                table_data = [magerit_data['headers'][:6]]  # Solo primeras 6 columnas
                for row in magerit_data['data']:
                    table_data.append(row[:6])
                
                # Crear tabla
                t = Table(table_data, repeatRows=1)
                t.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 8),
                    ('FONTSIZE', (0, 1), (-1, -1), 7),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black)
                ]))
                elements.append(t)
                elements.append(PageBreak())
        
        # ANEXO A
        if 'anexo_a' in include_sections:
            elements.append(Paragraph("2. Controles ISO 27001 (Anexo A)", styles['Heading2']))
            elements.append(Spacer(1, 0.1*inch))
            
            anexo_data = all_data['anexo_a']
            if anexo_data['data']:
                table_data = [anexo_data['headers'][:4]]
                for row in anexo_data['data'][:10]:  # Primeras 10 filas
                    table_data.append(row[:4])
                
                t = Table(table_data, repeatRows=1, colWidths=[1.5*inch, 1.5*inch, 2*inch, 2*inch])
                t.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3498db')),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 8),
                    ('FONTSIZE', (0, 1), (-1, -1), 6),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.lightblue),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black),
                    ('VALIGN', (0, 0), (-1, -1), 'TOP')
                ]))
                elements.append(t)
                elements.append(PageBreak())
        
        # COBIT
        if 'cobit' in include_sections:
            elements.append(Paragraph("3. Procesos de Gobernanza TI (COBIT)", styles['Heading2']))
            elements.append(Spacer(1, 0.1*inch))
            
            cobit_data = all_data['cobit']
            if cobit_data['data']:
                table_data = [['Proceso', 'Objetivo', 'KPIs']]
                for row in cobit_data['data'][:8]:
                    table_data.append([row[0], row[1][:100] + '...', row[4][:80] + '...'])
                
                t = Table(table_data, repeatRows=1, colWidths=[1.5*inch, 3*inch, 2*inch])
                t.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#e74c3c')),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 8),
                    ('FONTSIZE', (0, 1), (-1, -1), 6),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.lightpink),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black),
                    ('VALIGN', (0, 0), (-1, -1), 'TOP')
                ]))
                elements.append(t)
                elements.append(PageBreak())
        
        # NIST
        if 'nist' in include_sections:
            elements.append(Paragraph("4. Marco de Ciberseguridad (NIST)", styles['Heading2']))
            elements.append(Spacer(1, 0.1*inch))
            
            nist_data = all_data['nist']
            if nist_data['data']:
                table_data = [['Función', 'Control', 'Descripción']]
                for row in nist_data['data']:
                    table_data.append([row[0], row[1], row[2][:100] + '...'])
                
                t = Table(table_data, repeatRows=1, colWidths=[1.5*inch, 2*inch, 3*inch])
                t.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#27ae60')),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 8),
                    ('FONTSIZE', (0, 1), (-1, -1), 6),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.lightgreen),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black),
                    ('VALIGN', (0, 0), (-1, -1), 'TOP')
                ]))
                elements.append(t)
        
        # Construir PDF
        doc.build(elements)
        buffer.seek(0)
        
        # Enviar archivo
        filename = f"reporte_seguridad_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        return send_file(
            buffer,
            as_attachment=True,
            download_name=filename,
            mimetype='application/pdf'
        )
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
