## NVIDIA & CUDA drivers

NVIDIA Driver:
https://www.nvidia.com/content/DriverDownload-March2009/confirmation.php?url=/XFree86/Linux-x86_64/440.36/NVIDIA-Linux-x86_64-440.36.run&lang=us&type=TITAN

Has to disable nouveau-kernel-driver when installing NVIDIA driver:
https://askubuntu.com/questions/841876/how-to-disable-nouveau-kernel-driver

CUDA:
https://docs.nvidia.com/cuda/cuda-installation-guide-linux/index.html

Durinf CUDA install some files could not be deleted:
cat /var/log/nvidia-uninstall.log

Post install CUDA asked to set path to:
$ export PATH=/usr/local/cuda-10.2/bin:/usr/local/cuda-10.2/NsightCompute-2019.1${PATH:+:${PATH}}
but there is no 'NsightCompute-2019.1' after the install

## Mirror files to GPU server 2

https://www.digitalocean.com/community/tutorials/how-to-mirror-local-and-remote-directories-on-a-vps-with-lsyncd
