from kivy.app import App
from kivy.uix.button import Label
from kivy.core.window import Window

class HelloWorldApp(App):
    size = 800; 

    def build(self):
        Window.size = (self.size, self.size);
        return Label(text="Hello world")


if __name__ == '__main__':
    HelloWorldApp().run()
