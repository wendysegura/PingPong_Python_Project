from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty,\
    ObjectProperty, BooleanProperty
from kivy.vector import Vector
from kivy.clock import Clock

from time import strftime as stime


from kivy.core.audio import SoundLoader

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen, ScreenManager, WipeTransition


''''This is a Pong Ball Game that has paddles that move up and down and a ball that bounces from side to side and top to bottom, it contains a score keeper and goes up to 3 points till the game is over.'''


detective = SoundLoader.load('Detective.wav')
sound = SoundLoader.load('misc125.wav')
# started = False


class PongPaddle(Widget):
    score = NumericProperty(0)


    def bounce_ball(self, ball):
    	'''This is what cause the ball to bounce and where you set the velocity of how fast you want the ball to go.'''

        if self.collide_widget(ball):
        	vx, vy = ball.velocity
	        offset = (ball.center_y - self.center_y) / (self.height / 2)
	        bounced = Vector(-1 * vx, vy)
	        vel = bounced * 1.1
	        ball.velocity = vel.x, vel.y + offset
	        if self.parent.start:
	        	sound.play()


 
    	
    

class PongBall(Widget):
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)

    def move(self):
        self.pos = Vector(*self.velocity) + self.pos

    

class PongGame(Widget):
    ball = ObjectProperty(None)
    player1 = ObjectProperty(None)
    player2 = ObjectProperty(None)

  

    def __init__ (self, *args, **kwargs):
        super (PongGame, self).__init__(*args, **kwargs)
        Clock.schedule_interval(self.update, 1.0 / 60.0)
        self.start = False

    def serve_ball(self, vel=(8, 0)):
        self.ball.center = self.center
        self.ball.velocity = vel
        self.start = True



    # 	if self.ball.center:
       		# sound.stop()

       

    def update(self, dt):
        self.ball.move()


        #bounce of paddles
        self.player1.bounce_ball(self.ball)
        self.player2.bounce_ball(self.ball)
         		 

        #bounce ball off bottom or top
        if (self.ball.y < self.y) or (self.ball.top > self.top):
        	self.ball.velocity_y *= -1

        #went of to a side to score point?
        if self.ball.x < self.x:
            self.player2.score += 1
            self.serve_ball(vel=(8, 0))
        if self.ball.x > self.width:
            self.player1.score += 1
            self.serve_ball(vel=(-8, 0))


        if self.player1.score >= 3 or self.player2.score >=3:
        	self.player1.score = 0
        	self.player2.score = 0



        	self.parent.manager.current = 'EndMenu'


       
    
    def on_touch_move(self, touch):
        if touch.x < self.width / 3:
            self.player1.center_y = touch.y
        if touch.x > self.width - self.width / 3:
            self.player2.center_y = touch.y





class StartMenu(Screen):
	detective.play()
	detective.loop = True
	pass
    

class PongMenu(Screen):

	pass


class EndMenu(Screen):
    pass

class ScreenManagement(ScreenManager):
    pass



class PongApp(App):
    kv_file='pong.kv'
    def build(self):
        return ScreenManagement(transition = WipeTransition())


if __name__ == '__main__':
    PongApp().run()
# PingPong_Python_Project
