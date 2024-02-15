import kivy
from kivy.app import App
from kivy.uix.label import Label

class NeuralRandom(App):
    
    def build(self):
        return Label(text="NeuralRandom")

neuralRandom= NeuralRandom()
neuralRandom.run()