import gradio as gr
import openai
import datetime
import os
import yaml

openai.api_key = os.environ["OPENAI_API_KEY"]

messages = [
    {"role" : "system" , "content" : "You are a kind grumpy annoying assistant"}
]


with open('outputs.yaml') as f:
    dropdown = yaml.safe_load(f)

with open('instruction.yaml') as f:
    instruction_option = yaml.safe_load(f)


instruction = []



dd_list = list(map(lambda x: x, dropdown.keys()))

def reset_messages():
   global messages
   messages = [
    {"role" : "system" , "content" : "You are a kind grumpy annoying assistant"}
  ]

def ask_gpt(prompt):
    global messages
    messages.append(
        {"role" : "user", "content" : prompt}
    )
    response = openai.ChatCompletion.create(
      model="gpt-3.5-turbo",
      messages=messages,
#      max_tokens=1024,
#      n=1,
#      stop=None,
#      temperature=0.7,
    )

    message = response.choices[0].message.content
    messages.append({"role" : "assistant", "content" : message})
    return message

def convert_dropdown(input):
  result = ""
  for i in input:
    result = result + dropdown[i]
  return result

def update_inst_dd(inputs):
  global instruction
  try:
    instruction = list(instruction_option[inputs].keys())
  except:
     instruction = []
  print("instruction:" , instruction)
  return gr.Dropdown.update(choices=instruction)
   
def update_instruction(inputs, prompt):
  try:
    instruction = instruction_option[inputs][prompt]
  except:
     instruction = []
  return instruction
   

def chatbot(input, output_format, contxt):
    question = input + ", " + convert_dropdown(output_format) + ", " + contxt
    print("QUESTION:", question)
    return ask_gpt(question)

def save_history():
   write_to_file(messages)
   return messages
   
def copy_clipbrd(input):
   return input

def clear_clipboard():
   return None

def copy_context(input):
   return input

def write_to_file(mylist) :
  now = datetime.datetime.now()
  filename = now.strftime("%Y-%m-%d-%H%M") + ".txt"

  with open(filename, "w") as f:
    for n in messages:
      f.write("\n\n\n")
      f.write("Role:" + n['role'])
      f.write("\n")
      f.write(n['content'])
      f.write("\n")


if __name__ == '__main__':
   
  with gr.Blocks() as iface:
      gr.Markdown("Tanya Jawab dengan CIPI-GPT")
      with gr.Row():
          with gr.Column():
            with gr.Row():
              instr_opt = gr.Dropdown(list(instruction_option.keys()), show_label=False)
              instr = gr.Dropdown(instruction, show_label=False, interactive=True)
            inp = gr.Textbox(lines=3,label="Instruksi / pertanyaan", placeholder="Ketik disini")
            out_type = gr.Dropdown(dd_list, multiselect=True, label="Output format")
            contx = gr.Textbox(lines=4, label="Context")
            btn_run = gr.Button("Run")
          with gr.Column():
            with gr.Row():
              btn_save = gr.Button("Save Hist")
              btn_reset = gr.Button("Reset")             
            out = gr.Textbox(label="Jawaban")
            with gr.Row():
              with gr.Column():
                  with gr.Row():
                    btn_clip = gr.Button("Copy to CLPBRD")
                    btn_clearclip = gr.Button("Clear CLPBRD")
                    btn_context = gr.Button("Use CLPBRD to Cntext")
                  clipbrd = gr.Textbox(lines=7, label="Clipboard")
              with gr.Column():
                  with gr.Row():
                    btn_clip2 = gr.Button("Copy to CLPBRD")
                    btn_clearclip2 = gr.Button("Clear CLPBRD")
                    btn_context2 = gr.Button("Use CLPBRD to Cntext")
                  clipbrd2 = gr.Textbox(lines=7, label="Clipboard")


      instr_opt.change(fn=update_inst_dd , inputs=instr_opt, outputs=instr)
      #instr.update(interactive=True)
      instr.change(fn=update_instruction, inputs=[instr_opt,instr], outputs=inp)
      btn_reset.click(fn=reset_messages)
      btn_reset.style(size='sm', full_width=False)
      btn_run.click(fn=chatbot, inputs=[inp, out_type, contx], outputs=out)
      btn_save.click(fn=save_history, outputs=out)
      btn_save.style(size='sm', full_width=False)
      btn_clip.click(fn=copy_clipbrd, inputs=out, outputs=clipbrd)
      btn_clip.style(size='sm', full_width=False)
      btn_clearclip.click(fn=clear_clipboard, outputs=clipbrd)
      btn_clearclip.style(size='sm', full_width=False)
      btn_context.click(fn=copy_context, inputs=clipbrd, outputs=contx)
      btn_context.style(size='sm', full_width=False)

  iface.launch(share=True, server_port=9999)




  #iface = gr.Interface(fn=chatbot, 
  #                     inputs=gr.inputs.Textbox(lines=7, label="Masukan perintah / pertanyaan"), 
  #                     outputs=gr.outputs.Textbox(label="Jawaban CIPI"), 
  #                     title="CIPI-GPT", 
  #                     description="Ngobrol interaktif bersama CIPI-GPT")
  #iface.launch(share=True)