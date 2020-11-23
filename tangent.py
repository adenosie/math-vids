from manimlib.imports import *

def toward(angle):
    return np.array([np.cos(angle), np.sin(angle), 0])

class Tangent(Scene):
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

        "circle_config": {
            "radius": 3,
        },

        "dot_config": {
            "color": YELLOW,
            "radius": 0.05,
        },

        "line_config": {
            "stroke_width": 4
        },

        "tex_config": {
            "tex_to_color_map": {
                "\\sin": PURPLE,
                "\\cos": YELLOW,
                "\\tan": BLUE,
            },
        },
    }

    def construct(self):
        self.draw_things()
        self.derive_tan()
        self.layout_graph()
        self.draw_graph()
    
    def get_origin(self):
        return self.circle.get_center()

    def get_point_at_theta(self):
        return self.circle.point_at_angle(np.fmod(self.theta.get_value(), TAU))

    def get_foot(self):
        return self.circle.get_center() + RIGHT * self.circle.get_width() / 2 * np.cos(self.theta.get_value())

    def draw_things(self):
        self.theta = ValueTracker(np.radians(50))
        self.plane = NumberPlane(**self.plane_config)
        self.circle = Circle(**self.circle_config)

        self.play(ShowCreation(self.plane), ShowCreation(self.circle))

        # make sure that the radius is 1 (though it actually isn't)
        brace = BraceLabel(Line(self.get_origin(), self.circle.point_at_angle(0)), "1")
        self.play(GrowFromCenter(brace))
        self.wait(2)
        self.play(FadeOut(brace))

        # make dots
        p_o = Dot(**self.dot_config)
        p_a = Dot(**self.dot_config)
        p_b = Dot(**self.dot_config)

        p_o.add_updater(lambda o: o.move_to(self.get_origin()))
        p_a.add_updater(lambda a: a.move_to(self.get_point_at_theta()))
        p_b.add_updater(lambda b: b.move_to(self.get_foot()))

        self.dots = VGroup(p_o, p_a, p_b)

        # make lines connecting the points
        l_oa = always_redraw(lambda: Line(
            self.get_origin(), 
            self.get_point_at_theta(),
            stroke_color = WHITE, **self.line_config
        ))

        l_ob = always_redraw(lambda: Line(
            self.get_origin(),
            self.get_foot(),
            stroke_color = YELLOW, **self.line_config
        ))

        l_ab = always_redraw(lambda: Line(
            self.get_point_at_theta(),
            self.get_foot(),
            stroke_color = PURPLE, **self.line_config
        ))

        self.lines = VGroup(l_oa, l_ob, l_ab)

        self.add_foreground_mobjects(self.lines, self.dots)
        self.play(ShowCreation(self.lines), ShowCreation(self.dots))

        # make labels indicating the points
        label_o = TextMobject("O", **self.tex_config)
        label_a = TextMobject("A", **self.tex_config)
        label_b = TextMobject("B", **self.tex_config)

        label_o.add_updater(lambda l: l.next_to(p_o, -toward(self.theta.get_value() / 2)))
        label_a.add_updater(lambda l: l.next_to(p_a, toward(self.theta.get_value() + PI / 2)))
        label_b.add_updater(lambda l: l.next_to(p_b, DOWN * np.sign(np.sin(self.theta.get_value()))))

        self.labels = VGroup(label_o, label_a, label_b)
        self.play(Write(self.labels))

        # make a ray crossing through the origin and point A,
        # and a line tangent to the circle and perpendicular to the x-axis
        self.ray = always_redraw(lambda: Line(
            self.get_origin() - 9 * toward(self.theta.get_value()),
            self.get_origin() + 9 * toward(self.theta.get_value()),
            stroke_color = BLUE, **self.line_config
        ))

        self.perpend = always_redraw(lambda: Line(
            self.circle.point_at_angle(0) + DOWN * 5,
            self.circle.point_at_angle(0) + UP * 5,
            stroke_color = WHITE, **self.line_config
        ))
        
        self.play(ShowCreation(self.perpend))
        self.play(ShowCreation(self.ray))

        # make point C and D
        p_c = Dot(**self.dot_config)
        p_d = Dot(**self.dot_config)

        p_c.add_updater(lambda c: c.move_to(
            self.circle.point_at_angle(0) + UP * self.circle.get_width() / 2 * np.tan(self.theta.get_value())
        ))

        p_d.add_updater(lambda d: d.move_to(self.circle.point_at_angle(0)))

        self.dots.add(p_c, p_d)

        # make label to the points
        label_c = TextMobject("C", **self.tex_config).next_to(p_c, RIGHT)
        label_d = TextMobject("D", **self.tex_config).next_to(p_d, DR)
        self.labels.add(label_c, label_d)

        self.play(ShowCreation(p_c), ShowCreation(p_d), Write(label_c), Write(label_d))
        label_c.add_updater(lambda l: l.next_to(p_c, RIGHT))

        self.wait(3)

    def derive_tan(self):
        pass

    def layout_graph(self):
        pass

    def draw_graph(self):
        pass
