#ADMIN FRONT END
import gradio as gr
from cipi_iface import *
from conversations import Persona, Script, ConvMode


def get_conv_():
    all_conv = get_conversations()
    print(all_conv)
    all_conv = json.loads(all_conv)
    all_conv = list(all_conv['message'])
    return gr.Dropdown.update(choices=all_conv)

conversations = {}

def get_user_number(user_number: str) -> str:
    return user_number.split('###')[0].strip()


    return result

def main():
    all_conv = []
    persona = [e.name for e in Persona]
    mode = [e.name for e in ConvMode]
    script = [e.name for e in Script]

    def _conversation_info(user_number: str) -> list:
        un = user_number.split('###')[0].strip()
        response = obj_info(un)
        #user_msg.value(result['message']['messages'][1]['content'])
        #assistant_msg.value(result['message']['messages'][2]['content'])
        result = json.loads(response['message'])
        #return 
        return [
            result,
            result['messages'][0],
            result['messages'][1],
            result['messages'][2],
            result['interval'],
            Persona(result['persona']).name,
            ConvMode(result['mode']).name,
            #Script(result['script']).name,
            result['intro_msg'],
            result['outro_msg'],
            result['bot_name'],
            result['user_name']
        ]

    with gr.Blocks() as admin:
        with gr.Row():
            contacts = gr.Dropdown(choices=all_conv, label="Contact Number / Group", interactive=True)
            refresh_contact = gr.Button(value="Refresh", interactive=True)
            refresh_contact.style(size='sm', full_width=False)
            refresh_contact.click(fn=get_conv_, outputs=contacts)

            retrieve_data = gr.Button(value="Retrieve Data")
            retrieve_data.style(size='sm', full_width=False)

        with gr.Row():
            bot_name = gr.Textbox(label="Bot Name", interactive=True)
            user_name = gr.Textbox(label="User Name", interactive=True)
            set_bot_name = gr.Button(value="Set BotName")
            set_bot_name.style(size='sm', full_width=False)
        with gr.Column():
            json_msg = gr.JSON(label="JSON OBJECT")
            sys_msg = gr.Textbox( label='SYSTEM MESSAGE', interactive=True)
            user_msg = gr.Textbox(placeholder="user message", label='USER MESSAGE', interactive=True)
            assistant_msg = gr.Textbox(placeholder="assistant message", label='ASSISTANT MESSAGE', interactive=True)
        with gr.Row():
            persona = gr.Dropdown(choices=persona, label="Persona", interactive=True, allow_custom_value=True)
            set_persona = gr.Button(value="Set")
            set_persona.style(size='sm', full_width=False)

            mode = gr.Dropdown(choices=mode, label="Mode", interactive=True, allow_custom_value=True)
            set_mode = gr.Button(value="Set")
            set_mode.style(size='sm', full_width=False)
        with gr.Row():
            script = gr.Dropdown(choices=script, label="Script")
            set_script = gr.Button(value="Set")
            set_script.style(size='sm', full_width=False)

            interval = gr.Textbox(label="Timed Interval", interactive=True)
            set_interval = gr.Button(value="Set Interval")
            set_interval.style(size='sm', full_width=False)

        with gr.Column():
            intro_msg = gr.Textbox(label="Intro Message", interactive=True)
            outro_msg = gr.Textbox(label="Outro Message", interactive=True)
            in_out_msg = gr.Button(value="Set Intro and Outro")
        with gr.Column():
            questions = gr.Textbox(label="Questions", lines=7, interactive=True)
            set_questions = gr.Button(value="Set Questions")
        with gr.Column():
            he = gr.Textbox(label="hehe", interactive=True)
    
        retrieve_data.click(fn=_conversation_info, inputs=contacts, outputs=[json_msg, sys_msg, user_msg,assistant_msg, interval, persona, mode, intro_msg, outro_msg, bot_name, user_name])
        


    admin.launch(server_port=9666, share=True)


if __name__ == '__main__':
    main()


