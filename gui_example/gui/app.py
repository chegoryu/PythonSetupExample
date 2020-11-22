from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button


class CalcButton(Button):
    def __init__(self, **kwargs):
        super(CalcButton, self).__init__(**kwargs)

        self.counter = 0
        self.bind(on_press=CalcButton._on_press)
        self._update_text()


    def _update_text(self):
        self.text = 'Click me! ({})'.format(self.counter)


    def _update_counter(self):
        self.counter += 1


    @staticmethod
    def _on_press(instance):
        instance._update_counter()
        instance._update_text()


class MainLayout(BoxLayout):
    def __init__(self, **kwargs):
        super(MainLayout, self).__init__(**kwargs)

        self.orientation = 'vertical'

        self.calc_button = CalcButton()
        self.add_widget(self.calc_button)


class MainApp(App):
    def build(self):
        self.title = 'GUI example'

        return MainLayout()
