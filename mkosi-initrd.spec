%define date 20220914

Summary:	Generator for initrd images using distro packages
Name:		mkosi-initrd
Version:	0
Release:	0.%{date}.1
License:	LGPL2+
# git clone https://github.com/systemd/mkosi-initrd.git -b main
# cd mkosi-initrd && git archive --prefix=mkosi-initrd-0.$(date +%Y%m%d)/ --format=tar origin/main | xz -9ef > ../mkosi-initrd-0.$(date +%Y%m%d).tar.xz
Source0:	https://github.com/systemd/mkosi-initrd/archive/%{name}-%{version}.%{date}.tar.xz
Source1:	openmandriva.mkosi
BuildArch:	noarch
Requires:	mkosi >= 13
Requires:	rpm
Requires:	dnf
Requires:	dnf-command(download)
Requires:	cpio
Requires:	kmod
Requires:	systemd
Requires:	python3dist(xattr)

%description
%{summary}.

%prep
%autosetup -n %{name}-%{version}.%{date} -p1

%build

%install
mkdir -p %{buildroot}%{_sysconfdir}/kernel
printf '%s\n' 'initrd_generator=mkosi-initrd' >> %{buildroot}%{_sysconfdir}/kernel/install.conf
mkdir -p %{buildroot}%{_sysconfdir}/kernel/install.d
ln -s /dev/null %{buildroot}%{_sysconfdir}/kernel/install.d/50-dracut.install

sed -i -e 's/fedora.mkosi/mkosi.default/g' kernel-install/50-mkosi-initrd.install

install -Dt %{buildroot}%{_prefix}/lib/mkosi-initrd mkosi.finalize
install -Dt %{buildroot}%{_prefix}/lib/mkosi-initrd -m 0644 %{SOURCE1}
install -Dt %{buildroot}%{_prefix}/lib/kernel/install.d/ kernel-install/50-mkosi-initrd.install

sln openmandriva.mkosi %{buildroot}%{_prefix}/lib/mkosi-initrd/mkosi.default

%files
%doc README.md
%{_sysconfdir}/kernel/install.d/50-dracut.install
%{_sysconfdir}/kernel/install.conf
%dir %{_prefix}/lib/mkosi-initrd
%{_prefix}/lib/mkosi-initrd/mkosi.finalize
%{_prefix}/lib/mkosi-initrd/openmandriva.mkosi
%{_prefix}/lib/mkosi-initrd/mkosi.default
%{_prefix}/lib/kernel/install.d/50-mkosi-initrd.install
