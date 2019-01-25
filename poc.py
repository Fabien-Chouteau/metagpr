import toml
import os


def mkdir(path):
    if not os.path.exists(path):
        os.makedirs(path)


class IntParam():
    def __init__(self, name, default=None, min=None, max=None):
        self.name = name
        self.default = default
        self.min = min
        self.max = max
        self.value = None

    def set_value(self, value):
        v = int(value)
        if v < self.min:
            raise
        if v > self.max:
            raise

        self.value = v

    def gen_source(self):
        if self.value is None:
            self.value = self.default

        if self.value is None:
            raise

        out = ""
        if not self.min is None:
            out += "   %s_Min : constant := %d;\n" % (self.name, self.min)
        if not self.max is None:
            out += "   %s_Max : constant := %d;\n" % (self.name, self.max)

        out += "   %s : constant := %d;\n" % (self.name, self.value)

        return out


class BoolParam():
    def __init__(self, name, default=None):
        self.name = name
        self.default = default
        self.value = None

    def set_value(self, value):
        self.value = value

    def gen_source(self):
        if self.value is None:
            self.value = self.default

        if self.value is None:
            raise

        return "   %s : constant Boolean := %s;\n" % (self.name, str(self.value))


class StringParam():
    def __init__(self, name, default=None):
        self.name = name
        self.default = default
        self.value = None

    def set_value(self, value):
        self.value = value

    def gen_source(self):
        if self.value is None:
            self.value = self.default

        if self.value is None:
            raise

        return "   %s : constant String := \"%s\";\n" % (self.name, self.value)


class Project():
    def __init__(self, filepath):
        self.filepath = filepath
        self.toml = toml.load(filepath)
        self.root_dir = os.path.dirname(os.path.realpath(filepath))
        self.dependecies = []
        self.parameter = {}
        self.name = os.path.splitext(os.path.basename(filepath))[0]

        self.main = self.toml.get("main", [])

        # add quotes
        self.main = list(map(lambda x : "\"%s\"" % x, self.main))

        self.source_dirs = self.toml.get("source_dirs", [])

        # Convert to absolute path
        self.source_dirs = list(map(lambda x : os.path.join(self.root_dir, x), self.source_dirs))

        # add quotes
        self.source_dirs = list(map(lambda x : "\"%s\"" % x, self.source_dirs))

        self.object_dir = self.toml.get("object_dir", "obj")

        if "configuration" in self.toml:
            config = self.toml["configuration"]
            self.config_package = config.get("config_package", "Config")
            if "parameter" in config:
                params = config["parameter"]
                for id in params:
                    if params[id]["type"] == "int":
                        self.parameter[id] = IntParam(id,
                                                       params[id].get("default"),
                                                       params[id].get("min"),
                                                       params[id].get("max")
                                                       )
                    elif params[id]["type"] == "bool":
                        self.parameter[id] = BoolParam(id,
                                                        params[id].get("default")
                                                        )
                    elif params[id]["type"] == "string":
                        self.parameter[id] = StringParam(id,
                                                          params[id].get("default")
                                                          )
                    else:
                        raise

        if "dependencies" in self.toml:
            for dep in self.toml["dependencies"]:
                prj = Project(os.path.join (self.root_dir, dep["path"]))
                self.dependecies += [prj]

                if "parameter" in dep:
                    params = dep["parameter"]
                    for id in params:
                        prj.set_parameter(id, params[id])

    def set_parameter(self, id, value):
        self.parameter[id].set_value(value)

    def gen_project(self, base):
        object_dir = os.path.join (base, self.object_dir)
        mkdir(object_dir)

        # TODO: propagate parameter values from here

        prj_filepath = os.path.join(base, "%s.gpr" % self.name)
        with open(prj_filepath, "w") as file:
            for dep in self.dependecies:
                dep.gen_config(os.path.join (object_dir, dep.name))
                prj = dep.gen_project(os.path.join (object_dir, dep.name))

                file.write("with \"%s\";\n" % prj)

            file.write("project %s is\n" % self.name)
            file.write("   for Source_dirs use (%s);\n" % (", ".join(self.source_dirs + ["\"config\""])))
            file.write("   for Object_Dir use \"%s\";\n" % self.object_dir)

            if self.main:
                file.write("   for Main use (%s);\n" % (", ".join(self.main)))

            file.write("end %s;\n" % self.name)

        return prj_filepath

    def gen_config(self, base):
        conf_dir = os.path.join (base, "config")
        mkdir(conf_dir)
        with open(os.path.join(conf_dir, self.config_package.lower() + ".ads"), "w") as file:
            file.write("package %s is\n" % self.config_package)
            for param in self.parameter:
                file.write(self.parameter[param].gen_source())
            file.write("end %s;\n" % self.config_package)

Test = Project("example/app/app.mgpr")

Test.gen_config(".")
Test.gen_project(".")
