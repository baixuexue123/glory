import mistune
from mistune import escape
from lxml.html.clean import clean_html

from django import template
from django.utils.safestring import mark_safe

register = template.Library()


class HighlightRenderer(mistune.Renderer):
    def block_code(self, code, lang=None):
        """Rendering block level code. ``pre > code``.

        :param code: text content of the code block.
        :param lang: language of the given code.
        """
        code = code.rstrip('\n')
        if not lang:
            code = escape(code, smart_amp=False)
            return '<pre><code class="nohighlight">%s\n</code></pre>\n' % code
        code = escape(code, quote=True, smart_amp=False)
        return '<pre><code class="%s">%s\n</code></pre>\n' % (lang, code)


@register.filter
def markup(value, md=mistune.Markdown(escape=True, renderer=HighlightRenderer())):
    return mark_safe(md(value))


@register.filter
def safe_exclude(text):
    # eg: {{ post.text|safe_exclude|safe }}
    return clean_html(text)
