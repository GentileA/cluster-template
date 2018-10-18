#install nfs
sudo yum install nfs-utils
mkdir/scratch
chmod -R 755/var/scratch                
chown nfsnobody:nfsnobody/var/scratch

/scratch  192.168.0.101 (rw,sync,no_root_squash,no_all_squash)

systemct1 enable rpcbind
systemct1 enable nfs-server
systemct1 enable nfs-lock
systemct1 enable nfs-idmap
systemct1 start rpcbind
systemct1 start nfs-server
systemct1 start nfs-lock
systemct1 start nfs-idmap 

systemctl restart nfs-server

mkdir / scratch
mkdir –p/mnt/nfs/scratch


