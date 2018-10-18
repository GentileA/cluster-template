#  source:  https://www.howtoforge.com/nfs-server-and-client-on-centos-7

sudo yum install nsf-utils
mkdir /software                           # make directory called /software
chmod -R 755 /software                    # change user permissions 

/software    192.168.0.1(rw,sync,no_root_squash,no_all_squash) # create share points

systemctl enable rpcbind
systemctl enable nfs-server
systemctl enable nfs-lock
systemctl enable nfs-idmap                #preventing premissions being changed if our host directory is changed
systemctl start rpcbind
systemctl start nfs-server
systemctl start nfs-lock
systemctl start nfs-idmap

systemctl restart nfs-server              #start the NFS server

mkdir /scratch                            #make directory to be mounted      
mkdir -p /mnt/nfs/scratch             
touch /mnt/nfs/var/scratch/test_nfs
