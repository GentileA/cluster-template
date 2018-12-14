# Import the Portal object.
import geni.portal as portal
# Import the ProtoGENI library.
import geni.rspec.pg as pg
import geni.rspec.igext as IG

# Create a portal context.
pc = portal.Context()

# Create a Request object to start building the RSpec.
request = pc.makeRequestRSpec()


tourDescription = \
"""
This profile provides the template for a full research cluster with head node, scheduler, compute nodes, and shared file systems.
First node (head) should contain: 
- Shared home directory using Networked File System
- Management server for SLURM
Second node (metadata) should contain:
- Metadata server for SLURM
Third node (storage):
- Shared software directory (/software) using Networked File System
Remaining three nodes (computing):
- Compute nodes  
"""

#
# Setup the Tour info with the above description and instructions.
#  
tour = IG.Tour()
tour.Description(IG.Tour.TEXT,tourDescription)
request.addTour(tour)

prefixForIP = "192.168.1."

link = request.LAN("lan")

for i in range(15):
  if i == 0:
    node = request.XenVM("head")
    node.routable_control_ip = "true"
    
    #We are not using the head_setup.sh script, there is nothing in the local repository with this
    #node.addService(pg.Execute(shell="sh", command="sudo chmod 777 /local/repository/head_setup.sh"))
    #node.addService(pg.Execute(shell="sh", command="sudo /local/repository/head_setup.sh"))

  elif i == 1:
    node = request.XenVM("metadata")
  elif i == 2:
    node = request.XenVM("storage")
    
    #We are not using the storage_setup.sh script, there is nothing in the local repository
    #node.addService(pg.Execute(shell="sh", command="sudo chmod 777 /local/repository/storage_setup.sh"))
    #node.addService(pg.Execute(shell="sh", command="sudo /local/repository/storage_setup.sh"))
  
  else:
    node = request.XenVM("compute-" + str(i-2))
    node.cores = 4
    node.ram = 4096
    
  iface = node.addInterface("if" + str(i))
  iface.component_id = "eth1"
  iface.addAddress(pg.IPv4Address(prefixForIP + str(i + 1), "255.255.255.0"))
  link.addInterface(iface)
  
  node.disk_image = "urn:publicid:IDN+emulab.net+image+emulab-ops:CENTOS7-64-STD"

  #Disabling the firewall
  node.addService(pg.Execute(shell="sh", command="sudo systemct1 disable firewalld"))
  
  #Setup of directories and permissions for all nodes other than the head node
  if i != 1:
    node.addService(pg.Execute(shell="sh", command="sudo mkdir /scratch"))
    node.addService(pg.Execute(shell="sh", command="sudo chmod 777 /scratch"))
  if i != 1 and i != 2:
    node.addService(pg.Execute(shell="sh", command="sudo mkdir /software"))
    #node.addServcie(pg.Execute(shell="sh", command="sudo chmod 777 /software"))
  
  #Setup of Storage Node (2)
  if i == 2:
    node.addService(pg.Execute(shell="sh", command="sudo yum -y install nfs-utils"))
    node.addService(pg.Execute(shell="sh", command="sudo su ag781693 -c 'sudo cp /local/repository/source/* /scratch'"))
    node.addService(pg.Execute(shell="sh", command="sudo rm /etc/exports"))
    node.addService(pg.Execute(shell="sh", command="sudo cp /local/repository/export_scratch /etc/exports"))
    node.addService(pg.Execute(shell="sh", command="sudo systemctl enable nfs-server"))
    node.addService(pg.Execute(shell="sh", command="sudo systemctl start nfs-server"))
    node.addService(pg.Execute(shell="sh", command="sudo exportfs -a"))

  #needs fixed still
  #Setting up the Software NFS
  if i == 0:
    node.addService(pg.Execute(shell="sh", command="sudo yum -y install nfs-utils"))
    node.addService(pg.Execute(shell="sh", command="sudo chmod 755 /local/repository/install_mpi.sh"))
    node.addService(pg.Execute(shell="sh", command="sudo /local/repository/install_mpi.sh"))
    node.addService(pg.Execute(shell="sh", command="sudo rm /etc/exports"))
    node.addService(pg.Execute(shell="sh", command="sudo cp /local/repository/export_software /etc/exports"))
    node.addService(pg.Execute(shell="sh", command="sudo systemctl enable nfs-server"))
    node.addService(pg.Execute(shell="sh", command="sudo systemctl start nfs-server"))
    node.addService(pg.Execute(shell="sh", command="sudo exportfs -a"))
    node.addService(pg.Execute(shell="sh", command="sleep 2m"))
    node.addService(pg.Execute(shell="sh", command="sudo mount -t nfs 192.168.1.3:/scratch /scratch"))
    node.addService(pg.Execute(shell="sh", command="sudo echo '192.168.1.3:/scratch /scratch nfs4 rw,relatime,vers=4.1,rsize=131072,wsize=131072,namlen=255,hard,proto=tcp,port=0,timeo=600,retrans=2,sec=sys,local_lock=none,addr=192.168.1.3,_netdev,x-systemd.automount 0 0' | sudo tee --append /etc/fstab"))
  
  if i > 2:
    node.addService(pg.Execute(shell="sh", command="sudo yum -y install nfs-utils"))
    #runtime of install_mpi on the head node was taking 20 minutes to install so this will slepp for 25
    node.addService(pg.Execute(shell="sh", command="sleep 25m"))
    node.addService(pg.Execute(shell="sh", command="sudo mount -t nfs 192.168.1.3:/scratch /scratch"))
    node.addService(pg.Execute(shell="sh", command="sudo mount -t nfs 192.168.1.1:/software /software"))
    node.addService(pg.Execute(shell="sh", command="sudo chmod 777 /local/repository/scripts/mpi_path_setup.sh"))
    node.addService(pg.Execute(shell="sh", command="sudo -H -u gb773994 bash -c '/local/repository/scripts/mpi_path_setup.sh'"))   
    node.addService(pg.Execute(shell="sh", command="sudo echo '192.168.1.1:/software /software nfs4 rw,relatime,vers=4.1,rsize=131072,wsize=131072,namlen=255,hard,proto=tcp,port=0,timeo=600,retrans=2,sec=sys,local_lock=none,addr=192.168.1.1,_netdev,x-systemd.automount 0 0' | sudo tee --append /etc/fstab"))
    node.addService(pg.Execute(shell="sh", command="sudo echo '192.168.1.3:/scratch /scratch nfs4 rw,relatime,vers=4.1,rsize=131072,wsize=131072,namlen=255,hard,proto=tcp,port=0,timeo=600,retrans=2,sec=sys,local_lock=none,addr=192.168.1.3,_netdev,x-systemd.automount 0 0' | sudo tee --append /etc/fstab"))
  
  #Setting up the automatic ssh permissions using passwordless.sh
  node.addService(pg.Execute(shell="sh", command="sudo chmod 755 /local/repository/passwordless.sh"))
  node.addService(pg.Execute(shell="sh", command="sudo /local/repository/passwordless.sh"))
  
  #install_mpi.sh is only being installed on the head node
  #node.addService(pg.Execute(shell="sh", command="sudo chmod 755 /local/repository/install_mpi.sh"))
  #node.addService(pg.Execute(shell="sh", command="sudo /local/repository/install_mpi.sh"))
  
  # This code segment is added per Benjamin Walker's solution to address the StrictHostKeyCheck issue of ssh
  node.addService(pg.Execute(shell="sh", command="sudo chmod 755 /local/repository/ssh_setup.sh"))
  node.addService(pg.Execute(shell="sh", command="sudo -H -u ag781693 bash -c '/local/repository/ssh_setup.sh'"))
 
  node.addService(pg.Execute(shell="sh", command="sudo su ag781693 -c 'cp /local/repository/source/* /users/ag781693'"))
  
# Print the RSpec to the enclosing page.
pc.printRequestRSpec(request)
