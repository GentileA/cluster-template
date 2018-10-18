#install nfs
sudo yum install nfs-utils
mkdir/scratch
chmod -R 755/var/scratch                
chown nfsnobody:nfsnobody/var/scratch

/scratch  192.168.0.101 (rw,sync,no_root_squash,no_all_squash)

systemctl restart nfs-server

mkdir / scratch
mkdir –p/mnt/nfs/scratch
touch /mnt/nfs/var/scratch/test_nfs

