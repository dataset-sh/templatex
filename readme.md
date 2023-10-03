# TempLatex

A jinja2 dialect for latex templating in python.

## Why not the default jinja2?

jinja2's default escape works great for HTML but is not user-friendly for latex because latex heavily uses curly
brackets {} .

For example, if you want to produce the following latex code:

`x = \frac{b}{c}`

Where b and c will be replaced by an actual number, for example: `{"b": 42, "c": 3}`. 

The jinja2 version will be:

```python
from jinja2 import Template

template = """
x = \\frac{{{ b }}}{{"{"}}{{ c }}{{"}"}}
"""
# {{"}"}} will render to }

data = {
    'a': 13,
    'b': 42,
    'c': 3
}

j2_template = Template(template)
print(j2_template.render(data))
```

You will notice that because both latex and jinja2 heavily rely on `{}`, the template string will be populated
with `{}`, make it hard to read and modify.

In `templatex`, we can write the following code:

```python
from templatex import Template

template = """
x = \\frac{@= b =@}{@= c =@}
"""

data = {
    'a': 13,
    'b': 42,
    'c': 3
}

j2_template = Template(template)
print(j2_template.render(data))
```

## What this package changes

### Changed Default Jinja2 configuration.

Template changes jinja2's default configuration to the following:

```python
Enviroment(
    loader,
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
```

As a result, you only need to adopt the following syntax:

* variable render: `@= var_name =@`
* block logic: `@@ for my_item in my_collection @@`
* comment: `\#{ your comment }`


### Add a latex escape filter

Jinja2, by default, will perform auto HTML escaping on rendered variables, but I couldn't figure out how to change its default escape filter implementation. 
As a result, we disabled this feature and provided a latex escape filter so template authors can manually escape string variables as needed.

For example: 

When rendering `@= my_var =@`, and if `my_var="$5.0"`, the resulting latex code cannot be compiled due to the unescaped `$` character.
You can use `@= my_var | escape_latex =@`, where the `escape_latex` filter will escape `$` character to valid latex: `\$`.

### Other features

Since this is still the same jinja2 engine at its core, users should refer to the [jinja2 site](https://jinja.palletsprojects.com/en/3.0.x/) for documentation on other features. 

### Inspiration

I adopted the solution from [this answer on stackoverflow](https://stackoverflow.com/a/55715605), and added some modifications.
