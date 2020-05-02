# %%
import os
from pathlib import Path
import subprocess
import sys

import cv2
import face_recognition
from IPython.display import display
from IPython.display import Image


cwd = Path().resolve()


def exec_cmd(cmd):
    """ コマンド実行 """
    # cmd文字列の前後にスペースが入っていたら削除 -> スペースで分割しlist化
    cmd_split = cmd.strip().split()
    # stdoutの設定で標準出力を取得
    cp = subprocess.run(cmd_split, stdout=subprocess.PIPE)
    # cp = subprocess.check_output(cmd_split)
    if cp.returncode != 0:
        print(f'{cmd_split[0]} faild.', file=sys.stderr)
        sys.exit(1)
    # 標準出力があれば返す
    if cp.stdout is not None:
        return cp.stdout.decode('utf-8')


# def get_size(img_path):
#     """ 画像の高さ・幅を取得 """
#     img = cv2.imread(img_path)
#     height, width, _ = img.shape[:3]
#     return height, width


def display_image(img_path):
    img = cv2.imread(img_path)
    format = os.path.splitext(img_path)[1]  # .jpg, .png
    decoded_bytes = cv2.imencode(format, img)[1].tobytes()
    display(Image(data=decoded_bytes))


def get_face_location(img_path):
    cmd_face_detection = f'face_detection {img_path}'
    # cmd_face_detection = f'face_detection --model cnn {img_path}'
    stdout = exec_cmd(cmd_face_detection)
    stdout_list = stdout.strip().split(',')
    top = int(stdout_list[1])
    right = int(stdout_list[2])
    bottom = int(stdout_list[3])
    left = int(stdout_list[4])
    print(stdout)
    print(stdout_list)

    return top, right, bottom, left


if __name__ == '__main__':
    file_name = f'Zinedine_Zidane_0001.jpg'
    input_path = f'{cwd}/../input'
    output_path = f'{cwd}/../output'
    os.makedirs(output_path, exist_ok=True)

    top, right, bottom, left = get_face_location(f'{input_path}/{file_name}')
    print(top)
    print(bottom)
    print(left)
    print(right)

    img = cv2.imread(f'{input_path}/{file_name}')
    display_image(f'{input_path}/{file_name}')

    img_face = img[top:bottom, left:right]
    cv2.imwrite(f'{output_path}/{file_name}', img_face)
    display_image(f'{output_path}/{file_name}')

# %%
