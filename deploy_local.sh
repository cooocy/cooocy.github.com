#!/usr/bin/sh
hexo clean
git pull
hexo g

python3 baidu_sitemap_converter.py

rm -r ~/apps/web/www
mv public/ ~/apps/web/www/
cp baidu_verify_codeva-zMZTM1JNUX.html ~/apps/web/www/
cp google3c96eac445b3392c.html ~/apps/web/www/
cp BingSiteAuth.xml ~/apps/web/www/

hexo clean
