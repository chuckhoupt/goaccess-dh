bin/goaccess : goaccess/goaccess
	$(MAKE) --directory goaccess prefix=$(CURDIR) install-exec

goaccess/goaccess : goaccess/Makefile
	$(MAKE) --directory goaccess

goaccess/Makefile :
	cd goaccess && autoreconf -fiv && ./configure 

clean : goaccess/Makefile
	$(MAKE) --directory goaccess clean
	-rm -r bin	
