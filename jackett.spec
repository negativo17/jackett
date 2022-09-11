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
Version:        0.20.1885
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

Obsoletes:      %{name} < %{version}-%{release}

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

* Thu Mar 24 2022 Simone Caronni <negativo17@gmail.com> - 0.20.756-1
- Update to 0.20.756.
- Trim changelog.

* Fri Mar 11 2022 Simone Caronni <negativo17@gmail.com> - 0.20.689-1
- Update to 0.20.689.

* Thu Mar 10 2022 Simone Caronni <negativo17@gmail.com> - 0.20.684-1
- Update to 0.20.684.

* Sun Mar 06 2022 Simone Caronni <negativo17@gmail.com> - 0.20.667-1
- Update to 0.20.667.

* Tue Mar 01 2022 Simone Caronni <negativo17@gmail.com> - 0.20.654-1
- Update to 0.20.654.

* Mon Feb 28 2022 Simone Caronni <negativo17@gmail.com> - 0.20.643-1
- Update to 0.20.643.

* Sat Feb 12 2022 Simone Caronni <negativo17@gmail.com> - 0.20.555-1
- Update to 0.20.555.
- Fix building and remove old Mono migration leftover.

* Thu Dec 16 2021 Simone Caronni <negativo17@gmail.com> - 0.20.172-1
- Update to 0.20.172.

* Sat Oct 23 2021 Simone Caronni <negativo17@gmail.com> - 0.19.34-1
- Update to 0.19.34.
- Switch to .Net source builds.

* Tue Jul 20 2021 Simone Caronni <negativo17@gmail.com> - 0.18.455-1
- Update to 0.18.455.

* Sun Jun 20 2021 Simone Caronni <negativo17@gmail.com> - 0.18.364-1
- Update to 0.18.364.

* Mon Jun 07 2021 Simone Caronni <negativo17@gmail.com> - 0.18.259-1
- Update to version 0.18.259.

* Sun May 23 2021 Simone Caronni <negativo17@gmail.com> - 0.18.106-1
- Update to 0.18.106.

* Thu Feb 11 2021 Simone Caronni <negativo17@gmail.com> - 0.17.496-1
- Update to 0.17.496.

* Tue Feb 02 2021 Simone Caronni <negativo17@gmail.com> - 0.17.449-1
- Update to 0.17.449.

* Thu Jan 21 2021 Simone Caronni <negativo17@gmail.com> - 0.17.337-1
- Update to 0.17.337.

* Thu Jan  7 2021 Simone Caronni <negativo17@gmail.com> - 0.17.197-1
- Update to 0.17.197.
