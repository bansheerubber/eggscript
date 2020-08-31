### eggscript

Eggscript is an extension of TorqueScript, adding various new features which make programming in the archaic language a little easier.

Features include:
- string templates. i.e. ```%variable = $"Welcome to {%client.getPlayerName()}'s server!";``` will polyfill to ```%variable = "Welcome to " @ %client.getPlayerName() @ "'s server!";```
- minification (https://bansheerubber.com/i/f/GeuGv.png)
- de-minification or prettify

**It should be noted that eggscript does not have any error checking yet since this is still early days. Please write good code.**

### What is this:
This is an extension of TorqueScript, as mentioned above. What this means is eggscript keeps most of the same syntax and grammar of TorqueScript while adding on some extensions via additional syntax. The file format of eggscript is the ```.egg``` file. In one of these files, you will write mostly TorqueScript but you will also be able to use some of the extensions provided by eggscript. Any syntax will transpile down to TorqueScript when the eggscript transpiler program is run. Think Typescript, but for TorqueScript instead of Javascript.

### Usage:
There are two executables provided. One of them is a bash file, and the other is a Windows .cmd file. The differences are not important, and the usage between the two is the same.

To use, type ```eggscript [a .egg file]``` into the command line. This will transpile a .egg file into a .cs file with the same name in the same directory. There are some more complicated options that can be used. The ```-o``` or ```--output``` argument can be used to switch the output directory for the file. For instance, ```eggscript -o ./Add-Ons/Server_Example/ server.egg``` will transpile the ```server.egg``` file into ```server.cs``` and store the results in the relative path ```./Add-Ons/Server_Example/```. ```eggscript``` also supports transpiling entire directores by supplying a directory instead of a .egg file to the command. For instance, ```eggscript -o ./Add-Ons/Server_Example/ ./Server_Example-dev/``` will look through all files and subdirectories in ```./Server_Example-dev/``` and transpile any .egg files to ```./Add-Ons/Server_Example/```. There are other arguments you can view by running ```eggscript --help``` in the console. Arguments must come *before* the files or directories you include, or else the program will encounter errors.

It is recommended that you add the directory you download ```eggscript``` into to your PATH env variable. Look up how to do it for your operating system. This will allow you to use the ```eggscript``` command from anywhere in the OS.

By default, ```eggscript``` only recognizes .egg files. You can use the ```-c``` or ```--include-cs``` argument to include .cs files as well.

Any metadata files eggscript requires will be stored in the ```.eggscript``` directory in the same directory you run ```eggscript```.

#### Automatic Transpilation
The eggscript program has a feature that allows it to "watch" over the files or directories you provide to it, waiting for changes to be made. Once a change is made, the file you made a change to will be re-transpiled and automatically put into the output directory you have specified. This is a very useful feature, since you will only have to run the eggscript transpiler program once instead of multiple times as you make changes to your source code. To activate the watcher, use the ```-w``` or ```--watch``` argument. An example may look like ```eggscript --watch -o ./Add-Ons/Server_Example/ ./Server_Example-dev/```. This will transpile everything in the ```./Server_Example-dev/``` directory and then keep a close eye on any changes that are made in that directory. Once a change is made, eggscript will detect it and automatically transpile the individual file you have changed and output it to where it belongs in ```./Add-Ons/Server_Example/```.

#### Caching
The eggscript program will cache the status of all source files. If a file has not been modified since its last transpilation, then eggscript will not transpile it again. Eggscript is smart enough to know when to cache or not. If the output will be different from the last transpilation's output, then it will re-transpile all files (for instance, if you decide you want to minify all your files or remove all comments from your files in the middle of development). To ignore the cache, you can use the ```--clear-cache``` argument to force a transpilation of all files regardless of cache.