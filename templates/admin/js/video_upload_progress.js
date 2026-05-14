(function () {
  'use strict';

  function getCookie(name) {
    const match = document.cookie.match(new RegExp('(^| )' + name + '=([^;]+)'));
    return match ? decodeURIComponent(match[2]) : null;
  }

  function attachProgressToFileInput(input) {
    if (input.dataset.progressAttached) return;
    input.dataset.progressAttached = 'true';

    // Derive the name suffix used in our widget's IDs
    const name = input.name;
    const wrap   = document.getElementById('upload-progress-wrap-' + name);
    const bar    = document.getElementById('upload-bar-' + name);
    const pct    = document.getElementById('upload-percent-' + name);
    const status = document.getElementById('upload-status-' + name);

    if (!wrap) return;

    input.addEventListener('change', function () {
      // Reset bar when a new file is chosen
      bar.style.width = '0%';
      pct.textContent = '0%';
      status.textContent = '';
      wrap.style.display = 'none';
    });

    const form = input.closest('form');
    if (!form || form.dataset.xhrAttached) return;
    form.dataset.xhrAttached = 'true';

    form.addEventListener('submit', function (e) {
      // Only intercept if at least one file input has a file
      const fileInputs = form.querySelectorAll('input[type="file"]');
      let hasFile = false;
      fileInputs.forEach(function (inp) {
        if (inp.files && inp.files.length > 0) hasFile = true;
      });
      if (!hasFile) return; // let normal submit handle saves with no new files

      e.preventDefault();

      // Show all progress bars for file inputs that have files
      fileInputs.forEach(function (inp) {
        if (inp.files && inp.files.length > 0) {
          const w = document.getElementById('upload-progress-wrap-' + inp.name);
          if (w) w.style.display = 'block';
        }
      });

      const formData = new FormData(form);
      const xhr = new XMLHttpRequest();

      xhr.upload.addEventListener('progress', function (ev) {
        if (!ev.lengthComputable) return;
        const percent = Math.round((ev.loaded / ev.total) * 100);

        fileInputs.forEach(function (inp) {
          if (inp.files && inp.files.length > 0) {
            const b = document.getElementById('upload-bar-' + inp.name);
            const p = document.getElementById('upload-percent-' + inp.name);
            const s = document.getElementById('upload-status-' + inp.name);
            if (b) b.style.width = percent + '%';
            if (p) p.textContent = percent + '%';
            if (s && percent === 100) {
              s.textContent = 'Processing… compressing video, please wait.';
            }
          }
        });
      });

      xhr.addEventListener('load', function () {
        // Django admin redirects to the changelist on success
        if (xhr.responseURL && xhr.responseURL !== window.location.href) {
          window.location.href = xhr.responseURL;
        } else {
          window.location.reload();
        }
      });

      xhr.addEventListener('error', function () {
        fileInputs.forEach(function (inp) {
          if (inp.files && inp.files.length > 0) {
            const b = document.getElementById('upload-bar-' + inp.name);
            const s = document.getElementById('upload-status-' + inp.name);
            if (b) b.style.background = '#ba2121';
            if (s) s.textContent = 'Upload failed — please try again.';
          }
        });
      });

      xhr.open('POST', form.action || window.location.href);
      xhr.setRequestHeader('X-CSRFToken', getCookie('csrftoken'));
      xhr.send(formData);
    });
  }

  function init() {
    // Attach to all existing file inputs
    document.querySelectorAll('input[type="file"]').forEach(attachProgressToFileInput);

    // Also attach to dynamically added inline rows (Django's "Add another" button)
    const observer = new MutationObserver(function (mutations) {
      mutations.forEach(function (mutation) {
        mutation.addedNodes.forEach(function (node) {
          if (node.nodeType !== 1) return;
          node.querySelectorAll('input[type="file"]').forEach(attachProgressToFileInput);
        });
      });
    });

    observer.observe(document.body, { childList: true, subtree: true });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();