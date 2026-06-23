import os
import time
import requests

def run_automation():
    template_name = "KN-1112.txt"
    
    # Базовые настройки для подключения к новому/сброшенному роутеру
    ROUTER_IP = "192.168.1.1"
    # Если на сброшенном роутере пустой пароль, requests отправит базовую сессию.
    # Так как в твоем шаблоне уже зашит правильный пароль администратора,
    # после перезагрузки роутер станет доступен по вашим стандартам.
    
    if not os.path.exists(template_name):
        print(f"[-] Ошибка: Шаблон '{template_name}' не найден!")
        return

    print("=" * 60)
    print(" АВТОМАТИЗАЦИЯ КАНАЛА ПОДГОТОВКИ И ЗАЛИВКИ KEENETIC KN-1112 ")
    print("=" * 60)
    
    # 1. Сбор данных абонента
    login_pppoe = input("Введите логин PPPoE: ").strip()
    passwd_pppoe = input("Введите пароль PPPoE: ").strip()
    wifi_name = input("Введите название Wi-Fi (SSID): ").strip()
    wifi_passwd = input("Введите пароль Wi-Fi (WPA-PSK): ").strip()
    
    if not all([login_pppoe, passwd_pppoe, wifi_name, wifi_passwd]):
        print("[-] Ошибка: Все поля должны быть заполнены!")
        return

    # 2. Чтение и рендеринг конфига в памяти (без создания лишних файлов на ПК)
    with open(template_name, "r", encoding="utf-8") as f:
        template_data = f.read()
        
    try:
        final_config = template_data.format(
            LOGIN_PPPOE=login_pppoe,
            PASSWD_PPPOE=passwd_pppoe,
            WIFI_NAME=wifi_name,
            WIFI_PASSWD=wifi_passwd
        )
    except KeyError as e:
        print(f"[-] Ошибка в маркерах шаблона: {e}")
        return

# === НАЧАЛО БЛОКА ТЕСТОВОГО СОХРАНЕНИЯ ===
    output_folder = "test_configs"
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Имя файла будет содержать логин абонента, чтобы конфиги не перезаписывали друг друга
    filename = f"test_config_{login_pppoe}.txt"
    full_path = os.path.join(output_folder, filename)

    with open(full_path, "w", encoding="utf-8") as f:
        f.write(final_config)

    print("\n" + "*" * 50)
    print(f"[+] ТЕСТОВЫЙ ЗАПУСК УСПЕШЕН!")
    print(f"[+] Сгенерированный конфиг сохранен в папку: {full_path}")
    print("[+] Открой этот файл и проверь, встали ли пароли на свои места.")
    print("*" * 50 + "\n")
    # === КОНЕЦ БЛОКА ТЕСТОВОГО СОХРАНЕНИЯ ===
'''

    # 3. Отправка конфигурации на роутер через HTTP RCI
    print(f"\n[+] Подключение к роутеру {ROUTER_IP}...")
    
    # Сначала проверяем доступность роутера
    try:
        response = requests.get(f"http://{ROUTER_IP}/rci/show/system", timeout=5)
    except requests.exceptions.RequestException:
        print(f"[-] Ошибка: Не удалось связаться с роутером {ROUTER_IP}.")
        print("Проверь, подключен ли кабель в LAN-порт и получил ли комп IP-адрес 192.168.1.x.")
        return

    print("[+] Роутер ответил. Начинаем заливку конфигурации в flash...")
    
    # Keenetic принимает файлы конфигурации через специальный endpoint. 
    # Мы загружаем его прямо как text/plain в раздел `startup-config`
    url_upload = f"http://{ROUTER_IP}/rci/system/configuration/save"
    
    try:
        # Отправляем файл конфигурации
        files = {'startup-config': ('startup-config', final_config, 'text/plain')}
        upload_req = requests.post(f"http://{ROUTER_IP}/upload", files=files, timeout=15)
        
        if upload_req.status_code == 200:
            print("[+] Конфигурация успешно записана в startup-config!")
        else:
            print(f"[-] Ошибка при передаче файла. Код ответа: {upload_req.status_code}")
            return
            
    except Exception as e:
        print(f"[-] Что-то пошло не так при загрузке: {e}")
        return '''

'''

    # 4. Фиксация конфига в качестве ЗАВОДСКОГО (Дефолтного)
    # Чтобы при нажатии кнопки Reset роутер возвращался именно к этой конфигурации!
    print("[+] Фиксируем конфигурацию как заводскую (flash default-config)...")
    
    cmd_url = f"http://{ROUTER_IP}/rci/system/configuration/default"
    # Отправляем JSON-команду для подмены дефолтного конфига текущим startup-config
    try:
        # В зависимости от версии KeenOS, команда копирования дефолта передается через RCI
        rci_payload = {"source": "startup-config"}
        rci_req = requests.post(cmd_url, json=rci_payload, timeout=10)
        
        # 5. Отправляем роутер в перезагрузку
        print("[+] Перезагружаем роутер для применения всех хэшей и настроек...")
        requests.post(f"http://{ROUTER_IP}/rci/system/reboot", json={}, timeout=3)
        
        print("=" * 60)
        print("[+] ГОТОВО! Роутер настраивается и уходит в ребут.")
        print("[+] Теперь при любом сбросе кнопкой RESET он вернется к этим настройкам.")
        print("=" * 60)
        
    except requests.exceptions.ConnectionError:
        # Это нормально, так как роутер мгновенно рвет соединение при уходе в ребут
        print("\n[+] Роутер успешно ушел в перезагрузку. Отключай кабель!")
        print("=" * 60)
    except Exception as e:
        print(f"[-] Не удалось завершить команду фиксации/ребута: {e}") '''

if __name__ == "__main__":
    run_automation()