
// gy_send("Add-ons/Script_CityThing/emotes/emotes.cs", "Add-ons/Script_CityThing/emotes", 1);

function loadEmotes()
{
	for(%i = findFirstFile("config/emotes/*.png"); %i !$= ""; %i = findNextFile("config/emotes/*.png"))
	{
		%name = strLwr(FileBase(%i));
		
		talk(%name);
		
		eval("datablock particleData(bitmapEmote" @ %name @ "data){textureName=\"" @ %i @ "\";};");
		
		$City::Emote[":" @ %name @ ":"] = %i;
		
		$City::EmoteList = $City::EmoteList SPC ":" @ %name @ ":";
	}
	
	$City::EmoteInit = 1;
}

if(!$City::EmoteInit)
	loadEmotes();

function serverCmdViewEmoticons(%client)
{
	%tokens = $City::EmoteList;
	
	if(%tokens $= "")
		return;
	
	MessageClient(%client, '', "\c6Emoticon list:");
	
	while(%tokens !$= "")
	{
		%tokens = nextToken(%tokens, "token", " ");
		
		MessageClient(%client, '', "<bitmap:" @ $City::Emote[%token] @ ">\c7 - \c6 " @ %token);
	}
}

function serverCmdViewEmoji(%client)
{
	MessageClient(%client, '', "\c6IT'S EMOTICONS NOT EMOJI YOU MORON");
}

function checkStringForEmotes(%msg, %name)
{
	for(%i = 0; %i < getWordCount(%msg); %i++)
	{
		%word = strTrim(getWord(%msg, %i));
		%check = strPos($City::EmoteList, strLwr(%word));
		
		if(%check != -1 && $City::Emote[%word] !$= "")
		{
			%replace = "<bitmap:" @ $City::Emote[%word] @ ">\c6";
			
			if(strLen(%replace) + strLen(%final) > 255)
				continue;

			if(%final !$= "")
				%final = %final SPC %replace;
			else
				%final = %replace;
			
			%found++;
		}
		else if(%final !$= "")
			%final = %final SPC %word;
		else
			%final = %word;
	}
	
	if(%found > 0)
		return %final;
	else
		return 0;
}

deactivatePackage(City_Emotes);
package City_Emotes
{
	function serverCmdMessageSent(%client, %msg)
	{
		%thing = checkStringForEmotes(%msg, %client.getPlayerName());
		
		if(getSimTime() - %client.lastEmote < 100)
		{
			%client.stopEmoteSpam = getSimTime();
		}
		
		if(getSimTime() - %client.stopEmoteSpam < 5000)
		{
			MessageClient(%client, '', "\c6Don't spam.");
			return;
		}
		
		if(%thing !$= "0")
		{
			%msg = %thing;
		
			%format = '%1\c3%2\c7%3\c6: %4';
			
			CommandToAll('chatMessage', %client, '', '', %format, %client.clanPrefix, %client.getPlayerName(), %client.clanSuffix, %msg);
			
			%client.lastEmote = getSimTime();
			
			return;
		}
		
		Parent::serverCmdMessageSent(%client, %msg);
	}
};
activatePackage(City_Emotes);