Title: BOINC, systemd and Linux process priority, next
Date: 2018-12-05 01:00
Author: Paul
Tags: BOINC, Linux, Libre, systemd
Slug: boinc-systemd-et-priorite-des-processus-sous-linux-la-suite
Lang: en

In my [previous post]({filename}boinc-systemd-process-priority.md) I believed to have my problem solved, the BOINC daemon was leaving system resources free if needed.

To do so I had configured systemd to allocate the lowest priority to the cgroup containing BOINC compute processes:
`sudo systemctl set-property boinc.service CPUWeight=1`

This attribute is not available in systemd versions before 231, when it replaced the CPUShares attributes.

The equivalent setting for those versions is:
`systemctl set-property boinc.service CPUShares=2`

This change reflects a change in the kernel configuration for cgroups. The cpu.shares attributes was replaced by cpu.weight. This change was not merged into the main Linux branch, as such systemd has [to convert the CPUWeight value to its cpu.shares equivalent](https://github.com/systemd/systemd/blob/4c701096002fff540d9ddb3b21398c551ac3af78/src/core/cgroup.c#L732) on my system.

However I noticed that playing videos on my system was having some slow downs. By doing the experiment previously described again, I got different results showing that BOINC was still not releasing all CPU resources when needed.

After reading some documentation as the [systemd manual page about resource management](https://www.freedesktop.org/software/systemd/man/systemd.resource-control.html) and the [kernel documentation about cgroups](https://www.kernel.org/doc/Documentation/cgroup-v2.txt), I was able to understand better the problem.

Cgroups are hierarchically organized. CPU resources defined by a cgroup are shared by cgroups with the same parent.

Systemd also uses a specific hierarchy to group system processes, named slices. System groups service and user processes into different slices, user.slice and system.slice. Their parent is the root slice .slice. It can displayed by the command `systemd-cgls` which represents a tree of processes, services and slices. These slices are then used by systemd to layout the cgroups it creates.

The BOINC service is started in the system.slice slice, as most services are. It means that it shares its CPU time with other services in this slice using the CPUWeight provided configuration, and this slice shares CPU time with other slices depending on their configuration.

The CPU shares configuration for the system slice and user slice is:

```
% cat /sys/fs/cgroup/cpu/system.slice/cpu.shares

1024  

% cat /sys/fs/cgroup/cpu/user.slice/cpu.shares

1024 
```

Both slices has the same share number configured. As such if each uses all its CPU time, each will get 50% of CPU time. In the BOINC case, the user only gets 50% of CPU time!

One solution is to create a slice dedicated to BOINC, and to allocate a low priority to this new slice.

We do so by creating the slice configuration in the `/etc/systemd/system/lowprio.slice` file with the following content:

```
[Unit]  

Description=Slice with low CPU priority  

DefaultDependencies=no  

Before=slices.target  

[Slice]  

CPUWeight=1
```

Then we override the BOINC service configuration by creating the `/etc/systemd/system/boinc.service` file as such:

```
.include /usr/lib/systemd/system/boinc.service  

[Service]  

Slice=lowprio.slice  
```

Finally we reload systemd configuration and restart the BOINC service:

```
% sudo systemctl daemon-reload  

% sudo systemctl restart boinc.service  
```

We can now run the same experiment as before, and monitor with `systemd-cgtop` CPU usage per group:

```
Control Group Procs %CPU Memory Input/s Output/s  

/ 72 558.4 5.1G - -  

/lowprio.slice 8 520.0 - - -  

/user.slice 47 33.8 - - -  

/system.slice 16 2.9 - - -  

/init.scope 1 - - - -  

/lowprio.slice/boinc.service 8 - - - -  
```

We notice that boinc.service has no reported CPU time usage. I removed the CPUWeight attribute for the service, which disables the CPU time tracking for its cgroup. This is not an issue as its tracked by its parent group lowprio.slice, which uses around 558% CPU time.

We start the experiment again by running `` % for i in `seq 8`; do sha512sum /dev/zero&;done ``.

This time cgtop shows that most CPU time is used by the slice grouping user sessions user.slice:

```
Control Group Procs %CPU Memory Input/s Output/s  

/ 80 800.0 5.4G - -  

/user.slice 55 784.4 - - -  

/lowprio.slice 8 10.8 - - -  

/system.slice 16 4.0 - - -  

/init.scope 1 - - - -  

/lowprio.slice/boinc.service 8 - - - -  
```  

We notice that the system.slice has also some usage as the Xorg display server is started in this slice, and I am playing a video while testing. We so need enough priority for the system slice to prevent impacting display latency.

To conclude we can note that using cgroups and systemd has mode CPU ressource management more complex. It took me some effort to understand how to get BOINC expected behavior of not having impact on any other usage of the system.