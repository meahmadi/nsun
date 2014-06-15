from __future__ import print_function
import sys
import codecs
import os.path
import argparse

from ir.ac.iust.me_ahmadi.multiProcessMind.mind import Mind


if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description="Time+3D Cognitive Agent...")
    parser.add_argument("-v", help="increase output verbosity", action="store_true")
    parser.add_argument("-agent", help="location of datafiles for agent", nargs="?", default="../agentdata")
    parser.add_argument("inputs", nargs='*', help="input *.msg file for processing")
    args = parser.parse_args()
    
    mind = Mind(verbose = args.v, dbpath = args.agent)
    if len(args.inputs)>0:
        for fpath in args.inputs:
            if os.path.isfile(fpath):
                file = codecs.open(fpath,'r','utf-8')
                for line in file:
                    if not mind.listen(line):
                        break
                if mind.hasError():
                    break
            else:
                print("ERROR: ","File Not Found:"+fpath,file=sys.stderr)
                break
    else:
        print(mind.version())
        while True:
            print(mind.prompt(),end="")
            input = sys.stdin.readline()
            if not mind.listen(input):
                pass
    mind.shutdown()
    