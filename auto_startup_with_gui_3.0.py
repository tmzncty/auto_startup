import psutil
import os
import shutil
import sys
import time

def clear_startup_folder():
    startup_path = os.path.expanduser(r'~\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup')
    for item in os.listdir(startup_path):
        item_path = os.path.join(startup_path, item)
        if os.path.isfile(item_path):
            os.remove(item_path)  # 删除所有文件
        elif os.path.isdir(item_path):
            shutil.rmtree(item_path)  # 删除所有目录及其内容
    print("Startup folder cleared.")

def add_to_startup(exclude_list):
    startup_path = os.path.expanduser(r'~\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup')
    added_programs = []

    for proc in psutil.process_iter(['pid', 'name', 'exe']):
        try:
            exe_path = proc.info['exe']
            if proc.info['name'] not in exclude_list and exe_path and os.path.isfile(exe_path):
                shortcut_path = os.path.join(startup_path, proc.info['name'] + '.lnk')
                shutil.copyfile(exe_path, shortcut_path)
                added_programs.append(proc.info['name'])
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

    return added_programs

if __name__ == '__main__':
    clear_startup_folder()  # 清空启动文件夹

    exclude_list = ['Registry', os.path.basename(sys.executable)]  # 排除列表，包括程序自身
    added_programs = add_to_startup(exclude_list)  # 添加程序到启动文件夹

    print(f'Programs added to startup: {", ".join(added_programs)}')

    # 倒计时30秒
    for i in range(30, 0, -1):
        sys.stdout.write("\rClosing in {} seconds...".format(i))
        sys.stdout.flush()
        time.sleep(1)
