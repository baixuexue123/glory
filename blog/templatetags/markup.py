import markdown
import mistune
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import html

from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter
def markup1(value):
    md = markdown.markdown(value,
                           extensions=['markdown.extensions.extra',
                                       'markdown.extensions.codehilite',
                                       'markdown.extensions.toc'])
    return mark_safe(md)


def block_code(text, lang, inlinestyles=False, linenos=False):
    if not lang:
        text = text.strip()
        return u'<pre><code>%s</code></pre>\n' % mistune.escape(text)

    try:
        lexer = get_lexer_by_name(lang, stripall=True)
        formatter = html.HtmlFormatter(
            noclasses=inlinestyles, linenos=linenos
        )
        code = highlight(text, lexer, formatter)
        if linenos:
            return '<div class="highlight">%s</div>\n' % code
        return code
    except:
        return '<pre class="%s"><code>%s</code></pre>\n' % (lang, mistune.escape(text))


class HighlightRenderer(mistune.Renderer):
    def block_code(self, text, lang=None):
        # renderer has an options
        inlinestyles = self.options.get('inlinestyles', False)
        linenos = self.options.get('linenos', False)
        return block_code(text, lang, inlinestyles, linenos)


@register.filter
def markup3(value):
    renderer = HighlightRenderer(linenos=False, inlinestyles=False)
    md = mistune.Markdown(escape=True, renderer=renderer)
    return mark_safe(md(value))
