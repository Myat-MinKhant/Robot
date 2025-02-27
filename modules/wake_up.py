# def wake_word():
#     global streaming
#     global listener

#     while True:
#         try:
#             with sr.Microphone(device_index=1) as source:
#                 print('sleep mode...')
#                 listener.adjust_for_ambient_noise(source)
#                 wake = listener.listen(source)
#                 command = listener.recognize_google(wake)

#                 if 'computer' in command:
#                     run_ai()

#         except sr.UnknownValueError:
#             continue