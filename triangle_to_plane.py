from manimlib.imports import *
from math import *

# unit vector toward given angle
def toward(angle):
    return np.array([cos(angle), sin(angle), 0])

class TriangleToPlane(Scene):
    CONFIG = {
        "hypo_config": {
            "stroke_color": RED,
            "stroke_width": 4,
        },

        "width_config": {
            "stroke_color": YELLOW,
            "stroke_width": 4,
        },

        "height_config": {
            "stroke_color": PURPLE,
            "stroke_width": 4,
        },

        "angle_arc_config": {
            "radius": 0.5,
            "stroke_color": WHITE,
            "stroke_width": 2,
        },

        "right_indicator_config": {
            "stroke_color": WHITE,
            "stroke_width": 2,
        },

        "circle_config": {
            "radius": 3,
            "color": RED_B,
        },
        
        "dot_config": {
            "color": YELLOW,
        },

        "tex_config": {
            "tex_to_color_map": {
                "\\sin": PURPLE,
                "\\cos": YELLOW,
            }
        },

        "plane_config": {
            "x_axis_config": {
                "unit_size": 3,
                "include_numbers": True,
                "numbers_to_show": [-1, 1],
            },

            "y_axis_config": {
                "unit_size": 3,
                "include_numbers": True,
                "numbers_to_show": [-1, 1],
            },
        },
    }

    def construct(self):
        self.introduce_triangle()
        self.place_on_plane()
        self.write_coordinate()
        self.play_with_circle()

    def introduce_triangle(self):
        self.set_center(DL)
        self.radius = ValueTracker(4)
        self.theta = ValueTracker(0.7)

        self.triangle = self.make_triangle()
        self.right_indicator = self.make_right_indicator()

        self.play(ShowCreation(self.triangle), ShowCreation(self.right_indicator))
        self.wait(1)

        self.labels = self.make_labels("x", "y", "r")
        self.play(Write(self.labels))

        self.angle_label = self.make_angle_label("\\theta")

        self.play(Write(self.angle_label))
        self.wait(2)

        trig_def = VGroup(
                TexMobject("\\sin \\theta = \\frac{y}{r}", **self.tex_config),
                TexMobject("\\cos \\theta = \\frac{x}{r}", **self.tex_config)
                ).arrange(DOWN, center=False, aligned_edge=LEFT).to_corner(UR)

        self.play(Write(trig_def))
        self.wait(2)

        labels = self.make_labels("r\\cos\\theta", "r\\sin\\theta", "r")
        self.play(Transform(self.labels, labels))
        self.wait(3)

        self.play(FadeOut(trig_def))
        self.wait(1)

    def place_on_plane(self):
        labels = self.make_labels("1\\cos\\theta", "1\\sin\\theta", "1")
        self.play(ApplyMethod(self.radius.set_value, 3), Transform(self.labels, labels))
        self.wait(2)

        labels = self.make_labels("\\cos\\theta", "\\sin\\theta", "1")
        self.play(Transform(self.labels, labels))
        self.wait(1)

        _, _, rl = self.labels
        self.play(FadeOut(rl))
        self.labels.remove(rl)
        self.wait(1)

        self.move_center(ORIGIN)
        
        self.add_foreground_mobjects(self.triangle, self.angle_label, self.right_indicator, self.labels)

        # i think it's too heavy to always_redraw() them...
        self.circle = Circle(**self.circle_config).move_to(self.get_center())
        self.plane = NumberPlane(**self.plane_config).move_to(self.get_center())

        self.play(ShowCreation(self.plane), ShowCreation(self.circle))
        self.wait(2)

    def write_coordinate(self):
        self.dot = Dot(**self.dot_config)
        self.dot.add_updater(lambda d: d.move_to(
            self.get_center() + self.radius.get_value() * toward(self.theta.get_value())
        ))

        self.add_foreground_mobjects(self.dot)
        self.play(ShowCreation(self.dot))
        self.wait(1)

        self.coord = TexMobject("(", "x", ",", "y", ")", **self.tex_config)
        self.coord.next_to(self.dot.get_center(), toward(self.theta.get_value()))

        self.play(Write(self.coord))
        self.wait(1)
        
        coord = TexMobject("(", "\\cos\\theta", ",", "y", ")")
        coord.next_to(self.dot.get_center(), toward(self.theta.get_value()))

        cos_eq, sin_eq = self.labels
        cos_eq.clear_updaters()
        sin_eq.clear_updaters()

        self.play(
            Transform(self.coord[1], TexMobject("\\cos\\theta", **self.tex_config).move_to(coord[1])),
            ApplyMethod(cos_eq.move_to, coord[1]),
            *[ApplyMethod(self.coord[i].move_to, coord[i]) for i in range(2, 5)]
        )
        self.remove(cos_eq)
        self.wait(1)

        coord = TexMobject("(\\cos\\theta,", "\\sin\\theta", ")")
        coord.next_to(self.dot.get_center(), toward(self.theta.get_value()))

        self.play(
            Transform(self.coord[3], TexMobject("\\sin\\theta", **self.tex_config).move_to(coord[1])),
            ApplyMethod(sin_eq.move_to, coord[1]),
            ApplyMethod(self.coord[4].move_to, coord[2])
        )
        self.remove(sin_eq)

        self.coord.add_updater(lambda c: c.next_to(self.dot.get_center(), toward(self.theta.get_value())))
        self.wait(2)

    def play_with_circle(self):
        theta_display = VGroup(TexMobject("=", **self.tex_config), DecimalNumber()).arrange(RIGHT)
        theta_display[1].add_updater(lambda d: d.set_value(self.theta.get_value()))
        theta_display.add_updater(lambda d: d.next_to(self.angle_label[1]))
        
        self.play(Write(theta_display))

        xy_display = VGroup(
            TexMobject("\\cos\\theta=", **self.tex_config), DecimalNumber(cos(self.theta.get_value()), color = YELLOW),
            TexMobject("\\sin\\theta=", **self.tex_config), DecimalNumber(sin(self.theta.get_value()), color = PURPLE)
        )

        xy_display[1].next_to(xy_display[0])
        xy_display[2].next_to(xy_display[0], DOWN)
        xy_display[3].next_to(xy_display[2])
        xy_display.to_corner(UL)

        self.play(Write(xy_display[0]), Write(xy_display[2]))
        self.wait(1)

        coord = TexMobject("(", "\\cos\\theta", ",", "\\sin\\theta", ")")
        coord.next_to(self.dot.get_center(), toward(self.theta.get_value()))

        self.play(TransformFromCopy(coord[1], xy_display[1]), TransformFromCopy(coord[3], xy_display[3]))
        self.wait(2)

        xy_display[1].add_updater(lambda x: x.set_value(cos(self.theta.get_value())))
        xy_display[3].add_updater(lambda y: y.set_value(sin(self.theta.get_value())))

        self.play(self.theta.set_value, PI / 4)
        self.wait(0.5)
        self.play(self.theta.set_value, 0.7 * PI)
        self.wait(0.5)
        self.play(self.theta.set_value, -PI / 3, run_time = 1.5)
        self.wait(2)
        self.play(self.theta.set_value, 3/2 * PI, run_time = 2)
        self.wait(1.5)
        self.play(self.theta.set_value, 1, run_time = 2)
        self.wait(1.5)
        self.play(self.theta.set_value, -7/4 * PI, run_time = 2)
        self.wait(2)

        self.play(FadeOut(theta_display), FadeOut(xy_display))

    def get_center(self):
        return np.array([self.center_x.get_value(), self.center_y.get_value(), 0])

    def set_center(self, pos):
        self.center_x = ValueTracker(pos[0])
        self.center_y = ValueTracker(pos[1])

    def move_center(self, pos, run_time = 1):
        self.play(ApplyMethod(self.center_x.set_value, pos[0]), ApplyMethod(self.center_y.set_value, pos[1]))

    def make_triangle(self):
        # dirty...
        width = always_redraw(lambda: Line(
            self.get_center(),
            self.get_center() + self.radius.get_value() * cos(self.theta.get_value()) * toward(0),
            **self.width_config
        ))

        height = always_redraw(lambda: Line(
            self.get_center() + self.radius.get_value() * toward(self.theta.get_value()),
            self.get_center() + self.radius.get_value() * cos(self.theta.get_value()) * toward(0),
            **self.height_config
        ))

        hypo = always_redraw(lambda: Line(
            self.get_center(),
            self.get_center() + self.radius.get_value() * toward(self.theta.get_value()),
            **self.hypo_config
        ))

        return VGroup(width, height, hypo)

    def make_labels(self, wt, ht, rt):
        width, height, hypo = self.triangle

        width_label = TexMobject(wt, **self.tex_config)
        width_label.add_updater(lambda l: l.next_to(
            width.get_center(),
            DOWN if width.get_center()[0] - self.get_center()[0] > 0 else UP
        ))

        height_label = TexMobject(ht, **self.tex_config)
        height_label.add_updater(lambda l: l.next_to(
            height.get_center(),
            RIGHT if height.get_center()[1] - self.get_center()[1] > 0 else LEFT
        ))

        hypo_label = TexMobject(rt, **self.tex_config)
        hypo_label.add_updater(lambda l: l.next_to(
            hypo.get_center(),
            toward(self.theta.get_value() + PI / 2) if fmod(self.theta.get_value(), TAU) < PI else toward(self.theta.get_value() - PI / 2)
        ))

        return VGroup(width_label, height_label, hypo_label)

    def make_angle_label(self, tex):
        arc = always_redraw(lambda: Arc(
            arc_center = self.get_center(),
            angle = self.theta.get_value(),
            **self.angle_arc_config
        ))

        label = TexMobject(tex, **self.tex_config)
        label.add_updater(lambda l: l.move_to(self.get_center() + 0.75 * toward(self.theta.get_value() / 2)))

        return VGroup(arc, label)

    def get_right_len(self):
        l = self.radius.get_value() * min(abs(sin(self.theta.get_value())), abs(cos(self.theta.get_value()))) / 10
        return l if l < 0.7 else 0.7

    def make_right_indicator(self):
        # yeek...
        hor = always_redraw(lambda: Line(
            self.get_right_len() * (UP if sin(self.theta.get_value()) > 0 else DOWN),
            self.get_right_len() * ((UP if sin(self.theta.get_value()) > 0 else DOWN) + (LEFT if cos(self.theta.get_value()) > 0 else RIGHT)),
            **self.right_indicator_config
        ).shift(self.get_center() + RIGHT * self.radius.get_value() * cos(self.theta.get_value())))

        vert = always_redraw(lambda: Line(
            self.get_right_len() * (LEFT if cos(self.theta.get_value()) > 0 else RIGHT),
            self.get_right_len() * ((UP if sin(self.theta.get_value()) > 0 else DOWN) + (LEFT if cos(self.theta.get_value()) > 0 else RIGHT)),
            **self.right_indicator_config
        ).shift(self.get_center() + RIGHT * self.radius.get_value() * cos(self.theta.get_value())))

        return VGroup(hor, vert)
