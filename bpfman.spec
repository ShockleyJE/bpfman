# Generated by rust2rpm 25
%bcond_without check

%global crate bpfman
%global commit GITSHA
%global shortcommit GITSHORTSHA
%global base_version 0.4.0
%global prerelease dev
%global package_version %{base_version}%{?prerelease:~%{prerelease}}
%global upstream_version %{base_version}%{?prerelease:~%{prerelease}}

Name:           bpfman
Version:        %{package_version}
Release:        %autorelease
Summary:        An eBPF program manager

SourceLicense:  Apache-2.0
# (Apache-2.0 OR MIT) AND BSD-3-Clause
# (MIT OR Apache-2.0) AND Unicode-DFS-2016
# 0BSD OR MIT OR Apache-2.0
# Apache-2.0
# Apache-2.0 OR BSL-1.0
# Apache-2.0 OR ISC OR MIT
# Apache-2.0 OR MIT
# Apache-2.0 WITH LLVM-exception OR Apache-2.0 OR MIT
# BSD-2-Clause OR Apache-2.0 OR MIT
# BSD-3-Clause
# ISC
# MIT
# MIT AND BSD-3-Clause
# MIT OR Apache-2.0
# MIT OR Apache-2.0 OR BSD-1-Clause
# MIT OR Apache-2.0 OR Zlib
# MIT OR Zlib OR Apache-2.0
# MPL-2.0
# Unlicense OR MIT
# Zlib OR Apache-2.0 OR MIT
License: Apache-2.0 AND AND Unicode-DFS-2016 AND BSD-3-Clause AND ISC AND MIT AND MPL-2.0
# LICENSE.dependencies contains a full license breakdown

URL:            https://bpfman.io
Source0:         https://github.com/bpfman/bpfman/archive/%{commit}/%{name}-%{shortcommit}.tar.gz
# The vendor tarball is created using cargo-vendor-filterer to remove Windows
# related files (https://github.com/coreos/cargo-vendor-filterer)
#   cargo vendor-filterer --format tar.gz --prefix vendor bpfman-bpfman-vendor.tar.gz
Source1:         bpfman-bpfman-vendor.tar.gz

BuildRequires:  cargo-rpm-macros >= 25
BuildRequires:  systemd-rpm-macros

# TODO: Generate Provides for all of the vendored dependencies

%global _description %{expand:
An eBPF Program Manager.}

%description %{_description}

%prep
%autosetup %{name}-${version_no_tilde} -n bpfman-v0.3.1 -p1 -a1

# Source1 is vendored dependencies
tar -xoaf %{SOURCE1}
# Replace the Git Dependency on Aya with a path dependency
# TODO: This will be removed when we do an upstream Aya release
sed -i 's#aya = { git = "https://github.com/aya-rs/aya", branch = "main" }#aya = { path = "vendor/aya" }#g' Cargo.toml
# Let the macros setup Cargo.toml to use vendored sources
%cargo_prep -v vendor
%cargo_license_summary
%cargo_license

%build
%cargo_build
%{cargo_license_summary}
%{cargo_license} > LICENSE.dependencies
%{cargo_vendor_manifest}

%install
install -Dpm 0755 \
    -t %{buildroot}%{_sbindir} \
    ./target/release/bpfman

%post
%systemd_post scripts/bpfman.service

%preun
%systemd_preun scripts/bpfman.service

%postun
%systemd_postun_with_restart scripts/bpfman.service

%files
%license LICENSE-APACHE
%license LICENSE-BSD2
%license LICENSE-GPL2
%license LICENSE.dependencies
%license cargo-vendor.txt
%doc CODE_OF_CONDUCT.md
%doc CONTRIBUTING.md
%doc GOVERNANCE.md
%doc MAINTAINERS.md
%doc MEETINGS.md
%doc README.md
%doc RELEASE.md
%doc REVIEWING.md
%doc SECURITY.md
%{_sbindir}/bpfman

%changelog
%autochangelog
