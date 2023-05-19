import kivy
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.graphics import Color, Rectangle
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout
import requests

kivy.require('1.0.9')




class CurrencyConverterApp(App):

    CURRENCY_COUNTRY_MAP = {
        'USD': 'United States',
        'EUR': 'European Union',
        'GBP': 'United Kingdom',
        'JPY': 'Japan',
        'CAD': 'Canada',
        'AUD': 'Australia',
        'CNY': 'China',
        'INR': 'India',
        'NZD': 'New Zealand',
        'BRL': 'Brazil',
        'ZAR': 'South Africa',
        'PLN': 'Poland',
        'AFN': 'Afghanistan',
        'BDT': 'Bangladesh',
        'BYN': 'Belarus',
        'BGN': 'Bulgaria',
        'COP': 'Colombia',
        'CZK': 'Czech Republic',
        'DOP': 'Dominican Republic',
        'EGP': 'Egypt',
        'HKD': 'Hong-Kong',
        'HUF': 'Hungary',
        'ISK': 'Iceland',
        'IDR': 'Indonesia',
        'IRR': 'Iran',
        'ILS': 'Israel',
        'JMD': 'Jamaica',
        'KZT': 'Kazahstan',
        'KRW': 'Korea',
        'KES': 'Kenya',
        'LRD': 'Liberia',
        'LBP': 'Lebanon',
        'MGA': 'Madagascar',
        'MYR': 'Malaysia',
        'MVR': 'Maldives',
        'MXN': 'Mexico',
        'MAD': 'Morocco',
        'NDK': 'Norway',
        'PHP': 'Philippines',
        'RON': 'Romania',
        'RUB': 'Russia',
        'SGD': 'Singapore',
        'SEK': 'Sweden',
        'CHF': 'Switzerland',
        'THB': 'Thailand',
        'TRY': 'Turkey',
        'TND': 'Tunisia',
        'UAH': 'Ukraine',
        'AED': 'United Arab Emirates'
    }
    
    def build(self):
        self.title = 'Currency Converter'

        # Fetch all available currencies from the API
        response = requests.get("https://api.exchangerate-api.com/v4/latest/USD")
        data = response.json()
        self.currencies = [f'{code} ({self.CURRENCY_COUNTRY_MAP.get(code)})' 
                           for code in data['rates'].keys() if code in self.CURRENCY_COUNTRY_MAP.keys()]
        
        # Use a grid layout
        layout = GridLayout(cols=2)

        with layout.canvas.before:
            Color(0.9, 1, 1)  # You can set your own RGB color
            self.rect = Rectangle(size=layout.size, pos=layout.pos)

        layout.bind(size=self._update_rect, pos=self._update_rect)

        # Add widgets
        self.from_currency = Spinner(
            text=self.currencies[0],
            values=self.currencies,
            size_hint=(.5, .1))
        layout.add_widget(self.from_currency)

        self.to_currency = Spinner(
            text=self.currencies[1],
            values=self.currencies,
            size_hint=(.5, .1))
        layout.add_widget(self.to_currency)

        self.amount = TextInput(hint_text="Enter amount", multiline=False, size_hint=(1, .1), background_color = (240,248,255))
        layout.add_widget(self.amount)

        self.result = Label(text='')
        layout.add_widget(self.result)

        convert_button = Button(text='Convert', size_hint=(1, .1), background_color = (0.5,0.6,0.9))
        convert_button.bind(on_release=self.convert)
        layout.add_widget(convert_button)

        return layout
    
    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def convert(self, instance):
        amount = float(self.amount.text)
        from_currency = self.from_currency.text[:3]
        to_currency = self.to_currency.text[:3]

        response = requests.get(f"https://api.exchangerate-api.com/v4/latest/{from_currency}")
        data = response.json()

        rate = data['rates'][to_currency]
        converted_amount = amount * rate

        self.result.text = f"{amount} {from_currency} is equivalent to {converted_amount} {to_currency}"


if __name__ == "__main__":
    CurrencyConverterApp().run()



