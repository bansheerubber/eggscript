### eggscript

eggscript is an extension of TorqueScript, adding various new features which make programming in the archaic language a little easier.

features include:
- string templates. i.e. ```%variable = $"Welcome to {%client.getPlayerName()}'s server!";``` will polyfill to ```%variable = "Welcome to " @ %client.getPlayerName() @ "'s server!";```
- minification (https://bansheerubber.com/i/f/GeuGv.png)
- de-minification or prettify