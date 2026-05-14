from django.forms.widgets import ClearableFileInput
from django.utils.html import format_html

class VideoUploadWidget(ClearableFileInput):

    def render(self, name, value, attrs=None, renderer=None):
        # Render the original file input from parent
        original = super().render(name, value, attrs, renderer)

        progress_html = format_html('''
            <div id="upload-progress-wrap-{name}"
                 style="display:none; margin-top:10px; max-width:420px;">
              <div style="font-size:12px; color:#666; margin-bottom:5px;">
                Uploading… <span id="upload-percent-{name}">0%</span>
              </div>
              <div style="background:#e0e0e0; border-radius:4px;
                          height:6px; width:100%; overflow:hidden;">
                <div id="upload-bar-{name}"
                     style="height:6px; width:0%; background:#417690;
                            border-radius:4px; transition:width 0.15s ease;">
                </div>
              </div>
              <div id="upload-status-{name}"
                   style="font-size:12px; color:#666; margin-top:5px;"></div>
            </div>
        ''', name=name)

        return original + progress_html