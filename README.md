# metagpr

```
$ python poc.py && gprbuild -f -P app.gpr && ./obj/main
Compile
   [Ada]          main.adb
   [Ada]          lib1.adb
   [Ada]          lib2.adb
   [Ada]          lib3.adb
   [Ada]          lib1_config.ads
   [Ada]          lib2_config.ads
   [Ada]          lib3_config.ads
Bind
   [gprbind]      main.bexch
   [Ada]          main.ali
Link
   [link]         main.adb
Hello from app
Lib1: Max_Path_Len: 42
Lib1: Verbose:TRUE
Lib2: URL:example.com
Lib2: Verbose:TRUE
Lib3: Verbose:FALSE
```
