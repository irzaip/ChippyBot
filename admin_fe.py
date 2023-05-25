#ADMIN FRONT END
import gradio as gr
import cipi_iface as cp
from conversations import Persona, Script, ConvMode, ConvType


def get_conv_(user_filter: str):
    all_conv = cp.get_conversations()
    print(all_conv)
    all_conv = cp.json.loads(all_conv)
    all_conv = list(all_conv['message'])
    result = []
    for i in all_conv:
        if user_filter in i:
            result.append(i)
    return gr.Dropdown.update(choices=result)

conversations = {}

def get_user_number(user_number: str) -> str:
    return user_number.split('###')[0].strip()
    return result

def main():
    all_conv = []
    persona = [e.name for e in Persona]
    mode = [e.name for e in ConvMode]
    script = [e.name for e in Script]
    convtype = [e.name for e in ConvType]

    def toggle_maintenance_() -> None:
        cp.set_maintenance()

    def clean_(user_number: str):
        return user_number.split('###')[0].strip()

    def set_convtype_(user_number: str, convtype: ConvType):
        cp.set_convtype(clean_(user_number), convtype=convtype)

    def tambah_paid_messages_(user_number: str, unit: int):
        cp.tambah_paid_messages(clean_(user_number), unit)

    def tambah_free_tries_(user_number: str, unit: int):
        cp.tambah_free_tries(clean_(user_number), unit)

    def _conversation_info(user_number: str) -> list:
        un = user_number.split('###')[0].strip()
        response = cp.obj_info(un)
        #user_msg.value(result['message']['messages'][1]['content'])
        #assistant_msg.value(result['message']['messages'][2]['content'])
        result = cp.json.loads(response['message'])
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

    def reset_channel_(user_number: str) -> None:
        un = user_number.split('###')[0].strip()
        response = cp.reset_channel(un)
    
    with gr.Blocks() as admin:
        with gr.Row():
            contacts = gr.Dropdown(choices=all_conv, label="Contact Number / Group", interactive=True)
            refresh_contact = gr.Button(value="Refresh", interactive=True)
            refresh_contact.style(size='sm', full_width=False)

            retrieve_data = gr.Button(value="Retrieve Data")
            retrieve_data.style(size='sm', full_width=False)
            reset_ch = gr.Button(value="Reset MSG", interactive=True)
            reset_ch.style(size='sm', full_width=False)
        with gr.Row():
            user_filter = gr.Textbox(label="Filter", interactive=True)
            bot_name = gr.Textbox(label="Bot Name", interactive=True)
            user_name = gr.Textbox(label="User Name", interactive=True)
            set_bot_name = gr.Button(value="Set BotName")
            set_bot_name.style(size='sm', full_width=False)
            toggle_maintenance = gr.Button(value="Toggle Maintenance")
            toggle_maintenance.style(size='sm', full_width=False)
            toggle_maintenance.click(fn=toggle_maintenance_)

        with gr.Column():
            json_msg = gr.JSON(label="JSON OBJECT")

        with gr.Row():
            sys_msg = gr.Textbox( label='SYSTEM MESSAGE', interactive=True)
            sys_set = gr.Button(value="Set System", interactive=True)
            sys_set.style(size="sm", full_width=False)

        with gr.Row():
            user_msg = gr.Textbox(placeholder="user message", label='USER MESSAGE', interactive=True)
            user_set = gr.Button(value="Set User", interactive=True)
            user_set.style(size="sm", full_width=False)

        with gr.Row():
            assistant_msg = gr.Textbox(placeholder="assistant message", label='ASSISTANT MESSAGE', interactive=True)
            assistant_set = gr.Button(value="Set Assistant", interactive=True)
            assistant_set.style(size="sm", full_width=False)

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

        with gr.Row():
            convtype = gr.Dropdown(choices=convtype, label="Conv Type")
            st_convtype = gr.Button(value="Set conv Type")
            st_convtype.style(size='sm', full_width=False)

            unit = gr.Textbox(label="unit", interactive=True)
            st_free_tries = gr.Button(value="Set Free")
            st_free_tries.style(size='sm', full_width=False)
            st_paid_messages = gr.Button(value="Set Paid")
            st_paid_messages.style(size='sm', full_width=False)
            
        with gr.Column():
            intro_msg = gr.Textbox(label="Intro Message", interactive=True)
            outro_msg = gr.Textbox(label="Outro Message", interactive=True)
            in_out_msg = gr.Button(value="Set Intro and Outro")
        with gr.Column():
            questions = gr.Textbox(label="Questions", lines=7, interactive=True)
            set_questions = gr.Button(value="Set Questions")
        with gr.Column():
            he = gr.Textbox(label="hehe", interactive=True)
    
        #definisi klik
        refresh_contact.click(fn=get_conv_, inputs=user_filter, outputs=contacts)
        reset_ch.click(fn=reset_channel_, inputs=contacts)
        retrieve_data.click(fn=_conversation_info, inputs=contacts, outputs=[json_msg, sys_msg, user_msg,assistant_msg, interval, persona, mode, intro_msg, outro_msg, bot_name, user_name])
        st_convtype.click(fn=set_convtype_ , inputs=[contacts, convtype])
        st_free_tries.click(fn=tambah_free_tries_, inputs=[contacts,unit])
        st_paid_messages.click(fn=tambah_paid_messages_, inputs=[contacts,unit])

    admin.launch(server_port=9666, share=True)


if __name__ == '__main__':
    main()


