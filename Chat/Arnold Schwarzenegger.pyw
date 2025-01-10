from openai import OpenAI
import tkinter as tk
from tkinter import scrolledtext
from PIL import Image, ImageTk
import tempfile
import base64, zlib
import time

client = OpenAI()
system_msg = "short answers, act arrogant, curse words."
bg = "black"    #   color of background
fg = "red"      #   color of text
ibg = "white"   #   color of text cursor
ng = "yellow"   #   color of names
afg = fg        #   color of fg on hover
abg = bg        #   color of bg on hover

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
    
    chat_display.tag_configure("colored_text", foreground=ng)
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
    chat_display.tag_configure("colored_text", foreground=ng)
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
    

def log_chat(chat_display):
     millisecs = round(time.time() * 1000)
     with open(f"log/{millisecs}.txt", "w") as file:
        file.write(chat_display.get("1.0", tk.END))




root = tk.Tk()
root.title("Chat Window")
root.configure(background="black")
ICON = zlib.decompress(base64.b64decode('eJxjYGAEQgEBBiDJwZDBy'
    'sAgxsDAoAHEQCEGBQaIOAg4sDIgACMUj4JRMApGwQgF/ykEAFXxQRc='))
_, ICON_PATH = tempfile.mkstemp()
with open(ICON_PATH, 'wb') as icon_file:
    icon_file.write(ICON)
root.iconbitmap(default=ICON_PATH)

model = tk.StringVar(root)
options = ['o1-preview', 'o1-mini', 'gpt-4-0314']
model.set(options[0])
dropbox = tk.OptionMenu(root, model, *options)
dropbox.config(
    bg=bg, 
    fg=fg, 
    bd=0, 
    highlightthickness=0, 
    activebackground=abg, 
    activeforeground=afg)
dropbox.pack()

# Chat display area
chat_display = scrolledtext.ScrolledText(
    root, 
    wrap=tk.WORD, 
    width=100, 
    height=30, 
    bg=bg, 
    fg=fg, 
    insertbackground=ibg)
chat_display.vbar.pack_forget()
chat_display.pack(padx=10, pady=5)

# Bigger text input area
text_input = tk.Text(
    root, 
    width=100, 
    height=10, 
    bg=bg, 
    fg=fg, 
    insertbackground=ibg)
text_input.bind('<Control-Return>', lambda event: send_msg(chat_display, text_input, messages))
text_input.pack()

# Send button
send_button = tk.Button(
    root, 
    text="Send", 
    command=lambda:send_msg(chat_display, text_input, messages), 
    width=100, 
    bg=bg, 
    fg=fg)
send_button.pack()

reset_button = tk.Button(
    root, 
    text="Reset", 
    command=lambda:reset(chat_display, text_input), 
    width=100, 
    bg=bg, 
    fg=fg)
reset_button.pack()

log_button = tk.Button(
    root, 
    text="Log", 
    command=lambda:log_chat(chat_display), 
    width=100, 
    bg=bg, 
    fg=fg)
log_button.pack()

root.mainloop()




'''

# Example image message
image = Image.open("Untitled 1.png")
image = image.resize((100, 100))
photo = ImageTk.PhotoImage(image)
chat_display.image_create(tk.END, image=photo)
chat_display.insert(tk.END, "\n\n")

'''