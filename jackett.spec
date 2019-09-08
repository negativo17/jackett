%global user %{name}
%global group %{name}

Name:           jackett
Version:        0.11.675
Release:        1%{?dist}
Summary:        API Support for your favorite torrent trackers
License:        GPLv3
URL:            https://github.com/Jackett/Jackett
BuildArch:      noarch

Source0:        https://github.com/Jackett/Jackett/releases/download/v%{version}/Jackett.Binaries.Mono.tar.gz#/Jackett.Binaries.Mono.%{version}.tar.gz
Source10:       %{name}.service
Source11:       %{name}.xml

BuildRequires:  firewalld-filesystem
BuildRequires:  systemd
BuildRequires:  tar

Requires(post): curl
Requires:       firewalld-filesystem
Requires(post): firewalld-filesystem
Requires:       mono-core
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
%autosetup -n Jackett
find . -type d -exec chmod 755 {} \;
find . -type f -exec chmod 644 {} \;

%install
mkdir -p %{buildroot}%{_datadir}/%{name}
mkdir -p %{buildroot}%{_prefix}/lib/firewalld/services/
mkdir -p %{buildroot}%{_unitdir}
mkdir -p %{buildroot}%{_sharedstatedir}/%{name}

cp -fr * %{buildroot}%{_datadir}/%{name}

install -m 0644 -p %{SOURCE10} %{buildroot}%{_unitdir}/%{name}.service
install -m 0644 -p %{SOURCE11} %{buildroot}%{_prefix}/lib/firewalld/services/%{name}.xml

find %{buildroot}%{_datadir}/%{name} -name "*.pdb" -delete

%pre
getent group %{group} >/dev/null || groupadd -r %{group}
getent passwd %{user} >/dev/null || \
    useradd -r -g %{group} -d %{_sharedstatedir}/%{name} -s /sbin/nologin \
    -c "%{name}" %{user}
exit 0

%post
%systemd_post %{name}.service
%firewalld_reload
curl -sS https://curl.haxx.se/ca/cacert.pem | cert-sync /dev/stdin > /dev/null

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun_with_restart %{name}.service

%files
%license LICENSE
%doc README.md
%attr(750,%{user},%{group}) %{_sharedstatedir}/%{name}
%{_datadir}/%{name}
%{_prefix}/lib/firewalld/services/%{name}.xml
%{_unitdir}/%{name}.service

%changelog
* Sun Sep 08 2019 Simone Caronni <negativo17@gmail.com> - 0.11.675-1
- Update to 0.11.675.

* Tue Jul 09 2019 Simone Caronni <negativo17@gmail.com> - 0.11.476-1
- Update to 0.11.476.

* Sun Jun 16 2019 Simone Caronni <negativo17@gmail.com> - 0.11.427-1
- Update to 0.11.427.

* Mon May 27 2019 Simone Caronni <negativo17@gmail.com> - 0.11.379-1
- Update to 0.11.379.

* Mon May 06 2019 Simone Caronni <negativo17@gmail.com> - 0.11.294-1
- Update to 0.11.294.

* Tue Apr 30 2019 Simone Caronni <negativo17@gmail.com> - 0.11.259-1
- Update to 0.11.259.

* Mon Apr 01 2019 Simone Caronni <negativo17@gmail.com> - 0.11.173-1
- Update to 0.11.173.

* Sun Mar 10 2019 Simone Caronni <negativo17@gmail.com> - 0.11.2-1
- Update to 0.11.2.

* Sat Feb 23 2019 Simone Caronni <negativo17@gmail.com> - 0.10.828-1
- Update to 0.10.828.

* Fri Feb 08 2019 Simone Caronni <negativo17@gmail.com> - 0.10.723-1
- Update to v0.10.723.

* Thu Jan 24 2019 Simone Caronni <negativo17@gmail.com> - 0.10.649-1
- Update to 0.10.649.

* Sat Jan 12 2019 Simone Caronni <negativo17@gmail.com> - 0.10.611-1
- Update to 0.10.611.

* Sat Jan 05 2019 Simone Caronni <negativo17@gmail.com> - 0.10.579-1
- Update to version 0.10.579.

* Tue Dec 18 2018 Simone Caronni <negativo17@gmail.com> - 0.10.523-1
- Update to 0.10.523.

* Fri Dec 14 2018 Simone Caronni <negativo17@gmail.com> - 0.10.511-1
- Update to 0.10.511.

* Wed Nov 28 2018 Simone Caronni <negativo17@gmail.com> - 0.10.471-1
- First build.
