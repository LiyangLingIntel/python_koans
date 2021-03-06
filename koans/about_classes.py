#!/usr/bin/env python
# -*- coding: utf-8 -*-

from runner.koan import *


class AboutClasses(Koan):
    class Dog:
        "Dogs need regular walkies. Never, ever let them drive."

    def test_instances_of_classes_can_be_created_adding_parentheses(self):
        # NOTE: The .__name__ attribute will convert the class
        # into a string value.
        fido = self.Dog()
        self.assertEqual("Dog", fido.__class__.__name__)

    def test_classes_have_docstrings(self):
        self.assertRegex(self.Dog.__doc__, "Dogs need regular walkies. Never, ever let them drive.")

    # ------------------------------------------------------------------

    class Dog2:
        def __init__(self):
            self._name = 'Paul'
            self.__name = 'Tom'

        def set_name(self, a_name):
            self._name = a_name

    def test_init_method_is_the_constructor(self):
        dog = self.Dog2()
        self.assertEqual('Paul', dog._name)

    def test_private_attributes_are_not_really_private(self):
        dog = self.Dog2()
        dog.set_name("Fido")
        self.assertEqual("Fido", dog._name)
        # The _ prefix in _name implies private ownership, but nothing is truly
        # private in Python.
        # ???
        with self.assertRaises(AttributeError): private_name = dog.__name
        # After deeper searching:
        # https://stackoverflow.com/questions/1301346/what-is-the-meaning-of-single-and-double-underscore-before-an-object-name
        # _single_leading_underscore: weak "internal use" indicator,  nothing special is done with the name itself.
        # _double_leading_underscore: __spam (at least two leading underscores, at most one trailing underscore) is
        #                             textually replaced with _classname__spam, so it can be used to define
        #                             class-private attributes. This is called Name Mangling.
        # Note that the mangling rules are designed mostly to avoid accidents;
        # it still is possible for a determined soul to access or modify a variable that is considered private.
        self.assertEqual("Tom", dog._Dog2__name)

    def test_you_can_also_access_the_value_out_using_getattr_and_dict(self):
        fido = self.Dog2()
        fido.set_name("Fido")

        self.assertEqual("Fido", getattr(fido, "_name"))
        # getattr(), setattr() and delattr() are a way of accessing attributes
        # by method rather than through assignment operators

        self.assertEqual("Fido", fido.__dict__["_name"])
        # Yes, this works here, but don't rely on the __dict__ object! Some
        # class implementations use optimization which result in __dict__ not
        # showing everything.

    # ------------------------------------------------------------------

    class Dog3:
        def __init__(self):
            self._name = None

        def set_name(self, a_name):
            self._name = a_name

        def get_name(self):
            return self._name

        name = property(get_name, set_name)

    def test_that_name_can_be_read_as_a_property(self):
        fido = self.Dog3()
        fido.set_name("Fido")

        # access as method
        self.assertEqual("Fido", fido.get_name())

        # access as property
        self.assertEqual("Fido", fido.name)

    # ------------------------------------------------------------------

    class Dog4:
        def __init__(self):
            self._name = None

        @property
        def name(self):
            return self._name

        @name.setter
        def name(self, a_name):
            self._name = a_name

    def test_creating_properties_with_decorators_is_slightly_easier(self):
        fido = self.Dog4()

        fido.name = "Fido"
        self.assertEqual("Fido", fido.name)

    # ------------------------------------------------------------------

    class Dog5:
        def __init__(self, initial_name):
            self._name = initial_name

        @property
        def name(self):
            return self._name

    def test_init_provides_initial_values_for_instance_variables(self):
        fido = self.Dog5("Fido")
        self.assertEqual("Fido", fido.name)

    def test_args_must_match_init(self):
        with self.assertRaises(TypeError):
            self.Dog5()

        # THINK ABOUT IT:
        # Why is this so?
        # Cos positional argument: 'initial_name' is required

    def test_different_objects_have_different_instance_variables(self):
        fido = self.Dog5("Fido")
        rover = self.Dog5("Rover")

        self.assertEqual(False, rover.name == fido.name)

    # ------------------------------------------------------------------

    class Dog6:
        def __init__(self, initial_name):
            self._name = initial_name

        def get_self(self):
            return self

        def __str__(self):
            #
            # Implement this!
            #
            return "Fido"

        def __repr__(self):
            return "<Dog named '" + self._name + "'>"

    def test_inside_a_method_self_refers_to_the_containing_object(self):
        fido = self.Dog6("Fido")

        self.assertEqual(fido, fido.get_self())  # Not a string!

    def test_str_provides_a_string_version_of_the_object(self):
        fido = self.Dog6("Fido")

        self.assertEqual("Fido", str(fido))

    def test_str_is_used_explicitly_in_string_interpolation(self):
        fido = self.Dog6("Fido")

        self.assertEqual("My dog is Fido", "My dog is " + str(fido))

    def test_repr_provides_a_more_complete_string_version(self):
        fido = self.Dog6("Fido")
        self.assertEqual("<Dog named 'Fido'>", repr(fido))

    def test_all_objects_support_str_and_repr(self):
        seq = [1, 2, 3]

        self.assertEqual('[1, 2, 3]', str(seq))
        self.assertEqual('[1, 2, 3]', repr(seq))

        self.assertEqual('STRING', str("STRING"))
        self.assertEqual("'STRING'", repr("STRING"))  # by default, python string is wrapped by single quote

    # The default implementation is useless (it???s hard to think of one which wouldn???t be, but yeah)
    # __repr__ goal is to be unambiguous
    # __str__ goal is to be readable
    # Container???s __str__ uses contained objects??? __repr__
    # ideas from https://stackoverflow.com/questions/1436703/what-is-the-difference-between-str-and-repr/1436756#1436756
