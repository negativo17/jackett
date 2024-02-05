# mock configuration:
# - Requires network for running dotnet build

%global debug_package %{nil}
%define _build_id_links none

%global user %{name}
%global group %{name}

%global dotnet 6.0

%ifarch x86_64
%global rid x64
%endif

%ifarch aarch64
%global rid arm64
%endif

%ifarch armv7hl
%global rid arm
%endif

%if 0%{?fedora} >= 36
%global __requires_exclude ^liblttng-ust\\.so\\.0.*$
%endif

Name:           jackett
Version:        0.21.1682
Release:        1%{?dist}
Summary:        API Support for your favorite torrent trackers
License:        GPLv3
URL:            https://github.com/Jackett/Jackett

BuildArch:      x86_64 aarch64 armv7hl

Source0:        https://github.com/Jackett/Jackett/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
Source10:       %{name}.service
Source11:       %{name}.xml

BuildRequires:  dotnet-sdk-%{dotnet}
BuildRequires:  firewalld-filesystem
BuildRequires:  systemd
BuildRequires:  tar

Requires(post): curl
Requires:       firewalld-filesystem
Requires(post): firewalld-filesystem
Requires:       libmediainfo
Requires(pre):  shadow-utils
Requires:       libcurl

%description
Jackett works as a proxy server: it translates queries from apps (Sonarr,
Radarr, SickRage, CouchPotato, Mylar, DuckieTV, etc) into tracker-site-specific
http queries, parses the html response, then sends results back to the
requesting software. This allows for getting recent uploads (like RSS) and
performing searches. Jackett is a single repository of maintained indexer
scraping & translation logic - removing the burden from other apps.

%prep
%autosetup -p1 -n Jackett-%{version}

%build
pushd src
export DOTNET_CLI_TELEMETRY_OPTOUT=1
export DOTNET_SKIP_FIRST_TIME_EXPERIENCE=1
dotnet publish \
    --configuration Release \
    --framework net%{dotnet} \
    --output _output \
    --runtime linux-%{rid} \
    --self-contained \
    --verbosity normal \
    Jackett.Server
popd

%install
mkdir -p %{buildroot}%{_libdir}
mkdir -p %{buildroot}%{_prefix}/lib/firewalld/services/
mkdir -p %{buildroot}%{_unitdir}
mkdir -p %{buildroot}%{_sharedstatedir}/%{name}

cp -a src/_output %{buildroot}%{_libdir}/%{name}

install -m 0644 -p %{SOURCE10} %{buildroot}%{_unitdir}/%{name}.service
install -m 0644 -p %{SOURCE11} %{buildroot}%{_prefix}/lib/firewalld/services/%{name}.xml

find %{buildroot} -name "*.pdb" -delete

%pre
getent group %{group} >/dev/null || groupadd -r %{group}
getent passwd %{user} >/dev/null || \
    useradd -r -g %{group} -d %{_sharedstatedir}/%{name} -s /sbin/nologin \
    -c "%{name}" %{user}
exit 0

%post
%systemd_post %{name}.service
%firewalld_reload

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun_with_restart %{name}.service

%files
%license LICENSE
%doc README.md
%attr(750,%{user},%{group}) %{_sharedstatedir}/%{name}
%{_libdir}/%{name}
%{_prefix}/lib/firewalld/services/%{name}.xml
%{_unitdir}/%{name}.service

%changelog
* Mon Feb 05 2024 Simone Caronni <negativo17@gmail.com> - 0.21.1682-1
- Update to 0.21.1682.

* Wed Jan 31 2024 Simone Caronni <negativo17@gmail.com> - 0.21.1650-1
- Update to 0.21.1650.

* Thu Jan 25 2024 Simone Caronni <negativo17@gmail.com> - 0.21.1613-1
- Update to 0.21.1613.

* Wed Jan 17 2024 Simone Caronni <negativo17@gmail.com> - 0.21.1556-1
- Update to 0.21.1556.

* Fri Jan 12 2024 Simone Caronni <negativo17@gmail.com> - 0.21.1540-1
- Update to 0.21.1540.

* Mon Jan 08 2024 Simone Caronni <negativo17@gmail.com> - 0.21.1519-1
- Update to 0.21.1519.

* Sat Jan 06 2024 Simone Caronni <negativo17@gmail.com> - 0.21.1504-1
- Update to 0.21.1504.

* Thu Dec 28 2023 Simone Caronni <negativo17@gmail.com> - 0.21.1451-1
- Update to 0.21.1451.

* Thu Dec 21 2023 Simone Caronni <negativo17@gmail.com> - 0.21.1431-1
- Update to 0.21.1431.

* Tue Dec 12 2023 Simone Caronni <negativo17@gmail.com> - 0.21.1350-1
- Update to 0.21.1350.

* Mon Dec 04 2023 Simone Caronni <negativo17@gmail.com> - 0.21.1302-1
- Update to 0.21.1302.

* Sun Nov 26 2023 Simone Caronni <negativo17@gmail.com> - 0.21.1259-1
- Update to 0.21.1259.

* Wed Nov 15 2023 Simone Caronni <negativo17@gmail.com> - 0.21.1214-1
- Update to 0.21.1214.

* Mon Oct 30 2023 Simone Caronni <negativo17@gmail.com> - 0.21.1106-1
- Update to 0.21.1106.

* Tue Oct 17 2023 Simone Caronni <negativo17@gmail.com> - 0.21.1033-1
- Update to 0.21.1033.

* Tue Oct 03 2023 Simone Caronni <negativo17@gmail.com> - 0.21.950-1
- Update to 0.21.950.

* Wed Sep 27 2023 Simone Caronni <negativo17@gmail.com> - 0.21.919-1
- Update to 0.21.919.

* Fri Sep 22 2023 Simone Caronni <negativo17@gmail.com> - 0.21.866-1
- Update to 0.21.866.

* Mon Sep 04 2023 Simone Caronni <negativo17@gmail.com> - 0.21.741-1
- Update to 0.21.741.

* Sun Aug 27 2023 Simone Caronni <negativo17@gmail.com> - 0.21.705-1
- Update to 0.21.705.

* Wed Aug 23 2023 Simone Caronni <negativo17@gmail.com> - 0.21.687-1
- Update to 0.21.687.

* Sun Aug 20 2023 Simone Caronni <negativo17@gmail.com> - 0.21.671-1
- Update to 0.21.671.

* Mon Aug 07 2023 Simone Caronni <negativo17@gmail.com> - 0.21.589-1
- Update to 0.21.589.

* Mon Jul 17 2023 Simone Caronni <negativo17@gmail.com> - 0.21.481-1
- Update to 0.21.481.

* Tue Jul 11 2023 Simone Caronni <negativo17@gmail.com> - 0.21.455-1
- Update to 0.21.455.

* Sat Jul 01 2023 Simone Caronni <negativo17@gmail.com> - 0.21.356-1
- Update to 0.21.356.

* Thu Jun 22 2023 Simone Caronni <negativo17@gmail.com> - 0.21.275-1
- Update to 0.21.275.

* Mon Jun 12 2023 Simone Caronni <negativo17@gmail.com> - 0.21.203-1
- Update to 0.21.203.

* Tue Jun 06 2023 Simone Caronni <negativo17@gmail.com> - 0.21.157-1
- Update to 0.21.157.

* Tue May 23 2023 Simone Caronni <negativo17@gmail.com> - 0.21.17-1
- Update to 0.21.17.

* Tue May 16 2023 Simone Caronni <negativo17@gmail.com> - 0.20.4151-1
- Update to 0.20.4151.

* Fri Apr 28 2023 Simone Caronni <negativo17@gmail.com> - 0.20.4013-1
- Update to 0.20.4013.

* Mon Apr 10 2023 Simone Caronni <negativo17@gmail.com> - 0.20.3861-1
- Update to 0.20.3861.

* Sun Mar 26 2023 Simone Caronni <negativo17@gmail.com> - 0.20.3682-1
- Update to 0.20.3682.

* Mon Mar 20 2023 Simone Caronni <negativo17@gmail.com> - 0.20.3642-1
- Update to 0.20.3642.

* Tue Mar 07 2023 Simone Caronni <negativo17@gmail.com> - 0.20.3521-1
- Update to 0.20.3521.

* Thu Mar 02 2023 Simone Caronni <negativo17@gmail.com> - 0.20.3436-1
- Update to 0.20.3436.

* Fri Feb 24 2023 Simone Caronni <negativo17@gmail.com> - 0.20.3288-1
- Update to v0.20.3288

* Fri Feb 10 2023 Simone Caronni <negativo17@gmail.com> - 0.20.3017-1
- Update to 0.20.3017.

* Wed Feb 01 2023 Simone Caronni <negativo17@gmail.com> - 0.20.2814-1
- Update to 0.20.2814.

* Sun Jan 22 2023 Simone Caronni <negativo17@gmail.com> - 0.20.2687-1
- Update to 0.20.2687.

* Mon Jan 09 2023 Simone Caronni <negativo17@gmail.com> - 0.20.2603-1
- Update to 0.20.2603.

* Mon Dec 26 2022 Simone Caronni <negativo17@gmail.com> - 0.20.2437-1
- Update to 0.20.2437.

* Mon Dec 12 2022 Simone Caronni <negativo17@gmail.com> - 0.20.2365-1
- Update to 0.20.2365.

* Sun Dec 04 2022 Simone Caronni <negativo17@gmail.com> - 0.20.2319-1
- Update to 0.20.2319.

* Tue Nov 29 2022 Simone Caronni <negativo17@gmail.com> - 0.20.2304-1
- Update to 0.20.2304.

* Sun Nov 06 2022 Simone Caronni <negativo17@gmail.com> - 0.20.2210-1
- Update to 0.20.2210.

* Fri Oct 28 2022 Simone Caronni <negativo17@gmail.com> - 0.20.2163-2
- Add note about mock configuration.
- Trim changelog.

* Tue Oct 25 2022 Simone Caronni <negativo17@gmail.com> - 0.20.2163-1
- Update to 0.20.2163.

* Sun Sep 25 2022 Simone Caronni <negativo17@gmail.com> - 0.20.1992-1
- Update to 0.20.1992.

* Wed Sep 21 2022 Simone Caronni <negativo17@gmail.com> - 0.20.1915-1
- Update to 0.20.1915.

* Sun Sep 11 2022 Simone Caronni <negativo17@gmail.com> - 0.20.1885-1
- Update to 0.20.1885.

* Sun Sep 04 2022 Simone Caronni <negativo17@gmail.com> - 0.20.1830-1
- Update to 0.20.1830.

* Tue Aug 23 2022 Simone Caronni <negativo17@gmail.com> - 0.20.1790-1
- Update to 0.20.1790.

* Mon Aug 15 2022 Simone Caronni <negativo17@gmail.com> - 0.20.1698-1
- Update to 0.20.1698

* Tue Aug 09 2022 Simone Caronni <negativo17@gmail.com> - 0.20.1666-1
- Update to 0.20.1666.

* Fri Jul 22 2022 Simone Caronni <negativo17@gmail.com> - 0.20.1357-1
- Update to 0.20.1357.

* Thu Jun 16 2022 Simone Caronni <negativo17@gmail.com> - 0.20.1197-2
- Fix issues with LTTng Userspace Tracer library 2.13+.

* Thu Jun 16 2022 Simone Caronni <negativo17@gmail.com> - 0.20.1197-1
- Update to 0.20.1197.

* Wed Jun 01 2022 Simone Caronni <negativo17@gmail.com> - 0.20.1127-1
- Update to 0.20.1127.

* Wed May 18 2022 Simone Caronni <negativo17@gmail.com> - 0.20.1076-1
- Update to 0.20.1076.

* Mon May 16 2022 Simone Caronni <negativo17@gmail.com> - 0.20.1066-1
- Update to 0.20.1066.

* Sun Apr 17 2022 Simone Caronni <negativo17@gmail.com> - 0.20.892-1
- Update to 0.20.892.
