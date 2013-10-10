# BountyFunding - Open-Source Bounty Funding Platform
===================================
Website (including live demo): [http://bountyfunding.org](http://bountyfunding.org)

Introduction
------------
BountyFunding is a bounty funding platform designed specifically for Free / Open-Source Software. It allows users to collectively sponsor most wanted features / bugfixes, and gives developers another source of income or maybe even a business model. Currently BountyFunding only integrates with Trac, support for other issue tracking systems will be developed soon.
 
Requirements
------------
* Python (2.7)
* Database (SQLite / MySQL / PostgreSQL, anything supported SQLAlchemy)
* Message Transfer Agent, such as Postfix or Exim
* Trac (1.0+)
* All python packages listed in [requirements.txt](requirements.txt)
* For development: all python packages listed in [requirements-dev.txt](requirements-dev.txt)
* Recommended: pip and virtualenv

Installation
------------

### Install Python Libraries
Run below commands to install python dependencies if needed. I use [pip](http://www.pip-installer.org), but they could also be installed with easy_install, packaging system native to your operating system or directly from source. You may consider using [virtualenv](http://www.virtualenv.org) to isolate the installation from other Python applications.

* Install requirements

		pip install -r requirements.txt

* If you are a developer install development requirements instead

		pip install -r requirements-dev.txt

### Install and Configure Trac
Install Trac, at least version 1.0 is required. Make the following changes to the configuration:

* Configure [Message Transfer Agent](https://en.wikipedia.org/wiki/Mail_transfer_agent) such as [Postfix](http://www.postfix.org/) or [Exim](http://www.exim.org/). If you are using Linux one of them is probably already installed on your computer. To make sure it's running you can try connect to it using telnet:

		telnet localhost 25

* Enable mailing in Trac - it can be tested by creating an issue and completing it by a different user - you should receive a notification  		

		[notification]
		...
		smtp_enabled = yes

* All users or developers that want to use BountyFunding need to specify their emails as notifications and speedy replies are very important
* In case of problems you may consider enabling logging (to stderr or file) and increasing logging level to diagnose possible problems with configuration (in trac.ini):

		[logging]
		...
		log_level = DEBUG
		log_type = stderr

### Download BountyFunding
Download the archive from github [master.zip](https://github.com/bountyfunding/bountyfunding/archive/master.zip) or clone the repository:
	
	git clone https://github.com/bountyfunding/bountyfunding.git

### Deploy Trac Plugin
* Build Python egg
	
		cd plugins/bountyfunding_api_plugin/src
		./setup.py bdist_egg

* Put it in you Trac plugins directory

		cp dist/BountyFunding*.egg /<trac_home>/plugins

* Restart Trac
* To check if plugin has been installed properly go to Trac Admin / Plugins. Also you should see Bounty field on each ticket. It's also a good idea to check if email notifications are sent - create a ticket, sponsor it by one user and assign it or complete it by another user - first user should receive a notification. 

### Deploy API
* Run the API

		src/bountyfunding_api.py >& ../log/bountyfunding_api.log &

Development
-----------

### Tips
* During Trac plugin development it's useful to install a plugin link instead of deploying a full egg after every chage (however, trac still needs to be restarted). To do it execute (see [Trac Plugin Development](http://trac.edgewall.org/wiki/TracDev/PluginDevelopment) for more details):

		cd plugins/bountyfunding_api_plugin/src
		./setup.py develop -mxd /<trac_home>/plugins
