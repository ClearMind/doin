import codecs
from django.template.loader import get_template
from texcaller.texcaller import convert
from settings import PRINT_TEMPLATES_ROOT as root, MEDIA_ROOT, DEBUG
from shutil import copy
from os import path, makedirs
from django.template import Context, Template

from xhtml2pdf import pisa

def tex_printer(context, template_name):
    """
    pdf generator
    context -- dict with user id and other information needed by template
    template_name -- name of file of template without .ttex .tex
    """
    #1 copy template_name .tex & .ttex files to MEDIA_ROOT/pdf/user_id/
    uid = context["id"]
    target_dir = path.join(MEDIA_ROOT, "pdf/%s/" % uid)
    if not path.exists(target_dir):
        makedirs(target_dir)
    copy(path.join(root, template_name + ".tex"), target_dir)
    copy(path.join(root, template_name + ".ttex"), target_dir)
    #2 create sty content from .ttex (template.render(Context(context)))
    template_file = open(target_dir + template_name + ".ttex", 'r')
    template = Template(template_file.read())
    template_file.close()
    sty_content = template.render(Context(context))
    if DEBUG:
        sty_file = codecs.open(target_dir + template_name + ".sty", 'w', 'utf-8')
        sty_file.write(sty_content)
        sty_file.close()
    #3 use texcaller for generate .pdf from .tex(with .sty)
    tex_file = codecs.open(target_dir + template_name + '.tex', 'r', 'utf-8')
    tex_content = tex_file.read()
    tex_file.close()
    pdf, info = convert(tex_content % sty_content, 'LaTeX', 'PDF', 5)
    #4 return template_name.pdf full path
    pdf_file = open(target_dir + template_name + '.pdf', 'w')
    pdf_file.write(pdf)
    pdf_file.close()
    return target_dir + template_name + '.pdf'

def html_printer(template_name, context):
    uid = context["id"]
    target_dir = path.join(MEDIA_ROOT, "pdf/%s/" % uid)
    if not path.exists(target_dir):
        makedirs(target_dir)
    pdf_file = open(target_dir + template_name + '.pdf', 'wb')
    template = get_template("print/" + template_name + ".html")

    pisa.CreatePDF(template.render(Context(context)).encode('UTF-8'), pdf_file, encoding='UTF-8')
    pdf_file.close()

    return target_dir + template_name + '.pdf'