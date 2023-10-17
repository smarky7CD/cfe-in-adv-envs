# Change IDIR and LDIR to location of libsodium install

IDIR = /opt/homebrew/Cellar/libsodium/1.0.18_1/include
LIBS = -lsodium
LDIR = /opt/homebrew/Cellar/libsodium/1.0.18_1/lib/
CC = cc
CFLAGS= -Wall -W -std=c99  test.c ck.c -I$(IDIR) -L$(LDIR)

test: 
	$(CC) -o test $(CFLAGS) $(LIBS)

clean:
	rm test