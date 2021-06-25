import pymem, requests, re, time

def read_game():
	global pm, client, engine, connect

	global dwLocalPlayer, dwGlowObjectManager, dwEntityList, dwClientState, dwClientState_ViewAngles, dwForceAttack, dwForceJump, dwbSendPackets, dwInput
	global m_iTeamNum, m_iGlowIndex, m_iHealth, m_clrRender, m_bUseCustomAutoExposureMin, m_bUseCustomAutoExposureMax, m_flCustomAutoExposureMin, m_flCustomAutoExposureMax, m_iDefaultFOV, m_bSpottedByMask, m_dwBoneMatrix, m_vecOrigin, m_vecViewOffset, m_bDormant, m_aimPunchAngle, m_iShotsFired, m_iCrosshairId, m_hMyWeapons, m_iItemDefinitionIndex, m_OriginalOwnerXuidLow, m_iItemIDHigh, m_nFallbackPaintKit, m_iAccountID, m_nFallbackStatTrak, m_nFallbackSeed, m_flFallbackWear, m_fFlags, m_flFlashMaxAlpha, model_ambient_min
	global clientstate_net_channel, clientstate_last_outgoing_command

	connect = False

	while not connect:

		try:
			pm = pymem.Pymem("csgo.exe")
			client = pymem.process.module_from_name(pm.process_handle, "client.dll").lpBaseOfDll
			engine = pymem.process.module_from_name( pm.process_handle, "engine.dll" ).lpBaseOfDll
		except:
			time.sleep(0.5)
			continue

		try:
			def get_sig(modname, pattern, extra = 0, offset = 0, relative = True):
			    module = pymem.process.module_from_name(pm.process_handle, modname)
			    bytes = pm.read_bytes(module.lpBaseOfDll, module.SizeOfImage)
			    match = re.search(pattern, bytes).start()
			    non_relative = pm.read_int(module.lpBaseOfDll + match + offset) + extra
			    yes_relative = pm.read_int(module.lpBaseOfDll + match + offset) + extra - module.lpBaseOfDll
			    return "0x{:X}".format(yes_relative) if relative else "0x{:X}".format(non_relative)
		except:
			time.sleep(0.5)
			continue

		try:
			offsets = 'https://raw.githubusercontent.com/frk1/hazedumper/master/csgo.json'
			response = requests.get(offsets).json()

			dwLocalPlayer = int(get_sig('client.dll', rb'\x8D\x34\x85....\x89\x15....\x8B\x41\x08\x8B\x48\x04\x83\xF9\xFF', 4, 3), 0)
			dwGlowObjectManager = int(get_sig('client.dll', rb'\xA1....\xA8\x01\x75\x4B', 4, 1),0)
			dwEntityList = int(get_sig('client.dll',rb'\xBB....\x83\xFF\x01\x0F\x8C....\x3B\xF8',0,1),0)
			dwForceAttack = int(get_sig('client.dll', rb'\x89\x0D....\x8B\x0D....\x8B\xF2\x8B\xC1\x83\xCE\x04', 0, 2), 0)
			dwForceJump = int(get_sig('client.dll', rb'\x8B\x0D....\x8B\xD6\x8B\xC1\x83\xCA\x02', 0, 2), 0)
			dwClientState = int(response["signatures"]["dwClientState"])
			dwClientState_ViewAngles = int(response["signatures"]["dwClientState_ViewAngles"])
			dwbSendPackets = int(response["signatures"]["dwbSendPackets"])
			dwInput = int(response["signatures"]["dwInput"])

			clientstate_net_channel = int(response["signatures"]["clientstate_net_channel"])
			clientstate_last_outgoing_command = int(response["signatures"]["clientstate_last_outgoing_command"])

			m_iTeamNum = int(response["netvars"]["m_iTeamNum"])
			m_iGlowIndex = int(response["netvars"]["m_iGlowIndex"])
			m_iHealth = int(response["netvars"]["m_iHealth"])
			m_clrRender = int(response["netvars"]["m_clrRender"])
			m_bUseCustomAutoExposureMin = int(response["netvars"]["m_bUseCustomAutoExposureMin"])
			m_bUseCustomAutoExposureMax = int(response["netvars"]["m_bUseCustomAutoExposureMax"])
			m_flCustomAutoExposureMin = int(response["netvars"]["m_flCustomAutoExposureMin"]) 
			m_flCustomAutoExposureMax = int(response["netvars"]["m_flCustomAutoExposureMax"])
			m_bSpottedByMask = int(response["netvars"]["m_bSpottedByMask"])
			m_dwBoneMatrix = int(response["netvars"]["m_dwBoneMatrix"])
			m_vecOrigin = int(response["netvars"]["m_vecOrigin"])
			m_vecViewOffset = int(response["netvars"]["m_vecViewOffset"])
			m_bDormant = int(response["signatures"]["m_bDormant"])
			m_aimPunchAngle = int(response["netvars"]["m_aimPunchAngle"])
			m_iShotsFired = int(response["netvars"]["m_iShotsFired"])
			m_iCrosshairId = int(response["netvars"]["m_iCrosshairId"])
			m_hMyWeapons = int(response["netvars"]["m_hMyWeapons"])
			m_iItemDefinitionIndex = int(response["netvars"]["m_iItemDefinitionIndex"])
			m_OriginalOwnerXuidLow = int(response["netvars"]["m_OriginalOwnerXuidLow"])
			m_iItemIDHigh = int(response["netvars"]["m_iItemIDHigh"])
			m_nFallbackPaintKit = int(response["netvars"]["m_nFallbackPaintKit"])
			m_iAccountID = int(response["netvars"]["m_iAccountID"])
			m_nFallbackStatTrak = int(response["netvars"]["m_nFallbackStatTrak"])
			m_nFallbackSeed = int(response["netvars"]["m_nFallbackSeed"])
			m_flFallbackWear = int(response["netvars"]["m_flFallbackWear"])
			m_fFlags = int(response["netvars"]["m_fFlags"])
			m_flFlashMaxAlpha = int(response["netvars"]["m_flFlashMaxAlpha"])
			model_ambient_min = int(response["signatures"]["model_ambient_min"])
			m_hActiveWeapon = int(response["netvars"]["m_hActiveWeapon"])
			m_iDefaultFOV = 0x332C
		except:
			time.sleep(0.5)
			continue

		connect = True

read_game()