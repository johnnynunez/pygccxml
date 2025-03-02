# Copyright 2014-2017 Insight Software Consortium.
# Copyright 2004-2009 Roman Yakovenko.
# Distributed under the Boost Software License, Version 1.0.
# See http://www.boost.org/LICENSE_1_0.txt

import pytest

from . import autoconfig

from pygccxml import utils
from pygccxml import parser
from pygccxml import declarations


def is_sub_path(root, some_path):
    root = utils.normalize_path(root)
    some_path = utils.normalize_path(some_path)
    return some_path.startswith(root)


TEST_FILES = [
    "core_ns_join_1.hpp",
    "core_ns_join_2.hpp",
    "core_ns_join_3.hpp",
    "core_membership.hpp",
    "core_class_hierarchy.hpp",
    "core_types.hpp",
    "core_diamand_hierarchy_base.hpp",
    "core_diamand_hierarchy_derived1.hpp",
    "core_diamand_hierarchy_derived2.hpp",
    "core_diamand_hierarchy_final_derived.hpp",
    "core_overloads_1.hpp",
    "core_overloads_2.hpp",
    "abstract_classes.hpp",
]


@pytest.fixture
def global_ns_fixture_all_at_once1():
    COMPILATION_MODE = parser.COMPILATION_MODE.ALL_AT_ONCE
    INIT_OPTIMIZER = True
    config = autoconfig.cxx_parsers_cfg.config.clone()
    decls = parser.parse(TEST_FILES, config, COMPILATION_MODE)
    global_ns = declarations.get_global_namespace(decls)
    if INIT_OPTIMIZER:
        global_ns.init_optimizer()
    return global_ns


@pytest.fixture
def global_ns_fixture_all_at_once2():
    COMPILATION_MODE = parser.COMPILATION_MODE.ALL_AT_ONCE
    INIT_OPTIMIZER = False
    config = autoconfig.cxx_parsers_cfg.config.clone()
    decls = parser.parse(TEST_FILES, config, COMPILATION_MODE)
    global_ns = declarations.get_global_namespace(decls)
    if INIT_OPTIMIZER:
        global_ns.init_optimizer()
    return global_ns


@pytest.fixture
def global_ns_fixture_file_by_file1():
    COMPILATION_MODE = parser.COMPILATION_MODE.FILE_BY_FILE
    INIT_OPTIMIZER = True
    config = autoconfig.cxx_parsers_cfg.config.clone()
    decls = parser.parse(TEST_FILES, config, COMPILATION_MODE)
    global_ns = declarations.get_global_namespace(decls)
    if INIT_OPTIMIZER:
        global_ns.init_optimizer()
    return global_ns


@pytest.fixture
def global_ns_fixture_file_by_file2():
    COMPILATION_MODE = parser.COMPILATION_MODE.FILE_BY_FILE
    INIT_OPTIMIZER = False
    config = autoconfig.cxx_parsers_cfg.config.clone()
    decls = parser.parse(TEST_FILES, config, COMPILATION_MODE)
    global_ns = declarations.get_global_namespace(decls)
    if INIT_OPTIMIZER:
        global_ns.init_optimizer()
    return global_ns


@pytest.fixture
def global_ns(request):
    return request.getfixturevalue(request.param)


# @pytest.mark.parametrize(
#     "global_ns",
#     [
#         "global_ns_fixture_all_at_once1",
#         "global_ns_fixture_all_at_once2",
#         "global_ns_fixture_file_by_file1",
#         "global_ns_fixture_file_by_file2",
#     ],
#     indirect=True,
# )
# def test_top_parent(global_ns):
#     enum = global_ns.enumeration("::ns::ns32::E33")
#     assert global_ns is enum.top_parent


# # tests namespaces join functionality. described in gccxml.py
# @pytest.mark.parametrize(
#     "global_ns",
#     [
#         "global_ns_fixture_all_at_once1",
#         "global_ns_fixture_all_at_once2",
#         "global_ns_fixture_file_by_file1",
#         "global_ns_fixture_file_by_file2",
#     ],
#     indirect=True,
# )
# def test_nss_join(global_ns):
#     # list of all namespaces
#     nss = ["::ns", "::ns::ns12", "::ns::ns22", "::ns::ns32"]
#     # list of all namespaces that have unnamed namespace
#     # unnamed_nss = nss[1:] doing nothing with this list ?
#     # list of all enums [0:2] [3:5] [6:8] - has same parent
#     enums = [
#         "::E11",
#         "::E21",
#         "::E31",
#         "::ns::E12",
#         "::ns::E22",
#         "::ns::E32",
#         "::ns::ns12::E13",
#         "::ns::ns22::E23",
#         "::ns::ns32::E33",
#     ]

#     for ns in nss:
#         global_ns.namespace(ns)

#     for enum in enums:
#         global_ns.enumeration(enum)

#     ns = global_ns.namespace(nss[0])
#     ns12 = global_ns.namespace(nss[1])
#     ns22 = global_ns.namespace(nss[2])
#     ns32 = global_ns.namespace(nss[3])
#     assert ns is ns12.parent is ns22.parent is ns32.parent

#     e11 = global_ns.enumeration(enums[0])
#     e21 = global_ns.enumeration(enums[1])
#     e31 = global_ns.enumeration(enums[2])
#     assert e11.parent is e21.parent is e31.parent

#     nse12 = global_ns.enumeration(enums[3])
#     nse23 = global_ns.enumeration(enums[4])
#     nse33 = global_ns.enumeration(enums[5])
#     assert ns is nse12.parent is nse23.parent is nse33.parent


# def _test_ns_membership(ns, enum_name):
#     unnamed_enum = ns.enumeration(
#         lambda d: d.name == ""
#         and is_sub_path(autoconfig.data_directory, d.location.file_name),
#         recursive=False,
#     )
#     assert unnamed_enum in ns.declarations

#     enum = ns.enumeration(enum_name, recursive=False)
#     assert enum in ns.declarations
#     assert unnamed_enum.parent is ns
#     assert enum.parent is ns


# def _test_class_membership(class_inst, enum_name, access):
#     # getting enum through get_members function
#     nested_enum1 = class_inst.enumeration(
#         name=enum_name, function=declarations.access_type_matcher_t(access)
#     )

#     # getting enum through declarations property
#     nested_enum2 = class_inst.enumeration(enum_name)

#     # it shoud be same object
#     assert nested_enum1 is nested_enum2

#     # check whether we meaning same class instance
#     assert class_inst is nested_enum1.parent is nested_enum2.parent


# @pytest.mark.parametrize(
#     "global_ns",
#     [
#         "global_ns_fixture_all_at_once1",
#         "global_ns_fixture_all_at_once2",
#         "global_ns_fixture_file_by_file1",
#         "global_ns_fixture_file_by_file2",
#     ],
#     indirect=True,
# )
# # test gccxml_file_reader_t._update_membership algorithm
# def test_membership(global_ns):
#     core_membership = global_ns.namespace("membership")
#     _test_ns_membership(global_ns, "EGlobal")
#     _test_ns_membership(core_membership.namespace("enums_ns"), "EWithin")
#     _test_ns_membership(core_membership.namespace(""), "EWithinUnnamed")
#     class_nested_enums = core_membership.class_("class_for_nested_enums_t")
#     _test_class_membership(
#         class_nested_enums,
#         "ENestedPublic",
#         declarations.ACCESS_TYPES.PUBLIC
#     )
#     _test_class_membership(
#         class_nested_enums,
#         "ENestedProtected",
#         declarations.ACCESS_TYPES.PROTECTED
#     )
#     _test_class_membership(
#         class_nested_enums,
#         "ENestedPrivate",
#         declarations.ACCESS_TYPES.PRIVATE
#     )


@pytest.mark.parametrize(
    "global_ns",
    [
        # "global_ns_fixture_all_at_once1",
        # "global_ns_fixture_all_at_once2",
        "global_ns_fixture_file_by_file1",
        # "global_ns_fixture_file_by_file2",
    ],
    indirect=True,
)
def test_mangled_name_namespace(global_ns):
    std = global_ns.namespace("std")
    assert std is not None
    assert std.mangled is None
    raise
