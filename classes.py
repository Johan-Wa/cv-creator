# IMPORTS
from pathlib import Path
from fpdf import FPDF
# Data
import pandas as pd
# locals
import functions as fn

# My photo size 800X800

class PDF1(FPDF):

    def build(self,output):
        #
        self.add_page()
        self.body()
        
        return self.output(output)

    def process_dicts(self):
        if self.context['study']['title']:
            s_len = len(self.context['study']['title'])
            w_len = len(self.context['works']['job'])

        if s_len > w_len:
            w_lindex = w_len-1
            for i in range(s_len-w_len):
                w_lindex += 1
                self.context['works']['job'][w_lindex] = ''
                self.context['works']['date'][w_lindex] = ''
                self.context['works']['company'][w_lindex] = ''
                self.context['works']['description'][w_lindex] = ''


        elif w_len > s_len:
            s_lindex = s_len-1
            for i in range(w_len-s_len):
                s_lindex += 1
                self.context['study']['title'][s_lindex] = ''
                self.context['study']['date'][s_lindex] = ''
                self.context['study']['state'][s_lindex] = ''
                self.context['study']['institute'][s_lindex] = ''
    
    def set_context(self,context={},selected_font='Times San Serif',colors={}):
        self.selected_font = selected_font
        if self.selected_font in fn.fonts_dict.keys():
            fn.add_font(self, selected_font)
            
        self.context = {
            'use_work_desc': False,
            'name': '',
            'description_file': '',
            'photo': '',
            'bg': 'src/bg1.png',
            'phone': '',
            'page': '',
            'email': '',
            'carge': '',
            'social': [],
            'study': {},
            'works': {},
            'skills':{}
        }
        self.context.update(context)
        self.colors = {
            'color1': (95,193,171),
            'color2': (119,138,178),
            'b_color': (0,0,0),
            'c_color': (97,96,96)
            }
        self.colors.update(colors)

    def header(self):

        #Charge bg
        fn.change_bg_color(self.context['bg'], self.colors['color1'], (95,193,171),150)
        self.image('output.png', x=0,y=0,w=210,h=297)
        # Set the font
        fn.change_size_font(self, 20)

        # Title
        fn.change_text_color(self, self.colors['color1'])
        fn.change_draw_color(self,self.colors['color1'])
        self.multi_cell(w=0,h=15, txt=self.context['name'], border='B',
        align='C')
        fn.change_text_color(self,self.colors['b_color'])
        self.ln(5)

    def footer(self):
        # Position at 2cm from bottom
        self.set_y(-20)

        # Contact grid
        fn.change_draw_color(self)
        fn.change_size_font(self, 12)
        fn.change_text_color(self,self.colors['c_color'])

        if self.context['phone']:
            self.cell(w=63.3,h=10,txt='Telefono',border='T',align='C')
        else:
            self.cell(w=63.3,h=10,txt='',border='T',align='C')

        if self.context['page']:
            self.cell(w=63.3,h=10,txt='Pagína',border='T',align='C')
        else:
            self.cell(w=63.3,h=10,txt='',border='T',align='C')

        if self.context['page']:
            self.cell(w=0,h=10, txt='Correo',border='T', align='C',ln=1)
        else:
            self.cell(w=0,h=10, txt='',border='T', align='C',ln=1)

        fn.change_size_font(self, 11)
        self.cell(w=63.3,h=10,txt=self.context['phone'],border=0,align='C')
        self.cell(w=63.3,h=10,txt=self.context['page'], border=0,align='C', link=self.context['page'])
        self.cell(w=0,h=10,txt=self.context['email'],border=0,align='C')
        
    def body(self):
        '''print the body content'''
        # Description
        fn.change_text_color(self, self.colors['b_color'])
        count = 0
        if self.context['description_file']:
            txt = ''
            with open(self.context['description_file']) as f:
                for i in f.readlines():
                    txt = txt + i 
                    count +=1

            self.cell(w=40,h=20,txt='',border='B',align='C')
            fn.change_size_font(self, 11)
            fn.change_draw_color(self,self.colors['color2'])
            self.multi_cell(w=0, h=5, txt=txt,
            border='B',align='R')
            fn.change_draw_color(self, self.colors['b_color'])

        # Put photo
        if self.context['photo']:
            photo = Path('foto.jpeg')
            self.image(self.context['photo'], x=10, y=10,w=40,h=40)
            
            if count < 4:
                self.set_xy(10,50)
        self.ln(3)

        # Carge or profetion
        if self.context['carge']:
            fn.change_text_color(self,(199, 0 , 27))
            fn.change_size_font(self, 16)
            self.cell(w=0, h=7, border=0, align='R', txt=self.context['carge'], ln=1)
            fn.change_text_color(self,self.colors['b_color'])
        
        # Social links
        if self.context['social']:
            fn.change_size_font(self, 12)
            self.cell(w=0, h=6, border=0, align='L', txt='Social:', ln=1)
            fn.change_text_color(self,self.colors['c_color'])
            for i in self.context['social']:
                self.cell(w=0, h=6, border=0, align='L', txt=i, link=i, ln=1)
            fn.change_text_color(self,self.colors['b_color'])
        self.ln(2)

        # Work and study section
        fn.change_size_font(self, 14)
        fn.change_draw_color(self,self.colors['color1'])
        self.cell(w=95, h=10, txt='Educacion', border='BT', align='C')
        self.cell(w=95, h=10,txt='Trabajos', border='BT', align='C', ln=1)
        fn.change_size_font(self, 12)

        # Work and study information
        self.ln(5)
        self.process_dicts()
        fn.change_size_font(self, 11)
        for i in range(len(self.context['study']['title'])):
            # Line 1
            h_lines=6
            fn.change_size_font(self, 12)
            fn.change_text_color(self,self.colors['color2'])  
            self.cell(w=47.5, h=h_lines, txt=self.context['study']['title'][i], border=0, align='L')
            fn.change_size_font(self, 11)
            fn.change_text_color(self,self.colors['b_color']) 
            self.cell(w=47.5, h=h_lines, txt=self.context['study']['date'][i], border=0, align='C')
            fn.change_size_font(self, 12)
            fn.change_text_color(self,self.colors['color2']) 
            self.cell(w=95, h=h_lines, txt=self.context['works']['job'][i], border=0, align='C', ln=1)
            fn.change_size_font(self, 11)
            fn.change_text_color(self,self.colors['b_color']) 
            
            # Line 2
            self.cell(w=47.5, h=h_lines, txt=self.context['study']['institute'][i], border=0, align='L')
            self.cell(w=47.5, h=h_lines, txt=self.context['study']['state'][i], border=0, align='C')
            self.cell(w=47.5, h=h_lines, txt=self.context['works']['date'][i], border=0, align='L')
            self.multi_cell(w=47.5, h=h_lines, txt=self.context['works']['company'][i], border=0, align='R')

            if self.context['works']['description'] and self.context['use_work_desc']:
                # Line 3
                self.ln(2)
                self.cell(w=95,h=h_lines, txt='', border=0)
                self.multi_cell(w=95, h=h_lines, txt=self.context['works']['description'][i],border=0,
                align='L')
                self.ln(6)
            else:
                self.ln(5)
        # Habilidades
        fn.change_size_font(self, 14)
        fn.change_draw_color(self,self.colors['color2'])
        self.cell(w=0,h=15,txt='Habilidades',border='BT',align='C',ln=1)
        fn.change_size_font(self, 11)
        self.ln(5)
        
        # Skills
        for i in range(len(self.context['skills']['skill'])):
            self.cell(w=47.5, h=8, txt=self.context['skills']['skill'][i], border=0,align='C')
            self.multi_cell(w=142.5, h=8, txt=self.context['skills']['description'][i], 
            border=0)
            self.ln(1)

class PDF2(FPDF):

    def build(self,output):
        self.add_page()
        self.body()
        return self.output(output)

    def set_context(self,context={},selected_font='Helvetica',colors={}):
        self.selected_font = selected_font
        if self.selected_font in fn.fonts_dict.keys():
            fn.add_font(self, selected_font)
        self.context = {
            'use_work_desc': False,
            'name': '',
            'description_file': '',
            'photo': '',
            'bg': 'src/portrait1.png',
            'phone': '',
            'page': '',
            'email': '',
            'carge': '',
            'social': [],
            'study': {},
            'works': {},
            'skills':{}
        }
        self.context.update(context)
        self.colors = {
            'color1': (218,197,149),
            'color2': (127,91,6),
            'b_color':(0,0,0)
        }
        self.colors.update(colors)

    def footer(self):
        
        # Charge photo
        if self.context['photo']:
            self.image(self.context['photo'],x=10,y=10,w=50,h=50)
            self.set_xy(5,60)
            self.ln(4)
        # Charge Background
        fn.change_bg_color(self.context['bg'], self.colors['color1'], (218,197,149))
        self.image('output.png',x=0,y=0,w=210,h=297,)
        
        footer_titles = [5,60, 10,0,'C',1,0,'']
        # Contact
        fn.change_size_font(self, 18)
        fn.print_cell(self, footer_titles, 'Contacto')
        '''self.set_x(5)
        self.cell(w=60,h=10,txt='Contacto',align='C')'''
        
        footer_info = [5,60,8,'L','L',1,0,'']
        fn.change_size_font(self, 11)
        fn.print_data(self, footer_info, 'phone')
        fn.print_data(self, footer_info, 'email')
        fn.print_data(self, footer_info, 'page')

        # Education
        self.ln(5)
        fn.change_size_font(self,18)
        fn.print_cell(self, footer_titles, 'Educación')
        fn.change_size_font(self,11)

        fn.change_draw_color(self,self.colors['color2'])
        for i in range(len(self.context['study']['title'])):
            title = self.context['study']['title'][i]
            date = self.context['study']['date'][i]
            state = self.context['study']['state'][i]
            institute = self.context['study']['institute'][i]
            
            fn.print_cell(self, footer_info, date)
            fn.change_size_font(self,11,'B')
            fn.print_cell(self, footer_info, title)
            fn.change_size_font(self,11)
            fn.print_cell(self, footer_info, institute,'m')
            fn.print_cell(self, footer_info, state)
            self.ln(2)



        
        fn.change_size_font(self, 9)
        y= -10
        for i in self.context['social']:
            self.set_xy(0,y)
            if len(i) > 40:
                y -= 10 + 10*int(len(i)/40)
                
            else:
                y -= 10
        for i in self.context['social']:
            self.set_x(0)
            self.multi_cell(w=60, h=5,txt=i,align='R')
            

    def body(self):

        fn.change_size_font(self, 20)
        self.set_left_margin(70)
        fn.change_text_color(self,self.colors['color2'])
        self.cell(w=0,h=10, border=0, txt=self.context['name'],align='C', ln=1)
        fn.change_size_font(self, 14,'B')
        fn.change_text_color(self,(199, 0 , 27))
        self.cell(w=0,h=10, border='B', txt=self.context['carge'],align='R', ln=1)
        fn.change_text_color(self,self.colors['b_color'])
        self.ln(5)
        fn.change_size_font(self, 11)
        self.set_left_margin(75)
        # Works
        works_params_text1 = [0,0,8,'RTL','L',1,0,'']
        if self.context['use_work_desc'] == False:
            works_params_text2 = [0,0,8,'RBL','R',1,0,'']
        else:
            works_params_text2 = [0,0,8,'RL','R',1,0,'']
            works_params_text3 = [0,0,5,'RBL','L',1,0,'']

        txt = ''
        if self.context['description_file']:
            with open(self.context['description_file']) as f:
                for i in f.readlines():
                    txt = txt + i 
        self.multi_cell(w=0,h=5, border=0, txt=txt,align='L')
        self.ln(5)
        
        fn.change_size_font(self, 11)
        if self.context['works']:
            fn.change_size_font(self, 15,'B')
            fn.change_text_color(self,self.colors['color2'])
            self.cell(w=0,h=10, border=0, txt='Experiencia laboral',align='C', ln=1)
            fn.change_text_color(self,self.colors['b_color'])
            self.ln(5)
            for i in range(len(self.context['works']['job'])):
                # Line 1
                fn.change_size_font(self, 11,"B")
                fn.print_cell(self, works_params_text1, self.context['works']['job'][i],set_x=False)
                fn.change_size_font(self, 11)
                # Line 2
                txt = self.context['works']['company'][i] + '  |  ' + self.context['works']['date'][i]
                fn.print_cell(self, works_params_text2,txt=txt ,set_x=False)
                
                if self.context['use_work_desc']:
                    # Line 3
                    self.ln(2)
                    fn.print_cell(self, works_params_text3,txt=self.context['works']['description'][i],
                    type_cell='m',set_x=False)
                
                self.ln(5)
        
        # Skills
        if self.context['skills']:
            fn.change_draw_color(self,self.colors['color1'])
            fn.change_size_font(self, 15,'B')
            fn.change_text_color(self,self.colors['color2'])
            self.cell(w=0,h=10, border=0, txt='Habilidades',align='C', ln=1)
            fn.change_text_color(self,self.colors['b_color'])
            self.ln(5)
            skills_params_text1 = [0,0,6,'BT','C',1,0,'']
            skills_params_text2 = [0,0,6,0,'L',1,0,'']

            for i in range(len(self.context['skills']['skill'])):
                fn.change_size_font(self, 11,'B')
                fn.print_cell(self, skills_params_text1, self.context['skills']['skill'][i],set_x=False)
                fn.change_size_font(self, 10)
                fn.print_cell(self, skills_params_text2,
                    self.context['skills']['description'][i],'m',set_x=False)
                self.ln(3)
            