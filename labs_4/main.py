import jinja2
from flask import Flask

from twice_parser import bs_parser, regular_parser

app = Flask(__name__)


@app.route('/')
def hello():
    template_loader = jinja2.FileSystemLoader(searchpath="./jinja_templates")
    template_env = jinja2.Environment(loader=template_loader)
    template_file = "main.jinja"
    template = template_env.get_template(template_file)
    output_text = template.render()
    return output_text


@app.route('/re')
def re_pars():
    template_loader = jinja2.FileSystemLoader(searchpath="./jinja_templates")
    template_env = jinja2.Environment(loader=template_loader)
    template_file = "table.jinja"
    template = template_env.get_template(template_file)
    template_vars = {"columns": ["Код", "Название рубрики", "Журналов"],
                     "items": regular_parser()}
    output_text = template.render(template_vars)
    return output_text


@app.route('/bs')
def bs_pars():
    template_loader = jinja2.FileSystemLoader(searchpath="./jinja_templates")
    template_env = jinja2.Environment(loader=template_loader)
    template_file = "table.jinja"
    template = template_env.get_template(template_file)
    template_vars = {"columns": ["Код", "Название рубрики", "Журналов"],
                     "items": bs_parser()}
    output_text = template.render(template_vars)
    return output_text


if __name__ == '__main__':
    app.run()
