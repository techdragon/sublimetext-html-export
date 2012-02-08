import sublime, sublime_plugin
import webbrowser
import tempfile
import os

LANGUAGES = {
    'c': 'clike',
    'cc': 'clike',
    'cpp': 'clike',
    'cs': 'clike',
    'coffee': 'coffeescript',
    'css': 'css',
    'diff': 'diff',
    'go': 'go',
    'html': 'htmlmixed',
    'htm': 'htmlmixed',
    'js': 'javascript',
    'less': 'less',
    'lua': 'lua',
    'md': 'markdown',
    'markdown': 'markdown',
    'pl': 'perl',
    'php': 'php',
    'py': 'python',
    'pl': 'perl',
    'rb': 'ruby',
    'xml': 'xml',
    'xsl': 'xml',
    'xslt': 'xml'
}

DEPENDENCIES = {
    'php': ['xml', 'javascript', 'css'],
    'markdown': ['xml'],
    'htmlmixed': ['xml', 'javascript', 'css']
}


class HtmlExportCommand(sublime_plugin.TextCommand):
    """ Export file contents to a single HTML file"""
    def run(self, edit):
        region = sublime.Region(0, self.view.size())
        encoding = self.view.encoding()
        if encoding == 'Undefined':
            encoding = 'UTF-8'
        contents = self.view.substr(region)
        tmp_html = tempfile.NamedTemporaryFile(delete=False, suffix='.html')
        tmp_html.write('<meta charset="%s">' % self.view.encoding())
        plugin_dir = os.path.join(sublime.packages_path(), 'Html Export')
        filename = self.view.file_name()
        language = None
        if filename:
            fileext = os.path.splitext(filename)[1][1:]
            language = LANGUAGES.get(fileext.lower())
        else:
            filename = 'unamed file'
        js = open(os.path.join(plugin_dir, 'codemirror', 'lib', 'codemirror.js'), 'r').read()
        if language:
            if DEPENDENCIES.get(language):
                for dependency in DEPENDENCIES.get(language):
                    js += open(os.path.join(plugin_dir, 'codemirror', 'mode', dependency, '%s.js' % dependency), 'r').read()
            js += open(os.path.join(plugin_dir, 'codemirror', 'mode', language, '%s.js' % language), 'r').read()
        css = open(os.path.join(plugin_dir, 'codemirror', 'lib', 'codemirror.css'), 'r').read()

        datas = {
             'title': os.path.basename(filename),
             'css': css,
             'js': js,
             'code': contents
        }
        # theme
        # <link rel="stylesheet" href="../theme/elegant.css">
        html = u"""
            <!doctype html>
            <html>
              <head>
                <title>%(title)s</title>
                <script>%(js)s</script>
                <style>%(css)s</style>
                <style>.CodeMirror-scroll {overflow:visible}</style>
              </head>
              <body>
                <h3>%(title)s</h3>
                <textarea id="code" name="code">%(code)s</textarea>
                <script>
                var editor = CodeMirror.fromTextArea(document.getElementById("code"), {
                    lineNumbers: true
                });
                </script>
              </body>
            </html>
        """ % datas
        tmp_html.write(html.encode(encoding))
        tmp_html.close()
        webbrowser.open_new_tab(tmp_html.name)
