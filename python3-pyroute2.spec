#
# Conditional build:
%bcond_without	tests	# unit tests

%define		module		pyroute2
Summary:	Python Netlink library
Name:		python3-%{module}
Version:	0.9.6
Release:	1
License:	GPLv2+ or Apache v2
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/pyroute2/
Source0:	https://files.pythonhosted.org/packages/source/p/%{module}/%{module}-%{version}.tar.gz
# Source0-md5:	a8c34ff9de89e55d5d50e9959937e56f
URL:		https://pyroute2.org/
BuildRequires:	python3-build
BuildRequires:	python3-installer
BuildRequires:	python3-modules >= 1:3.9
BuildRequires:	python3-setuptools
%if %{with tests}
BuildRequires:	python3-pytest
BuildRequires:	python3-pytest-asyncio
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 2.044
Requires:	python3-modules >= 1:3.9
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Python Netlink library.

%prep
%setup -q -n %{module}-%{version}

%build
%py3_build_pyproject

%if %{with tests}
cd tests
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTEST_PLUGINS=pytest_asyncio \
PYTHONPATH=$(pwd)/.. \
%{__python3} -m pytest test_unit
cd ..
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install_pyproject

install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
cp -a examples/* $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
find $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version} -name '*.py' \
	| xargs sed -i '1s,^#!.*python[0-9.]*,#!%{__python3},'

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README* CHANGELOG.rst
%attr(755,root,root) %{_bindir}/dhcp-server-detector
%attr(755,root,root) %{_bindir}/pyroute2-decoder
%attr(755,root,root) %{_bindir}/pyroute2-dhcp-client
%attr(755,root,root) %{_bindir}/pyroute2-test-platform
%attr(755,root,root) %{_bindir}/ss2
%{py3_sitescriptdir}/%{module}
%{py3_sitescriptdir}/%{module}-%{version}.dist-info
%{_examplesdir}/%{name}-%{version}
