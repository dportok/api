Vagrant.configure("2") do |config|
  config.vm.box = "centos/7"
  config.vm.box_version = "2004.01"
  config.vm.hostname = "application-server"
  config.vm.network "private_network", ip: "192.168.50.11"
   config.ssh.insert_key = false
# Virtualbox related parameters
  config.vm.provider "virtualbox" do |vb|
    vb.memory = "4096"
    vb.cpus = "2"
    vb.name = "msd"
    end
end