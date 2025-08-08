import socket

class Wake:
    def __init__(self, target_ip:str, mac_address:str):
        self.target_ip = target_ip
        self.mac_address = mac_address


    def wake_on_lan(self, port=9):
        mac = self.mac_address.replace(":", "").replace("-", "")
        if len(mac) != 12:
            raise ValueError("无效的MAC地址格式，请使用AA:BB:CC:DD:EE:FF格式")
        
        try:
            mac_bytes = bytes.fromhex(mac)
            magic_packet = b'\xff' * 6 + mac_bytes * 16
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            sock.sendto(magic_packet, (self.target_ip, port))
            
            print(f"已发送WOL魔术包到 {self.target_ip}:{port} (MAC: {self.mac_address})")
            
        except Exception as e:
            print(f"发送魔术包失败: {str(e)}")
        finally:
            if 'sock' in locals():
                sock.close()