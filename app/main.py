from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.lang.builder import Builder
from kivy.utils import get_color_from_hex as hex
from math import *
from kivymd.app import MDApp


Builder.load_file('main.kv')


class Home(Screen):
    operator = [['(', ')'], ['^', 'sqrt'], ['log', 'exp'], ['', ''], '+', '-', '*', '/']
    number, numberProp = range(9), ['.', '', '']
    assignment = [['=', 'c', 'ce'], ['->', '<-']]
    input_btn_background_color = hex('57C7BB')
    input_btn_background_normal = ''
    # optimal font size
    input_btn_font_size = 0.25
    # input_btn_font_size = 0.5

    def __init__(self, **kwargs):
        super(Home, self).__init__(**kwargs)
        self.name = 'homeSc'

    # init [+, -, *, /]
    def createOperatorWidgets(self, root):
        operator_0_bl = self.ids.operator_0_bl
        operator_1_bl = self.ids.operator_1_bl
        tmpOperator = list()
        try:
            # bl = BoxLayout(orientation='vertical')
            for x in self.operator:
                if isinstance(x, list):
                    # tmpOperator.append(x)
                    bl1 = BoxLayout(spacing=1)
                    for x1 in x:
                        btn = Button(text=str(x1),
                                     background_color=self.input_btn_background_color,
                                     background_normal=self.input_btn_background_normal)
                        btn.font_size = btn.size[1]*self.input_btn_font_size
                        btn.bind(on_release=lambda exp=btn: self.appendPrepExp(exp))
                        bl1.add_widget(btn)
                    operator_0_bl.add_widget(bl1)
                else:
                    tmpOperator.append(x)
            for x in tmpOperator:
                btn = Button(text=str(x),
                             background_color=self.input_btn_background_color,
                             background_normal=self.input_btn_background_normal)
                btn.font_size = btn.size[1] * self.input_btn_font_size
                btn.bind(on_release=lambda exp=btn: self.appendPrepExp(exp))
                operator_1_bl.add_widget(btn)

        except Exception as e:
            print('createOperatorWidgets: Failed')
            print(e)
            # raise e

    # init [0, 1, ..., 9]
    def createNumberWidgets(self, root):
        try:
            root.cols = 3
            for x in self.number:
                btn = Button(text=str(x),
                             background_color=self.input_btn_background_color,
                             background_normal=self.input_btn_background_normal)
                btn.font_size = btn.size[1] * self.input_btn_font_size
                btn.bind(on_release=lambda exp=btn: self.appendPrepExp(exp))
                root.add_widget(btn)
            # for number additional
            for x in self.numberProp:
                btn = Button(text=str(x),
                             background_color=self.input_btn_background_color,
                             background_normal=self.input_btn_background_normal)
                btn.font_size = btn.size[1] * self.input_btn_font_size
                btn.bind(on_release=lambda exp=btn: self.appendPrepExp(exp))
                root.add_widget(btn)

        except Exception as e:
            print('createNumberWidgets: Failed')
            print(e)
            # raise e

    # init [=, C, CE]
    def createAssignmentWidgets(self, root):
        try:
            bl = BoxLayout(spacing=1)
            for x in self.assignment:
                print(x)
                for x1 in x.__reversed__():
                    btn = Button(text=str(x1.upper()),
                                 background_color=self.input_btn_background_color,
                                 background_normal=self.input_btn_background_normal)
                    btn.font_size = btn.size[1] * self.input_btn_font_size
                    btn.bind(on_release=lambda btnRoot=btn: self.execAssignment(btnRoot))
                    bl.add_widget(btn)
                root.add_widget(bl)
                bl = BoxLayout(spacing=1)
        except Exception as e:
            print('createAssigmentWidgets: Failed')
            print(e)

    def appendPrepExp(self, exp):
        prepExp = self.ids.prep_exp
        brackets = str()

        def expChecking():
            nonlocal prepExp, brackets
            specialOperator = ['^', 'sqrt', 'log', 'exp']
            for x in specialOperator:
                if exp.text == x:
                    print(exp.text, ' = ', x)
                    brackets = '()'
                    break
        expChecking()
        prepExp.text += str(exp.text) + brackets
        brackets = str()

    def execAssignment(self, root):
        # assignment = root.text.lower()
        prepExp = self.ids.prep_exp
        result_bl, result = self.ids.result_bl, self.ids.result

        def calculate():
            print('calculating')
            result.text = str(prepExp.text) + ' = RESULT'
            prepExpString = prepExp.text
            try:
                finalResult = eval(prepExpString)
                result.text = str(f'{prepExp.text} = {finalResult}')
            except Exception as e:
                print(e)
                result.text = str(e)

        def clear():
            print('reseting prepExp Dec')
            # prepExp.text = prepExp.text[0: -1]
            # prepExpText = str()
            # if prepExp.focus:
            #     prepExp.focus = True
            #     i = 0
            #     for char in prepExp.text:
            #         if i == prepExp.cursor_col:
            #             print(f'index: {i}, '
            #                   f'\nprepExpCCol: {prepExp.cursor_col}, '
            #                   f'\nchar: {char}')
            #             char = ''
            #         prepExpText += char
            #         i += 1
            #     print(prepExpText)
            #     prepExp.text = prepExpText
            # else:
            prepExp.text = prepExp.text[0: -1]

        def clearEntire():
            print('reseting prepExp')
            prepExp.text = str('')

        def navLeft():
            prepExp.focus = True
            prepExp.cursor = (prepExp.cursor_col-1, 0)
            print('navLeft')

        def navRight():
            prepExp.focus = True
            prepExp.cursor = (prepExp.cursor_col+1, 0)
            print('navRight')

        print(prepExp.cursor_col)
        execAssignment = {'=': calculate,
                          'c': clear,
                          'ce': clearEntire,
                          '<-': navLeft,
                          '->': navRight}
        if isinstance(root, str):
            execAssignment[root]()
            self.ids.prep_exp.focus = True
        else:
            assignment = root.text.lower()
            execAssignment[assignment]()

    @staticmethod
    def appExit(self):
        print('appExit: Success')
        MainApp().get_running_app().stop()


class Sm(ScreenManager):
    pass


class MainApp(MDApp):
    def build(self):
        return Sm()


MainApp().run()
