from servo_wrapper import ServoWrapper, ServoModel
import maestromaster.maestro

class MaestroConnection(ServoWrapper):
    type_ = 'maestro'
    CENTRE = 6000
    RANGE = 3600

    def __init__(self, config):
        ServoWrapper.__init__(self, config)
        self.port = config.get('port')
        self.Controller = maestro.Controller(port=self.port)

    def getPos(self, angle):
        if angle > 90:
            angle = 90
        if angle < -90:
            angle = -90
        return self.CENTRE + int(self.RANGE * angle / 90)

    @staticmethod
    def calc_speed(speed):  # s/60 deg
        QuarterTickPer60Deg = 2000 / 4
        TenMSPerSecond = 100
        out = int(1 / (speed / QuarterTickPer60Deg * TenMSPerSecond))
        print("Calc Speed: ", out)
        return out

    def create_servo_model(self, channel, config):
        sm = ServoModel(channel, config["speed"], config["neutral"],
                          self.Controller.getPosition(channel))
        self.Controller.setRange(channel, self.CENTRE-self.RANGE, self.CENTRE+self.RANGE)
        self.Controller.setSpeed(channel, sm.speed)
        self.Controller.setAccel(channel, 0)
        return sm

    def go_to(self, channel, pos):
        self.Controller.setTarget(channel, pos)

    def stop(self):
        pass

    def close(self):
        self.Controller.close()
