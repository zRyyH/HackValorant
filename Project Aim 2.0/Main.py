from Hack import DetectPlayer
import asyncio
import websockets
import serial

server_serial = serial.Serial('COM15', 128000, timeout=0)

# Variaveis compartilhada
y = 0
x = 0
scroll = 0
l = 0
r = 0
scroll_click = 0


# Lock para garantir acesso seguro à variável compartilhada
lock = asyncio.Lock()


async def serial_emit():
    data = "{},{},{},{},{},{}".format(y, x, scroll, l, r, scroll_click)
    server_serial.write(data.encode())
    
    
async def mouse_inject(msg):
    global y, x, scroll, l, r, scroll_click
    
    data = list(map(int, msg.split(',')))
    
    if data[3:] != [l, r, scroll_click] or data[0] != 0 or data[1] != 0 or data[2] != 0:
        async with lock:
            y, x, scroll, l, r, scroll_click = data
            await serial_emit()
            
            
def move(number):
    x, y = DetectPlayer()
    return [y, x]


async def cheat_inject():
    global y, x, r
    loop = asyncio.get_event_loop()
    
    while True:
        pos_x, pos_y = await loop.run_in_executor(None, move, 1)
        if r:
            async with lock:
                x, y = pos_x, pos_y
                await serial_emit()
                
                
async def server(websocket):
    asyncio.create_task(cheat_inject())
    async for msg in websocket:
        await mouse_inject(msg)
        
        
start_server = websockets.serve(server, "192.168.3.220", 9999, ping_timeout=None)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()