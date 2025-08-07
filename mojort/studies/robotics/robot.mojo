from python import Python

fn main():
    try:
        robotmod = Python.import_module("robotmod")
        robotmod.robot_move()
    except:
        print("Exception occurred!")
