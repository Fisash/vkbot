import vk_api
import time
import datetime

while True:
    vk = vk_api.VkApi(token="токен")
    
    vk.method("status.set", {"text" : "тест"})
    print("Успешно!")
    time.sleep(120)