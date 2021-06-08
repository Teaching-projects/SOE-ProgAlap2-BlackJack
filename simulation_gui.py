from ai import AI, Game_simulation
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import matplotlib.pyplot as plt
import json
import os

class Statistics_frame(tk.Frame):
    """A statisztikai adatok megjelenését definiálja az osztály."""
    def __init__(self, master) -> None:
        super().__init__(master)
        self.configure(background='white')

    def update(self, data:dict) -> None:
        """Egy szimuláció adatait jeleníti meg.

        Args:
            data (dict): A szimuláció adatai.
        """
        for label in self.grid_slaves():
            label.grid_forget()
        self._img = tk.PhotoImage(file=data["plot_img"])
        img_widget = tk.Label(self, image=self._img, bd=0)
        text_frame = tk.Frame(self, background='white')
        padding = 20
        img_widget.configure()
        tk.Label(text_frame, text=f'Number of decks: {data["deck_count"]}', background='white').grid(padx=padding, row=0, column=0)
        tk.Label(text_frame, text=f'Minimum bet: {data["min_bet"]}', background='white').grid(padx=padding, row=0, column=1)
        tk.Label(text_frame, text=f'Maximum bet: {data["max_bet"]}', background='white').grid(padx=padding, row=0, column=2)
        tk.Label(text_frame, text=f'Starting chips: {data["chips"]}', background='white').grid(padx=padding, row=1, column=0)
        tk.Label(text_frame, text=f'Basic strategy: {"on" if data["basic_strategy"] else "off"}', background='white').grid(padx=padding, row=1, column=1)
        tk.Label(text_frame, text=f'Card counting: {"off" if data["bet_system"] == False else data["bet_system"]}', background='white').grid(padx=padding, row=1, column=2)
        tk.Label(text_frame, text=f'After {data["rounds"]} rounds, the value of the chips is {data["history"][- 1]}.', background='white').grid(padx=padding, row=3, columnspan=3)
        img_widget.grid(row=0, column=0)
        text_frame.grid(row=1, column=0)

class Form_frame(tk.Frame):
    """Új szimuláció számára fenntartott beviteli mezők megjelenését definiálja az osztály."""
    def __init__(self, master) -> None:
        super().__init__(master)
        self._padding=15
        self.configure(background='white')

        tk.Label(self, text="New simulation", font=('Arial', 16)).grid(pady=self._padding, row=0, columnspan=3)

        self.decks_var = tk.IntVar(self, value=1)
        tk.Label(self, text="Decks: ").grid(sticky='w', row=1, column=0)
        tk.Spinbox(self, textvariable=self.decks_var, width=2, from_=1, to=8).grid(pady=self._padding, sticky='w', row=1, column=1)

        self.rounds_var = tk.IntVar(self, value=1000)
        tk.Label(self, text="Rounds: ").grid(sticky='w', row=2, column=0)
        tk.Spinbox(self, textvariable=self.rounds_var, width=7, from_=1, to=100000, increment=100).grid(pady=self._padding, sticky='w', row=2, column=1)

        self.minimum_bet_var = tk.IntVar(self, value=100)
        tk.Label(self, text="Minimum bet: ").grid(sticky='w', row=3, column=0)
        tk.Spinbox(self, textvariable=self.minimum_bet_var, width=7, from_=100, to=99999, increment=100).grid(pady=self._padding, sticky='w', row=3, column=1)
        
        self.maximum_bet_var = tk.IntVar(self, value=3000)
        tk.Label(self, text="Maximum bet: ").grid(sticky='w', row=4, column=0)
        tk.Spinbox(self, textvariable=self.maximum_bet_var, width=7, from_=101, to=100000, increment=100).grid(pady=self._padding, sticky='w', row=4, column=1)

        self.chips_var = tk.IntVar(self, value=5000)
        tk.Label(self, text="Chips: ").grid(sticky='w', row=5, column=0)
        tk.Label(self, textvariable=self.chips_var, width=6).grid(sticky='e', row=5, column=2)
        tk.Scale(self, variable=self.chips_var, orient='horizontal', troughcolor='white', showvalue=0, from_=100, to=100000, resolution=100).grid(pady=self._padding, sticky='w', row=5, column=1)

        self.basic_strategy_state = tk.BooleanVar(self, value=True)
        tk.Label(self, text="Basic strategy: ").grid(sticky='w', row=6, column=0)
        tk.Checkbutton(self, variable=self.basic_strategy_state, onvalue=True, offvalue=False).grid(pady=self._padding, sticky='w', row=6, column=1)

        self.card_counter_state = tk.BooleanVar(self, value=False)
        tk.Label(self, text="Card counter: ").grid(sticky='w', row=7, column=0)
        tk.Checkbutton(self, variable=self.card_counter_state, onvalue=True, offvalue=False, command=self._select_system).grid(pady=self._padding, sticky='w', row=7, column=1)
        
        self.counting_system_var = tk.StringVar(self)
        
        for widget in self.grid_slaves():
            widget.configure(background='white', bd=0)
    
    def _get_counting_system_names(self) -> list:
        """Visszaadja azoknak lapszámolási technikák nevét, amik megtalálhatóak az erre létrehozott mappában.
        
        Returns:
            list: A lapszámolási technikák neveinek a listája.
        """
        return [os.path.splitext(f)[0] for f in os.listdir('basic_data/counting_systems')]

    def _select_system(self) -> None:
        """Ha be van állítva a lapszámolás, akkor ki lehet választani, hogy melyik technika legyen alkalmazva a szimuláció során."""
        if self.card_counter_state.get():
            self._counting_system_label = tk.Label(self, background='white', text="System: ")
            self._counting_system_label.grid(sticky='w', row=8, column=0)
            self._counting_system_combobox = ttk.Combobox(self, width=16, state='readonly', textvariable=self.counting_system_var, values=self._get_counting_system_names())
            self._counting_system_combobox.current(0)
            self._counting_system_combobox.grid(pady=self._padding, row=8, column=1, columnspan=2)
        else:
            self._counting_system_label.destroy()
            self._counting_system_combobox.destroy()

class Simulation_window(tk.Tk):
    """Egy ablakot definiál, ami ha van régebbi szimulációs adat akkor annak a statisztikáját jeleníti meg és, emelett új szimulációra is ad lehetőséget."""
    def __init__(self) -> None:
        super().__init__()
        self.title('Epic blackjack simulator by Csabi')
        self.configure(background='white', padx=15, pady=15)
        self.resizable(False,False)
        style = ttk.Style()
        style.map('TCombobox', fieldbackground=[('readonly','white')])
        style.map('TCombobox', selectbackground=[('readonly', 'white')])
        style.map('TCombobox', selectforeground=[('readonly', 'black')])

        self._save_file = 'save/last_statistics.json'
        self._statistics_frame = Statistics_frame(self)
        self._statistics_frame.grid(column=0, rowspan=2)
        if os.path.isfile(self._save_file): 
            self._last_data = self._load_last_statistics()
            self._statistics_frame.update(self._last_data)

        self._form_frame = Form_frame(self)
        self._form_frame.grid(row=0, column=1, padx=20)

        tk.Button(self._form_frame, text='Simulate game', background='white', command=self._new_simulation).grid(sticky='we', row=9, columnspan=3, padx=20, pady=15)

        self.eval('tk::PlaceWindow . center')

    def _plot(self, stat:list, file_name:str) -> None:
        """Grafikon formájában menti el, hogy a szimúláció során a játékosnak a körök után mennyi zsetonja volt.
        
        Args:
            stat (list): A körök utáni zseton mennyiségek.
            file_name (str): Megadja, hogy milyen néven legyen elmentve a grafikon képe.
        """
        fig, ax = plt.subplots()
        ax.tick_params(axis='both', which='major', labelsize=7)
        ax.set_xlabel('Rounds')
        ax.set_title('Last simulation')
        ax.set_ylabel('Chips')
        ax.plot(stat)
        fig.savefig(file_name)

    def _save_statistics(self) -> None: 
        """JSON formátumban elmenti a szimuláció adatait."""
        with open(self._save_file, "wt") as f:
            json.dump(self._last_data, f)

    def _load_last_statistics(self) -> dict:
        """Betölti az utolsó szimuláció adatait.
        
        Returns:
            dict: A szimuláció adatai.
        """
        with open(self._save_file) as f:
            return json.load(f)

    def _simulation(self) -> None:
        """Leszimulál egy játékot a megadott adatok alapján, majd elmenti azt."""
        history = []
        decks = self._form_frame.decks_var.get()
        rounds = self._form_frame.rounds_var.get() 
        min_bet = self._form_frame.minimum_bet_var.get()
        max_bet = self._form_frame.maximum_bet_var.get()
        chips = self._form_frame.chips_var.get()
        system_state = self._form_frame.card_counter_state.get()
        system = self._form_frame.counting_system_var.get()

        if rounds > 100000: raise Exception('Invalid rounds value')
        else:
            basic_strategy = self._form_frame.basic_strategy_state.get()
            ai = AI(chips)
            g = Game_simulation(ai, min_bet, max_bet, decks)
            if system_state: ai.set_card_counter(system, decks)
            if basic_strategy: ai.set_basic_strategy()
 
            for i in range(rounds): 
                g.round()
                if system_state: ai.view_cards_on_the_table(g.get_cards_on_the_table())
                history.append(g.get_player_chips_value())

            plot_fname = 'save/last_statistics.png'
            self._plot(history, plot_fname)

            self._last_data = {
                "deck_count": decks,
                "rounds": rounds,
                "min_bet": min_bet,
                "max_bet": max_bet,
                "chips": chips,
                "basic_strategy": basic_strategy,
                "bet_system": system if system_state else system_state,
                "history": history,
                "plot_img": plot_fname
            }
            self._save_statistics()
            self._statistics_frame.update(self._last_data)

    def _new_simulation(self) -> None:
        """Ha hiba nélkül futtatható a szimuláció akkor lefuttatja, ha nem, akkor hibaüzenet formájában értésíti a felhasználót a probléma okáról."""
        try: self._simulation()
        except Exception as e: messagebox.showerror('Error', e)

if __name__ == '__main__':
    w = Simulation_window()
    w.mainloop() 
