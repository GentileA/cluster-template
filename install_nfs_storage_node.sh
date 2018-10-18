yum install nfs-utils
mkdir /var/scratch

chmod -R 755/var/scratch                
chown nfsnobody:nfsnobody/var/scratch

/scratch  192.168.0.101 (rw,sync,no_root_squash,no_all_squash
)
/home     192.168.0.101( rw,sync,no_root_squash,no_all_squash 
)
