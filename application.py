import requests

import sublime
import sublime_plugin


LEXERS = {
    'c': 'c',
    'py': 'python',
    'java': 'java',
    'rs': 'rust',
    'go': 'go',
    'hs': 'haskell'
}


def push_to_dpaste(to_paste, extension):
    try:
        req = requests.post(
            "https://dpaste.org/api/",
            data={
                "content": to_paste,
                "format": "url",
                "lexer": LEXERS.get(extension, '_text'),
                "expires": "604800"
            }
        )
        url = req.text.strip()
        sublime.set_clipboard(url)
        sublime.status_message(
            'dpaste URL copied to clipboard: {}'.format(url)
        )
    except requests.exceptions.RequestException:
        sublime.status_message(
            'dpaste URL copying failed'
        )


class DpasteCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        selection = self.view.sel()
        to_paste = '\n\n'.join(self.view.substr(x) for x in selection if not x.empty())
        filename = self.view.file_name()
        extension = filename.split('.')[-1]
        push_to_dpaste(to_paste, extension)
  

