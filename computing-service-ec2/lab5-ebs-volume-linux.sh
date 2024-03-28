######################## Mount and extend EBS volume #################
#list all partition and mountpoint
lsblk
#display all volume and free space
df -h
#Using fdisk to create partition.
sudo fdisk /dev/xvdf

#format partition
sudo mkfs -t xfs /dev/xvdf1
#Mount
sudo mount /dev/xvdf1 /data

#Make volume auto mount after restart
sudo blkid
sudo lsblk -o +UUID

#Modify fstab file, then add 1 line for /data volume
sudo vi /etc/fstab
#Test auto mount
sudo umount /data
sudo mount -a

#Grow part after extend EBS volume on AWS Console.
sudo growpart /dev/xvdf 1
