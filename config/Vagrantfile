# need cifs-utils and linux-azure and a nice reboot
$script = <<-SCRIPT
echo I am provisioning...
update-locale LANG=en_US.UTF-8
echo "nameserver 1.1.1.1" > /etc/resolv.conf  # needed before installing linux-azure
apt install -y curl make git
SCRIPT

Vagrant.configure("2") do |config|
  config.vm.box = "generic/ubuntu1804"
  config.vm.provider "hyperv" do |h|
    h.enable_virtualization_extensions = true
    h.linked_clone = true
  end
  config.vm.provider "virtualbox" do |v|
    v.linked_clone = true
    v.memory = 2048
    v.cpus = 2
  end
  config.vm.synced_folder ".", "/vagrant"
  config.trigger.after [:provision] do |t|
    t.name = "Reboot after provisioning"
    t.run = {inline: "vagrant reload"}
  end
  config.vm.provision "shell", inline: $script
  config.vm.network "forwarded_port", guest: 8000, host: 8888
  config.ssh.forward_agent = true
end
