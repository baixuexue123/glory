import markdown

import mistune
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import html


# markdown.markdownFromFile('python.md', output='python.html',
#                           extensions=['extra', 'codehilite', 'toc'])
#
# markdown.markdownFromFile('sql.md', output='sql.html',
#                           extensions=['extra', 'codehilite', 'toc'])


# class HighlightRenderer(mistune.Renderer):
#     def block_code(self, code, lang=None):
#         if not lang:
#             return '\n<pre><code>%s</code></pre>\n' % \
#                 mistune.escape(code)
#         lexer = get_lexer_by_name(lang, stripall=True)
#         fmter = html.HtmlFormatter()
#         return highlight(code, lexer, fmter)
#
#
# renderer = HighlightRenderer()
# markdown = mistune.Markdown(renderer=renderer)
# print(markdown('```python\nassert 1 == 1\n```'))


print(mistune.markdown('```python\nassert 1 == 1\n```'))
print()
print(markdown.markdown('```python\nassert 1 == 1\n```', extensions=['extra']))
