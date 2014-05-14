Debian Packaging
****************

See debian's `New Maintainer Gudie <https://www.debian.org/doc/manuals/maint-guide/index.en.html`_ for an introduction to debian packaging.
The following has some notes and specific details on more involved bits.

Debian packaging is controlled by a number of files in the :directory:`debian` directory.

There are serveral required files:
   - control: This file has metadata about the source package as well as any binary packages.
   - changelog
   - compat: This specifies the debhelper compatibility level. It should contain ``9``.
     This is currently the most recent stable compatibility level.
     It isn't strictly required but debhelper makes the :file:`debian/rules` much shorter.
   - rules: This file has instructions for building the package.
     Using debhelper, the minimal file looks as follows::

        #!/usr/bin/make -f

	export DH_ALWAYS_EXCLUDE=flocker/local

	%:
		dh $@


upstart
=======

To install an upstart service for a package, include it as :file:`debian/<package>.upstart`.


debconf
=======

Debconf is a tools for providing initial configuration for deb packages.
Debconf configuration can be provided from cloud-init, or a preseed file for bare-metal installation.

This shouldn't be the primary method of configuration, but may be useful for getting people running with a simple configuration.


Example
-------

   1. Add a script to prompt for configuration variables (:file:`flocker-buildslave`)::

         #!/bin/sh -e

         # Source debconf library.
         /usr/share/debconf/confmodule

         db_input critical flocker-buildslave/slavename || true
         db_go

         db_stop

      This can also be written in python [1]_::

         #!/usr/bin/python

         from debconf import runFrontEnd, Debconf, CRITICIAL

         runFrontEnd()

         db = Debconf()
         db.input(CRITICAL, 'flocker-buildslave/slavename')
         db.go()
         db.stop()

   2. Add templates for how the question should be displayed to users (:file:`debian/flocker-buildslave.template`)::

         Template: flocker-buildslave/slavename
         Type: string
         Description: What is the name of this slave?

   3. Add a postinit script to use the debconf settings (:file:`debian/flocker-buildslave.postinst`)::

         #!/bin/sh -e

         . /usr/share/debconf/confmodule

         db_get flocker-buildslave/slavename
	 SLAVENAME=$RET

	 # Do something with the result
	 # XXX This should probably check if this is running from dpkg-reconfigure
	 if [ -e /tmp/slavename ]; then
           echo $SLAVENAME > /tmp/slavename
	 fi

	 db_stop

         #DEBHLPER#

      This file needs to have a ``#DEBHELPER#`` line that will be substituted with sh snippets from various debhelper commands.

.. [1] https://mknowles.com.au/wordpress/2009/10/09/python-debconf-configuration-by-example/


config-package-dev
==================

A `package <http://debathena.mit.edu/config-package-dev/>`_ from MIT that helps packaging deployment specific configuration files that are typically provided by distribution packages.
It does this by:

   1. using `dpkg-divert` to move the distribution proivded file out of the way (with a ``.<prefix>-orig>`` extension)
   2. Installing the new config file with a ``.<prefix>`` extension.
   3. Creating a symlink from the real name to the ``.<prefix>`` extension.

This is useful when there is a specific static configuraiton that needs to be done,
but probably less useful if the configuration file needs some user-input added to it.


Example
-------

To create a package that installs a custom sshd_config:

   1. Add a stanza for the package in :file:`debian/control`::

         Package: flocker-ssh-port
         Architecture: all
         Depends: openssh-server, ${misc:Depends}
         Provides: ${diverted-files}
         Conflicts: ${diverted-files}
         Description: Custom ssh configuration

      and add ``config-package-dev (>= 5.0)`` to the ``Build-Depends`` line there.

   2. Indicate the file that should be replaced (:file:`debian/flocker-ssh-port.displace`)::

         /etc/ssh/sshd_flocker.config

   3. Create the new configuration file that should be installed (:file:`sshd_config.flocker`)::

         Port 2222
         PermitRootLogin no
         # ...

   4. Indicate that the file should be installed (:file:`debian/flocker-ssh-port.install`)::

         sshd_config.flocker etc/ssh

   5. Add ``config-package`` to the list of debhelper addons in :file:`debian/rules`::

	dh $@ --with config-package

Creating Users
==============

To create a user in a package, include something like the following in the postinst script::

   if ! getent passwd flocker-buildslave>/dev/null; then
       adduser --quiet \
           --system \
           --disabled-login \
           --disabled-password \
           --no-create-home \
           --group \
           --gecos "Flocker Buildslave" \
           --home /srv/flocker-buildslave \
           flocker-buildslave
       chown flocker-buildslave:flocker-buildslave /srv/flocker-buildslave /srv/flocker-buildslave/slave
   fi


References
----------
- https://www.debian.org/doc/debian-policy/ch-files.html#s-permissions-owners
- https://wiki.debian.org/AccountHandlingInMaintainerScripts


Building Packages
=================

- dpkg-buildpackage
  debuild = dpkg-buildpkg + lintian + signing
- pdebuild /cowbuilder

  pbuilder is a tool for creating chroots and building packages in them that just have the declared dependencies installed.
  pdebuilder used pbuilder to build a debian


Signing Packages
================

Need to see if we can safely automate this.
We need to sign packages for an archive of them to be built automatically


Package Archive
===============
http://upsilon.cc/~zack/blog/posts/2009/04/howto:_uploading_to_people.d.o_using_dput/


Cloud Init
**********

Cloud Init is a package installed on most (ubuntu?) cloud images that reads instance metadata and perform initialization.
It deals with generating fresh ssh host keys.
It can also be used to add new package repositories, as well as configure (via debconf) and install packages.

For example, providing the following user-data::

   #cloud-config
   apt_sources:
     - source: "deb http://archive.example.net/apt flocker-trusty/"
   debconf_selections: |
     flocker-buildslave flocker-buildslave/slavename string the-slave
     flocker-buildslave flocker-buildslave/password password the-password
   packages:
     - flocker-buildslave

will install a package from a custom repository and configure it.
