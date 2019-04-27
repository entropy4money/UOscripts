
def move_tool(tool=None,color=None,quantity=0,ret = False):
    
    item = Items.FindByID(tool,color,resourceBag)
    Items.Move(item, backpack, quantity)
    Misc.Pause(2000)
    if ret:
        return item
        
def check_resources():
    
    tool = Items.FindByID(toolID,toolColor,backpack)
    ingot = Items.FindByID(ingotID,ingotColor,backpack)
    
    if ingot == None or ingot.Amount < 15:
        move_tool(ingotID,ingotColor,200)
    if tool == None:
        move_tool(toolID,toolColor,0)

def check_shuri(shurik):
    Items.WaitForProps(shurik,1000)
    for prop in shurik.Properties:
        if str(prop).find("uses remaining") != -1:
            uses = str(prop).split()
            uses = float(uses[-1])
            Misc.SendMessage(uses)

    if uses == 10:
        return True
    else:
        return False
        
def check_belt():
    
    Items.WaitForProps(belt,1000)
    for prop in belt.Properties:
        if str(prop).find("uses remaining") != -1:
            uses = str(prop).split()
            uses = float(uses[-1])
            Misc.SendMessage(uses)

    if uses == 10:
        return True
    else:
        return False
        
def load_belt():
    
    shuriken = Items.FindByID(shuriID,-1,backpack)
    Items.SingleClick(belt)
    Misc.WaitForContext(0x437E56A6, 10000)
    Misc.ContextReply(0x437E56A6, 701)
    Target.WaitForTarget(10000, False)
    Target.TargetExecute(shuriken)

def unload_belt():
    Items.SingleClick(belt)
    Misc.WaitForContext(0x437E56A6, 10000)
    Misc.ContextReply(0x437E56A6, 702)  
    
def craft_shuriken():
    tool = Items.FindByID(toolID,toolColor,backpack)
    Items.UseItem(tool)
    Gumps.WaitForGump(460, 10000)
    Gumps.SendAction(460, 9004)
    Gumps.WaitForGump(460, 10000)
    Gumps.SendAction(460, 56)
    Gumps.WaitForGump(460, 10000)
    Gumps.SendAction(460, 0)

def move_to_bag(item):
    Items.Move(item, weponsBag, 0)
    Misc.Pause(2000)
    
backpack = Player.Backpack.Serial
resourceBag = 0x43F69EC3 #SERIAL bag of resources (ingots, tools,etc...)
toolColor = 0x0000 #DO NOT CHANGE
toolID = 0x13E3 #ID regular tool (smith hammer, fletcher, etc..)
ingotID = 0x1BF2 #ID raw materials (wooden boards, ingots, etc...)
ingotColor = 0x0000 #DO NOT CHANGE
beltID = 0x2790
belt = Items.FindByID(beltID,-1,backpack)
shuriID = 0x27AC
weponsBag = 0x43F69F07

while True:
    check_resources()
    Misc.Pause(1000)
    beltFull = check_belt()
    Misc.Pause(1000)
    if not beltFull:
        craft_shuriken()
    Misc.Pause(1000)
    beltFull = check_belt()
    Misc.Pause(2000)
    if beltFull:
        unload_belt()
        Misc.Pause(3000)
        shurik = Items.FindByID(shuriID,-1,backpack)
        full = check_shuri(shurik)
        while not full:
            shurik = Items.FindByID(shuriID,-1,backpack)
            full = check_shuri(shurik)
            Misc.Pause(1000)

        move_to_bag(shurik)

    else:
        load_belt()

        
        
        
        


