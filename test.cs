
// gy_send("Add-ons/Script_CityThing/god/main.cs", "Add-ons/Script_CityThing/god", 1);

// NOTES: pope should get a readout of all the negative piety laws that are currently enacted

datablock AudioProfile(InceptionSound)
{
	filename = $City::Path @ "/sounds/inception.wav";
	description = AudioDefault3d;
};

if(!isObject(GodSO))
	schedule(1, 0, createGodSO);

function createGodSO()
{
	new ScriptObject(GodSO)
	{
		events_num = 0;
		piety = 0;
		events = true;
	};
	GodSO.tick();
}

exec("config/server/City/god.cs");

// exec("./piety.cs");
exec("./meteors.cs");
exec("./money.cs");
schedule(1, 0, exec, $City::Path @ "/god/alligators.cs"); // this changes some alligator hole bot datablock shit so it needs to be executed after bot_alligator
exec("./misc.cs");
exec("./guns.cs");
exec("./pope.cs");

exec("./radio.cs");

function serverCmdUpdateGod(%client)
{
	if(%client.isAdmin)
	{
		talk("Updating god...");
		schedule(500, 0, exec, $City::Path @ "/god/main.cs");
	}
}

function godTalk(%msg)
{
	MessageAll('', "<color:1ECC35>God\c6:<font:Palatino Linotype bold:128>" SPC strUpr(%msg));
}

$City::God::SunFlare["dilbert", "color"] = "0.579439 0.399266 0.362826";
$City::God::SunFlare["penguin", "color"] = "1.00 1.00 1.00";
$City::God::SunFlare["simi", "color"] = "1.00 0.689056 0.626168";

function god_annoyingSun2()
{
	god_radioEvent($City::God::CurrentNewsCaster, "HUGE_SUN");
	
	god_keyframeSunSize(SunLight.flareSize, 15, 0.04);
	
	CitySO.schedule((2.9 * 60) * 1000, loadEnv);
}

function god_annoyingSun1()
{
	god_radioEvent($City::God::CurrentNewsCaster, "HUGE_SUN");
	
	god_keyframeSunSize(SunLight.flareSize, 40, 0.04);
	
	CitySO.schedule((2.9 * 60) * 1000, loadEnv);
}

function god_keyframeSunSize(%start, %end, %step, %pos)
{
	cancel($City::God::SunFlareSizeSch);
	
	if(%pos $= "")
		%pos = %start;
	
	%pos += %step;
	
	if((%step > 0 && %pos > %end) || (%step < 0 && %pos < %end))
		return;
	
	SunLight.setFlareSize(%pos);
	$City::God::SunFlareSizeSch = schedule(5, 0, god_keyframeSunSize, %start, %end, %step, %pos);
}

function god_setSunFlareBitmap(%image_path)
{
	%color = $City::God::SunFlare[fileBase(%image_path), "color"];
	
	if(%color $= "")
		%color = "1.00 0.689056 0.626168";
		
	SunLight.setFlareColor(getWord(%color, 0), getWord(%color, 1), getWord(%color, 2));
	SunLight.setFlareBitmaps(%image_path, %image_path);
	SunLight.sendUpdate();
}

function god_showSunFlare()
{
	%sunflare = SunLight;
	$City::God::CurrentSunflare = %sunflare;
	
	%count = ClientGroup.getCount();
	for(%i = 0; %i < %count; %i++)
		ClientGroup.getObject(%i).setSunFlare(%sunflare);
}

function god_clearSunFlare()
{
	$City::God::CurrentSunflare = "";
	
	%count = ClientGroup.getCount();
	for(%i = 0; %i < %count; %i++)
		ClientGroup.getObject(%i).clearSunFlare();
}



function GodSO::tick(%this)
{
	cancel(GodSO.tickSch);
	
	if(ClientGroup.getCount() > 2)
	{
		if(GodSO.getpietyLevel() > -3)
		{
			if(($Sim::Time - GodSO.last_event_time) > (60 * 1.9) && GodSO.events == true)
			{
				GodSO.startEvent();
				GodSO.last_event_time = $Sim::Time;
			}
		}
		else
		{
			if(($Sim::Time - GodSO.last_event_time) > 29 && GodSO.events == true)
			{
				GodSO.startEvent();
				GodSO.last_event_time = $Sim::Time;
			}
		}
	}
	
	if(ClientGroup.getCount() > 2)
	{
		for(%i = 0; %i < 20; %i++)
		{
			GodSO.piety += $City::God::PietyBoost[%i];
			
			if($City::God::PietyBoost[%i] && $City::TempGod::LastPietySend != $SaveSO::Store["time"])
			{
				if($City::God::PietyBoost[%i] > 0)
					GodSO.getPope().sendPopePietyHistory($City::God::PietyBoost[%i] * 4 SPC "piety gained from" SPC $City::God::PietyBoost[%i, "name"], $City::God::PietyBoost[%i] * 2);
				else
					GodSO.getPope().sendPopePietyHistory($City::God::PietyBoost[%i] * 4 SPC "piety lost to" SPC $City::God::PietyBoost[%i, "name"], $City::God::PietyBoost[%i] * 2);
			}
		}
	}
	
	if(%this.drug_piety > 0)
	{
		GodSO.getPope().sendPopePietyHistory(GodSO.drug_piety * 2 SPC "piety lost to" SPC (GodSO.drug_piety / 3) SPC "unbusted drugs", GodSO.drug_piety);
		GodSO.drug_piety = 0;
	}
	
	%count = ClientGroup.getCount();
	for(%i = 0; %i < %count; %i++)
	{
		%client = ClientGroup.getObject(%i);
		
		if(%client.perk $= "devout")
		{
			GodSO.piety += 4;
			%devout_piety += 4;
		}
	}
	
	%this.piety = mClamp(%this.piety, -500, 500);
	
	if(%devout_piety && $City::TempGod::LastPietySend != $SaveSO::Store["time"])
		GodSO.getPope().sendPopePietyHistory(%devout_piety * 4 SPC "piety gained from devout citizens", %devout_piety * 2);
	
	$City::TempGod::LastPietySend = $SaveSO::Store["time"];
	
	%this.handleEnv();
	
	GodSO.tickSch = %this.schedule(30 * 1000, tick);
}

function GodSO::handleEnv(%this)
{
	// if lightning is enabled, don't change the environment
	if($Sim::Time - $City::God::StartLightning < 200)
		return;
	
	if(%this.getPietyLevel() == -3)
	{
		CitySO.loadEnv($City::Path @ "/envs/god_angry.txt");
		SunLight.setFlareBitmaps("Add-Ons/SunFlare_City/simi.png", "Add-Ons/SunFlare_City/simi.png");
		GodSO.different_env = true;
	}
	else if(%this.getPietyLevel() >= -2 && %this.getPietyLevel() <= 2)
	{
		if(GodSO.different_env)
		{
			CitySO.loadEnv();
			GodSO.different_env = false;
		}
	}
	else if(%this.getPietyLevel() == 3)
	{
		CitySO.loadEnv($City::Path @ "/envs/god_happy.txt");
		SunLight.setFlareBitmaps("Add-Ons/SunFlare_City/penguin.png", "base/lighting/lightFalloffMono.png");
		GodSO.different_env = true;
	}
	
	for(%i = 0; %i < ClientGroup.getCount(); %i++)
	{
		%client = ClientGroup.getObject(%i);
		
		if(%client.isJob("Pope") && isObject(%client.player))
		{
			%client.player.mountImage("City_PopeHat" @ %this.getPietyLevel() + 4 @ "Image", 2);
			%client.sendpietyLevel();
		}
	}
}

function GodSO::pope_triggerGoodEvent(%this)
{
	if(%this.getpietyLevel() == 3)
		%this.startEvent(3);
	else
		%this.startEvent(2);
	
	%this.handleEnv();
}

function GodSO::pope_triggerBadEvent(%this)
{
	if(%this.getpietyLevel() == -3)
		%this.startEvent(-3);
	else
		%this.startEvent(-2);
	
	%this.handleEnv();
}

function GodSO::simiEvent(%this)
{
	CitySO.loadEnv($City::Path @ "/envs/god_angry.txt");
	SunLight.setFlareBitmaps("Add-Ons/SunFlare_City/simi.png", "Add-Ons/SunFlare_City/simi.png");
	GodSO.different_env = true;
	
	god_keyframeSunSize(0, 5, 0.01);
	
	ServerPlay2D(InceptionSound);
	schedule(3700, 0, ServerPlay2D, InceptionSound);
	
	for(%i = 0; %i < 15; %i++)
		schedule(getRandom(300, 500) * %i, 0, god_smiteRandomPoint);
}

function GodSO::registerEvent(%this, %name, %piety, %function, %piety_amt)
{
	if(%this.event[%name] !$= "")
		return;
	
	%this.event[%this.events_num] = %name;
	%this.event[%this.events_num, "level"] = %piety;
	%this.event[%this.events_num, "function"] = %function;
	%this.event[%this.events_num, "piety"] = %piety_amt;
	%this.event[%name] = %this.events_num;
	
	%this.events_num++;
}

function GodSO::getPietyLevel(%this)
{
	if(%this.piety >= 500)
		return 3; // super good tier
	else if(%this.piety <= 499 && %this.piety >= 250)
		return 2; // good tier
	else if(%this.piety <= 249 && %this.piety >= 50)
		return 1; // slightly good tier
	else if(%this.piety <= 49 && %this.piety >= -49)
		return 0; // neutral tier
	else if(%this.piety <= -50 && %this.piety >= -249)
		return -1; // slightly bad tier
	else if(%this.piety <= -250 && %this.piety >= -499)
		return -2; // bad tier
	else if(%this.piety <= -500)
		return -3; // super bad tier
}

function GodSO::getPietyLevelF(%this)
{
	if(%this.piety >= 500)
		return 3; // super good tier
	else if(%this.piety <= 499 && %this.piety >= 250)
		return 2 + ((%this.piety - 250) / (499 - 250)); // good tier
	else if(%this.piety <= 249 && %this.piety >= 50)
		return 1 + ((%this.piety - 50) / (249 - 50)); // slightly good tier
	else if(%this.piety <= 49 && %this.piety >= -49)
		return 0 + ((%this.piety) / (49 - -49)) * 2; // neutral tier
	else if(%this.piety <= -50 && %this.piety >= -249)
		return -1 + ((mAbs(%this.piety) - 50) / (249 - 50)); // slightly bad tier
	else if(%this.piety <= -250 && %this.piety >= -499)
		return -2 + ((mAbs(%this.piety) - 250) / (499 - 250)); // bad tier
	else if(%this.piety <= -500)
		return -3; // super bad tier
}

function GodSO::getEventCost(%this, %level)
{
	switch(%level)
	{
		case -3: return 400;
		case -2: return 200;
		case -1: return 80;
		case 0: return -25;
		case 1: return -80;
		case 2: return -200;
		case 3: return -400;
	}
}

// picking an event will work like this:
// a god event will be registered at a certain 'tick' along the piety meter and piety will round up/down to that tick and then pull from a random pool of events that were registered on that tick

function GodSO::startEvent(%this, %level)
{
	if(%level $= "")
		%level = %this.getpietyLevel();
	
	for(%i = 0; %i < %this.events_num; %i++)
	{
		if(%this.event[%i, "level"] == %level && %i != %this.last_event)
			%list = trim(%list SPC %i);
	}
	
	%random_event = getWord(%list, getRandom(0, getWordCount(%list) - 1));
	%this.last_event = %random_event;
	
	%this.piety += %this.event[%random_event, "piety"];
	
	if(%this.event[%random_event, "piety"] > 0)
		GodSO.getPope().sendPopepietyHistory(%this.event[%random_event, "piety"] * 2 SPC "piety gained from God event" SPC %this.event[%random_event], %this.event[%random_event, "piety"]);
	else
		GodSO.getPope().sendPopepietyHistory(%this.event[%random_event, "piety"] * 2 SPC "piety lost to God event" SPC %this.event[%random_event], %this.event[%random_event, "piety"]);
	
	echo("GOD EVENT >>>>>>>>>>>>>>>>>>>>>>" SPC %this.event[%random_event]);
	eval(%this.event[%random_event, "function"]);
}

/// god event tier:
// super bad -> bad -> slightly bad -> neutral -> slightly good -> good -> super good

GodSO.registerEvent("Raining Money 3", 3, "startMoney3();", -400);
GodSO.registerEvent("Gun Rain 3", 3, "startGunRain3();", -400);
GodSO.registerEvent("Tax Subsidization 3", 3, "god_taxSubsidization3();", -400);
GodSO.registerEvent("Raise Paychecks 3", 3, "god_raisePaychecks3();", -400);
GodSO.registerEvent("Super Money Meteors", 3, "superMoneyMeteors();", -400);
GodSO.registerEvent("Social Security 2", 3, "god_socialSecurity();", -400);

GodSO.registerEvent("Raining Money 2", 2, "startMoney2();", -200);
GodSO.registerEvent("Gun Rain 2", 2, "startGunRain2();", -200);
GodSO.registerEvent("Tax Subsidization 2", 2, "god_taxSubsidization2();", -200);
GodSO.registerEvent("Raise Paychecks 2", 2, "god_raisePaychecks2();", -200);
GodSO.registerEvent("Money Meteors", 3, "moneyMeteors();", -200);
GodSO.registerEvent("Social Security 1", 3, "god_socialSecurity();", -200);

GodSO.registerEvent("Raining Money 1", 1, "startMoney1();", -80);
GodSO.registerEvent("Raining Guns 1", 1, "startGunRain1();", -80);
GodSO.registerEvent("Friendly Alligators", 1, "startFriendlyAlligators();", -80);
GodSO.registerEvent("Tax Subsidization 1", 1, "god_taxSubsidization1();", -80);
GodSO.registerEvent("Raise Paychecks 1", 1, "god_raisePaychecks1();", -80);

GodSO.registerEvent("Alligator Rain 2", 0, "startAlligators();", 25);
GodSO.registerEvent("Fake Meteors", 0, "startFakeMeteors();", -25);
GodSO.registerEvent("Server-wide Music 2", 0, "god_randomMusic();", -25);
GodSO.registerEvent("Kill Mayor Election Losers", 0, "god_killLosers();", -25);
GodSO.registerEvent("Explode Random Trees 2", 0, "god_explodeRandomTrees();", 25);
GodSO.registerEvent("Praise the Lord", 0, "startPraiseTheLord();", -25);
GodSO.registerEvent("Change Road Signs", 0, "god_changeRoadSigns();", -25);
GodSO.registerEvent("Random Road Walls 2", 0, "god_placeWallsOnRoads();", 25);
GodSO.registerEvent("Badspot Face Skybox", 0, "god_badspotifyTheSun();", -25);
GodSO.registerEvent("Larger Sun 2", 0, "god_annoyingSun2();", 25);

GodSO.registerEvent("Change Vehicles to ZiQs", -1, "god_changeVehiclesToZiQs();", 80);
GodSO.registerEvent("Server-wide Music 1", -1, "god_randomMusic();", 80);
GodSO.registerEvent("Explode Random Trees 1", -1, "god_explodeRandomTrees();", 80);
GodSO.registerEvent("Server-wide Music 1", -1, "god_randomMusic();", 80);
GodSO.registerEvent("Random Road Walls 1", -1, "god_placeWallsOnRoads();", 80);
GodSO.registerEvent("Larger Sun 1", -1, "god_annoyingSun1();", 80);
GodSO.registerEvent("Production Decrease 1", -1, "startProductionDecrease1();", 80);
GodSO.registerEvent("Rocket Trees 1", -1, "god_explodeRandomTrees2();", 80);
GodSO.registerEvent("Big Pope Chat", -1, "startBigPopeChat();", 80);
GodSO.registerEvent("Give Hunger 1", -1, "god_hungerEverybody2();", 80);
GodSO.registerEvent("Gunigators 1", -1, "startWeaponizedAlligators1();", 80);

GodSO.registerEvent("Wanted Levels", -2, "god_crimEverybody();", 200);
GodSO.registerEvent("Giant Sea Alligator", -2, "god_create_monster_alligator();", 200);
GodSO.registerEvent("Everybody Muted", -2, "god_muteEverybody();", 200);
GodSO.registerEvent("Production Decrease 2", -2, "startProductionDecrease2();", 200);
GodSO.registerEvent("Rocket Trees 2", -2, "god_explodeRandomTrees3();", 200);
GodSO.registerEvent("Handcuff Everybody", -2, "god_cuffEverybody();", 200);
GodSO.registerEvent("Give Hunger 2", -2, "god_hungerEverybody2();", 200);
GodSO.registerEvent("Meteors", -2, "startMeteors();", 200);
GodSO.registerEvent("Gunigators 2", -2, "startWeaponizedAlligators2();", 200);
GodSO.registerEvent("Lightning 1", -2, "godsWrathLoop();", 200);

GodSO.registerEvent("Production Decrease 3", -3, "startProductionDecrease3();", 400);
GodSO.registerEvent("Rocket Trees 3", -3, "god_explodeRandomTrees4();", 400);
GodSO.registerEvent("Give Hunger 3", -3, "god_hungerEverybody3();", 400);
GodSO.registerEvent("Super Meteors", -3, "startSuperMeteors();", 400);
GodSO.registerEvent("Gunigators 3", -3, "startWeaponizedAlligators3();", 400);
GodSO.registerEvent("Lava Ocean", -3, "god_makeOceanLava();", 400);
GodSO.registerEvent("Legal Crime", -3, "god_legalCrime();", 400);
// GodSO.registerEvent("Kill Non-Voters", -3, "god_killNonVoters();", 400);
GodSO.registerEvent("Tasergators", -3, "startWeaponizedAlligators4();", 400);
GodSO.registerEvent("Lightning 1", -3, "godsWrathLoop();", 400);




// this is the pope sacrifice pit
datablock triggerData(City_SacrificeData)
{
	tickPeriodMS = 30;
	parent = 0;
};

if(!isObject($City::TempGod::SacrificePit))
	schedule(100, 0, CreateSacrificePit);
	
function CreateSacrificePit()
{
	%size = 16;
	$City::TempGod::SacrificePit = new Trigger()
	{
		datablock = City_SacrificeData;
		
		position = "-452.5 -361.5 18";
		rotation = eulerToAxis("0 0 45");
		scale = "1 1 1";
		
		polyhedron =  -(%size / 4) SPC -(%size / 4)  SPC "0" SPC %size / 2 SPC "0 0" SPC "0" SPC %size / 2 SPC "0" SPC "0 0 2";
	};
}

function City_SacrificeData::onEnterTrigger(%this, %trigger, %obj)
{
	if((%obj.getClassName() $= "Player" || %obj.getClassName() $= "AiPlayer") && !%obj.isCorpse)
	{
		%obj.tossCuffedPlayer();
		
		if(isObject(%obj.getObjectMount()) || isObject(%obj.getMountedObject(0)))
			return;
		
		// make it so that priests can't sacrifice themselves
		if(!%obj.client.isJob("Priest") && !%obj.client.isJob("Pope"))
		{
			ServerPlay2D(ThunderCrash1Sound);
			ServerPlay2D(ThunderCrash1Sound);
			ServerPlay2D(ThunderCrash1Sound);
			
			%obj.client.spawn_corpse = false;
			%obj.client.spawn_items = false;
			%obj.church_sacrificed = true;
			
			if($Sim::Time - %obj.city_lastHeldByTime < 5)
				%attacker = %obj.city_lastHeldBy;
			else
				%attacker = %obj.client;
			
			if($City::TempGov::Laws["Church Sacrifices", "enacted"])
				%attacker = %obj.client;
			
			%obj.schedule(1, damage, %attacker, %obj.getPosition(), 10000, $DamageType::Suicide);
		}
		else
			%obj.setTransform("-446.5 -361.5 33.3");
	}
}

if(isObject(City_PriestJob))
	City_PriestJob.delete();

new ScriptObject(City_PriestJob)
{
	name = "Priest";
	paycheck = 10;
	initial_invest = 0;
	
	police = 0;
	civilian = 0;
	
	tool[3] = "";
	tool[4] = "";
	tool[5] = "";
	tool[6] = "";
	tool[7] = "";
	tool[8] = "";
	tool[9] = "";
	
	description = "\c6Become holier than thou";
};
JobSO.add(City_PriestJob);

function City_PriestJob::onSpawn(%this, %client)
{
	%total_cost = 0;
	for(%i = 3; %i < 10; %i++)
	{
		%tool = %this.tool[%i];
		%index = GodSO.pope_weapons[%tool.uiName];
		
		if(GodSO.pope_weapons[%index, "cost"] !$= "")
			%total_cost += CitySO.getInflationPrice(GodSO.pope_weapons[%index, "cost"]);
	}
	
	if(%total_cost > getChurchMoney())
		MessageClient(%client, '', "\c6You have not received your holy tools due to a lack of funds.");
	else
	{
		for(%i = 3; %i < 10; %i++)
		{
			if(%client.player.addItem(%this.tool[%i].getId()) != -1)
				%total_cost2 += CitySO.getInflationPrice(GodSO.pope_weapons[%index, "cost"]);
		}
	}
	
	if(%total_cost != 0)
		deductChurchMoney(%total_cost, "$" @ %total_cost SPC "spent on equipping" SPC %client.getPlayerName());
}


if(isObject(City_PopeJob))
	City_PopeJob.delete();

new ScriptObject(City_PopeJob)
{
	name = "Pope";
	paycheck = 10;
	initial_invest = 0;
	
	police = 0;
	civilian = 0;
	
	tool[3] = "";
	tool[4] = "";
	tool[5] = "";
	tool[6] = "";
	tool[7] = "";
	tool[8] = "";
	tool[9] = "";
};
JobSO.add(City_PopeJob);

function City_PopeJob::onSpawn(%this, %client)
{
	cancel($City::TempGod::FindNewPopeSch);
	
	CommandToAll('Suburbia_SetPopeSelected', false);
	
	%client.player.mountImage("City_PopeHat" @ GodSO.getpietyLevel() + 4 @ "Image", 2);
	%client.schedule(1, applyBodyParts);
	
	%total_cost = 0;
	for(%i = 3; %i < 10; %i++)
	{
		%tool = %this.tool[%i];
		%index = GodSO.pope_weapons[%tool.uiName];
		
		if(GodSO.pope_weapons[%index, "cost"] !$= "")
			%total_cost += GodSO.pope_weapons[%index, "cost"];
	}
	
	if(%total_cost > getChurchMoney())
		MessageClient(%client, '', "\c6You have not received your holy tools due to a lack of funds.");
	else
	{
		for(%i = 3; %i < 10; %i++)
		{
			if(%client.player.addItem(%this.tool[%i].getId()) != -1)
				%total_cost2 += GodSO.pope_weapons[%index, "cost"];
		}
	}
	
	if(%total_cost != 0)
		GodSO.getPope().sendPopeBudget("$" @ %total_cost SPC "spent on equipping" SPC %client.getPlayerName(), %total_cost);
}

function City_PopeJob::onDeath(%this, %client, %obj, %killer, %type, %area)
{
	%client.setJob(City_PriestJob, true);
	
	$City::TempGod::LastPopeDeath = $Sim::Time;
	
	if(%client != %killer)
	{
		MessageClient(%killer, '', "<font:Calibri bold:25>\c0Since you killed the Pope, you will become the Pope in 15 seconds. Use \c3/deny \c0to cancel this.");
		%killer.make_pope = %killer.schedule(15000, setJob, City_PopeJob);
		%killer.make_pope2 = schedule(15000, 0, MessageAll, '', "<font:Calibri bold:30><color:9FEF65>" @ %killer.getPlayerName() SPC "\c6has become the new <color:9FEF65>Pope\c6!");
		$City::TempGod::FindNewPopeSch = schedule(17000, 0, god_findNewPope);
	}
	
	CommandToAll('Suburbia_SetPopeSelected', false);
	return;
	
	for(%i = 0; %i < ClientGroup.getCount(); %i++)
	{
		%priest = ClientGroup.getObject(%i);
		
		%priest.god_donated_money = 0;
		MessageClient(%priest, '', "<font:Calibri bold:30>\c6The <color:9FEF65>Pope\c6 has died! Sacrifice more money than your fellow citizens using <color:9FEF65>/donate\c6 to be chosen as the new <color:9FEF65>Pope\c6.");
	}
	
	cancel($City::TempGod::FindNewPopeSch);
	$City::TempGod::FindNewPopeSch = schedule((60 * 1) * 1000, 0, god_findNewPope);
}

function City_PopeJob::onLeaveJob(%this, %client)
{
	schedule(100, 0, god_findNewPope);
	$City::TempGod::LastPopeDeath = $Sim::Time;
	return;
	
	%client.player.unMountImage(2);
	%client.schedule(1, applyBodyParts);
	
	for(%i = 0; %i < ClientGroup.getCount(); %i++)
	{
		%priest = ClientGroup.getObject(%i);
		
		%priest.god_donated_money = 0;
		MessageClient(%priest, '', "<font:Calibri bold:30>\c6The <color:9FEF65>Pope \c6has left! Sacrifice more money than your fellow citizens using <color:9FEF65>/donate\c6 to be chosen as the new <color:9FEF65>Pope\c6.");
	}
	
	cancel($City::TempGod::FindNewPopeSch);
	$City::TempGod::FindNewPopeSch = schedule((60 * 1) * 1000, 0, god_findNewPope);
}

function City_PopeJob::onArrest(%this, %client, %cop)
{
	%client.setJob(City_CitizenJob, true);
	
	MessageClient(%priest, '', "<font:Calibri bold:30>\c6The <color:9FEF65>Pope\c6 has been arrested! Apply for <color:9FEF65>Pope \c6in the GUI to become the next <color:9FEF65>Pope!");
	schedule(100, 0, god_findNewPope, true);
	$City::TempGod::LastPopeDeath = $Sim::Time;
	return;
	
	
	MessageClient(%client, '', "\c6You are no longer the \c3Pope\c6.");
	
	for(%i = 0; %i < ClientGroup.getCount(); %i++)
	{
		%priest = ClientGroup.getObject(%i);
		
		if(%priest.isJob("Pope") || %priest.isJob("Priest"))
		{
			%priest.god_donated_money = 0;
			MessageClient(%priest, '', "<font:Calibri bold:30>\c6The <color:9FEF65>Pope\c6 has been arrested! Sacrifice more money than your fellow citizens using <color:9FEF65>/donate\c6 to be chosen as the new <color:9FEF65>Pope\c6.");
		}
	}
	
	cancel($City::TempGod::FindNewPopeSch);
	$City::TempGod::FindNewPopeSch = schedule((60 * 1) * 1000, 0, god_findNewPope);
	
	%client.player.umMountImage(2);
	%client.schedule(1, applyBodyParts);
}

function City_PopeJob::onLeaveGame(%client)
{
	schedule(100, 0, god_findNewPope);
	$City::TempGod::LastPopeDeath = $Sim::Time;
	return;
	
	for(%i = 0; %i < ClientGroup.getCount(); %i++)
	{
		%priest = ClientGroup.getObject(%i);
		
		if(%priest.isJob("Pope") || %priest.isJob("Priest"))
		{
			%priest.god_donated_money = 0;
			MessageClient(%priest, '', "<font:Calibri bold:30>\c6The <color:9FEF65>Pope\c6 has left! Sacrifice more money than your fellow citizens using <color:9FEF65>/donate\c6 to be chosen as the new <color:9FEF65>Pope\c6.");
		}
	}
	
	cancel($City::TempGod::FindNewPopeSch);
	$City::TempGod::FindNewPopeSch = schedule((60 * 1) * 1000, 0, god_findNewPope);
}

function GodSO::getPope(%this)
{
	%count = ClientGroup.getCount();
	for(%i = 0; %i < %count; %i++)
		if((%client = ClientGroup.getObject(%i)).isJob("Pope"))
			return %client;
}

function serverCmdDeny(%client)
{
	if(isEventPending(%client.make_pope))
	{
		cancel(%client.make_pope);
		cancel(%client.make_pope2);
		cancel($City::TempGod::FindNewPopeSch);
		
		MessageClient(%client, '', "<font:Calibri bold:25>\c0You declined the offer to become the new Pope.");
		
		god_findNewPope();
	}
}

DeactivatePackage(City_PopePackage);
package City_PopePackage
{
	function GameConnection::applyBodyParts(%client) 
	{
		%r = Parent::applyBodyParts(%client);

		if(isObject(%player = %client.player) && %client.isJob("Pope"))
		{
			// hide hat/accent note shit
			for(%i=0; $hat[%i] !$= ""; %i++)
				%player.hideNode($hat[%i]);

			for(%i=0; $accent[%i] !$= ""; %i++)
				%player.hideNode($accent[%i]);
		}

		return %r;
	}
};
ActivatePackage(City_PopePackage);

function serverCmdDonate(%client, %money)
{
	return;
	
	if(!isNumber(%money))
	{
		MessageClient(%client, '', "\c6You cannot donate \c3" @ %money @ "\c6. Please enter a valid amount.");
		return;
	}
	
	if(!isEventPending($City::TempGod::FindNewPopeSch) && isObject(GodSO.getPope()))
	{
		MessageClient(%client, '', "\c6You cannot donate money to \c3God \c6while there is a \c3Pope \c6in office.");
		return;
	}
	
	%money = mFloor(%money);
	if(%money > %client.getMoney())
	{
		MessageClient(%client, '', "\c6You do not have that much money to donate!");
		return;
	}
	
	if(%money <= 0)
	{
		MessageClient(%client, '', "\c6You cannot donate \c2$" @ %money @ "\c6. Please enter a valid amount.");
		return;
	}
	
	%client.god_donated_money += %money;
	%client.addMoney(-%money);
	
	MessageClient(%client, '', "\c3God \c6has accepted your donation of \c2$" @ %money @ "\c6.");
}

// this chooses the new pope based on how much money they've donated as a preist
// function god_findNewPope()
// {
	// cancel($City::TempGod::FindNewPopeSch);
	
	// if(isObject(GodSO.getPope()))
		// return;
	
	// %max = 0;
	// for(%i = 0; %i < ClientGroup.getCount(); %i++)
	// {
		// %client = ClientGroup.getObject(%i);
		
		// if(%client.god_donated_money > %max)
		// {
			// %new_pope = %client;
			// %max = %client.god_donated_money;
		// }
	// }
	
	// if(isObject(%new_pope))
	// {
		// %new_pope.setJob(City_PopeJob);
		// MessageAll('', "\c3God \c6has chosen \c3" @ %new_pope.getPlayerName() SPC "\c6to become the next \c3Pope\c6 for donating \c2$" @ %new_pope.god_donated_money @ "\c6.");
		// // MessageClient(%new_pope, '', "\c6God has chosen you to become the new pope because you sacrificed the most amount of money.");
	// }
	// else
	// {
		// for(%i = 0; %i < ClientGroup.getCount(); %i++)
		// {
			// %priest = ClientGroup.getObject(%i);
			
			// %priest.god_donated_money = 0;
			// MessageClient(%priest, '', "<font:Calibri bold:30>\c6There is no <color:9FEF65>Pope\c6! Sacrifice more money than your fellow citizens using <color:9FEF65>/donate\c6 to be chosen as the new <color:9FEF65>Pope\c6.");
		// }
		
		// $City::TempGod::FindNewPopeSch = schedule((60 * 1) * 1000, 0, god_findNewPope);
	// }
// }

function god_findNewPope(%nomsg)
{
	if(isObject(GodSO.getPope()))
		return;
	
	cancel($City::TempGod::FindNewPopeSch);
	
	if(!%nomsg)
		MessageAll('', "<font:Calibri bold:30>\c6The <color:9FEF65>Pope \c6has left! Apply for <color:9FEF65>Pope \c6in the GUI to become the next <color:9FEF65>Pope\c6!");
	
	$City::TempGod::FindNewPopeSch = schedule(120000, 0, god_findNewPope);
}

if(!isEventPending($City::TempGod::FindNewPopeSch) && !isObject(GodSO.getPope()))
	god_findNewPope();

// radio personas:
// Bob Dull: default guy, he's the most boring
// Bobblez Paihorslol: is a 12 year old who refuses to not chat cat faces and xd's
// Bob the Cat: cat puns only
// Bob Bantreudaux: only casts scientific explanations for what events are occuring
// Bob Biggums: sounds like he's on drugs all the time
