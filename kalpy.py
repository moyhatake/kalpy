from tkinter import *

margin = 7
max_len = 14
colors = {
    'dark': '#202020',
    'light': '#fbf9e7',
    'semi-light': '#a6a599',
    'accent-1': '#e8a976',
    'accent-2': '#323232',
    'accent-3': '#3b3b3b',
    'dimmed': "#e87676"
}

class Kalpy:
    def __init__(self, root):
        self.root = root
        self.root.title("Kalpy")
        self.root.config(bg=colors['dark'])
        
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width // 2) - (320 // 2)
        y = (screen_height // 2) - (490 // 2)
        
        self.root.geometry(f"{320}x{490}+{x}+{y}")
        self.root.resizable(False, False)
        try:
            self.root.iconbitmap('src/appicon.ico')
        except:
            pass

        # State variables
        self.counter = 0
        self.pre_result = 0
        self.idle = True
        self.stacked = False
        self.pnt_check = False
        self.add_check = False
        self.sub_check = False
        self.mul_check = False
        self.div_check = False
        self.calculated = False

		# History text area
        self.history = Text(root, bd=0, width=34, height=1, font=('sans-serif', 13), bg=colors['dark'], fg=colors['semi-light'], wrap='none', padx=0, pady=2)
        self.history.tag_configure('tag-right', justify='right')
        self.history.place(x=margin, y=margin+1)
        self.history.config(state=DISABLED)
        
        # Main text area
        self.entry = Text(root, bg=colors['dark'], fg=colors['light'], bd=0, width=16, height=1, font=('sans-serif', 26, 'bold'), wrap='none', padx=1, pady=2)
        self.entry.tag_configure('tag-right', justify='right')
        self.entry.insert('end', '0', 'tag-right')
        self.entry.place(x=margin, y=39)
        self.entry.config(state=DISABLED)

        self.create_buttons()

    # Helper funcs
    def get_value(self):
        try:
            val = self.entry.get('1.0', 'end-1c').replace(',', '')
            return int(val) if val.isdigit() else float(val)
        except:
            return None
        
    def get_sym(self, op_type):
        if op_type == "add":
            return "+"
        elif op_type == "sub":
            return "-"
        elif op_type == "mul":
            return "×"
        elif op_type == "div":
            return "÷"
        return ""

    def show_error(self):
        self.entry.config(state=NORMAL)
        self.entry.delete('1.0', END)
        self.entry.insert('end', "¡ERROR!", 'tag-right')
        self.entry.config(state=DISABLED)

        self.counter = 0
        self.pre_result = 0
        self.stacked = False
        self.pnt_check = False
        self.add_check = False
        self.sub_check = False
        self.mul_check = False
        self.div_check = False
        self.calculated = True
        
    def apply_filter(self, value):
        if isinstance(value, float):
            decimal_pos = str(value).find('.')
            if decimal_pos != -1:
                decimal_places = max_len - decimal_pos - 1
                value = round(value, max(decimal_places, 0))

        if isinstance(value, float) and value.is_integer():
            value = int(value)
            
        if value == 0:
            self.idle = True
            
        return value
    
    def apply_format(self, value):
        str_value = str(value)
        if isinstance(value, float):
            decimal_pos = str_value.find('.')
            if decimal_pos != -1:
                decimal_places = len(str_value) - decimal_pos - 1
                str_value = f"{value:,.{decimal_places}f}"
        
        try:
            value = int(str_value) if str(abs(int(str_value))).isdigit() else float(str_value)
            str_value = f"{value:,}"
        except:
            pass
        
        return str_value
    
    # Main funcs
    def insert_char(self, char):
        if self.calculated:
            self.clear()

        self.entry.config(state=NORMAL)

        if self.idle:
            self.idle = False
            self.entry.delete('1.0', END)
        
        commas = self.entry.get('1.0', 'end-1c').count(',')
        extra = 1 if (self.pnt_check and commas <= 1) else 0
        if self.counter < max_len + extra:
            value = char
            self.counter += 1

            if not self.pnt_check:
                value = self.entry.get('1.0', 'end-1c').replace(',', '') + char
                try:
                    value = int(value) if value.isdigit() else float(value) ###
                except:
                    self.show_error()
                    return
                value = self.apply_format(value)
                self.entry.delete('1.0', END)

            self.entry.insert('end', value, 'tag-right')

        self.entry.config(state=DISABLED)

    def insert_point(self):
        if self.calculated:
            self.clear()
        
        if not self.pnt_check:
            self.idle = False
            self.pnt_check = True
            self.entry.config(state=NORMAL)

            if self.get_value() is None:
                self.entry.insert('end', '0', 'tag-right')
                self.counter += 1

            commas = self.entry.get('1.0', 'end-1c').count(',')
            if commas < 4:
                self.entry.insert('end', '.', 'tag-right')

            self.entry.config(state=DISABLED)

    def delete_char(self):
        if self.idle:
            return

        if self.calculated:
            self.history.config(state=NORMAL)
            self.history.delete('1.0', END)
            self.history.config(state=DISABLED)
            return
    
        if self.counter > 0:
            self.entry.config(state=NORMAL)

            value = self.entry.get('1.0', 'end-1c')[:-1]
            self.entry.delete('1.0', END)

            if not value.endswith('.'):
                self.counter -= 1

            if not '.' in value:
                self.pnt_check = False
                value = value.replace(',', '')
                try:
                    value = int(value) if value.isdigit() else float(value)
                except:
                    pass
                value = self.apply_format(value)

            self.entry.insert('end', value, 'tag-right')
            self.entry.config(state=DISABLED)
            
            if self.counter == 0 and not self.stacked:
                self.clear()
    
    def clear(self):
        self.entry.config(state=NORMAL)
        self.entry.delete('1.0', END)
        self.entry.insert('end', '0', 'tag-right')
        self.entry.config(state=DISABLED)
        self.history.config(state=NORMAL)
        self.history.delete('1.0', END)
        self.history.config(state=DISABLED)

        self.counter = 0
        self.pre_result = 0
        self.idle = True
        self.stacked = False
        self.pnt_check = False
        self.add_check = False
        self.sub_check = False
        self.mul_check = False
        self.div_check = False
        self.calculated = False

    def store_op(self, op_type):
        value = self.get_value()
        
        if self.stacked:
            self.add_check = False
            self.sub_check = False
            self.mul_check = False
            self.div_check = False
            setattr(self, f"{op_type}_check", True)

            if value is None:
                stored = self.history.get('1.0', 'end-2c')
                stored = f"{stored[:-2]} {self.get_sym(op_type)} "

                self.history.config(state=NORMAL)
                self.history.delete('1.0', END)
                self.history.insert('end', stored, 'tag-right')
                self.history.config(state=DISABLED)
                return
            
            self.auto_op(self.get_sym(op_type))
            return
        
        self.counter = 0
        self.pre_result = value
        self.pnt_check = False
        self.add_check = False
        self.sub_check = False
        self.mul_check = False
        self.div_check = False
        setattr(self, f"{op_type}_check", True)
            
        self.entry.config(state=NORMAL)
        self.entry.delete('1.0', END)
        self.entry.config(state=DISABLED)
            
        self.history.config(state=NORMAL)
        if self.calculated:
            self.calculated = False
            self.history.delete('1.0', END)
        self.history.insert('end', f"{str(value)} {self.get_sym(op_type)} ", 'tag-right')
        self.history.config(state=DISABLED)

        self.stacked = True

    def percentage(self):
        value = self.get_value()
        if value is not None:
            result = 0
            str_result = ""
            try:
                result = self.apply_filter(value / 100)
                tmp_str = self.apply_format(result)
                str_result = tmp_str if len(str(result)) <= max_len else '¡TOO LONG NUM!'
                self.entry.config(state=NORMAL)
                self.entry.delete('1.0', END)
                self.entry.insert('end', str_result, 'tag-right')
                self.entry.config(state=DISABLED)

                str_history = str(result) if len(str(result)) <= 34 else '¡TOO LONG NUM!'
                self.history.config(state=NORMAL)
                self.history.delete('1.0', END)
                if str_result != '¡TOO LONG NUM!':
                    self.history.insert('end', str_history, 'tag-right')
                self.history.config(state=DISABLED)
            except:
                self.show_error()
                return
                
            self.add_check = False
            self.sub_check = False
            self.mul_check = False
            self.div_check = False
            self.calculated = True
            self.pnt_check = True if str_result.find('.') != -1 else False
            self.counter = len(str_result)
    
    def sign(self):
        value = self.get_value()
        if value is not None:
            result = 0
            str_result = ""
            try:
                result = self.apply_filter(-value)
                tmp_str = self.apply_format(result)
                str_result = tmp_str if len(str(result)) <= max_len else '¡TOO LONG NUM!'
                self.entry.config(state=NORMAL)
                self.entry.delete('1.0', END)
                self.entry.insert('end', str_result, 'tag-right')
                self.entry.config(state=DISABLED)

                str_history = f"negate({str(-result)})" if len(f"negate({str(-result)})") <= 34 else '¡TOO LONG EXP!'
                self.history.config(state=NORMAL)
                self.history.delete('1.0', END)
                if str_result != '¡TOO LONG NUM!':
                    self.history.insert('end', str_history, 'tag-right')
                self.history.config(state=DISABLED)
            except:
                self.show_error()
                return
                
            self.add_check = False
            self.sub_check = False
            self.mul_check = False
            self.div_check = False
            self.calculated = True
            self.pnt_check = True if str_result.find('.') != -1 else False
            self.counter = len(str_result)
    
    def auto_op(self, op_current):
        value = self.get_value()

        if value is None:
            self.show_error()
            return
        
        result = 0
        str_result = ""
        op_history = self.history.get('1.0', END)
        try:
            if '+' in op_history:
                result = self.pre_result + value
            elif '-' in op_history:
                result = self.pre_result - value
            elif '×' in op_history:
                result = self.pre_result * value
            elif '÷' in op_history:
                result = (self.pre_result / value) if value != 0 else None
                if result is None:
                    self.show_error()
                    return
            else:
                result = value

            result = self.apply_filter(result)
            tmp_str = self.apply_format(result)
            str_result = tmp_str if len(str(result)) <= max_len else '¡TOO LONG NUM!'
            self.entry.config(state=NORMAL)
            self.entry.delete('1.0', END)
            self.entry.config(state=DISABLED)
            
            str_history = f"{str_result.replace(',', '')} {op_current} " if len(f"{str_result.replace(',', '')} {op_current} ") <= 34 else '¡TOO LONG EXP!'
            self.history.config(state=NORMAL)
            self.history.delete('1.0', END)
            if str_result != '¡TOO LONG NUM!':
                self.history.insert('end', str_history, 'tag-right')
            self.history.config(state=DISABLED)
        except:
            self.show_error()
            return

        self.pnt_check = False
        self.calculated = False
        self.counter = 0
        self.pre_result = result
    
    def calculate(self):
        value = self.get_value()

        if value is None:
            self.show_error()
            return
        
        result = 0
        str_result = ""
        try:
            if self.add_check:
                result = self.pre_result + value
            elif self.sub_check:
                result = self.pre_result - value
            elif self.mul_check:
                result = self.pre_result * value
            elif self.div_check:
                result = (self.pre_result / value) if value != 0 else None
                if result is None:
                    self.show_error()
                    return
            else:
                result = value

            result = self.apply_filter(result)
            tmp_str = self.apply_format(result)
            str_result = tmp_str if len(str(result)) <= max_len else '¡TOO LONG NUM!'
            self.entry.config(state=NORMAL)
            self.entry.delete('1.0', END)
            self.entry.insert('end', str_result, 'tag-right')
            self.entry.config(state=DISABLED)
            
            stored = self.history.get('1.0', 'end-2c')
            str_history = f"{str(value)} =" if len(f"{stored} {str(value)} =") <= 34 else '¡TOO LONG EXP!'
            self.history.config(state=NORMAL)
            if str_history == f"{str_result} =" or str_result == '¡TOO LONG NUM!':
                self.history.delete('1.0', END)
            if str_result != '¡TOO LONG NUM!':
                self.history.insert('end', str_history, 'tag-right')
            self.history.config(state=DISABLED)
        except:
            self.show_error()
            return

        self.stacked = False
        self.add_check = False
        self.sub_check = False
        self.mul_check = False
        self.div_check = False
        self.calculated = True
        self.pnt_check = True if str_result.find('.') != -1 else False
        self.pre_result = 0
        self.counter = len(str_result)

    # UI funcs
    def on_enter(self, e):
        hover_color = ""
        origin_color = e.widget.base_color
        if origin_color == colors['accent-2']:
            hover_color = colors['accent-3']
        elif origin_color == colors['accent-3']:
            hover_color = colors['accent-2']
        else:
            hover_color = colors['dimmed']
        e.widget['background'] = hover_color

    def on_leave(self, e):
        e.widget['background'] = e.widget.base_color

    def create_buttons(self): # Mapping: [text, x, y, command]
        height = 78
        from_point = 92
        btn_info = [
            ("C", margin, from_point, self.clear), ("<", height+1, from_point, self.delete_char), ("%", height*2+1, from_point, self.percentage), ("÷", height*3, from_point, lambda: self.store_op("div")),
            ("7", margin, from_point+height, lambda: self.insert_char('7')), ("8", height+1, from_point+height, lambda: self.insert_char('8')), ("9", height*2+1, from_point+height, lambda: self.insert_char('9')), ("×", height*3+1, from_point+height, lambda: self.store_op("mul")),
            ("4", margin, from_point+height*2, lambda: self.insert_char('4')), ("5", height+1, from_point+height*2, lambda: self.insert_char('5')), ("6", height*2+1, from_point+height*2, lambda: self.insert_char('6')), (" -", height*3+1, from_point+height*2, lambda: self.store_op("sub")),
            ("1", margin, from_point+height*3, lambda: self.insert_char('1')), ("2", height+1, from_point+height*3, lambda: self.insert_char('2')), ("3", height*2+1, from_point+height*3, lambda: self.insert_char('3')), ("+", height*3+1, from_point+height*3, lambda: self.store_op("add")),
            ("±", margin, from_point+height*4, self.sign), ("0", height+1, from_point+height*4, lambda: self.insert_char('0')), (" . ", height*2+1, from_point+height*4, self.insert_point), ("=", height*3+1, from_point+height*4, self.calculate)
        ]

        for text, x, y, cmd in btn_info:
            init_color = self.get_color(text)
            btn = Button(self.root, text=text, command=cmd, padx=29 if text=="÷" else 28, pady=23, bd=0, font=('sans-serif', 14),
                   bg=init_color, fg=colors['dark'] if text == "=" else colors['light'], activebackground=colors['dark'], activeforeground=colors['semi-light'])
            btn.base_color = init_color
            btn.place(x=x, y=y)
            btn.bind("<Enter>", self.on_enter)
            btn.bind("<Leave>", self.on_leave)

    def get_color(self, char):
        if char in " -+×÷%=<C":
            return colors['accent-2'] if char != "=" else colors['accent-1']
        else:
            return colors['accent-3']
    
if __name__ == "__main__":
    root = Tk()
    Kalpy(root)
    root.mainloop()