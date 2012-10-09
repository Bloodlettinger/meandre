mkdir -p ./cache/pil
cd ./cache/pil

wget --continue http://www.ijg.org/files/jpegsrc.v8c.tar.gz
tar xzf jpegsrc.v8c.tar.gz
cd jpeg-8c
./configure --prefix=${VIRTUAL_ENV} && make && make install
cd -

wget --continue http://zlib.net/zlib-1.2.7.tar.gz
tar xzf zlib-1.2.7.tar.gz
cd zlib-1.2.7
./configure --prefix=${VIRTUAL_ENV} && make && make install
cd -

wget --continue http://download.savannah.gnu.org/releases/freetype/freetype-2.4.10.tar.gz
tar xzf freetype-2.4.10.tar.gz
cd freetype-2.4.10
./configure --prefix=${VIRTUAL_ENV} && make && make install
cd -
