

from python import Python

fn main():  
    try:
        let sys = Python.import_module("sys")
          for p in sys.path:
              print(p)
        Python.add_to_path(".")
        let alg = Python.import_module("algorithm_x")
        alg.main()
        print("Hello, world!")
    except e:
        print(e)