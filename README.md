# KubeSEC

# Install Kubernetes Cluster using kubeadm

<img src="Kubernetes.png" width="50%">

Follow this documentation to set up a Kubernetes cluster on __Ubuntu 20.04 LTS__.

This documentation guides you in setting up a cluster with one master node and one worker node.

## Assumptions
|Role|FQDN|IP|OS|RAM|CPU|
|----|----|----|----|----|----|
|Master|kmaster.example.com|172.16.16.100|Ubuntu 20.04|2G|2|
|Worker|kworker.example.com|172.16.16.101|Ubuntu 20.04|1G|1|

## On both Kmaster and Kworker
##### Login as `root` user
```
sudo su -
```
Perform all the commands as root user unless otherwise specified
##### Disable Firewall
```
ufw disable
```
##### Disable swap
```
swapoff -a; sed -i '/swap/d' /etc/fstab
```
##### Update sysctl settings for Kubernetes networking
```
cat >>/etc/sysctl.d/kubernetes.conf<<EOF
net.bridge.bridge-nf-call-ip6tables = 1
net.bridge.bridge-nf-call-iptables = 1
EOF
sysctl --system
```
##### Install docker engine
```
{
  apt install -y apt-transport-https ca-certificates curl gnupg-agent software-properties-common
  curl -fsSL https://download.docker.com/linux/ubuntu/gpg | apt-key add -
  add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
  apt update
  apt install -y docker-ce=5:19.03.10~3-0~ubuntu-focal containerd.io
}
```
### Kubernetes Setup
##### Add Apt repository
```
{
  curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key add -
  echo "deb https://apt.kubernetes.io/ kubernetes-xenial main" > /etc/apt/sources.list.d/kubernetes.list
}
```
##### Install Kubernetes components
```
apt update && apt install -y kubeadm=1.18.5-00 kubelet=1.18.5-00 kubectl=1.18.5-00
```
##### In case you are using LXC containers for Kubernetes nodes
Hack required to provision K8s v1.15+ in LXC containers
```
{
  mknod /dev/kmsg c 1 11
  echo '#!/bin/sh -e' >> /etc/rc.local
  echo 'mknod /dev/kmsg c 1 11' >> /etc/rc.local
  chmod +x /etc/rc.local
}
```

## On kmaster
##### Initialize Kubernetes Cluster
Update the below command with the ip address of kmaster
```
kubeadm init --apiserver-advertise-address=172.16.16.100 --pod-network-cidr=192.168.0.0/16  --ignore-preflight-errors=all
```
##### Deploy Calico network
```
kubectl --kubeconfig=/etc/kubernetes/admin.conf create -f https://docs.projectcalico.org/v3.14/manifests/calico.yaml
```

##### Cluster join command
```
kubeadm token create --print-join-command
```

##### To be able to run kubectl commands as non-root user
If you want to be able to run kubectl commands as non-root user, then as a non-root user perform these
```
mkdir -p $HOME/.kube
sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
sudo chown $(id -u):$(id -g) $HOME/.kube/config
```

## On Kworker
##### Join the cluster
Use the output from __kubeadm token create__ command in previous step from the master server and run here.

## Verifying the cluster (On kmaster)
##### Get Nodes status
```
kubectl get nodes
```
##### Get component status
```
kubectl get cs
```

Have Fun!!


#Mod Security Setup 

<img src="modsec.png" width="50%">

Libmodsecurity is one component of the ModSecurity v3 project. The library
codebase serves as an interface to ModSecurity Connectors taking in web traffic
and applying traditional ModSecurity processing. In general, it provides the
capability to load/interpret rules written in the ModSecurity SecRules format
and apply them to HTTP content provided by your application via Connectors.

If you are looking for ModSecurity for Apache (aka ModSecurity v2.x), it is still under maintenance and available:
[here](https://github.com/owasp-modsecurity/ModSecurity/tree/v2/master).

### What is the difference between this project and the old ModSecurity (v2.x.x)?

* All Apache dependencies have been removed
* Higher performance
* New features
* New architecture

Libmodsecurity is a complete rewrite of the ModSecurity platform. When it was first devised the ModSecurity project started as just an Apache module. Over time the project has been extended, due to popular demand, to support other platforms including (but not limited to) Nginx and IIS. In order to provide for the growing demand for additional platform support, it has became necessary to remove the Apache dependencies underlying this project, making it more platform independent.

As a result of this goal we have rearchitected Libmodsecurity such that it is no longer dependent on the Apache web server (both at compilation and during runtime). One side effect of this is that across all platforms users can expect increased performance. Additionally, we have taken this opportunity to lay the groundwork for some new features that users have been long seeking. For example we are looking to natively support auditlogs in the JSON format, along with a host of other functionality in future versions.


### It is no longer just a module.

The 'ModSecurity' branch no longer contains the traditional module logic (for Nginx, Apache, and IIS) that has traditionally been packaged all together. Instead, this branch only contains the library portion (libmodsecurity) for this project. This library is consumed by what we have termed 'Connectors' these connectors will interface with your webserver and provide the library with a common format that it understands. Each of these connectors is maintained as a separate GitHub project. For instance, the Nginx connector is supplied by the ModSecurity-nginx project (https://github.com/owasp-modsecurity/ModSecurity-nginx).

Keeping these connectors separated allows each project to have different release cycles, issues and development trees. Additionally, it means that when you install ModSecurity v3 you only get exactly what you need, no extras you won't be using.

# Compilation

Before starting the compilation process, make sure that you have all the
dependencies in place. Read the subsection “Dependencies”  for further
information.

After the compilation make sure that there are no issues on your
build/platform. We strongly recommend the utilization of the unit tests and
regression tests. These test utilities are located under the subfolder ‘tests’.

As a dynamic library, don’t forget that libmodsecurity must be installed to a location (folder) where you OS will be looking for dynamic libraries.



### Unix (Linux, MacOS, FreeBSD, …)

On unix the project uses autotools to help the compilation process.

```shell
$ ./build.sh
$ ./configure
$ make
$ sudo make install
```

Details on distribution specific builds can be found in our Wiki:
[Compilation Recipes](https://github.com/owasp-modsecurity/ModSecurity/wiki/Compilation-recipes)

### Windows

Windows build is not ready yet.


## Dependencies

This library is written in C++ using the C++17 standards. It also uses Flex
and Yacc to produce the “Sec Rules Language” parser. Other, mandatory dependencies include YAJL, as ModSecurity uses JSON for producing logs and its testing framework, libpcre (not yet mandatory) for processing regular expressions in SecRules, and libXML2 (not yet mandatory) which is used for parsing XML requests.

All others dependencies are related to operators specified within SecRules or configuration directives and may not be required for compilation. A short list of such dependencies is as follows:

* libinjection is needed for the operator @detectXSS and @detectSQL
* curl is needed for the directive SecRemoteRules.

If those libraries are missing ModSecurity will be compiled without the support for the operator @detectXSS and the configuration directive SecRemoteRules.

# Library documentation

The library documentation is written within the code in Doxygen format. To generate this documentation, please use the doxygen utility with the provided configuration file, “doxygen.cfg”, located with the "doc/" subfolder. This will generate HTML formatted documentation including usage examples.

# Library utilization

The library provides a C++ and C interface. Some resources are currently only
available via the C++ interface, for instance, the capability to create custom logging
mechanism (see the regression test to check for how those logging mechanism works).
The objective is to have both APIs (C, C++) providing the same functionality,
if you find an aspect of the API that is missing via a particular interface, please open an issue.

Inside the subfolder examples, there are simple examples on how to use the API.
Below some are illustrated:

###  Simple example using C++

```c++
using ModSecurity::ModSecurity;
using ModSecurity::Rules;
using ModSecurity::Transaction;

ModSecurity *modsec;
ModSecurity::Rules *rules;

modsec = new ModSecurity();

rules = new Rules();

rules->loadFromUri(rules_file);

Transaction *modsecTransaction = new Transaction(modsec, rules);

modsecTransaction->processConnection("127.0.0.1");
if (modsecTransaction->intervention()) {
   std::cout << "There is an intervention" << std::endl;
}
```

### Simple example using C

```c
#include "modsecurity/modsecurity.h"
#include "modsecurity/transaction.h"


char main_rule_uri[] = "basic_rules.conf";

int main (int argc, char **argv)
{
    ModSecurity *modsec = NULL;
    Transaction *transaction = NULL;
    Rules *rules = NULL;

    modsec = msc_init();

    rules = msc_create_rules_set();
    msc_rules_add_file(rules, main_rule_uri);

    transaction = msc_new_transaction(modsec, rules);

    msc_process_connection(transaction, "127.0.0.1");
    msc_process_uri(transaction, "http://www.modsecurity.org/test?key1=value1&key2=value2&key3=value3&test=args&test=test");
    msc_process_request_headers(transaction);
    msc_process_request_body(transaction);
    msc_process_response_headers(transaction);
    msc_process_response_body(transaction);

    return 0;
}

```

 Check the list of items by performing a grep:

```
$ cd /path/to/modsecurity-nginx
$ egrep -Rin "TODO|FIXME" -R *
```



