#!/bin/env python3
import sys
import time

import requests

task_list_url = (
    "http://10.166.23.51:8080/rt/workflow/sutdentTasklist/getTaskAndBusinessInfoList"
)
headers = {"X-Requested-With": "XMLHttpRequest"}


def send_notify(notify: str) -> None:
    print(f"[{time.strftime("%Y:%m:%d %H:%M:%S")}] {notify}")
    if sys.platform.startswith("linux"):
        import subprocess

        subprocess.run(["notify-send", "-a", "生产认知实习", "新任务通知", notify])
    elif sys.platform.startswith("win"):
        from windows_toasts import Toast, WindowsToaster

        toaster = WindowsToaster("生产认知实习")
        new_toast = Toast()
        new_toast.text_fields = [notify]
        toaster.show_toast(new_toast)


def mainloop(session_id: str) -> None:
    task = -1
    while True:
        response = requests.post(
            task_list_url,
            cookies={"JSESSIONID": session_id},
            headers=headers,
            data={"listMap[0].inMap.taskCode": ""},
        )
        now_task = len(response.json()[0]["outMap"]["data"][0]["second_menu"])
        if now_task > task:
            task = now_task
            send_notify(f"你有 {task} 个待办任务")
        time.sleep(1)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: ./notify.py [JSSESSIONID]")
    try:
        mainloop(sys.argv[1])
    except KeyboardInterrupt:
        print()
