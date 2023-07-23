import subprocess
import queue

def getControllerInput(inFile: str) -> str:
    subprocess.Popen(inFile)


if __name__ == "__main__":
    getControllerInput