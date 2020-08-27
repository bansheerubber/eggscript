// all enemies have basic states: idle, seek, and attack. the states are defined using tagged fields

// %player.idleFOV						bot's fov
// %player.idleDrawDistance 			how far a bot can see
// %player.seekTimeout					how long a bot seeks until giving up if it hasn't seen the player
// %player.attackRange					determines how far away target has to be to trigger attack state

// %player.idleCleanup 					method that is called when we have to cleanup an idle transition
// %player.seekCleanup 					method that is called when we have to cleanup a seek transition
// %player.attackCleanup 				method that is called when we have to cleanup an attack transition
// %player.idle 						method that is called when we idle
// %player.seek 						method that is called when we seek
// %player.canFlank						method that determines if the bot can flank
// %player.onFlank						method that is called when a bot flanks
// %player.flankStopDistance			distance at which we stop flanking
// %player.attackRange					distance at which we switch to attack state
// %player.attack 						method that is called when we attack

$MD::AiIdle = 0;
$MD::AiSeek = 1;
$MD::AiAttack = 2;

function AiPlayer::onSpawn(%this, %roomIndex) {
	%this.spawnTime = getSimTime();
}

function AiPlayer::setAiState(%this, %state) {
	%this.ai = %this.schedule(33, _setAIState, %state);
}

function AiPlayer::_setAiState(%this, %state) {
	if(isObject(%this.ai)) {
		%this.ai.delete(); // handling wait schedule
	}
	else {
		cancel(%this.ai);
	}
	
	// cleanup
	if(%this.state != %state) {
		switch(%this.state) {
			case 0:
				%this.call(%this.idleCleanup, %state);
			
			case 1:
				%this.call(%this.seekCleanup, %state);
			
			case 2:
				%this.call(%this.attackCleanup, %state);
		}
	}
	
	switch(%state) {
		case 0:
			%this.call(%this.idle);

		case 1:
			%this.call(%this.seek);
		
		case 2:
			%this.call(%this.attack);
	}
	%this.state = %state;
}

function AiPlayer::talkForTime(%this, %time) {
	%this.playThread(3, "talk");
	%this.talkSchedule = %this.schedule(%time * 1000, playThread, 3, "root");
}

deActivatePackage(MiniDungeonsAI);
package MiniDungeonsAI {
	function AiPlayer::playDeathCry(%this) {
		if(%this.customDeathCry !$= "") {
			%this.playAudio(3, %this.customDeathCry);
			return;
		}

		%this.loseTarget();
		
		Parent::playDeathCry(%this);
	}

	function Armor::onDisabled(%this, %obj) {
		cancel(%obj.talkSchedule);

		if(%obj.getClassName() $= "AiPlayer") {
			if(
				isObject(%obj.target)
				&& isObject(%obj.target.client)
				&& %obj.reward
			) {
				%obj.target.client.addCurrency(%obj.reward);
			}
			
			%obj.loseTarget();

			if(%obj.room) {
				%obj.room.roomOnBotKilled(%obj);
			}
		}
		
		if(isObject(%obj.ai)) {
			%obj.ai.delete();
		}
		else {
			cancel(%obj.ai);
		}

		Parent::onDisabled(%this, %obj);
	}

	function Player::damage(%this, %col, %position, %damage, %damageType) {
		if(%this.state !$= "") {
			%this.target = %col;
		}
		
		Parent::damage(%this, %col, %position, %damage, %damageType);
	}
};
activatePackage(MiniDungeonsAI);