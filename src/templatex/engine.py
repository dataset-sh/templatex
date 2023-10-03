import copy

from jinja2 import Environment as Jinja2Environment
from jinja2 import Template as Jinja2Template
import re


def escape_latex(content):
    conv = {
        '&': r'\&',
        '%': r'\%',
        '$': r'\$',
        '#': r'\#',
        '_': r'\_',
        '{': r'\{',
        '}': r'\}',
        '~': r'\textasciitilde{}',
        '^': r'\^{}',
        '\\': r'\textbackslash{}',
        '<': r'\textless{}',
        '>': r'\textgreater{}',
    }
    regex = re.compile('|'.join(re.escape(str(key)) for key in sorted(conv.keys(), key=lambda item: - len(item))))
    return regex.sub(lambda match: conv[match.group()], content)


__FILTERS = {
    'escape_latex': escape_latex
}

__EnvArgs = dict(
    trim_blocks=True,
    block_start_string='@@',
    block_end_string='@@',
    variable_start_string='@=',
    variable_end_string='=@',
    autoescape=False,
    comment_start_string='\#{',
    comment_end_string='}',
    line_statement_prefix='%%',
    line_comment_prefix='%#',
)


def Environment(loader, **kwargs):  # noqa
    env_args = get_jinja_env_args()
    env_args.update(kwargs)

    jinja_ev = Jinja2Environment(
        loader=loader,
        **env_args
    )

    filters = get_jinja_filters()

    for name, f in filters.items():
        jinja_ev.filters[name] = f

    return jinja_ev


def get_jinja_env_args():
    return copy.deepcopy(__EnvArgs)


def get_jinja_filters():
    return copy.deepcopy(__FILTERS)


def Template(source, **kwargs):  # noqa
    env_args = get_jinja_env_args()
    env_args.update(kwargs)
    return Jinja2Template(source, **env_args)
