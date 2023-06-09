from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
import os
from google.cloud import texttospeech
import pygame  # Import the pygame library
import glob

class MyApp(App):
    def build(self):
        self.text_input = TextInput()  # Create a TextInput instance
        self.button = Button(text='Print input')
        self.button.bind(on_press=self.print_input)  # Bind button press event to a method

        layout = BoxLayout(orientation='vertical')
        layout.add_widget(self.text_input)
        layout.add_widget(self.button)

        return layout

    def print_input(self, instance):
        print(self.text_input.text)  # Print text input content to console
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'credenials.json'

        # Instantiates a client
        client = texttospeech.TextToSpeechClient()

        text = '<speak>' + "" + self.text_input.text + "" + '</speak>'

        # Set the text input to be synthesized
        synthesis_input = texttospeech.SynthesisInput(ssml=text)

        # Build the voice request, select the language code ("en-US") and the ssml
        # voice gender ("neutral")
        voice = texttospeech.VoiceSelectionParams(
            language_code='en-US',
            ssml_gender=texttospeech.SsmlVoiceGender.FEMALE,
        )

        # Select the type of audio file you want returned
        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3,
        )

        # Perform the text-to-speech request on the text input with the selected
        # voice parameters and audio file type
        response = client.synthesize_speech(
            input=synthesis_input, voice=voice, audio_config=audio_config,
        )

        # Initialize pygame
        pygame.mixer.init()

        # Load a dummy audio file to unlock previous one
        pygame.mixer.music.load('dummy.mp3')  # a small silent mp3 file

        # Delete all previous audio files
        files = glob.glob('audio*.mp3')
        for f in files:
            try:
                os.remove(f)
            except OSError as e:
                print("Error: %s - %s." % (e.filename, e.strerror))

        # Save the synthesized audio to a file.
        filename = 'audio' + str(pygame.time.get_ticks()) + '.mp3'
        with open(filename, 'wb') as out:
            out.write(response.audio_content)

        # Load and play the audio file
        pygame.mixer.music.load(filename)
        pygame.mixer.music.play()

MyApp().run()
