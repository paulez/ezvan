Title: BOINC, systemd and Linux process priority
Date: 2018-12-05 00:00
Author: Paul
Tags: Libre, Linux, systemd, BOINC
Slug: boinc-systemd-et-priorite-des-processus-sous-linux
Lang: en

I've recently started to run [BOINC](https://boinc.berkeley.edu/) in my computer again. It is a nice way to donate computing capacity to research projects.

BOINC principle is to only use unused ressources of my computer. It does so be giving the lowest priority to computing processes. On Linux this is done by setting the highest [nice](https://fr.wikipedia.org/wiki/Nice_(Unix)) value to processes launched by BOINC, which is 19. The highest the nice value is, the least the process has priority.

19 is the idle priority, which means it allows using only CPU time which is not used by any process with higher priority. It is equivalent to use only unused resources of the system.

This setup was working fine for long on Linux. But I recently noticed that BOINC seemed to use more resources that what it should, as some applications were slower to run than usual. I tried to verify that. A simple way to do so is try using all computer ressources, and ensure they are available.

To so I launched 8 times (as my computer has 8 logical processing units) a command which uses all available CPU time.

`` for i in `seq 8`; do sha512sum /dev/zero&;done ``

By observing CPU using with the top command, I realize that each sha512sum process only gets 50% of CPU time. Moreover the "ni" column in top shows a 50% usage for lowest priority processes. It should be 0!

What is going on ?

Process priority management has become more complex in Linux since [cgroups](https://fr.wikipedia.org/wiki/Cgroups), or control groups, were introduced.
These groups allow grouping kernel resources and controlling them. As such it is possible to limit the CPU time used by a group of processes.

This introduces a new hierarchy to manage process priority. In my case BOINC processes were always using a minimum of 50% CPU time as CPU time is shared equitably between groups, independently of each process priority.

This type of mechanism has been introduced as it was easy to use bigger share of CPU time by launching a lot of processes. By managing priorities on group of processes this problem is avoided.

In this case I want that the group containing BOINC processes to be have the lowest priority. Those groups can be configured by the initialization system [systemd](https://en.wikipedia.org/wiki/Systemd) which manages system services and user sessions amongst other things. It starts each service processes in separate groups, and does the same for user sessions. We can just tell systemd to give the lowest priority to the BOINC group:

`sudo systemctl set-property boinc.service CPUWeight=1`

After running this command, I ran again my experiment. This time my test processes each used 100% of CPU time.
BOINC doesn't slow down my computer anymore!