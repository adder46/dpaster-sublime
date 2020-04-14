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

LEXER = __file__.split('.')[-1]


def push_to_dpaste(to_paste):
    try:
        req = requests.post(
            "https://dpaste.org/api/",
            data={
                "content": to_paste,
                "format": "url",
                "lexer": LEXERS[LEXER],
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


class DpasteFileCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        with open(__file__, 'r') as f:
            to_paste = f.read()
        push_to_dpaste(to_paste)



class DpasteSelectionCommand(sublime_plugin.WindowCommand):

    def run(self):
        view = self.window.active_view()
        selection = view.sel()
        to_paste = '\n\n'.join(view.substr(x) for x in selection)
        push_to_dpaste(to_paste)
  

