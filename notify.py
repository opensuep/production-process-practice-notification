#!/usr/bin/env python3
# Copyright (c) 2025 zhengxyz123
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import sys
import time

import requests

notify_title = "生产认识实习"
task_list_url = (
    "http://10.166.23.51:8080/rt/workflow/sutdentTasklist/getTaskAndBusinessInfoList"
)
check_sign_url = "http://10.166.23.51:8080/rt/com/mainstu/checkSign"
user_sign_url = "http://10.166.23.51:8080/rt/com/mainstu/userSign"
headers = {"X-Requested-With": "XMLHttpRequest"}


def show_notify(title: str, notify: str) -> None:
    print(f"[{time.strftime("%Y:%m:%d %H:%M:%S")}] {notify}")
    if sys.platform == "darwin":
        import subprocess

        subprocess.run(
            ["osascript", "-e", f'display notification "{notify}" with title "{title}"']
        )
    elif sys.platform == "linux":
        import subprocess

        subprocess.run(["notify-send", title, notify])
    elif sys.platform == "win32":
        from windows_toasts import Toast, WindowsToaster

        toaster = WindowsToaster(title)
        new_toast = Toast([notify])
        toaster.show_toast(new_toast)


def main(session_id: str) -> None:
    task = -1
    while True:
        # 新任务提醒
        response = requests.post(
            task_list_url,
            cookies={"JSESSIONID": session_id},
            headers=headers,
            data={"listMap[0].inMap.taskCode": ""},
        )
        if response.json()[0]["outMap"] is None:
            show_notify(notify_title, "请重新登陆")
            break
        now_task = len(response.json()[0]["outMap"]["data"][0]["second_menu"])
        if now_task > task:
            task = now_task
            if task == 0:
                show_notify(notify_title, "现在没有待办任务")
            else:
                show_notify(notify_title, f"你有 {task} 个待办任务")

        # 自动签到
        response = requests.post(
            check_sign_url, cookies={"JSESSIONID": session_id}, headers=headers
        )
        if response.json()[0]["outMap"]["flag"]:
            requests.post(
                user_sign_url, cookies={"JSESSIONID": session_id}, headers=headers
            )
            show_notify(notify_title, "已完成自动签到")
        time.sleep(1)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: ./notify.py [JSESSIONID]")
    try:
        main(sys.argv[1])
    except KeyboardInterrupt:
        print()
