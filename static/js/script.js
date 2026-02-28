// Global utility functions
class SmartCourseUtils {
    static formatDate(dateString) {
        const date = new Date(dateString);
        return date.toLocaleString();
    }

    static showToast(message, type = 'info') {
        // Create toast element
        const toastContainer = document.getElementById('toastContainer') || this.createToastContainer();
        const toast = document.createElement('div');
        toast.className = `toast align-items-center text-bg-${type} border-0`;
        toast.innerHTML = `
            <div class="d-flex">
                <div class="toast-body">${message}</div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
            </div>
        `;
        toastContainer.appendChild(toast);
        
        const bsToast = new bootstrap.Toast(toast);
        bsToast.show();
        
        // Remove toast after hide
        toast.addEventListener('hidden.bs.toast', () => {
            toast.remove();
        });
    }

    static createToastContainer() {
        const container = document.createElement('div');
        container.id = 'toastContainer';
        container.className = 'toast-container position-fixed top-0 end-0 p-3';
        container.style.zIndex = '9999';
        document.body.appendChild(container);
        return container;
    }
}