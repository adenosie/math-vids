from manimlib.imports import *

def toward(angle):
    return np.array([np.cos(angle), np.sin(angle), 0])

class Sine(Scene):
    CONFIG = {
        "plane_config": {
            "x_min": -2.5,
            "x_max": 2.5,
            "y_min": -2.5,
            "y_max": 2.5,

            "axis_config": {
                "unit_size": 3,
                "include_numbers": True,
                "numbers_to_show": [-1, 1],
            },
        },

        "graph_plane_config": {
            "x_min": 0,
            "x_max": 4.3 * PI,
            "y_min": -2,
            "y_max": 2,

            "number_line_config": {
                "include_tip": True,
            },

            "x_axis_config": {
                "unit_size": 1.5 / PI,
                "tick_frequency": PI,
                "include_tip": True,
            },

            "y_axis_config": {
                "unit_size": 1,
            },
        },

        "graph_config": {
            "color": BLUE,
        },

        "circle_config": {
            "radius": 3,
        },

        "dot_config": {
            "color": YELLOW,
        },

        "arc_config": {
            "radius": 0.5,
            "stroke_width": 2,
        },

        "hypo_config": {
            "color": WHITE,
        },

        "oppo_config": {
            "color": PURPLE,
        },

        "tex_config": {
            "tex_to_color_map": {
                "\\sin": PURPLE,
                "\\pi": RED,
            }
        },
    }

    def construct(self):
        self.introduce_sine()
        self.show_graph()
        self.draw_graph()

    def introduce_sine(self):
        self.theta = ValueTracker(PI / 3)

        self.plane = NumberPlane(**self.plane_config)
        self.circle = Circle(**self.circle_config)

        self.play(ShowCreation(self.plane), ShowCreation(self.circle))
        self.wait(2)

        # make sure that the radius is 1
        brace = BraceLabel(Line(self.circle.get_center(), RIGHT * self.circle.get_width() / 2), "1")
        self.play(GrowFromCenter(brace))
        self.wait(2)
        self.play(FadeOut(brace))
        
        # show a point on the circle
        dot = Dot(self.circle.point_at_angle(np.mod(self.theta.get_value(), TAU)), **self.dot_config)
        hypo = always_redraw(lambda: Line(self.circle.get_center(), self.circle.point_at_angle(np.mod(self.theta.get_value(), TAU)), **self.hypo_config))

        arc = always_redraw(lambda: Arc(arc_center = self.circle.get_center(), angle = self.theta.get_value(), **self.arc_config))
        label = TexMobject("\\theta", **self.tex_config)
        label.add_updater(lambda l: l.move_to(self.circle.get_center() + 0.75 * toward(self.theta.get_value() / 2)))

        angle_label = VGroup(arc, label)

        self.add_foreground_mobjects(dot) # the dot must be drawn above the line
        self.play(ShowCreation(dot))
        self.play(ShowCreation(hypo))
        self.play(Write(angle_label))
        self.wait(1)

        oppo = always_redraw(lambda: Line(
            self.circle.point_at_angle(np.mod(self.theta.get_value(), TAU)),
            self.circle.get_center() + RIGHT * self.circle.get_width() / 2 * np.cos(self.theta.get_value()),
            **self.oppo_config
        ))
        self.play(ShowCreation(oppo))
        self.wait(1)

        dot.add_updater(lambda d: d.move_to(
            self.circle.point_at_angle(np.mod(self.theta.get_value(), TAU))
        ))
        self.point = VGroup(dot, hypo, oppo)

        sin_eq = TexMobject("\\sin\\theta", **self.tex_config)
        brace = always_redraw(lambda: Brace(
                oppo, RIGHT * np.sign(np.cos(self.theta.get_value()))
            ).put_at_tip(sin_eq)
        )

        self.play(GrowFromCenter(brace), Write(sin_eq))
        self.wait(2)

        self.play(self.theta.set_value, 0.1 * PI)
        self.wait(0.5)
        self.play(self.theta.set_value, 0.8 * PI)
        self.wait(0.5)
        self.play(self.theta.set_value, -1, run_time = 2)
        self.wait(0.5)
        self.play(self.theta.set_value, PI / 6)
        self.wait(3)

        self.play(FadeOut(brace), FadeOut(sin_eq), FadeOut(angle_label))
        self.play(ApplyMethod(self.theta.set_value, 0))
        self.wait(1)

    def show_graph(self):
        everything = VGroup(self.plane, self.circle)
        self.play(ApplyMethod(everything.scale, 1/3))

        wrap = Square(side_length = everything.get_width() + 0.5, fill_color = DARK_GRAY)
        self.play(DrawBorderThenFill(wrap))
        everything.add(wrap)

        self.play(ApplyMethod(everything.to_edge, LEFT))

        self.graph_plane = Axes(**self.graph_plane_config).to_edge(RIGHT)

        numbers = VGroup()
        for i in range(1, 5):
            label = TexMobject(str(i), "\\pi", **self.tex_config).move_to(self.graph_plane.coords_to_point(i * PI, -0.3)).scale(0.5)
            numbers.add(label)

        numbers.add(TexMobject("\\theta").move_to(self.graph_plane.coords_to_point(4.2 * PI, -0.5)).scale(0.75))

        sin_eq = TexMobject("\\sin\\theta", **self.tex_config).next_to(self.graph_plane, UP)
        self.play(ShowCreation(self.graph_plane), Write(numbers), Write(sin_eq))
        self.wait(3)

    def draw_graph(self):
        sine_graph = ParametricFunction(
            lambda t: self.graph_plane.coords_to_point(t, np.sin(t)),
            t_min = -0.001,
            t_max = 4.8 * PI,
            **self.graph_config
        )

        dot = Dot(**self.dot_config)
        dot.add_updater(lambda d: d.move_to(
            self.graph_plane.coords_to_point(self.theta.get_value(), np.sin(self.theta.get_value()))
        ))

        perpend = always_redraw(lambda: Line(
            self.graph_plane.coords_to_point(self.theta.get_value(), np.sin(self.theta.get_value())),
            self.graph_plane.coords_to_point(self.theta.get_value(), 0),
            **self.oppo_config
        ))

        self.add(sine_graph, perpend, dot)
        sine_graph.save_state()

        self.play(
            ShowCreation(sine_graph, rate_func = linear, run_time = 15), # a little trick to use ShowCreation() to simulate plotting
            ApplyMethod(self.theta.set_value, 4.8 * PI, rate_func = linear, run_time = 15)
        )
        self.wait(2)

        sine_graph.restore()
        self.theta.set_value(0)
        hor = always_redraw(lambda: Line(
            self.circle.point_at_angle(np.mod(self.theta.get_value(), TAU)),
            self.graph_plane.coords_to_point(self.theta.get_value(), np.sin(self.theta.get_value())),
            color = YELLOW
        ))
        self.add(hor)

        self.play(
            ShowCreation(sine_graph, rate_func = linear, run_time = 15),
            ApplyMethod(self.theta.set_value, 4.8 * PI, rate_func = linear, run_time = 15)
        )
        self.wait(3)
