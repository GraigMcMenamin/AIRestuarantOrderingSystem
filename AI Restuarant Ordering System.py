from gtts import gTTS
import pygame
import os
import time
import speech_recognition as sr

class BurgerBlissCLI:
    def __init__(self):
        self.menu = {
            "Burger": 5.99,
            "Fries": 2.99,
            "Soda": 1.99,
            "Ice Cream": 3.49
        }
        self.toppings_prices = {
            "lettuce": 0.5,
            "tomato": 0.5,
            "cheese": 1.0,
            "onions": 0.5,
            "pickles": 0.5,
            "bacon": 1.5,
            "Coke": 0.0,  # Soda variations have no extra cost
            "Sprite": 0.0,
            "Dr Pepper": 0.0,
            "Orange Soda": 0.0,
            "vanilla": 0.0,  # Ice Cream flavors have no extra cost
            "chocolate": 0.0,
            "swirl": 0.0
        }
        self.order = {}
        self.total_cost = 0.0
        

    def speech_to_text(self):
        """
        A method for converting speech from a microphone to text.
        :return: text
        """
        try:
            
            with sr.Microphone(1) as source:
                print("Listening for speech...")
                audio_data = self.recognizer.listen(source)

            text = self.recognizer.recognize_google(audio_data)
            print('speech:',text)
            return text
        except sr.UnknownValueError:
            print("Could not understand audio")
        except sr.RequestError as e:
            print(f"Could not request results; {e}")

    def find_word(self, word, string):
        """
        Check if a word exists in a given string.

        Parameters:
        word (str): The word to find.
        string (str): The string to search in.

        Returns:
        bool: True if the word is found, False otherwise.
        """
        word = word.lower()
        string = string.lower()
        return word in string

    def text_to_speech_and_play(self, text):
        # Create a unique filename with a timestamp
        timestamp = time.strftime("%Y%m%d%H%M%S")
        filename = f"temp_audio_{timestamp}.mp3"

        # converting text to speech and saving as MP3
        tts = gTTS(text, lang='en')
        tts.save(filename)

        # initialize pygame mixer
        pygame.mixer.init()
        pygame.mixer.music.load(filename)

        # play audio
        pygame.mixer.music.play()

        # wait for the audio to play before the program ends
        while pygame.mixer.music.get_busy():
            time.sleep(1)

        # clean up temp file
        # os.remove(filename)  THIS NEVER WORKS AND I HAVE TO REMOVE THEM MANUALLY


    def display_menu(self):
        print("Burger Bliss Menu:")
        for item, price in self.menu.items():
            print(f"{item}: ${price:.2f}")

    def take_order(self):
        text = "\nWelcome to Burger Bliss! Please place your order. Speak your order, and say 'done' when finished."
        self.text_to_speech_and_play(text)
        
        while True:
            # Speech to text
            text = "Please speak your order."
            self.text_to_speech_and_play(text)
            self.recognizer = sr.Recognizer()
            order_text = self.speech_to_text()

            if 'done' in order_text.lower():
                break

            # Check for specific words in the order
            items = ["Burger", "Fries", "Soda", "Ice Cream"]
            recognized_item = None
            for item in items:
                if self.find_word(item, order_text):
                    recognized_item = item
                    break

            if recognized_item:
                self.handle_customization(recognized_item)
            else:
                text = "Sorry, I couldn't recognize any items in your order."
                self.text_to_speech_and_play(text)


    def handle_customization(self, item):
        quantity_text = f"How many {item}s would you like?"
        self.text_to_speech_and_play(quantity_text)
        
        quantity = int(input())
        
        customization = ""
        extra_cost = 0.0
        
        if item == "Burger":
            toppings_text = "Choose toppings (lettuce, tomato, cheese, onions, pickles, bacon):"
            self.text_to_speech_and_play(toppings_text)
            toppings = input().split(',')
            for topping in toppings:
                extra_cost += self.toppings_prices.get(topping.strip().lower(), 0.0)
        elif item == "Soda":
            soda_type_text = "Choose type (Coke, Sprite, Dr Pepper, Orange Soda):"
            self.text_to_speech_and_play(soda_type_text)
            soda_type = input().lower()
            extra_cost = self.toppings_prices.get(soda_type, 0.0)
        elif item == "Ice Cream":
            flavor_text = "Choose flavor (vanilla, chocolate, swirl):"
            self.text_to_speech_and_play(flavor_text)
            flavor = input().lower()
            extra_cost = self.toppings_prices.get(flavor, 0.0)
        elif item == "Fries":
            fry_toppings_text = "Add toppings? (cheese, bacon):"
            self.text_to_speech_and_play(fry_toppings_text)
            fry_toppings = input().split(',')
            for topping in fry_toppings:
                extra_cost += self.toppings_prices.get(topping.strip().lower(), 0.0)

        order_update_text = "Order updated. What else would you like to add?"
        self.text_to_speech_and_play(order_update_text)

        order_key = f"{item} - {customization}" if customization else item
        quantity_in_order, existing_extra_cost = self.order.get(order_key, [0, 0.0])
        self.order[order_key] = (quantity_in_order + quantity, existing_extra_cost + extra_cost)

    def calculate_total(self):
        self.total_cost = sum((self.menu[item.split(' - ')[0]] + extra_cost) * quantity for item, (quantity, extra_cost) in self.order.items())
        text = f"Your total is ${self.total_cost:.2f}."
        self.text_to_speech_and_play(text)

    def display_receipt(self):
        text = "\nBurger Bliss Receipt:"
        for item, (quantity, extra_cost) in self.order.items():
            base_item = item.split(' - ')[0]
            text += f"\n{item} x{quantity}: ${self.menu[base_item] * quantity + extra_cost:.2f}"
        text += f"\n\nTotal: ${self.total_cost:.2f}\nPayment Processed. Thank you for dining at Burger Bliss!"
        self.text_to_speech_and_play(text)

    def run(self):
        self.display_menu()
        self.take_order()
        self.calculate_total()
        self.display_receipt()

if __name__ == "__main__":
    burger_bliss_cli = BurgerBlissCLI()
    burger_bliss_cli.run()