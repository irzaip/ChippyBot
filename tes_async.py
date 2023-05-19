import asyncio

async def do_something(item):
    # Melakukan tugas yang diinginkan dengan item
    print(f"Melakukan tugas dengan item: {item}")
    await asyncio.sleep(10)  # Contoh tugas yang memakan waktu

async def process_queue(queue):
    while True:
        item = await queue.get()  # Mengambil item dari antrian
        await do_something(item)  # Melakukan tugas dengan item
        queue.task_done()  # Menandai bahwa item telah selesai diproses
        

async def main():
    queue = asyncio.Queue()
    
    # Menambahkan item ke antrian
    for i in range(5):
        await queue.put(i)

    # Membuat beberapa coroutine untuk memproses antrian
    tasks = []
    for _ in range(1):
        task = asyncio.create_task(process_queue(queue))
        tasks.append(task)

    # Menunggu semua item dalam antrian selesai diproses
    await queue.join()

    # Membatalkan semua coroutine
    for task in tasks:
        task.cancel()

asyncio.run(main())