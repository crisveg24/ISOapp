// Funciones utilitarias y globales para ISOapp

// Animación de números al cargar
function animateValue(id, start, end, duration) {
    const obj = document.getElementById(id);
    if (!obj) return;
    
    const range = end - start;
    const increment = end > start ? 1 : -1;
    const stepTime = Math.abs(Math.floor(duration / range));
    let current = start;
    
    const timer = setInterval(() => {
        current += increment;
        obj.textContent = current;
        if (current === end) {
            clearInterval(timer);
        }
    }, stepTime);
}

// Notificaciones toast
function showToast(message, type = 'info') {
    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    toast.innerHTML = `
        <i class="fas fa-${type === 'success' ? 'check-circle' : type === 'error' ? 'times-circle' : 'info-circle'}"></i>
        <span>${message}</span>
    `;
    
    // Estilos inline para toast
    toast.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: ${type === 'success' ? '#27ae60' : type === 'error' ? '#e74c3c' : '#3498db'};
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 5px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.2);
        z-index: 10000;
        display: flex;
        align-items: center;
        gap: 0.75rem;
        animation: slideInRight 0.3s;
    `;
    
    document.body.appendChild(toast);
    
    setTimeout(() => {
        toast.style.animation = 'slideOutRight 0.3s';
        setTimeout(() => toast.remove(), 300);
    }, 3000);
}

// Formatear números
function formatNumber(num) {
    return new Intl.NumberFormat('es-CO').format(num);
}

// Formatear moneda COP
function formatCurrency(amount) {
    return new Intl.NumberFormat('es-CO', {
        style: 'currency',
        currency: 'COP',
        minimumFractionDigits: 0
    }).format(amount);
}

// Validar formulario
function validateForm(formId) {
    const form = document.getElementById(formId);
    if (!form) return false;
    
    const inputs = form.querySelectorAll('input[required], textarea[required], select[required]');
    let isValid = true;
    
    inputs.forEach(input => {
        if (!input.value.trim()) {
            input.style.borderColor = '#e74c3c';
            isValid = false;
        } else {
            input.style.borderColor = '#bdc3c7';
        }
    });
    
    return isValid;
}

// Exportar tabla a CSV
function exportTableToCSV(tableId, filename = 'export.csv') {
    const table = document.getElementById(tableId);
    if (!table) return;
    
    let csv = [];
    const rows = table.querySelectorAll('tr');
    
    rows.forEach(row => {
        const cols = row.querySelectorAll('td, th');
        const rowData = Array.from(cols).map(col => {
            let text = col.textContent.trim();
            return `"${text.replace(/"/g, '""')}"`;
        });
        csv.push(rowData.join(','));
    });
    
    const csvContent = csv.join('\n');
    const blob = new Blob(['\ufeff' + csvContent], { type: 'text/csv;charset=utf-8;' });
    const link = document.createElement('a');
    const url = URL.createObjectURL(blob);
    
    link.setAttribute('href', url);
    link.setAttribute('download', filename);
    link.style.visibility = 'hidden';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
}

// Buscar en tabla
function searchTable(tableId, searchInputId) {
    const input = document.getElementById(searchInputId);
    const table = document.getElementById(tableId);
    
    if (!input || !table) return;
    
    input.addEventListener('keyup', function() {
        const filter = this.value.toLowerCase();
        const rows = table.querySelectorAll('tbody tr');
        
        rows.forEach(row => {
            const text = row.textContent.toLowerCase();
            row.style.display = text.includes(filter) ? '' : 'none';
        });
    });
}

// Copiar al portapapeles
function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(() => {
        showToast('Copiado al portapapeles', 'success');
    }).catch(err => {
        showToast('Error al copiar', 'error');
    });
}

// Confirmar acción
function confirmAction(message, callback) {
    if (confirm(message)) {
        callback();
    }
}

// Loader global
function showLoader() {
    const loader = document.createElement('div');
    loader.id = 'globalLoader';
    loader.innerHTML = `
        <div style="
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0,0,0,0.5);
            display: flex;
            justify-content: center;
            align-items: center;
            z-index: 9999;
        ">
            <div class="spinner"></div>
        </div>
    `;
    document.body.appendChild(loader);
}

function hideLoader() {
    const loader = document.getElementById('globalLoader');
    if (loader) loader.remove();
}

// Scroll suave
function smoothScrollTo(elementId) {
    const element = document.getElementById(elementId);
    if (element) {
        element.scrollIntoView({
            behavior: 'smooth',
            block: 'start'
        });
    }
}

// Detección de tema oscuro/claro
function detectColorScheme() {
    if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
        return 'dark';
    }
    return 'light';
}

// Añadir animaciones CSS dinamicamente
const style = document.createElement('style');
style.textContent = `
    @keyframes slideInRight {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes slideOutRight {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(100%);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);

// Inicialización al cargar la página
document.addEventListener('DOMContentLoaded', function() {
    console.log('ISOapp iniciada correctamente');
    
    // Añadir tooltips automáticamente
    const elements = document.querySelectorAll('[title]');
    elements.forEach(el => {
        el.style.cursor = 'help';
    });
    
    // Auto-close alerts
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.animation = 'fadeOut 0.3s';
            setTimeout(() => alert.remove(), 300);
        }, 5000);
    });
});

// Manejo de errores global
window.addEventListener('error', function(e) {
    console.error('Error global:', e.error);
});

// Prevenir pérdida de datos en formularios
window.addEventListener('beforeunload', function(e) {
    const forms = document.querySelectorAll('form');
    let hasChanges = false;
    
    forms.forEach(form => {
        if (form.dataset.changed === 'true') {
            hasChanges = true;
        }
    });
    
    if (hasChanges) {
        e.preventDefault();
        e.returnValue = '';
    }
});

// Marcar formularios como modificados
document.querySelectorAll('form input, form textarea, form select').forEach(field => {
    field.addEventListener('change', function() {
        this.closest('form').dataset.changed = 'true';
    });
});

// Exportar funciones
window.ISOapp = {
    animateValue,
    showToast,
    formatNumber,
    formatCurrency,
    validateForm,
    exportTableToCSV,
    searchTable,
    copyToClipboard,
    confirmAction,
    showLoader,
    hideLoader,
    smoothScrollTo,
    detectColorScheme
};
