### eggscript

eggscript is an extension of TorqueScript, adding various new features which make programming in the archaic language a little easier.

Features include:
- string templates. i.e. ```%variable = $"Welcome to {%client.getPlayerName()}'s server!";``` will polyfill to ```%variable = "Welcome to " @ %client.getPlayerName() @ "'s server!";```
- minification (https://bansheerubber.com/i/f/GeuGv.png)
- de-minification or prettify

### Usage:
There are two executables provided. One of them is a bash file, and the other is a Windows .cmd file. The differences are not important, the usage between the two is the same.

To use, type ```eggscript [a .egg file]``` into the command line. This will transpile a .egg file into a .cs file with the same name in the same directory. There are some more complicated options that can be used. The ```-o``` or ```--output``` argument can be used to switch the output directory for the file. For instance, ```eggscript -o ./Add-Ons/Server_Minigame server.egg``` will transpile the ```server.egg``` file into ```server.cs``` and store the results in the relative path ```./Add-Ons/Server_Minigame```. ```eggscript``` also supports transpiling entire directores by supplying a directory instead of a .egg file to the command. There are other arguments you can view by doing ```eggscript --help``` into the console. Arguments must come *before* the files or directories you include, or else the program will encounter errors.

It is recommended that you add the directory you download ```eggscript``` into to your PATH env variable. Look up how to do it for your operating system. This will allow you to use the ```eggscript``` command from anywhere in the OS.

By default, ```eggscript``` only recognizes .egg files. You can use the ```-c``` or ```--include-cs``` argument to include .cs files as well.