BOOSTDIR="/cvmfs/cms.cern.ch/slc6_amd64_gcc700/external/boost/1.63.0-gnimlf/"

RoccoR.so: RoccoR.o
	g++ -shared -Wl,-soname,libRoccoR.so -o libRoccoR.so RoccoR.o

RoccoR.o: RoccoR.cc
	g++ -c -fPIC -I${BOOSTDIR}include/ -L${BOOSTDIR}lib/ -std=gnu++1y RoccoR.cc -o RoccoR.o

clean:
	rm *.so *.o
