import os, re, glob
import subprocess

print(f"Flash_Tool v1.0 一键编译下载py脚本")
print(f"适用于linux 由Makefile编译的stm32工程")
print(" ")
print("--------------------------------Made By Liam (Quan.2003@outlook.com)")
print(" ")
print(" ")

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

'''
openocd -s /usr/share/openocd/scripts 
-f /home/lyn/Code_Workspace/STM32/microROS_test/stm32f429discovery.cfg 
-c "tcl_port disabled" 
-c "gdb_port disabled" 
-c "tcl_port disabled" 
-c "program \"E:/microROS_test.elf\"" 
-c reset -c shutdown
'''


ws_path_ = os.popen("pwd")
ws_path = ws_path_.read()
ws_path = ws_path.rstrip()

openocd_path_ = os.popen("which openocd")
openocd_path = openocd_path_.read()
if(openocd_path):
    print(f"Found {openocd_path}")
else:
    print("Not Found openocd")

directory_name = "/usr/share/openocd/scripts"
if(os.path.exists(directory_name)):
    print(f"Found openocd/scripts")
else:
    print(f"Not Found the openocd/scripts!!!")

try:
    with open('Makefile','r') as file:
        makefile_content = file.read()
    target_pattern = re.compile(r'^TARGET\s*=\s*(\S+)',re.MULTILINE)
    match = target_pattern.search(makefile_content)
    
    if match:
        target = match.group(1)
        print(f'Found TARGET:{target}')
    else:
        print("Not Found Makefile")
except FileNotFoundError:
    print('Not Found Makefile')
except Exception as e:
    print("发生错误，退出！！！")

name_elf = target + ".elf"
elf_path = os.path.join(ws_path,"build",name_elf)
print("Found path xx.elf: %s\n"%elf_path)
    
cfg_path = r"stm32*.cfg"
cfg_list = glob.glob(cfg_path)
print(f"Found {cfg_list[0]}")

tcl_cmd = "-c \"tcl_port disabled\""
gdb_cmd = "-c \"gdb_port disabled\""
c_cmd   = "-c"
pro_cmd = "\"program"
reset_cmd = "-c reset"
poff_cmd = "-c shutdown"
s_cmd = "-s"
f_cmd = "-f"
cv_cmd = "\""

cmd_list = [openocd_path.rstrip(),s_cmd,"/usr/share/openocd/scripts",f_cmd,os.path.abspath(cfg_list[0]),tcl_cmd,gdb_cmd,tcl_cmd,c_cmd,pro_cmd,"\\"+cv_cmd+elf_path+"\\"+cv_cmd+cv_cmd,reset_cmd,poff_cmd]

# 定义要执行的Bash命令
cmd = " ".join(cmd_list)
print(cmd)

os.popen(cmd)
print(" ")
print(f"Openocd 脚本执行完成！！！")
print(f"执行权利移交至Openocd")
print(" ")

