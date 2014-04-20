set -e
git add -A .
git commit -m "$1"
git pull
git push -u origin master
echo "yfzhao123@gmail.com\nZHAOyufei816" | appcfg.py update .