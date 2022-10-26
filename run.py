import sys
from coverage.cmdline import main

if __name__ == '__main__':
    sys.argv = ['coverage', 'report']
    main()
