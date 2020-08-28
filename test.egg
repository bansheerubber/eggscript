datablock AudioProfile(GladiusDeath1Sound) {
	filename    = "./sounds/gladius death1.wav";
	description = AudioDefault3d;
	preload = true;
};

datablock AudioProfile(GladiusDeath2Sound) {
	filename    = "./sounds/gladius death2.wav";
	description = AudioDefault3d;
	preload = true;
};

datablock AudioProfile(GladiusDeath3Sound) {
	filename    = "./sounds/gladius death3.wav";
	description = AudioDefault3d;
	preload = true;
};

function createGladiusAi(%transform, %roomIndex) {
	%ai = new AiPlayer() {
		datablock = MiniDungeonsArmor;
		position = getWords(%transform, 0, 2);
		rotation = "0 0 0 1";

		idleDrawDistance = 200;
		idleThirdSenseDistance = 5;
		idleFOV = 360;
		attackRange = 7;
		idle = "idle";
		seek = "seek";
		canFlank = "gladiusCanFlank";
		onFlank = "gladiusOnFlank";
		flankStopDistance = 5; // distance at which we stop flanking
		attack = "gladiusAttack";

		idleCleanup = "idleCleanup";
		seekCleanup = "gladiusSeekCleanup";
		attackCleanup = "gladiusAttackCleanup";

		reward = 1;

		seekHeightCheck = true;

		customDeathCry = "GladiusDeath" @ getRandom(1, 3) @ "Sound";

		isEnemyAi = true;
		isBot = true;

		name = generateRandomName();
	};
	%ai.setTransform(%transform);
	%ai.setAIState($MD::AiIdle);
	%ai.setMaxSideSpeed(MiniDungeonsArmor.maxForwardSpeed);

	%ai.setShapeName(%ai.name, 8564862);
	%ai.setShapeNameDistance(50);

	GladiusSwordArmor.mount(%ai, 0);

	%ai.setAvatar("gladius");

	%ai.onSpawn(%roomIndex);

	return %ai;
}

function AiPlayer::gladiusAttack(%this) {
	if(!%this.hasValidTarget()) {
		%this.loseTarget();
		%this.setAiState($MD::AiIdle);
		return;
	}

	%targetPosition = %this.target.getPosition();
	%position = %this.getPosition();

	if(
		getSimTime() > %this.nextGladiusAttack
		&& mAbs(getWord(%targetPosition, 2) - getWord(%position, 2)) < 2
	) {
		%this.setSwordTrigger(0, true);
		%this.schedule(1400, setSwordTrigger, 0, false);

		%this.setAimObject(%this.target);
		%this.setMoveX(getRandom(0, 1) ? -0.3 : 0.3);
		%this.setMoveY(0.4);

		%this.playThread(0, "plant");
		
		%this.nextGladiusAttack = getSimTime() + 2000;
		%this.nextGladiusMove = getSimTime() + 1000;
		%this.gladiusMoveX = getRandom(0, 1) ? -1 : 1;
	}

	if(getSimTime() > %this.nextGladiusMove) {
		%raycast = containerRaycast(%this.getEyePoint(), %this.target.getHackPosition(), $TypeMasks::fxBrickObjectType | $TypeMasks::PlayerObjectType, %this);
		if(vectorDist(%targetPosition, %position) > %this.attackRange || getWord(%raycast, 0) != %this.target) {
			%this.setAiState($MD::AiSeek);
			return;
		}
		
		%this.setMoveX(%this.gladiusMoveX);
		%this.setMoveY(0);
	}

	%this.ai = %this.schedule(100, gladiusAttack);
}

function AiPlayer::gladiusAttackCleanup(%this, %state) {
	// %this.setMoveX(0);
	// %this.setMoveY(0);

	%this.attackCleanup();
}

function AiPlayer::gladiusSeekCleanup(%this, %state) {
	if(getSimTime() > %this.nextGladiusAttack && %this.aiSuprise) {
		%this.nextGladiusAttack = getSimTime() + 500;
		%this.nextGladiusMove = getSimTime();
	}

	%this.seekCleanup();
}

function AiPlayer::gladiusCanFlank(%this) {
	if(isObject(%this.target)) {
		%targetPosition = %this.target.getPosition();
		%position = %this.getPosition();

		if(vectorDist(%targetPosition, %position) < 20) {
			return !%this.gladiusHasFlanked;
		}
		else if(vectorDist(%targetPosition, %position) > 35) {
			%this.gladiusHasFlanked = false;
			return false;
		}
		else {
			return false;
		}
	}
	else {
		return false;
	}
}

function AiPlayer::gladiusOnFlank(%this) {
	%this.gladiusHasFlanked = true;
}