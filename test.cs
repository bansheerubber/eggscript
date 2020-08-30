function Armor::Damage(%data, %obj, %sourceObject, %position, %damage, %damageType)
{
	if(%obj.getState() $= "Dead")
		return;

	if(getSimTime() - %obj.spawnTime < $Game::PlayerInvulnerabilityTime && !%obj.hasShotOnce)
		return;

	if((%obj.getMaxHealth() == 0 || %obj.getDatablock().invulnerable || %obj.isInvincible || %obj.invulnerable) && %damageType != $DamageType::Suicide)
	{
		if(isFunction(%obj.getClassName(), "sendHealthData"))
			%obj.sendHealthData(1);

		return;
	}

	if(%obj.isFallInvincible && (%damageType == $DamageType::Fall || %damageType == $DamageType::Impact))
		return;

	if(%obj.isMounted() && %damageType != $DamageType::Suicide && %data.rideAble == 0.0)
	{
		%mountData = %obj.getObjectMount().getDataBlock();
		if($Damage::Direct[%damageType] && %mountData.protectPassengersDirect)
			return;
		else if(!$Damage::Direct[%damageType] && %mountData.protectPassengersRadius)
			return;
	}

	if($Damage::Direct[%damageType] == 1)
	{
		%obj.lastDirectDamageType = %damageType;
		%obj.lastDirectDamageTime = getSimTime();
	}

	%obj.lastDamageType = %damageType;
	if (getSimTime() - %obj.lastPainTime > 300)
		%obj.painLevel = %damage;
	else
		%obj.painLevel += %damage;

	%obj.lastPainTime = getSimTime();
	if (%obj.isCrouched())
	{
		if ($Damage::Direct[%damageType])
			%damage *= 2.1;
		else
			%damage *= 0.75;
	}

	if(%damage != 0)
	{
		if(%obj.maxHealth > 0)
		{
			%obj.health -= %damage;
			%obj.lastDamageType = %damageType;

			%obj.health = mClampF(%obj.health, 0, %obj.maxHealth);
			%obj.setDamageLevel(%obj.getHealthLevel());
		}
		else
			%obj.applyDamage(%damage);
	}
	if(isFunction(%obj.getClassName(), "sendHealthData"))
		%obj.sendHealthData(0);

	%location = "Body";
	%client = %obj.client;
	if(isObject(%sourceObject))
	{
		if(%sourceObject.getClassName() $= "GameConnection")
			%sourceClient = %sourceObject;
		else
			%sourceClient = %sourceObject.client;
	}
	else
		%sourceClient = 0;

	if(isObject(%sourceObject) && (%sourceObject.getType() & $TypeMasks::VehicleObjectType) && %sourceObject.getControllingClient())
		%sourceClient = %sourceObject.getControllingClient();

	if(%obj.getState() $= "Dead")
	{
		if(isObject(%client))
			%client.onDeath(%sourceObject, %sourceClient, %damageType, %location);
		else if(isObject(%obj.spawnBrick))
		{
			%mg = getMiniGameFromObject(%sourceObject);
			if(isObject(%mg))
				%obj.spawnBrick.spawnVehicle(%mg.VehicleRespawnTime);
			else
				%obj.spawnBrick.spawnVehicle(5000);
		}
	}
	else
	{
		if(%data.useCustomPainEffects == 1)
		{
			if(%obj.painLevel >= 40)
			{
				if(isObject(%data.PainHighImage))
					%obj.emote(%data.PainHighImage, 1);
			}
			else
			{
				if(%obj.painLevel >= 25)
				{
					if(isObject(%data.PainMidImage))
						%obj.emote(%data.PainMidImage, 1);
				}
				else
				{
					if (isObject(%data.PainLowImage))
						%obj.emote(%data.PainLowImage, 1);
				}
			}
		}
		else
		{
			if(%obj.painLevel >= 40)
				%obj.emote(PainHighImage, 1);
			else
			{
				if(%obj.painLevel >= 25)
					%obj.emote(PainMidImage, 1);
				else
					%obj.emote(PainLowImage, 1);
			}
		}
	}
}

deactivatepackage("Support_CustomHealth");
package Support_CustomHealth
{
	function Player::setHealth(%this, %health)
	{
		if(!isObject(%this))
			return false;

		if(!strLen(%health))
			return false;

		if(%this.getMaxHealth() == 0 || %this.getDatablock().invulnerable || %this.isInvincible || %this.invulnerable)
		{
			if(isFunction(%this.getClassName(), "sendHealthData"))
				%this.sendHealthData(1);

			return true;
		}

		if(%this.maxHealth <= 0)
		{
			Parent::setHealth(%this, %health);
			return true;
		}

		if(%health < 0)
		{
			%health = 0;
			%this.health = 0;
			%this.damage(%this, %this.getPosition(), %this.getDatablock().maxDamage * %this.getSize(), $DamageType::Default, "body", true);
			return true;
		}

		%health = mClampF(%health, 0, %this.getMaxHealth());

		%this.health = %health;
		%this.setDamageLevel(%this.getHealthLevel());

		return true;
	}

	function Player::AddHealth(%this, %health)
	{
		if(!isObject(%this))
			return false;

		if(%this.getMaxHealth() == 0 || %this.getDatablock().invulnerable || %this.isInvincible || %this.invulnerable)
		{
			if(%health > 0)
				%this.setHealth(%this.getHealth() + %health);
			
			if(isFunction(%this.getClassName(), "sendHealthData"))
				%this.sendHealthData(1);

			return true;
		}

		if(%this.maxHealth <= 0)
		{
			Parent::AddHealth(%this, %health);
			return true;
		}

		if(%this.health > 0)
		{
			if(%health < 0)
				%this.damage(%this, %this.getPosition(), mAbs(%health), $DamageType::Default, "body", false);
			else
				%this.setHealth(%this.getHealth() + %health);
		}

		if(%this.health <= 0)
		{
			%this.health = 0;
			%this.damage(%this, %this.getPosition(), %this.getMaxHealth() * %this.getSize(), %damageType, "body", true);
		}

		return true;
	}

	function AIPlayer::setHealth(%this,%health)
	{
		if(!isObject(%this))
			return false;

		if(!strLen(%health))
			return false;

		if(%this.getMaxHealth() == 0 || %this.getDatablock().invulnerable || %this.isInvincible || %this.invulnerable)
			return true;

		if(%this.maxHealth <= 0)
		{
			Parent::setHealth(%this, %health);
			return true;
		}

		if(%health < 0)
		{
			%health = 0;
			%this.health = 0;
			%this.damage(%this, %this.getPosition(), %this.getDatablock().maxDamage * %this.getSize(), $DamageType::Default, "body", true);
			return true;
		}

		%health = mClampF(%health, 0, %this.getMaxHealth());

		%this.health = %health;
		%this.setDamageLevel(%this.getHealthLevel());

		return true;
	}

	function AIPlayer::AddHealth(%this,%health)
	{
		if(!isObject(%this))
			return false;

		if(%this.getMaxHealth() == 0 || %this.getDatablock().invulnerable || %this.isInvincible || %this.invulnerable)
			return true;

		if(%this.maxHealth <= 0)
		{
			Parent::AddHealth(%this, %health);
			return true;
		}

		if(%this.health > 0)
		{
			if(%health < 0)
				%this.damage(%this, %this.getPosition(), mAbs(%health), $DamageType::Default, "body", false);
			else
				%this.setHealth(%this.getHealth() + %health);
		}

		if(%this.health <= 0)
		{
			%this.health = 0;
			%this.damage(%this, %this.getPosition(), %this.getMaxHealth() * %this.getSize(), %damageType, "body", true);
		}

		return true;
	}
	
	function ShapeBase::kill(%this, %damageType, %last)
	{
		if(!isObject(%this))
			return false;

		if(getSimTime() - %this.spawnTime < $Game::PlayerInvulnerabilityTime)
			return false;
		
		if(!strLen(%damageType))
			%damageType = $DamageType::Suicide;
		
		if(!isObject(%last))
			%last = %this;

		%this.health = 0;
		%this.damage(%last, %this.getPosition(), %this.getMaxHealth() * %this.getSize(), %damageType, "body");
	}
	
	function Armor::onNewDatablock(%data, %obj)
	{
		Parent::onNewDatablock(%data, %obj);
		if(%obj.maxHealth > 0)
			%obj.setDamageLevel(%obj.getHealthLevel());
	}

	function ShapeBase::applyImpulse(%this, %origin, %velocity)
	{
		if(%this.getMaxHealth() == 0 || %this.getDatablock().invulnerable || %this.isInvincible || %this.invulnerable)
			return;

		Parent::applyImpulse(%this, %origin, %velocity);
	}
};
schedule(0,0,activatePackage,"Support_CustomHealth");

//Gets the size of the object
function ShapeBase::getSize(%this)
{
	if(!isObject(%this))
		return -1;

	return getWord(%this.getScale(), 2);
}

function ShapeBase::addMaxHealth(%this, %maxHealth, %bool)
{
	if(!isObject(%this))
		return -1;

	if(!strLen(%maxHealth))
		return false;

	//If we are adding max health, make sure we have it first
	if(%this.maxHealth < 0 || %this.maxHealth $= "")
	{
		%this.maxHealth = %this.getDatablock().maxDamage;
		%this.health = %this.getDatablock().maxDamage - %this.getDamageLevel();
	}

	%this.maxHealth = mClampF(%this.maxHealth + %maxHealth, 1, 999999);
	if(%bool)
		%this.health = %this.maxHealth;
	else
		%this.health += %maxHealth;

	%this.oldMaxHealth = %this.maxHealth;
	%this.oldHealth = %this.health;

	%this.setDamageLevel(%this.getHealthLevel());

	return true;
}

function GameConnection::setMaxHealth(%this, %maxHealth, %bypass)
{
	if(!isObject(%this))
		return -1;

	if(mFloor(%maxHealth) <= 0 && !%bypass)
		return false;

	%this.maxHealth = mClampF(%maxHealth, 0, 999999);
	if(isObject(%player = %this.player))
		%player.setMaxHealth(%this.maxHealth, %bypass);

	return true;
}

function ShapeBase::setMaxHealth(%this, %maxHealth, %bypass)
{
	if(!isObject(%this))
		return -1;

	if(mFloor(%maxHealth) <= 0 && !%bypass)
		return false;

	%this.maxHealth = mClampF(%maxHealth, 0, 999999);

	%this.health = %this.maxHealth;
	%this.oldMaxHealth = %this.maxHealth;
	%this.oldHealth = %this.health;
	%this.setDamageLevel(0);
	if(isFunction(%this.getClassName(), "sendHealthData"))
		%this.sendHealthData(%this.getMaxHealth() == 0 || %this.getDatablock().invulnerable || %this.isInvincible || %this.invulnerable);

	return true;
}

function ShapeBase::setFInvulnerbilityTime(%this, %time)
{
	%this.setFInvulnerbility(true);
	if(%time > 0)
		%this.vulFallWasteSch = %this.schedule(%time * 1000, setFInvulnerbility, false);
}

function ShapeBase::setFInvulnerbility(%this, %val)
{
	cancel(%this.vulFallWasteSch);
	%this.isFallInvincible = %val;
}

function ShapeBase::setInvulnerbilityTime(%this, %time)
{
	%this.setInvulnerbility(true);
	if(%time > 0)
		%this.vulWasteSch = %this.schedule(%time * 1000, setInvulnerbility, false);
}

function ShapeBase::setInvulnerbility(%this, %val)
{
	cancel(%this.vulWasteSch);
	%this.isInvincible = %val;
	%this.invulnerable = %val;
	if(isFunction(%this.getClassName(), "sendHealthData"))
		%this.sendHealthData(%val);
}

function ShapeBase::getHealth(%this)
{
	if(!isObject(%this))
		return -1;

	if(%this.maxHealth !$= "" && %this.maxHealth >= 0)
	{
		if(%this.health $= "")
			return 0;

		return %this.health;
	}

	return %this.getDatablock().maxDamage - %this.getDamageLevel();
}

function ShapeBase::getMaxHealth(%this)
{
	if(!isObject(%this))
		return -1;

	if(%this.maxHealth !$= "" && %this.maxHealth >= 0)
		return %this.maxHealth;

	return %this.getDatablock().maxDamage;
}

function ShapeBase::getHealthLevel(%this) //This is used to set their damage level, which is opposite of their health, aka ShapeBase::getDamageLevel()
{
	if(%this.getMaxHealth() == 0)
		return 0;

	%maxDmg = %this.getDatablock().maxDamage;
	%level = %maxDmg - (%maxDmg / %this.getMaxHealth() * %this.getHealth());
	//Make sure we don't break the scale
	%level = mClampF(%level, 0, %maxDmg);

	return %level;
}