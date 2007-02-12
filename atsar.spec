# TODO
# - cron errors:
#awk: line 36: regular expression compile failed (bad class -- [], [^] or [)
#[\[
#awk: line 36: syntax error at or near ]
#awk: line 87: regular expression compile failed (bad class -- [], [^] or [)
#[\[
#awk: line 87: syntax error at or near ]
Summary:	AT Computing System Activity Report - a sar clone for Linux
Summary(pl.UTF-8):   Atsar - odpowiednik uniksowego programu sar dla Linuksa
Name:		atsar
Version:	1.7
Release:	3
License:	GPL
Group:		Daemons
Source0:	ftp://ftp.atcomputing.nl/pub/tools/linux/%{name}_linux-%{version}.tar.gz
# Source0-md5:	2aa73a4a99dd176a02c5336889d8b028
Source1:	%{name}.init
Source2:	%{name}.cron
Patch0:		%{name}-runfrompath.patch
URL:		ftp://ftp.atcomputing.nl/pub/tools/linux/
BuildRequires:	rpmbuild(macros) >= 1.268
Requires(post,preun):	/sbin/chkconfig
Requires:	rc-scripts
ExclusiveOS:	Linux
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Atsar can be used to measure the load on the most relevant system
resources, such as CPU, disk, memory and network. Long-term analysis
can be done via cron, by maintaining log files with statistical
information. Short-term analysis can be done by starting the command
atsar with an interval and a number of samples. The current version of
atsar gathers statistics about the utilization of CPU's, disks, memory
and swap, serial lines and network (TCP/IP v4 and v6).

%description -l pl.UTF-8
Atsar przydaje się do pomiarów obciążenia najbardziej istotnych
zasobów systemowych, takich jak procesor, dysk, pamięć i sieć. Dzięki
połączeniu z cronem możliwe jest otrzymanie logów z informacją
statystyczną, przydatnych do długoterminowych analiz. Krótkoterminowe
analizy mogą być wykonywane przez bezpośrednie uruchomienie programu
atsar z podaniem parametrów takich jak ilość próbek i odstęp czasowy
między próbkami. Aktualna wersja programu atsar gromadzi informacje o
wykorzystaniu procesora, dysków, pamięci (operacyjnej i wymiany),
łączy szeregowych i sieci (TCP/IP v4 i v6).

%prep
%setup -q -n %{name}_linux-%{version}
%patch0 -p1

%build
for r in atsar atsadc \*.o ;do
	find -iname $r -exec rm -v {} \;
done
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_mandir}/man1,/var/log/atsar} \
	$RPM_BUILD_ROOT/etc/{rc.d/init.d,cron.d}

for s in scripts/atsa1 atsar_linux.conf ;do
	cat $s | sed -e 's|usr/local/bin|%{_bindir}|g' > sed.$$
	mv -f sed.$$ $s
done

install atsar/atsar atsadc/atsadc scripts/atsa1	\
	scripts/atsaftp scripts/atsahttp $RPM_BUILD_ROOT%{_bindir}
install man/* $RPM_BUILD_ROOT%{_mandir}/man1

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/atsar
install %{SOURCE2} $RPM_BUILD_ROOT/etc/cron.d/atsar
install atsar_linux.conf $RPM_BUILD_ROOT%{_sysconfdir}/atsar.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
%{_bindir}/atsa1
%service atsar restart

%preun
if [ "$1" = "0" ]; then
	%service atsar stop
	/sbin/chkconfig --del atsar
fi

%files
%defattr(644,root,root,755)
%doc README
%attr(755,root,root) %{_bindir}/atsar
%attr(755,root,root) %{_bindir}/atsadc
%attr(755,root,root) %{_bindir}/atsa1
%attr(755,root,root) %{_bindir}/atsaftp
%attr(755,root,root) %{_bindir}/atsahttp
%{_mandir}/man1/atsar.1*
%{_mandir}/man1/atsadc.1*
%dir /var/log/atsar
%attr(754,root,root) %config /etc/rc.d/init.d/atsar
%config(noreplace) %verify(not md5 mtime size) /etc/cron.d/atsar
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/atsar.conf
