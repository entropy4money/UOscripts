"""
Elemental craft script
Copyright 2019, Henry Angola (Entropy), ALL rights reserved.
"""
def move_tool(tool=None,color=None,quantity=0,ret = False):
    
    item = Items.FindByID(tool,color,resourceBag)
    Items.Move(item, backpack, quantity)
    Misc.Pause(2000)
    if ret:
        return item
    
def move_to_bag(item):
    Items.Move(item, weponsBag, 0)
    Misc.Pause(2000)
    
def check_resources():
    
    tool = Items.FindByID(toolID,toolColor,backpack)
    ingot = Items.FindByID(ingotID,ingotColor,backpack)
    shadowTool = Items.FindByID(toolID,shadowToolColor,backpack)
    
    #check if tool has enough charges
    

    if ingot == None or ingot.Amount < 15:
        move_tool(ingotID,ingotColor,200)
    if tool == None:
        move_tool(toolID,toolColor,0)
    if shadowTool == None:
        move_tool(toolID,shadowToolColor,0)
        shadowTool = Items.FindByID(toolID,shadowToolColor,backpack)
        Misc.Pause(500)

    Items.GetPropStringList(shadowTool)
    for prop in shadowTool.Properties:
        #str(prop).find("uses remaining")
        if str(prop).find("uses remaining") != -1:
            uses = str(prop).split()
            uses = float(uses[-1])

    
    if uses < 4:
        newTool = move_tool(toolID,shadowToolColor,0,True)
        Items.UseItem(shadowTool)
        Target.WaitForTarget(10000, False)
        Target.TargetExecute(newTool)
        Misc.Pause(2000)
        
def craft_axe():
    tool = Items.FindByID(toolID,toolColor,backpack)
    Items.UseItem(tool)
    Gumps.WaitForGump(460, 10000)
    Gumps.SendAction(460, 5000)
    Gumps.WaitForGump(460, 10000)
    Gumps.SendAction(460, 9005)
    Gumps.WaitForGump(460, 10000)
    Gumps.SendAction(460, 61)
    Misc.Pause(2000)
    

def craft_bow(bow='composite'):
    if bow == 'composite':
        menu = 9
    if bow == 'yumi':
        menu = 11
    tool = Items.FindByID(toolID,toolColor,backpack)
    Items.UseItem(tool)

    Gumps.WaitForGump(460, 10000)
    Gumps.SendAction(460, menu)
    Gumps.WaitForGump(460, 10000)
    Gumps.SendAction(460, 0)
    Misc.Pause(2000)
    
    
def check_exceptional(item):
    Items.GetPropStringList(item)
    for prop in item.Properties:
        if str(prop) == 'exceptional':
            return True
    
    return False

     
def reforge():
    shadowTool = Items.FindByID(toolID,shadowToolColor,backpack)
    dAxe = Items.FindByID(dAxeID,0x0000,backpack)
    Items.UseItem(shadowTool)
    Target.WaitForTarget(10000, False)
    Target.TargetExecute(dAxe.Serial)
    Gumps.WaitForGump(999084, 10000)
    Gumps.SendAction(999084, 2)
    dAxe = Items.FindByID(dAxeID,-1,backpack)
    Misc.Pause(1000)
    elemental = check_elemental(dAxe)
    Misc.Pause(2000)
    return elemental
    
def check_elemental(item):
    Items.GetPropStringList(item)
    for prop in item.Properties:
        Misc.SendMessage(prop)
        if str(prop) in elementals:
            return True
        
    return False    

def burn(item):
    if toolID == 0x1022:
        Player.UseSkill('Imbuing')
        Gumps.WaitForGump(999059, 10000)
        Gumps.SendAction(999059, 2)
        Target.WaitForTarget(10000, False)
        Target.TargetExecute(item.Serial)
        Misc.Pause(3000)
        notMagic = Journal.Search('You cannot magically unravel this item.')
        Journal.Clear()
        if notMagic:
            Items.Move(item, trash, 0)
        else:
            residue = Items.FindByID(0x2DB1,-1,backpack)
            if residue != None:
                move_to_bag(residue)
                
    else:
        tool = Items.FindByID(toolID,toolColor,backpack)
        Items.UseItem(tool)
        Gumps.WaitForGump(460, 10000)
        Gumps.SendAction(460, 7000)
        Target.WaitForTarget(10000, False)
        Target.TargetExecute(item.Serial)
        
    Misc.Pause(2000)

##################
###USEFUL ID'S####
##################
###Blacksmith tool/color: 0x13E3/0x0966
###Bowsmith tool/color: 0x1022/0x07DA   
###ingot ID: 0x1BF2
###Boards ID: 0x1BD7
###dAxeID : 0x0F4B
###Yumi ID : 0x27A5
##Composite: 0x26C2 
######################
### MAIN VARIABLES ###
######################
######SETUP###########
######################

resourceBag = 0x43F69EC3 #SERIAL bag of resources (wood, ingots, tools,etc...)
shadowToolColor = 0x07DA #ID magic tool (shadow hammer, oak fletchers, etc...)
toolColor = 0x0000 #DO NOT CHANGE
toolID = 0x1022 #ID regular tool (smith hammer, fletcher, etc..)
ingotID = 0x1BD7 #ID raw materials (wooden boards, ingots, etc...)
ingotColor = 0x0000 #DO NOT CHANGE
backpack = Player.Backpack.Serial #DO NOT CHANGE
dAxeID = 0x26C2 #ID of item to craft (Double axe, bow, etc..)
elementals = ['fire damage 100%','poison damage 100%','chaos damage 100%','cold damage 100%','cold damage 70%','fire damage 70%','energy damage 100%'] #List of elementals to keep
weponsBag = 0x43F69F07 #SERIAL bag to store elemental weapons
trash = 0x46038FEE #SERIAL trashcan
######################

###MAIN LOOP#####
###DO NOT TOUCH ANYTHING HERE###
##############################
while True:
    Journal.Clear()
    check_resources()
    craft_bow('composite')
    check_resources()
    item = Items.FindByID(dAxeID,-1,backpack)
    if item != None:
        ex = check_exceptional(item)
        if not ex:
            burn(item)
        else:
            elemental = reforge()
            item = Items.FindByID(dAxeID,-1,backpack)
            if not elemental:
                burn(item)
            else:
                move_to_bag(item)
    else:
        Misc.Pause(2000)
            







