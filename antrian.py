import asyncio

class TimedCoroutine:
    def __init__(self, interval):
        self.interval = interval
        self.loop = asyncio.get_event_loop()
        self.queue = asyncio.Queue()
        self.task = None

    async def execute_function(self, function, *args):
        await function(*args)

    async def process_queue(self):
        while True:
            item = await self.queue.get()
            function, *args = item
            await self.execute_function(function, *args)
            self.queue.task_done()

    async def print_hello(self):
        while True:
            await self.queue.put((self.say_hello, 'World'))  # Menambahkan fungsi say_hello ke dalam antrian dengan argumen 'World'
            await asyncio.sleep(self.interval)

    def say_hello(self, name):
        print(f'Hello, {name}!')

    def start(self):
        self.task = self.loop.create_task(self.print_hello())
        self.loop.create_task(self.process_queue())

    def stop(self):
        self.task.cancel()

# Penggunaan contoh:
tc = TimedCoroutine(10)
tc.start()

try:
    tc.loop.run_forever()
except KeyboardInterrupt:
    tc.stop()
    tc.loop.close()