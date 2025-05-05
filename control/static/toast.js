function showToast(message, type = 'info', title='') {
    const toastContainer = document.getElementById('toastContainer');

    let bg;
    switch (type) {
        case 'info': bg = 'primary'; break;
        case 'error': bg = 'danger'; break;
        case 'danger': bg = 'danger'; break;
        case 'success': bg = 'success'; break;
        case 'warning': bg = 'warning'; break;
        default: bg = 'primary';
    }

    const toast = document.createElement('div');
    toast.className = `toast text-white bg-${bg} border-0`;
    toast.setAttribute('role', 'alert');
    toast.setAttribute('aria-live', 'assertive');
    toast.setAttribute('aria-atomic', 'true');

    const titleElement = title ? `<strong class="me-auto">${title}</strong>` : '';

    let toastContent;
    if (title) {
        toastContent = `
            <div class="toast-header text-white bg-${bg} border-0">
                <strong class="me-auto">${title}</strong>
                <button type="button" class="btn-close btn-close-white" data-bs-dismiss="toast" aria-label="Close"></button>
            </div>
            <div class="toast-body">
                ${message}
            </div>
        `;
    } else {
        toastContent = `
            <div class="toast-body position-relative">
                ${message}
                <button type="button" class="btn-close btn-close-white position-absolute top-0 end-0 mt-2 me-2" data-bs-dismiss="toast" aria-label="Close"></button>
            </div>
        `;
    }

    toast.innerHTML = toastContent;
    toastContainer.appendChild(toast);

    // Initialize the toast with autohide set to true
    const bsToast = new bootstrap.Toast(toast, {
        autohide: true
    });
    bsToast.show();

    // Remove the toast when it's manually closed
    toast.addEventListener('hidden.bs.toast', function () {
        toast.remove();
    });
}

document.addEventListener('DOMContentLoaded', function() {
    const url_params = new URLSearchParams(window.location.search);
    const toast_message = url_params.get('toast_message');
    const toast_status = url_params.get('toast_status');
    const toast_title = url_params.get('toast_title');


    if (toast_message) {
        showToast(toast_message, toast_status, toast_title);
    }
});