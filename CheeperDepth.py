import pyxel

R_X = 103
R_Y = 204
R_W = 52
R_H = 38

GPAD = [pyxel.GAMEPAD1_BUTTON_DPAD_DOWN,
        pyxel.GAMEPAD1_BUTTON_DPAD_UP,
        pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT,
        pyxel.GAMEPAD1_BUTTON_DPAD_LEFT]
KEY = [pyxel.KEY_DOWN,pyxel.KEY_UP,pyxel.KEY_RIGHT,pyxel.KEY_LEFT]
D =   [[0,1],[0,-1],[1,0],[-1,0]]

dcharge_max = 4
dcharges = []
submarines = []
manbous = []
mines = []
torpedos = []
explos = []
pwupitems = []
messages = []

class Message():
    def __init__(self,x,y,text,color,limit_time) -> None:
        self.x = x
        self.y = y
        self.text = text
        self.color = color
        self.limit_time = limit_time
    def update(self):
        self.limit_time -= 1
    def draw(self):
        pyxel.text(self.x,self.y,self.text,self.color)

class DCharge():
    def __init__(self,x,y) -> None:
        self.x = x
        self.y = y
        self.dy = 0.2
        self.cnt = 0
    def update(self):
        self.cnt += 1
        self.y += self.dy
    def draw(self):
        pyxel.blt(self.x,self.y,0,self.cnt//12%2*8,48,8,8,5)

class Mine():
    def __init__(self,x,y) -> None:
        self.x = x
        self.y = y
        self.dy = -0.2
        self.cnt = 0
    def update(self):
        self.cnt += 1
        self.y += self.dy
    def draw(self):
        pyxel.blt(self.x,self.y,0,self.cnt//12%2*9,80,9,9,5)

class PwUpItem():
    def __init__(self,x,y,type) -> None:
        self.x = x
        self.y = y
        self.type = type
        self.dy = -0.4
        self.wait_counter = 144
        self.status = 0  ## 0:浮上中　1:海面で待機中　2:待機終了で削除町
    def update(self):
        if self.status == 0:
            self.y += self.dy
            if round(self.y) == 24:
                self.status = 1
        elif self.status == 1:
            self.wait_counter -= 1
            if self.wait_counter == 0:
                self.status = 2
    def draw(self):
        pyxel.blt(self.x,self.y,0,self.type*9,128,9,9,5)

class Torpedo():
    def __init__(self,x,y) -> None:
        self.x = x
        self.y = y
        self.dy = -0.8
        self.myship_x = myship.x + 13
        self.dx = 1
        self.up_only_flag = False
        self.muki = 0
    def update(self):
        if self.up_only_flag == False:
            if self.x > self.myship_x:
                self.x -= self.dx
                self.muki = 1
            else:
                self.x += self.dx
                self.muki = 2
            if round(self.x - self.myship_x) == 0:
                self.up_only_flag = True
                self.muki = 0
        self.y += self.dy
    def draw(self):
        pyxel.blt(self.x,self.y,0,32+self.muki*8,80,8,8,5)

class Explo():
    def __init__(self,x,y) -> None:
        self.x = x
        self.y = y
        self.cnt = 0
        self.is_alive = True
    def update(self):
        self.cnt += 1
        if self.cnt > 12:
            self.is_alive = False
    def draw(self):
        pyxel.blt(self.x,self.y,0,self.cnt//4%3*16,96,16,16,0)

class MyShip():
    def __init__(self) -> None:
        self.x = 112
        self.y = 17
    def update(self):
        pass
    def draw(self):
        pyxel.blt(self.x,self.y, 0, 0,16, 32,16, 12)
        x = R_X+self.x/5
        y = R_Y+self.y/5
        pyxel.rect(x,y,4,2,7)
myship = MyShip()

class Submarine():
    def __init__(self,x,y,type) -> None:
        self.x = x
        self.y = y
        self.type = type
        #self.dx = [0.3, 0.6, 1.2]
        self.c = [10, 8, 3]
        self.wx = [4, 4, 2]
        if x < 0:
            self.dx = [0.3, 0.6, 1.2]
        else:
            self.dx = [-0.3, -0.6, -1.2]
    def update(self):
        self.x += self.dx[self.type]

    def draw(self):
        if self.dx[self.type] < 0:
            pyxel.blt(self.x,self.y,0,self.type*32,64,32,16,0)
        else:
            pyxel.blt(self.x,self.y,0,self.type*32,64,-32,16,0)
        x = R_X+self.x/5
        y = R_Y+self.y/5
        pyxel.rect(x,y,self.wx[self.type],2,self.c[self.type])
    def check_hit(self,x,y):
        if self.type <= 1:  ## type==0 or 1
            if x > self.x and x < self.x + 23 and y > self.y and y < self.y + 12:
                return True
        else:  ## type==2
            if x > self.x and x < self.x + 23 and y > self.y and y < self.y + 12:
                return True
        return False

class Manbou():
    def __init__(self,x,y) -> None:
        self.x = x
        self.y = y
        self.dy = 0.8
        if x < 0:
            self.dx = 0.6
        else:
            self.dx = -0.6
        self.straight_counter = 0
        self.updown_counter = 30
    def update(self):
        if self.straight_counter > 0:
            self.x += self.dx
            self.straight_counter -= 1
            if self.straight_counter == 0:
                self.updown_counter = 30
        else:
            self.x += self.dx
            self.y += self.dy
            self.updown_counter -= 1
            if self.updown_counter == 0:
                self.dy = -self.dy
                self.straight_counter = 14
    def draw(self):
        if self.dx < 0:
            pyxel.blt(self.x,self.y,0,0,112,16,16,5)
        else:
            pyxel.blt(self.x,self.y,0,0,112,-16,16,5)
        x = R_X+self.x/5
        y = R_Y+self.y/5
        pyxel.rect(x,y,2,2,pyxel.frame_count//3%2*7)
    def check_hit(self,x,y):
        if x > self.x and x < self.x + 8 and y > self.y and y < self.y + 12:
            return True
        return False


class App():
    def __init__(self):
        pyxel.init(256,256,title="チーパーデプス（CheepeerDepth）",fps=48)
        pyxel.load("depth.pyxres")
        self.init_game()
        pyxel.run(self.update, self.draw)

    def init_game(self):
        self.cnt = 0
        self.score = 0
        self.hi_score = 0
        self.gamestart_flag = False
        self.gamestart_waittime = 0

    def start_game(self):
        global dcharge_max,dcharges,submarines,manbous,mines,torpedos,explos,pwupitems,messages
        if self.score > self.hi_score:
            self.hi_score = self.score
        self.score = 0
        self.myship_dx = 0.4
        dcharge_max = 4
        dcharges = []
        submarines = []
        manbous = []
        mines = []
        torpedos = []
        explos = []
        pwupitems = []
        messages = []
        messages.append(Message(104,80,"GAME START!",7,72))
        pyxel.play(3,11,loop=True)

    def update(self):
        global myshipcls,dcharge_max
        self.cnt += 1

        ### 入力イベントの処理
        if self.gamestart_flag == True:
            ### マイシップの移動
            for i in range(2,4):
                if pyxel.btn(KEY[i]) or pyxel.btn(GPAD[i]):
                    myship.x += (D[i][0] * self.myship_dx)
            ### マイシップから爆雷の投下
            if dcharge_max > len(dcharges):
                if pyxel.btnp(pyxel.KEY_Z) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_A):
                    dcharges.append(DCharge(myship.x-8,20))
                    pyxel.play(0,0)
                elif pyxel.btnp(pyxel.KEY_X) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_B):
                    dcharges.append(DCharge(myship.x+32,20))
                    pyxel.play(0,0)
        else: # ゲーム開始前
            if self.gamestart_waittime > 0:
                self.gamestart_waittime -= 1
            elif pyxel.btnp(pyxel.KEY_RETURN) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_START):
                self.gamestart_flag = True
                self.start_game()
                return

        ### 時間経過による処理
        if self.cnt%300 == 0 and len(submarines) < 10:
            if pyxel.rndi(0,1) == 0:
                submarines.append(Submarine(384+pyxel.rndi(0,60),pyxel.rndi(60,160),pyxel.rndi(0,2)))
            else:
                submarines.append(Submarine(-160-pyxel.rndi(0,60),pyxel.rndi(60,160),pyxel.rndi(0,2)))

        ### マンボウの出現
        if pyxel.rndi(0,1440) == 0:
            if pyxel.rndi(0,1) == 0:
                manbous.append(Manbou(384+pyxel.rndi(0,60),pyxel.rndi(60,160)))
            else:
                manbous.append(Manbou(-160-pyxel.rndi(0,60),pyxel.rndi(60,160)))
        ### 潜水艦から機雷または魚雷の発射（浮上）
        for submarine in submarines:
            if pyxel.rndi(0,120) == 0:
                if submarine.x > 10 and submarine.x < 245:
                    if submarine.type == 1:
                        torpedos.append(Torpedo(submarine.x+8,submarine.y))
                        pyxel.play(2,3)
                    else:  #if submarine.type == 0 or 2:
                        mines.append(Mine(submarine.x+8,submarine.y))

        ### 自機の更新
        myship.update()
        ### 潜水艦の更新
        for submarine in reversed(submarines):
            submarine.update()
            if submarine.x < -280 or submarine.x > 480:
                submarines.remove(submarine)
        ### マンボウの更新
        for manbou in reversed(manbous):
            manbou.update()
            if manbou.x < -280 or manbou.x > 480:
                manbous.remove(manbou)
        ### 爆発エフェクトの更新
        for explo in reversed(explos):
            explo.update()
            if explo.is_alive == False:
                explos.remove(explo)
        ### マイシップから投下した爆雷の更新　※敵との当たり判定
        for dcharge in reversed(dcharges):
            dcharge.update()
            if dcharge.y > 190:
                dcharges.remove(dcharge)
                continue
            for submarine in reversed(submarines):
                if submarine.check_hit(dcharge.x,dcharge.y):
                    explos.append(Explo(dcharge.x,dcharge.y))
                    pyxel.play(1,1)
                    ten = (submarine.type+1)*50
                    messages.append(Message(submarine.x+10,submarine.y,"{}".format(ten),7,48))
                    self.score += ten
                    submarines.remove(submarine)
                    dcharges.remove(dcharge)
                    break
            for manbou in reversed(manbous):
                if manbou.check_hit(dcharge.x,dcharge.y):
                    explos.append(Explo(dcharge.x,dcharge.y))
                    pyxel.play(1,1)
                    pwupitems.append(PwUpItem(manbou.x,manbou.y,pyxel.rndi(0,1)))
                    #pwupitems.append(PwUpItem(manbou.x,manbou.y,0))
                    manbous.remove(manbou)
                    dcharges.remove(dcharge)
                    break

        ### 機雷の更新（※マイシップとの当たり判定）
        for mine in reversed(mines):
            mine.update()
            if mine.y < 25:
                if myship.x < mine.x and myship.x + 24 > mine.x and self.gamestart_flag:
                    self.gamestart_flag = False
                    self.gamestart_waittime = 320
                    self.gamestart_flag = False
                    explos.append(Explo(mine.x,mine.y))
                    explos.append(Explo(mine.x-3,mine.y-5))
                    explos.append(Explo(mine.x-2,mine.y+2))
                    explos.append(Explo(mine.x+4,mine.y-3))
                    explos.append(Explo(mine.x+7,mine.y-1))
                    pyxel.stop(3)
                    pyxel.play(1,[1,1,1,1,1])
                    pyxel.play(2,10)
                mines.remove(mine)
        ### 魚雷の更新（※マイシップとの当たり判定）
        for torpedo in reversed(torpedos):
            torpedo.update()
            if round(torpedo.y) == 25:
                if myship.x < torpedo.x and myship.x + 28 > torpedo.x and self.gamestart_flag:
                    self.gamestart_waittime = 320
                    self.gamestart_flag = False
                    explos.append(Explo(torpedo.x,torpedo.y))
                    explos.append(Explo(torpedo.x-3,torpedo.y-5))
                    explos.append(Explo(torpedo.x-2,torpedo.y+2))
                    explos.append(Explo(torpedo.x+4,torpedo.y-3))
                    explos.append(Explo(torpedo.x+7,torpedo.y-1))
                    pyxel.stop(3)
                    pyxel.play(1,[1,1,1,1,1])
                    pyxel.play(2,10)
                    torpedos.remove(torpedo)
            elif torpedo.y < -8:
                torpedos.remove(torpedo)
        ### パワーアップアイテムの更新
        for pwupitem in reversed(pwupitems):
            pwupitem.update()
            if pwupitem.status == 1:
                if myship.x < pwupitem.x and myship.x + 32 > pwupitem.x:
                    if pwupitem.type == 0:
                        if dcharge_max < 8:
                            dcharge_max += 1
                            messages.append(Message(74,3,"MAX",8,32))
                            messages.append(Message(74,9,"UP!",8,32))
                    elif pwupitem.type == 1:
                            self.myship_dx += 0.1
                            messages.append(Message(myship.x,6,"SPEED UP!",5,32))
                    ten = 300
                    messages.append(Message(pwupitem.x,14,"{}".format(ten),7,48))
                    pyxel.play(2,2)
                    self.score += ten
                    pwupitems.remove(pwupitem)
            elif pwupitem.status == 2:
                pwupitems.remove(pwupitem)
        ### メッセージの更新
        for message in reversed(messages):
            message.update()
            if message.limit_time < 0:
                messages.remove(message)




    def draw(self):
        pyxel.cls(5)                 # 海の色
        pyxel.rect(0,0,256,30,6)     # 空の色
        pyxel.rect(0,190,256,66,13)  # 情報欄の背景（グレー）
        pyxel.rect(R_X-30,R_Y,R_W+60,R_H+1,0) # レーダー
        pyxel.line(R_X,R_Y,R_X,R_Y+R_H,5)
        pyxel.line(R_X+R_W,R_Y,R_X+R_W,R_Y+R_H,5)

        ### 自機の描画
        if self.gamestart_flag:
            myship.draw()
        ### マンボウの描画
        for manbou in reversed(manbous):
            manbou.draw()
        ### 潜水艦の描画
        for submarine in submarines:
            submarine.draw()
        ### 爆発エフェクトの更新
        for explo in reversed(explos):
            explo.draw()
        ### マイシップが投下した爆雷の描画
        for dcharge in reversed(dcharges):
            dcharge.draw()
        ### 機雷の描画
        for mine in reversed(mines):
            mine.draw()
        ### 魚雷の描画
        for torpedo in reversed(torpedos):
            torpedo.draw()
        ### パワーアップアイテムの描画
        for pwupitem in reversed(pwupitems):
            pwupitem.draw()
        ### 爆雷残数の表示
        if self.gamestart_flag:
            for x in range(dcharge_max - len(dcharges)):
                pyxel.blt(100+x*10,6,0,24,48,8,8,5)
            if dcharge_max == 8:
                pyxel.blt(74,5,0,0,144,19,8,7)
        ### メッセージの描画
        for message in reversed(messages):
            message.draw()
        ### ゲームオーバー表示またはタイトル画像の描画
        if self.gamestart_flag == False:
            if self.gamestart_waittime > 0:
                pyxel.blt(80,100,1,0,128,96,10,0)
            else:
                pyxel.blt(54,60,1,0,0,144,72,0)


        pyxel.rect(0,190,256,10,13)  # レーダーの上（爆雷）を消す
        pyxel.rect(R_X-60,R_Y,30,R_H+1,13) # レーダーの左を消す
        pyxel.rect(R_X+R_W+30,R_Y,30,R_H+1,13) # レーダーの左を消す
        ### スコア
        pyxel.blt(16,200,1,0,105,28,7,0)
        for i in range(0,6):  ## スコア
            n = self.score//(10**i)%10*8
            pyxel.blt(50-i*6,210,1,n,96,8,8,0)
        ### ハイスコア
        pyxel.blt(16,224,1,0,113,40,7,0)
        for i in range(0,6):
            n = self.hi_score//(10**i)%10*8
            pyxel.blt(50-i*6,234,1,n,96,8,8,0)
        ### 操作説明
        pyxel.blt(196,206,1,0,72,45,21,0)  ## 操作説明

        ### デバッグ用
        #pyxel.text(10,50,"self.cnt:{}".format(self.cnt),7)
        #pyxel.text(10,60,"len(pw):{}".format(len(pwupitems)),7)
        #pyxel.text(10,70,"submarines[0].x:{}".format(submarines[0].x),7)

App()

