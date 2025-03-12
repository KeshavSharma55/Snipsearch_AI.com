from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
import sqlite3
import math

# Database Setup
conn = sqlite3.connect("snipsearch_ai.db")
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS knowledge (
    question TEXT PRIMARY KEY, 
    answer TEXT
)
""")
conn.commit()

class SnipsearchAI(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', **kwargs)

        self.chat_display = Label(text="Welcome to Snipsearch AI - Index Model", size_hint_y=0.6)
        self.add_widget(self.chat_display)

        self.user_input = TextInput(hint_text="Ask a question...", size_hint_y=0.1, multiline=False)
        self.add_widget(self.user_input)

        self.answer_input = TextInput(hint_text="Enter answer (only when training AI)", size_hint_y=0.1, multiline=False)
        self.add_widget(self.answer_input)

        button_layout = BoxLayout(size_hint_y=0.2)
        
        self.ask_button = Button(text="Ask", on_press=self.process_input)
        button_layout.add_widget(self.ask_button)

        self.train_button = Button(text="Train AI", on_press=self.train_ai)
        button_layout.add_widget(self.train_button)

        self.add_widget(button_layout)

    def process_input(self, instance):
        user_question = self.user_input.text.lower().strip()
        
        if not user_question:
            return
        
        # Check in database
        cursor.execute("SELECT answer FROM knowledge WHERE question = ?", (user_question,))
        result = cursor.fetchone()
        
        if result:
            response = result[0]
        else:
            try:
                response = str(eval(user_question))  # Math calculation
            except:
                response = "I don't know. You can teach me!"

        self.chat_display.text = f"User: {user_question}\nAI: {response}"
        self.user_input.text = ""

    def train_ai(self, instance):
        question = self.user_input.text.lower().strip()
        answer = self.answer_input.text.strip()

        if question and answer:
            cursor.execute("INSERT OR REPLACE INTO knowledge (question, answer) VALUES (?, ?)", (question, answer))
            conn.commit()
            self.chat_display.text = "AI learned a new answer!"
            self.user_input.text = ""
            self.answer_input.text = ""
        else:
            self.chat_display.text = "Enter both question and answer to train AI."

class SnipsearchApp(App):
    def build(self):
        return SnipsearchAI()

if __name__ == "__main__":
    SnipsearchApp().run()