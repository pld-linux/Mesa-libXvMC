#
# Conditional build:
%bcond_without	gallium		# gallium drivers
%bcond_without	gallium_nouveau	# gallium nouveau driver
%bcond_without	gallium_radeon	# gallium radeon drivers
%bcond_without	radv		# radeon Vulkan driver
%bcond_with	sse2		# SSE2 instructions
%bcond_with	lm_sensors	# HUD lm_sensors support
%bcond_with	tests		# tests

# other packages
%define		libdrm_ver		2.4.110
%define		dri2proto_ver		2.8
%define		glproto_ver		1.4.14
%define		zlib_ver		1.2.8
%define		llvm_ver		11.0.0
%define		gcc_ver 		6:4.8.0

%if %{without gallium}
%undefine	with_gallium_nouveau
%undefine	with_gallium_radeon
%endif

%ifarch %{x86_with_sse2}
%define		with_sse2	1
%endif

Summary:	Free OpenGL implementation - XvMC drivers
Summary(pl.UTF-8):	Wolnodostępna implementacja standardu OpenGL - sterowniki XvMC
Name:		Mesa-libXvMC
# 22.2.x were the last containing libXvMC drivers
Version:	22.2.4
Release:	1
License:	MIT (core) and others - see license.html file
Group:		X11/Libraries
Source0:	https://archive.mesa3d.org/mesa-%{version}.tar.xz
# Source0-md5:	a258a3d590d76bc1ff89a204f063e3b8
URL:		https://www.mesa3d.org/
BuildRequires:	bison > 2.3
BuildRequires:	elfutils-devel
BuildRequires:	expat-devel >= 1.95
BuildRequires:	flex
BuildRequires:	gcc >= %{gcc_ver}
%ifarch %{armv6}
BuildRequires:	libatomic-devel
%endif
BuildRequires:	libdrm-devel >= %{libdrm_ver}
BuildRequires:	libselinux-devel
BuildRequires:	libstdc++-devel >= %{gcc_ver}
BuildRequires:	libunwind-devel
BuildRequires:	libxcb-devel >= 1.13
%{?with_gallium:BuildRequires:	llvm-devel >= %{llvm_ver}}
%{?with_radv:BuildRequires:	llvm-devel >= %{llvm_ver}}
BuildRequires:	meson >= 0.53
BuildRequires:	ninja >= 1.5
BuildRequires:	pkgconfig
BuildRequires:	pkgconfig(talloc) >= 2.0.1
BuildRequires:	pkgconfig(xcb-dri2) >= 1.8
BuildRequires:	pkgconfig(xcb-dri3) >= 1.13
BuildRequires:	pkgconfig(xcb-glx) >= 1.8.1
BuildRequires:	pkgconfig(xcb-present) >= 1.13
BuildRequires:	pkgconfig(xcb-randr) >= 1.12
BuildRequires:	python3 >= 1:3.2
BuildRequires:	python3-Mako >= 0.8.0
BuildRequires:	rpmbuild(macros) >= 2.007
BuildRequires:	sed >= 4.0
BuildRequires:	tar >= 1:1.22
BuildRequires:	udev-devel
BuildRequires:	xorg-lib-libX11-devel
BuildRequires:	xorg-lib-libXext-devel >= 1.0.5
BuildRequires:	xorg-lib-libXfixes-devel >= 2.0
BuildRequires:	xorg-lib-libXrandr-devel >= 1.3
BuildRequires:	xorg-lib-libXv-devel
BuildRequires:	xorg-lib-libXvMC-devel >= 1.0.6
BuildRequires:	xorg-lib-libXxf86vm-devel
BuildRequires:	xorg-lib-libxshmfence-devel >= 1.1
BuildRequires:	xorg-proto-dri2proto-devel >= %{dri2proto_ver}
BuildRequires:	xorg-proto-glproto-devel >= %{glproto_ver}
%if %{with gallium}
%{?with_lm_sensors:BuildRequires:	lm_sensors-devel}
BuildRequires:	xz
%endif
BuildRequires:	zlib-devel >= %{zlib_ver}
BuildRequires:	zstd-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Mesa is a 3-D graphics library with an API which is very similar to
that of OpenGL(R). To the extent that Mesa utilizes the OpenGL command
syntax or state machine, it is being used with authorization from
Silicon Graphics, Inc. However, the author does not possess an OpenGL
license from SGI, and makes no claim that Mesa is in any way a
compatible replacement for OpenGL or associated with SGI.

%description -l pl.UTF-8
Mesa jest biblioteką grafiki 3D z API bardzo podobnym do OpenGL(R). Do
tego stopnia, że Mesa używa składni i automatu OpenGL jest używana z
autoryzacją Silicon Graphics, Inc. Jednak autor nie posiada licencji
OpenGL od SGI i nie twierdzi, że Mesa jest kompatybilnym zamiennikiem
OpenGL ani powiązana z SGI.

%package nouveau
Summary:	Mesa implementation of XvMC API for NVidia adapters
Summary(pl.UTF-8):	Implementacja Mesa API XvMC dla kart NVidia
License:	MIT
Group:		Libraries
Requires:	libdrm >= %{libdrm_ver}
Requires:	xorg-lib-libXvMC >= 1.0.6
Requires:	zlib >= %{zlib_ver}
Conflicts:	Mesa-libXvMC

%description nouveau
Mesa implementation of XvMC API for NVidia adapters (NV40-NV96, NVa0).

%description nouveau -l pl.UTF-8
Implementacja Mesa API XvMC dla kart NVidia (NV40-NV96, NVa0).

%package r600
Summary:	Mesa implementation of XvMC API for ATI Radeon R600 series adapters
Summary(pl.UTF-8):	Implementacja Mesa API XvMC dla kart ATI Radeon z serii R600
License:	MIT
Group:		Libraries
Requires:	libdrm >= %{libdrm_ver}
Requires:	xorg-lib-libXvMC >= 1.0.6
Requires:	zlib >= %{zlib_ver}
Conflicts:	Mesa-libXvMC

%description r600
Mesa implementation of XvMC API for ATI Radeon adapters based on
R600/R700 chips.

%description r600 -l pl.UTF-8
Implementacja Mesa API XvMC dla kart ATI Radeon opartych na układach
R600/R700.

%prep
%setup -q -n mesa-%{version}

%build
gallium_drivers="
%if %{with gallium_radeon}
r600
%endif
%if %{with gallium_nouveau}
nouveau
%endif
"
gallium_drivers=$(echo $gallium_drivers | xargs | tr ' ' ',')

vulkan_drivers="
%{?with_radv:amd}
%ifarch %{ix86} %{x8664} x32
intel
%endif
"

vulkan_drivers=$(echo $vulkan_drivers | xargs | tr ' ' ',')

%meson build \
	-Dplatforms=x11 \
	-Ddri3=enabled \
	-Ddri-drivers-path=%{_libdir}/xorg/modules/dri \
	-Degl=disabled \
	-Dgallium-drivers=${gallium_drivers} \
	-Dgallium-nine=false \
	-Dgallium-omx=disabled \
	-Dgallium-opencl=disabled \
	-Dgallium-va=disabled \
	-Dgallium-vdpau=disabled \
	-Dgallium-xvmc=enabled \
	-Dgallium-xa=disabled \
	-Dgbm=disabled \
	-Dglvnd=false \
	-Dglx=disabled \
	-Dlibunwind=enabled \
	-Dlmsensors=%{?with_lm_sensors:enabled}%{!?with_lm_sensors:disabled} \
	-Dopengl=false \
	-Dselinux=true \
	-Dsse2=%{__true_false sse2} \
	-Dvideo-codecs=h264dec,h264enc,h265dec,h265enc,vc1dec \
	-Dvulkan-drivers=${vulkan_drivers} \
	-Dvulkan-icd-dir=/usr/share/vulkan/icd.d

%ninja_build -C build

%{?with_tests:%ninja_test -C build}

%install
rm -rf $RPM_BUILD_ROOT

%ninja_install -C build

# leave only XvMC drivers
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libvulkan_intel.so
%if %{with radv}
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libvulkan_radeon.so
%endif
%{__rm} -r $RPM_BUILD_ROOT%{_datadir}/{drirc.d,vulkan}

%clean
rm -rf $RPM_BUILD_ROOT

%post	nouveau -p /sbin/ldconfig
%postun	nouveau -p /sbin/ldconfig

%post	r600 -p /sbin/ldconfig
%postun	r600 -p /sbin/ldconfig

%if %{with gallium_nouveau}
%files nouveau
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libXvMCnouveau.so.1.*.*
%attr(755,root,root) %ghost %{_libdir}/libXvMCnouveau.so.1
%attr(755,root,root) %{_libdir}/libXvMCnouveau.so
%endif

%if %{with gallium_radeon}
%files r600
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libXvMCr600.so.1.*.*
%attr(755,root,root) %ghost %{_libdir}/libXvMCr600.so.1
%attr(755,root,root) %{_libdir}/libXvMCr600.so
%endif
