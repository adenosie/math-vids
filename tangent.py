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
            "color": GREEN
        },

        "circle_config": {
            "radius": 3,
        },

        "arc_config": {
            "radius": 0.5,
        },

        "dot_config": {
            "color": YELLOW,
        },

        "line_config": {
            "stroke_width": 4
        },

        "tex_config": {
            "tex_to_color_map": {
                "\\tan": BLUE,
                "\\pi": RED,
            },
        },
    }

    def construct(self):
        self.draw_things()
        self.layout_graph()
        self.draw_graph()
    
    def get_origin(self):
        return self.circle.get_center()

    def get_point_at_theta(self):
        return self.circle.point_at_angle(np.mod(self.theta.get_value(), TAU))

    def get_intersection(self):
        return self.circle.point_at_angle(0) + UP * self.circle.get_width() / 2 * np.tan(self.theta.get_value())

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
        p_a = Dot(**self.dot_config)
        p_a.add_updater(lambda a: a.move_to(self.get_point_at_theta()))

        # make a radius connecting O and A
        self.radius = always_redraw(lambda: Line(
            self.get_origin(), 
            self.get_point_at_theta(),
            stroke_color = WHITE, **self.line_config
        ))

        self.play(ShowCreation(self.radius), ShowCreation(p_a))

        # make angle label
        arc = always_redraw(lambda: Arc(arc_center = self.get_origin(), angle = self.theta.get_value(), **self.arc_config))
        label = TexMobject("\\theta", **self.tex_config)
        label.add_updater(lambda l: l.move_to(self.get_origin() + 0.75 * toward(self.theta.get_value() / 2)))

        angle_label = VGroup(arc, label)
        self.play(Write(angle_label))
        self.wait(0.5)

        # make a ray crossing through the origin and point A,
        # and a line tangent to the circle and perpendicular to the x-axis
        self.ray = always_redraw(lambda: Line(
            self.get_origin() - 12 * toward(self.theta.get_value()),
            self.get_origin() + 12 * toward(self.theta.get_value()),
            stroke_color = BLUE, **self.line_config
        ))

        self.perpend = always_redraw(lambda: Line(
            self.circle.point_at_angle(0) + DOWN * 5,
            self.circle.point_at_angle(0) + UP * 5,
            stroke_color = GREEN, **self.line_config
        ))

        # make point B
        p_b = Dot(**self.dot_config)
        p_b.add_updater(lambda b: b.move_to(self.get_intersection()))
        self.dots = VGroup(p_a, p_b)
        
        self.add_foreground_mobjects(self.radius, p_a)
        self.play(ShowCreation(self.perpend))
        self.play(ShowCreation(self.ray))
        self.wait(0.5)

        self.add_foreground_mobjects(p_b)
        self.play(ShowCreation(p_b))

        # the height of point B is tangent of the given angle
        tan_eq = TexMobject("\\tan\\theta", **self.tex_config)
        brace = always_redraw(lambda: Brace(
                Line(self.circle.point_at_angle(0), self.get_intersection()),
                RIGHT
            ).put_at_tip(tan_eq)
        )

        self.play(GrowFromCenter(brace), Write(tan_eq))
        self.wait(2)

        self.play(self.theta.set_value, np.radians(-30))
        self.wait(0.5)
        self.play(self.theta.set_value, np.radians(145), run_time = 2)
        self.wait(0.5)
        self.play(self.theta.set_value, np.radians(225))
        self.wait(0.5)
        self.play(self.theta.set_value, np.radians(25))
        self.wait(2)

        self.play(FadeOut(brace), FadeOut(tan_eq), FadeOut(angle_label))
        self.play(ApplyMethod(self.theta.set_value, 0))
        self.wait(1)

    def layout_graph(self):
        everything = VGroup(self.plane, self.circle)
        self.play(ApplyMethod(everything.scale, 1/3))

        wrap = Square(side_length = everything.get_width() + 0.5, fill_color = DARK_GRAY)
        self.play(DrawBorderThenFill(wrap))
        everything.add(wrap)

        self.play(ApplyMethod(everything.to_edge, LEFT))
        self.bring_to_back(self.plane, self.circle)

        self.graph_plane = Axes(**self.graph_plane_config).to_edge(RIGHT)

        numbers = VGroup()
        for i in range(1, 5):
            label = TexMobject(str(i), "\\pi", **self.tex_config).move_to(self.graph_plane.coords_to_point(i * PI, -0.3)).scale(0.5)
            numbers.add(label)

        numbers.add(TexMobject("\\theta").move_to(self.graph_plane.coords_to_point(4.2 * PI, -0.5)).scale(0.75))

        tan_eq = TexMobject("\\tan\\theta", **self.tex_config).next_to(self.graph_plane, UP)
        self.play(ShowCreation(self.graph_plane), Write(numbers), Write(tan_eq))
        self.wait(3)

    def draw_graph(self):
        tan_graph = VGroup(**self.graph_config)
        tan_graph.set_points_as_corners([self.graph_plane.coords_to_point(0, 0), self.graph_plane.coords_to_point(-0.001, 0)])

        def tan_update(graph):
            dest = self.graph_plane.coords_to_point(self.theta.get_value(), np.tan(self.theta.get_value()))

            if dest[1] < tan_graph.get_last_point()[1]:
                tan_graph.start_new_path(dest)
            else:
                tan_graph.add_line_to(dest)

        tan_graph.add_updater(tan_update)

        dot = Dot(**self.dot_config)
        dot.add_updater(lambda d: d.move_to(
            self.graph_plane.coords_to_point(self.theta.get_value(), np.tan(self.theta.get_value()))
        ))
            
        perpend = always_redraw(lambda: Line(
            self.graph_plane.coords_to_point(self.theta.get_value(), np.tan(self.theta.get_value())),
            self.graph_plane.coords_to_point(self.theta.get_value(), 0),
            color = WHITE
        ))

        self.add(tan_graph, perpend, dot)
        tan_graph.save_state()

        self.play(ApplyMethod(self.theta.set_value, 4.8 * PI, rate_func = linear, run_time = 30))
        self.wait(2)

        self.theta.set_value(0)
        tan_graph.restore()
        hor = always_redraw(lambda: Line(
            self.get_intersection(),
            self.graph_plane.coords_to_point(self.theta.get_value(), np.tan(self.theta.get_value())),
            color = YELLOW
        ))

        self.add(hor)

        self.play(ApplyMethod(self.theta.set_value, 4.8 * PI, rate_func = linear, run_time = 30))
        self.wait(3)
