BountyFunding Trac Plugin
===================================

Requirements
------------
* Python (2.7)
* Message Transfer Agent, such as Postfix or Exim
* Trac (1.0+)
* Recommended: pip and virtualenv
* Python packages listed in requirements.txt file

Installation
------------
### Download BountyFunding
Download the archive from github [master.zip](https://github.com/bountyfunding/bountyfunding/archive/master.zip) or clone the repository:
	
	git clone https://github.com/bountyfunding/bountyfunding.git

### Install Python Libraries
Run below command to install python dependencies if needed. I use [pip](http://www.pip-installer.org), but they could also be installed with easy_install, packaging system native to your operating system or directly from source. You may consider using [virtualenv](http://www.virtualenv.org) to isolate the installation from other Python applications.

* Install requirements

		pip install -r requirements.txt

### Install and Configure Trac
Install Trac, at least version 1.0 is required. Make the following changes to the configuration:

* Configure [Message Transfer Agent](https://en.wikipedia.org/wiki/Mail_transfer_agent) such as [Postfix](http://www.postfix.org/) or [Exim](http://www.exim.org/). If you are using Linux one of them is probably already installed on your computer. To make sure it's running you can try connect to it using telnet:

		telnet localhost 25

* Enable mailing in Trac - it can be tested by creating an issue and completing it by a different user - you should receive a notification  		

		[notification]
		...
		smtp_enabled = yes
		...
		smtp_from = <valid email address with domain name>
		...

* All users or developers that want to use BountyFunding need to specify their emails as notifications and speedy replies are very important
* Install Trac [Account Manager Plugin](http://trac-hacks.org/wiki/AccountManagerPlugin) to allow new user registration. Alternatively use my lightweight [SimpleRegister](https://github.com/loomchild/simpleregister) plugin or just include an information how to register on your Trac wiki.
* In case of problems you may consider enabling logging (to stderr or file) and increasing logging level to diagnose possible problems with configuration (in trac.ini):

		[logging]
		...
		log_level = DEBUG
		log_type = stderr

### Deploy Trac Plugin
* Change directory

		cd plugin/trac

* Build Python egg
	
		./setup.py bdist_egg

* Put it in you Trac plugins directory

		cp dist/BountyFunding*.egg <trac_home>/plugins

* Configure the plugin - add the following to trac.ini in appriopriate sections:
  
  		[components]
		bountyfunding.* = enabled

		[ticket-custom]
		bounty = text
		bounty.label = Bounty
		
		[bountyfunding]
		url = http://localhost:8080

* You can add new bounty field to your existing reports using [TracQuery](http://trac.edgewall.org/wiki/TracQuery) or [TracReports](http://trac.edgewall.org/wiki/TracReports). Due to technical limitations this field can be only sorted in alphabetical order which is not ideal - there is a small workaround for TracReports to cast it as INTEGER. For example Active Tickets By Milestone report can look like this:
		
		SELECT p.value AS __color__,
		   'Milestone '||milestone AS __group__,
		   id AS ticket, summary, component, version, t.type AS type,
		   owner, status,
		   time AS created,
		   changetime AS _changetime, description AS _description,
		   reporter AS _reporter,
		   CAST(c.value AS INTEGER) AS bounty
		FROM ticket t
		LEFT JOIN enum p ON p.name = t.priority AND p.type = 'priority'
		LEFT OUTER JOIN ticket_custom c ON t.id = c.ticket AND c.name = 'bounty'
		WHERE status <> 'closed'
		ORDER BY (milestone IS NULL),milestone, CAST(p.value AS integer), t.type, time

* You can also change the mapping between Trac statuses and bountyfunding statuses. This controls when user can pledge, confirm the payment and validate the ticket. One variation to simplify the funding process could be to allow users to confirm the payment when the ticket is accepted, without waiting for it to be assigned to specific developer - this can be achieved by moving 'accepted' Trac status to status_mapping_started setting. See below the default configuration:

		[bountyfunding]
		...
		status_mapping_ready = new, accepted, reopened
		status_mapping_started = assigned
		status_mapping_completed = closed

* If you are connecting multiple trac instances to a single BountyFunding webapp, set an access token:
  	
		[bountyfunding]
		...
		token = <mytoken>

* Restart Trac
* To check if plugin has been installed properly go to Trac Admin / Plugins. Also you should see Bounty field on each ticket. It's also a good idea to check if email notifications are sent - create a ticket, sponsor it by one user and assign it or complete it by another user - first user should receive a notification. 

Development
-----------

### Requirements
For development you will need all python packages listed in [requirements-dev.txt](requirements-dev.txt):
	
		pip install -r requirements-dev.txt

### Tips
* During Trac plugin development it's useful to install a plugin link instead of deploying a full egg after every chage (however, trac still needs to be restarted). To do it execute (see [Trac Plugin Development](http://trac.edgewall.org/wiki/TracDev/PluginDevelopment) for more details):

		cd plugin/trac
		./setup.py develop -mxd <trac_home>/plugins
* When Trac and BountyFunding webapp tickets become out of sync (due to manual modification, temporary webapp downtime, etc.), go to the following URL: http://\<trac_url\>/bountyfunding/sync - this will refresh local Trac cache. This operation will be automated in the future.
