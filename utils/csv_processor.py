"""
Módulo para procesar y calcular datos de los CSV de seguridad
"""
import csv
import os
from typing import List, Dict, Any


class CSVProcessor:
    """Clase para manejar operaciones con los CSV"""
    
    def __init__(self, base_path: str = '.'):
        self.base_path = base_path
        self.csv_files = {
            'magerit': 'Matiz(MAGERIT).csv',
            'anexo_a': 'Matiz(Anexo A).csv',
            'cobit': 'Matiz(COBIT).csv',
            'nist': 'Matiz(NIST).csv'
        }
    
    def read_csv(self, csv_type: str, encoding: str = 'utf-8-sig') -> List[List[str]]:
        """Lee un archivo CSV y retorna todas las filas"""
        file_path = os.path.join(self.base_path, self.csv_files[csv_type])
        
        try:
            with open(file_path, 'r', encoding=encoding) as f:
                reader = csv.reader(f)
                return list(reader)
        except UnicodeDecodeError:
            # Intentar con latin-1 si utf-8 falla
            with open(file_path, 'r', encoding='latin-1') as f:
                reader = csv.reader(f)
                return list(reader)
    
    def write_csv(self, csv_type: str, data: List[List[str]], encoding: str = 'utf-8-sig'):
        """Escribe datos en un archivo CSV"""
        file_path = os.path.join(self.base_path, self.csv_files[csv_type])
        
        with open(file_path, 'w', encoding=encoding, newline='') as f:
            writer = csv.writer(f)
            writer.writerows(data)
    
    def get_magerit_data(self) -> Dict[str, Any]:
        """
        Obtiene y procesa los datos de MAGERIT
        Retorna información estructurada con los activos y sus riesgos
        """
        rows = self.read_csv('magerit')
        
        # Buscar la fila de encabezados
        header_row_idx = None
        for idx, row in enumerate(rows):
            if len(row) > 0 and row[0] == 'N° Activos':
                header_row_idx = idx
                break
        
        if header_row_idx is None:
            return {'header': [], 'data': [], 'metadata': rows[:8]}
        
        headers = rows[header_row_idx]
        data_rows = []
        
        # Procesar filas de datos
        for row in rows[header_row_idx + 1:]:
            if len(row) > 0 and row[0] and row[0].strip():
                data_rows.append(row)
        
        return {
            'metadata': rows[:header_row_idx],
            'headers': headers,
            'data': data_rows
        }
    
    def calculate_magerit_risk(self, frecuencia: float, impacto: float, 
                               salvaguarda_pct: float) -> Dict[str, float]:
        """
        Calcula el riesgo intrínseco y residual según la metodología MAGERIT
        
        Args:
            frecuencia: Valor de frecuencia (ej: 1 para cada 3 meses)
            impacto: Valor de impacto (ej: 3.5 para muy alto)
            salvaguarda_pct: Porcentaje de efectividad de la salvaguarda (0-100)
        
        Returns:
            Dict con riesgo_intrinseco y riesgo_residual
        """
        riesgo_intrinseco = frecuencia * impacto
        valor_salvaguarda = riesgo_intrinseco * (salvaguarda_pct / 100)
        riesgo_residual = riesgo_intrinseco - valor_salvaguarda
        
        return {
            'riesgo_intrinseco': round(riesgo_intrinseco, 2),
            'riesgo_residual': round(riesgo_residual, 2)
        }
    
    def update_magerit_row(self, row_index: int, updated_data: Dict[str, Any]):
        """
        Actualiza una fila de MAGERIT y recalcula los riesgos
        
        Args:
            row_index: Índice de la fila a actualizar (basado en N° Activos)
            updated_data: Diccionario con los campos a actualizar
        """
        rows = self.read_csv('magerit')
        
        # Encontrar la fila de encabezados
        header_row_idx = None
        for idx, row in enumerate(rows):
            if len(row) > 0 and row[0] == 'N° Activos':
                header_row_idx = idx
                break
        
        if header_row_idx is None:
            raise ValueError("No se encontraron los encabezados en MAGERIT")
        
        # Encontrar la fila de datos
        data_start_idx = header_row_idx + 1
        target_row_idx = None
        
        for idx, row in enumerate(rows[data_start_idx:], start=data_start_idx):
            if len(row) > 0 and row[0] == str(row_index):
                target_row_idx = idx
                break
        
        if target_row_idx is None:
            raise ValueError(f"No se encontró el activo N° {row_index}")
        
        # Actualizar los campos
        row = rows[target_row_idx]
        
        if 'valor_economico' in updated_data:
            row[4] = updated_data['valor_economico']
        if 'frecuencia' in updated_data:
            row[5] = str(updated_data['frecuencia'])
        if 'impacto' in updated_data:
            row[6] = str(updated_data['impacto'])
        if 'salvaguarda' in updated_data:
            row[8] = updated_data['salvaguarda']
        if 'valor_salvaguarda' in updated_data:
            row[9] = updated_data['valor_salvaguarda']
        
        # Recalcular riesgos si tenemos los valores necesarios
        try:
            frecuencia = float(updated_data.get('frecuencia', row[5]))
            impacto = float(str(updated_data.get('impacto', row[6])).replace(',', '.'))
            salvaguarda_str = updated_data.get('valor_salvaguarda', row[9])
            
            # Extraer porcentaje de salvaguarda
            salvaguarda_pct = 0
            if '%' in str(salvaguarda_str):
                salvaguarda_pct = float(str(salvaguarda_str).split(':')[1].strip().replace('%', ''))
            
            # Calcular riesgos
            risks = self.calculate_magerit_risk(frecuencia, impacto, salvaguarda_pct)
            
            # Actualizar las columnas de riesgo
            row[7] = f"{frecuencia} * {impacto} = {risks['riesgo_intrinseco']}"
            row[10] = f"{risks['riesgo_intrinseco']} - {risks['riesgo_intrinseco'] * salvaguarda_pct / 100:.2f} = {risks['riesgo_residual']} (Riesgo {'Bajo' if risks['riesgo_residual'] < 2 else 'Medio-Bajo' if risks['riesgo_residual'] < 3 else 'Alto'})"
            
        except (ValueError, IndexError) as e:
            print(f"Error al calcular riesgos: {e}")
        
        # Guardar cambios
        self.write_csv('magerit', rows)
        
        return rows[target_row_idx]
    
    def add_magerit_asset(self, asset_data: Dict[str, Any]):
        """
        Agrega un nuevo activo a MAGERIT
        
        Args:
            asset_data: Diccionario con los datos del nuevo activo
                - tipo_activo: Tipo de activo
                - activo: Nombre del activo
                - amenaza: Amenaza identificada
                - valor_economico: Valor económico
                - frecuencia: Frecuencia de la amenaza
                - impacto: Impacto de la amenaza
                - salvaguarda: Salvaguardas implementadas
                - valor_salvaguarda_pct: Porcentaje de efectividad de salvaguarda
        """
        rows = self.read_csv('magerit')
        
        # Encontrar la fila de encabezados
        header_row_idx = None
        for idx, row in enumerate(rows):
            if len(row) > 0 and row[0] == 'N° Activos':
                header_row_idx = idx
                break
        
        if header_row_idx is None:
            raise ValueError("No se encontraron los encabezados en MAGERIT")
        
        # Encontrar el último número de activo
        max_activo_num = 0
        data_start_idx = header_row_idx + 1
        
        for row in rows[data_start_idx:]:
            if len(row) > 0 and row[0] and row[0].strip().isdigit():
                max_activo_num = max(max_activo_num, int(row[0]))
        
        # Nuevo número de activo
        new_activo_num = max_activo_num + 1
        
        # Calcular riesgos
        frecuencia = float(asset_data['frecuencia'])
        impacto = float(asset_data['impacto'])
        salvaguarda_pct = float(asset_data['valor_salvaguarda_pct'])
        
        risks = self.calculate_magerit_risk(frecuencia, impacto, salvaguarda_pct)
        
        # Clasificar el riesgo residual
        if risks['riesgo_residual'] < 2:
            clasificacion = "Riesgo Bajo"
        elif risks['riesgo_residual'] < 3:
            clasificacion = "Riesgo Medio-Bajo"
        elif risks['riesgo_residual'] < 4:
            clasificacion = "Riesgo Medio-Alto"
        else:
            clasificacion = "Riesgo Alto"
        
        # Determinar nivel de impacto en texto
        if impacto <= 1.5:
            nivel_impacto = "Bajo"
        elif impacto <= 2.5:
            nivel_impacto = "Normal"
        elif impacto <= 3.5:
            nivel_impacto = "Alto"
        else:
            nivel_impacto = "Muy Alto"
        
        # Determinar nivel de salvaguarda
        if salvaguarda_pct >= 80:
            nivel_salvaguarda = "Muy alto"
        elif salvaguarda_pct >= 60:
            nivel_salvaguarda = "Alto"
        elif salvaguarda_pct >= 40:
            nivel_salvaguarda = "Normal"
        else:
            nivel_salvaguarda = "Bajo"
        
        # Crear nueva fila
        new_row = [
            str(new_activo_num),
            asset_data['tipo_activo'],
            asset_data['activo'],
            asset_data['amenaza'],
            asset_data['valor_economico'],
            asset_data.get('frecuencia_texto', str(frecuencia)),
            f"{nivel_impacto}: {impacto}".replace('.', ','),
            f"{frecuencia} * {impacto} = {risks['riesgo_intrinseco']}".replace('.', ','),
            asset_data['salvaguarda'],
            f"{nivel_salvaguarda}: {salvaguarda_pct:.0f}%",
            f"{risks['riesgo_intrinseco']} - {risks['riesgo_intrinseco'] * salvaguarda_pct / 100:.2f} = {risks['riesgo_residual']} ({clasificacion})".replace('.', ',')
        ]
        
        # Encontrar la primera fila vacía después de los datos
        insert_idx = data_start_idx
        for idx in range(data_start_idx, len(rows)):
            if len(rows[idx]) > 0 and rows[idx][0] and rows[idx][0].strip():
                insert_idx = idx + 1
            else:
                break
        
        # Insertar la nueva fila
        rows.insert(insert_idx, new_row)
        
        # Guardar cambios
        self.write_csv('magerit', rows)
        
        return new_row
    
    def get_anexo_a_data(self) -> Dict[str, Any]:
        """Obtiene y estructura los datos de ISO 27001 (Anexo A)"""
        rows = self.read_csv('anexo_a')
        
        # Buscar encabezados
        header_row_idx = None
        for idx, row in enumerate(rows):
            if len(row) > 0 and row[0] == 'Categoría':
                header_row_idx = idx
                break
        
        if header_row_idx is None:
            return {'header': [], 'data': [], 'metadata': rows[:6]}
        
        return {
            'metadata': rows[:header_row_idx],
            'headers': rows[header_row_idx],
            'data': [row for row in rows[header_row_idx + 1:] if len(row) > 0 and row[0]]
        }
    
    def get_cobit_data(self) -> Dict[str, Any]:
        """Obtiene y estructura los datos de COBIT"""
        rows = self.read_csv('cobit')
        
        # Buscar encabezados
        header_row_idx = None
        for idx, row in enumerate(rows):
            if len(row) > 0 and row[0] == 'Proceso COBIT':
                header_row_idx = idx
                break
        
        if header_row_idx is None:
            return {'header': [], 'data': [], 'metadata': rows[:6]}
        
        return {
            'metadata': rows[:header_row_idx],
            'headers': rows[header_row_idx],
            'data': [row for row in rows[header_row_idx + 1:] if len(row) > 0 and row[0]]
        }
    
    def get_nist_data(self) -> Dict[str, Any]:
        """Obtiene y estructura los datos de NIST"""
        rows = self.read_csv('nist')
        
        # Buscar encabezados
        header_row_idx = None
        for idx, row in enumerate(rows):
            if len(row) > 0 and row[0] == 'Función NIST':
                header_row_idx = idx
                break
        
        if header_row_idx is None:
            return {'header': [], 'data': [], 'metadata': rows[:4]}
        
        return {
            'metadata': rows[:header_row_idx],
            'headers': rows[header_row_idx],
            'data': [row for row in rows[header_row_idx + 1:] if len(row) > 0 and row[0]]
        }
    
    def get_all_data(self) -> Dict[str, Dict[str, Any]]:
        """Obtiene todos los datos de los 4 CSV"""
        return {
            'magerit': self.get_magerit_data(),
            'anexo_a': self.get_anexo_a_data(),
            'cobit': self.get_cobit_data(),
            'nist': self.get_nist_data()
        }
