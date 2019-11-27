import sys
import kickoff

def main():
    kickoff.__main__.main(['kickoff', ":demo"] + sys.argv[1:])

if __name__ == '__main__':
    main()


