
sudo yum install nsf-utils        #https://www.howtoforge.com/nfs-server-and-client-on-centos-7
mkdir /software                   # make directory called /software
chmod -R 755 /software            # change user permissions 

/software    192.168.0.101(rw,sync,no_root_squash,no_all_squash) # assign ip possibly loop to get more

systemctl restart nfs-server      #start the NFS server

mkdir /scratch
mkdir -p /mnt/nfs/scratch
