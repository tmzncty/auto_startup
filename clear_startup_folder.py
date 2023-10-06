import os
import shutil

def clear_startup_folder():
    startup_path = os.path.expanduser(r'~\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup')
    for item in os.listdir(startup_path):
        item_path = os.path.join(startup_path, item)
        if os.path.isfile(item_path):
            os.remove(item_path)  # 删除所有文件
        elif os.path.isdir(item_path):
            shutil.rmtree(item_path)  # 删除所有目录及其内容

    print("Startup folder cleared.")

if __name__ == "__main__":
    clear_startup_folder()
