// we only seek if we have a target. if no target, then return to idle state. transition to attack state when we are within attack range
function AiPlayer::seek(%this) {
	if(!%this.hasValidTarget()) {
		%this.loseTarget();
		%this.setAiState($MD::AiIdle);
		return;
	}

	%position = %this.getHackPosition();
	%targetPosition = %this.target.getHackPosition();

	%raycast = containerRaycast(
		%this.getEyePoint(),
		%targetPosition,
		$TypeMasks::fxBrickObjectType,
		false
	);

	if(
		(
			isObject(%raycast) // if we cannot see our target
			||
			( // if our target is above us
				%this.seekHeightCheck
				&& %this.target.isGrounded
				&& getWord(%targetPosition, 2) - getWord(%position, 2) > 3
			)
		)
		&& getSimTime() > %this.nextPathAttempt
	) {
		if(isObject(%raycast)) {
			%this.alarmEmote = false;
		}
		else {
			%this.alarmEmote = true;
		}
		
		if(!%this.hasPath()) { // if we have no path, then get one. wait around until we have one
			%this.setAimObject(%this.target);

			%closestNode = getClosestNode(%position);
			%targetClosestNode = getClosestNode(%targetPosition);

			// if we couldn't find nodes, then try just normal pathing stuff for a little
			if(%closestNode == -1 || %targetClosestNode == -1) {
				%this.ai = %this.waitSchedule(300, seek);
				%this.nextPathAttempt = getSimTime() + 5000;
				return;
			}

			%this.requestPath(%closestNode, %targetClosestNode);
			%this.nextPathRequest = getSimTime() + 10000;
			%this.lastPathRequest = getSimTime();
			
			%this.ai = %this.waitSchedule(500, seek).addMethodCondition(%this, "hasPathOrTimeout", true);
			
			return;
		}
		else { // iterate through the path
			if(getSimTime() > %this.nextPathRequest) {
				%closestNode = getClosestNode(%position);
				%targetClosestNode = getClosestNode(%targetPosition);
				%this.requestPath(%closestNode, %targetClosestNode);
				%this.nextPathRequest = getSimTime() + 10000;
			}
			
			%nextPosition = %this.path[%this.currentPathIndex];

			// skip over nodes that we can see
			// while(
			// 	(%raycast = containerRaycast(
			// 		%position,
			// 		%nextPosition,
			// 		$TypeMasks::fxBrickObjectType,
			// 		0)
			// 	)
			// 	&& (
			// 		%raycast.getName() $= "_node"
			// 		|| %raycast.getDatablock().getName() $= "BrickPathfindingNodeData"
			// 	)
			// 	&& %this.currentPathIndex < %this.pathCount
			// 	&& mAbs(getWord(%nextPosition, 2) - getWord(%position, 2)) < 3
			// ) {
			// 	%this.currentPathIndex++;
			// 	%nextPosition = %this.path[%this.currentPathIndex];
			// }

			// %this.currentPathIndex--;
			// %nextPosition = %this.path[%this.currentPathIndex];
			
			if(vectorDist(%this.getPosition(), %nextPosition) < 3) { // if we're close to the next node, then increment the path
				%this.currentPathIndex++;
				%nextPosition = %this.path[%this.currentPathIndex];
			}

			// if we're standing ontop of a player, stop for a second so we dismount
			if(
				isObject(
					containerRaycast(
						%this.getPosition(),
						vectorAdd(%this.getPosition(), "0 0 -1"),
						$TypeMasks::PlayerObjectType,
						%this
					)
				)
			) {
				%this.setMoveX(0);
				%this.setMoveY(0);
			}
			else if(%this.currentPathIndex >= %this.pathCount) { // if we've run out of path, then reset the path
				%this.resetPath();
			}
			else {
				%this.setAimVector(
					vectorNormalize(
						getWords(
							vectorSub(%nextPosition, %this.getPosition()),
							0, 1
						)
					)
				);
				%this.setMoveY(1);
			}
		}

		%this.lastPathTick = getSimTime();
	}
	else {
		%this.aiSuprise = false; // reset the suprise every tick
		if(!%this.alarmEmote && getSimTime() > %this.nextAlarmEmote) {
			%this.alarmEmote = true;
			%this.emote(AlarmProjectile);

			if(!%this.noJumpOnAlert) {
				%this.setJumping(true);
				%this.schedule(33, setJumping, false);
			}
			%this.aiSuprise = true; // if we are suprised and we are close enough to switch to the attack state, this variable will be remembered and utilized

			%this.nextAlarmEmote = getSimTime() + 6000;
		}
		else {
			%this.alarmEmote = true;
		}
		
		if(%this.hasPath()) {
			%this.resetPath();
		}

		if(
			isObject(
				containerRaycast(
					%this.getPosition(),
					vectorAdd(%this.getPosition(), "0 0 -1"),
					$TypeMasks::PlayerObjectType,
					%this
				)
			)
		) {
			%this.setMoveX(0);
			%this.setMoveY(0);
		}
		else {
			%position = %this.getPosition();
			%targetPosition = %this.target.getPosition();
			
			// setup flanking
			if(
				!%this.isFlanking
				&& %this.canFlank !$= "" &&
				%this.call(%this.canFlank)
			) {
				%forwardVector = %this.target.getForwardVector();
				%angle = mATan(
					getWord(%forwardVector, 0),
					getWord(%forwardVector, 1)
				);
				// %radius = vectorDist(%position, %targetPosition) * 0.6;
				%radius = 10;
				%x1 = mSin(%angle - $pi / 2) * %radius;
				%y1 = mCos(%angle - $pi / 2) * %radius;
				%position1 = vectorAdd(%targetPosition, %x1 SPC %y1 SPC "0");

				%x2 = mSin(%angle + $pi / 2) * %radius;
				%y2 = mCos(%angle + $pi / 2) * %radius;
				%position2 = vectorAdd(%targetPosition, %x2 SPC %y2 SPC "0");

				// if position2 is closer than position 1, then head to position2
				if(vectorDist(%position, %position1) > vectorDist(%position, %position2)) {
					%this.flankAngle = $pi / 2;
				}
				else {
					%this.flankAngle = -$pi / 2;
				}

				%this.call(%this.onFlank);

				%this.flankForwardVector = %forwardVector;
				%this.flankRadius = 10;

				%this.flankStopTime = getSimTime() + 5000; // imeditally stop flanking if we've been trying to for the last 5 seconds

				%this.isFlanking = true;
			}

			if(%this.isFlanking) {
				%angle = mATan(
					getWord(%this.flankForwardVector, 0),
					getWord(%this.flankForwardVector, 1)
				);
				%x1 = mSin(%angle + %this.flankAngle) * %this.flankRadius;
				%y1 = mCos(%angle + %this.flankAngle) * %this.flankRadius;
				%flankPosition = vectorAdd(%targetPosition, %x1 SPC %y1 SPC "0");
				
				// calculate correct heading based off of targets current position
				%flankVector = vectorNormalize(
					getWords(
						vectorSub(%flankPosition, %position),
						0, 1
					)
				);

				// if we have a wall in the way, then stop flanking
				%raycast = containerRaycast(
					%position,
					vectorAdd(%position, vectorScale(%flankVector, 4)),
					$TypeMasks::fxBrickObjectType,
					false
				);

				if(
					isObject(%raycast)
					|| vectorDist(%flankPosition, %position) < 3
					|| vectorDist(%position, %targetPosition) < %this.flankStopDistance
					|| getSimTime() > %this.flankStopTime
				) {
					%this.setAimObject(%this.target);
					%this.setMoveY(1);
					%this.isFlanking = false;
				}
				else {
					%this.setAimVector(%flankVector);
					%this.setMoveY(1);
				}
			}
			else {
				%this.setMoveX(0);
				%this.setMoveY(1);
				%this.setAimObject(%this.target);
			}
		}

		if(
			vectorDist(
				%targetPosition,
				%this.getPosition()
			) < %this.attackRange
			&& getSimTime() - %this.lastPathTick > 200
		) {
			%this.setAiState($MD::AiAttack);
			return;
		}
	}

	%this.ai = %this.schedule(300, seek);
}