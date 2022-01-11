# runcommand.py
# Handy function that executes an external command in the shell
# and returns 3 values: exit code of the command, its standard output
# and its error output.
# If you run the script directly, an example is provided:
# first it will run a successful command and then one with errors
# (you may want to modify them if not running a Unix system).

#std_out data type is str

import subprocess

def runcommand (cmd):
    try:
      proc = subprocess.Popen(cmd,
                              stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE,
                              shell=True,
                              universal_newlines=True)
      std_out, std_err = proc.communicate()
      return proc.returncode, std_out, std_err
    except:
      print("Something went wrong while trying to execute command:",cmd) 

def output_command(cmd,exit_program="False",print_error="True"):
    code, stdout, err = runcommand(cmd)
    if print_error=="True" and code!=0:
      print("-----------------------------------------------------------------")
      print(f"For the command: {cmd} \nThe error is : {err}")
      print("-----------------------------------------------------------------")
    if exit_program == "True" and code!=0:
      exit()
      ##Convert str output to list
    return stdout.split(" ")


def main():
    command="ls -la"
    list = output_command(command)
    print(list)
    print("==================================================");
    print('Running "ls -lh"...');
    print("==================================================");
    code, out, err = runcommand("ls -lh");
    print("Return code: {}".format(code));
    print("--------------------------------------------------");
    print("stdout:");
    print(out);
    print("--------------------------------------------------");
    print("stderr:");
    print(err);
    print("--------------------------------------------------");

    print("==================================================");
    print('Running "ls -lj"...');
    print("==================================================");
    code, out, err = runcommand("ls -lj");
    print("Return code: {}".format(code));
    print("--------------------------------------------------");
    print("stdout:");
    print(out);
    print("--------------------------------------------------");
    print("stderr:");
    print(err);
    print("--------------------------------------------------");
    
if __name__ == '__main__':
    main()
