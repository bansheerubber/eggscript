function createNewBrick ( %data, %pos, %angID, %color, %plant, %group, %ignoreStuck, %ignoreFloat )
{
	// Make sure that the datablock exists and is even a brick datablock.
	if(!isObject (%data) || %data.getClassName () !$= "fxDTSBrickData")
	{
		createBrickError ($CreateBrick::Error::DataBlock, "Invalid datablock '" @ %data @ "'");
		return -1;
	}
}