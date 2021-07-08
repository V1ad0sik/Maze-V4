from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QColorDialog
from PIL import ImageColor
from module.game_module import *
from module.gui import *
from module.data import *
from threading import Thread
from math import *
from win32api import GetKeyState
from win32gui import GetWindowText, GetForegroundWindow

import pymem, time, keyboard, numpy, math, configparser, psutil, os

_translate = QtCore.QCoreApplication.translate

class Widget(QtWidgets.QWidget, Ui_Form):
    def __init__(self, parent=None):
        super(Widget, self).__init__(parent)
        self.setupUi(self)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            x_main, y_main = self.geometry().x(), self.geometry().y()
            cursor_x, cursor_y = QtGui.QCursor.pos().x(), QtGui.QCursor.pos().y()

            if x_main <= cursor_x <= x_main + self.geometry().width():
                if y_main <= cursor_y <= y_main + self.geometry().height():
                    self.old_pos = event.pos()
                else:
                    self.old_pos = None
        elif event.button() == QtCore.Qt.RightButton:
            self.old_pos = None

    def mouseReleaseEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.old_pos = None

    def mouseMoveEvent(self, event):
        try:
                if not self.old_pos:
                    return
                delta = event.pos() - self.old_pos
                self.move(self.pos() + delta)
        except:
                pass

def ESP():
   while ESP_Status:
    try:
          glow_manager = pm.read_int(client + dwGlowObjectManager)

          for i in range(1, 32):
             entity = pm.read_int(client + dwEntityList + i * 0x10)

             if entity:
                entity_glow = pm.read_int(entity + m_iGlowIndex)

                if HP_ESP_Status == True:

                    entity_hp = pm.read_int(entity + m_iHealth)
                    if entity_hp > 60:
                            R, G, B = ESP_R / 255, ESP_G / 255, ESP_B / 255
                    if entity_hp < 40:
                            R, G, B = 1,1,0
                    if entity_hp < 20 and entity_hp > 0:
                            R, G, B = 1,0,0
                else:
                    R, G, B = ESP_R / 255, ESP_G / 255, ESP_B / 255

                if pm.read_int(entity + m_iTeamNum) != pm.read_int((pm.read_int(client + dwLocalPlayer)) + m_iTeamNum):
                    pm.write_float(glow_manager + entity_glow * 0x38 + 0x8, float(R))
                    pm.write_float(glow_manager + entity_glow * 0x38 + 0xC, float(G))
                    pm.write_float(glow_manager + entity_glow * 0x38 + 0x10, float(B))
                    pm.write_float(glow_manager + entity_glow * 0x38 + 0x14, line)

                    pm.write_int(glow_manager + entity_glow * 0x38 + 0x28, 1)

          time.sleep(0.01)
    except:
        continue

def Distance_ESP():
    while Distance_ESP_Status:
        try:
            glow_manager = pm.read_int(client + dwGlowObjectManager)
            localPlayer = pm.read_int(client + dwLocalPlayer)
            closestPlayer = 99999.0

            for i in range(1, 32):
                ent = pm.read_int(client + dwEntityList + i * 0x10) 

                if ent:
                    entity_glow = pm.read_int(ent + m_iGlowIndex)

                    distance = math.sqrt((pow(((pm.read_float(ent + m_vecOrigin)) - (pm.read_float(localPlayer + m_vecOrigin))), 2) + pow(((pm.read_float(ent + m_vecOrigin + 0x4)) - (pm.read_float(localPlayer + m_vecOrigin + 0x4))), 2) + pow(((pm.read_float(ent + m_vecOrigin + 0x8)) - (pm.read_float(localPlayer + m_vecOrigin + 0x8))), 2)))

                    if pm.read_int(localPlayer + m_iTeamNum) != pm.read_int(ent + m_iTeamNum) and closestPlayer > distance:
                        closestPlayer = distance

                    if closestPlayer < enit_distance:
                        R, G, B = ESP_R / 255, ESP_G / 255, ESP_B / 255

                        if pm.read_int(ent + m_iTeamNum) != pm.read_int((localPlayer) + m_iTeamNum):
                            pm.write_float(glow_manager + entity_glow * 0x38 + 0x4, float(R))
                            pm.write_float(glow_manager + entity_glow * 0x38 + 0x8, float(G))
                            pm.write_float(glow_manager + entity_glow * 0x38 + 0xC, float(B))
                            pm.write_float(glow_manager + entity_glow * 0x38 + 0x10, line)
                            pm.write_int(glow_manager + entity_glow * 0x38 + 0x24, 1)

                    time.sleep(0.01)
        except:
            continue

def Chams():
    while Chams_status:
        try:
            for ent_id in range(1, 32):
                ent = pm.read_int(client + dwEntityList + ent_id * 0x10)

                if ent:
                    if pm.read_int(ent + m_iTeamNum) != pm.read_int((pm.read_int(client + dwLocalPlayer)) + m_iTeamNum):
                        pm.write_int(ent + m_clrRender, Chams_R)
                        pm.write_int(ent + m_clrRender + 1, Chams_G)
                        pm.write_int(ent + m_clrRender + 2, Chams_B)
                        pm.write_int(ent + m_clrRender + 3, 1)

            time.sleep(0.1)
        except:
            pass

def Chams_Reset():
    try:
        for ent_id in range(1, 32):
            ent = pm.read_int(client + dwEntityList + ent_id * 0x10)

            if ent:
                if pm.read_int(ent + m_iTeamNum) != pm.read_int((pm.read_int(client + dwLocalPlayer)) + m_iTeamNum):
                    pm.write_int(ent + m_clrRender, 255)
                    pm.write_int(ent + m_clrRender + 1, 255)
                    pm.write_int(ent + m_clrRender + 2, 255)
                    pm.write_int(ent + m_clrRender + 3, 1)
    except:
        pass

def Night_Mod():
    while Night_Mod_Status:
        try:
            for i in range(0, 2048):
                entity = pm.read_uint(client + dwEntityList + i * 0x10)
                if entity:
                    EntityClassID = pm.read_int(entity + 0x8)
                    a = pm.read_int(EntityClassID + 2 * 0x4)
                    b = pm.read_int(a + 0x1)
                    c = pm.read_int(b + 20)

                    if (c != 69):
                        continue
                    
                    if (True):
                        pm.write_int(entity + m_bUseCustomAutoExposureMin, 1)
                        pm.write_int(entity + m_bUseCustomAutoExposureMax, 1)
                        pm.write_float(entity + m_flCustomAutoExposureMin, Night_Mod_value)
                        pm.write_float(entity + m_flCustomAutoExposureMax, Night_Mod_value)
                    else:
                        pm.write_bool(entity + m_bUseCustomAutoExposureMin, 0)
                        pm.write_bool(entity + m_bUseCustomAutoExposureMax, 0)
        except:
            continue

def Night_Mod_Reset():
    try:
        for i in range(0, 2048):
            entity = pm.read_uint(client + dwEntityList + i * 0x10)
            if entity:
                EntityClassID = pm.read_int(entity + 0x8)
                a = pm.read_int(EntityClassID + 2 * 0x4)
                b = pm.read_int(a + 0x1)
                c = pm.read_int(b + 20)

                if (c != 69):
                    continue
                
                if (True):
                    pm.write_int(entity + m_bUseCustomAutoExposureMin, 1)
                    pm.write_int(entity + m_bUseCustomAutoExposureMax, 1)
                    pm.write_float(entity + m_flCustomAutoExposureMin, 1.0)
                    pm.write_float(entity + m_flCustomAutoExposureMax, 1.0)
                else:
                    pm.write_bool(entity + m_bUseCustomAutoExposureMin, 0)
                    pm.write_bool(entity + m_bUseCustomAutoExposureMax, 0)
    except:
        pass

def Game_WH():
    try:
        pm = pymem.Pymem('csgo.exe')
        client = pymem.process.module_from_name(pm.process_handle,'client.dll')
        clientModule = pm.read_bytes(client.lpBaseOfDll, client.SizeOfImage)
        address = client.lpBaseOfDll + re.search(rb'\x83\xF8.\x8B\x45\x08\x0F',clientModule).start() + 2
        pm.write_uchar(address, 2 if pm.read_uchar(address) == 1 else 1)
        pm.close_process()
    except:
        pass

def calc_distance(current_x, current_y, new_x, new_y):
    distancex = new_x - current_x
    if distancex < -89:
        distancex += 360
    elif distancex > 89:
        distancex -= 360
    if distancex < 0.0:
        distancex = -distancex

    distancey = new_y - current_y

    if distancey < -180:
        distancey += 360
    elif distancey > 180:
        distancey -= 360
    if distancey < 0.0:
        distancey = -distancey
    return distancex, distancey

def checkangles(x, y):
    if x > 89:
        return False
    elif x < -89:
        return False
    elif y > 360:
        return False
    elif y < -360:
        return False
    else:
        return True

def normalizeAngles(viewAngleX, viewAngleY):
    if viewAngleX > 89:
        viewAngleX -= 360
    if viewAngleX < -89:
        viewAngleX += 360
    if viewAngleY > 180:
        viewAngleY -= 360
    if viewAngleY < -180:
        viewAngleY += 360
    return viewAngleX, viewAngleY

def calcangle(localpos1, localpos2, localpos3, enemypos1, enemypos2, enemypos3):
    delta_x, delta_y, delta_z = localpos1 - enemypos1, localpos2 - enemypos2, localpos3 - enemypos3
    hyp = sqrt( delta_x * delta_x + delta_y * delta_y + delta_z * delta_z )

    try:
        x = asin( delta_z / hyp ) * 57.295779513082
        y = atan( delta_y / delta_x ) * 57.295779513082
    except:
        x,y = 0

    if delta_x >= 0.0:
        y += 180.0
    return x, y

def nanchecker(first, second):
    if math.isnan(first) or math.isnan(second):
        return False
    else:
        return True

def GetBestBoneTarget(mypos_x, mypos_y, mypos_z, viewanglex, viewangley, entity):
    diffs = []
    for x in range(4):
        if x == 0:
            x = 5
        elif x == 1:
            x = 6
        elif x == 2:
            x = 7
        elif x == 3:
            x = 8

        entity_bones = pm.read_int(entity + m_dwBoneMatrix)
        entitypos_x, entitypos_y, entitypos_z = pm.read_float(entity_bones + 0x30 * x + 0xC), pm.read_float(entity_bones + 0x30 * x + 0x1C), pm.read_float(entity_bones + 0x30 * x + 0x2C)
        X, Y = calcangle(mypos_x, mypos_y, mypos_z, entitypos_x, entitypos_y, entitypos_z)
        distancex, distancey = calc_distance(viewanglex, viewangley, X, Y)
        diffs.append(distancex + distancey)
    if diffs:
        return int(numpy.argmin(diffs)) + 5

def GetBestTarget():
    global enginepointer
    while True:
        try:
            olddistx, olddisty = 111111111111, 111111111111
            newdist_x, newdist_y = 0, 0
            target = None
            aimlocalplayer, enginepointer = pm.read_int(client + dwLocalPlayer), pm.read_int(engine + dwClientState)

            if aimlocalplayer:
                localplayer_team, localplayer_index = pm.read_int(aimlocalplayer + m_iTeamNum), pm.read_int(aimlocalplayer + 0x64) - 1

                for x in range(32):
                    if pm.read_int(client + dwEntityList + x * 0x10):
                        entity = pm.read_int(client + dwEntityList + x * 0x10)

                        if (pm.read_int(entity + m_bSpottedByMask)) == 1 << localplayer_index and localplayer_team != (pm.read_int(entity + m_iTeamNum)) and (pm.read_int(entity + m_iHealth)) > 0:
                            entity_bones = pm.read_int(int(entity) + int(m_dwBoneMatrix))
                            localpos_x_angles, localpos_y_angles = pm.read_float(int(enginepointer) + int(dwClientState_ViewAngles)), pm.read_float(enginepointer + dwClientState_ViewAngles + 0x4)
                            localpos1, localpos2 = pm.read_float(aimlocalplayer + m_vecOrigin), pm.read_float(aimlocalplayer + m_vecOrigin + 4)
                            localpos3 = pm.read_float(aimlocalplayer + m_vecOrigin + 8) + pm.read_float(aimlocalplayer + m_vecViewOffset + 0x8)
                            aimbone = GetBestBoneTarget(localpos1, localpos2, localpos3, localpos_x_angles, localpos_y_angles, entity)
                            if AIM_Bot_bone == 0:
                                entitypos_x, entitypos_y, entitypos_z = pm.read_float(entity_bones + 0x30 * aimbone + 0xC), pm.read_float(entity_bones + 0x30 * aimbone + 0x1C), pm.read_float(entity_bones + 0x30 * aimbone + 0x2C)
                            else:
                                 entitypos_x, entitypos_y, entitypos_z = pm.read_float(entity_bones + 0x30 * AIM_Bot_bone + 0xC), pm.read_float(entity_bones + 0x30 * AIM_Bot_bone + 0x1C), pm.read_float(entity_bones + 0x30 * AIM_Bot_bone + 0x2C)
                            X, Y = calcangle(localpos1, localpos2, localpos3, entitypos_x, entitypos_y, entitypos_z)
                            newdist_x, newdist_y = calc_distance(localpos_x_angles, localpos_y_angles, X, Y)

                            if newdist_x < olddistx and newdist_y < olddisty:
                                olddistx, olddisty, target = newdist_x, newdist_y, entity, 
                                target_hp = pm.read_int(target + m_iHealth)

                if target and target_hp > 0:
                    return target, aimbone, aimlocalplayer
        except:
            pass

def AIM_Bot():
    while AIM_Bot_Status:
        try:
            if AIM_Mouse_Status:
                if GetKeyState(1) == -127 or GetKeyState(1) == -128:
                    aimplayer, aimbone, aimlocalplayer = GetBestTarget()
                    aimplayerbone = pm.read_int(aimplayer + m_dwBoneMatrix)
                    localpos1, localpos2 = pm.read_float(aimlocalplayer + m_vecOrigin), pm.read_float(aimlocalplayer + m_vecOrigin + 4)
                    localpos_z_angles = pm.read_float(aimlocalplayer + m_vecViewOffset + 0x8)
                    localpos3 = pm.read_float(aimlocalplayer + m_vecOrigin + 8) + localpos_z_angles
                    if AIM_Bot_bone == 0:
                        enemypos1, enemypos2, enemypos3 = pm.read_float(aimplayerbone + 0x30 * aimbone + 0xC), pm.read_float(aimplayerbone + 0x30 * aimbone + 0x1C), pm.read_float(aimplayerbone + 0x30 * aimbone + 0x2C)
                    else:
                        enemypos1, enemypos2, enemypos3 = pm.read_float(aimplayerbone + 0x30 * AIM_Bot_bone + 0xC), pm.read_float(aimplayerbone + 0x30 * AIM_Bot_bone + 0x1C), pm.read_float(aimplayerbone + 0x30 * AIM_Bot_bone + 0x2C)
                    viewanglex, viewangley = pm.read_float(enginepointer + dwClientState_ViewAngles), pm.read_float(enginepointer + dwClientState_ViewAngles + 0x4)
                    x, y = calcangle(localpos1, localpos2, localpos3, enemypos1, enemypos2, enemypos3)
                    diff_x, diff_y = x - viewanglex, y - viewangley
                    diff_x, diff_y = normalizeAngles(diff_x, diff_y)
                    distancex, distancey = calc_distance(viewanglex, viewangley, x, y)

                    if distancex < fov and distancey < fov and (pm.read_int(aimplayer + m_iHealth)) > 0:
                        pm.write_float(enginepointer + dwClientState_ViewAngles, viewanglex + (diff_x / smooth))
                        pm.write_float(enginepointer + dwClientState_ViewAngles + 0x4, viewangley + (diff_y / smooth))

                    continue
            else:
                aimplayer, aimbone, aimlocalplayer = GetBestTarget()
                aimplayerbone = pm.read_int(aimplayer + m_dwBoneMatrix)
                localpos1, localpos2 = pm.read_float(aimlocalplayer + m_vecOrigin), pm.read_float(aimlocalplayer + m_vecOrigin + 4)
                localpos_z_angles = pm.read_float(aimlocalplayer + m_vecViewOffset + 0x8)
                localpos3 = pm.read_float(aimlocalplayer + m_vecOrigin + 8) + localpos_z_angles
                if AIM_Bot_bone == 0:
                    enemypos1, enemypos2, enemypos3 = pm.read_float(aimplayerbone + 0x30 * aimbone + 0xC), pm.read_float(aimplayerbone + 0x30 * aimbone + 0x1C), pm.read_float(aimplayerbone + 0x30 * aimbone + 0x2C)
                else:
                    enemypos1, enemypos2, enemypos3 = pm.read_float(aimplayerbone + 0x30 * AIM_Bot_bone + 0xC), pm.read_float(aimplayerbone + 0x30 * AIM_Bot_bone + 0x1C), pm.read_float(aimplayerbone + 0x30 * AIM_Bot_bone + 0x2C)
                viewanglex, viewangley = pm.read_float(enginepointer + dwClientState_ViewAngles), pm.read_float(enginepointer + dwClientState_ViewAngles + 0x4)
                x, y = calcangle(localpos1, localpos2, localpos3, enemypos1, enemypos2, enemypos3)
                diff_x, diff_y = x - viewanglex, y - viewangley
                diff_x, diff_y = normalizeAngles(diff_x, diff_y)
                distancex, distancey = calc_distance(viewanglex, viewangley, x, y)

                if distancex < fov and distancey < fov and (pm.read_int(aimplayer + m_iHealth)) > 0:
                    pm.write_float(enginepointer + dwClientState_ViewAngles, viewanglex + (diff_x / smooth))
                    pm.write_float(enginepointer + dwClientState_ViewAngles + 0x4, viewangley + (diff_y / smooth))
        except:
            pass

def RCS():
    oldpunchx = 0.0
    oldpunchy = 0.0

    while RCS_Status:
        try:
            rcslocalplayer = pm.read_int(client + dwLocalPlayer)
            rcsengine = pm.read_int(engine + dwClientState)

            if pm.read_int(rcslocalplayer + m_iShotsFired) > 2:
                rcs_x = pm.read_float(rcsengine + dwClientState_ViewAngles)
                rcs_y = pm.read_float(rcsengine + dwClientState_ViewAngles + 0x4)
                punchx = pm.read_float(rcslocalplayer + m_aimPunchAngle)
                punchy = pm.read_float(rcslocalplayer + m_aimPunchAngle + 0x4)
                newrcsx = rcs_x - (punchx - oldpunchx) * (RCS_X * 0.02)
                newrcsy = rcs_y - (punchy - oldpunchy) * (RCS_Y * 0.02)
                newrcs, newrcy = normalizeAngles(newrcsx, newrcsy)
                oldpunchx = punchx
                oldpunchy = punchy
                if nanchecker(newrcsx, newrcsy) and checkangles(newrcsx, newrcsy):
                    pm.write_float(rcsengine + dwClientState_ViewAngles, newrcsx)
                    pm.write_float(rcsengine + dwClientState_ViewAngles + 0x4, newrcsy)
            else:
                oldpunchx = 0.0
                oldpunchy = 0.0
                newrcsx = 0.0
                newrcsy = 0.0
        except:
            pass

def Trigger_BOT():
    while Trigger_BOT_Status:
        try:
            player = pm.read_int(client + dwLocalPlayer)
            entity_id = pm.read_int(player + m_iCrosshairId)

            if entity_id > 0 and entity_id <= 64 and (pm.read_int(player + m_iTeamNum)) != (pm.read_int((pm.read_int(client + dwEntityList + (entity_id - 1) * 0x10)) + m_iTeamNum)):
                time.sleep (delay)
                pm.write_int(client + dwForceAttack, 6)

            time.sleep(0.01)
        except:
            pass

def Skinchanger():
    gun_id_list = {}
    try:
        config = configparser.ConfigParser()
        config.read(r'resourse\cfg\skins.ini')

        gun_id_list = {32:int(config.get("P2000", "sid")), 
            61:int(config.get("USP-S", "sid")), 
            4:int(config.get("Glock", "sid")), 
            2:int(config.get("Dual Berettas", "sid")), 
            36:int(config.get("P250", "sid")), 
            30:int(config.get("Tec-9", "sid")), 
            63:int(config.get("CZ75-Auto", "sid")), 
            1:int(config.get("Desert Eagle", "sid")), 
            3:int(config.get("Five-SeveN", "sid")), 
            64:int(config.get("R8", "sid")), 
            35:int(config.get("Nova", "sid")), 
            25:int(config.get("XM1014", "sid")), 
            27:int(config.get("MAG-7", "sid")), 
            14:int(config.get("M249", "sid")), 
            28:int(config.get("Negev", "sid")), 
            29:int(config.get("Sawed-Off", "sid")), 
            17:int(config.get("MAC-10", "sid")), 
            23:int(config.get("MP5-SD", "sid")), 
            24:int(config.get("UMP-45", "sid")), 
            19:int(config.get("P90", "sid")), 
            26:int(config.get("PP-19", "sid")), 
            34:int(config.get("MP9", "sid")), 
            33:int(config.get("MP7", "sid")), 
            10:int(config.get("FAMAS", "sid")), 
            16:int(config.get("M4A4", "sid")), 
            60:int(config.get("M4A1-S", "sid")), 
            40:int(config.get("SSG 08", "sid")), 
            8:int(config.get("AUG", "sid")), 
            9:int(config.get("AWP", "sid")), 
            38:int(config.get("SCAR-20", "sid")), 
            13:int(config.get("Galil", "sid")), 
            7:int(config.get("AK-47", "sid")), 
            39:int(config.get("SG 553", "sid")), 
            11:int(config.get("C3SG1", "sid"))}
    except:
        pass

    while Skinchanger_Status:
        try:
            engine_state = pm.read_int(int(engine) + int(dwClientState))
            local_player = pm.read_int(client + dwLocalPlayer)

            if local_player == 0:
                continue

            for i in range(0, 8):
                my_weapons = pm.read_int(local_player + m_hMyWeapons + (i - 1) * 0x4) & 0xFFF
                weapon_address = pm.read_int(client + dwEntityList + (my_weapons - 1) * 0x10)

                if weapon_address:
                    weapon_id = pm.read_int(weapon_address + m_iItemDefinitionIndex)
                    weapon_owner = pm.read_int(weapon_address + m_OriginalOwnerXuidLow)

                    if weapon_id in gun_id_list:
                        fallbackpaint = gun_id_list[weapon_id]
                    else:
                        continue

                    pm.write_int(weapon_address + m_iItemIDHigh, -1)
                    pm.write_int(weapon_address + m_nFallbackPaintKit, fallbackpaint)
                    pm.write_int(weapon_address + m_iAccountID, weapon_owner)
                    pm.write_int(weapon_address + m_nFallbackStatTrak, 1337)
                    pm.write_int(weapon_address + m_nFallbackSeed, 520)
                    pm.write_float(weapon_address + m_flFallbackWear, float(0.000001))

            if keyboard.is_pressed( "f6" ):
                pm.write_int(engine_state + 0x174, -1)
        except:
            pass

def Auto_Pistol():
    while Auto_Pistol_status:
        try:
            if GetWindowText(GetForegroundWindow()) == "Counter-Strike: Global Offensive":
                if GetKeyState(0x01) == -127 or GetKeyState(0x01) == -128:
                    pm.write_int(client + dwForceAttack, 6)
                    time.sleep(0.02)
        except:
            pass

def Bunny_Hop():
    while Bunny_Hop_status:
        try:
            if GetWindowText(GetForegroundWindow()) == "Counter-Strike: Global Offensive":
                force_jump = (client + dwForceJump)

                if pm.read_int(client + dwLocalPlayer):
                    on_ground = pm.read_int((pm.read_int(client + dwLocalPlayer)) + m_fFlags)
                    if keyboard.is_pressed("space"):
                        if on_ground == 257 or on_ground == 263:
                            pm.write_int(force_jump, 5)
                            time.sleep(0.17)
                            pm.write_int(force_jump, 4)
        except:
            pass

def Radar_Hack():
    try:
        pm = pymem.Pymem('csgo.exe')
        client = pymem.process.module_from_name(pm.process_handle, 'client.dll')
        clientModule = pm.read_bytes(client.lpBaseOfDll, client.SizeOfImage)
        address = client.lpBaseOfDll + re.search(rb'\x80\xB9.{5}\x74\x12\x8B\x41\x08', clientModule).start() + 6
        pm.write_uchar(address, 0 if pm.read_uchar(address) != 0 else 2)
        pm.close_process()
    except:
        pass

def No_Flash():
    while No_Flash_Status:
        try:
            player = pm.read_int(client + dwLocalPlayer)
            flash_value = (player + m_flFlashMaxAlpha)

            if player:
                if flash_value:
                    pm.write_float(flash_value, float(0))

            time.sleep(0.1)
        except:
            pass

def No_Flash_Reset():
    try:
        player = pm.read_int(client + dwLocalPlayer)
        flash_value = (player + m_flFlashMaxAlpha)

        if player:
            if flash_value:
                pm.write_float(flash_value, float(255))
    except:
        pass

def Show_Money():
    try:
        pm = pymem.Pymem('csgo.exe')
        client = pymem.process.module_from_name(pm.process_handle,'client.dll')
        clientModule = pm.read_bytes(client.lpBaseOfDll, client.SizeOfImage)
        address = client.lpBaseOfDll + re.search(rb'.\x0C\x5B\x5F\xB8\xFB\xFF\xFF\xFF',clientModule).start()
        pm.write_uchar(address, 0xEB if pm.read_uchar(address) == 0x75 else 0x75)
    except:
        pass

if __name__ == "__main__":
   import sys
   app = QtWidgets.QApplication(sys.argv)
   ui = Widget()
   ui.show()

   def command_No_Flash():
    global No_Flash_Status

    if bool(ui.checkBox_17.isChecked()) == True:
        No_Flash_Status = True
        Thread(target = No_Flash).start()
    else:
        No_Flash_Status = False
        Thread(target = No_Flash_Reset).start()

   def command_Bunny_Hop():
    global Bunny_Hop_status

    if bool(ui.checkBox_15.isChecked()) == True:
        Bunny_Hop_status = True
        Thread(target = Bunny_Hop).start()
    else:
        Bunny_Hop_status = False

   def command_Auto_Pistol():
    global Auto_Pistol_status

    if bool(ui.checkBox_14.isChecked()) == True:
        Auto_Pistol_status = True
        Thread(target = Auto_Pistol).start()
    else:
        Auto_Pistol_status = False

   def command_skinchanger():
    global Skinchanger_Status

    if bool(ui.checkBox_13.isChecked()) == True:
        Skinchanger_Status = True
        Thread(target = Skinchanger).start()
    else:
        Skinchanger_Status = False

   def command_Trigger_BOT():
    global Trigger_BOT_Status, delay

    if bool(ui.checkBox_12.isChecked()) == True:
        try:
            delay = float(ui.lineEdit_2.text())
        except:
            delay = 0.3
            ui.lineEdit_2.setText(str(delay))

        Trigger_BOT_Status = True
        Thread(target = Trigger_BOT).start()
    else:
        Trigger_BOT_Status = False

   def command_RCS():
    global RCS_Status

    if bool(ui.checkBox_11.isChecked()) == True:
        RCS_Status = True
        Thread(target = RCS).start()
    else:
        RCS_Status = False

   def set_RCS():
    global RCS_X, RCS_Y

    RCS_X = int(ui.horizontalSlider_6.value())
    RCS_Y = int(ui.horizontalSlider_7.value())

    ui.label_12.setText(_translate("Form", f"<html><head/><body><p><span style=\" color:#ffffff;\">{RCS_X}</span></p></body></html>"))
    ui.label_14.setText(_translate("Form", f"<html><head/><body><p><span style=\" color:#ffffff;\">{RCS_Y}</span></p></body></html>"))

   def set_AIM_Mouse():
    global AIM_Mouse_Status

    if bool(ui.checkBox_10.isChecked()) == True:
        AIM_Mouse_Status = True
    else:
        AIM_Mouse_Status = False

   def command_AIM():
    global AIM_Bot_Status, AIM_Bot_bone

    if bool(ui.checkBox_9.isChecked()) == True:
        bone_list = {"Nearest": 0, "Head":8, "Neck": 7, "Chest": 6, "Stomach": 5, "Pelvis": 3}
        bone = ui.comboBox.currentText()

        AIM_Bot_bone = bone_list[bone]
        AIM_Bot_Status = True

        Thread(target = AIM_Bot).start()
    else:
        AIM_Bot_Status = False
  
   def set_AIM():
    global fov, smooth

    fov = int(ui.horizontalSlider_4.value())
    smooth = int(ui.horizontalSlider_5.value())

    ui.label_8.setText(_translate("Form", f"<html><head/><body><p><span style=\" color:#ffffff;\">{fov}</span></p></body></html>"))
    ui.label_10.setText(_translate("Form", f"<html><head/><body><p><span style=\" color:#ffffff;\">{smooth}</span></p></body></html>"))

   def set_FOV():
    global player_FOV
    player_FOV = int(ui.horizontalSlider_3.value())

    ui.label_6.setText(_translate("Form", f"<html><head/><body><p><span style=\" color:#ffffff;\">{player_FOV}</span></p></body></html>"))

    if bool(ui.checkBox_7.isChecked()) == True:
        try:
            pm.write_int((pm.read_int(client + dwLocalPlayer)) + m_iDefaultFOV, player_FOV)
        except:
            pass
    else:
        try:
            pm.write_int((pm.read_int(client + dwLocalPlayer)) + m_iDefaultFOV, 90)
        except:
            passs

   def command_Night_Mod():
    global Night_Mod_Status

    if bool(ui.checkBox_6.isChecked()) == True:
        Night_Mod_Status = True
        Thread(target = Night_Mod).start()
    else:
        Night_Mod_Status = False
        Thread(target = Night_Mod_Reset).start()

   def set_Night_Mod():
    global Night_Mod_value

    Night_Mod_value = int(ui.horizontalSlider_2.value())
    Night_Mod_value = round(Night_Mod_value * 0.001,3)
    ui.label_5.setText(_translate("Form", f"<html><head/><body><p><span style=\" color:#ffffff;\">{Night_Mod_value}</span></p></body></html>"))

   def command_Light_model():

    if bool(ui.checkBox_5.isChecked()) == True:
        try:
            pm.write_int(engine+ model_ambient_min, 1084227584 ^ pm.read_int(engine + model_ambient_min - 44))
        except:
            pass
    else:
        try:
            pm.write_int(engine+ model_ambient_min, 1084227584 ^ pm.read_int(engine + model_ambient_min - 45))
        except:
            pass

   def command_Chams():
    global Chams_status

    if bool(ui.checkBox_4.isChecked()) == True:
        Chams_status = True
        Thread(target = Chams).start()
    else:
        Chams_status = False
        Thread(target = Chams_Reset).start()

   def set_RGB_Chams():
    global Chams_R, Chams_G, Chams_B

    color = QColorDialog.getColor()
    Chams_R, Chams_G, Chams_B = ImageColor.getcolor(color.name(), "RGB")[0], ImageColor.getcolor(color.name(), "RGB")[1], ImageColor.getcolor(color.name(), "RGB")[2]

    ui.pushButton_2.setStyleSheet("QPushButton{background-color: rgb" + f"({Chams_R},{Chams_G},{Chams_B})" + ";border: none; border-radius: 3px;}")

   def command_Distance_ESP():
    global Distance_ESP_Status

    if bool(ui.checkBox_3.isChecked()) == True:
        Distance_ESP_Status = True
        Thread(target = Distance_ESP).start()
    else:
        Distance_ESP_Status = False

   def set_Distance_ESP():
    global enit_distance
    enit_distance = int(ui.horizontalSlider.value())

    ui.label_4.setText(_translate("Form", f"<html><head/><body><p><span style=\" color:#ffffff;\">{enit_distance}</span></p></body></html>"))
    
   def command_HP_ESP():
        global HP_ESP_Status

        if bool(ui.checkBox_2.isChecked()) == True:
                HP_ESP_Status = True
        else:
                HP_ESP_Status = False

   def command_ESP():
      global ESP_Status, line

      if bool(ui.checkBox.isChecked()) == True:
         try:
            line = float(ui.lineEdit.text())
         except:
            line = 0.6
            ui.lineEdit.setText(_translate("Form", f"{line}"))
         ESP_Status = True
         Thread(target = ESP).start()

      else:
         ESP_Status = False

   def set_RGB_ESP():
      global ESP_R, ESP_G, ESP_B

      color = QColorDialog.getColor()
      ESP_R, ESP_G, ESP_B = ImageColor.getcolor(color.name(), "RGB")[0], ImageColor.getcolor(color.name(), "RGB")[1], ImageColor.getcolor(color.name(), "RGB")[2]

      ui.pushButton.setStyleSheet("QPushButton{background-color: rgb" + f"({ESP_R},{ESP_G},{ESP_B})" + ";border: none; border-radius: 3px;}")

   def out_side():
    global ESP_Status, Distance_ESP_Status, Chams_status, Night_Mod_Status, AIM_Bot_Status, AIM_Mouse_Status, RCS_Status, Trigger_BOT_Status, Skinchanger_Status, Auto_Pistol_status, Bunny_Hop_status, No_Flash_Status

    AIM_Bot_Status = False
    AIM_Mouse_Status = False
    ESP_Status = False
    Distance_ESP_Status = False
    Chams_status = False
    Night_Mod_Status = False
    RCS_Status = False
    Trigger_BOT_Status = False
    Skinchanger_Status = False
    Auto_Pistol_status = False
    Bunny_Hop_status = False
    No_Flash_Status = False

    for process in psutil.process_iter():
        if process.name() == "Maze V4":
            process.kill()

    app.exit()

   ui.checkBox.stateChanged.connect(command_ESP)
   ui.checkBox_2.stateChanged.connect(command_HP_ESP)
   ui.checkBox_3.stateChanged.connect(command_Distance_ESP)
   ui.checkBox_4.stateChanged.connect(command_Chams)
   ui.checkBox_5.stateChanged.connect(command_Light_model)
   ui.checkBox_6.stateChanged.connect(command_Night_Mod)
   ui.checkBox_7.stateChanged.connect(set_FOV)
   ui.checkBox_8.stateChanged.connect(lambda: Thread(target = Game_WH).start())
   ui.checkBox_9.stateChanged.connect(command_AIM)
   ui.checkBox_10.stateChanged.connect(set_AIM_Mouse)
   ui.checkBox_11.stateChanged.connect(command_RCS)
   ui.checkBox_12.stateChanged.connect(command_Trigger_BOT)
   ui.checkBox_13.stateChanged.connect(command_skinchanger)
   ui.checkBox_14.stateChanged.connect(command_Auto_Pistol)
   ui.checkBox_15.stateChanged.connect(command_Bunny_Hop)
   ui.checkBox_16.stateChanged.connect(lambda: Thread(target = Radar_Hack).start())
   ui.checkBox_17.stateChanged.connect(command_No_Flash)
   ui.checkBox_18.stateChanged.connect(lambda: Thread(target = Show_Money).start())
   ui.pushButton.clicked.connect(set_RGB_ESP)
   ui.pushButton_2.clicked.connect(set_RGB_Chams)
   ui.horizontalSlider.valueChanged.connect(set_Distance_ESP)
   ui.horizontalSlider_2.valueChanged.connect(set_Night_Mod)
   ui.horizontalSlider_3.valueChanged.connect(set_FOV)
   ui.horizontalSlider_4.valueChanged.connect(set_AIM)
   ui.horizontalSlider_5.valueChanged.connect(set_AIM)
   ui.horizontalSlider_6.valueChanged.connect(set_RCS)
   ui.horizontalSlider_7.valueChanged.connect(set_RCS)

   keyboard.add_hotkey('*', out_side)
   
   sys.exit(app.exec_())
