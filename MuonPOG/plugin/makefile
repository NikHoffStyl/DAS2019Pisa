RoccoR.so: RoccoR.o
	g++ -shared -Wl,-soname,libRoccoR.so -o libRoccoR.so RoccoR.o

RoccoR.o: RoccoR.cc
	g++ -c -fPIC -std=gnu++1y -IRoccoR.h RoccoR.cc -o RoccoR.o

clean:
	rm *.so *.o
