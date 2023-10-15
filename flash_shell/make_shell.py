import subprocess

# 定义要执行的Bash命令
command = "make -j12"

try:
    # 执行Bash命令，并捕获输出
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()

    if process.returncode == 0:
        print("标准输出:\n", stdout.decode("utf-8"))
    else:
        print("错误输出:\n", stderr.decode("utf-8"))
except subprocess.CalledProcessError as e:
    print(f'执行Bash命令时发生错误: {e}')