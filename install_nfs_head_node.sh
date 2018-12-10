#  source:  https://www.howtoforge.com/nfs-server-and-client-on-centos-7

sudo yum install nsf-utils
mkdir /software                           # make directory called /software
chmod -R 755 /software                    # change user permissions 

#let nfs service override centos7 firewall
sudo firewall-cmd --permanent --zone=public --add-service=nfs
sudo firewall-cmd --permanent --zone=public --add-service=mountd
sudo firewall-cmd --permanent --zone=public --add-service=rpc-bind
sudo firewall-cmd --reload

#set client up
sudo sleep 180
sudo mkdir -p/ scratch
sudo mount -t nfs 192.168.1.3:/scratch /scratch
#setup automount
sudo echo "192.168.1.3:/scratch /scratch nfs defaults 0 0" >> /etc/fstab

#export directory
sudo echo "/software   *(rw,sync,no_root_squash,no_all_squash) > etc/exports 
sudo systemctl restart nfs-serve

#install mpi
sudo chmod 777/local/respository/install_mpi.sh
sudo /local/respositroy/install_mpi_sh


systemctl enable rpcbind
systemctl enable nfs-server
systemctl enable nfs-lock
systemctl enable nfs-idmap                #preventing premissions being changed if our host directory is changed
systemctl start rpcbind
systemctl start nfs-server
systemctl start nfs-lock
systemctl start nfs-idmap


