import pytest

from clickhouse.utils import (_Unset, convert_classname_to_tablename,
                              convert_tablename_to_classname, unset)


@pytest.mark.parametrize(
    "classname, tablename",
    (
        ("API", "api"),
        ("Request", "request"),
        ("APIRequest", "api_request"),
        ("ServiceRequest", "service_request"),
        ("API_Request", "api_request"),
        ("API_ServiceRequest", "api_service_request"),
    ),
)
def test_convert_classname_to_tablename(classname, tablename):
    assert (got := convert_classname_to_tablename(classname)) == tablename, "got %s want %s" % (
        got,
        tablename,
    )


@pytest.mark.parametrize(
    "tablename, classname",
    (
        ("request", "Request"),
        ("service_request", "ServiceRequest"),
        ("api_service_request", "ApiServiceRequest"),
        ("service__request", "ServiceRequest"),
    ),
)
def test_convert_tablename_to_classname(tablename, classname):
    assert (got := convert_tablename_to_classname(tablename)) == classname, "got %s want %s" % (
        got,
        classname,
    )


def test_unset():
    assert unset == _Unset()
    assert unset == unset
    assert unset is unset
    assert isinstance(unset, _Unset)
    assert not unset
    assert str(unset) == "<unset>"
