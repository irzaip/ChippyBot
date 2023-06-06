import requests

def main():
    # Mengatur URL server streaming
    url = 'https://stream.trakteer.id/notification/?key=trstream-8bbqIqVmoIFhy8Rv2bvD&unit=Cendol&mod=3&hash=wmkv57yrjy05blag'  # ganti dengan URL yang sesuai
    
    try:
        # Mengirim permintaan GET ke URL
        response = requests.get(url, stream=True)
        
        # Memeriksa status respons
        if response.status_code == 200:
            # Mengakses aliran respons
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    # Menampilkan data di console
                    print(chunk.decode())
        else:
            print("Permintaan tidak berhasil. Kode status:", response.status_code)
    
    except requests.exceptions.RequestException as e:
        print("Terjadi kesalahan saat melakukan permintaan:", str(e))

if __name__ == '__main__':
    main()