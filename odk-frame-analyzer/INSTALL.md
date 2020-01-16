## NVIDIA & CUDA drivers

CUDA:
https://docs.nvidia.com/cuda/cuda-installation-guide-linux/index.html

During CUDA install some files could not be deleted:
cat /var/log/nvidia-uninstall.log

Post install CUDA asked to set a path, but there is no 'NsightCompute-2019.1' after the install:
```
$ export PATH=/usr/local/cuda-10.2/bin:/usr/local/cuda-10.2/NsightCompute-2019.1${PATH:+:${PATH}}
```

CUDA should install a NVIDIA driver, if not:

NVIDIA Driver:
https://www.nvidia.com/content/DriverDownload-March2009/confirmation.php?url=/XFree86/Linux-x86_64/440.36/NVIDIA-Linux-x86_64-440.36.run&lang=us&type=TITAN

Has to disable nouveau-kernel-driver when installing NVIDIA driver:
https://askubuntu.com/questions/841876/how-to-disable-nouveau-kernel-driver

In order to install a new Nvidia driver the current display server, X, must be stopped:
```
$ sudo telinit 3 
```

Now you can install the driver:
```
$ sudo bash NVIDIA-Linux-x86_64-440.36.run
```

## Mirror files to GPU server 2

https://www.digitalocean.com/community/tutorials/how-to-mirror-local-and-remote-directories-on-a-vps-with-lsyncd
