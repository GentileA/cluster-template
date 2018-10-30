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
    
    node.addService(pg.Execute(shell="sh", command="sudo chmod 777 /local/repository/head_setup.sh"))
    node.addService(pg.Execute(shell="sh", command="sudo /local/repository/head_setup.sh"))

  elif i == 1:
    node = request.XenVM("metadata")
  elif i == 2:
    node = request.XenVM("storage")
    
    node.addService(pg.Execute(shell="sh", command="sudo chmod 777 /local/repository/storage_setup.sh"))
    node.addService(pg.Execute(shell="sh", command="sudo /local/repository/storage_setup.sh"))
  
  else:
    node = request.XenVM("compute-" + str(i-2))
    node.cores = 4
    node.ram = 4096
    
  iface = node.addInterface("if" + str(i))
  iface.component_id = "eth1"
  iface.addAddress(pg.IPv4Address(prefixForIP + str(i + 1), "255.255.255.0"))
  link.addInterface(iface)
  
  node.disk_image = "urn:publicid:IDN+emulab.net+image+emulab-ops:CENTOS7-64-STD"
  

  #needs fixed still
  #Setting up the Software NFS
  if i == 0:
    node.addService(pg.Execute(shell="sh", command="sudo yum -y install nfs-utils"))
    node.addService(pg.Execute(shell="sh", command="sudo chmod 755 /local/repository/scripts/install_mpi.sh"))
    node.addService(pg.Execute(shell="sh", command="sudo /local/repository/scripts/install_mpi.sh"))
    node.addService(pg.Execute(shell="sh", command="sudo rm /etc/exports"))
    node.addService(pg.Execute(shell="sh", command="sudo cp /local/repository/export/export_software /etc/exports"))
    node.addService(pg.Execute(shell="sh", command="sudo systemctl enable nfs-server"))
    node.addService(pg.Execute(shell="sh", command="sudo systemctl start nfs-server"))
    node.addService(pg.Execute(shell="sh", command="sudo exportfs -a"))
    node.addService(pg.Execute(shell="sh", command="sleep 2m"))
    node.addService(pg.Execute(shell="sh", command="sudo mount -t nfs 192.168.1.3:/scratch /scratch"))
    node.addService(pg.Execute(shell="sh", command="sudo echo '192.168.1.3:/scratch /scratch nfs4 rw,relatime,vers=4.1,rsize=131072,wsize=131072,namlen=255,hard,proto=tcp,port=0,timeo=600,retrans=2,sec=sys,local_lock=none,addr=192.168.1.3,_netdev,x-systemd.automount 0 0' | sudo tee --append /etc/fstab"))
  
  node.addService(pg.Execute(shell="sh", command="sudo chmod 755 /local/repository/passwordless.sh"))
  node.addService(pg.Execute(shell="sh", command="sudo /local/repository/passwordless.sh"))
  node.addService(pg.Execute(shell="sh", command="sudo chmod 755 /local/repository/install_mpi.sh"))
  node.addService(pg.Execute(shell="sh", command="sudo /local/repository/install_mpi.sh"))
  
  # This code segment is added per Benjamin Walker's solution to address the StrictHostKeyCheck issue of ssh
  node.addService(pg.Execute(shell="sh", command="sudo chmod 755 /local/repository/ssh_setup.sh"))
  node.addService(pg.Execute(shell="sh", command="sudo -H -u ag781693 bash -c '/local/repository/ssh_setup.sh'"))
 
  node.addService(pg.Execute(shell="sh", command="sudo su ag781693 -c 'cp /local/repository/source/* /users/ag781693'"))
  
# Print the RSpec to the enclosing page.
pc.printRequestRSpec(request)
