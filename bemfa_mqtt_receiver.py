# bemfa_mqtt_receiver.py
import paho.mqtt.client as mqtt
import time

# 导入关机和唤醒模块
from shutdown import Shutdown
from wol import Wake

class BemfaMQTTReceiver:
    
    def __init__(self, uid: str, topic: str, target_ip: str, target_user: str, target_passwd: str, target_mac: str):
        self.uid = uid
        self.topic = topic
        self.target_ip = target_ip
        self.target_user = target_user
        self.target_passwd = target_passwd
        self.target_mac = target_mac
        
        self.broker = "bemfa.com"
        self.port = 9501
        self.connected = False
        
        # 创建MQTT客户端
        self.client = mqtt.Client(client_id=uid)
        
        # 绑定回调函数
        self.client.on_connect = self._on_connect
        self.client.on_message = self._on_message
        self.client.on_disconnect = self._on_disconnect

    def _on_connect(self, client, userdata, flags, rc: int) -> None:
        if rc == 0:
            self.connected = True
            print(f"已连接到巴法云服务器，订阅主题: {self.topic}")
            self.client.subscribe(self.topic)
            print("等待指令... (支持的指令: off, on)")
        else:
            self.connected = False
            print(f"连接失败，错误代码: {rc}")

    def _on_message(self, client, userdata, msg) -> None:
        command = msg.payload.decode('utf-8').strip().lower()
        print(f"收到指令: {command}")
        
        if command == "off":
            self._handle_shutdown()
        elif command == "on":
            self._handle_wake()
        else:
            print(f"未知指令: {command}")

    def _on_disconnect(self, client, userdata, rc: int) -> None:
        self.connected = False
        if rc != 0:
            print(f"意外断开连接 (错误码: {rc})")

    def _handle_shutdown(self) -> None:
        print(f"执行关机操作 (IP: {self.target_ip})")
        try:
            shutdown = Shutdown(self.target_ip, self.target_user, self.target_passwd)
            shutdown.shutdown()
            print("关机指令已发送")
        except Exception as e:
            print(f"关机失败: {str(e)}")

    def _handle_wake(self) -> None:
        print(f"执行唤醒操作 (IP: {self.target_ip}, MAC: {self.target_mac})")
        try:
            wake = Wake(self.target_mac)
            wake.wake_on_lan()
            print("唤醒指令已发送")
        except Exception as e:
            print(f"唤醒失败: {str(e)}")

    def start(self, timeout: int = 5) -> bool:
        try:
            self.client.connect(self.broker, self.port, keepalive=60)
            self.client.loop_start()
            
            # 等待连接成功
            start_time = time.time()
            while not self.connected and (time.time() - start_time) < timeout:
                time.sleep(0.5)
                
            return self.connected
        except Exception as e:
            print(f"启动失败: {str(e)}")
            return False

    def stop(self) -> None:
        if self.connected:
            self.client.loop_stop()
            self.client.disconnect()
        self.connected = False