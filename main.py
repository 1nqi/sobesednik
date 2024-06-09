from elevenlabs import Voice, VoiceSettings, play
from elevenlabs.client import ElevenLabs
from openai import OpenAI

import speech_recognition as sr
client = ElevenLabs(
#   api_key="995f600b1fdc40b04dc1272a9ea0d4aa",
  api_key="sk_35a766d902e5d77bcca04e08ef857dea24f6b54158f092ae"
)
recognitor1 = sr.Recognizer()
client1 = OpenAI(
    api_key='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'
)

system_message = {"role": "system", "content": "Ты голосовой ассистент Джарвис из железного человека. Отзывайся на имя Джарвис и прибавляй в конце обращения СЭР если это уместно. Старайся отвечать очень кратко."}
message_log = [system_message]

def gpt():
    global message_log
    global client1
    response = client1.chat.completions.create(
            model="gpt-4o",
            messages=message_log,
        )
    return response.choices[0].message.content

def recognition():
    while True:
        with sr.Microphone() as source:
            print("Я слушаю...")
            audio1 = recognitor1.listen(source)
            print("Recognition..")
            try:
                searching = recognitor1.recognize_google(audio1, language='ru-RU')
                if not searching:
                    print("Пустой результат, продолжаем слушать...")
                    continue
            except sr.UnknownValueError:
                print("Google Speech Recognition не смог распознать аудио, продолжаем слушать...")
                continue
            except sr.RequestError as e:
                print(f"Ошибка запроса к Google Speech Recognition сервису; {e}")
                continue
        return searching

def huy(searching):
                message_log.append({"role": "user", "content": searching})
                print(searching)
                response = gpt()
                message_log.append({"role": "assistant", "content": response})
                audio = client.generate(
                text=f"{response}",
                voice=Voice(
                    voice_id='EXAVITQu4vr4xnSDxMaL',
                settings=VoiceSettings(stability=0.71, similarity_boost=0.5, style=0.0, use_speaker_boost=True)),
                model="eleven_multilingual_v2")
                print(response)
                play(audio)
while True: 
    huy(recognition())
