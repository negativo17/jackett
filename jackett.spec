%global user %{name}
%global group %{name}

Name:           jackett
Version:        0.18.364
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

* Sat Dec 26 2020 Simone Caronni <negativo17@gmail.com> - 0.17.159-1
- Update to 0.17.159.

* Tue Dec 08 2020 Simone Caronni <negativo17@gmail.com> - 0.17.3-1
- Update to 0.17.3.

* Sat Nov 21 2020 Simone Caronni <negativo17@gmail.com> - 0.16.2215-1
- Update to 0.16.2215.

* Tue Nov 17 2020 Simone Caronni <negativo17@gmail.com> - 0.16.2173-1
- Update to 0.16.2173.

* Thu Nov 05 2020 Simone Caronni <negativo17@gmail.com> - 0.16.2076-1
- Update to 0.16.2076.

* Thu Oct 29 2020 Simone Caronni <negativo17@gmail.com> - 0.16.1933-1
- Update to 0.16.1933.

* Fri Oct 16 2020 Simone Caronni <negativo17@gmail.com> - 0.16.1757-1
- Update to 0.16.1757.

* Tue Oct 06 2020 Simone Caronni <negativo17@gmail.com> - 0.16.1600-1
- Update to 0.16.1600.

* Tue Aug 25 2020 Simone Caronni <negativo17@gmail.com> - 0.16.1038-1
- Update to 0.16.1038.

* Sun Aug 16 2020 Simone Caronni <negativo17@gmail.com> - 0.16.1002-1
- Update to 0.16.1002.

* Tue Jul 21 2020 Simone Caronni <negativo17@gmail.com> - 0.16.865-1
- Update to 0.16.865.

* Tue Jul 14 2020 Simone Caronni <negativo17@gmail.com> - 0.16.838-1
- Update to 0.16.838.

* Tue Jun 30 2020 Simone Caronni <negativo17@gmail.com> - 0.16.779-1
- Update to 0.16.779.

* Sun Jun 07 2020 Simone Caronni <negativo17@gmail.com> - 0.16.640-1
- Update to 0.16.640.

* Tue Jun 02 2020 Simone Caronni <negativo17@gmail.com> - 0.16.598-1
- Update to 0.16.598.

* Fri May 22 2020 Simone Caronni <negativo17@gmail.com> - 0.16.515-1
- Update to 0.16.515.

* Wed Apr 01 2020 Simone Caronni <negativo17@gmail.com> - 0.14.376-1
- Update to 0.14.376.

* Thu Feb 20 2020 Simone Caronni <negativo17@gmail.com> - 0.13.144-1
- Update to 0.13.144.

* Thu Feb 06 2020 Simone Caronni <negativo17@gmail.com> - 0.12.1701-1
- Update to 0.12.1701.

* Sat Dec 21 2019 Simone Caronni <negativo17@gmail.com> - 0.12.1323-1
- Update to 0.12.1323.

* Sun Dec 01 2019 Simone Caronni <negativo17@gmail.com> - 0.12.1053-1
- Update to 0.12.1053.

* Wed Oct 02 2019 Simone Caronni <negativo17@gmail.com> - 0.11.761-1
- Update to 0.11.761.

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
