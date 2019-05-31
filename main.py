import threading

from kivy.app import App
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.widget import Widget

from Cristalization import dyslocation
from Expansion.Radius import Radius
from Expansion.User import User
from Smoothing import algorithm
from Smoothing.algorithm import calculate_energy
from Utility.Drawing import Drawing
from Utility.RandomCase import RandomCase
from Utility.Uniform import Uniform


class Board(Widget):

    def __init__(self, **kwargs):
        super(Board, self).__init__(**kwargs)
        self.bind(on_touch_down=self.touch_down)

        self.register_event_type('on_test')

    def touch_down(self, _, touch):
        self.dispatch('on_test', touch)
        print(touch)

    def on_test(self, touch):
        pass


class NewClass(FloatLayout):

    def __init__(self, **kwargs):
        super(NewClass, self).__init__(**kwargs)

        self.speed = 1.0
        self.mesh_height = int(1)
        self.mesh_width = int(1)
        self.callback_cout = 1
        self.animation_length = 100
        self.border_condition = False
        self.neighbourhood_type = 'von Neumann'
        self.hex_type = 'random'
        self.no_iteration = 1
        self.kt = 0.2

        self.with_radius = 0

        self.radiusLabel = None
        self.rowLabel = None
        self.randomAmountLabel = None

        Window.size = (1100, 650)

        label = Label(text='Rozmiar siatki: ', pos_hint={'x': 0.02, 'y': 1.85}, size_hint=(.15, .09))
        self.add_widget(label)

        self.heightInput = TextInput(text='', size_hint=(.05, .09), pos_hint={'x': 0.17, 'y': 1.85}, multiline=False)
        self.heightInput.bind(text=lambda x, y: self.save_width(mesh_width=self.heightInput.text))
        self.add_widget(self.heightInput)

        self.widthInput = TextInput(text='', size_hint=(.05, .09), pos_hint={'x': 0.22, 'y': 1.85}, multiline=False)
        self.widthInput.bind(text=lambda x, y: self.save_height(mesh_height=self.widthInput.text))
        self.add_widget(self.widthInput)

        label = Label(text='Sasiedztwo: ', pos_hint={'x': 0.02, 'y': 1.75}, size_hint=(.15, .09))
        self.add_widget(label)

        btn1 = ToggleButton(text='z promieniem', group='neighbourhood_type', size_hint=(.15, .09),
                            pos_hint={'x': 0.07, 'y': 1.65})
        btn1.bind(on_press=lambda x: self.save_neighbourhood_type(nbr_type='radius'))
        self.add_widget(btn1)

        btn1 = ToggleButton(text='von Neumann', group='neighbourhood_type', state='down', size_hint=(.15, .09),
                            pos_hint={'x': 0.07, 'y': 1.55})
        btn1.bind(on_press=lambda x: self.save_neighbourhood_type(nbr_type='von Neumann'))
        self.add_widget(btn1)
        btn2 = ToggleButton(text='Moore', group='neighbourhood_type', size_hint=(.15, .09),
                            pos_hint={'x': 0.07, 'y': 1.45})
        btn2.bind(on_press=lambda x: self.save_neighbourhood_type(nbr_type='Moore'))
        self.add_widget(btn2)

        hexButton = ToggleButton(text='Heksagonalne', group='neighbourhood_type',
                                 size_hint=(.15, .09),
                                 pos_hint={'x': 0.07, 'y': 1.35})
        hexButton.bind(on_press=lambda x: self.save_neighbourhood_type(nbr_type='hexagonal'))
        self.add_widget(hexButton)

        pentaButton = ToggleButton(text='Pentagonalne', group='neighbourhood_type', size_hint_x=None,
                                   size_hint=(.15, .09),
                                   pos_hint={'x': 0.07, 'y': 1.25})
        pentaButton.bind(on_press=lambda x: self.save_neighbourhood_type(nbr_type='pentagonal'))
        self.add_widget(pentaButton)

        # -----------------------------------

        label = Label(text='Zarodkowanie: ', pos_hint={'x': 0.02, 'y': 1.1}, size_hint=(.15, .09))
        self.add_widget(label)

        randomButton = ToggleButton(text='Losowe', group='zarodkowanie', size_hint_x=None, size_hint=(.15, .09),
                                    pos_hint={'x': 0.07, 'y': 1})
        randomButton.bind(on_press=lambda x: self.save_embryo_type(embryo_type='random'))
        self.add_widget(randomButton)

        randomButton = ToggleButton(text='Z promieniem', group='zarodkowanie', size_hint_x=None, size_hint=(.15, .09),
                                    pos_hint={'x': 0.07, 'y': 0.9})
        randomButton.bind(on_press=lambda x: self.save_embryo_type(embryo_type='radius'))
        self.add_widget(randomButton)

        randomButton = ToggleButton(text='Jednorodne', group='zarodkowanie', size_hint_x=None, size_hint=(.15, .09),
                                    pos_hint={'x': 0.07, 'y': .8})
        randomButton.bind(on_press=lambda x: self.save_embryo_type(embryo_type='uniform'))
        self.add_widget(randomButton)

        randomButton = ToggleButton(text='Ręczne', group='zarodkowanie', size_hint_x=None, size_hint=(.15, .09),
                                    pos_hint={'x': 0.07, 'y': .7})
        randomButton.bind(on_press=lambda x: self.save_embryo_type(embryo_type='user_input'))
        self.add_widget(randomButton)

        label = Label(text='Warunki brzegowe: ', pos_hint={'x': 0.03, 'y': .5}, size_hint=(.15, .09))
        self.add_widget(label)

        btn1 = ToggleButton(text='absorbujące', group='border_condition', state='down', size_hint=(.15, .09),
                            pos_hint={'x': 0.07, 'y': .4})
        btn1.bind(on_press=lambda x: self.save_border_condition(state=False))
        self.add_widget(btn1)
        btn2 = ToggleButton(text='perdiodyczne', group='border_condition', size_hint=(.15, .09),
                            pos_hint={'x': 0.07, 'y': .3})
        btn2.bind(on_press=lambda x: self.save_border_condition(state=True))
        self.add_widget(btn2)

        resetButton = Button(text='RESET', size_hint_x=None, size_hint=(.15, .09),
                             pos_hint={'x': 0.02, 'y': 0.1})
        resetButton.bind(on_press=lambda x: self.reset())
        self.add_widget(resetButton)

        self.animation = Button(text='START', size_hint=(.15, .09),
                                background_color=(1, 0, 0, 1), pos_hint={'x': 0.18, 'y': .1})
        self.animation.bind(on_press=self.call_animation)
        self.add_widget(self.animation)

        board = Board(pos_hint={'x': .5, 'y': .5}, size_hint=(.2, .1))
        board.bind(on_test=self.on_board_event)
        self.add_widget(board)

    def reset(self):

        if hasattr(self, "nr_of_embryos"):
            self.remove_widget(self.nr_of_embryos)
        if self.radiusLabel is not None:
            self.remove_widget(self.radiusLabel)
            self.remove_widget(self.radiusAmount)
            self.remove_widget(self.amountLabel)
            self.remove_widget(self.amount)
        if self.randomAmountLabel is not None:
            self.remove_widget(self.randomAmountLabel)
            self.remove_widget(self.randomAmount)
        if self.rowLabel is not None:
            self.remove_widget(self.rowLabel)
            self.remove_widget(self.rowAmount)
            self.remove_widget(self.columnLabel)
            self.remove_widget(self.columnAmount)

        self.cancel_animation()

        self.__delattr__('drawing')
        wid.canvas.clear()
        self.heightInput.text = ''
        self.widthInput.text = ''

    def on_board_event(self, _, touch):

        if hasattr(self, 'drawing'):
            User.create_user_input(mesh_height=self.mesh_height, mesh_width=self.mesh_width, touch=touch,
                                   drawing=self.drawing)

    def save_border_condition(self, state):
        self.border_condition = state

    def save_neighbourhood_type(self, nbr_type):
        self.neighbourhood_type = nbr_type

        if hasattr(self, 'btn1'):
            self.remove_widget(self.btn1)
            self.remove_widget(self.btn2)
            self.remove_widget(self.btn3)
        if hasattr(self, 'with_radiusLabel'):
            self.remove_widget(self.with_radiusLabel)
            self.remove_widget(self.with_radiusAmount)

        if self.neighbourhood_type == 'hexagonal':
            self.hexagonal()

        if self.neighbourhood_type == 'radius':
            self.with_radius_method()

    def save_embryo_type(self, embryo_type):

        if hasattr(self, "nr_of_embryos"):
            self.remove_widget(self.nr_of_embryos)
        if self.radiusLabel is not None:
            self.remove_widget(self.radiusLabel)
            self.remove_widget(self.radiusAmount)
            self.remove_widget(self.amountLabel)
            self.remove_widget(self.amount)
        if self.randomAmountLabel is not None:
            self.remove_widget(self.randomAmountLabel)
            self.remove_widget(self.randomAmount)
        if self.rowLabel is not None:
            self.remove_widget(self.rowLabel)
            self.remove_widget(self.rowAmount)
            self.remove_widget(self.columnLabel)
            self.remove_widget(self.columnAmount)

        if embryo_type == 'random':
            self.losowe()
        elif embryo_type == 'radius':
            self.z_promieniem()
        elif embryo_type == 'uniform':
            self.jednorodne()
        elif embryo_type == 'user_input':
            pass

    def with_radius_method(self):

        self.drawing.draw_center_points(self.mesh_height, self.mesh_width)

        self.with_radiusLabel = Label(text="promien", pos_hint={'x': 0.25, 'y': 1.65}, size_hint_x=None,
                                      size_hint=(.07, .09))
        self.add_widget(self.with_radiusLabel)
        self.with_radiusAmount = TextInput(size_hint_x=None, size_hint=(.03, .09), pos_hint={'x': 0.32, 'y': 1.65},
                                           multiline=False)
        self.with_radiusAmount.bind(
            on_text_validate=lambda x: self.save_with_radius(radius=self.with_radiusAmount.text))
        self.add_widget(self.with_radiusAmount)

    def save_hex_type(self, hex_type):
        self.hex_type = hex_type

    def save_with_radius(self, radius):
        self.with_radius = int(radius)

        # create mesh woth points

    def hexagonal(self):

        self.btn1 = ToggleButton(text='lewe', group='hex_type', size_hint=(.07, .09),
                                 pos_hint={'x': 0.25, 'y': 1.45}, disabled=True)
        self.btn1.bind(on_press=lambda x: self.save_hex_type(hex_type='left'))
        self.add_widget(self.btn1)
        self.btn2 = ToggleButton(text='prawe', group='hex_type', size_hint=(.07, .09),
                                 pos_hint={'x': 0.25, 'y': 1.35}, disabled=True)
        self.btn2.bind(on_press=lambda x: self.save_hex_type(hex_type='right'))
        self.add_widget(self.btn2)
        self.btn3 = ToggleButton(text='losowe', group='hex_type', size_hint=(.07, .09),
                                 pos_hint={'x': 0.25, 'y': 1.25}, disabled=True)
        self.btn3.bind(on_press=lambda x: self.save_hex_type(hex_type='random'))
        self.add_widget(self.btn3)

    def losowe(self):

        self.randomAmountLabel = Label(text="ilosc", pos_hint={'x': 0.25, 'y': 1}, size_hint_x=None,
                                       size_hint=(.05, .09))
        self.add_widget(self.randomAmountLabel)
        self.randomAmount = TextInput(size_hint_x=None, size_hint=(.05, .09), pos_hint={'x': 0.32, 'y': 1},
                                      multiline=False)
        self.randomAmount.bind(
            on_text_validate=lambda x: RandomCase.create_random(drawing=self.drawing, amount=self.randomAmount.text,
                                                                mesh_width=self.mesh_width,
                                                                mesh_height=self.mesh_height))
        self.add_widget(self.randomAmount)

    def z_promieniem(self):

        self.radiusLabel = Label(text="promien", pos_hint={'x': 0.25, 'y': .95}, size_hint_x=None,
                                 size_hint=(.07, .09))
        self.add_widget(self.radiusLabel)
        self.radiusAmount = TextInput(size_hint_x=None, size_hint=(.03, .09), pos_hint={'x': 0.32, 'y': .95},
                                      multiline=False)
        self.add_widget(self.radiusAmount)

        self.amountLabel = Label(text="ilosc", pos_hint={'x': 0.25, 'y': 0.85}, size_hint_x=None, size_hint=(.05, .09))
        self.add_widget(self.amountLabel)
        self.amount = TextInput(size_hint_x=None, size_hint=(.03, .09), pos_hint={'x': 0.32, 'y': .85},
                                multiline=False)
        self.amount.bind(
            on_text_validate=lambda x: Radius.create_radius(newclass=self,
                                                            drawing=self.drawing, radius=self.radiusAmount.text,
                                                            amount=self.amount.text, mesh_width=self.mesh_width,
                                                            mesh_height=self.mesh_height))
        self.add_widget(self.amount)

    def jednorodne(self):

        self.rowLabel = Label(text="wiersz", pos_hint={'x': .25, 'y': .85}, size_hint_x=None, size_hint=(.05, .09),
                              id="rowLabel")
        self.add_widget(self.rowLabel)

        self.rowAmount = TextInput(size_hint_x=None, size_hint=(.05, .09), pos_hint={'x': 0.32, 'y': .85},
                                   multiline=False)
        self.add_widget(self.rowAmount)

        self.columnLabel = Label(text="kolumna", pos_hint={'x': .25, 'y': .75}, size_hint_x=None,
                                 size_hint=(.05, .09))
        self.add_widget(self.columnLabel)
        self.columnAmount = TextInput(size_hint_x=None, size_hint=(.05, .09), pos_hint={'x': 0.32, 'y': .75},
                                      multiline=False)
        self.columnAmount.bind(
            on_text_validate=lambda x: Uniform.create_uniform(drawing=self.drawing, row=self.rowAmount.text,
                                                              column=self.columnAmount.text,
                                                              mesh_height=self.mesh_height,
                                                              mesh_width=self.mesh_width))
        self.add_widget(self.columnAmount)

    def print_no_embryos(self, nr):
        self.nr_of_embryos = Label(text="Znaleziono:" + str(nr), pos_hint={'x': 0.2, 'y': 0.5}, size_hint_x=None,
                                   size_hint=(.2, .55))
        self.add_widget(self.nr_of_embryos)

    def call_animation(self, *args):

        if self.neighbourhood_type == 'hexagonal':
            self.animate_hexagonal()
        if self.neighbourhood_type == 'radius':
            self.animate_radius()
        else:
            self.animate_rest()

    def animate_hexagonal(self, *args):

        # keep_going = self.drawing.draw_animation()

        self.t = threading.Timer(self.speed, self.animate_hexagonal)
        self.t.start()

        print(self.neighbourhood_type)
        print(self.hex_type)

        keep_going = self.drawing.draw_animation(self.border_condition, self.neighbourhood_type, self.hex_type, None)

        if not keep_going:
            self.cancel_animation()

    def animate_radius(self, *args):

        self.t = threading.Timer(self.speed, self.animate_radius)
        self.t.start()

        keep_going = self.drawing.draw_animation(self.border_condition, self.neighbourhood_type, None, self.with_radius)

        if not keep_going:
            self.cancel_animation()

    def animate_rest(self, *args):

        # keep_going = self.drawing.draw_animation()

        self.t = threading.Timer(self.speed, self.animate_rest)
        self.t.start()

        keep_going = self.drawing.draw_animation(self.border_condition, self.neighbourhood_type, None, None)

        if not keep_going:
            self.cancel_animation()

    def cancel_animation(self):

        if hasattr(self, 't'):
            self.t.cancel()

        if self.animation is not None:
            self.remove_widget(self.animation)

            self.wygladzanie = ToggleButton(text='Wygładzanie ziaren', size_hint=(.15, .09),
                                      background_color=(0, 1, 0, 1), pos_hint={'x': 0.18, 'y': .1})
            self.wygladzanie.bind(on_press=self.wygladzanie_ziaren)
            self.add_widget(self.wygladzanie)

            self.animation = ToggleButton(text='Gęstość dyslokacji', size_hint=(.15, .09),
                                    background_color=(0, 1, 0, 1), pos_hint={'x': 0.35, 'y': .1})
            self.animation.bind(on_press=self.dyslokacje)
            self.add_widget(self.animation)

    def dyslokacje(self, *args):
        dyslocation.algorithm(self.drawing.surface, self.mesh_width, self.mesh_height)

        print("back in main")
        self.drawing.draw_dislocations()
        print("aaaaand back")

    def wygladzanie_ziaren(self, *args):
        self.clear_widgets()

        self.calculate_energy()

        btn1 = ToggleButton(text='Mikrostruktura', group='view_type', state='down', size_hint=(.13, .09),
                            pos_hint={'x': 0.04, 'y': 1.85})
        btn1.bind(on_press=lambda x: self.view(view_type='mikrostruktura'))
        self.add_widget(btn1)
        btn2 = ToggleButton(text='Energia', group='view_type', size_hint=(.13, .09),
                            pos_hint={'x': 0.18, 'y': 1.85})
        btn2.bind(on_press=lambda x: self.view(view_type='energia'))
        self.add_widget(btn2)

        label = Label(text='Sasiedztwo: ', pos_hint={'x': 0.02, 'y': 1.65}, size_hint=(.15, .09))
        self.add_widget(label)

        btn1 = ToggleButton(text='z promieniem', group='neighbourhood_type', size_hint=(.15, .09),
                            pos_hint={'x': 0.07, 'y': 1.55})
        btn1.bind(on_press=lambda x: self.save_neighbourhood_type(nbr_type='radius'))
        self.add_widget(btn1)

        btn1 = ToggleButton(text='von Neumann', group='neighbourhood_type', state='down', size_hint=(.15, .09),
                            pos_hint={'x': 0.07, 'y': 1.45})
        btn1.bind(on_press=lambda x: self.save_neighbourhood_type(nbr_type='von Neumann'))
        self.add_widget(btn1)
        btn2 = ToggleButton(text='Moore', group='neighbourhood_type', size_hint=(.15, .09),
                            pos_hint={'x': 0.07, 'y': 1.35})
        btn2.bind(on_press=lambda x: self.save_neighbourhood_type(nbr_type='Moore'))
        self.add_widget(btn2)

        hexButton = ToggleButton(text='Heksagonalne', group='neighbourhood_type',
                                 size_hint=(.15, .09),
                                 pos_hint={'x': 0.07, 'y': 1.25})
        hexButton.bind(on_press=lambda x: self.save_neighbourhood_type(nbr_type='hexagonal'))
        self.add_widget(hexButton)

        pentaButton = ToggleButton(text='Pentagonalne', group='neighbourhood_type', size_hint_x=None,
                                   size_hint=(.15, .09),
                                   pos_hint={'x': 0.07, 'y': 1.15})
        pentaButton.bind(on_press=lambda x: self.save_neighbourhood_type(nbr_type='pentagonal'))
        self.add_widget(pentaButton)

        self.wygladzanie_iloscLabel = Label(text="Liczba iteracji", pos_hint={'x': 0.08, 'y': .9}, size_hint_x=None,
                                            size_hint=(.05, .09))
        self.add_widget(self.wygladzanie_iloscLabel)
        wygladzanie_iloscInput = TextInput(size_hint_x=None, size_hint=(.03, .09), pos_hint={'x': 0.20, 'y': .9},
                                           multiline=False)
        wygladzanie_iloscInput.bind(
            on_text_validate=lambda x: self.save_no_iteration_for_smoothing(no_iteration=wygladzanie_iloscInput.text))
        self.add_widget(wygladzanie_iloscInput)

        self.ktLabel = Label(text="Wartość kt", pos_hint={'x': 0.08, 'y': .8}, size_hint_x=None, size_hint=(.05, .09))
        self.add_widget(self.ktLabel)
        self.ktInput = TextInput(size_hint_x=None, size_hint=(.03, .09), pos_hint={'x': 0.20, 'y': .8},
                                 multiline=False)
        self.ktInput.bind(on_text_validate=lambda x: self.save_kt(kt=self.ktInput.text))
        self.add_widget(self.ktInput)

        label = Label(text='Warunki brzegowe: ', pos_hint={'x': 0.03, 'y': .6}, size_hint=(.15, .09))
        self.add_widget(label)

        btn1 = ToggleButton(text='absorbujące', group='border_condition', state='down', size_hint=(.15, .09),
                            pos_hint={'x': 0.07, 'y': .5})
        btn1.bind(on_press=lambda x: self.save_border_condition(state=False))
        self.add_widget(btn1)
        btn2 = ToggleButton(text='perdiodyczne', group='border_condition', size_hint=(.15, .09),
                            pos_hint={'x': 0.07, 'y': .4})
        btn2.bind(on_press=lambda x: self.save_border_condition(state=True))
        self.add_widget(btn2)

        resetButton = Button(text='GO BACK', size_hint_x=None, size_hint=(.15, .09),
                             pos_hint={'x': 0.02, 'y': 0.1})
        resetButton.bind(on_press=lambda x: self.go_back())
        self.add_widget(resetButton)

        self.animation = Button(text='START', size_hint=(.15, .09),
                                background_color=(1, 0, 0, 1), pos_hint={'x': 0.18, 'y': .1})
        self.animation.bind(on_press=lambda x: self.start_smoothing())
        self.add_widget(self.animation)

    def calculate_energy(self):
        for x in range(self.mesh_height):
            for y in range(self.mesh_width):
                calculate_energy(self.drawing.surface, self.drawing.surface[x][y], self.mesh_height, self.mesh_width,
                                 self.border_condition, self.neighbourhood_type,
                                 self.hex_type, self.with_radius)

    def view(self, view_type):
        if view_type == 'mikrostruktura':
            self.drawing.draw_all_points()
           # self.start_smoothing()
        elif view_type == 'energia':
            self.drawing.draw_energy()

    def go_back(self):
        pass

    def start_smoothing(self):
        for i in range(self.no_iteration):
            # wid.canvas.clear()

            algorithm.Algorithm.iteration(self.drawing, self.drawing.surface, self.mesh_width, self.mesh_height,
                                          self.border_condition,
                                          self.neighbourhood_type, self.kt, self.hex_type, self.with_radius)

    def save_kt(self, kt):
        if kt is not '':

            if float(0.1 <= float(kt) <= 0.6):
                self.kt = float(kt)
                print('kt', self.kt)
                if hasattr(self, 'nr_kt'):
                    self.remove_widget(self.nr_kt)
            else:
                self.ktInput.text = ''
                self.nr_kt = Label(text="Zakres kt: <0.1-6>", pos_hint={'x': 0.2, 'y': 0.55},
                                   size_hint_x=None,
                                   size_hint=(.2, .55))
                self.add_widget(self.nr_kt)

    def save_no_iteration_for_smoothing(self, no_iteration):
        if no_iteration is not '':
            if int(no_iteration) < 0:
                return
            self.no_iteration = int(no_iteration)
            print('no_iteration', self.no_iteration)

    def save_width(self, mesh_width):
        if mesh_width != '' and int(mesh_width) >= 0:
            self.mesh_width = int(mesh_width)
            # create_mesh(self.mesh_width, self.mesh_height)

    def save_height(self, mesh_height):
        if mesh_height != '' and int(mesh_height) >= 0:
            self.mesh_height = int(mesh_height)

            self.drawing = Drawing(wid, self.mesh_width, self.mesh_height)
            self.drawing.create_mesh()


class RozrostZiarenApp(App):

    def build(self):
        root = BoxLayout(orientation='vertical')
        root.add_widget(wid)
        root.add_widget(NewClass())
        return root


if __name__ == '__main__':
    wid = Widget()
    RozrostZiarenApp().run()
