## 鸟哥的Linux私房菜重点精选

### 系统管理

##### 开机 关机 重启

```bash
#关机
alpine:/# poweroff

#重启
alpine:/# reboot

#关机 显示终端最后输出
alpine:/# halt

#将已修改的文件同步到磁盘
alpine:/# sync
```



##### 查看系统信息

```bash
alpine:/# uname --help
BusyBox v1.35.0 (2022-08-01 15:14:44 UTC) multi-call binary.

Usage: uname [-amnrspvio]

Print system information

        -a      Print all					#打印所有信息
        -m      Machine (hardware) type		#查看硬件平台
        -n      Hostname					#查看主机名称
        -r      Kernel release				#查看发行版本
        -s      Kernel name (default)		#查看内核名称
        -p      Processor type
        -v      Kernel version				#查看内核信息
        -i      Hardware platform
        -o      OS name
alpine:/#

```



### 用户管理

##### 添加用户 adduser 或者 useradd

```bash
alpine:/# adduser test
Changing password for test
New password:
Retype password:
Passwords don't match
passwd: password for test is unchanged
```



##### 添加用户组 addgroup 或者 groupadd

```bash
alpine:/# addgroup Go
alpine:/# adduser go-1 -G Go		#使用-G 指定用户组
Changing password for go-1
New password:
Bad password: too weak
Retype password:
passwd: password for go-1 changed by root
alpine:/#

```



### 文件权限管理

##### 查看文件权限

```bash
#使用ls -la 列出该目录下所有的文件信息
alpine:/var/lib/docker/volumes/mysql5_7/_data# ls -la
total 188484
drwxrwxrwt    5 999      ping          4096 Oct 10 06:43 .
drwx-----x    3 root     root          4096 Oct  9 08:45 ..
-rw-r-----    1 999      ping            56 Oct  9 08:45 auto.cnf
-rw-------    1 999      ping          1680 Oct  9 08:45 ca-key.pem
-rw-r--r--    1 999      ping          1112 Oct  9 08:45 ca.pem
-rw-r--r--    1 999      ping          1112 Oct  9 08:45 client-cert.pem
-rw-------    1 999      ping          1676 Oct  9 08:45 client-key.pem
-rw-r-----    1 999      ping           383 Oct 10 06:43 ib_buffer_pool
-rw-r-----    1 999      ping      50331648 Oct 10 06:43 ib_logfile0
-rw-r-----    1 999      ping      50331648 Oct  9 08:45 ib_logfile1
-rw-r-----    1 999      ping      79691776 Oct 10 06:43 ibdata1
-rw-r-----    1 999      ping      12582912 Oct 10 06:43 ibtmp1
drwxr-x---    2 999      ping          4096 Oct  9 08:45 mysql
drwxr-x---    2 999      ping          4096 Oct  9 08:45 performance_schema
-rw-------    1 999      ping          1680 Oct  9 08:45 private_key.pem
-rw-r--r--    1 999      ping           452 Oct  9 08:45 public_key.pem
-rw-r--r--    1 999      ping          1112 Oct  9 08:45 server-cert.pem
-rw-------    1 999      ping          1680 Oct  9 08:45 server-key.pem
drwxr-x---    2 999      ping         12288 Oct  9 08:45 sys

#文件权限为十个字母 - --- --- ---
#第一个表示文件或者文件夹 后九个每三个一组分别表示 文件拥有者 拥有组 其他用户的权限
# r:读取 w:写入 x:执行


```



##### 修改文件权限

```bash
#赋予文件执行的权限
alpine:~# chmod +x run.sh

#赋予文件-rwxrwxrwx 的权限
alpine:~# chmod 777 run.sh

# r=4	w=2    x=1
#r+w = 6	r+x = 5	  r+w+x = 7
```



### 磁盘管理

##### 查看磁盘挂载信息 lsblk

```bash
alpine:~# lsblk
NAME   MAJ:MIN RM  SIZE RO TYPE MOUNTPOINTS
sda      8:0    0   16G  0 disk
├─sda1   8:1    0  100M  0 part /boot
├─sda2   8:2    0  1.8G  0 part [SWAP]
└─sda3   8:3    0 14.1G  0 part /var/lib/docker
                                /
sdb      8:16   0    8G  0 disk
└─sdb1   8:17   0    8G  0 part /root/8G
sr0     11:0    1 1024M  0 rom
alpine:~#

```



##### 创建分区 fdisk

```bash
alpine:/dev# fdisk /dev/sdb

The number of cylinders for this disk is set to 1044.
There is nothing wrong with that, but this is larger than 1024,
and could in certain setups cause problems with:
1) software that runs at boot time (e.g., old versions of LILO)
2) booting and partitioning software from other OSs
   (e.g., DOS FDISK, OS/2 FDISK)

Command (m for help): m
Command Action
a       toggle a bootable flag
b       edit bsd disklabel
c       toggle the dos compatibility flag
d       delete a partition							#删除一个分区
l       list known partition types
n       add a new partition							#创建一个分区
o       create a new empty DOS partition table
p       print the partition table					#打印分区信息
q       quit without saving changes					#不保存退出分区工具
s       create a new empty Sun disklabel
t       change a partition's system id
u       change display/entry units
v       verify the partition table
w       write table to disk and exit				#保存
x       extra functionality (experts only)

```



##### 格式化分区 mkfs

```bash
#分区格式 分区设备号
alpine:~# mkfs.ext3 /dev/sdb1
```



##### 挂载分区 mount

```bash
# mount 设备名称 挂载点
# 挂载点要先创建好
alpine:~# mount /dev/sdb1 /root/8G
```



##### 卸载分区 umount

```bash
#umount 挂载点或者设备名称
alpine:~# umount /root/8G
```



##### 查看分区UUID blkid

```bash
alpine:~# blkid /dev/sdb1
/dev/sdb1: UUID="387cc1fb-fd56-4e9c-a66a-d8768089ad6f" BLOCK_SIZE="4096" TYPE="ext3"
```



##### 设置启动自动挂载

挂载文件一般为 /etc/fstab 或者 /etc/mtab

```bash
#设备名称或者UUID		挂载点		文件系统		参数配置		0 0 
#第一个0 为 是否被dump备份命令作用
#第二个0 为 是否开启fsck扇区校验

UUID=e7e49d5c-bec4-4272-a7e7-9776a86a1cd4       /       ext4    rw,relatime 0 1
UUID=e3176e62-71c3-4edc-a26f-09930724dc3f       /boot   ext4    rw,relatime 0 2
UUID=54579ece-42e1-470f-b332-9fc740489994       swap    swap    defaults        0 0
/dev/cdrom      /media/cdrom    iso9660 noauto,ro 0 0
/dev/usbdisk    /media/usb      vfat    noauto  0 0
tmpfs   /tmp    tmpfs   nosuid,nodev    0       0
/dev/sdb1       /root/8G        ext4    defaults        0 0

```



##### 使用parted管理硬盘

```bash
alpine:~# parted 设备名 命令 参数
	-mkpart [primary|logical|Extended] [ext4|vfat|xfs]	添加分区
	-print	打印所有分区信息
	-rm		删除分区
```



### 虚拟内存管理

##### 用磁盘分区创建内存交换空间

```bash
#使用swap格式化分区
alpine:~# mkswap /dev/sdb1
Setting up swapspace version 1, size = 8589898240 bytes
UUID=7cdd4284-62ee-4980-9699-358137da11ac

#使用swapon 激活交换空间分区
alpine:~# swapon /dev/sdb1
alpine:~# free -m
              total        used        free      shared  buff/cache   available
Mem:            944         489         149           3         306         303
Swap:         10080           0       10080

#可以使用swapoff /dev/sdb1 卸载交换空间
```



##### 使用文件创建内存交换空间

```bash
#使用dd 命令构建一个文件
#of=文件路径	bs=块大小	count=块数量

alpine:/# dd if=/dev/zero of=/SWAP.BLOCK bs=1M count=4096
4096+0 records in
4096+0 records out
alpine:/# ls -l
total 4194377
-rw-r--r--    1 root     root     4294967296 Oct 10 06:56 SWAP.BLOCK
drwxr-xr-x    2 root     root          4096 Oct 10 06:15 bin
drwxr-xr-x    3 root     root          1024 Sep 18 05:52 boot
drwxr-xr-x   14 root     root          3300 Oct 10 06:43 dev
drwxr-xr-x   34 root     root          4096 Oct 10 06:47 etc
drwxr-xr-x    2 root     root          4096 Sep 18 05:52 home
drwxr-xr-x   10 root     root          4096 Oct 10 06:15 lib
drwx------    2 root     root         16384 Sep 18 05:52 lost+found
drwxr-xr-x    5 root     root          4096 Sep 18 05:52 media
drwxr-xr-x    2 root     root          4096 Sep 18 05:52 mnt
drwxr-xr-x    3 root     root          4096 Sep 18 05:56 opt
dr-xr-xr-x  214 root     root             0 Oct 10 06:43 proc
drwx------    4 root     root          4096 Oct 10 06:47 root
drwxr-xr-x    8 root     root           460 Oct 10 06:43 run
drwxr-xr-x    2 root     root          4096 Sep 18 05:55 sbin
drwxr-xr-x    2 root     root          4096 Sep 18 05:52 srv
drwxr-xr-x    2 root     root          4096 Sep 18 05:53 swap
dr-xr-xr-x   13 root     root             0 Oct 10 06:43 sys
drwxrwxrwt    4 root     root            80 Oct 10 06:43 tmp
drwxr-xr-x    8 root     root          4096 Sep 18 05:52 usr
drwxr-xr-x   11 root     root          4096 Sep 18 05:53 var

#将文件转换为swap文件
alpine:/# mkswap /SWAP.BLOCK
Setting up swapspace version 1, size = 4294963200 bytes
UUID=6da9006a-cc35-41e5-b777-4fc783556991

#使用swapon 激活交换空间分区
alpine:/# swapon /SWAP.BLOCK
alpine:/# free -m
              total        used        free      shared  buff/cache   available
Mem:            944         468          62           3         414         329
Swap:          5984          18        5966
alpine:/#

```

