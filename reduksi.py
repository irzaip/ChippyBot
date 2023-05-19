## reduksi.py
def count_words(input: str) -> int:
    result = input.split(" ")
    return len(result)

def hitung_total_kata(input: list):
    total = 0
    for i in input:
        hasil = count_words(i['content'])
        #print(f"{i['role']} ada {hasil} kata")
        total += hasil
    print(f"total : {total}")
    return (len(input), total)
    
def trim_msg(messages: list)-> list:
    length, total = hitung_total_kata(messages)
    if total > 800:
        #if length % 2 != 0:
        sys_prom = messages[:3]
        trim_at = int(3+(length/2))
        sys_prom.extend(messages[trim_at:])
        print(f"menjalankan reduksi karena kata sudah: {total}")
        return sys_prom
    return messages

