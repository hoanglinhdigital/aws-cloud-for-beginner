######################## Mount and extend EBS volume #################
#list all partition and mountpoint
lsblk
#display all volume and free space
df -h
#Using fdisk to create partition.
sudo fdisk /dev/xvdb
Nhan: 'n', default ... enter
Nhan: 'w' để save lại.
#Kiểm tra bằng lệnh sau, nếu thấy partiion tạo ra ngay dưới level disk là OK
lsblk

#format partition
sudo mkfs -t xfs /dev/xvdb1
#Tạo folder để mount
sudo mkdir /data
#Mount
sudo mount /dev/xvdb1 /data

#Test write data to /data
sudo vi /data/test.txt

#Make volume auto mount after restart EC2
sudo blkid
sudo lsblk -o +UUID

#Modify fstab file, then add 1 line for /data volume
sudo vi /etc/fstab
#Test auto mount
sudo umount /data
sudo mount -a
df -h

#Extend volume in AWS Console.
#Login to Linux server, check disk and partition.
lsblk
#Grow Volume after extend EBS volume on AWS Console.
sudo growpart /dev/xvdb 1
#Grow part after extend volume
sudo xfs_growfs -d /data
#Kiem tra lai:
df -h
