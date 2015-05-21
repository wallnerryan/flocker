==================
Installing Flocker
==================

As a user of Flocker you will need to install the ``flocker-cli`` package which provides command line tools to control the cluster.
This should be installed on a machine with SSH credentials to control the cluster nodes
(e.g., if you use our Vagrant setup then the machine which is running Vagrant).

There is also a ``clusterhq-flocker-node`` package which is installed on each node in the cluster.
It contains the services that need to run on each node.

.. note:: The ``clusterhq-flocker-node`` package is pre-installed by the :doc:`Vagrant configuration in the tutorial <./tutorial/vagrant-setup>`.

.. note:: If you're interested in developing Flocker (as opposed to simply using it) see :doc:`../gettinginvolved/contributing`.

.. _installing-flocker-cli:

Installing ``flocker-cli``
==========================

Linux
-----

Before you install ``flocker-cli`` you will need a compiler, Python 2.7, and the ``virtualenv`` Python utility installed.
On Fedora 20 you can install these by running:

.. code-block:: console

   alice@mercury:~$ sudo yum install @buildsys-build python python-devel python-virtualenv

On Ubuntu or Debian you can run:

.. code-block:: console

   alice@mercury:~$ sudo apt-get install gcc python2.7 python-virtualenv python2.7-dev

Then run the following script to install ``flocker-cli``:

:version-download:`linux-install.sh.template`

.. version-literalinclude:: linux-install.sh.template
   :language: sh

Save the script to a file and then run it:

.. code-block:: console

   alice@mercury:~$ sh linux-install.sh
   ...
   alice@mercury:~$

The ``flocker-deploy`` command line program will now be available in ``flocker-tutorial/bin/``:

.. version-code-block:: console

   alice@mercury:~$ cd flocker-tutorial
   alice@mercury:~/flocker-tutorial$ bin/flocker-deploy --version
   |latest-installable|
   alice@mercury:~/flocker-tutorial$

If you want to omit the prefix path you can add the appropriate directory to your ``$PATH``.
You'll need to do this every time you start a new shell.

.. version-code-block:: console

   alice@mercury:~/flocker-tutorial$ export PATH="${PATH:+${PATH}:}${PWD}/bin"
   alice@mercury:~/flocker-tutorial$ flocker-deploy --version
   |latest-installable|
   alice@mercury:~/flocker-tutorial$

OS X
----

Install the `Homebrew`_ package manager.

Make sure Homebrew has no issues:

.. code-block:: console

   alice@mercury:~$ brew doctor
   ...
   alice@mercury:~$

Fix anything which ``brew doctor`` recommends that you fix by following the instructions it outputs.

Add the ``ClusterHQ/tap`` tap to Homebrew and install ``flocker``:

.. task:: test_homebrew flocker-|latest-installable|
   :prompt: alice@mercury:~$

You can see the Homebrew recipe in the `homebrew-tap`_ repository.

The ``flocker-deploy`` command line program will now be available:

.. version-code-block:: console

   alice@mercury:~$ flocker-deploy --version
   |latest-installable|
   alice@mercury:~$

.. _Homebrew: http://brew.sh
.. _homebrew-tap: https://github.com/ClusterHQ/homebrew-tap


.. _installing-flocker-node:

Installing ``clusterhq-flocker-node``
=====================================

There are a number of ways to install Flocker.

These easiest way to get Flocker going is to use our vagrant configuration.

- :ref:`Vagrant <vagrant-install>`

It is also possible to deploy Flocker in the cloud, on a number of different providers.

- :ref:`Using Amazon Web Services <aws-install>`
- :ref:`Using Rackspace <rackspace-install>`

It is also possible to install Flocker on any Fedora 20, CentOS 7, or Ubuntu 14.04 machine.

- :ref:`Installing on Fedora 20 <fedora-20-install>`
- :ref:`Installing on CentOS 7 <centos-7-install>`
- :ref:`Installing on Ubuntu 14.04 <ubuntu-14.04-install>`


.. _vagrant-install:

Vagrant
-------

The easiest way to get Flocker going on a cluster is to run it on local virtual machines using the :doc:`Vagrant configuration in the tutorial <./tutorial/vagrant-setup>`.
You can therefore skip this section unless you want to run Flocker on a cluster you setup yourself.

.. warning:: These instructions describe the installation of ``clusterhq-flocker-node`` on a Fedora 20 operating system.
             This is the only supported node operating system right now.


.. _aws-install:

Using Amazon Web Services
-------------------------

.. note:: If you are not familiar with EC2 you may want to `read more about the terminology and concepts <https://fedoraproject.org/wiki/User:Gholms/EC2_Primer>`_ used in this document.
          You can also refer to `the full documentation for interacting with EC2 from Amazon Web Services <http://docs.amazonwebservices.com/AWSEC2/latest/GettingStartedGuide/>`_.

#. Choose a nearby region and use the link to it below to access the EC2 Launch Wizard

   * `Asia Pacific (Singapore) <https://console.aws.amazon.com/ec2/v2/home?region=ap-southeast-1#LaunchInstanceWizard:ami=ami-6ceebe3e>`_
   * `Asia Pacific (Sydney) <https://console.aws.amazon.com/ec2/v2/home?region=ap-southeast-2#LaunchInstanceWizard:ami=ami-eba038d1>`_
   * `Asia Pacific (Tokyo) <https://console.aws.amazon.com/ec2/v2/home?region=ap-northeast-1#LaunchInstanceWizard:ami=ami-9583fd94>`_
   * `EU (Ireland) <https://console.aws.amazon.com/ec2/v2/home?region=eu-west-1#LaunchInstanceWizard:ami=ami-a5ad56d2>`_
   * `South America (Sao Paulo) <https://console.aws.amazon.com/ec2/v2/home?region=sa-east-1#LaunchInstanceWizard:ami=ami-2345e73e>`_
   * `US East (Northern Virginia) <https://console.aws.amazon.com/ec2/v2/home?region=us-east-1#LaunchInstanceWizard:ami=ami-21362b48>`_
   * `US West (Northern California) <https://console.aws.amazon.com/ec2/v2/home?region=us-west-1#LaunchInstanceWizard:ami=ami-f8f1c8bd>`_
   * `US West (Oregon) <https://console.aws.amazon.com/ec2/v2/home?region=us-west-2#LaunchInstanceWizard:ami=ami-cc8de6fc>`_

#. Configure the instance

   Complete the configuration wizard; in general the default configuration should suffice.
   However, we do recommend at least the ``m3.large`` instance size.

   If you wish to customize the instance's security settings make sure to permit SSH access both from the intended client machine (for example, your laptop) and from any other instances on which you plan to install ``clusterhq-flocker-node``.

   .. warning::

      Keep in mind that (quite reasonably) the default security settings firewall off all ports other than SSH.
      E.g. if you run the tutorial you won't be able to access MongoDB over the Internet, nor will other nodes in the cluster.
      You can choose to expose these ports but keep in mind the consequences of exposing unsecured services to the Internet.
      Links between nodes will also use public ports but you can configure the AWS VPC to allow network connections between nodes and disallow them from the Internet.

#. Add the *Key* to your local key chain (download it from the AWS web interface first if necessary):

   .. prompt:: bash alice@mercury:~$

      mv ~/Downloads/my-instance.pem ~/.ssh/
      chmod 600 ~/.ssh/my-instance.pem
      ssh-add ~/.ssh/my-instance.pem

#. Look up the public DNS name or public IP address of the new instance and, depending on the OS, log in as user ``fedora``, ``centos``, or ``ubuntu`` e.g.:

   .. prompt:: bash alice@mercury:~$

      ssh fedora@ec2-AA-BB-CC-DD.eu-west-1.compute.amazonaws.com

#. Allow SSH access for the ``root`` user, then log out.

   .. task:: install_ssh_key
      :prompt: [user@aws]$

#. Log back into the instances as user "root", e.g.:

   .. prompt:: bash alice@mercury:~$

      ssh root@ec2-AA-BB-CC-DD.eu-west-1.compute.amazonaws.com


#. Follow the operating system specific installation instructions below.


.. _rackspace-install:

Using Rackspace
---------------

Another way to get a Flocker cluster running is to use Rackspace.
You'll probably want to setup at least two nodes.

#. Create a new Cloud Server running Fedora 20

   * Visit https://mycloud.rackspace.com
   * Click "Create Server".
   * Choose the Fedora 20 Linux distribution as your image.
   * Choose a Flavor. We recommend at least "8 GB General Purpose v1".
   * Add your SSH key

#. SSH in

   You can find the IP in the Server Details page after it is created.

   .. prompt:: bash alice@mercury:~$

      ssh root@203.0.113.109

#. Follow the :ref:`generic Fedora 20 installation instructions <fedora-20-install>` below.

.. _fedora-20-install:

Installing on Fedora 20
-----------------------

.. note:: The following commands all need to be run as root on the machine where ``clusterhq-flocker-node`` will be running.

Now install the ``clusterhq-flocker-node`` package.
To install ``clusterhq-flocker-node`` on Fedora 20 you must install the RPM provided by the ClusterHQ repository.
The following commands will install the two repositories and the ``clusterhq-flocker-node`` package.
Paste them into a root console on the target node:

.. task:: install_flocker fedora-20
   :prompt: [root@node]#
   
Installing ``flocker-node`` will automatically install Docker, but the ``docker`` service may not have been enabled or started.
To enable and start Docker, run the following commands in a root console:

.. task:: enable_docker fedora-20
   :prompt: [root@fedora]#

Finally, you will need to run the ``flocker-ca`` tool that is installed as part of the CLI package.
This tool generates TLS certificates that are used to identify and authenticate the components of your cluster when they communicate, which you will need to copy over to your nodes. Please see the :ref:`cluster authentication <authentication>` instructions.

.. _centos-7-install:

Installing on CentOS 7
----------------------

.. note:: The following commands all need to be run as root on the machine where ``clusterhq-flocker-node`` will be running.

First disable SELinux.

.. task:: disable_selinux centos-7
   :prompt: [root@centos]#

.. note:: Flocker does not currently set the necessary SELinux context types on the filesystem mount points that it creates on nodes.
          This prevents Docker containers from accessing those filesystems as volumes.
          A future version of Flocker may provide a different integration strategy.
          See :issue:`619`.

Now install the ``flocker-node`` package.
To install ``flocker-node`` on CentOS 7 you must install the RPM provided by the ClusterHQ repository.
The following commands will install the two repositories and the ``flocker-node`` package.
Paste them into a root console on the target node:

.. task:: install_flocker centos-7
   :prompt: [root@node]#

Installing ``flocker-node`` will automatically install Docker, but the ``docker`` service may not have been enabled or started.
To enable and start Docker, run the following commands in a root console:

.. task:: enable_docker centos-7
   :prompt: [root@centos]#
   
Finally, you will need to run the ``flocker-ca`` tool that is installed as part of the CLI package.
This tool generates TLS certificates that are used to identify and authenticate the components of your cluster when they communicate, which you will need to copy over to your nodes. Please see the :ref:`cluster authentication <authentication>` instructions.

.. _ubuntu-14.04-install:

Installing on Ubuntu 14.04
--------------------------

.. note:: The following commands all need to be run as root on the machine where ``clusterhq-flocker-node`` will be running.

Setup the pre-requisite repositories and install the ``clusterhq-flocker-node`` package.

.. task:: install_flocker ubuntu-14.04
   :prompt: [root@ubuntu]#

.. _authentication:

Cluster Authentication Layer Configuration
------------------------------------------

Communication between the different parts of your cluster is secured and authenticated via TLS.
The Flocker CLI package includes the ``flocker-ca`` tool that is used to generate TLS certificate and key files that you will need to copy over to your nodes.

Once you have installed the ``flocker-node`` package, you will need to generate:

- A control service certificate and key file, to be copied over to the machine running your :doc:`control service <../advanced/architecture>`.
- A certificate and key file for each of your nodes, which you will also need to copy over to the nodes.

Both types of certificate will be signed by a certificate authority identifying your cluster, which is also generated using the ``flocker-ca`` tool.

Using the machine on which you installed the ``flocker-cli`` package, run the following command to generate your cluster's root certificate authority, replacing ``mycluster`` with any name you like to uniquely identify this cluster.

.. code-block:: console

    $ flocker-ca initialize mycluster
    Created cluster.key and cluster.crt. Please keep cluster.key secret, as anyone who can access it will be able to control your cluster.

You will find the files ``cluster.key`` and ``cluster.crt`` have been created in your working directory.
The file ``cluster.key`` should be kept only by the cluster administrator; it does not need to be copied anywhere.

.. warning::

   The cluster administrator needs this file to generate new control service, node and API certificates.
   The security of your cluster depends on this file remaining private.
   Do not lose the cluster private key file, or allow a copy to be obtained by any person other than the authorised cluster administrator.

You are now able to generate authentication certificates for the control service and each of your nodes.
To generate the control service certificate, run the following command from the same directory containing your authority certificate generated in the previous step.
Replace ``example.org`` with the hostname of your control service node; this hostname should match the one you will give to REST API clients.

.. code-block:: console

   $ flocker-ca create-control-certificate example.org
   Created control-example.org.crt. Copy it over to /etc/flocker/control-service.crt on your control service machine and make sure to chmod 0600 it.
   
You will need to copy both ``control-example.org.crt`` and ``control-example.org.key`` over to the node that is running your control service, to the directory ``/etc/flocker/`` and rename the files to ``control-service.crt`` and ``control-service.key`` respectively.
You should also copy the cluster's public certificate, the `cluster.crt` file.
On the server, the ``/etc/flocker`` directory and private key file should be set to secure permissions via ``chmod``:

.. code-block:: console

   root@mercury:~/$ chmod 0700 /etc/flocker
   root@mercury:~/$ chmod 0600 /etc/flocker/control-service.key

You should copy these files via a secure communication medium such as SSH, SCP or SFTP.

.. warning::

   Only copy the file ``cluster.crt`` to the control service and node machines, not the ``cluster.key`` file; this must kept only by the cluster administrator.

You will also need to generate authentication certificates for each of your nodes.
Do this by running the following command as many times as you have nodes; for example, if you have two nodes in your cluster, you will need to run this command twice.
This step should be followed for all nodes on the cluster, as well as the machine running the control service.
Run the command in the same directory containing the certificate authority files you generated in the first step.

.. code-block:: console

   $ flocker-ca create-node-certificate
   Created 8eab4b8d-c0a2-4ce2-80aa-0709277a9a7a.crt. Copy it over to /etc/flocker/node.crt on your node machine, and make sure to chmod 0600 it.

The actual certificate and key file names generated in this step will vary from the example above; when you run ``flocker-ca create-node-certificate``, a UUID for a node will be generated to uniquely identify it on the cluster and the files produced are named with that UUID.

As with the control service certificate, you should securely copy the generated certificate and key file over to your node, along with the `cluster.crt` certificate.
Copy the generated files to ``/etc/flocker/`` on the target node and name them ``node.crt`` and ``node.key``.
Perform the same ``chmod 600`` commands on ``node.key`` as you did for the control service in the instructions above.
The ``/etc/flocker/`` directory should be set to ``chmod 700``.

You can read more about how Flocker's authentication layer works in the :doc:`security and authentication guide <../advanced/security>`.

Post installation configuration
-------------------------------

Your firewall will need to allow access to the ports your applications are exposing.

.. warning::

   Keep in mind the consequences of exposing unsecured services to the Internet.
   Both applications with exposed ports and applications accessed via links will be accessible by anyone on the Internet.

To enable the Flocker control service on Fedora / CentOS
--------------------------------------------------------

.. task:: enable_flocker_control fedora-20
   :prompt: [root@control-node]#

The control service needs to accessible remotely.
To configure FirewallD to allow access to the control service REST API, and for agent connections:

.. task:: open_control_firewall fedora-20
   :prompt: [root@control-node]#

For more details on configuring the firewall, see Fedora's `FirewallD documentation <https://fedoraproject.org/wiki/FirewallD>`_.

On AWS, an external firewall is used instead, which will need to be configured similarly.

To start the agents on a node, a configuration file must exist on the node at ``/etc/flocker/agent.yml``.
This should be as follows, replacing ``${CONTROL_NODE}`` with the address of the control node.
The optional ``port`` variable is the port on the control node to connect to:

.. code-block:: yaml

   "version": 1
   "control-service":
      "hostname": "${CONTROL_NODE}"
      "port": 4524
	"dataset":
	  "backend": "zfs"

.. task:: enable_flocker_agent fedora-20 ${CONTROL_NODE}
   :prompt: [root@agent-node]#

To enable the Flocker control service on Ubuntu
-----------------------------------------------

.. task:: enable_flocker_control ubuntu-14.04
   :prompt: [root@control-node]#

The control service needs to accessible remotely.
To configure ``UFW`` to allow access to the control service REST API, and for agent connections:

.. task:: open_control_firewall ubuntu-14.04
   :prompt: [root@control-node]#

For more details on configuring the firewall, see Ubuntu's `UFW documentation <https://help.ubuntu.com/community/UFW>`_.

On AWS, an external firewall is used instead, which will need to be configured similarly.

To start the agents on a node, a configuration file must exist on the node at ``/etc/flocker/agent.yml``.
This should be as follows, replacing ``${CONTROL_NODE}`` with the address of the control node.
The optional ``port`` variable is the port on the control node to connect to:

.. code-block:: yaml

   "version": 1
   "control-service":
      "hostname": "${CONTROL_NODE}"
      "port": 4524
  	"dataset":
  	  "backend": "zfs"

.. task:: enable_flocker_agent ubuntu-14.04 ${CONTROL_NODE}
   :prompt: [root@agent-node]#

What to do next
---------------

You have now installed ``clusterhq-flocker-node`` and created a ZFS for it.

Next you may want to perform the steps in :doc:`the tutorial <./tutorial/moving-applications>`, to ensure that your nodes are correctly configured.
Replace the IP addresses in the ``deployment.yaml`` files with the IP address of your own nodes.
Keep in mind that the tutorial was designed with local virtual machines in mind, and results in an insecure environment.


ZFS Backend Configuration
-------------------------

The ZFS backend requires ZFS to be installed.


Installing ZFS on CentOS 7
..........................

Installing ZFS requires the kernel development headers for the running kernel.
Since CentOS doesn't provide easy access to old package versions,
the easiest way to get appropriate headers is to upgrade the kernel and install the headers.

.. task:: upgrade_kernel centos-7
   :prompt: [root@centos-7]#

You will need to reboot the node after updating the kernel.

.. prompt:: bash [root@aws]#

   shutdown -r now

You must also install the ZFS package repository.

.. task:: install_zfs centos-7
   :prompt: [root@centos-7]#


Installing ZFS on Ubuntu 14.04
..............................

.. task:: install_zfs ubuntu-14.04
   :prompt: [root@ubuntu-14.04]#


Creating a ZFS pool
...................

Flocker requires a ZFS pool named ``flocker``.
The following commands will create a 10 gigabyte ZFS pool backed by a file.
Paste them into a root console:

.. task:: create_flocker_pool_file
   :prompt: [root@node]#

.. note:: It is also possible to create the pool on a block device.

.. XXX: Document how to create a pool on a block device: https://clusterhq.atlassian.net/browse/FLOC-994

To support moving data with the ZFS backend, every node must be able to establish an SSH connection to all other nodes.
So ensure that the firewall allows access to TCP port 22 on each node from the every node's IP addresses.
