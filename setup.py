import os

def install_venv():    
    os.system("bash ./src/initsetup.sh")

if __name__ == "__main__":
    if os.path.exists("./.venv"):
        print("A virtual enviornment was already found. Activate it using:"
              "\nsource ./src/setvenv.sh"
              "\nAnd then run:"
              "\npip install -r requirements.txt"
        )
    else:
        if input("A virtual enviornment was not found. Would you like to create one? (y|n): ").lower() != 'y':
            print("You will now need to install the packages manually. You can do this by running:"
                "\npip install -r requirements.txt"
                "\nNote that this will install the packages to your main instance of Python."
            )
        else:
            print("This will take a little bit. Now creating virtual enviornment and installing packages.")
            install_venv()
            
            # TODO: get this working to automatically activate the venv, I cant be bothered rn, too tired
            # subprocess.run("source .venv/bin/activate", shell=True)
            # os.system("cd ../..")
            # exit()