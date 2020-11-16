from manimlib.imports import *
from math import *

# unit vector toward given angle
def toward(angle):
    return np.array([cos(angle), sin(angle), 0])

class Sine(Scene):
    CONFIG = {
        "hypo_config": {
            "stroke_color": WHITE,
            "stroke_width": 4
        },

        "wh_config": {
            "stroke_color": YELLOW,
            "stroke_width": 4
        },

        "angle_arc_config": {
            "radius": 0.5,
            "stroke_color": WHITE,
            "stroke_width": 2
        }
    }

    def construct(self):
        self.introduce_triangle()
        self.place_on_plane()
        self.play_with_circle()
        self.show_graph()

    def introduce_triangle(self):
        self.center = Dot(DL)
        self.radius = ValueTracker(4)
        self.theta = ValueTracker(0.7)

        tri = self.make_triangle()

        self.play(ShowCreation(tri))

        label_group = self.make_labels_to_triangle(tri, "x", "y", "r")
        self.play(Write(label_group))

        angle_label = self.make_angle_label("\\theta")

        self.play(Write(angle_label))
        self.wait(2)

        trig_def = VGroup(
                TexMobject("\\sin \\theta = \\frac{y}{r}"),
                TexMobject("\\cos \\theta = \\frac{x}{r}")
                ).arrange(DOWN, center=False, aligned_edge=LEFT).to_corner(UR)

        self.play(Write(trig_def))

        labels_new = self.make_labels_to_triangle(tri, "r\\cos\\theta", "r\\sin\\theta", "r")
        self.play(Transform(label_group, labels_new))
        label_group = labels_new

        self.wait(1)
        self.play(self.theta.set_value, PI / 3, run_time = 1)
        self.play(self.theta.set_value, PI / 6, run_time = 1)
        self.play(self.theta.set_value, PI / 4, run_time = 1)

        self.play(FadeOut(trig_def))

    def make_triangle(self):
        # dirty...
        width = always_redraw(lambda: Line(
            self.center.get_center(),
            self.center.get_center() + self.radius.get_value() * cos(self.theta.get_value()) * toward(0),
            **self.wh_config
        ))

        height = always_redraw(lambda: Line(
            self.center.get_center() + self.radius.get_value() * toward(self.theta.get_value()),
            self.center.get_center() + self.radius.get_value() * cos(self.theta.get_value()) * toward(0),
            **self.wh_config
        ))

        hypo = always_redraw(lambda: Line(
            self.center.get_center(),
            self.center.get_center() + self.radius.get_value() * toward(self.theta.get_value()),
            **self.hypo_config
        ))

        return VGroup(width, height, hypo)

    def make_labels_to_triangle(self, tri, wt, ht, rt):
        width, height, hypo = tri

        width_label = TexMobject(wt)
        width_label.add_updater(lambda l: l.next_to(
            width.get_center(),
            DOWN if width.get_center()[0] - self.center.get_center()[0] > 0 else UP
        ))

        height_label = TexMobject(ht)
        height_label.add_updater(lambda l: l.next_to(
            height.get_center(),
            RIGHT if height.get_center()[1] - self.center.get_center()[1] > 0 else LEFT
        ))

        hypo_label = TexMobject(rt)
        hypo_label.add_updater(lambda l: l.next_to(
            hypo.get_center(),
            toward(self.theta.get_value() + PI / 2) if fmod(self.theta.get_value(), TAU) < PI else toward(self.theta.get_value() - PI / 2)
        ))

        return VGroup(width_label, height_label, hypo_label)

    def make_angle_label(self, tex):
        arc = always_redraw(lambda: Arc(
            arc_center = self.center.get_center(),
            angle = self.theta.get_value(),
            **self.angle_arc_config
        ))

        label = TexMobject(tex)
        label.add_updater(lambda l: l.next_to(arc.point_from_proportion(.5), toward(self.theta.get_value() / 2)))

        return VGroup(arc, label)

    def place_on_plane(self):
        pass

    def play_with_circle(self):
        pass

    def show_graph(self):
        pass
