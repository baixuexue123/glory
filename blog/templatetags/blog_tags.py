import mistune
from mistune import escape
from bs4 import BeautifulSoup

from django import template
from django.utils.safestring import mark_safe
from django.utils.html import escape

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


INVALID_TAGS = ('script',)


def clean_html(value):
    soup = BeautifulSoup(value)
    for tag in soup.findAll(True):
        if tag.name in INVALID_TAGS:
            tag.replaceWith(escape(tag))
    return soup.renderContents()


@register.filter
def safe_exclude(text):
    # eg: {{ post.description|safe_exclude|safe }}
    return clean_html(text)
