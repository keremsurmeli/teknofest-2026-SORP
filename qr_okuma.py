import cv2
from pyzbar.pyzbar import decode
import time

class ForkliftNavigator:
    def __init__(self):
        self.current_state = "IDLE"  
        self.target_gate = None
        self.last_read_qr = None
        self.last_read_time = 0

    def process_qr_data(self, qr_text):
        current_time = time.time()
      
        if qr_text == self.last_read_qr and (current_time - self.last_read_time) < 3:
            return

        print(f"\n[YENİ QR TESPİT EDİLDİ]: {qr_text}")
        self.last_read_qr = qr_text
        self.last_read_time = current_time

        if "KAPI_" in qr_text:
            self.target_gate = qr_text.split("_")[1]
            self.current_state = "NAVIGATING"
            self.execute_navigation()
            
        elif qr_text == "DUR":
            print("Forklift acil duruş moduna geçiyor.")
            self.current_state = "IDLE"
            self.target_gate = None

    def execute_navigation(self):
        if self.current_state == "NAVIGATING":
            print(f"[ROTA]: Hedef Kapı {self.target_gate} olarak belirlendi.")
            print(f"[HAREKET]: Kapı {self.target_gate} yönüne doğru sürüş başlatıldı...")
            
            self.current_state = "ARRIVED" 

def main():
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    navigator = ForkliftNavigator()
    print("Forklift QR Navigasyon Sistemi Başlatıldı. Kamera Açılıyor...")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Kameradan görüntü alınamıyor!")
            break

        detected_qrs = decode(frame)
        
        for qr in detected_qrs:
            qr_data = qr.data.decode('utf-8')
            
            points = qr.polygon
            if len(points) == 4:
                pts = [(p.x, p.y) for p in points]
                for i in range(4):
                    cv2.line(frame, pts[i], pts[(i+1)%4], (0, 255, 0), 3)
            
            navigator.process_qr_data(qr_data)


        # 'q' tuşuna basılırsa döngüden çık
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    print("Sistem kapatıldı.")

