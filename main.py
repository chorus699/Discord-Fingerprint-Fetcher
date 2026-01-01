import tls_client
import threading
import queue

def get_fingerprint():
    proxy_url = "http://"
    
    session = tls_client.Session(
        client_identifier="chrome_124",
        random_tls_extension_order=True
    )
    
    session.proxies = {
        "http": proxy_url,
        "https": proxy_url
    }
    
    try:
        response = session.get("https://discord.com/api/v9/experiments")
        
        if response.status_code == 200:
            data = response.json()
            fingerprint = data.get('fingerprint')
            if fingerprint:
                return fingerprint
        return None
        
    except:
        return None

def worker(fingerprint_queue, worker_id):
    while True:
        fingerprint = get_fingerprint()
        
        if fingerprint:
            fingerprint_queue.put(fingerprint)
            print(f"[Worker-{worker_id}] Got fingerprint")
        else:
            print(f"[Worker-{worker_id}] Failed")

def saver_thread(fingerprint_queue):
    while True:
        fingerprint = fingerprint_queue.get()
        if fingerprint:
            with open("fingerprint.txt", "a") as f:
                f.write(fingerprint + "\n")
            print(f"[Saver] Saved fingerprint")

def main():
    fingerprint_queue = queue.Queue()
    
    saver = threading.Thread(target=saver_thread, args=(fingerprint_queue,), daemon=True)
    saver.start()
    
    num_workers = 100
    
    for i in range(num_workers):
        worker_thread = threading.Thread(
            target=worker,
            args=(fingerprint_queue, i+1),
            daemon=True
        )
        worker_thread.start()

    while True:
        pass

if __name__ == "__main__":
    main()
