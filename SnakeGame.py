import turtle
import random
import time


class SnakeGame:
    """ Juego de Snake """

    def __init__(self, width=600, height=800):
        """ Permite inicializar los atributos de instancia.

            Args:
                width(float): Tamaño del ancho en px.
                height(float): Tamaño de la altura en px.
        """
        self.width = width
        self.height = height

        # Creación del entorno gráfico
        self.screen = turtle.Screen()

        self.screen.setup(width=self.width, height=self.height, startx=0, starty=0)
        self.screen.title("Juego Snake")
        self.screen.bgcolor("green")
        self.screen.tracer(0)
        # Creación de la serpiente
        self.snake = turtle.Turtle()
        self.snake.color("black")
        self.snake.shape("square")
        self.snake.speed(0)
        self.snake.penup()

        # Creación del cuerpo de la serpiente
        self.snake_body = []

        # Creación del puntaje
        self.puntos = "0"
        self.record = "0"
        self.score = turtle.Turtle()
        self.score.color("white")
        self.score.hideturtle()
        self.score.penup()
        self.score.goto(0, (self.height / 2 - 40))
        self.score.write("Puntos: " + self.puntos + " Record: " + self.record, False, "center",
                         font=("Arial", 24, "normal"))

        # Dirección de la serpiente
        self._direccion = None

        # Uso de las teclas
        self.screen.listen()
        self.screen.onkeypress(self.up, "w")
        self.screen.onkeypress(self.down, "s")
        self.screen.onkeypress(self.right, "d")
        self.screen.onkeypress(self.left, "a")

        # Creación de la primera manzana

        self.apple = turtle.Turtle()
        self.apple.color("red")
        self.apple.shape("circle")
        self.apple.penup()
        cordx = int(random.randrange(-290, 290))
        cordy = int(random.randrange(-390, 390))
        self.apple.teleport(cordx, cordy)

        self._delay = 0.1

    def up(self):
        """ Establece la dirección hacia arriba. """
        if self._direccion != "down":
            self._direccion = "up"

    def down(self):
        """ Establece la dirección hacía abajo. """
        if self._direccion != "up":
            self._direccion = "down"

    def right(self):
        """ Establece la dirección hacía la derecha. """
        if self._direccion != "left":
            self._direccion = "right"

    def left(self):
        """ Establece la dirección hacía la izquierda. """
        if self._direccion != "right":
            self._direccion = "left"

    def move(self):
        """ Realiza el movimiento de la serpiente según la dirección indicada """

        hx = self.snake.xcor()
        hy = self.snake.ycor()

        for i in range(len(self.snake_body) - 1, 0, -1):
            sx = self.snake_body[i - 1].xcor()
            sy = self.snake_body[i - 1].ycor()

            self.snake_body[i].goto(sx, sy)

        if len(self.snake_body) > 0:
            self.snake_body[0].goto(hx, hy)

        if self._direccion == "up":
            self.snake.sety(hy + 20)
        elif self._direccion == "down":
            self.snake.sety(hy - 20)
        elif self._direccion == "right":
            self.snake.setx(hx + 20)
        elif self._direccion == "left":
            self.snake.setx(hx - 20)

    def play(self):
        """ Inicio de la partida """
        while True:
            self.dead_wall()
            self.snake_conflict()
            self.apple_conflict()
            time.sleep(self._delay)
            self.move()
            self.screen.update()
        self.screen.mainloop()

    def dead_wall(self):
        """ Establece los límites de la pantalla """

        if self.snake.ycor() > (self.height / 2 - 10) or self.snake.ycor() < (
                -self.height / 2 + 10) or self.snake.xcor() > (self.width / 2 - 10) or self.snake.xcor() < (
                -self.width / 2 + 10):
            self.snake.goto(0, 0)
            self._direccion = None
            if int(self.puntos) > int(self.record):
                self.record = self.puntos
            self.score.clear()
            self.puntos = "0"
            self.score.write("Puntos: " + self.puntos + " Record: " + self.record, False, "center",
                             font=("Arial", 24, "normal"))

            for i in self.snake_body:
                i.hideturtle()
            self.snake_body.clear()

    def apple_conflict(self):
        """ Permite generar manzanas aleatorias en el momento de que ambos punteros choquen. """

        if self.snake.distance(self.apple) < 20:
            self.apple.goto(int(random.randrange(-290, 290)), (random.randrange(-390, 390)))
            self.puntos = str(int(self.puntos) + 10)
            self.score.clear()
            self.score.write("Puntos: " + self.puntos + " Record: " + self.record, False, "center",
                             font=("Arial", 24, "normal"))
            self.add_snake_body()
            self._delay -= 0.001

    def add_snake_body(self):
        """ Agranda el cuerpo de la serpiente. """

        add_body = turtle.Turtle()
        add_body.color("grey")
        add_body.shape("square")
        add_body.speed(0)
        add_body.penup()
        self.snake_body.append(add_body)

    def snake_conflict(self):
        """ Reinicia el juego en el caso de chocar contra el cuerpo de la serpiente. """

        x = self.snake.xcor()
        y = self.snake.ycor()

        for i in self.snake_body:
            if x == i.xcor() and y == i.ycor():
                self.snake.goto(0, 0)
                self._direccion = None
                if int(self.puntos) > int(self.record):
                    self.record = self.puntos
                self.score.clear()
                self.puntos = "0"
                self.score.write("Puntos: " + self.puntos + " Record: " + self.record, False, "center",
                                 font=("Arial", 24, "normal"))

                for i in self.snake_body:
                    i.hideturtle()
                self.snake_body.clear()

playGame = SnakeGame()
playGame.play()