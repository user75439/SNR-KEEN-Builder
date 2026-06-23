import os
from datetime import datetime

def run_snr_automation():
    # Имя нашего шаблона для SNR
    template_name = "SNR-W4N.dat"
    output_folder = "test_configs_snr"
    
    if not os.path.exists(template_name):
        print(f"[-] Ошибка: Шаблон '{template_name}' не найден в текущей папке!")
        print("Пожалуйста, переименуй свой файл в 'SNR-W4N.dat' и положи рядом со скриптом.")
        return

    print("=" * 60)
    print(" ТЕСТОВЫЙ ГЕНЕРАТОР КОНФИГУРАЦИЙ ДЛЯ SNR-CPE-W4N (.DAT) ")
    print("=" * 60)
    
    # Сбор данных абонента
    login_pppoe = input("Введите логин PPPoE: ").strip()
    passwd_pppoe = input("Введите пароль PPPoE: ").strip()
    wifi_name = input("Введите название Wi-Fi (SSID): ").strip()
    wifi_passwd = input("Введите пароль Wi-Fi (WPA-PSK): ").strip()
    
    if not all([login_pppoe, passwd_pppoe, wifi_name, wifi_passwd]):
        print("[-] Ошибка: Все поля должны быть заполнены!")
        return

    # Читаем шаблон целиком в одну строку
    print("[+] Чтение шаблона...")
    with open(template_name, "r", encoding="utf-8") as f:
        template_data = f.read()
        
    # Подставляем переменные абонента
    print("[+] Подстановка данных абонента...")
    try:
        final_config = template_data.format(
            LOGIN_PPPOE=login_pppoe,
            PASSWD_PPPOE=passwd_pppoe,
            WIFI_NAME=wifi_name,
            WIFI_PASSWD=wifi_passwd
        )
    except KeyError as e:
        print(f"[-] Ошибка: В шаблоне SNR обнаружен неизвестный или ошибочный маркер: {e}")
        return

    # Создаем папку для тестов, если её нет
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Сохраняем итоговый файл с расширением .dat
    filename = f"SNR_{login_pppoe}.dat"
    full_path = os.path.join(output_folder, filename)

    # newline="\n" важен для Unix-подобных систем прошивки, чтобы переносы строк не поплыли
    with open(full_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(final_config)

    print("\n" + "*" * 50)
    print(f"[+] ТЕСТОВЫЙ ЗАПУСК ДЛЯ SNR УСПЕШЕН!")
    print(f"[+] Готовый файл сохранен: {full_path}")
    print("[+] Проверь его текстовым редактором перед заливкой на роутер.")
    print("*" * 50 + "\n")

if __name__ == "__main__":
    run_snr_automation()