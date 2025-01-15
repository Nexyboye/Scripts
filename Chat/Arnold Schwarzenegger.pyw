from openai import OpenAI
import tkinter as tk
from tkinter import scrolledtext
from PIL import Image, ImageTk
import tempfile
import base64, zlib
import time
client = OpenAI()


bg = "black"    #   color of background
fg = "red"      #   color of text
ibg = "white"   #   color of text cursor
ng = "yellow"   #   color of names
afg = fg        #   color of fg on hover
abg = bg        #   color of bg on hover
window_w = 600
window_h = 900



def send_msg(chat_display, text_input):
    global messages
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
    
def reset(chat_display, text_input, persona):
    global messages
    p = persona.get()
    if p == "rude":
        system_msg = "short answers, act arrogant, curse words."
    elif p == "code":
        system_msg = "short answers, code only." 
    
    messages = [
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


#---------------------------------------------------------------------------------------------------------------- shitty frontend

root = tk.Tk()
root.title("Chat Window")
root.configure(background="black")
root.geometry(f"{window_w}x{window_h}")
ICON = zlib.decompress(base64.b64decode('eJxjYGAEQgEBBiDJwZDBy'
    'sAgxsDAoAHEQCEGBQaIOAg4sDIgACMUj4JRMApGwQgF/ykEAFXxQRc='))
_, ICON_PATH = tempfile.mkstemp()
with open(ICON_PATH, 'wb') as icon_file:
    icon_file.write(ICON)
root.iconbitmap(default=ICON_PATH)
#root.bind("<Configure>", on_resize) ############################# IMPLEMENT THE FUNCTION


top_frame = tk.Frame(root)
top_frame.pack()



model = tk.StringVar(root)
model_options = ['o1-preview', 'o1-mini', 'gpt-4-0314']
model.set(model_options[0])
model_dropbox = tk.OptionMenu(top_frame, model, *model_options)
model_dropbox.config(
    bg=bg, 
    fg=fg, 
    bd=0, 
    highlightthickness=0, 
    activebackground=abg, 
    activeforeground=afg)
model_dropbox.pack(side='left')

persona = tk.StringVar(root)
persona_options = ['rude', 'code']
persona.set(persona_options[0])
persona_dropbox = tk.OptionMenu(top_frame, persona, *persona_options)
persona_dropbox.config(
    bg=bg, 
    fg=fg, 
    bd=0, 
    highlightthickness=0, 
    activebackground=abg, 
    activeforeground=afg)
persona_dropbox.pack(side='left')

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
text_input.bind('<Control-Return>', lambda event: send_msg(chat_display, text_input))
text_input.pack()
text_input.focus_set()


bot_frame = tk.Frame(root)
bot_frame.pack()

# Send button
send_button = tk.Button(
    bot_frame, 
    text="Send", 
    command=lambda:send_msg(chat_display, text_input), 
    width=30, 
    bg=bg, 
    fg=fg)
send_button.pack(side='left')

reset_button = tk.Button(
    bot_frame, 
    text="Reset", 
    command=lambda:reset(chat_display=chat_display, text_input=text_input, persona=persona), 
    width=30, 
    bg=bg, 
    fg=fg)
reset_button.pack(side='left')

log_button = tk.Button(
    bot_frame, 
    text="Log", 
    command=lambda:log_chat(chat_display), 
    width=30, 
    bg=bg, 
    fg=fg)
log_button.pack(side='left')

#----------------------------------------------------------------------------------------------------------------

messages = None
reset(chat_display, text_input, persona)



root.mainloop()




'''

# Example image message
image = Image.open("Untitled 1.png")
image = image.resize((100, 100))
photo = ImageTk.PhotoImage(image)
chat_display.image_create(tk.END, image=photo)
chat_display.insert(tk.END, "\n\n")




'''
