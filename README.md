GoAccess for DreamHost
======================

An easy to setup packaging of [GoAccess](https://goaccess.io) for use on [DreamHost](https://www.dreamhost.com) web-hosting
services (shared servers and VPS).

![GoAccess-DH Screenshot](screenshot.png)

Features:

- Automatically lists active web sites.
- Generate GoAccess reports based on current logs.
- Generate Reports for single or multiple sites.
- Entirely written in Bash CGI!

Notes:

- Reports use the avaiable raw logs, which DH default to 3 days. Sites can be configured to keep up to 30 days of raw logs in the [Site Statistics Panel](https://panel.dreamhost.com/index.cgi?tree=advanced.stats&).
- Reports are generated on the fly, so expect ~60 seconds of processing time per million requests.


Installation
------------

GoAccess-DH can be installed anywhere on a web site. It comes with a pre-built binary of GoAccess (see below for building from scratch).

- **Quick Install**
  
  Log in to a site's shell user (e.g. `ssh myuser@myhost.dreamhost.com`) and clone GoAccess-DH into the site's web directory. For example:
  
  ```
  git clone https://github.com/chuckhoupt/goaccess-dh.git ~/example.com/goaccess-dh
  ```
  
  Now visit `example.com/goaccess-dh/` to see stats for all the sites hosted under that shell user.

Further Configuration
---------------------

- **Secure Reports**

   Setup password protection for the `goaccess-dh` directory via
   [DH's Htaccess Panel](https://panel.dreamhost.com/index.cgi?tree=advanced.webdav&).

- **Build from Source**

  If you'd prefer to build your own binary, log into a shell user and clone GoAccess-DH into `example.com`'s web directory:

  ```
  git clone --recurse-submodules https://github.com/chuckhoupt/goaccess-dh.git ~/example.com/goaccess-dh
  ```

  Run Make to configure and compile GoAccess:
   
  ```
  make -C ~/example.com/goaccess-dh
  ```
  

Related Projects
----------------

These projects have a similar intent to GoAccess-DH, but require root access:

- [gopanel - Multi-site Web Analytics Menu for goaccess](https://github.com/neocogent/gopanel)
- [Using GoAccess with PHP](https://gist.github.com/Jiab77/b7eff1dc6c0996b339c753c82e9daa42)

