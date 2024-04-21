GOACCESS=goaccess-1.9.2
LIBMMDBVER=1.9.1
LIBMMDB=libmaxminddb-$(LIBMMDBVER)

goaccess : $(LIBMMDB)/src/.libs/libmaxminddb.a $(GOACCESS).tar.gz
	rm -rf $(GOACCESS)
	tar xzvf $(GOACCESS).tar.gz
	cd $(GOACCESS) \
	&& ./configure --enable-geoip=mmdb CFLAGS=-I$(CURDIR)/$(LIBMMDB)/include LDFLAGS=-L$(CURDIR)/$(LIBMMDB)/src/.libs
	$(MAKE) --directory $(GOACCESS)
	$(MAKE) --directory $(GOACCESS) prefix=$(CURDIR)/.. install-exec
	strip goaccess

$(LIBMMDB)/src/.libs/libmaxminddb.a : $(LIBMMDB).tar.gz
	tar xzvf $(LIBMMDB).tar.gz
	cd $(LIBMMDB) && ./configure --disable-shared
	$(MAKE) --directory $(LIBMMDB)

$(GOACCESS).tar.gz:
	wget https://tar.goaccess.io/$(GOACCESS).tar.gz

$(LIBMMDB).tar.gz :
	wget https://github.com/maxmind/libmaxminddb/releases/download/$(LIBMMDBVER)/$(LIBMMDB).tar.gz

clean :
	rm -rf $(GOACCESS) $(GOACCESS).tar.gz
	rm -rf $(LIBMMDB) $(LIBMMDB).tar.gz
	rm -f goaccess

test :
	shellcheck ../*.cgi
