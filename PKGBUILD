# Maintainer: Natal Bumann wgtray@rcklt.ch
pkgname=wgtray
pkgver=1.4.0
pkgrel=1
pkgdesc="WireGuard system tray client for easy VPN switching"
arch=('any')
url="https://github.com/0xNatal/wgtray"
license=('GPL-3.0-or-later')
depends=(
    'python'
    'pyside6'
    'python-pyroute2'
    'python-tomlkit'
    'wireguard-tools'
    'polkit'
)
install=wgtray.install
source=("$pkgname-$pkgver.tar.gz::$url/archive/v$pkgver.tar.gz")
sha256sums=('SKIP')

package() {
    cd "$pkgname-$pkgver"
    make DESTDIR="$pkgdir" PREFIX=/usr install
}