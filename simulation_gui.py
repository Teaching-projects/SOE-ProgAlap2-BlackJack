from tkinter.constants import S
from blackjack_logic import Game
from ai import AI
import matplotlib.pyplot as plt
from tkinter import ttk
from tkinter import messagebox
import tkinter as tk
import json
import os

class Picture(tk.Label):
    def __init__(self, master):
        super().__init__(master) 
        self.configure(bd=0)
        
    def update(self, file_name):
        self.img = tk.PhotoImage(file=file_name)
        self.configure(image=self.img)

class Statistics_frame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        tk.Label(self, background='white', text='hehe').grid(row=0, column=0)
        tk.Label(self, background='white', text='hehe').grid(row=1, column=0)
        
class Form_frame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self._padding=15
        self.configure(background='white')

        tk.Label(self, text="New simulation", font=('Arial', 16)).grid(pady=self._padding, row=0, columnspan=3)

        self.decks_var = tk.IntVar(self, value=1)
        tk.Label(self, text="Decks: ").grid(sticky='w', row=1, column=0)
        tk.Spinbox(self, textvariable=self.decks_var, width=2, from_=1, to=8).grid(pady=self._padding, sticky='w', row=1, column=1)

        self.laps_var = tk.IntVar(self, value=1000)
        tk.Label(self, text="Laps: ").grid(sticky='w', row=2, column=0)
        tk.Spinbox(self, textvariable=self.laps_var, width=7, from_=1, to=1000000, increment=100).grid(pady=self._padding, sticky='w', row=2, column=1)

        self.minimum_bet_var = tk.IntVar(self, value=100)
        tk.Label(self, text="Minimum bet: ").grid(sticky='w', row=3, column=0)
        tk.Spinbox(self, textvariable=self.minimum_bet_var, width=7, from_=100, to=999999, increment=100).grid(pady=self._padding, sticky='w', row=3, column=1)
        
        self.maximum_bet_var = tk.IntVar(self, value=400)
        tk.Label(self, text="Maximum bet: ").grid(sticky='w', row=4, column=0)
        tk.Spinbox(self, textvariable=self.maximum_bet_var, width=7, from_=101, to=1000000, increment=100).grid(pady=self._padding, sticky='w', row=4, column=1)

        self.chips_var = tk.IntVar(self, value=500)
        tk.Label(self, text="Chips: ").grid(sticky='w', row=5, column=0)
        tk.Label(self, textvariable=self.chips_var, width=5).grid(sticky='e', row=5, column=2)
        tk.Scale(self, variable=self.chips_var, orient='horizontal', troughcolor='white', bd=5, showvalue=0, from_=100, to=10000, resolution=100).grid(pady=self._padding, sticky='w', row=5, column=1)

        self.basic_strategy_state = tk.BooleanVar(self, value=True)
        tk.Label(self, text="Basic strategy: ").grid(sticky='w', row=6, column=0)
        tk.Checkbutton(self, variable=self.basic_strategy_state, onvalue=True, offvalue=False).grid(pady=self._padding, sticky='w', row=6, column=1)

        self.card_counter_state = tk.BooleanVar(self, value=False)
        tk.Label(self, text="Card counter: ").grid(sticky='w', row=7, column=0)
        tk.Checkbutton(self, variable=self.card_counter_state, onvalue=True, offvalue=False, command=self._select_system).grid(pady=self._padding, sticky='w', row=7, column=1)
        
        self.counting_system_var = tk.StringVar(self)
        
        for widget in self.grid_slaves():
            widget.configure(background='white', bd=0)
    
    def get_counting_system_names(self): 
        return [os.path.splitext(f)[0] for f in os.listdir('basic_data/counting_systems')]

    def _select_system(self):
        if self.card_counter_state.get():
            self._counting_system_label = tk.Label(self, background='white', text="System: ")
            self._counting_system_label.grid(sticky='w', row=8, column=0)
            self._counting_system_combobox= ttk.Combobox(self, width=10, state='readonly', textvariable=self.counting_system_var, values=self.get_counting_system_names())
            self._counting_system_combobox.current(0)
            self._counting_system_combobox.grid(pady=self._padding, row=8, column=1)
        else:
            self._counting_system_label.destroy()
            self._counting_system_combobox.destroy()


class Simulation_window(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Epic blackjack simulator')
        self.configure(background='white')
        self.resizable(False,False)

        style = ttk.Style()
        style.map('TCombobox', fieldbackground=[('readonly','white')])
        style.map('TCombobox', selectbackground=[('readonly', 'white')])
        style.map('TCombobox', selectforeground=[('readonly', 'black')])

        self._statistics_img = Picture(self)
        self._statistics_img.grid(row=0, column=0)
        self._save_file = 'save/last_statistics.json'
        
        if os.path.isfile(self._save_file): 
            self._last_data = self._load_last_statistics()
            self._statistics_img.update(self._last_data['plot_img'])

        #self._statistics_frame = Statistics_frame(self)
        #self._statistics_frame.grid(row=1, column=0)
        
        self._form_frame = Form_frame(self)
        self._form_frame.grid(sticky='n', row=0, column=1, padx=20)

        tk.Button(self, text='Simulate game', background='white', command=self._new_simulation).grid(sticky='wen', row=1, column=1, padx=20)

    def _plot(self, stat:list, file_name:str):
        fig, ax = plt.subplots()
        ax.plot(stat)
        fig.savefig(file_name)

    def _save_statistics(self, file_name:str): 
        with open(file_name, "wt") as f:
            json.dump(self._last_data, f)

    def _load_last_statistics(self):
        with open(self._save_file) as f:
            return json.load(f)

    def _simulation(self):
        history = []
        decks = self._form_frame.decks_var.get()
        laps = self._form_frame.laps_var.get() 
        min_bet = self._form_frame.minimum_bet_var.get()
        max_bet = self._form_frame.maximum_bet_var.get()
        chips = self._form_frame.chips_var.get()
        system_state = self._form_frame.card_counter_state.get()
        system = self._form_frame.counting_system_var.get()

        if laps > 1000000: raise Exception('Invalid laps value')
        else:
            basic_strategy = self._form_frame.basic_strategy_state.get()
            ai = AI(chips)
            g = Game(ai, min_bet, max_bet, decks)
            if system_state: ai.set_card_counter(system)
            if basic_strategy: ai.set_basic_strategy()
 
            for i in range(laps): 
                g.round()
                history.append(g.get_player_chips_value())

            plot_fname = 'save/last_statistics.png'
            self._plot(history, plot_fname)

            self._last_data = {
                "deck_count": decks,
                "laps": laps,
                "min_bet": min_bet,
                "max_bet": max_bet,
                "chips": chips,
                "Basic_strategy": basic_strategy,
                "bet_system": system if system_state else system_state,
                "history": history,
                "plot_img": plot_fname
            }
            self._save_statistics(self._save_file)
            self._statistics_img.update(plot_fname)

    def _new_simulation(self):
        try:
            self._simulation()
        except Exception as e:
            messagebox.showerror('Error', e)

if __name__ == '__main__':
    w = Simulation_window()
    w.mainloop() 
