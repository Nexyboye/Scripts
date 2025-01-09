from openai import OpenAI
import tkinter as tk
from tkinter import scrolledtext
from PIL import Image, ImageTk

client = OpenAI()
system_msg = "short answers, act arrogant, curse words."

messages=[
            {
              "role": "user",
              "content": [
                {
                  "type": "text",
                  "text": system_msg
                }
              ]
            }
         ]

def send_msg(chat_display, text_input, messages):
    
    message = text_input.get("1.0", tk.END)
    text_input.delete("1.0", "end")
    
    chat_display.tag_configure("colored_text", foreground="red")
    chat_display.insert(tk.END, "Nex\n", "colored_text")
    chat_display.insert(tk.END, f"{message}\n")
    
    messages.append(
        {
          "role": "user",
          "content": [
            {
              "type": "text",
              "text": message
            }
          ]
        }
    )
    
    response = client.chat.completions.create(
                              model=model.get(),
                              messages=messages)
    chat_display.tag_configure("colored_text", foreground="red")
    chat_display.insert(tk.END, "Arnold Schwarzenegger\n", "colored_text")        
    chat_display.insert(tk.END, f"{response.choices[0].message.content}\n\n")                          
    
    messages.append(
        {
          "role": "assistant",
          "content": [
            {
              "type": "text",
              "text": response.choices[0].message.content
            }
          ]
        }
    )
    
    return 'break'
    
def reset(chat_display, text_input):
    global messages
    messages=[
            {
              "role": "user",
              "content": [
                {
                  "type": "text",
                  "text": system_msg
                }
              ]
            }
         ]
    chat_display.delete('1.0', tk.END)
    text_input.delete("1.0", "end")

root = tk.Tk()
root.title("Chat Window")

model = tk.StringVar(root)
options = ['o1-preview', 'o1-mini', 'gpt-4-0314']
model.set(options[2])
dropbox = tk.OptionMenu(root, model, *options)
dropbox.pack()

# Chat display area
chat_display = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=100, height=30)
chat_display.pack(padx=10, pady=5)

# Bigger text input area
text_input = tk.Text(root, width=100, height=10)
text_input.bind('<Control-Return>', lambda event: send_msg(chat_display, text_input, messages))
text_input.pack()

# Send button
send_button = tk.Button(root, text="Send", command=lambda:send_msg(chat_display, text_input, messages), width=100)
send_button.pack()

reset_button = tk.Button(root, text="Reset", command=lambda:reset(chat_display, text_input), width=100)
reset_button.pack()

root.mainloop()




'''

# Example image message
image = Image.open("Untitled 1.png")
image = image.resize((100, 100))
photo = ImageTk.PhotoImage(image)
chat_display.image_create(tk.END, image=photo)
chat_display.insert(tk.END, "\n\n")

'''
