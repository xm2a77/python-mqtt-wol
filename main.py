from bemfa_mqtt_receiver import BemfaMQTTReceiver
import time
import os

# 配置参数
ip = os.getenv("IP")  # 目标设备的ip地址
user = os.getenv("USER")   # 目标设备的管理员用户名
passwd = os.getenv("PASSWORD") # 目标设备的管理员密码
mac = os.getenv("MAC")  # 目标设备的MAC地址
bemfa_uid = os.getenv("BEMFA_PRIVATE_KEY")  # 巴法云的私钥
bemfa_topic = os.getenv("TOPIC")   # 巴法云的MQTT目标设备的主题

#ip = ""  # 目标设备的ip地址
#user = ""   # 目标设备的管理员用户名
#passwd = "" # 目标设备的管理员密码
#mac = ""  # 目标设备的MAC地址
#bemfa_uid = ""  # 巴法云的私钥
#bemfa_topic = ""   # 巴法云的MQTT目标设备的主题

# 创建接收器实例
if __name__ == "__main__":
    try:
        receiver = BemfaMQTTReceiver(
            uid=bemfa_uid,
            topic=bemfa_topic,
            target_ip=ip,
            target_user=user,
            target_passwd=passwd,
            target_mac=mac
        )
        if receiver.start():
            print("接收器启动成功，等待指令...")
            while True:
                time.sleep(1)
        else:
            print("接收器启动失败")
    except KeyboardInterrupt:
        receiver.stop()
        print("程序已退出")