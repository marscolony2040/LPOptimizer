import tkinter as tk
import tkinter.ttk as ttk
from scipy.optimize import minimize
import numpy as np
from functools import partial


class Home(tk.Tk):

    bg = 'red'
    fg = 'yellow'

    def __init__(self):
        tk.Tk.__init__(self)
        tk.Tk.wm_title(self, 'LP Optimizer')
        self.geometry('370x100')
        self.configure(bg=self.bg)

        ctrl_frame = tk.Frame(self, bg=self.bg)
        ctrl_frame.pack(side=tk.TOP)

        self.controlFrame(ctrl_frame)

    def open_window(self):
        def optimizer():
            def obj(x):
                total = np.sum([x[i]*float(self.iv[i].get()) for i in range(self.vars)])
                if self.mm == 'Max':
                    return -total
                return total

            cs = {}
            cons = []
            for i in range(self.cons):
                if self.var[i].get() == '<=':
                    cs[i] = lambda x, a, b: a - np.sum([x[j]*float(b[j].get()) for j in range(self.vars)])
                    cons.append({'type':'ineq', 'fun':partial(cs[i], a=float(self.const_out[i].get()), b=self.const[i])})
                elif self.var[i].get() == '>=':
                    cs[i] = lambda x, a, b: np.sum([x[j]*float(b[j].get()) for j in range(self.vars)]) - a
                    cons.append({'type':'ineq', 'fun':partial(cs[i], a=float(self.const_out[i].get()), b=self.const[i])})
                else:
                    cs[i] = lambda x, a, b: np.sum([x[j]*float(b[j].get()) for j in range(self.vars)]) - a
                    cons.append({'type':'eq', 'fun':partial(cs[i], a=float(self.const_out[i].get()), b=self.const[i])})

            x = [0 for i in range(self.vars)]
            res = minimize(obj, x, method='SLSQP', bounds=None, constraints=cons)
            px = res.x.tolist()

            for i in range(self.vars):
                self.w[i].configure(text=str(round(px[i], 4)))

            total_s = 0
            for i in range(self.vars):
                total_s += px[i]*float(self.iv[i].get())

            self.max.configure(text=str(round(total_s, 4)))

            for i in range(self.cons):
                total_c = 0
                for j in range(self.vars):
                    total_c += float(self.const[i][j].get())*px[j]
                self.cz[i].configure(text=str(round(total_c, 4)))

            sub.update_idletasks()                   
                
                    
        
        self.vars = int(self.entry['Variables'].get())
        self.cons = int(self.entry['Constraints'].get())
        self.mm = self.entry['Min or Max'].get()
        
        sub = tk.Toplevel(self, bg=self.bg)
        sub.geometry(f'{320 + self.vars*100}x{self.cons*100}')

        tk.Label(sub, text='\t', bg=self.bg, fg=self.fg).grid(row=1, column=1)
        tk.Label(sub, text='\t', bg=self.bg, fg=self.fg).grid(row=2, column=1)
        tk.Label(sub, text='Result', bg=self.bg, fg=self.fg).grid(row=3, column=1)
        tk.Label(sub, text='IndepV', bg=self.bg, fg=self.fg).grid(row=4, column=1)

        
        
        self.iv = {}
        self.w = {}
        self.cz = {}
        self.const = {i:{} for i in range(self.cons)}
        self.const_eq = {}
        self.const_out = {}
        
        for i in range(self.vars):
            tk.Label(sub, text='\t', bg=self.bg, fg=self.fg).grid(row=1, column=i+2)
            tk.Label(sub, text=f'Var: {i+1}', bg=self.bg, fg=self.fg).grid(row=2, column=i+2)
            self.w[i] = tk.Label(sub, text='0', bg=self.bg, fg=self.fg)
            self.w[i].grid(row=3, column=i+2)
            self.iv[i] = ttk.Entry(sub, justify='center', width=7)
            self.iv[i].grid(row=4, column=i+2)
            
        tk.Label(sub, text='\t', bg=self.bg, fg=self.fg).grid(row=2, column=self.vars+2)            
        tk.Label(sub, text=self.mm, bg=self.bg, fg=self.fg).grid(row=2, column=self.vars+3)
        self.max = tk.Label(sub, text='0', bg=self.bg, fg=self.fg)
        self.max.grid(row=3, column=self.vars+3)

        tk.Button(sub, text='Optimize', bg=self.fg, fg=self.bg, command=lambda: optimizer()).grid(row=4, column=self.vars+3)

        for i in range(5, 9):
            tk.Label(sub, text='\t', bg=self.bg, fg=self.fg).grid(row=i, column=1)

        for ik, qf in enumerate(['Constraints'] + [f'Var: {i+1}' for i in range(self.vars)] + ['LHS','Sign','RHS']):
            tk.Label(sub, text=qf, bg=self.bg, fg=self.fg).grid(row=9, column=1+ik)

        self.var = {}
        for i in range(self.cons):
            self.cz[i] = tk.Label(sub, text='0', bg=self.bg, fg=self.fg)
            self.var[i] = tk.StringVar(sub)
            self.var[i].set('=')
            self.const_eq[i] = tk.OptionMenu(sub, self.var[i], *['>=','=','<='])
            tk.Label(sub, text=f'C{i+1}', bg=self.bg, fg=self.fg).grid(row=10+i, column=1)
            self.const_out[i] = ttk.Entry(sub, justify='center', width=7)
            for j in range(self.vars):
                self.const[i][j] = ttk.Entry(sub, justify='center', width=7)
                self.const[i][j].grid(row=10+i, column=j+2)
            self.cz[i].grid(row=10+i, column=self.vars+2)
            self.const_eq[i].grid(row=10+i, column=self.vars+3)
            self.const_out[i].grid(row=10+i, column=self.vars+4)


    def controlFrame(self, frame):
        self.entry = {}
        for i, j in enumerate(('Variables','Constraints','Min or Max')):
            tk.Label(frame, text=j, bg=self.bg, fg=self.fg).grid(row=1, column=i+1)
            self.entry[j] = ttk.Entry(frame, justify='center', width=10)
            self.entry[j].grid(row=2, column=i+1)

        tk.Label(frame, text='\t', bg=self.bg, fg=self.fg).grid(row=3, column=2)
        tk.Button(frame, text='Launch', bg=self.fg, fg=self.bg, command=lambda: self.open_window()).grid(row=4, column=2)
        tk.Label(frame, text='\t', bg=self.bg, fg=self.fg).grid(row=5, column=2)

Home().mainloop()


    
