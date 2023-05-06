#imports
import os
#
from fpdf import errors
import numpy as np
from PIL import Image

fonts_dict = {
    'Times San Serif': ('Times San Serif','','fonts/TIMESS__.ttf')
}


def change_size_font(pdf,size, style=''):
    try:
        pdf.set_font(pdf.selected_font,style,size)
    except errors.FPDFException:
        pdf.set_font(pdf.selected_font,'',size)

def print_data(pdf,param,context_item,set_x=True):
    '''Print a fixe cell'''
    if set_x:
        pdf.set_x(param[0])
    if pdf.context[context_item]:
        
        pdf.cell(w=param[1],h=param[2],txt=pdf.context[context_item],border=param[3],
        align=param[4], ln=param[5], fill=param[6],link=param[7])

def print_cell(pdf,param,txt,type_cell='c',set_x=True):
    
    if set_x:
        pdf.set_x(param[0])
    if type_cell == 'c':
        pdf.cell(w=param[1],h=param[2],txt=txt,border=param[3],
            align=param[4], ln=param[5], fill=param[6],link=param[7])
    elif type_cell == 'm':
        pdf.multi_cell(w=param[1],h=param[2],txt=txt,border=param[3],
            align=param[4], fill=param[6])


def change_fill_color(pdf,color=(0,0,0)):
    #rgb = select_color(color)
    pdf.set_fill_color(color)
def change_text_color(pdf,color=(0,0,0)):
    #rgb = select_color(color)
    pdf.set_text_color(color)
def change_draw_color(pdf,color=(0,0,0)):
    #rgb = select_color(color)
    pdf.set_draw_color(color)

def change_bg_color(image,new_color,color,alpha=''):
    new_color=new_color
    #color=select_color(color)

    #rgb = select_color(new_color)

    icon = Image.open(image)
    icon = icon.convert("RGBA")

    pixels = icon.load()

    width, height = icon.size

    for x in range(width):
        for y in range(height):
            r, g, b, a = pixels[x, y]
            if alpha != '':
                a=alpha
            if (r, g, b) == color:
                
                pixels[x, y] = (new_color[0], new_color[1], new_color[2], a)
    icon.save('output.png')


def change_alpha(image,alpha):
    im = Image.open(image)
    alpha = Image.new("L", im.size, alpha)

    im.putalpha(alpha)

    im.save('output.png')

def create_CV(pdf,output='cv.pdf',*args, **kwargs):
    output=output
    pdf = pdf
    pdf.set_context(*args, **kwargs)
    pdf.build(output)
    try:
        os.system('rm output.png')
    except:
        pass
