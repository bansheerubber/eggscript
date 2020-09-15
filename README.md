### eggscript

Eggscript is an extension of TorqueScript, adding various new features which make programming in the archaic language a little easier.

Features include:
- string templates. i.e. ```%variable = $"Welcome to {%client.getPlayerName()}'s server!";``` will polyfill to ```%variable = "Welcome to " @ %client.getPlayerName() @ "'s server!";```
- vector expressions. i.e. ```%muzzleVelocity = `%aimVector * {%muzzleVelocity - %speedLoss + %client.getSpeedMod()}`;```
- minification (https://bansheerubber.com/i/f/GeuGv.png)
- de-minification or prettify

**It should be noted that eggscript does not have any error checking yet since this is still early days. Please write good code.**

### What is this:
This is an extension of TorqueScript, as mentioned above. What this means is eggscript keeps most of the same syntax and grammar of TorqueScript while adding on some extensions via additional syntax. The file format of eggscript is the ```.egg``` file. In one of these files, you will write mostly TorqueScript but you will also be able to use some of the extensions provided by eggscript. Any syntax will transpile down to TorqueScript when the eggscript transpiler program is run. Think Typescript, but for TorqueScript instead of Javascript.

For more information, check the pages on the GitHub wiki.