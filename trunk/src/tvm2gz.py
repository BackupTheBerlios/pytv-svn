#!/usr/bin/python2.4

def convertTvmGz(tvmfile,gzfile):

	f = open(tvmfile, "rb")
	g = open(gzfile, "wb")

	f.seek(0x006a,0)
	g.write(f.read(6))
	f.seek(0x0064,0)
	g.write(f.read(6))
	f.seek(0x0070,0)
	g.write(f.read(88))
	f.seek(0x0320,0)
	g.write(f.read(17))
	f.seek(0x0011,0)
	g.write(f.read(83))
	f.seek(0x012c,0)
	g.write(f.read(100))
	f.seek(0x0000,0)
	g.write(f.read(17))
	f.seek(0x0331,0)
	g.write(f.read(183))
	f.seek(0x0258,0)
	g.write(f.read(200))
	f.seek(0x0190,0)
	g.write(f.read(200))
	f.seek(0x00c8,0)
	g.write(f.read(100))
	f.seek(0x03e8,0)
	g.write(f.read())

	f.close()
	g.close()
	
def main():
	tvmfile = "test.tvm"
	gzfile = "test2.gz"
	print("Converting " + tvmfile + " to " + gzfile)
	
	convertTvmGz(tvmfile,gzfile)
	
if __name__=='__main__': main()