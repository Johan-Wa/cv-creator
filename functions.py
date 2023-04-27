#imports
import os
import numpy as np
from PIL import Image

colors_dict = {
    'black': (0,0,0),
    'blue1': (95,193,171),
    'blue2': (119,138,178),
    'red1': (199, 0 , 27),
    'gray1': (97,96,96),
    'gray-red': (145,121,121),
    'naranja-piel': (218,197,149),
    'marron-naranja': (127,91,6)
}


def change_size_font(pdf,size, style=''):
    try:
        pdf.set_font(pdf.selected_font,style,size)
    except RuntimeError:
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
        
def select_color(color):
    if colors_dict[color]:
        return colors_dict[color]


def change_fill_color(pdf,color='black'):
    rgb = select_color(color)
    pdf.set_fill_color(r=rgb[0],g=rgb[1],b=rgb[2])
def change_text_color(pdf,color='black'):
    rgb = select_color(color)
    pdf.set_text_color(r=rgb[0],g=rgb[1],b=rgb[2])
def change_draw_color(pdf,color='black'):
    rgb = select_color(color)
    pdf.set_draw_color(r=rgb[0],g=rgb[1],b=rgb[2])

def change_bg_color(image,new_color,color,alpha=''):
    new_color=new_color
    color=select_color(color)

    rgb = select_color(new_color)

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
                
                pixels[x, y] = (rgb[0], rgb[1], rgb[2], a)
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
