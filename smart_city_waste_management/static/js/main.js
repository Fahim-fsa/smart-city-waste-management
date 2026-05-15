// Smart City Waste Management - Main JS

document.addEventListener('DOMContentLoaded', function () {

    // Auto-dismiss alerts after 4 seconds
    setTimeout(function () {
        document.querySelectorAll('.alert.alert-dismissible').forEach(function (el) {
            var bsAlert = bootstrap.Alert.getOrCreateInstance(el);
            if (bsAlert) bsAlert.close();
        });
    }, 4000);

    // Highlight active sidebar link
    var currentPath = window.location.pathname;
    document.querySelectorAll('.sidebar .nav-link').forEach(function (link) {
        if (link.getAttribute('href') === currentPath) {
            link.classList.add('active');
        }
    });

    // Mobile sidebar toggle
    var sidebarToggle = document.getElementById('sidebarToggle');
    var sidebar = document.querySelector('.sidebar');
    if (sidebarToggle && sidebar) {
        sidebarToggle.addEventListener('click', function () {
            sidebar.classList.toggle('show');
        });
    }

    // Confirm delete actions
    document.querySelectorAll('[data-confirm]').forEach(function (el) {
        el.addEventListener('click', function (e) {
            if (!confirm(el.dataset.confirm || 'Are you sure?')) {
                e.preventDefault();
            }
        });
    });

    // Image preview on file input change
    document.querySelectorAll('input[type="file"]').forEach(function (input) {
        input.addEventListener('change', function () {
            var preview = document.getElementById(input.id + '_preview');
            if (preview && input.files && input.files[0]) {
                var reader = new FileReader();
                reader.onload = function (e) {
                    preview.src = e.target.result;
                    preview.style.display = 'block';
                };
                reader.readAsDataURL(input.files[0]);
            }
        });
    });

    // Waste level slider live label
    var wasteSlider = document.getElementById('id_waste_level');
    if (wasteSlider) {
        var label = document.createElement('span');
        label.className = 'ms-2 fw-bold';
        label.textContent = wasteSlider.value + '%';
        wasteSlider.parentNode.appendChild(label);
        wasteSlider.addEventListener('input', function () {
            label.textContent = wasteSlider.value + '%';
        });
    }

});
