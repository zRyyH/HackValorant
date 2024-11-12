from evdev import list_devices, InputDevice, ecodes

import asyncio
import websockets

MouseName = "SINOWEALTHDC Wired Gaming Mouse"

async def client():
    async with websockets.connect("ws://192.168.3.220:9999") as websocket:
        
        # ENVIAR COMANDO
        async def emit(rel_y, rel_x, rel_scroll, button_left, button_right, button_scroll):
            data = "{},{},{},{},{},{}".format(rel_y, rel_x, rel_scroll, button_left, button_right, button_scroll)
            await websocket.send(data)
            
        # OBTER MOVIMENTOS DO MOUSE
        async def MouseCapture(mouse):
            mouse.grab()
            
            rel_x = 0
            rel_y = 0
            rel_scroll = 0
            
            button_left = 0
            button_right = 0
            button_scroll = 0
            
            try:
                for event in mouse.read_loop():
                    if event.code == 0 and event.type == 2:
                        rel_y = event.value
                        
                    if event.code == 1 and event.type == 2:
                        rel_x = event.value
                    
                    if event.code == 8 and event.type == 2:
                        rel_scroll = event.value
                        
                    if event.code == 272 and event.type == 1:
                        button_left = event.value

                    if event.code == 273 and event.type == 1:
                        button_right = event.value
                        
                    if event.code == 274 and event.type == 1:
                        button_scroll = event.value
                        
                    if event.type == 0:
                        await emit(rel_y, rel_x, rel_scroll, button_left, button_right, button_scroll)
                        
                        rel_x = 0
                        rel_y = 0
                        rel_scroll = 0
                        
            except KeyboardInterrupt:
                mouse.ungrab()
                print("Captura Encerrada...")
                
        # PROCURANDO MOUSE
        async def list_input_devices():
            devices = [InputDevice(device) for device in list_devices()]
            
            for device in devices:
                print(device.name)
                if device.name == MouseName:
                    await MouseCapture(device)
                    
        await list_input_devices()
        
if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(client())
