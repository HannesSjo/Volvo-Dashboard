from kivy.graphics import Line, Color, Canvas
from kivy.uix.label import Label
from kivy.uix.relativelayout import RelativeLayout
from utils.constants import Constants

class MiniGauge:
    def __init__(self, layout, position, value, minValue, maxValue, size, unit):
        adjusted_position = (position[0] - size / 2, position[1])
        
        self.layout = RelativeLayout(pos=adjusted_position, size=(size, size))
        self.value = value
        self.minValue = minValue
        self.maxValue = maxValue
        self.unit = unit
        self.size = size

        layout.add_widget(self.layout)
        self.Setup()

    def Update(self, newValue):
        if newValue == self.value:
            return
        
        self.value = newValue
        
        self.valueLabel.text = str(self.value)

        angle = 270 + ((self.value - self.minValue) / (self.maxValue - self.minValue)) * 180
        
        self.updateGauge(angle)

    def updateGauge(self, angle):
        self.gauge_drawing_canvas.clear()

        with self.gauge_drawing_canvas:
            Color(*Constants.dakGrey())
            Line(circle=(self.size / 2, self.size / 2, self.size / 2 - 10, 270, 270 + 180), width=self.getSize(4))
            Color(*Constants.white())
            Line(circle=(self.size / 2, self.size / 2, self.size / 2 - 10, 270, angle), width=self.getSize(3))

    def Setup(self):
        self.valueLabel = Label(text=str(self.value),
                                font_name=Constants.font(),
                                size_hint=(None, None),
                                font_size=self.getFontSize(12))
        
        self.unitLabel = Label(text=self.unit,
                                font_name=Constants.font(),
                                size_hint=(None, None),
                                font_size=self.getFontSize(4))

        
        self.valueLabel.color = Constants.white()
        self.unitLabel.color = Constants.white()
        
        self.layout.add_widget(self.valueLabel)
        self.layout.add_widget(self.unitLabel)

        self.valueLabel.center = (self.size / 2, self.size / 2 + self.getSize(19))
        self.unitLabel.center = (self.size / 2, self.size / 2 + self.getSize(1.8))
        
        self.gauge_drawing_canvas = Canvas()
        self.layout.canvas.add(self.gauge_drawing_canvas)

        angle = 270 + ((self.value - self.minValue) / (self.maxValue - self.minValue)) * 180
        self.updateGauge(angle)

    def getSize(self, size):
        return self.size * (size/100)

    def getFontSize (self, size):
        return self.size * (size * 0.02)