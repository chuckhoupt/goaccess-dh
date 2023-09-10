bin/goaccess : libmaxminddb/src/.libs/libmaxminddb.a goaccess/goaccess
	$(MAKE) --directory goaccess \
	CFLAGS=-I$(CURDIR)/libmaxminddb/include LDFLAGS=-L$(CURDIR)/libmaxminddb/src/.libs \
	prefix=$(CURDIR) install-exec
	strip bin/goaccess

goaccess/goaccess : goaccess/Makefile
	$(MAKE) --directory goaccess

goaccess/Makefile :
	cd goaccess && autoreconf -fiv \
	&& ./configure --enable-geoip=mmdb CFLAGS=-I$(CURDIR)/libmaxminddb/include LDFLAGS=-L$(CURDIR)/libmaxminddb/src/.libs

libmaxminddb/src/.libs/libmaxminddb.a : libmaxminddb/Makefile
	$(MAKE) --directory libmaxminddb

libmaxminddb/Makefile :
	cd libmaxminddb && ./bootstrap && ./configure --disable-shared

clean :
	-$(MAKE) --directory goaccess distclean
	-$(MAKE) --directory libmaxminddb distclean
	-rm -r bin	

test :
	shellcheck *.cgi
